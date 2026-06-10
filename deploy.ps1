#requires -Version 5.1
<#
.SYNOPSIS
    Pushes the latest convertibles dashboard data to GitHub for Vercel auto-deploy.

.DESCRIPTION
    Cowork's scheduled refresh task writes data.json directly into this
    repo folder (index.html is a static template). This script just
    commits and pushes whatever has changed.

    Run daily via Windows Task Scheduler at 7:10 AM (5 min after lexcars
    deploy at 7:05 AM, so Cowork has time to finish both refreshes).

.PARAMETER RepoPath
    Path to your local git repo for convertibles-rocketph-one.
    Default: $PSScriptRoot (the dir this script lives in).

.EXAMPLE
    .\deploy.ps1
#>

param(
    [string]$RepoPath = $PSScriptRoot
)

$ErrorActionPreference = "Stop"

function Write-Step($msg) { Write-Host ">>> $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "    $msg" -ForegroundColor Green }
function Write-Skip($msg) { Write-Host "    $msg" -ForegroundColor Yellow }
function Write-Warn($msg) { Write-Host "    $msg" -ForegroundColor Yellow }

Write-Step "Convertibles deploy starting at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

# 1. Verify repo path
if (-not (Test-Path (Join-Path $RepoPath ".git"))) {
    Write-Error "Not a git repo: $RepoPath`nRun 'git init' and link to GitHub first (see SETUP.md)."
    exit 1
}
Write-Ok "Repo path: $RepoPath"

Push-Location $RepoPath
try {
    # 2. Sweep stale git lock files
    $lockFiles = @(
        ".git\index.lock",
        ".git\HEAD.lock",
        ".git\refs\remotes\origin\master.lock",
        ".git\refs\remotes\origin\main.lock",
        ".git\objects\maintenance.lock"
    )
    foreach ($lock in $lockFiles) {
        $full = Join-Path $RepoPath $lock
        if (Test-Path $full) {
            Remove-Item $full -Force -ErrorAction SilentlyContinue
            if (-not (Test-Path $full)) {
                Write-Warn "Cleared stale lock: $lock"
            }
        }
    }

    # 3. Verify data.json is fresh
    $dataPath = Join-Path $RepoPath "data.json"
    if (-not (Test-Path $dataPath)) {
        Write-Error "No data.json in repo. Did the Cowork refresh task run today?"
        exit 1
    }
    $mtime = (Get-Item $dataPath).LastWriteTime
    $ageMinutes = ((Get-Date) - $mtime).TotalMinutes
    Write-Ok "data.json last modified: $mtime ($([int]$ageMinutes) min ago)"
    if ($ageMinutes -gt (24 * 60)) {
        Write-Warn "data.json is more than 24h old. Pushing anyway, but data may be stale."
    }

    # 4. Pull latest. --autostash lets pull --rebase succeed even if there are
    #    uncommitted local edits (e.g. an in-progress edit to index.html or SKILL.md);
    #    git stashes them, rebases, then re-applies the stash automatically.
    Write-Step "git pull --rebase --autostash"
    # Wrap in SilentlyContinue so git's informational stderr lines (e.g. "Applied autostash.")
    # don't become terminating errors under $ErrorActionPreference = "Stop".
    $pullResult = & { $ErrorActionPreference = "SilentlyContinue"; git pull --rebase --autostash 2>&1 }
    $pullResult | ForEach-Object { Write-Host "    $_" }
    if ($LASTEXITCODE -ne 0) {
        Write-Error "git pull --rebase failed (likely a merge conflict). Resolve manually, then re-run."
        exit 1
    }

    # 5. Stage every tracked change. The original deploy script staged only
    #    data.json / index.html / vercel.json, which meant edits to SKILL.md,
    #    README.md, deploy.ps1 itself, etc. were silently dropped. The script's
    #    stated intent is "commits and pushes whatever has changed", so trust
    #    .gitignore to keep junk out and stage all tracked changes.
    git add -A

    # 6. Check if anything is staged. If working tree was clean to start with
    #    and nothing came in via the pull, exit clean.
    $statusOutput = git status --porcelain
    if ([string]::IsNullOrWhiteSpace($statusOutput)) {
        Write-Skip "No changes to commit - exiting."
        exit 0
    }

    # 7. Commit + push
    Write-Step "git commit"
    $commitMsg = "Daily refresh: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    git commit -m $commitMsg
    if ($LASTEXITCODE -ne 0) {
        Write-Error "git commit failed - see output above."
        exit 1
    }
    Write-Ok "Committed: $commitMsg"

    $branch = git rev-parse --abbrev-ref HEAD
    Write-Step "git push origin $branch"
    git push origin $branch 2>&1 | ForEach-Object { Write-Host "    $_" }
    if ($LASTEXITCODE -ne 0) {
        # Most common cause: a new commit landed on origin between our pull
        # and our push. One retry with rebase usually fixes it.
        Write-Warn "Push rejected. Retrying with a fresh pull --rebase..."
        $retryResult = & { $ErrorActionPreference = "SilentlyContinue"; git pull --rebase --autostash 2>&1 }
        $retryResult | ForEach-Object { Write-Host "    $_" }
        git push origin $branch 2>&1 | ForEach-Object { Write-Host "    $_" }
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Push still failing after retry. Investigate manually."
            exit 1
        }
    }
    Write-Ok "Pushed. Vercel will redeploy in ~30s. Visit https://convertibles.rocketph.one to verify."
}
finally {
    Pop-Location
}

Write-Step "Done."
