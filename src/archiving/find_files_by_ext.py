import os

def find_files_by_ext(
        directory: str,
        extensions = None,
        search_subdir: bool = True
):
    """
    Finds all files given an extention in the given directory and its subdirectories.

    Args:
        directory (str): The directory to search.
        extentions (str): The extention to search.
        extentions (list, tupple, set): The extentions to search.
        extentions (None): The extentions to search. None if all extentions.

    Returns:
        set: A set of full file paths to files.
    """
    if not isinstance(directory, str):
        raise TypeError("Directory must be a string representing a directory path.")
    
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"Path is not a directory: {directory}")
    
    if extensions is not None and not isinstance(extensions, (str, tuple, list, set)):
        raise TypeError("Extensions must be a string, list, tuple, set, or None.")
    
    if isinstance(extensions, str):
        extensions = {extensions}

    if extensions is not None:
        extensions = {ext.lower() if ext.startswith('.') else '.' + ext.lower() for ext in extensions}

    files_found = set()

    if search_subdir:
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                _, ext = os.path.splitext(filename)
                if extensions is None or ext.lower() in extensions:
                    full_path = os.path.join(root, filename)
                    files_found.add(full_path)
    
    else:
        for filename in os.listdir(directory):
            full_path = os.path.join(directory, filename)
            if os.path.isfile(full_path):
                _, ext = os.path.splitext(filename)
                if extensions is None or ext.lower() in extensions:
                    files_found.add(full_path)

    return files_found
    
    

def main():
    search_directory = r"test"


    print("==== Test 1 ==== ")
    files = find_files_by_ext(search_directory)
    for file in files:
        print(file)


    print("==== Test 2 ==== ")
    files = find_files_by_ext(search_directory, '.txt')
    for file in files:
        print(file)


    print("==== Test 3 ==== ")
    files = find_files_by_ext(search_directory, 'txt')
    for file in files:
        print(file)


    print("==== Test 4 ==== ")
    files = find_files_by_ext(search_directory, {'txt', '.mp4'})
    for file in files:
        print(file)


    print("==== Test 5 ==== ")
    files = find_files_by_ext(search_directory, search_subdir=False)
    for file in files:
        print(file)

if __name__ == "__main__":
    main()