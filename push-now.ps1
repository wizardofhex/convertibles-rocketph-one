cd "C:\Users\billb\Documents\AI Agents\AI Agent Team\convertibles-site"
Write-Host "=== Git status ===" -ForegroundColor Cyan
git status
Write-Host ""
Write-Host "=== Pushing 3 commits to GitHub ===" -ForegroundColor Cyan
git push origin main
Write-Host ""
if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS - Vercel will redeploy in ~30s" -ForegroundColor Green
} else {
    Write-Host "FAILED (exit code $LASTEXITCODE)" -ForegroundColor Red
}
Write-Host ""
Read-Host "Press Enter to close"
