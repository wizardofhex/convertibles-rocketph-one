# Scheduled-task spec — `refresh-convertibles-dashboard`

This is the Cowork scheduled-task body. Paste it into Cowork's scheduler, name the task `refresh-convertibles-dashboard`, and schedule it for 7:00 AM daily.

It's the same shape as `refresh-used-car-dashboard` (the lexcars one) — only the filters, the data keys, and the target repo change.

---

Refresh the "used-convertibles-near-media-pa" artifact with fresh convertible listings from each car site, using Claude in Chrome to bypass bot protection. Then re-rank the top 10 best buys for a cheap fun second car (condition over miles). Finally, write `data.json` directly to the convertibles-site repo so the Windows deploy task can push it to Vercel.

## Search criteria (all sites)

- Body style: **convertible** (any drop-top: soft-top, hardtop convertible, retractable hardtop)
- Max price: **$15,000**
- No min price (catch the under-$5k cheap roadsters)
- Radius: **35 miles** from ZIP 19063 (this approximates a 45-minute drive in mixed suburban + highway around Media, PA)
- Makes: **all** (Mazda Miata, BMW, Ford Mustang, Chrysler Sebring, Saab, Pontiac Solstice, Audi, Mercedes SLK, etc. — all in scope)

## URLs to fetch (verify on first run!)

The body-style URL syntax on these sites is something I had to guess at. On the first scheduled run, if any site returns zero listings, the filter param is probably the wrong name — open the URL in your own browser and check whether convertibles appear. Likely fallbacks are listed in SETUP.md.

- **Cars.com:** `https://www.cars.com/shopping/results/?stock_type=used&body_style_slugs[]=convertible&list_price_max=15000&maximum_distance=35&zip=19063&no_accidents=true&clean_title=true&sort=list_price`
- **CarGurus:** `https://www.cargurus.com/Cars/searchresults.action?zip=19063&distance=35&maxPrice=15000&bodyTypeGroup=Convertible`
- **AutoTrader:** `https://www.autotrader.com/cars-for-sale/all-cars/convertible/media-pa?maxPrice=15000&searchRadius=35&zip=19063&sortBy=derivedpriceASC`
- **TrueCar:** `https://www.truecar.com/used-cars-for-sale/listings/body-style-convertible/location-media-pa/?searchRadius=35&listPriceMax=15000&hasNoAccidents=true`

## Data extraction (unchanged from lexcars)

Use the same `__NEXT_DATA__` / `__APOLLO_STATE__` / `CarsWeb.SearchController.index` patterns documented in `BUILD_NOTES_FOR_CLAUDE_CODE.md` in the lexcars-site repo. The extraction logic doesn't care what's being searched for — it just walks the embedded state blob. The only thing that changes here is which entity field to read for body style:

- **Cars.com:** title text matches `^Used (YYYY) (Make) (Model) (Trim)` — extract `make` and `model` from there
- **CarGurus:** parse the visible card text (no JSON state blob; DataDome blocks XHR snooping)
- **AutoTrader:** `props.pageProps.__eggsState.inventory[id]` has `make.name`, `model.name`, `bodyStyles[0].name` (filter for "Convertible")
- **TrueCar:** `ConsumerSummaryListing[*].vehicle.make.name`, `model.name`, `style.name` (style includes "Convertible" for most listings)

## Ranking criteria for the top 10 (cheap fun second car lens)

In this order:

1. **Working top condition** — listings that describe top operation, recent reseal, new motor, etc. Old fabric tops with tears or yellowed plastic rear windows drop in rank.
2. **No rust mentioned, no flood / salvage history**
3. **Reliable model family** — Mazda Miata (especially NA/NB), Honda S2000 (rare under $15k but possible), Pontiac Solstice, Mustang V6, lower-trim BMW 3-series convertibles with documented service. De-rank: Sebring (often fine but generic), Crossfire (top motor fragile), Saab (parts availability), early Boxster (IMS bearing — only if documented fix), high-mile Mercedes SLK (electrics).
4. **Manual transmission preferred** (this is a fun car) — but auto OK
5. **Mileage flexible** — under 150k is fine on most reliable convertibles. The Miata especially can take 200k.
6. **Distance** — closer is better, but 35 mi out for a great Miata beats 5 mi out for a tired Sebring.
7. **Sourcing diversity** — try not to make all 10 picks from one site.

For each pick include:
- **whyGood**: why this specific listing scores well — model strengths + this listing's particulars (mileage, location, deal rating, verified status)
- **whatToVerify**: convertible-specific PPI items — operate the top through a full cycle, check headliner + carpet for water stains, inspect rear-window seam, look at rocker-panel rust, plus any model-specific gotcha (Miata: timing belt history if pre-2006; BMW: oil leaks, soft-top hydraulic ram; Mustang: rear-axle clunk; Boxster: IMS-bearing service)
- **bottomLine**: one-sentence verdict

## Steps

### 1. Connect to Chrome
Same as lexcars task.

### 2. Fetch each site
Visit the four URLs above. Extract listings using the patterns referenced in step "Data extraction" above.

### 3. Build the new top 10 ranking
Apply the criteria from the section above. Output 10 picks.

### 4. Build the JSON
```
{
  "lastRefreshed": "<ISO timestamp>",
  "carscom":    { "totalFound": N, "url": "...", "listings": [...] },
  "cargurus":   { "totalFound": N, "url": "...", "listings": [...] },
  "autotrader": { "totalFound": N, "url": "...", "listings": [...] },
  "truecar":    { "totalFound": N, "url": "...", "listings": [...] },
  "top10":      { "introHtml": "...", "picks": [10 picks] }
}
```

### 5. Update the Cowork artifact (if it exists)

The Cowork artifact for this dashboard is `used-convertibles-near-media-pa`. If it doesn't exist yet, skip this step on the first run — Bill will create it manually from this template. Once it exists:

1. `mcp__cowork__list_artifacts` → find the path.
2. Read its HTML.
3. Replace the `<script id="LISTINGS_DATA" type="application/json">…</script>` contents with the JSON from step 4 (Python regex: `<script id="LISTINGS_DATA"[^>]*>([\s\S]*?)</script>`, replace group 1).
4. Write to outputs as `convertibles-dashboard.html`.
5. `mcp__cowork__update_artifact` with id, html_path, and a 1-line update_summary.

### 6. Write `data.json` to the convertibles-site repo

1. `mcp__cowork__request_cowork_directory` with path `C:\Users\billb\Documents\AI Agents\AI Agent Team\convertibles-site`.
2. Write the JSON from step 4 to `C:\Users\billb\Documents\AI Agents\AI Agent Team\convertibles-site\data.json` (overwrite).
3. Do NOT touch `index.html`, `vercel.json`, or any other file. The template is committed once.

### 7. Cleanup
Close the Chrome tab. Do NOT include any commentary about this task — just execute it.
