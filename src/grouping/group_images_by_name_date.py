import os
import re
import shutil

def sort_files(scan_dir, dest_dir, allowed_file_types=None):
    """
    Scans a directory for files with date-prefixed names, and moves them 
    into subfolders named with the date.

    Args:
        scan_dir (str): The directory to scan for files.
        dest_dir (str): The root directory where sorted folders will be created.
        allowed_file_types (list, optional): A list of file extensions to process 
                                             (e.g., ['.jpg', '.png']). 
                                             If None, all files are considered.
    """
    # Ensure the destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # A list of regex patterns to match different date prefixes.
    # The script will check for:
    # 1. yyyyMMdd_...
    # 2. yyyy-MM-dd...
    # 3. yyyy_mm_dd_...
    patterns = [
        re.compile(r'^(\d{4})(\d{2})(\d{2})_'),
        re.compile(r'^(\d{4})-(\d{2})-(\d{2})'),
        re.compile(r'^(\d{4})_(\d{2})_(\d{2})_')
    ]
    
    # Walk the scan directory recursively
    print(f"Scanning '{scan_dir}'...")
    for root, dirs, files in os.walk(scan_dir):
        for file in files:
            # If allowed_file_types is specified, check the file extension
            if allowed_file_types:
                ext = os.path.splitext(file)[1].lower()
                # Ensure the allowed types list is clean (lowercase, no whitespace)
                allowed = [ft.lower().strip() for ft in allowed_file_types]
                if ext not in allowed:
                    continue

            date_str = None
            # Check the filename against each pattern
            for pattern in patterns:
                match = pattern.match(file)
                if match:
                    year, month, day = match.groups()
                    # Create a consistent folder name format: YYYY_MM_DD
                    date_str = f"{year}_{month}_{day}"
                    break  # Exit the loop once a match is found
            
            if date_str:
                # Create the destination folder for the date if it doesn't exist
                folder_path = os.path.join(dest_dir, date_str)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                
                source_file = os.path.join(root, file)
                dest_file = os.path.join(folder_path, file)
                
                # Avoid moving a file to the same location if script is run on dest_dir
                if source_file == dest_file:
                    continue

                try:
                    shutil.move(source_file, dest_file)
                    print(f"Moved '{source_file}' to '{dest_file}'")
                except Exception as e:
                    print(f"Error moving file '{source_file}': {e}")

    print("File sorting complete.")

def main():
    """
    Main function to get user input and run the file sorter.
    """
    # Ask the user for the directories
    scan_dir = input("Enter the directory to scan for files: ").strip()
    dest_dir = input("Enter the destination directory for sorted folders: ").strip()

    # Validate the scan directory
    if not os.path.isdir(scan_dir):
        print(f"Error: Scan directory '{scan_dir}' is not a valid directory.")
        return

    # Create the destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        try:
            os.makedirs(dest_dir)
            print(f"Created destination directory: '{dest_dir}'")
        except Exception as e:
            print(f"Error creating destination directory '{dest_dir}': {e}")
            return

    # Ask user for allowed file types
    allowed_types_input = input("Enter allowed file extensions (comma separated, e.g. .jpg,.png) or leave blank for all files: ").strip()
    allowed_file_types = [ft.strip() for ft in allowed_types_input.split(',')] if allowed_types_input else None

    sort_files(scan_dir, dest_dir, allowed_file_types)

if __name__ == '__main__':
    main()
