# Batch PDF Printer

Simple Windows script to batch print all PDFs in a folder with Adobe Reader.

## Features
- Print all PDFs in a folder with a single click
- Works with Windows "Send to" context menu
- Multiple script options: Python, PowerShell, or Batch file
- Processes PDFs recursively through subdirectories
- No admin rights required

## Requirements
- Windows 7/10/11
- Adobe Acrobat Reader DC
- A configured default printer
- Python 3.x (only for Python script option)

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

## License
GNU General Public License v3.0

Copyleft (C) Nicolas Simond - 2018

This script is free software licensed under GPL v3.0. See LICENSE file for details.

