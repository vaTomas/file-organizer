import os

def append_file_extension(path: str, file_extension: str):
    """
    Appends the .file extension to a file path if it doesn't already have it.

    Args:
        file_path (str): The file path.
        file_extension (str): The file extension.

    Returns:
        str: The file path with the .file extension appended, or the original path if it already has it.
    """
    if not isinstance(path, str):
        raise TypeError("Path must be a string representation of a path.")
    if not isinstance(file_extension, str):
        raise TypeError("Extension must be a string representation of a file extension.")
    
    if not file_extension.startswith('.'):
        file_extension = '.' + file_extension

    if path.lower().endswith(file_extension.lower()):
        return path

    return path + file_extension
    
    

def replace_file_extension(path: str, new_extension: str):
    """
    Replaces the extension of a file with a new extension.

    Args:
        filepath (str): The path to the file.
        new_extension (str): The new file extension (e.g., ".txt", ".jpg").

    Returns:
        Optional[str]: The new file path with the replaced extension,
                       or None if the input filepath is invalid.
    """
    if not isinstance(path, str):
        raise TypeError("Path must be a string representation of a path.")
    if not isinstance(new_extension, str):
        raise TypeError("Extension must be a string representation of a file extension.")

    if not new_extension.startswith('.'):
        new_extension = '.' + new_extension

    if path.lower().endswith(new_extension.lower()):
        return path

    directory, filename = os.path.split(path)
    filename_without_ext, _ = os.path.splitext(filename)
    new_filename = filename_without_ext + new_extension
    new_filepath = os.path.join(directory, new_filename)
    return new_filepath