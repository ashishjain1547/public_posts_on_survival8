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
import sys
from pathlib import Path


# Windows invalid filename characters
INVALID_WINDOWS_CHARS = r'[<>:"/\\|?*]'
MAX_FILENAME_LENGTH = 255
MAX_PATH_LENGTH = 260  # Windows MAX_PATH limit


def make_filename_windows_compatible(filename, dirpath=''):
    """
    Convert a filename to be Windows-compatible by:
    1. Replacing invalid characters with underscores
    2. Truncating to 255 characters (filename only)
    3. Ensuring full path doesn't exceed 260 characters (Windows MAX_PATH)
    
    Args:
        filename (str): The original filename
        dirpath (str): The directory path (for full path validation)
        
    Returns:
        str: The Windows-compatible filename
    """
    # Replace invalid characters with underscores
    compatible_name = re.sub(INVALID_WINDOWS_CHARS, '_', filename)
    
    # Handle individual filename length limitation (255 chars max)
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
    
    # Handle full path length limitation (260 chars max for Windows)
    if dirpath:
        full_path = os.path.join(dirpath, compatible_name)
        if len(full_path) > MAX_PATH_LENGTH:
            # We need to truncate further
            name_parts = compatible_name.rsplit('.', 1)
            if len(name_parts) == 2:
                name, ext = name_parts
                ext = '.' + ext
                # Calculate available space
                prefix_len = len(dirpath) + 1  # +1 for separator
                available = MAX_PATH_LENGTH - prefix_len - len(ext)
                if available > 0:
                    compatible_name = name[:available] + ext
                else:
                    # Last resort: very aggressive truncation
                    compatible_name = name[:MAX_PATH_LENGTH - prefix_len - len(ext) - 1] + ext if ext else compatible_name[:available]
            else:
                # No extension
                prefix_len = len(dirpath) + 1
                available = MAX_PATH_LENGTH - prefix_len
                if available > 0:
                    compatible_name = compatible_name[:available]
    
    return compatible_name


def process_directory(root_dir='.'):
    """
    Process all files and directories in the directory tree,
    renaming them to be Windows-compatible.
    
    Args:
        root_dir (str): The root directory to start from (default: current directory)
        
    Returns:
        tuple: (items_processed, items_renamed)
    """
    items_processed = 0
    items_renamed = 0
    
    # Walk through all directories and subdirectories (bottom-up to handle renames)
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # Process directories (bottom-up to avoid path issues)
        for dirname in dirnames:
            items_processed += 1
            
            # Get the compatible name (pass parent directory path for path length check)
            compatible_name = make_filename_windows_compatible(dirname, dirpath)
            
            # Only rename if the name changed
            if dirname != compatible_name:
                old_path = os.path.join(dirpath, dirname)
                new_path = os.path.join(dirpath, compatible_name)
                
                try:
                    # Handle case where new directory already exists
                    if os.path.exists(new_path) and old_path != new_path:
                        print(f"⚠️  Skipped (target exists): {dirname}/ → {compatible_name}/")
                    else:
                        os.rename(old_path, new_path)
                        print(f"✓ Renamed: {dirname}/ → {compatible_name}/ (path: {len(new_path)} chars)")
                        items_renamed += 1
                except Exception as e:
                    print(f"✗ Error renaming directory {dirname}: {e}")
        
        # Process files
        for filename in filenames:
            items_processed += 1
            
            # Get the compatible name (pass directory path for full path validation)
            compatible_name = make_filename_windows_compatible(filename, dirpath)
            
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
                        print(f"✓ Renamed: {filename} → {compatible_name} (path: {len(new_path)} chars)")
                        items_renamed += 1
                except Exception as e:
                    print(f"✗ Error renaming {filename}: {e}")
    
    return items_processed, items_renamed


def main():
    """Main function to process the current directory or specified directory."""
    # Get target directory from command line or use current directory
    target_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    # Validate the directory exists
    if not os.path.isdir(target_dir):
        print(f"Error: Directory '{target_dir}' does not exist.")
        sys.exit(1)
    
    start_time = time.time()
    
    print("=" * 70)
    print("Windows-Compatible Filename Converter")
    print("=" * 70)
    print(f"Starting scan of: {os.path.abspath(target_dir)}\n")
    
    # Process the directory
    items_processed, items_renamed = process_directory(target_dir)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Print results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Items Processed: {items_processed}")
    print(f"Items Renamed: {items_renamed}")
    print(f"Time taken: {elapsed_time:.2f} seconds")
    print("=" * 70)


if __name__ == "__main__":
    main()