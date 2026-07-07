@echo off
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
echo Step 2: Paste the token below (it won't show as you type)
echo.
set /p TOKEN=Paste token here and press Enter:
echo.
if "%TOKEN%"=="" (
    echo ERROR: No token entered. Run this again.
    pause
    exit /b 1
)
echo Storing credential in Windows Credential Manager...
cmdkey /add:git:https://github.com /user:wizardofhex /pass:%TOKEN%
echo.
echo Testing push now...
echo.
cd /d "C:\Users\billb\Documents\AI Agents\AI Agent Team\convertibles-site"
git push origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo ============================================
    echo  SUCCESS! Token stored, push complete.
    echo  Vercel will redeploy in ~30 seconds.
    echo  Future scheduled deploys will work too.
    echo ============================================
) else (
    echo FAILED - token may be wrong or missing repo scope.
    echo Delete it and try again: cmdkey /delete:git:https://github.com
)
echo.
pause
