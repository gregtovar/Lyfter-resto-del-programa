#
# 
#  Count words from a flat file
# 
# 
# 

#  Default Directory
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


def print_header(colors: dict) -> None:  # Prints Header
    print(f"{colors['DARK_GREEN']}")
    print("=" * 55)
    print("      📄 Word Counter — Count Words in a File")
    print("=" * 55)


def ask_directory(colors: dict) -> str: # Shows the default directory and lets the user keep it or enter a custom one
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


def ask_filename(colors: dict, directory: str) -> str:  # Asks the user for the input file name and returns the full path
    print(f"\n{colors['BLUE']}ℹ️  Make sure your file is located in:")
    print(f"   {directory}")
    print(f"   Include the .txt extension when entering the file name.{colors['DARK_GREEN']}\n")

    while True:
        filename = input("🔷 Enter the file name (e.g. myfile.txt): ").strip()

        if not filename:
            print(f"{colors['RED']}❌ File name cannot be empty. Try again.{colors['DARK_GREEN']}")
            continue

        if not filename.endswith(".txt"):
            print(f"{colors['RED']}❌ File name must end in .txt. Try again.{colors['DARK_GREEN']}")
            continue

        return directory + filename


def read_file(filepath: str, colors: dict) -> str | None: # Reads the full content of the file and returns it as a string. Returns None on error
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"\n{colors['GREEN']}✅ File read successfully: '{filepath}'{colors['DARK_GREEN']}")
        return content
    except FileNotFoundError:
        print(f"{colors['RED']}❌ Error: File not found at '{filepath}'{colors['DARK_GREEN']}")
        return None


def count_words(content: str) -> int: #Splits the content by whitespace (spaces and newlines) and returns the word count.
    return len(content.split())


def print_result(word_count: int, colors: dict) -> None:  # Prints the final word count result
    print(f"\n{colors['BLUE']}📋 Result:{colors['DARK_GREEN']}")
    print(f"   This file contains {colors['GREEN']}{word_count}{colors['DARK_GREEN']} words.")


def main() -> None: # Main Program
    colors = color_setup()
    print_header(colors)

    directory  = ask_directory(colors)
    filepath   = ask_filename(colors, directory)
    content    = read_file(filepath, colors)

    if content is not None:
        word_count = count_words(content)
        print_result(word_count, colors)

    print(colors["RESET"])

#
# Main
#

if __name__ == "__main__":
    main()

#
#
#