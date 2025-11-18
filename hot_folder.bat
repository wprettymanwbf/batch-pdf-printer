@echo off
REM Hot Folder PDF Printer - Windows Batch Wrapper
REM This script starts the hot folder monitoring service

echo ============================================================
echo Hot Folder PDF Printer
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.x from https://www.python.org/
    pause
    exit /b 1
)

REM Check if watchdog is installed
python -c "import watchdog" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependency: watchdog
    pip install watchdog
    if errorlevel 1 (
        echo Error: Failed to install watchdog
        pause
        exit /b 1
    )
)

REM Run the hot folder script
echo Starting hot folder monitoring...
echo.
python "%~dp0hot_folder.py" %*

if errorlevel 1 (
    echo.
    echo Hot folder monitoring stopped with errors.
    pause
)
