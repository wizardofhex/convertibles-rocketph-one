$log = "C:\Users\billb\Documents\AI Agents\AI Agent Team\convertibles-site\push-log.txt"
"=== $(Get-Date) ===" | Out-File $log
Set-Location "C:\Users\billb\Documents\AI Agents\AI Agent Team\convertibles-site"
"--- git status ---" | Out-File $log -Append
(git status 2>&1) | Out-File $log -Append
"--- git push origin main ---" | Out-File $log -Append
(git push origin main 2>&1) | Out-File $log -Append
"--- Exit code: $LASTEXITCODE ---" | Out-File $log -Append
"--- git log (top 5) ---" | Out-File $log -Append
(git log --oneline -5 2>&1) | Out-File $log -Append
"--- git remote -v ---" | Out-File $log -Append
(git remote -v 2>&1) | Out-File $log -Append
"--- git config credential.helper ---" | Out-File $log -Append
(git config credential.helper 2>&1) | Out-File $log -Append
"=== Done ===" | Out-File $log -Append
