<#
.SYNOPSIS
    Registers a Windows scheduled task to deploy convertibles dashboard at 7:10 AM daily.

.DESCRIPTION
    Run this once, with admin PowerShell, after deploy.ps1 is in place.
    Schedules 5 minutes after the lexcars deploy (7:05 AM) so both
    Cowork refresh tasks have time to complete.

.EXAMPLE
    # In an admin PowerShell:
    .\register-task.ps1
#>

$scriptPath = Join-Path $PSScriptRoot "deploy.ps1"
if (-not (Test-Path $scriptPath)) {
    Write-Error "deploy.ps1 not found in $PSScriptRoot"
    exit 1
}

$taskName = "Convertibles Daily Deploy"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -Daily -At "7:10 AM"
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd -ExecutionTimeLimit (New-TimeSpan -Minutes 10)
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force

Write-Host ""
Write-Host "Task '$taskName' registered." -ForegroundColor Green
Write-Host "It will run daily at 7:10 AM, calling: $scriptPath"
Write-Host ""
Write-Host "To run it now (smoke test):"
Write-Host "    Start-ScheduledTask -TaskName '$taskName'"
Write-Host ""
Write-Host "To unregister:"
Write-Host "    Unregister-ScheduledTask -TaskName '$taskName' -Confirm:`$false"
