import os
import shutil
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from datetime import datetime

def get_media_created(file_path):
    """
    Extract the media creation date from the file metadata.
    Returns a string in 'yyyy_MM_dd' format or None if unavailable.
    """
    try:
        parser = createParser(file_path)
        if not parser:
            print(f"Unable to parse {file_path}")
            return None
        metadata = extractMetadata(parser)
        if metadata and metadata.has("creation_date"):
            creation_date = metadata.get("creation_date")
            return creation_date.strftime("%Y_%m_%d")
    except Exception as e:
        print(f"Error reading metadata from {file_path}: {e}")
    return None

def organize_mov_files_by_date(src_folder, dest_folder):
    """
    Organizes .MOV files from src_folder into subfolders in dest_folder
    based on the 'Media Created' property.
    """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for root, _, files in os.walk(src_folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Skip non-MOV files
                if not file.lower().endswith('.mov'):
                    continue
                
                media_created_date = get_media_created(file_path)
                if media_created_date:
                    target_folder = os.path.join(dest_folder, media_created_date)
                    if not os.path.exists(target_folder):
                        os.makedirs(target_folder)
                    
                    shutil.move(file_path, os.path.join(target_folder, file))
                    print(f"Moved {file} to {target_folder}")
                else:
                    print(f"No 'Media Created' date found for {file}. Skipping...")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    source_folder = input("Enter the source folder path containing .MOV files: ")
    destination_folder = input("Enter the destination folder path: ")

    organize_mov_files_by_date(source_folder, destination_folder)
