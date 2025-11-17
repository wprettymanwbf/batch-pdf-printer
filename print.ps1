# Batch PDF Printer - PowerShell Version
# Script for batch printing all PDF in a folder on Windows Platform with Adobe Reader
# Copyleft (C) Nicolas Simond - 2018
# Licensed under GNU General Public License v3.0

# Kill all existing Adobe Reader instances
Write-Host "Closing any existing Adobe Reader instances..."
Get-Process -Name "AcroRd32" -ErrorAction SilentlyContinue | Stop-Process -Force

# Determine the target directory
# If a parameter is passed, use it; otherwise use the current directory
if ($args.Count -eq 0) {
    $targetDir = Get-Location
} else {
    $param = $args[0]
    
    # Check if the parameter is a file or directory
    if (Test-Path -Path $param -PathType Container) {
        # Parameter is a directory
        $targetDir = $param
    } elseif (Test-Path -Path $param -PathType Leaf) {
        # Parameter is a file, use its directory
        $targetDir = Split-Path -Path $param -Parent
    } else {
        Write-Host "Error: The specified path does not exist: $param"
        exit 1
    }
}

# Change to the target directory
Set-Location -Path $targetDir
Write-Host "Processing PDFs in directory: $targetDir"

# Path to Adobe Reader executable
$adobeReaderPath = "C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe"

# Check if Adobe Reader exists
if (-not (Test-Path -Path $adobeReaderPath)) {
    # Try 64-bit version path
    $adobeReaderPath = "C:\Program Files\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe"
    
    if (-not (Test-Path -Path $adobeReaderPath)) {
        Write-Host "Error: Adobe Reader not found. Please check the installation path."
        exit 1
    }
}

# Get all PDF files in the target directory and subdirectories, sorted by full name
$pdfFiles = Get-ChildItem -Path $targetDir -Filter "*.pdf" -Recurse | Sort-Object -Property FullName

if ($pdfFiles.Count -eq 0) {
    Write-Host "No PDF files found in the directory."
    exit 0
}

Write-Host "Found $($pdfFiles.Count) PDF file(s) to print."

# Launch the loop to print all the files in the folder
$counter = 0
foreach ($pdf in $pdfFiles) {
    $counter++
    Write-Host "Printing ($counter/$($pdfFiles.Count)): $($pdf.Name)"
    Start-Process -FilePath $adobeReaderPath -ArgumentList "/t", "`"$($pdf.FullName)`"" -Wait:$false
}

Write-Host "All PDF files have been sent to the printer."
Write-Host "Note: Adobe Reader will close automatically after printing."
