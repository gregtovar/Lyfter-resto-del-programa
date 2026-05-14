#
# Append Line to flat file
# 

import os
from datetime import datetime

# Default Directory
DEFAULT_DIR = "/Users/gregoriotovar/Library/CloudStorage/GoogleDrive-gregtovar@gmail.com/My Drive/A_Lyfter/Programs/"


def color_setup() -> dict:
    """Returns a dictionary with ANSI color codes."""
    return {
        "GREEN":      "\033[92m",
        "DARK_GREEN": "\033[32m",
        "RED":        "\033[91m",
        "YELLOW":     "\033[93m",
        "BLUE":       "\033[94m",
        "RESET":      "\033[0m",
    }


def print_header(colors: dict) -> None: #Prints the program header
    print(f"{colors['DARK_GREEN']}")
    print("=" * 55)
    print("      ✏️  Line Appender — Add Text to a File")
    print("=" * 55)


def ask_directory(colors: dict) -> str:  #Shows the default directory and lets the user keep it or enter a custom one.
    print(f"\n{colors['BLUE']}📁 Default working directory:")
    print(f"   {DEFAULT_DIR}{colors['DARK_GREEN']}\n")

    print(f"   {colors['YELLOW']}Enter 0{colors['DARK_GREEN']} to keep the default directory.")
    print(f"   {colors['YELLOW']}Enter 1{colors['DARK_GREEN']} to use a different directory.\n")

    while True:
        choice = input("🔷 Your choice (0 or 1): ").strip()

        if choice == "0":
            print(f"\n{colors['GREEN']}✅ Using default directory.{colors['DARK_GREEN']}")
            return DEFAULT_DIR

        elif choice == "1":
            while True:
                custom_dir = input("\n🔷 Enter the full directory path: ").strip()

                if not custom_dir:
                    print(f"{colors['RED']}❌ Directory cannot be empty. Try again.{colors['DARK_GREEN']}")
                    continue

                if not custom_dir.endswith("/"):
                    custom_dir += "/"

                print(f"\n{colors['GREEN']}✅ Using custom directory: {custom_dir}{colors['DARK_GREEN']}")
                return custom_dir

        else:
            print(f"{colors['RED']}❌ Invalid choice. Please enter 0 or 1.{colors['DARK_GREEN']}")


def ask_text_line(colors: dict) -> str: #Asks the user to enter a line of text to append. Cannot be empty.
    print(f"\n{colors['BLUE']}ℹ️  Enter the line of text you want to add to the file.{colors['DARK_GREEN']}\n")

    while True:
        line = input("🔷 Enter your text: ").strip()

        if not line:
            print(f"{colors['RED']}❌ Text cannot be empty. Try again.{colors['DARK_GREEN']}")
            continue

        return line


def ask_filename(colors: dict, directory: str) -> str: #Asks the user for a file name and returns the full path
    print(f"\n{colors['BLUE']}ℹ️  Enter the file name to append to (must be in):")
    print(f"   {directory}")
    print(f"   Include the .txt extension. If the file does not exist,")
    print(f"   a new one will be created automatically with a timestamp.{colors['DARK_GREEN']}\n")

    while True:
        filename = input("🔷 Enter the file name (e.g. myfile.txt): ").strip()

        if not filename:
            print(f"{colors['RED']}❌ File name cannot be empty. Try again.{colors['DARK_GREEN']}")
            continue

        if not filename.endswith(".txt"):
            print(f"{colors['RED']}❌ File name must end in .txt. Try again.{colors['DARK_GREEN']}")
            continue

        return directory + filename


def generate_timestamped_filename(directory: str) -> str: #Generates a unique file name using 'file_' + current timestamp.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return directory + f"file_{timestamp}.txt"


def file_exists(filepath: str) -> bool: #Returns True if the file already exists on disk.
    return os.path.exists(filepath)


def append_to_file(line: str, filepath: str, colors: dict) -> bool: #Appends the line to an existing file. Returns True on success
    try:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        print(f"\n{colors['GREEN']}✅ Line appended to '{filepath}'{colors['DARK_GREEN']}")
        return True
    except IOError as e:
        print(f"{colors['RED']}❌ Error writing to file: {e}{colors['DARK_GREEN']}")
        return False


def create_new_file(line: str, filepath: str, colors: dict) -> bool: #Creates a new file with the given line as its content. Returns True on success.
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(line + "\n")
        print(f"\n{colors['GREEN']}✅ File did not exist. Created new file: '{filepath}'{colors['DARK_GREEN']}")
        return True
    except IOError as e:
        print(f"{colors['RED']}❌ Error creating file: {e}{colors['DARK_GREEN']}")
        return False


def append_or_create(line: str, filepath: str, directory: str, colors: dict) -> None: #Checks if the file exists: appends to it if yes, creates a timestamped file if no.
    if file_exists(filepath):
        append_to_file(line, filepath, colors)
    else:
        print(f"\n{colors['YELLOW']}⚠️  File not found. Creating a new timestamped file...{colors['DARK_GREEN']}")
        new_filepath = generate_timestamped_filename(directory)
        create_new_file(line, new_filepath, colors)


def main() -> None: # Main 
    colors = color_setup()
    print_header(colors)

    directory = ask_directory(colors)
    text_line = ask_text_line(colors)
    filepath  = ask_filename(colors, directory)

    append_or_create(text_line, filepath, directory, colors)

    print(colors["RESET"])

#
# Main
#
if __name__ == "__main__":
    main()
#
# End of Main
#
