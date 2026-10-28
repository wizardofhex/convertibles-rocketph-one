#!/usr/bin/env python3
"""
github_push.py — Push data.json AND index.html to GitHub via REST API.

The page reads data from an inline <script id="LISTINGS_DATA"> block inside
index.html (it takes priority over the data.json fetch), so both files must
be updated on every refresh.

No local git required. No index.lock. Works from the Cowork bash sandbox
or any machine without git credentials configured.

Token lookup order:
  1. .github-token   — file in this repo folder (gitignored; preferred)
  2. ~/.convertibles-github-token — original Windows location
  3. GITHUB_TOKEN    — environment variable

Usage:
    python github_push.py          # inject data.json into index.html, push both
    python github_push.py --dry-run  # validate token + show what would be pushed
"""

import json, base64, re, urllib.request, urllib.error
import os, sys, argparse
from pathlib import Path
from datetime import datetime, timezone

# ── Repo config ──────────────────────────────────────────────────────────────
REPO_OWNER = "wizardofhex"
REPO_NAME  = "convertibles-rocketph-one"
BRANCH     = "main"
SITE_URL   = "https://convertibles.rocketph.one"

SCRIPT_DIR = Path(__file__).parent


# ── Token discovery ───────────────────────────────────────────────────────────
def find_token():
    candidates = [
        (SCRIPT_DIR / ".github-token",                      ".github-token in repo"),
        (Path.home() / ".convertibles-github-token",        "~/.convertibles-github-token"),
        (Path("/c/Users/billb/.convertibles-github-token"), "/c/Users/billb/..."),
    ]
    for path, label in candidates:
        try:
            t = path.read_text().strip()
            if t:
                return t, label
        except (FileNotFoundError, PermissionError):
            pass
    env = os.environ.get("GITHUB_TOKEN", "").strip()
    if env:
        return env, "GITHUB_TOKEN env var"
    return None, None


# ── GitHub API helper ─────────────────────────────────────────────────────────
def gh(method, path, token, body=None):
    url  = f"https://api.github.com{path}"
    data = json.dumps(body).encode() if body else None
    req  = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization",        f"Bearer {token}")
    req.add_header("Accept",               "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode(errors="replace")
        raise RuntimeError(
            f"GitHub API {method} {path} → HTTP {e.code}\n{body_text}"
        ) from e


def get_sha(token, filename):
    """Return current blob SHA for a file, or None if it doesn't exist yet."""
    api_path = f"/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filename}?ref={BRANCH}"
    try:
        cur = gh("GET", api_path, token)
        return cur["sha"]
    except RuntimeError as e:
        if "404" in str(e):
            return None
        raise


def push_file(token, filename, content_bytes, commit_msg, sha):
    """Push a single file. sha=None means first-ever push."""
    encoded = base64.b64encode(content_bytes).decode()
    body = {"message": commit_msg, "content": encoded, "branch": BRANCH}
    if sha:
        body["sha"] = sha
    return gh("PUT", f"/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filename}", token, body)


def inject_data_into_html(data_bytes, html_path):
    """
    Replace the <script id="LISTINGS_DATA"> block in index.html with the
    contents of data.json and write it back. Returns the updated bytes.
    """
    data_str = json.dumps(json.loads(data_bytes), indent=2)
    html = html_path.read_text(encoding="utf-8")

    marker_open  = '<script id="LISTINGS_DATA" type="application/json">'
    marker_close = '</script>'

    start = html.find(marker_open)
    if start == -1:
        raise ValueError("LISTINGS_DATA script block not found in index.html")
    content_start = start + len(marker_open)
    content_end   = html.find(marker_close, content_start)
    if content_end == -1:
        raise ValueError("Closing </script> for LISTINGS_DATA not found")

    new_html = html[:content_start] + data_str + html[content_end:]
    html_path.write_text(new_html, encoding="utf-8")
    return new_html.encode("utf-8")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Validate without pushing")
    args = ap.parse_args()

    # 1. Token
    token, token_src = find_token()
    if not token:
        print("ERROR: No GitHub token found.")
        print("Fix: echo ghp_YOUR_TOKEN > .github-token")
        sys.exit(1)
    print(f"  token : {token_src}")

    # 2. Read data.json
    data_path = SCRIPT_DIR / "data.json"
    if not data_path.exists():
        print(f"ERROR: data.json not found — run the refresh task first.")
        sys.exit(1)
    data_bytes = data_path.read_bytes()
    print(f"  data  : data.json  ({len(data_bytes):,} bytes)")

    # 3. Build commit message from lastRefreshed
    try:
        d = json.loads(data_bytes)
        refreshed = d.get("lastRefreshed", "")
        date_str  = refreshed[:10] if refreshed else datetime.now(timezone.utc).strftime("%Y-%m-%d")
    except Exception:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    commit_msg = f"Daily refresh: {date_str}"
    print(f"  commit: {commit_msg}")

    # 4. Inject data into index.html
    html_path = SCRIPT_DIR / "index.html"
    if not html_path.exists():
        print("ERROR: index.html not found.")
        sys.exit(1)
    try:
        html_bytes = inject_data_into_html(data_bytes, html_path)
        print(f"  html  : index.html updated  ({len(html_bytes):,} bytes)")
    except Exception as e:
        print(f"ERROR injecting data into index.html: {e}")
        sys.exit(1)

    if args.dry_run:
        try:
            me = gh("GET", "/user", token)
            print(f"\nDry-run OK — authenticated as {me['login']}")
        except RuntimeError as e:
            print(f"\nDry-run FAILED — token rejected:\n{e}")
            sys.exit(1)
        return

    # 5. Push data.json
    print(f"\nPushing to github.com/{REPO_OWNER}/{REPO_NAME} …")
    sha_data = get_sha(token, "data.json")
    result_data = push_file(token, "data.json", data_bytes, commit_msg, sha_data)
    print(f"  ✓  data.json committed")

    # 6. Push index.html (separate commit — both trigger a single Vercel deploy)
    sha_html = get_sha(token, "index.html")
    result_html = push_file(token, "index.html", html_bytes, commit_msg, sha_html)
    commit_url = result_html["commit"]["html_url"]
    print(f"  ✓  index.html committed")
    print(f"     {commit_url}")
    print(f"     Vercel redeploys in ~30s → {SITE_URL}")


if __name__ == "__main__":
    main()
