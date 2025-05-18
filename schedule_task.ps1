# PowerShell script to schedule the auto_run.py script using Task Scheduler

# Get the current directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$autoRunPath = Join-Path -Path $scriptPath -ChildPath "auto_run.py"
$pythonPath = "python"

# Create the action to run the script
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument $autoRunPath

# Create a trigger (daily at 2 AM)
$trigger = New-ScheduledTaskTrigger -Daily -At 2am

# Create the task settings
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd -AllowStartIfOnBatteries

# Register the task
$taskName = "PenTestToolkit_AutoRun"
$description = "Automatically runs the Penetration Testing Toolkit with predefined settings"

# Check if the task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "Task '$taskName' already exists. Removing it..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create the task
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description $description

Write-Host "Task '$taskName' has been scheduled to run daily at 2 AM."
Write-Host "You can modify the schedule in Task Scheduler."
