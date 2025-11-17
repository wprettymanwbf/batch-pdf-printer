#!/usr/bin/env python3
"""
Batch PDF Printer - Python Version
Script for batch printing all PDF in a folder on Windows Platform with Adobe Reader

Copyleft (C) Nicolas Simond - 2018
Licensed under GNU General Public License v3.0

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
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def find_adobe_reader():
    """
    Find the Adobe Reader executable path.
    Returns the path if found, None otherwise.
    """
    if platform.system() != 'Windows':
        print("Error: This script is designed for Windows platform.")
        print("On Linux/Mac, consider using 'lpr' command for printing PDFs.")
        return None
    
    # Common Adobe Reader paths
    possible_paths = [
        r"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
        r"C:\Program Files\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
        r"C:\Program Files (x86)\Adobe\Acrobat Reader\Reader\AcroRd32.exe",
        r"C:\Program Files\Adobe\Acrobat Reader\Reader\AcroRd32.exe",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None


def kill_adobe_reader():
    """
    Kill all existing Adobe Reader instances.
    """
    if platform.system() != 'Windows':
        return
    
    try:
        print("Closing any existing Adobe Reader instances...")
        subprocess.run(['taskkill', '/F', '/IM', 'Acrobat.exe'], 
                      stderr=subprocess.DEVNULL, 
                      stdout=subprocess.DEVNULL)
    except Exception:
        # If taskkill fails, it's not critical - just continue
        pass


def get_pdf_files(directory):
    """
    Get all PDF files in the specified directory and its subdirectories.
    
    Args:
        directory: Path to the directory to search
    
    Returns:
        List of Path objects for PDF files, sorted by full path
    """
    directory_path = Path(directory)
    if not directory_path.exists():
        print(f"Error: Directory does not exist: {directory}")
        return []
    
    if not directory_path.is_dir():
        print(f"Error: Path is not a directory: {directory}")
        return []
    
    pdf_files = sorted(directory_path.glob('**/*.pdf'))
    return pdf_files


def print_pdfs(directory, adobe_reader_path):
    """
    Print all PDF files in the specified directory.
    
    Args:
        directory: Path to the directory containing PDFs
        adobe_reader_path: Path to Adobe Reader executable
    """
    pdf_files = get_pdf_files(directory)
    
    if not pdf_files:
        print("No PDF files found in the directory.")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s) to print.")
    
    for pdf_file in pdf_files:
        print(f"Printing: {pdf_file.name}")
        try:
            # Use /t parameter to print the PDF and close Adobe Reader
            subprocess.Popen([adobe_reader_path, '/t', str(pdf_file)])
        except Exception as e:
            print(f"Error printing {pdf_file.name}: {e}")
    
    print("\nAll PDF files have been sent to the printer.")
    print("Note: Adobe Reader will close automatically after printing with recent updates.")


def main():
    """
    Main function to execute the batch PDF printing.
    """
    # Kill any existing Adobe Reader instances
    kill_adobe_reader()
    
    # Determine target directory
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
        
        # Check if the argument is a file or directory
        path_obj = Path(target_path)
        if path_obj.is_file():
            # If it's a file, use its parent directory
            target_dir = str(path_obj.parent)
        elif path_obj.is_dir():
            # If it's a directory, use it directly
            target_dir = target_path
        else:
            print(f"Error: The specified path does not exist: {target_path}")
            sys.exit(1)
    else:
        # Use current directory if no argument provided
        target_dir = os.getcwd()
    
    print(f"Processing PDFs in directory: {target_dir}")
    
    # Find Adobe Reader
    adobe_reader_path = find_adobe_reader()
    if not adobe_reader_path:
        print("Error: Adobe Reader not found. Please check the installation.")
        print("Expected locations:")
        print("  - C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32.exe")
        print("  - C:\\Program Files\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32.exe")
        sys.exit(1)
    
    print(f"Using Adobe Reader: {adobe_reader_path}")
    
    # Print all PDFs in the directory
    print_pdfs(target_dir, adobe_reader_path)


if __name__ == "__main__":
    main()
