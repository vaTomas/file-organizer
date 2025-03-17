import os
import shutil
import pytz
import datetime
from win32com.propsys import propsys, pscon

def get_media_created_date(filepath, target_timezone):
    """
    Extracts the media created date from a file's metadata.
    Returns a datetime object localized to the target timezone (e.g. 'Asia/Tokyo')
    in 'yyyy_MM_dd' format or None if unavailable.
    """
    try:
        properties = propsys.SHGetPropertyStoreFromParsingName(filepath)
        dt = properties.GetValue(pscon.PKEY_Media_DateEncoded).GetValue()
        # If the property is not already a datetime, convert it from a timestamp.
        if not isinstance(dt, datetime.datetime):
            dt = datetime.datetime.fromtimestamp(int(dt))
            dt = dt.replace(tzinfo=pytz.timezone('UTC'))
        # Convert the date to the target timezone
        target_tz = pytz.timezone(target_timezone)
        dt_converted = dt.astimezone(target_tz)
        return dt_converted
    except Exception as e:
        print(f"Error extracting media created date from '{filepath}': {e}")
        return None

def sort_by_media_created(src_folder, dest_folder, allowed_file_types=None, timezone='UTC'):
    """
    Scans the src_folder (recursively) and moves files into subfolders within dest_folder
    based on the file's media created date. The subfolder names are in the format yyyy_MM_dd.
    
    Parameters:
      src_folder (str): The directory to scan.
      dest_folder (str): The directory where sorted subfolders will be created.
      allowed_file_types (list): List of allowed file extensions (e.g. ['.jpg', '.png']). If None, all files are processed.
      timezone (str): The target timezone (e.g. 'UTC', 'Asia/Tokyo') for the media created date.
    """
    if not os.path.isdir(src_folder):
        print(f"Source folder '{src_folder}' does not exist.")
        return
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    # Prepare allowed file extensions tuple (lowercase) if provided.
    if allowed_file_types:
        allowed_exts = tuple(ext.lower() for ext in allowed_file_types)
    else:
        allowed_exts = None

    for root, _, files in os.walk(src_folder):
        for file in files:
            # Skip files that do not match allowed file types.
            if allowed_exts and not file.lower().endswith(allowed_exts):
                continue
            
            src_path = os.path.join(root, file)
            dt = get_media_created_date(src_path, timezone)
            if dt:
                folder_name = dt.strftime("%Y_%m_%d")
                target_folder = os.path.join(dest_folder, folder_name)
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                target_path = os.path.join(target_folder, file)
                try:
                    shutil.move(src_path, target_path)
                    print(f"Moved '{src_path}' to '{target_path}'")
                except Exception as e:
                    print(f"Error moving file '{src_path}' to '{target_path}': {e}")
            else:
                print(f"Media created date not found for file: '{src_path}'")

if __name__ == "__main__":
    src_folder = input("Enter the source folder path: ").strip()
    dest_folder = input("Enter the destination folder path: ").strip()
    allowed_types_input = input("Enter allowed file types/extensions (comma separated, e.g. .jpg,.png) or leave blank for all: ").strip()
    allowed_file_types = [ext.strip() for ext in allowed_types_input.split(',')] if allowed_types_input else None
    timezone_input = input("Enter the target timezone (e.g. 'UTC', 'Asia/Tokyo'): ").strip() or 'UTC'
    
    sort_by_media_created(src_folder, dest_folder, allowed_file_types, timezone_input)
