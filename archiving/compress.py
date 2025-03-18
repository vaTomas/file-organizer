import subprocess
import os

def create_7z_archive(folder_path, archive_path):
    """
    Creates a 7z archive from the specified folder.

    Args:
        folder_path (str): The path to the folder to archive.
        archive_name (str): The desired name of the archive (e.g., "my_archive.7z").
    """

    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        return

    # 7z a -t7z -mx9 -ms16g -v4292m -ssp -stl -spe "D:\programming\sort_folder\test\2005\2005.7z" "D:\programming\sort_folder\test\2005"
    command = [
        "7z",
        "a",
        "-t7z",
        "-mx9",
        "-ms16g",
        "-v4092m",
        "-ssp",
        "-stl",
        "-spe",
        "-sdel",
        archive_path,
        folder_path,
    ]

    try:
        subprocess.run(command, check=True) # check=True will raise an exception if the command fails
        print(f"Archive '{archive_path}' created successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating archive: {e}")
        return False
    except FileNotFoundError:
        print("Error: 7z command not found. Make sure 7-Zip is installed and in your PATH.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def create_par2_recovery(src_files, redundancy_rate = 10, slice_size = 4096):

    for file in src_files:
        if not os.path.exists(file):
            print(f"Error: File or directory not found: {file}")
            return False

    output_directory = src_files[0][:-4] + '.par2'

    command = [
        "par2j64",
        "c",
        f"/rr{redundancy_rate}",
        f"/sm{slice_size}",
        "/lc256", #Max cores (0) + GPU (+256) 
        output_directory
    ]
    command.extend(src_files)

    try:
        subprocess.run(command, check=True)
        print(f"PAR2 recovery files created successfully for: {output_directory}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating PAR2 recovery files: {e}")
        return False
    except FileNotFoundError:
        print("Error: par2 command not found. Make sure it is installed and in your PATH.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def find_paths_starting_with(search_path, filter_str):
    """
    Finds all file and directory paths within a search path that start with a given filter string.

    Args:
        search_path (str): The directory to search within.
        filter_str (str): The string that paths must start with.

    Returns:
        list: A list of full paths that start with the filter string.
    """
    matching_paths = []
    if not os.path.exists(search_path):
        return matching_paths

    for item in os.listdir(search_path):
        full_path = os.path.join(search_path, item)
        if item.startswith(filter_str):
            matching_paths.append(full_path)
    return matching_paths


def archive_and_parchive(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        return

    folder_name = os.path.basename(folder_path)
    output_path = os.path.join(folder_path, folder_name + '.7z')

    if not create_7z_archive(folder_path, output_path):
        return
    
    archive_paths = find_paths_starting_with(folder_path, os.path.basename(output_path))
    create_par2_recovery(archive_paths)


def archive_and_parchive_subfolders(folder_path):

    subfolders = []
    if not os.path.exists(folder_path):
        return subfolders

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            subfolders.append(item_path)

    for folder in subfolders:
        archive_and_parchive(folder)
    


def main():
    folder_path = input("Enter the directory folder: ")
    # archive_and_parchive(folder_path)
    archive_and_parchive_subfolders(folder_path)


if __name__ == "__main__":
    main()