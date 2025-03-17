import os
import random
import string

def generate_random_folder_name(length=8):
    """Generate a random folder name consisting of alphabetic characters."""
    return ''.join(random.choices(string.ascii_letters, k=length))

def create_random_folders(current_dir, current_depth, max_depth, max_folders):
    """Recursively create random folders up to a specified depth and number per level."""
    if current_depth > max_depth:
        return

    # Decide a random number of subfolders for this level (0 to max_folders)
    num_folders = random.randint(0, max_folders)
    for _ in range(num_folders):
        folder_name = generate_random_folder_name()
        new_folder_path = os.path.join(current_dir, folder_name)
        try:
            os.makedirs(new_folder_path, exist_ok=True)
            print(f"Created folder: {new_folder_path}")
        except Exception as e:
            print(f"Error creating folder {new_folder_path}: {e}")
            continue

        # Recursively create subfolders within the newly created folder
        create_random_folders(new_folder_path, current_depth + 1, max_depth, max_folders)


def main():
    base_dir = input("Enter the base directory where random folders will be created: ").strip()
    if not os.path.exists(base_dir):
        try:
            os.makedirs(base_dir)
            print(f"Created base directory: {base_dir}")
        except Exception as e:
            print(f"Error creating base directory '{base_dir}': {e}")
            return

    try:
        max_depth = int(input("Enter the maximum subfolder depth: ").strip())
        max_folders = int(input("Enter the maximum number of folders per level: ").strip())
    except ValueError:
        print("Please enter valid integer values for maximum depth and number of folders.")
        return

    create_random_folders(base_dir, current_depth=1, max_depth=max_depth, max_folders=max_folders)
    print("Folder creation complete.")


if __name__ == '__main__':
    main()
