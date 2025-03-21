import os
from typing import Optional

from find_files_by_name import find_files_by_name as find_files

def delete_files_by_name(
        directory: str,
        starts_with: Optional[str] = None,
        contains: Optional[str] = None,
        ends_with: Optional[str] = None,
        match_case: bool = False,
        must_pass_all: bool = False, # AND operation
        search_subdir: bool = False
):
    files = find_files(
        directory,
        starts_with,
        contains,
        ends_with,
        match_case,
        must_pass_all,
        search_subdir
    )

    for file in files:
        try:
            os.remove(file)
            print(f"File removed: {file}")
        except FileNotFoundError:
            print(f"Warning: File '{file}' not found.")
        except Exception as e:
            print(f"An error occurred while moving folder: {e}")
    

def main():
    directory = input("Enter the directory folder: ")
    starts_with = input("Enter name starts (optional): ") or None
    contains = input("Enter name contains (optional): ") or None
    ends_with = input("Enter name ends (optional): ") or None
    match_case_input = input("Match case? (y/n): ").lower()
    match_case = match_case_input == 'y'
    must_pass_all_input = input("Must pass all conditions? (y/n): ").lower()
    must_pass_all = must_pass_all_input == 'y'
    search_subdir_input = input("Include subdirectories? (y/n): ").lower()
    search_subdir = search_subdir_input == 'y'

    delete_files_by_name(
        directory,
        starts_with,
        contains,
        ends_with,
        match_case,
        must_pass_all,
        search_subdir
    )
    print("Done!")


if __name__ == "__main__":
    main()