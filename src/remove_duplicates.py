import os
import shutil
from typing import Set, List
from hash import calculate_md5 as get_md5
from size_of_directory import get_file_size as get_file_size
from find_files_by_name import find_files_by_name as find_files


def find_duplicates(path: str, file_types_allowed: List[str]) -> Set[str]:
    if not os.path.isdir(path):
        return NotADirectoryError(f"Path is not a directory: {path}")

    files = set()
    for file_type in file_types_allowed:
        if not file_type.startswith('.'):
            file_type = '.' + file_type

        files.update(find_files(path, ends_with=file_type, search_subdir=True))
    
    file_hosts = {} # key: MD5, value: size
    duplicate_files = set()
    
    for file in files:
        size = get_file_size(file)
        if not size:
            continue

        file_hash = get_md5(file)

        if size not in file_hosts.values():
            file_hosts[file_hash] = size
        else:
            if file_hosts.get(file_hash) == size:
                duplicate_files.add(file)         
           
    return duplicate_files

def move_to_duplicates(file: str, dir_path: str) -> None:
    """
    Moves a file to a "duplicates" subdirectory within the given directory.

    Args:
        file (str): The path to the file to move.
        dir_path (str): The path to the directory where the "duplicates" subdirectory will be created.
    """
    duplicates_dir = os.path.join(dir_path, "duplicates")

    try:
        os.makedirs(duplicates_dir, exist_ok=True)  # Create directory if it doesn't exist
        shutil.move(file, duplicates_dir)
        print(f"Moved '{file}' to '{duplicates_dir}'")
    except FileNotFoundError:
        print(f"Error: File '{file}' not found.")
    except OSError as e:
        print(f"Error moving '{file}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    dir_path = input("Path: ")
    if not os.path.isdir(dir_path):
        return NotADirectoryError(f"Path is not a directory: {dir_path}")
    
    file_types = {'.png', '.jpg', '.mp4', '.mov'}
    duplicate_files = find_duplicates(dir_path, file_types)

    

    for file in duplicate_files:
        move_to_duplicates(file, os.path.dirname(file))


if __name__ == "__main__":
    main()


    