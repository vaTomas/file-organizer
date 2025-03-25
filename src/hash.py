import os
import hashlib

def calculate_md5(file_path: str) -> str:
    """
    Calculates the MD5 checksum of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The hexadecimal representation of the MD5 checksum, or None if an error occurs.
    """
    try:
        if not os.path.isfile(file_path):
            return None #file does not exist.

        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    except OSError as e:
        print(f"Error calculating MD5: {e}")
        return None