import os
from typing import Union, Set, Optional

from find_files_by_name import find_files_by_name as find_files

def get_file_size(file_path) -> int:
    """
    Gets the size of a file in bytes.

    Args:
        file_path (str): The path to the file.

    Returns:
        int: The size of the file in bytes, or None if the file doesn't exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File does not exist: {file_path}")

    try:
        file_size = os.path.getsize(file_path)
        return file_size
    except FileNotFoundError(f"File does not exist: {file_path}"):
        return None
    

def get_folder_size(folder_path):
    """
    Gets the total size of a folder and its subfolders in bytes.

    Args:
        folder_path (str): The path to the folder.

    Returns:
        int: The total size of the folder in bytes, or None if the folder doesn't exist.
    """

    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Folder does not exist or is not a directory: {FileNotFoundError}")

    total_size = 0
    try:
        for dirpath, _, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                total_size += os.path.getsize(file_path)
        return total_size
    except FileNotFoundError:
        return None
    

def get_directory_size(path: Union[str, Set[str]]) -> Optional[int]:
    """
    Gets the total size of a file or a folder and its subfolders in bytes.

    Args:
        folder_path (str): The path to the file, files, or folder.

    Returns:
        int: The total size of the folder in bytes, or None if the file, files, or folder doesn't exist.
    """
    
    if isinstance(path, set): #if set of files or folders
        path = remove_redundant_items_in_set(path)

        size = 0
        for item_path in path:
            if os.path.isdir(item_path):
                size += get_folder_size(item_path)
            else:
                size += get_file_size(item_path)
        return size

    if isinstance(path, str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File or directory not found: {path}")

        if os.path.isdir(path): #if folder
            return get_folder_size(path)
        
        else:
            return get_file_size(path)
        
    return None

        
def remove_redundant_items_in_set(files: Set[str]) -> Set[str]:
    """
    Removes items from the set if they are already contained within a folder in the set.

    Args:
        path (Set[str]): A set of file or folder paths.

    Returns:
        Set[str]: A new set with items removed if contained within a folder.
    """

    folders = {p for p in files if os.path.isdir(p)}
    files = {p for p in files if not os.path.isdir(p)}
    
    items_to_keep = set()

    for file in files:
        is_contained = False
        for folder in folders:
            if os.path.commonpath([file, folder]) == folder:
                if file != folder:
                    is_contained = True
                    break
        if not is_contained:
            items_to_keep.add(file)

    for folder in folders:
        is_contained = False
        for _folder in folders:
            if os.path.commonpath([folder, _folder]) == _folder:
                if folder != _folder:
                    is_contained = True
                    break
        if not is_contained:
            items_to_keep.add(folder) 

    return items_to_keep



def main():
    path = 'test'
    contents = set()
    
    for dirpath, folders, filenames in os.walk(path):
        contents.add(dirpath)
        for folder in folders:
            contents.add(os.path.join(dirpath,folder))
        for filename in filenames:
            contents.add(os.path.join(dirpath,filename))

    # contents = remove_redundant_items_in_set(contents)

    print(get_directory_size(contents))

if __name__ == "__main__":
    main()


