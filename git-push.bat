@echo off
cd /d "C:\Users\billb\Documents\AI Agents\AI Agent Team\convertibles-site"
echo === Git push to GitHub ===
echo.
git push origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS - Vercel will redeploy in ~30s
) else (
    echo FAILED - exit code %ERRORLEVEL%
)
echo.
pause
