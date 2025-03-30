import os

from grouping.group_files_by_name import sort_files as group_by_name
from delete_empty_folders import delete_empty_folders as delete_empty_folders
from grouping.group_images_by_name_date import sort_files as group_by_name_date
from grouping.group_folders_by_year import group_folders_by_year as group_folders
from grouping.group_images_by_date_taken import organize_images_by_date as group_by_date_taken
from grouping.group_files_by_media_created import sort_by_media_created as group_by_media_created
from match_files_by_name_start import sort_by_matching_name as match_by_name


def main():
    src_dir = input("Enter the directory to scan for image files: ").strip()
    dest_dir = input("Enter the destination directory for sorted folders: ").strip()

    group_by_name(
        scan_dir = src_dir,
        target_dir = os.path.join(dest_dir, r'unsorted\facebook\facebook_messenger'),
        startswith = 'received_',
        match_case = True,
        allowed_file_types=['.jpeg', '.png', '.gif']
    )
    
    group_by_date_taken(src_dir, dest_dir, ['.png', '.jpg', '.jpeg', '.cr2'])
    group_by_media_created(src_dir, dest_dir, ['.mov', '.mp4', '.cr2'], 'Asia/Singapore')
    
    group_by_name(
        scan_dir = src_dir,
        target_dir = os.path.join(dest_dir, r'unsorted\facebook'),
        startswith = 'FB_IMG_',
        match_case = True,
        allowed_file_types=['.jpg']
    )
    
    group_by_name(
        scan_dir = src_dir,
        target_dir = os.path.join(dest_dir, r'unsorted\screenshots'),
        startswith = 'screenshot',
        allowed_file_types=['.jpg', '.png']
    )
    
    group_by_name_date(
        src_dir,
        dest_dir,
        ['.png', '.jpg', '.jpeg', '.mov', '.mp4', '.modd']
    )

    match_by_name(
        src_dir,
        dest_dir,
        ['.aee', '.thm', '.modd']
    )

    group_folders(dest_dir, dest_dir)

    for _ in range(3):
        delete_empty_folders(src_dir)



if __name__ == '__main__':
    main()