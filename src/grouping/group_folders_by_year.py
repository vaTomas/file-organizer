import os
import shutil

def group_folders_by_year(src_folder, dest_folder):
    """
    Groups folders in the format YYYY_MM_DD by year, creating subfolders in the destination.

    Args:
        src_folder (str): The source folder containing the folders to group.
        dest_folder (str): The destination folder where year-based subfolders will be created.
    """

    if not os.path.exists(src_folder):
        print(f"Error: Source folder '{src_folder}' does not exist.")
        return

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for item in os.listdir(src_folder):
        item_path = os.path.join(src_folder, item)

        if os.path.isdir(item_path):
            year = item.split('_')[0]  # Extract the year from the folder name
            year_folder = os.path.join(dest_folder, year)
            
            if item_path == year_folder:
                continue

            try:
                if not os.path.exists(year_folder):
                    os.makedirs(year_folder)

                dest_item_path = os.path.join(year_folder, item)
                shutil.move(item_path, dest_item_path)

            except (IndexError, ValueError) as e:
                print(f"Warning: Skipping '{item}'. Invalid folder name format or other error: {e}")


def main():
    # Ask the user for the directories
    scan_dir = input("Enter the directory to scan for folders: ").strip()
    dest_dir = input("Enter the destination directory for grouped folders: ").strip()

    if not os.path.isdir(scan_dir):
        print(f"Error: '{scan_dir}' is not a valid directory.")
        return

    if not os.path.exists(dest_dir):
        try:
            os.makedirs(dest_dir)
        except Exception as e:
            print(f"Error creating destination directory '{dest_dir}': {e}")
            return

    group_folders_by_year(scan_dir, dest_dir)

if __name__ == '__main__':
    main()