import os
import shutil

def sort_by_matching_name(src_path, dest_path, allowed_src_file_types=None, allowed_dest_file_types=None):
    """
    Move files from match_path to the directory containing a file in src_path with the same base name.
    
    Parameters:
      src_path (str): The directory (and its subfolders) containing files to be moved.
      dest_path (str): The directory (and its subfolders) where matching files reside.
      allowed_src_file_types (list or None): List of allowed extensions (e.g. ['.modd']) for source files.
                                              If None, all source file types are allowed.
      allowed_dest_file_types (list or None): List of allowed extensions (e.g. ['.jpg', '.png']) for destination match files.
                                              If None, all match file types are allowed.
    """
    # Prepare allowed extensions as tuples (lowercased) if provided.
    if allowed_src_file_types is not None:
        allowed_src_file_types = tuple(ext.lower() for ext in allowed_src_file_types)
    if allowed_dest_file_types is not None:
        allowed_dest_file_types = tuple(ext.lower() for ext in allowed_dest_file_types)
    
    # Build a mapping from base filename (without extension) to the directory in src_path.
    src_map = {}
    for root, _, files in os.walk(src_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if not (allowed_src_file_types is None or ext in allowed_src_file_types):
                continue

            base = os.path.splitext(file)[0]
            file_path = os.path.join(root, file)
            # In case multiple files have the same base, the last one found will be used.
            src_map[base] = file_path

    # Process files in match_path.
    for root, _, files in os.walk(dest_path):
        for file in files:

            ext = os.path.splitext(file)[1].lower()
            if not (allowed_dest_file_types is None or ext in allowed_dest_file_types):
                continue

            matched_key = None
            for key in src_map:
                if file.startswith(key):
                    matched_key = key
                    break

            if matched_key is None:
                continue

            src_file_path = src_map[matched_key]
            dest_file_path = os.path.join(root, os.path.basename(src_file_path))

            
            try:
                shutil.move(src_file_path, dest_file_path)
                print(f"Moved '{src_file_path}' to '{dest_file_path}'")
            except Exception as e:
                print(f"Error moving '{src_file_path}' to '{dest_file_path}': {e}")

                


def main():
    src_path = input("Enter the source folder path (files to be moved): ").strip()
    match_path = input("Enter the destination folder path (where matching files reside): ").strip()

    allowed_src_input = input("Enter allowed source file types (comma separated, e.g. .abc) or leave blank for all: ").strip()
    allowed_src_file_types = [ext.strip() for ext in allowed_src_input.split(',')] if allowed_src_input else None

    allowed_match_input = input("Enter allowed match file types (comma separated, e.g. .efg,.def) or leave blank for all: ").strip()
    allowed_match_file_types = [ext.strip() for ext in allowed_match_input.split(',')] if allowed_match_input else None

    if not os.path.isdir(src_path):
        print(f"Error: '{src_path}' is not a valid directory.")
        return
    if not os.path.isdir(match_path):
        print(f"Error: '{match_path}' is not a valid directory.")
        return

    sort_by_matching_name(src_path, match_path, allowed_src_file_types, allowed_match_file_types)

    # sort_by_matching_name(r"test/src", r"test/mat")


if __name__ == '__main__':
    main()
