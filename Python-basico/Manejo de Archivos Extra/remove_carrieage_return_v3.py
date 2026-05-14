# Default Directory
DEFAULT_DIR = "/Users/gregoriotovar/Library/CloudStorage/GoogleDrive-gregtovar@gmail.com/My Drive/A_Lyfter/Programs/"


def color_setup() -> dict:
    return {
        "GREEN":      "\033[92m",
        "DARK_GREEN": "\033[32m",
        "RED":        "\033[91m",
        "YELLOW":     "\033[93m",
        "BLUE":       "\033[94m",
        "RESET":      "\033[0m",
    }


def print_header(colors: dict) -> None:
    print(f"{colors['DARK_GREEN']}")
    print("=" * 55)
    print("      📄 File Joiner — Merge Lines into One")
    print("=" * 55)


def ask_directory(colors: dict) -> str:    # Gives option to change directory
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

                # Ensure the path ends with a slash
                if not custom_dir.endswith("/"):
                    custom_dir += "/"

                print(f"\n{colors['GREEN']}✅ Using custom directory: {custom_dir}{colors['DARK_GREEN']}")
                return custom_dir

        else:
            print(f"{colors['RED']}❌ Invalid choice. Please enter 0 or 1.{colors['DARK_GREEN']}")


def ask_input_filename(colors: dict, directory: str) -> str:   #Ask for file names
    print(f"\n{colors['BLUE']}ℹ️  Make sure your input file is located in:")
    print(f"   {directory}")
    print(f"   Include the .txt extension when entering the file name.{colors['DARK_GREEN']}\n")

    while True:
        filename = input("🔷 Enter the INPUT file name (e.g. myfile.txt): ").strip()

        if not filename:
            print(f"{colors['RED']}❌ File name cannot be empty. Try again.{colors['DARK_GREEN']}")
            continue

        if not filename.endswith(".txt"):
            print(f"{colors['RED']}❌ File name must end in .txt. Try again.{colors['DARK_GREEN']}")
            continue

        return directory + filename


def ask_output_filename(colors: dict, directory: str) -> str:   # Output file name
    print(f"\n{colors['BLUE']}ℹ️  The output file will be saved to:")
    print(f"   {directory}")
    print(f"   Include the .txt extension when entering the file name.{colors['DARK_GREEN']}\n")

    while True:
        filename = input("🔷 Enter the OUTPUT file name (e.g. output.txt): ").strip()

        if not filename:
            print(f"{colors['RED']}❌ File name cannot be empty. Try again.{colors['DARK_GREEN']}")
            continue

        if not filename.endswith(".txt"):
            print(f"{colors['RED']}❌ File name must end in .txt. Try again.{colors['DARK_GREEN']}")
            continue

        return directory + filename


def read_lines(filepath: str, colors: dict) -> list[str] | None:   # Read file
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f if line.strip()]
        print(f"\n{colors['GREEN']}✅ Read {len(lines)} lines from '{filepath}'{colors['DARK_GREEN']}")
        return lines
    except FileNotFoundError:
        print(f"{colors['RED']}❌ Error: File not found (or directory not vaid) at '{filepath}'{colors['DARK_GREEN']}")
        return None


def join_lines(lines: list[str]) -> str:
    """Joins a list of stripped lines into a single space-separated string."""
    return " ".join(lines)


def write_output(content: str, filepath: str, colors: dict) -> bool:
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"{colors['GREEN']}✅ Output saved to '{filepath}'{colors['DARK_GREEN']}")
        return True
    except IOError as e:
        print(f"{colors['RED']}❌ Error writing file: {e}{colors['DARK_GREEN']}")
        return False


def print_preview(content: str, colors: dict) -> None:
    preview = content if len(content) <= 80 else content[:80] + "..."
    print(f"\n{colors['BLUE']}📋 Preview of output:{colors['DARK_GREEN']}")
    print(f'   "{preview}"')


def main() -> None:
    colors = color_setup()
    print_header(colors)
    directory   = ask_directory(colors)
    input_path  = ask_input_filename(colors, directory)
    output_path = ask_output_filename(colors, directory)
    lines = read_lines(input_path, colors)
    if lines is not None:
        joined = join_lines(lines)
        print_preview(joined, colors)
        write_output(joined, output_path, colors)

    print(colors["RESET"])


#
# Main
#

if __name__ == "__main__":
    main()


#
#
#
