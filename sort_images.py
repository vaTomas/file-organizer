import os
import shutil
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

def get_date_taken(image_path):
    """
    Extract the date an image was taken from its metadata.
    Returns a string in 'yyyy_MM_dd' format or None if unavailable.
    """
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == "DateTimeOriginal":
                    date_taken = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                    return date_taken.strftime("%Y_%m_%d")
    except Exception as e:
        print(f"Error reading metadata from {image_path}: {e}")
    return None

def organize_images_by_date(src_folder, dest_folder):
    """
    Organizes images from src_folder into subfolders in dest_folder based on the 'Date Taken' property.
    """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for root, _, files in os.walk(src_folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Skip non-image files
                if not file.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.mov')):
                    continue
                
                date_taken = get_date_taken(file_path)
                if date_taken:
                    target_folder = os.path.join(dest_folder, date_taken)
                    if not os.path.exists(target_folder):
                        os.makedirs(target_folder)
                    
                    shutil.move(file_path, os.path.join(target_folder, file))
                    print(f"Moved {file} to {target_folder}")
                else:
                    print(f"No 'Date Taken' found for {file}. Skipping...")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    source_folder = input("Enter the source folder path containing images: ")
    destination_folder = input("Enter the destination folder path: ")

    organize_images_by_date(source_folder, destination_folder)
