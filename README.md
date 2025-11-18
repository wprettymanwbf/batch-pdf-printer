# Batch PDF Printer

Simple Windows script to batch print all PDFs in a folder with Adobe Reader.

## Features
- Print all PDFs in a folder with a single click
- **Hot Folder**: Automatically monitor a folder and print PDFs as they are added
- Works with Windows "Send to" context menu
- Multiple script options: Python, PowerShell, or Batch file
- Processes PDFs recursively through subdirectories
- No admin rights required

## Requirements
- Windows 7/10/11
- Adobe Acrobat Reader DC
- A configured default printer
- Python 3.x (only for Python script option)
- `watchdog` library (only for hot folder feature - install via `pip install watchdog`)

## Quick Start

Choose one of the three available scripts based on your preference:

### Option 1: Python Script (Recommended for flexibility)
```bash
python print.py
python print.py "C:\Path\To\Folder"
```

**Advantages:** Cross-platform compatible, better error handling, easy to modify

### Option 2: PowerShell Script (Recommended for Windows)
```powershell
.\print.ps1
.\print.ps1 "C:\Path\To\Folder"
```

**Note:** If you encounter execution policy issues:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Option 3: Batch File (Traditional)
```cmd
print.bat
```

**Note:** Works immediately on all Windows systems without configuration.

## Installation

1. Download and extract this folder to a permanent location (e.g., `C:\Tools\batch-pdf-printer`)
2. Choose your preferred script from the options above

## Usage

### Direct Execution
Run the script in any folder containing PDFs:
- The script will automatically find and print all PDFs in the current directory and subdirectories

### Print from Any Folder (Python/PowerShell only)
Pass a folder or file path as an argument:
```bash
python print.py "C:\Path\To\Folder"
.\print.ps1 "C:\Path\To\Folder"
```

### Windows "Send to" Context Menu Setup

1. Press `Win + R`, type `shell:sendto`, press Enter
2. Create a shortcut in the SendTo folder:
   - **For Python:** Create `BatchPrintPDFs.bat` with:
     ```batch
     @echo off
     python "C:\Tools\batch-pdf-printer\print.py" %1
     ```
     (Adjust path to match your installation location)
   - **For PowerShell:** Right-click → New → Shortcut to `print.ps1`
   - **For Batch:** Right-click → New → Shortcut to `print.bat`
3. Right-click any folder or PDF file → Send to → Your shortcut

## How It Works
- Closes any running Adobe Reader instances
- Finds all PDF files in the target directory (recursively)
- Sends each PDF to Adobe Reader for printing using the `/t` parameter
- Adobe Reader prints and closes automatically

## Hot Folder Monitoring

The hot folder feature allows you to automatically print PDFs as they are added to a specified directory.

### Installation

1. Install the required dependency:
   ```bash
   pip install -r requirements.txt
   ```
   Or manually:
   ```bash
   pip install watchdog
   ```
   
   **Note:** The convenience scripts (`hot_folder.bat` and `hot_folder.ps1`) will automatically install the dependency if it's missing.

### Configuration

1. Create a configuration file:
   ```bash
   python hot_folder.py --create-config
   ```

2. Edit `hot_folder_config.json` to set your hot folder path:
   ```json
   {
       "hot_folder": "C:\\PDFs\\HotFolder",
       "retry_count": 3,
       "retry_delay": 2,
       "processing_delay": 1,
       "log_level": "INFO",
       "log_file": "hot_folder.log",
       "success_folder": "C:\\PDFs\\HotFolder\\Success",
       "error_folder": "C:\\PDFs\\HotFolder\\Error"
   }
   ```

   **Configuration Options:**
   - `hot_folder`: Path to the directory to monitor for new PDFs
   - `retry_count`: Number of times to retry printing if a file is locked or fails (default: 3)
   - `retry_delay`: Seconds to wait between retries (default: 2)
   - `processing_delay`: Seconds to wait before processing to ensure file is fully written (default: 1)
   - `log_level`: Logging level - DEBUG, INFO, WARNING, ERROR (default: INFO)
   - `log_file`: Path to the log file (default: hot_folder.log)
   - `success_folder`: Path to move successfully printed PDFs (optional, leave empty to keep files in place)
   - `error_folder`: Path to move PDFs that failed to print (optional, leave empty to keep files in place)

### Usage

1. **Using configuration file:**
   ```bash
   python hot_folder.py
   ```
   Or use the convenience scripts:
   - **Windows Batch**: `hot_folder.bat`
   - **PowerShell**: `.\hot_folder.ps1`

2. **Specifying folder via command line:**
   ```bash
   python hot_folder.py "C:\Path\To\HotFolder"
   ```
   Or:
   - **Windows Batch**: `hot_folder.bat "C:\Path\To\HotFolder"`
   - **PowerShell**: `.\hot_folder.ps1 "C:\Path\To\HotFolder"`

3. The script will:
   - Monitor the specified folder for new PDF files
   - Automatically print each PDF as it's detected
   - Process files sequentially to avoid conflicts
   - Retry failed prints with configurable retry logic
   - Log all activities to the specified log file
   - Move successfully printed files to the Success folder (if configured)
   - Move failed files to the Error folder (if configured)

4. Press `Ctrl+C` to stop monitoring

### File Organization

The hot folder feature can automatically organize processed files:
- **Success Folder**: Successfully printed PDFs are moved here (if `success_folder` is configured)
- **Error Folder**: PDFs that failed to print are moved here (if `error_folder` is configured)
- **Duplicate Handling**: If a file with the same name exists in the destination folder, a timestamp is appended to the filename
- **Optional**: Leave `success_folder` and `error_folder` empty in the configuration to keep files in the hot folder

### Error Handling

The hot folder feature includes robust error handling:
- **File Locking**: If a file is locked (still being written), it will retry after a delay
- **Missing Files**: Gracefully handles files that are deleted before processing
- **Print Errors**: Logs errors and continues monitoring for new files
- **Retry Logic**: Configurable retry attempts for problematic files
- **Failed Files**: Files that fail after all retry attempts are moved to the Error folder (if configured)

### Running as a Service

To run the hot folder monitor continuously in the background:

**Option 1: Using Task Scheduler (Recommended for Windows)**
1. Open Task Scheduler
2. Create a new Basic Task
3. Set trigger to "At startup" or "At log on"
4. Action: Start a program
5. Program: `python` or `pythonw` (for no console window)
6. Arguments: `"C:\Path\To\hot_folder.py"`
7. Start in: `C:\Path\To\batch-pdf-printer`

**Option 2: Using a batch file with pythonw (no console window)**
Create `run_hot_folder.bat`:
```batch
@echo off
pythonw "C:\Path\To\batch-pdf-printer\hot_folder.py"
```

Then add this batch file to your Startup folder (`shell:startup`).

## License
GNU General Public License v3.0

Copyleft (C) Nicolas Simond - 2018

This script is free software licensed under GPL v3.0. See LICENSE file for details.

