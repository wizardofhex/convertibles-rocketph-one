$log = "C:\Users\billb\Documents\AI Agents\AI Agent Team\convertibles-site\creds-check.txt"
"=== Windows Credential Manager - GitHub entries ===" | Out-File $log
(cmdkey /list) | Where-Object { $_ -match "github|git:" } | Out-File $log -Append
"" | Out-File $log -Append
"=== All git: entries ===" | Out-File $log -Append
(cmdkey /list) | Select-String "git:" | Out-File $log -Append
"" | Out-File $log -Append
"=== GCM version ===" | Out-File $log -Append
(git-credential-manager --version 2>&1) | Out-File $log -Append
"=== Done ===" | Out-File $log -Append
