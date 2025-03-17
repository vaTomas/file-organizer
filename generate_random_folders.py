import os
import random
import string

def format_word():
    """Generate a simple word of random lowercase letters."""
    length = random.randint(3, 8)
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def format_word_dash_numbers():
    """Generate a name like: word-123-45-6"""
    word_part = format_word()
    # Generate three groups of digits with random lengths
    num1 = ''.join(random.choices(string.digits, k=random.randint(1, 3)))
    num2 = ''.join(random.choices(string.digits, k=random.randint(1, 3)))
    num3 = ''.join(random.choices(string.digits, k=random.randint(1, 3)))
    return f"{word_part}-{num1}-{num2}-{num3}"

def format_word_space_word():
    """Generate a name like: word word word (three random words separated by spaces)"""
    return f"{format_word()} {format_word()} {format_word()}"

def format_gt():
    """Generate a name like: GT-I9205"""
    letter = random.choice(string.ascii_uppercase)
    num = ''.join(random.choices(string.digits, k=random.randint(4, 6)))
    return f"GT-{letter}{num}"

def format_numbers():
    """Generate a folder name consisting only of numbers."""
    length = random.randint(3, 10)
    return ''.join(random.choices(string.digits, k=length))

def format_numbers_and_letters():
    """Generate an alphanumeric folder name."""
    length = random.randint(5, 12)
    choices = string.ascii_letters + string.digits
    return ''.join(random.choices(choices, k=length))

def format_names_event():
    """Generate a name like: Names's event mmm dd, yyyy."""
    names = ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace"]
    name = random.choice(names)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month = random.choice(months)
    day = random.randint(1, 28)
    year = random.randint(1990, 2025)
    return f"{name}'s event {month} {day:02d}, {year}"

def generate_random_folder_name():
    """Randomly choose one of several formats to generate a folder name."""
    formats = [
        format_word,
        format_word_dash_numbers,
        format_word_space_word,
        format_gt,
        format_numbers,
        format_numbers_and_letters,
        format_names_event,
    ]
    chosen_format = random.choice(formats)
    return chosen_format()

def create_random_folders(current_dir, current_depth, max_depth, max_folders):
    """Recursively create random folders up to a specified depth and max folders per level."""
    if current_depth > max_depth:
        return

    # Decide a random number of folders to create at this level (0 to max_folders)
    num_folders = random.randint(0, max_folders)
    for _ in range(num_folders):
        folder_name = generate_random_folder_name()
        new_folder_path = os.path.join(current_dir, folder_name)
        try:
            os.makedirs(new_folder_path, exist_ok=True)
            print(f"Created folder: {new_folder_path}")
        except Exception as e:
            print(f"Error creating folder {new_folder_path}: {e}")
            continue

        # Recursively create subfolders in the new folder
        create_random_folders(new_folder_path, current_depth + 1, max_depth, max_folders)


def main():
    base_dir = input("Enter the base directory where random folders will be created: ").strip()
    if not os.path.exists(base_dir):
        try:
            os.makedirs(base_dir)
            print(f"Created base directory: {base_dir}")
        except Exception as e:
            print(f"Error creating base directory '{base_dir}': {e}")
            return

    try:
        max_depth = int(input("Enter the maximum subfolder depth: ").strip())
        max_folders = int(input("Enter the maximum number of folders per level: ").strip())
    except ValueError:
        print("Please enter valid integer values for maximum depth and number of folders.")
        return

    create_random_folders(base_dir, current_depth=1, max_depth=max_depth, max_folders=max_folders)
    print("Folder creation complete.")


if __name__ == '__main__':
    main()
