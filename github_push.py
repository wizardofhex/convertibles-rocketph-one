#!/usr/bin/env python3
"""
github_push.py — Push data.json to GitHub via REST API.

No local git required. No index.lock. Works from the Cowork bash sandbox
or any machine without git credentials configured.

Token lookup order:
  1. .github-token   — file in this repo folder (gitignored; preferred)
  2. ~/.convertibles-github-token — original Windows location
  3. GITHUB_TOKEN    — environment variable

Usage:
    python github_push.py                    # pushes data.json
    python github_push.py --file data.json   # explicit (same effect)
    python github_push.py --dry-run          # validate token + show what would be pushed
"""

import json, base64, urllib.request, urllib.error
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
    """Return (token_str, source_description) or (None, None)."""
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


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file",    default="data.json", help="File in repo to update")
    ap.add_argument("--dry-run", action="store_true",  help="Validate without pushing")
    args = ap.parse_args()

    # 1. Token
    token, token_src = find_token()
    if not token:
        print("ERROR: No GitHub token found.")
        print()
        print("Fix: create  .github-token  in this repo folder with your PAT (repo scope):")
        print("     echo ghp_YOUR_TOKEN > .github-token")
        print()
        print("Or run setup-github-token.bat to refresh the original credential file.")
        sys.exit(1)
    print(f"  token : {token_src}")

    # 2. Local file
    local = SCRIPT_DIR / args.file
    if not local.exists():
        print(f"ERROR: {local} not found — run the refresh task first.")
        sys.exit(1)

    content = local.read_bytes()
    encoded = base64.b64encode(content).decode()
    print(f"  file  : {local.name}  ({len(content):,} bytes)")

    # 3. Parse lastRefreshed for commit message
    try:
        d = json.loads(content)
        refreshed = d.get("lastRefreshed", "")
        date_str  = refreshed[:10] if refreshed else datetime.now(timezone.utc).strftime("%Y-%m-%d")
    except Exception:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    commit_msg = f"Daily refresh: {date_str}"
    print(f"  commit: {commit_msg}")

    if args.dry_run:
        # Validate token by pinging the API
        try:
            me = gh("GET", "/user", token)
            print(f"\nDry-run OK — authenticated as {me['login']}")
        except RuntimeError as e:
            print(f"\nDry-run FAILED — token rejected:\n{e}")
            sys.exit(1)
        return

    # 4. Get current SHA (required for update; None means first-ever push)
    file_api = f"/repos/{REPO_OWNER}/{REPO_NAME}/contents/{args.file}?ref={BRANCH}"
    try:
        cur = gh("GET", file_api, token)
        sha = cur["sha"]
        print(f"  sha   : {sha[:12]}…")
    except RuntimeError as e:
        if "404" in str(e):
            sha = None
            print("  sha   : (new file)")
        else:
            print(f"ERROR fetching current SHA:\n{e}")
            sys.exit(1)

    # 5. Push
    body = {"message": commit_msg, "content": encoded, "branch": BRANCH}
    if sha:
        body["sha"] = sha

    print(f"\nPushing to github.com/{REPO_OWNER}/{REPO_NAME}/{args.file} …")
    try:
        result = gh(
            "PUT",
            f"/repos/{REPO_OWNER}/{REPO_NAME}/contents/{args.file}",
            token,
            body,
        )
    except RuntimeError as e:
        print(f"ERROR: push failed:\n{e}")
        sys.exit(1)

    commit_url = result["commit"]["html_url"]
    print(f"  ✓  committed: {commit_msg}")
    print(f"     {commit_url}")
    print(f"     Vercel redeploys in ~30s → {SITE_URL}")


if __name__ == "__main__":
    main()
