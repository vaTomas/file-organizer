import os
from datetime import datetime
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
import shutil
import pytz
from win32com.propsys import propsys, pscon

def extract_date_taken(file_path):
    """
    Extracts the date a video or image was taken from its metadata.
    Returns a string in 'yyyy_MM_dd' format or None if unavailable.
    """
    try:
        file_path = Path(file_path)
        if file_path.suffix.lower() in {'.jpg', '.jpeg', '.png'}:
            # Handle image files
            image = Image.open(file_path)
            exif_data = image._getexif()
            if exif_data is not None:
                for tag, value in exif_data.items():
                    if TAGS.get(tag) == "DateTimeOriginal":
                        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S").strftime("%Y_%m_%d")
        elif file_path.suffix.lower() in {'.mp4', '.mov', '.avi'}:
            # Handle video files using win32com
            properties = propsys.SHGetPropertyStoreFromParsingName(str(file_path))
            dt = properties.GetValue(pscon.PKEY_Media_DateEncoded).GetValue()
            if not isinstance(dt, datetime):
                dt = datetime.fromtimestamp(int(dt))
                dt = dt.replace(tzinfo=pytz.timezone('UTC'))
            dt_local = dt.astimezone(pytz.timezone('Asia/Tokyo'))  # Convert to desired timezone
            return dt_local.strftime("%Y_%m_%d")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    return None

def organize_media_by_date(src_folder, dest_folder):
    """
    Organizes images and videos from src_folder into subfolders in dest_folder
    based on the 'Date Taken' property. Folder names are in 'yyyy_MM_dd' format.
    """
    src_folder = Path(src_folder)
    dest_folder = Path(dest_folder)
    dest_folder.mkdir(parents=True, exist_ok=True)

    for file_path in src_folder.iterdir():
        if file_path.is_file():
            date_taken = extract_date_taken(file_path)
            if date_taken:
                target_folder = dest_folder / date_taken
                target_folder.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file_path), target_folder)
                print(f"Moved {file_path.name} to {target_folder}")
            else:
                print(f"Date metadata not found for {file_path.name}")

if __name__ == "__main__":
    src_folder = input("Enter the source folder path: ").strip()
    dest_folder = input("Enter the destination folder path: ").strip()

    organize_media_by_date(src_folder, dest_folder)
