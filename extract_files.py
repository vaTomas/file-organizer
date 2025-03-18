import os
import shutil

def extract_and_move_files(src_folder, dest_folder, allowed_file_types=None):
    """
    Extracts all files (or files of specified types) from folders and subfolders
    and moves them to the destination folder.

    Args:
        src_folder (str): The source folder containing files and subfolders.
        dest_folder (str): The destination folder where files will be moved.
        allowed_file_types (list, optional): A list of allowed file extensions (e.g., ['.txt', '.jpg']).
                                            If None, all files are moved.
    """

    if not os.path.exists(src_folder):
        print(f"Error: Source folder '{src_folder}' does not exist.")
        return

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for root, _, files in os.walk(src_folder):
        for file in files:
            file_path = os.path.join(root, file)
            _, file_extension = os.path.splitext(file)

            if allowed_file_types is None or file_extension.lower() in allowed_file_types:
                dest_file_path = os.path.join(dest_folder, file)
                try:
                    shutil.move(file_path, dest_file_path)
                    print(f"Moved: {file_path} to {dest_file_path}")
                except Exception as e:
                    print(f"Error moving {file_path}: {e}")


def main():
    # Ask the user for directories
    scan_dir = input("Enter the directory to scan for files: ").strip()
    target_dir = input("Enter the target directory to place the files: ").strip()

    if not os.path.isdir(scan_dir):
        print(f"Error: '{scan_dir}' is not a valid directory.")
        return
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    allowed_types_input = input("Allowed file types/extensions (comma separated, e.g. .jpg,.png): ").strip()
    allowed_file_types = [ft.strip() for ft in allowed_types_input.split(',') if ft.strip()] if allowed_types_input else None

    # Move files that match the criteria
    extract_and_move_files(scan_dir, target_dir, allowed_file_types)

if __name__ == '__main__':
    main()