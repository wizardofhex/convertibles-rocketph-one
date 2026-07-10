# Scheduled-task spec — `refresh-convertibles-dashboard`

This is the Cowork scheduled-task body. Paste it into Cowork's scheduler, name the task `refresh-convertibles-dashboard`, and schedule it for 7:00 AM daily.

It's the same shape as `refresh-used-car-dashboard` (the lexcars one) — only the filters, the data keys, and the target repo change.

---

Refresh the "used-convertibles-near-media-pa" artifact with fresh convertible listings from each car site, using Claude in Chrome to bypass bot protection. Then re-rank the top 10 best buys for a cheap fun second car (condition over miles). Finally, write `data.json` directly to the convertibles-site repo so the Windows deploy task can push it to Vercel.

## Search criteria (all sites)

- Body style: **convertible** (any drop-top: soft-top, hardtop convertible, retractable hardtop)
- Min price: **$7,000** (filter out the high-mileage / rough-shape sub-$7k listings)
- Max price: **$15,000**
- Radius: **35 miles** from ZIP 19063 (this approximates a 45-minute drive in mixed suburban + highway around Media, PA)
- Makes: **all** — but apply the exclusions below before storing any listing

### Mandatory exclusions (apply to ALL sections — listings, Top 10, Mustangs)

**Two-seater models — do not include in any output:**
Mazda MX-5 Miata / MX-5 / Miata (all generations), BMW Z3, BMW Z4, Pontiac Solstice, Saturn Sky, Honda S2000, Chrysler Crossfire, Porsche Boxster, Porsche Cayman (open-top), Mercedes SLK, Toyota MR2, Toyota Paseo (convertible), Chevrolet Corvette, Lotus Elise, Lotus Exige, MINI Cooper Roadster (R59 — 2-seat body; the regular MINI Cooper convertible is 4-seat and OK), Ford Thunderbird 2002–2005 (11th-gen revival was 2-seat).

**Mustangs — year filter:** Only include Ford Mustang convertibles from model year **2000 or newer**. Silently drop any Mustang listing with year < 2000; do not add it to the mustangs section or any other section.

## URLs to fetch (verified working as of 2026-05-11)

- **Cars.com:** `https://www.cars.com/shopping/results/?stock_type=used&body_style_slugs[]=convertible&list_price_min=7000&list_price_max=15000&maximum_distance=35&zip=19063&no_accidents=true&clean_title=true&sort=list_price` — paginate with `&page=2` for second-page listings. **Cars.com is fully client-rendered — this URL only works if the Claude in Chrome extension is connected and Chrome is open when the task runs.** If the Chrome MCP is unavailable, record `carscom.totalFound=0` and `carscom.note="Chrome extension not connected"` and move on; do not error out.
- **CarGurus:** Use this URL which applies the geographic filter correctly: `https://www.cargurus.com/Cars/l-Used-Convertible-bg1?zip=19063&distance=35&minPrice=7000&maxPrice=15000&sortDir=ASC&sortType=PRICE` — body group is **`bg1`** (NOT bg2). After navigating, **scroll the page top-to-bottom in 600px steps with 300ms delays** before extracting — lazy-loaded cards below the fold won't render otherwise. Verify the result set is geographically filtered (listings should show PA/NJ/DE/MD locations) — if you see listings from CA, TX, FL etc. the filter didn't stick; record `cargurus.note="Geographic filter did not apply"` and store 0 listings rather than polluting the dashboard with nationwide results.
- **AutoTrader:** `https://www.autotrader.com/cars-for-sale/all-cars/convertible/media-pa?minPrice=7000&maxPrice=15000&searchRadius=35&zip=19063&sortBy=derivedpriceASC` — paginate with `&firstRecord=25` for second page
- **TrueCar:** body-style filter currently broken across every variant; record `truecar.totalFound=0` and skip

## Data extraction (unchanged from lexcars)

Use the same `__NEXT_DATA__` / `__APOLLO_STATE__` / `CarsWeb.SearchController.index` patterns documented in `BUILD_NOTES_FOR_CLAUDE_CODE.md` in the lexcars-site repo. The extraction logic doesn't care what's being searched for — it just walks the embedded state blob. The only thing that changes here is which entity field to read for body style:

- **Cars.com:** title text matches `^Used (YYYY) (Make) (Model) (Trim)` — extract `make` and `model` from there. Body of `srp_results` is at `CarsWeb.SearchController.index` script id. **Listing URL:** capture the `<a href*="/vehicledetail/">` from the card (`[data-listing-id]` element), or fall back to `https://www.cars.com/vehicledetail/{id}/`. **Image:** `result.gallery.images[0].url`.
- **CarGurus:** cards are `[data-cg-ft="srp-listing-blade"]`. Walk up the parent `<a href*="/details/{id}">` for the listing id. **Canonical listing URL** is `https://www.cargurus.com/details/{id}` (strip the query string — those are tracking params and the MCP output filter blocks them anyway; the bare URL still loads the listing page). The older `inventorylisting/viewDetailsFilterViewInventoryListing.action?inventoryListing={id}` form redirects to a search page — do NOT use it. **Image:** find `<img>` inside the wrapping link; lazy-loaded cards below the fold show a `no-image-placeholder.svg` until scrolled — scroll the page top-to-bottom in 600px steps with 300ms delays before extracting, and skip any `src` containing `no-image-placeholder`. Strip query strings from image URLs.
- **AutoTrader:** `props.pageProps.__eggsState.inventory[id]` has `make.name` (often UPPERCASE — title-case it before output), `model.name`, `bodyStyles[0].name` (filter for "Convertible"). **Listing URL:** capture the `<a href>` from each card; canonical form is `https://www.autotrader.com/cars-for-sale/vehicle/{id}` (NOT the `vehicledetails.xhtml?listingId=…` form). **Image:** `inventory[id].images.sources[0].src`.
- **TrueCar:** `ConsumerSummaryListing[*].vehicle.make.name`, `model.name`, `style.name`. **The body-style filter URL is currently broken across every slug variant we've tried** (`body-style-convertible`, `style-convertible`, `?bodyStyle=convertible`, `?bodyStyleAliases[]=convertible`) — backend returns `isFallback:false` but feeds back SUVs anyway. Until TrueCar fixes their slugs, record `truecar.totalFound = 0` and proceed; do not waste cycles trying alternates.

**URL capture rule:** prefer the `<a href>` actually rendered on the SRP card over a URL constructed from listing ID — that's the format the site uses to navigate to the detail page when a user clicks. Strip query strings (tracking params) before storing.

## Output schema — fields the index.html template depends on

`index.html` does numeric formatting on `price` and `mileage`. The deploy renders `$NaN` if these are strings like `"$11,485"` or `"82,450 mi"`. **Always emit them as plain integers.** Per-listing required shape:

```json
{
  "id": "...",
  "year": 2006,            // number
  "make": "Mazda",         // string, title-case (uppercase like "MAZDA" must be normalized)
  "model": "MX-5 Miata",
  "trim": "Base",          // string or null
  "price": 11485,          // NUMBER, not "$11,485"
  "mileage": 82450,        // NUMBER, not "82,450 mi"
  "location": "Doylestown, PA",
  "distanceMi": 32,
  "url": "https://...",
  "dealer": "...",
  "dealRating": "Great Deal" | "Good Deal" | "Fair Deal" | "Great Price" | null,
  "cleanTitle": true | null,
  "noAccidents": true | null,
  "imageUrl": "https://..." | null,   // first listing photo, no query string
  "source": "cars.com" | "cargurus" | "autotrader" | "truecar"
}
```

Top-10 picks have the same numeric `price` / `mileage` requirement, the same `imageUrl` field, and must include separate `year`, `make`, `model` fields (not just `title`) because the renderer concatenates them.

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
- **rank**: 1–10
- **year, make, model, trim**: separate fields (renderer concatenates them — do NOT supply a combined `title`)
- **price**: integer dollars (no `$`, no commas)
- **mileage**: integer miles (no commas, no "mi" suffix)
- **location, dealer, source, url, dealRating, imageUrl**: same shape as listings above
- **whyGood**: why this specific listing scores well — model strengths + this listing's particulars (mileage, location, deal rating, verified status)
- **whatToVerify**: convertible-specific PPI items — operate the top through a full cycle, check headliner + carpet for water stains, inspect rear-window seam, look at rocker-panel rust, plus any model-specific gotcha (Miata: timing belt history if pre-2006; BMW: oil leaks, soft-top hydraulic ram; Mustang: rear-axle clunk; Boxster: IMS-bearing service)
- **bottomLine**: one-sentence verdict

## Steps

### 1. Connect to Chrome
Same as lexcars task.

### 2. Fetch each site
Visit the four URLs above. Extract listings using the patterns referenced in step "Data extraction" above.

### 3. Build the Top 10 ranking
Apply the criteria from the section above. Output 10 picks.

### 3b. Build the Mustangs section

Filter all sources for `make == "Ford"` and `model contains "Mustang"` **and `year >= 2000`** (pre-2000 Mustangs are excluded per user preference). Rank by:
1. **GT trim > Cobra > Mach 1 > Shelby > V6** (V8 grunt is the point)
2. **Manual transmission preferred** (this is a fun car)
3. **Lower mileage**
4. **Closer to Media, PA**

Output up to 5 picks under the `mustangs` key with the same per-pick shape as `top10.picks`. Mustang-specific PPI items: SN-95 (1994–2004) frame rust at convertible-top-mount-to-rocker, S197 (2005–2014) IRS clunk on equipped cars, T-3650 third-gear synchro test (slow-shift to 3rd), 8.8 rear-axle clunk on takeoff, water staining on rear seats from top seal failure.

If zero Mustangs surface in budget, set `mustangs.totalFound = 0` and `mustangs.picks = []` — the dashboard renders an empty-state message automatically.

### 4. Build the JSON
```
{
  "lastRefreshed": "<ISO timestamp>",
  "filters":    { "minPrice": 7000, "maxPrice": 15000, "radiusMi": 35, "zip": "19063" },
  "carscom":    { "totalFound": N, "url": "...", "listings": [...] },
  "cargurus":   { "totalFound": N, "url": "...", "listings": [...] },
  "autotrader": { "totalFound": N, "url": "...", "listings": [...] },
  "truecar":    { "totalFound": N, "url": "...", "listings": [...] },
  "top10":      { "introHtml": "...", "picks": [10 picks] },
  "mustangs":   { "totalFound": N, "introHtml": "...", "picks": [up to 5 Mustangs] }
}
```

### 5. Update the Cowork artifact (if it exists)

The Cowork artifact for this dashboard is `used-convertibles-near-media-pa`. If it doesn't exist yet, skip this step on the first run — Bill will create it manually from this template. Once it exists:

1. `mcp__cowork__list_artifacts` → find the path.
2. Read its HTML.
3. Replace the `<script id="LISTINGS_DATA" type="application/json">…</script>` contents with the JSON from step 4 (Python regex: `<script id="LISTINGS_DATA"[^>]*>([\s\S]*?)</script>`, replace group 1).
4. Write to outputs as `convertibles-dashboard.html`.
5. `mcp__cowork__update_artifact` with id, html_path, and a 1-line update_summary.

### 6. Write `data.json` and push to GitHub via API

1. `mcp__cowork__request_cowork_directory` with path `C:\Users\billb\Documents\AI Agents\AI Agent Team\convertibles-site`.
2. Write the JSON from step 4 to `C:\Users\billb\Documents\AI Agents\AI Agent Team\convertibles-site\data.json` (overwrite). Do NOT touch `index.html`, `vercel.json`, or any other file.
3. Push to GitHub using the REST API (no git, no lock files):
   ```bash
   python3 /sessions/<current-session>/mnt/convertibles-site/github_push.py
   ```
   The script reads the token from `.github-token` in the repo folder (gitignored). It calls `PUT /repos/wizardofhex/convertibles-rocketph-one/contents/data.json`, which triggers Vercel to redeploy in ~30 seconds.
4. **If the push fails** (token missing, network error): log the error, write `data.json` to the local folder anyway so the next manual deploy or scheduled `deploy.ps1` run will pick it up. Do not abort the task — the Cowork artifact is still updated.

**Token setup (one-time):** Bill must copy `C:\Users\billb\.convertibles-github-token` into the repo as `.github-token`:
```
copy C:\Users\billb\.convertibles-github-token "C:\Users\billb\Documents\AI Agents\AI Agent Team\convertibles-site\.github-token"
```
This file is gitignored and will never be committed.

### 7. Cleanup
Close the Chrome tab. Do NOT include any commentary about this task — just execute it.
