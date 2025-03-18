import os

from sort_images_by_date_taken import organize_images_by_date as group_by_date_taken
from delete_empty_folder import delete_empty_folders as delete_empty_folders
from sort_images_by_name_date import sort_files as group_by_name_date
from sort_files_by_media_created import sort_by_media_created as group_by_media_created
from sort_files_by_name import sort_files as group_by_name
from group_folders_by_year import group_folders_by_year as group_folders


def main():
    src_dir = input("Enter the directory to scan for image files: ").strip()
    dest_dir = input("Enter the destination directory for sorted folders: ").strip()

    group_by_date_taken(src_dir, dest_dir, ['.png', '.jpg', '.jpeg'])
    group_by_media_created(src_dir, dest_dir, ['.mov', '.mp4'], 'Asia/Singapore')

    group_by_name(
        scan_dir = src_dir,
        target_dir = os.path.join(dest_dir, 'facebook_messenger'),
        startswith = 'received_',
        match_case = True,
        allowed_file_types=['.jpeg', '.png', '.gif']
        )
    
    group_by_name(
        scan_dir = src_dir,
        target_dir = os.path.join(dest_dir, 'facebook'),
        startswith = 'FB_IMG_',
        match_case = True,
        allowed_file_types=['.jpg']
        )
    
    group_by_name(
        scan_dir = src_dir,
        target_dir = os.path.join(dest_dir, 'screenshots'),
        startswith = 'screenshot',
        allowed_file_types=['.jpg', '.png']
        )
    
    group_by_name_date(src_dir, dest_dir, ['.png', '.jpg', '.jpeg', '.mov', '.mp4', '.modd'])

    group_folders(dest_dir, dest_dir)

    for _ in range(3):
        delete_empty_folders(src_dir)



if __name__ == '__main__':
    main()