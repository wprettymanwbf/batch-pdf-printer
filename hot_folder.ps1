# Hot Folder PDF Printer - PowerShell Version
# This script starts the hot folder monitoring service

param(
    [string]$HotFolderPath = ""
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Hot Folder PDF Printer" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.x from https://www.python.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if watchdog is installed
try {
    & python -c "import watchdog" 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw
    }
} catch {
    Write-Host "Installing required dependency: watchdog" -ForegroundColor Yellow
    & pip install watchdog
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to install watchdog" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$hotFolderScript = Join-Path $scriptDir "hot_folder.py"

# Run the hot folder script
Write-Host "Starting hot folder monitoring..." -ForegroundColor Green
Write-Host ""

if ($HotFolderPath) {
    & python $hotFolderScript $HotFolderPath
} else {
    & python $hotFolderScript
}

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Hot folder monitoring stopped with errors." -ForegroundColor Red
    Read-Host "Press Enter to exit"
}
