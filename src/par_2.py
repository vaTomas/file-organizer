import os
import subprocess

from find_files_by_name import find_files_by_name as find_files

def verify_and_repair_par2(par2_file_path, repair=True):
    """
    Verifies and optionally repairs files using a PAR2 file.
    """
    if not os.path.exists(par2_file_path):
        print(f"Error: PAR2 file not found: {par2_file_path}")
        return False

    par2_dir = os.path.dirname(par2_file_path)
    try:
        verify_process = subprocess.run(
            ["par2j64", "v", par2_file_path],
            cwd=par2_dir,
            capture_output=True,
            text=True,
        )

        if "All Files Complete" in verify_process.stdout:
            print(f"Verification successful: All files are correct for {par2_file_path}")
            return True
        elif "Ready to repair" in verify_process.stdout:
            print(f"Verification failed: Some files are missing or damaged for {par2_file_path}")
            if repair:
                print(f"Attempting repair for {par2_file_path}...")
                repair_process = subprocess.run(
                    ["par2j64", "r", par2_file_path],
                    cwd=par2_dir,
                    capture_output=True,
                    text=True,
                )
                if "Repaired successfully" in repair_process.stdout:
                    print(f"Repair successful for {par2_file_path}.")
                    return True
                else:
                    print(f"Repair failed for {par2_file_path}.")
                    print(repair_process.stdout)
                    print(repair_process.stderr)
                    return False
            else:
                return False
        else:
            print(f"Unknown PAR2 output during verification for {par2_file_path}:")
            print(verify_process.stdout)
            print(verify_process.stderr)
            return False

    except FileNotFoundError:
        print("Error: par2j64 command not found. Make sure it is installed and in your PATH.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    

def main():
    dir_path = input("Path: ")
    if not os.path.isdir(dir_path):
        return NotADirectoryError(f"Path is not a directory: {dir_path}")
    
    files = find_files(dir_path, ends_with='.par2', search_subdir=True)

    for file in files:
        verify_and_repair_par2(file)
    

if __name__ == "__main__":
    main()