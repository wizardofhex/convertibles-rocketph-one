@echo off
setlocal
echo =============================================
echo  GitHub Token Setup for wizardofhex account
echo =============================================
echo.
echo Step 1: Create a Personal Access Token at:
echo   https://github.com/settings/tokens/new
echo.
echo   - Token name: convertibles-site-deploy
echo   - Expiration: No expiration (or 1 year)
echo   - Scopes: check "repo" (top-level)
echo   - Click Generate token and COPY it
echo.
echo Step 2: Paste the token below
echo.
set /p TOKEN=Paste token here and press Enter:
echo.
if "%TOKEN%"=="" (
    echo ERROR: No token entered. Run this again.
    pause
    exit /b 1
)

echo Saving token to %USERPROFILE%\.convertibles-github-token
echo (outside the repo, so it can never be committed; deploy.ps1 reads it on every push)
(echo %TOKEN%)> "%USERPROFILE%\.convertibles-github-token"

echo Also storing in Windows Credential Manager for interactive git use...
cmdkey /delete:git:https://github.com >nul 2>&1
cmdkey /add:git:https://github.com /user:wizardofhex /pass:%TOKEN%
echo.
echo Testing push now (authenticated as wizardofhex)...
echo.
cd /d "C:\Users\billb\Documents\AI Agents\AI Agent Team\convertibles-site"
git push https://wizardofhex:%TOKEN%@github.com/wizardofhex/convertibles-rocketph-one.git main
if %ERRORLEVEL% EQU 0 (
    git fetch origin >nul 2>&1
    echo ============================================
    echo  SUCCESS! Token stored, push complete.
    echo  Vercel will redeploy in ~30 seconds.
    echo  Future scheduled deploys will work too.
    echo ============================================
) else (
    echo FAILED - token may be wrong or missing repo scope.
    echo Create a new token and run this script again.
)
echo.
pause
endlocal
