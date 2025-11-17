Batch PDF Printer
=================

## License
Script for batch printing all PDF in a folder on Windows Platform with Adobe Reader

Copyleft (C) Nicolas Simond - 2018

This script is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This script is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this script.  If not, see <http://www.gnu.org/licenses/gpl.txt>

## About this script
Simple script to batch print every PDF in a folder just with a click without bothering about the number of PDF files to print.

The script can be executed directly or configured to work with Windows "Send to" context menu, allowing you to print PDFs from any folder on your computer.


## Dependencies
- Adobe Acrobat or Adobe Reader
- A default printer
- No admin rights needed

## Designed for
- Windows 7/10/11
- Adobe Reader DC / Can fit Adobe Acrobat (with path change to .exe)

## Installation
Download the archive and extract the folder to a permanent location on your computer (e.g., `C:\Tools\batch-pdf-printer`).

## Usage

### Method 1: Direct Execution (Traditional)
Put all the PDF files in the folder where the batch scripts reside.

Run ***print.bat*** and let everything run until the end.

### Method 2: Send To Context Menu (Recommended)
You can print PDFs from any folder using the Windows "Send to" context menu:

1. Press `Win + R` to open the Run dialog
2. Type `shell:sendto` and press Enter
3. This opens the SendTo folder (typically `C:\Users\YourUsername\AppData\Roaming\Microsoft\Windows\SendTo`)
4. Create a shortcut to ***print.bat*** in this folder:
   - Right-click in the SendTo folder and select `New > Shortcut`
   - Browse to the location where you extracted print.bat
   - Name the shortcut "Batch Print PDFs" (or any name you prefer)
5. Now you can right-click any folder containing PDFs, select `Send to > Batch Print PDFs`, and all PDFs in that folder will be printed

**Note:** You can also select a single PDF file and send it to "Batch Print PDFs" - the script will print all PDFs in the same folder as the selected file.

Adapt the timer in ***kill.bat*** if your computer is too slow.
