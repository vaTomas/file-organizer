from sort_images_by_date_taken import organize_images_by_date as group_by_date_taken
from delete_empty_folder import delete_empty_folders as delete_empty_folders
from sort_images_by_name_date import sort_files as group_by_name_date
from sort_files_by_media_created import sort_by_media_created as group_by_media_created



def main():
    src_dir = input("Enter the directory to scan for image files: ").strip()
    dest_dir = input("Enter the destination directory for sorted folders: ").strip()

    group_by_date_taken(src_dir, dest_dir, ['.png', '.jpg', '.jpeg'])
    group_by_media_created(src_dir, dest_dir, ['.mov', '.mp4'])

    group_by_name_date(src_dir, dest_dir)

    delete_empty_folders(src_dir)



if __name__ == '__main__':
    main()