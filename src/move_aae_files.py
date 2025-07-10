import os
import shutil
import re
from datetime import datetime

def get_file_date(file_path):
    """
    Extracts a date from the file. It first tries to find a date tag 
    (e.g., <date>yyyy-MM-ddTHH:mm:ssZ</date>) within the file content.
    If no date tag is found, it falls back to the file's last modification time.

    Args:
        file_path (str): The full path to the file.

    Returns:
        datetime.datetime: The extracted date as a datetime object, or None if no date is found.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Use regex to find any date tag in the content
            match = re.search(r"<date>(.*?)</date>", content)
            if match:
                date_str = match.group(1)
                # Parse the standard ISO 8601 format date
                return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except Exception as e:
        print(f"Could not read file {os.path.basename(file_path)} to find date tag: {e}")

    # Fallback to file modification time if no date tag is found
    try:
        mod_time = os.path.getmtime(file_path)
        return datetime.fromtimestamp(mod_time)
    except OSError as e:
        print(f"Could not get modification time for {os.path.basename(file_path)}: {e}")

    return None

def process_and_move_file(file_path, dest_folder, allowed_exts):
    """
    Processes a single file: checks its type, extracts the date, and moves it.

    Args:
        file_path (str): The full path to the file to process.
        dest_folder (str): The root destination directory.
        allowed_exts (tuple): A tuple of lowercase file extensions to process.
    """
    if not file_path.lower().endswith(allowed_exts):
        return # Skip files that don't match the allowed types

    file_date = get_file_date(file_path)

    if file_date:
        # Create a folder name in yyyy_MM_dd format
        date_folder_name = file_date.strftime("%Y_%m_%d")
        target_folder = os.path.join(dest_folder, date_folder_name)

        # Create the date-specific folder if it doesn't exist
        os.makedirs(target_folder, exist_ok=True)

        # Move the file
        try:
            shutil.move(file_path, os.path.join(target_folder, os.path.basename(file_path)))
            print(f"Moved '{os.path.basename(file_path)}' to '{target_folder}'")
        except Exception as e:
            print(f"Error moving file '{file_path}': {e}")
    else:
        print(f"Could not determine date for '{os.path.basename(file_path)}'. Skipping.")

def sort_files_by_date(src_folder, dest_folder, allowed_file_types, recursive):
    """
    Organizes files into date-stamped folders based on an extracted date.

    Args:
        src_folder (str): The path to the source directory to scan.
        dest_folder (str): The path to the destination directory.
        allowed_file_types (str or tuple or list): File extensions to process.
        recursive (bool): If True, scans all child directories.
    """
    # Normalize allowed_file_types to a tuple of lowercase strings for consistent checks
    if isinstance(allowed_file_types, str):
        allowed_exts = (allowed_file_types.lower(),)
    elif isinstance(allowed_file_types, (list, tuple)):
        allowed_exts = tuple(ext.lower() for ext in allowed_file_types if ext)
    else:
        print("Error: 'allowed_file_types' must be a string, tuple, or list.")
        return
        
    if not allowed_exts:
        print("Error: No allowed file types specified.")
        return

    # Scan directories and process files
    if recursive:
        for root, _, files in os.walk(src_folder):
            for filename in files:
                process_and_move_file(os.path.join(root, filename), dest_folder, allowed_exts)
    else:
        for filename in os.listdir(src_folder):
            file_path = os.path.join(src_folder, filename)
            if os.path.isfile(file_path):
                process_and_move_file(file_path, dest_folder, allowed_exts)

def main():
    """
    Main function to get user input and run the file sorter.
    """
    print("--- File Sorter ---")
    
    # 1. Get and validate the source directory
    src_dir = input("Enter the directory to scan for files: ").strip()
    if not os.path.isdir(src_dir):
        print(f"Error: Source directory '{src_dir}' not found.")
        return

    # 2. Get and create the destination directory
    dest_dir = input("Enter the destination directory for sorted folders: ").strip()
    if not os.path.exists(dest_dir):
        try:
            os.makedirs(dest_dir)
            print(f"Created destination directory: '{dest_dir}'")
        except OSError as e:
            print(f"Error creating destination directory '{dest_dir}': {e}")
            return
            
    # 3. Get allowed file types
    types_input = input("Enter allowed file extensions (comma-separated, e.g. .plist,.jpg): ").strip()
    if not types_input:
        print("Error: You must specify at least one file type.")
        return
    allowed_types = [ft.strip() for ft in types_input.split(',')]

    # 4. Ask about recursive scanning
    recursive_input = input("Do you want to scan child directories? (y/n): ").strip().lower()
    is_recursive = recursive_input == 'y'

    print("\nStarting the sorting process...")
    sort_files_by_date(src_dir, dest_dir, allowed_types, is_recursive)
    print("\nSorting complete.")

if __name__ == "__main__":
    main()