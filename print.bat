REM Kill all existings Reader instance
taskkill /F /IM AcroRd32.exe

REM Determine the target directory
REM If a parameter is passed, use it; otherwise use the current directory
if "%~1"=="" (
    set "TARGET_DIR=%cd%"
) else (
    REM Check if the parameter is a file or directory
    if exist "%~1\" (
        REM Parameter is a directory
        set "TARGET_DIR=%~1"
    ) else (
        REM Parameter is a file, use its directory
        set "TARGET_DIR=%~dp1"
    )
)

REM Change to the target directory
cd /d "%TARGET_DIR%"

REM Launch the background script to kill the Acrobat Reader after each print because he don't do that itself
REM start cmd.exe /c kill.bat

REM Launch the loop to print all the files in the folder and subfolders, sorted by name
REM The /r flag makes the loop recursive through subdirectories
for /r "%TARGET_DIR%" %%i in (*.pdf) do (
    "C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe" /t "%%i"
REM	start cmd.exe /c kill.bat
)


REM Kill loop no longer needed for latest Adobe update
