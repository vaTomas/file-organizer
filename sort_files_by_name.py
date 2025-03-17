import os
import shutil

def file_matches(filename, startswith=None, endswith=None, contains=None, match_case=False, allowed_file_types=None):
    """
    Check if a given filename matches the filtering criteria.
    
    Parameters:
      filename (str): Name of the file.
      startswith (str): Filename must start with this string.
      endswith (str): Filename must end with this string.
      contains (str): Filename must contain this substring.
      match_case (bool): Whether the match is case sensitive.
      allowed_file_types (list): List of allowed file extensions (e.g., ['.jpg', '.png']).
    
    Returns:
      bool: True if the filename matches all criteria; False otherwise.
    """
    test_name = filename if match_case else filename.lower()
    
    # Check allowed file types if provided
    if allowed_file_types:
        ext = os.path.splitext(filename)[1]
        allowed_types = allowed_file_types if match_case else [ft.lower() for ft in allowed_file_types]
        if ext.lower() not in allowed_types:
            return False

    if startswith:
        sw = startswith if match_case else startswith.lower()
        if not test_name.startswith(sw):
            return False

    if endswith:
        ew = endswith if match_case else endswith.lower()
        if not test_name.endswith(ew):
            return False

    if contains:
        sub = contains if match_case else contains.lower()
        if sub not in test_name:
            return False

    return True

def sort_files(scan_dir, target_dir, startswith=None, endswith=None, contains=None, match_case=False, allowed_file_types=None):
    """
    Recursively scans the scan_dir and moves files that match the criteria into target_dir.
    """
    # Ensure the target directory exists
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for root, dirs, files in os.walk(scan_dir):
        for file in files:
            if file_matches(file, startswith, endswith, contains, match_case, allowed_file_types):
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_dir, file)
                try:
                    shutil.move(source_file, target_file)
                    print(f"Moved: {source_file} -> {target_file}")
                except Exception as e:
                    print(f"Error moving {source_file}: {e}")

def main():
    # Ask the user for directories
    scan_dir = input("Enter the directory to scan for files: ").strip()
    target_dir = input("Enter the target directory to place the files: ").strip()

    if not os.path.isdir(scan_dir):
        print(f"Error: '{scan_dir}' is not a valid directory.")
        return
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Ask the user for filtering criteria
    print("\nProvide filtering criteria (leave blank if not needed):")
    startswith = input("File should start with: ").strip() or None
    endswith = input("File should end with: ").strip() or None
    contains = input("File should contain: ").strip() or None
    match_case_input = input("Case sensitive matching? (y/n): ").strip().lower()
    match_case = True if match_case_input == 'y' else False
    allowed_types_input = input("Allowed file types/extensions (comma separated, e.g. .jpg,.png): ").strip()
    allowed_file_types = [ft.strip() for ft in allowed_types_input.split(',') if ft.strip()] if allowed_types_input else None

    # Move files that match the criteria
    sort_files(scan_dir, target_dir, startswith, endswith, contains, match_case, allowed_file_types)

if __name__ == '__main__':
    main()
