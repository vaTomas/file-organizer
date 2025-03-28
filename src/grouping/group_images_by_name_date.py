import os
import re
import shutil

def sort_files(scan_dir, dest_dir, allowed_file_types=None):
    # Ensure the destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Regex patterns for date prefixes
    pattern1 = re.compile(r'^(\d{4})(\d{2})(\d{2})_')
    pattern2 = re.compile(r'^(\d{4})-(\d{2})-(\d{2})')
    
    # Walk the scan directory recursively
    for root, dirs, files in os.walk(scan_dir):
        for file in files:
            # If allowed_file_types is specified, check the file extension
            if allowed_file_types:
                ext = os.path.splitext(file)[1].lower()
                allowed = [ft.lower().strip() for ft in allowed_file_types]
                if ext not in allowed:
                    continue

            date_str = None
            # Check for the first format: yyyyMMdd_
            match = pattern1.match(file)
            if match:
                year, month, day = match.groups()
                date_str = f"{year}_{month}_{day}"
            else:
                # Check for the second format: yyyy-MM-dd
                match = pattern2.match(file)
                if match:
                    year, month, day = match.groups()
                    date_str = f"{year}_{month}_{day}"
            
            if date_str:
                # Create the destination folder for the date if it doesn't exist
                folder_path = os.path.join(dest_dir, date_str)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                
                source_file = os.path.join(root, file)
                dest_file = os.path.join(folder_path, file)
                
                try:
                    shutil.move(source_file, dest_file)
                    print(f"Moved '{source_file}' to '{dest_file}'")
                except Exception as e:
                    print(f"Error moving file '{source_file}': {e}")

def main():
    # Ask the user for the directories
    scan_dir = input("Enter the directory to scan for image files: ").strip()
    dest_dir = input("Enter the destination directory for sorted folders: ").strip()

    if not os.path.isdir(scan_dir):
        print(f"Error: '{scan_dir}' is not a valid directory.")
        return

    if not os.path.exists(dest_dir):
        try:
            os.makedirs(dest_dir)
        except Exception as e:
            print(f"Error creating destination directory '{dest_dir}': {e}")
            return

    # Ask user for allowed file types
    allowed_types_input = input("Enter allowed file types/extensions (comma separated, e.g. .jpg,.png) or leave blank for all files: ").strip()
    allowed_file_types = [ft.strip() for ft in allowed_types_input.split(',')] if allowed_types_input else None

    sort_files(scan_dir, dest_dir, allowed_file_types)

if __name__ == '__main__':
    main()
