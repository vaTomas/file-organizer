import os
import sys
import math
import subprocess

__parent_dir__ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(__parent_dir__)

from size_of_directory import get_directory_size as get_size
from find_files_by_name import find_files_by_name as find_files
from file_extention_helper import replace_file_extension as replace_file_extension


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


# src_files must not be relative
def create_par2_recovery(src_files, redundancy_rate: int = 10, slice_size_factor: int = 4096, maximum_recovery_file_size: int = 4290772992):
    

    src_files_paths = set()
    for file in src_files:
        if not os.path.exists(file):
            print(f"Error: File or directory not found: {file}")
            return False
        
        if not os.path.isabs(file):
            src_files_paths.add(os.path.abspath(file))

    output_directory = sorted(list(src_files_paths), key=len)[0] + '.par2'
    if os.path.exists(output_directory):
        raise FileExistsError(f"Output file already exists: {output_directory}")

    source_files_size = get_size(src_files_paths)
    recovery_file_count = math.ceil((source_files_size * redundancy_rate/100) / maximum_recovery_file_size)
           

    command = [
        "par2j64",
        "c",
        f"/rr{redundancy_rate}",
        f"/sm{slice_size_factor}",
        "/rd0",
        f"/rf{recovery_file_count}",
        "/lc256", #Max cores (0) + GPU (+256) 
        output_directory
    ]
    command.extend(src_files_paths)

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


def archive_and_parchive(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        return

    folder_name = os.path.basename(folder_path)
    output_path = os.path.join(folder_path, folder_name + '.7z')

    try:
        create_7z_archive(folder_path, output_path)
    except FileExistsError:
        pass
    except Exception as e:
        raise Exception(f"An unknown error occured: {e}")
    
    archive_paths = find_files(folder_path, starts_with=os.path.basename(output_path))

    try:
        create_par2_recovery(archive_paths)
    except FileExistsError:
        return
    except Exception as e:
        raise Exception(f"An unknown error occured: {e}")


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
    archive_and_parchive_subfolders(folder_path)


if __name__ == "__main__":
    main()