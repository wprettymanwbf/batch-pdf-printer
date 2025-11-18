#!/usr/bin/env python3
"""
Hot Folder PDF Printer - Automatic PDF printing when files are added to a folder
Script for monitoring a directory and automatically printing PDFs with Adobe Reader

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
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from threading import Lock

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Error: 'watchdog' library is required for hot folder monitoring.")
    print("Please install it using: pip install watchdog")
    sys.exit(1)

# Import functions from the existing print.py script
from print import find_adobe_reader, kill_adobe_reader


class PDFPrintHandler(FileSystemEventHandler):
    """
    File system event handler that processes PDF files when they are created or modified.
    """
    
    def __init__(self, adobe_reader_path, config):
        """
        Initialize the PDF print handler.
        
        Args:
            adobe_reader_path: Path to Adobe Reader executable
            config: Configuration dictionary
        """
        super().__init__()
        self.adobe_reader_path = adobe_reader_path
        self.config = config
        self.processing_lock = Lock()
        self.processed_files = set()
        self.retry_count = config.get('retry_count', 3)
        self.retry_delay = config.get('retry_delay', 2)
        self.processing_delay = config.get('processing_delay', 1)
        
    def on_created(self, event):
        """
        Called when a file or directory is created.
        
        Args:
            event: File system event
        """
        if event.is_directory:
            return
        
        if event.src_path.lower().endswith('.pdf'):
            self._process_pdf(event.src_path)
    
    def on_modified(self, event):
        """
        Called when a file or directory is modified.
        
        Args:
            event: File system event
        """
        if event.is_directory:
            return
        
        if event.src_path.lower().endswith('.pdf'):
            # Only process if we haven't processed this file yet
            if event.src_path not in self.processed_files:
                self._process_pdf(event.src_path)
    
    def _process_pdf(self, file_path):
        """
        Process and print a PDF file with retry logic.
        
        Args:
            file_path: Path to the PDF file
        """
        with self.processing_lock:
            # Skip if already processed
            if file_path in self.processed_files:
                return
            
            # Add small delay to ensure file is fully written
            time.sleep(self.processing_delay)
            
            file_name = Path(file_path).name
            logging.info(f"Detected new PDF: {file_name}")
            
            # Attempt to print with retries
            for attempt in range(1, self.retry_count + 1):
                try:
                    # Check if file still exists and is accessible
                    if not os.path.exists(file_path):
                        logging.warning(f"File no longer exists: {file_name}")
                        return
                    
                    # Try to open the file to ensure it's not locked
                    with open(file_path, 'rb') as f:
                        pass
                    
                    # Print the PDF
                    logging.info(f"Printing (attempt {attempt}/{self.retry_count}): {file_name}")
                    self._print_pdf(file_path)
                    
                    # Mark as processed
                    self.processed_files.add(file_path)
                    logging.info(f"Successfully printed: {file_name}")
                    return
                    
                except PermissionError:
                    if attempt < self.retry_count:
                        logging.warning(f"File is locked, retrying in {self.retry_delay}s: {file_name}")
                        time.sleep(self.retry_delay)
                    else:
                        logging.error(f"Failed to access file after {self.retry_count} attempts: {file_name}")
                
                except Exception as e:
                    if attempt < self.retry_count:
                        logging.warning(f"Error printing (attempt {attempt}), retrying: {file_name} - {e}")
                        time.sleep(self.retry_delay)
                    else:
                        logging.error(f"Failed to print after {self.retry_count} attempts: {file_name} - {e}")
    
    def _print_pdf(self, file_path):
        """
        Print a single PDF file using Adobe Reader.
        
        Args:
            file_path: Path to the PDF file
        """
        import subprocess
        
        try:
            # Use /t parameter to print the PDF and close Adobe Reader
            subprocess.Popen([self.adobe_reader_path, '/t', str(file_path)],
                           stderr=subprocess.DEVNULL,
                           stdout=subprocess.DEVNULL)
            # Small delay to avoid overwhelming the print queue
            time.sleep(0.5)
        except Exception as e:
            raise Exception(f"Failed to execute Adobe Reader: {e}")


def load_config(config_path):
    """
    Load configuration from JSON file.
    
    Args:
        config_path: Path to configuration file
    
    Returns:
        Configuration dictionary
    """
    default_config = {
        'hot_folder': '',
        'retry_count': 3,
        'retry_delay': 2,
        'processing_delay': 1,
        'log_level': 'INFO',
        'log_file': 'hot_folder.log'
    }
    
    if not os.path.exists(config_path):
        logging.warning(f"Configuration file not found: {config_path}")
        logging.warning("Using default configuration")
        return default_config
    
    try:
        with open(config_path, 'r') as f:
            user_config = json.load(f)
        
        # Merge user config with defaults
        config = default_config.copy()
        config.update(user_config)
        return config
    
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in configuration file: {e}")
        logging.warning("Using default configuration")
        return default_config
    
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        logging.warning("Using default configuration")
        return default_config


def save_default_config(config_path):
    """
    Save a default configuration file.
    
    Args:
        config_path: Path where to save the configuration file
    """
    default_config = {
        'hot_folder': 'C:\\PDFs\\HotFolder',
        'retry_count': 3,
        'retry_delay': 2,
        'processing_delay': 1,
        'log_level': 'INFO',
        'log_file': 'hot_folder.log'
    }
    
    try:
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=4)
        print(f"Default configuration file created: {config_path}")
        print("Please edit this file to set your hot folder path.")
        return True
    except Exception as e:
        print(f"Error creating configuration file: {e}")
        return False


def setup_logging(config):
    """
    Setup logging configuration.
    
    Args:
        config: Configuration dictionary
    """
    log_level = getattr(logging, config.get('log_level', 'INFO').upper())
    log_file = config.get('log_file', 'hot_folder.log')
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """
    Main function to start hot folder monitoring.
    """
    print("=" * 60)
    print("Hot Folder PDF Printer")
    print("Automatic PDF printing when files are added to a folder")
    print("=" * 60)
    
    # Configuration file path
    config_path = 'hot_folder_config.json'
    
    # Check if --create-config option is provided
    if len(sys.argv) > 1 and sys.argv[1] == '--create-config':
        if save_default_config(config_path):
            sys.exit(0)
        else:
            sys.exit(1)
    
    # Load configuration
    config = load_config(config_path)
    
    # Setup logging
    setup_logging(config)
    
    # Get hot folder path
    hot_folder = config.get('hot_folder', '')
    
    # Check for command line argument
    if len(sys.argv) > 1 and sys.argv[1] != '--create-config':
        hot_folder = sys.argv[1]
    
    # Validate hot folder
    if not hot_folder:
        logging.error("Hot folder path not specified.")
        print("\nUsage:")
        print(f"  python {sys.argv[0]} <hot_folder_path>")
        print(f"  python {sys.argv[0]} --create-config")
        print(f"\nOr edit the configuration file: {config_path}")
        sys.exit(1)
    
    hot_folder_path = Path(hot_folder)
    
    if not hot_folder_path.exists():
        logging.error(f"Hot folder does not exist: {hot_folder}")
        print(f"\nError: The specified hot folder does not exist: {hot_folder}")
        print("Please create the folder or specify a valid path.")
        sys.exit(1)
    
    if not hot_folder_path.is_dir():
        logging.error(f"Hot folder path is not a directory: {hot_folder}")
        print(f"\nError: The specified path is not a directory: {hot_folder}")
        sys.exit(1)
    
    # Find Adobe Reader
    logging.info("Searching for Adobe Reader...")
    adobe_reader_path = find_adobe_reader()
    
    if not adobe_reader_path:
        logging.error("Adobe Reader not found")
        print("\nError: Adobe Reader not found. Please check the installation.")
        print("Expected locations:")
        print("  - C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32.exe")
        print("  - C:\\Program Files\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32.exe")
        sys.exit(1)
    
    logging.info(f"Found Adobe Reader: {adobe_reader_path}")
    
    # Kill any existing Adobe Reader instances
    logging.info("Closing any existing Adobe Reader instances...")
    kill_adobe_reader()
    
    # Setup file system observer
    event_handler = PDFPrintHandler(adobe_reader_path, config)
    observer = Observer()
    observer.schedule(event_handler, str(hot_folder_path), recursive=False)
    
    # Start monitoring
    observer.start()
    
    print(f"\nMonitoring hot folder: {hot_folder_path}")
    print(f"Log file: {config.get('log_file', 'hot_folder.log')}")
    print("\nWaiting for PDF files...")
    print("Press Ctrl+C to stop monitoring\n")
    
    logging.info(f"Started monitoring hot folder: {hot_folder_path}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Stopping hot folder monitoring...")
        print("\nStopping hot folder monitoring...")
        observer.stop()
    
    observer.join()
    logging.info("Hot folder monitoring stopped")
    print("Hot folder monitoring stopped.")


if __name__ == "__main__":
    main()
