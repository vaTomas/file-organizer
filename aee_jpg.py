import os
import shutil

def map_jpg_directories(images_dir):
    """
    Recursively scans the images_dir for .jpg files and returns a mapping:
    { base_filename (without extension): directory containing the .jpg file }
    """
    mapping = {}
    for root, dirs, files in os.walk(images_dir):
        for file in files:
            if file.lower().endswith('.jpg'):
                base = os.path.splitext(file)[0]
                mapping[base] = root
    return mapping

def move_aee_files(aee_dir, jpg_mapping):
    """
    Recursively scans the aee_dir for .aee files. If an aee file's base name exists in jpg_mapping,
    it moves that aee file to the directory of the corresponding .jpg file.
    """
    for root, dirs, files in os.walk(aee_dir):
        for file in files:
            if file.lower().endswith('.aae'):
                base = os.path.splitext(file)[0]
                if base in jpg_mapping:
                    target_dir = jpg_mapping[base]
                    source_file = os.path.join(root, file)
                    target_file = os.path.join(target_dir, file)
                    print(f"Moving {source_file} to {target_file}")
                    try:
                        shutil.move(source_file, target_file)
                    except Exception as e:
                        print(f"Error moving file {source_file}: {e}")
                else:
                    print(f"No matching .jpg file found for {file}")

def main():
    images_dir = input("Enter the directory containing .jpg files: ").strip()
    aee_dir = input("Enter the directory containing .aee files: ").strip()

    if not os.path.isdir(images_dir):
        print(f"Error: '{images_dir}' is not a valid directory.")
        return
    if not os.path.isdir(aee_dir):
        print(f"Error: '{aee_dir}' is not a valid directory.")
        return

    # Map each JPG file's base name to its directory
    jpg_mapping = map_jpg_directories(images_dir)
    if not jpg_mapping:
        print("No .jpg files found in the provided images directory.")
        return

    # Move corresponding AEE files to the directories with matching JPG files
    move_aee_files(aee_dir, jpg_mapping)

if __name__ == '__main__':
    main()
