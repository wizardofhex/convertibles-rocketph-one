#!/usr/bin/env python3
"""
validate_data.py — the single source of truth for the data.json contract that
index.html renders. github_push.py imports this and REFUSES TO PUSH if the
data does not pass, so a malformed refresh can never reach the live site
(the previous good deploy simply stays up).

Why this exists: index.html reads DATA[source].listings, pick.rank,
pick.whyGood, pick.whatToVerify and pick.bottomLine. Refresh runs that wrote
sources as plain arrays, or picks without those fields, produced "No listings",
"Rank undefined" and empty Why/Verify/Bottom-line boxes.

Usage:
    python3 validate_data.py            # normalize + validate data.json in place
    python3 validate_data.py --check    # validate only, do not rewrite the file
Exit code 0 = safe to push, 1 = do not push.
"""
import json, sys
from pathlib import Path

SOURCES   = ["carscom", "cargurus", "autotrader", "truecar"]
PICK_KEYS = ["top10", "manual10", "mustangs"]
PICK_TEXT = ["whyGood", "whatToVerify", "bottomLine"]
MAX_PICKS = {"top10": 10, "manual10": 10, "mustangs": 5}
SOURCE_LABEL = {"carscom": "cars.com", "cars": "cars.com", "cars_com": "cars.com"}
DEAL_LABEL = {
    "GREAT_PRICE": "Great Deal", "GREAT_DEAL": "Great Deal",
    "GOOD_PRICE": "Good Deal",   "GOOD_DEAL": "Good Deal",
    "FAIR_PRICE": "Fair Deal",   "FAIR_DEAL": "Fair Deal",
    "POOR_PRICE": "High Price",  "HIGH_PRICE": "High Price",
    "OVERPRICED": "High Price",
    "NA": None, "N/A": None, "NO_PRICE_ANALYSIS": None, "": None,
}


def _fix_item(it):
    if not isinstance(it, dict):
        return
    s = it.get("source")
    if isinstance(s, str) and s in SOURCE_LABEL:
        it["source"] = SOURCE_LABEL[s]
    r = it.get("dealRating")
    if isinstance(r, str) and r.strip().upper().replace(" ", "_") in DEAL_LABEL and r not in DEAL_LABEL.values():
        it["dealRating"] = DEAL_LABEL[r.strip().upper().replace(" ", "_")]
    t = it.get("transmission")
    if isinstance(t, str) and t not in ("Manual", "Automatic"):
        it["transmission"] = "Manual" if "manual" in t.lower() else ("Automatic" if t.strip() else None)
    # legacy field names seen in past broken runs
    if "imageUrl" not in it and it.get("imgSrc"):
        it["imageUrl"] = it["imgSrc"]
    if "url" not in it and it.get("detailUrl"):
        it["url"] = it["detailUrl"]


def normalize(d):
    """Repair purely mechanical shape mistakes. Returns list of fixes applied.
    Never invents content (whyGood / whatToVerify / bottomLine must be written
    by the refresh run)."""
    fixes = []
    if isinstance(d.get("sources"), dict):
        for k, v in d.pop("sources").items():
            key = {"cars": "carscom", "cars.com": "carscom", "cars_com": "carscom"}.get(k, k)
            d.setdefault(key, v)
        fixes.append("unwrapped 'sources' object to top level")
    for k in SOURCES:
        v = d.get(k)
        if isinstance(v, list):
            d[k] = {"totalFound": len(v), "url": "", "listings": v}
            fixes.append(f"{k}: wrapped plain array into {{totalFound,url,listings}}")
        elif v is None and k == "truecar":
            d[k] = {"totalFound": 0, "url": "", "listings": []}
        if isinstance(d.get(k), dict):
            d[k].setdefault("totalFound", len(d[k].get("listings") or []))
            d[k].setdefault("url", "")
            for it in d[k].get("listings") or []:
                _fix_item(it)
    for k in PICK_KEYS:
        v = d.get(k)
        if isinstance(v, list):
            d[k] = {"introHtml": "", "picks": v}
            fixes.append(f"{k}: wrapped plain array into {{introHtml,picks}}")
        if isinstance(d.get(k), dict) and isinstance(d[k].get("picks"), list):
            d[k].setdefault("introHtml", "")
            d[k].setdefault("totalFound", len(d[k]["picks"]))
            for i, p in enumerate(d[k]["picks"], 1):
                _fix_item(p)
                if isinstance(p, dict) and p.get("rank") != i:
                    p["rank"] = i
                    fixes.append(f"{k}.picks[{i-1}]: set rank={i}")
    return fixes


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _check_vehicle(p, where, errs, need_image=False):
    if not isinstance(p, dict):
        errs.append(f"{where}: not an object"); return
    if not _is_int(p.get("year")) or not (1950 <= p["year"] <= 2100):
        errs.append(f"{where}: 'year' must be an integer (got {p.get('year')!r})")
    for f in ("make", "model"):
        if not isinstance(p.get(f), str) or not p[f].strip():
            errs.append(f"{where}: '{f}' must be a non-empty string")
    if not _is_int(p.get("price")) or p["price"] <= 0:
        errs.append(f"{where}: 'price' must be a positive integer (got {p.get('price')!r})")
    if p.get("mileage") is not None and not _is_int(p["mileage"]):
        errs.append(f"{where}: 'mileage' must be an integer or null (got {p.get('mileage')!r})")
    if not isinstance(p.get("url"), str) or not p["url"].startswith("http"):
        errs.append(f"{where}: 'url' must be an http(s) link (got {p.get('url')!r})")
    img = p.get("imageUrl")
    if need_image and not (isinstance(img, str) and img.startswith("http")):
        errs.append(f"{where}: pick needs a non-null imageUrl")
    if img is not None and not isinstance(img, str):
        errs.append(f"{where}: 'imageUrl' must be a string or null")


def validate(d):
    """Return a list of error strings; empty list means safe to push."""
    errs = []
    if not isinstance(d, dict):
        return ["top level must be a JSON object"]
    if "sources" in d:
        errs.append("data wrapped in a 'sources' object — sources must be top-level keys")
    if not isinstance(d.get("lastRefreshed"), str) or not d["lastRefreshed"]:
        errs.append("'lastRefreshed' must be an ISO timestamp string")
    total_listings = 0
    for k in SOURCES:
        s = d.get(k)
        if not isinstance(s, dict):
            errs.append(f"'{k}' must be an object {{totalFound, url, listings}} (got {type(s).__name__})")
            continue
        if not isinstance(s.get("listings"), list):
            errs.append(f"'{k}.listings' must be an array"); continue
        if not _is_int(s.get("totalFound")):
            errs.append(f"'{k}.totalFound' must be an integer")
        if not isinstance(s.get("url"), str):
            errs.append(f"'{k}.url' must be a string")
        if len(s["listings"]) > 30:
            errs.append(f"'{k}.listings' has {len(s['listings'])} entries (cap is 30)")
        total_listings += len(s["listings"])
        for i, l in enumerate(s["listings"]):
            _check_vehicle(l, f"{k}.listings[{i}]", errs)
    for k in PICK_KEYS:
        s = d.get(k)
        if not isinstance(s, dict):
            errs.append(f"'{k}' must be an object {{introHtml, picks}} (got {type(s).__name__})")
            continue
        if not isinstance(s.get("picks"), list):
            errs.append(f"'{k}.picks' must be an array"); continue
        if not isinstance(s.get("introHtml"), str):
            errs.append(f"'{k}.introHtml' must be a string")
        if len(s["picks"]) > MAX_PICKS[k]:
            errs.append(f"'{k}.picks' has {len(s['picks'])} entries (max {MAX_PICKS[k]})")
        for i, p in enumerate(s["picks"]):
            w = f"{k}.picks[{i}]"
            _check_vehicle(p, w, errs, need_image=True)
            if not isinstance(p, dict):
                continue
            if p.get("rank") != i + 1:
                errs.append(f"{w}: 'rank' must be {i+1} (got {p.get('rank')!r}) — page shows 'Rank undefined'")
            if not isinstance(p.get("source"), str) or not p["source"]:
                errs.append(f"{w}: 'source' must be a non-empty string")
            for f in PICK_TEXT:
                if not isinstance(p.get(f), str) or len(p[f].strip()) < 20:
                    errs.append(f"{w}: '{f}' missing or too short — page shows an empty box")
            if k == "manual10" and p.get("transmission") != "Manual":
                errs.append(f"{w}: manual10 pick must have transmission == 'Manual'")
            if k == "mustangs" and _is_int(p.get("year")) and p["year"] < 2005:
                errs.append(f"{w}: Mustang picks must be 2005 or newer")
    if total_listings and isinstance(d.get("top10"), dict) and not (d["top10"].get("picks") or []):
        errs.append("top10.picks is empty even though listings were captured")
    return errs


def main():
    check_only = "--check" in sys.argv
    path = Path(__file__).parent / "data.json"
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"VALIDATION FAILED: data.json is not readable JSON: {e}")
        sys.exit(1)
    if not check_only:
        fixes = normalize(d)
        for f in fixes:
            print(f"  auto-fixed: {f}")
        if fixes:
            path.write_text(json.dumps(d, indent=2), encoding="utf-8")
    errs = validate(d)
    if errs:
        print(f"VALIDATION FAILED — {len(errs)} problem(s). DO NOT PUSH; fix data.json and re-run:")
        for e in errs[:60]:
            print(f"  - {e}")
        if len(errs) > 60:
            print(f"  ... and {len(errs) - 60} more")
        sys.exit(1)
    print("Schema OK — safe to push")


if __name__ == "__main__":
    main()
