import os

def delete_empty_folders(start_path):
    deletion_occurred = False
    # Walk the directory tree from the bottom up
    for root, dirs, files in os.walk(start_path, topdown=False):
        # If both subdirectories and files are empty, then the folder is empty
        if not dirs and not files:
            try:
                os.rmdir(root)
                print(f"Deleted empty folder: {root}")
                deletion_occurred = True
            except Exception as e:
                print(f"Error deleting folder {root}: {e}")
    return deletion_occurred

def main():
    starting_directory = input("Please enter the directory to start from: ").strip()
    
    if not os.path.isdir(starting_directory):
        print(f"Error: '{starting_directory}' is not a valid directory.")
        return

    # Continue deleting until no further empty folders are found
    while delete_empty_folders(starting_directory):
        pass

if __name__ == '__main__':
    main()
