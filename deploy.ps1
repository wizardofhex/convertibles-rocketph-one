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

    # 4. Pull latest
    Write-Step "git pull --rebase"
    git pull --rebase 2>&1 | ForEach-Object { Write-Host "    $_" }

    # 5. Check if anything changed
    $statusOutput = git status --porcelain
    if ([string]::IsNullOrWhiteSpace($statusOutput)) {
        Write-Skip "No changes to commit - exiting."
        exit 0
    }

    # 6. Commit + push
    Write-Step "git add + commit"
    git add data.json index.html vercel.json
    $commitMsg = "Daily refresh: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    git commit -m $commitMsg
    Write-Ok "Committed: $commitMsg"

    $branch = git rev-parse --abbrev-ref HEAD
    Write-Step "git push origin $branch"
    git push origin $branch 2>&1 | ForEach-Object { Write-Host "    $_" }
    Write-Ok "Pushed. Vercel will redeploy in ~30s. Visit https://convertibles.rocketph.one to verify."
}
finally {
    Pop-Location
}

Write-Step "Done."
