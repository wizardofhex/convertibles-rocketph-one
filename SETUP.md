# Convertibles Dashboard — Setup Guide

Static dashboard hosted on Vercel at **convertibles.rocketph.one**, refreshed daily by a scheduled task on Bill's PC that pushes to GitHub. This is a second instance of the lexcars-site pattern, set up identically except for the target domain and the search criteria.

## Architecture

```
[Bill's PC, 7:05 AM daily]
    Cowork scheduled task `refresh-convertibles-dashboard`
    fetches fresh convertible listings via Claude in Chrome
    -> writes data.json to repo folder
                |
                v
[Bill's PC, 7:10 AM daily]
    Windows scheduled task `Convertibles Daily Deploy`
    -> git pull, git add data.json, git commit, git push
                |
                v
         [GitHub repo]
                |
                v (auto-deploy webhook)
                |
            [Vercel]
                |
                v
       convertibles.rocketph.one
```

The scheduling avoids collision with the lexcars deploy (which runs at 7:05 AM). Cowork's refresh task is queued to run at 7:00 AM (concurrent for both sites is fine — Claude in Chrome handles them sequentially in the same chat session). The two `deploy.ps1` Windows tasks run at 7:05 and 7:10 to keep their pulls/pushes clean.

## One-time setup

### 1. Move this folder to its permanent home

The scaffold lives in your Cowork outputs folder. Move it next to lexcars-site:

```powershell
robocopy "C:\Users\billb\AppData\Roaming\Claude\local-agent-mode-sessions\<session>\<sub>\outputs\convertibles-site" `
         "C:\Users\billb\Documents\AI Agents\AI Agent Team\convertibles-site" `
         /E /COPYALL
```

(Or just `xcopy /E` if robocopy is fussy. Or drag-and-drop in Explorer.)

### 2. Create the GitHub repo

```powershell
cd "C:\Users\billb\Documents\AI Agents\AI Agent Team\convertibles-site"
git init
git add .
git commit -m "Initial commit"
gh repo create convertibles-rocketph-one --public --source=. --push
```

(Or create the repo on github.com first, then `git remote add origin ...` and `git push -u origin main`.)

### 3. Connect to Vercel

```powershell
cd "C:\Users\billb\Documents\AI Agents\AI Agent Team\convertibles-site"
vercel link
```

Prompts:
- Set up and deploy? **Y**
- Scope? **Your account**
- Link to existing project? **N**
- Project name? **convertibles-rocketph-one**
- Directory? **./**

Then:
```powershell
vercel --prod
```

Vercel returns a `*.vercel.app` URL — confirm the page loads (it'll show the "Awaiting first refresh" placeholder until Cowork runs).

### 4. Add custom domain in Vercel

Vercel dashboard → Project → Settings → Domains → Add `convertibles.rocketph.one`. Vercel shows the CNAME target.

### 5. Add CNAME at your DNS provider for rocketph.one

- Type: **CNAME**
- Name: **convertibles**
- Value: **cname.vercel-dns.com** (whatever Vercel shows you)
- TTL: 300

DNS propagates in 5–60 min. Vercel auto-issues an SSL cert.

### 6. Register the daily deploy task on Windows

Open an admin PowerShell and run:
```powershell
cd "C:\Users\billb\Documents\AI Agents\AI Agent Team\convertibles-site"
.\register-task.ps1
```

This registers `Convertibles Daily Deploy` to run at 7:10 AM each day.

Smoke test:
```powershell
Start-ScheduledTask -TaskName "Convertibles Daily Deploy"
```

(It'll fail the freshness check the first time because data.json has the placeholder mtime — that's fine, just wait for Cowork's first refresh.)

### 7. Add the Cowork scheduled task

Open Cowork → Scheduled tasks → Add new task. Paste the contents of `SKILL.md` (in this folder) as the task body. Name it `refresh-convertibles-dashboard`. Schedule it for 7:00 AM daily.

After Cowork's first run, data.json will populate and the 7:10 AM deploy will push it.

### 8. Confirm in browser

After the first scheduled run + deploy, visit `https://convertibles.rocketph.one` — you should see fresh listings.

## Verification: filter URLs

The five search URLs in `SKILL.md` and `index.html` use my best guess at each site's body-style filter syntax. On the first scheduled run, watch the Cowork output for "0 listings" on any site — that usually means the body filter parameter is wrong. Likely culprits and fixes:

- **Cars.com:** `body_style_slugs[]=convertible` — if 0 results, try `bodystyles[]=Convertible` (older format)
- **CarGurus:** `bodyTypeGroup=Convertible` — if 0 results, try `bodyType=Convertible` or use the URL CG generates when you select the convertible filter manually in the UI and copy the resulting URL
- **AutoTrader:** path-based `/cars-for-sale/all-cars/convertible/media-pa` — if redirected, try `vehicleStyleCodes=CONV` as a query param
- **TrueCar:** path-based `/listings/body-style-convertible/location-media-pa/` — if 0 results, try `?body=convertible`

The fastest sanity check is to open each URL in your own browser and confirm the result page shows convertibles in your price range.

## Daily refresh flow

```
07:00 — Cowork scheduled task fires
        Opens Chrome, visits 4 search pages, extracts listings via JSON state blobs
        Ranks top 10 for "cheap fun second car"
        Writes data.json to this repo folder
        Updates the Cowork artifact (used-convertibles-near-media-pa)

07:10 — Windows Task Scheduler fires `Convertibles Daily Deploy`
        Checks data.json mtime (must be < 24h old)
        git pull --rebase
        git add data.json
        git commit -m "Daily refresh: YYYY-MM-DD HH:MM"
        git push origin main

07:11 — Vercel webhook receives push, redeploys
07:12 — convertibles.rocketph.one serves fresh data.json
```

## Troubleshooting

**Site shows "Awaiting first refresh"** — Cowork hasn't run yet. Either the scheduled task isn't registered, or Chrome wasn't connected when it tried to fire. Open Cowork, check the task's last run timestamp.

**Some site has 0 listings** — Filter URL is wrong, OR bot protection blocked the fetch. The task should preserve the previous day's data for that site (per the lexcars pattern). If the issue persists, ask Claude in chat to re-probe and update the parser.

**View Listing links go to a search page instead of a vehicle** — The site changed its DOM and the URL-extraction regex needs updating. Tell Claude in chat with the site name; we'll re-test.

**deploy.ps1 fails with "no data.json"** — Cowork's task didn't run or didn't write to this folder. Check Cowork's task log.
