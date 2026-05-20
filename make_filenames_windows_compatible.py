r"""
# TASK
Write a Python script that takes a list of filenames and makes them compatible with Windows by replacing any invalid characters with an underscore (_). The invalid characters for Windows filenames are: < > : " / \ | ? *
Also: handle the long filename issue by truncating filenames to a maximum of 255 characters, including the file extension.

# ROLE
Expert Python Developer

# INPUT DIRECTORY
./
AND: any other subdirectories

# OUTPUT
The script should output the modified filenames in the same directory, replacing the original files with the new names.

# RUN-STATS
- Files Processed: 0
- Files Renamed: 0
- Time taken: 0 seconds
"""

import os
import re
import time
from pathlib import Path


# Windows invalid filename characters
INVALID_WINDOWS_CHARS = r'[<>:"/\\|?*]'
MAX_FILENAME_LENGTH = 255


def make_filename_windows_compatible(filename):
    """
    Convert a filename to be Windows-compatible by:
    1. Replacing invalid characters with underscores
    2. Truncating to 255 characters (including extension)
    
    Args:
        filename (str): The original filename
        
    Returns:
        str: The Windows-compatible filename
    """
    # Replace invalid characters with underscores
    compatible_name = re.sub(INVALID_WINDOWS_CHARS, '_', filename)
    
    # Handle length limitation (255 chars max including extension)
    if len(compatible_name) > MAX_FILENAME_LENGTH:
        # Split into name and extension
        name_parts = compatible_name.rsplit('.', 1)
        if len(name_parts) == 2:
            name, ext = name_parts
            ext = '.' + ext
            # Calculate available length for name
            max_name_length = MAX_FILENAME_LENGTH - len(ext)
            compatible_name = name[:max_name_length] + ext
        else:
            # No extension, just truncate
            compatible_name = compatible_name[:MAX_FILENAME_LENGTH]
    
    return compatible_name


def process_directory(root_dir='.'):
    """
    Process all files in the directory and subdirectories,
    renaming them to be Windows-compatible.
    
    Args:
        root_dir (str): The root directory to start from (default: current directory)
        
    Returns:
        tuple: (files_processed, files_renamed)
    """
    files_processed = 0
    files_renamed = 0
    
    # Walk through all directories and subdirectories
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            files_processed += 1
            
            # Get the compatible name
            compatible_name = make_filename_windows_compatible(filename)
            
            # Only rename if the name changed
            if filename != compatible_name:
                old_path = os.path.join(dirpath, filename)
                new_path = os.path.join(dirpath, compatible_name)
                
                try:
                    # Handle case where new filename already exists
                    if os.path.exists(new_path) and old_path != new_path:
                        print(f"⚠️  Skipped (target exists): {filename} → {compatible_name}")
                    else:
                        os.rename(old_path, new_path)
                        print(f"✓ Renamed: {filename} → {compatible_name}")
                        files_renamed += 1
                except Exception as e:
                    print(f"✗ Error renaming {filename}: {e}")
    
    return files_processed, files_renamed


def main():
    """Main function to process the current directory."""
    start_time = time.time()
    
    print("=" * 70)
    print("Windows-Compatible Filename Converter")
    print("=" * 70)
    print(f"Starting scan of: {os.path.abspath('.')}\n")
    
    # Process the directory
    files_processed, files_renamed = process_directory('.')
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Print results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Files Processed: {files_processed}")
    print(f"Files Renamed: {files_renamed}")
    print(f"Time taken: {elapsed_time:.2f} seconds")
    print("=" * 70)


if __name__ == "__main__":
    main()