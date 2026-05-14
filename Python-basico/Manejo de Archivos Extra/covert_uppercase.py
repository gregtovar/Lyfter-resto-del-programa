#
# read flat file - change to Upper Ce
# 
# 

#  Default Directory
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
    print("      🔠 Uppercase Converter — Line by Line")
    print("=" * 55)


def ask_directory(colors: dict) -> str:
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


def ask_input_filename(colors: dict, directory: str) -> str:
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


def ask_output_filename(colors: dict, directory: str) -> str:
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


def read_lines(filepath: str, colors: dict) -> list[str] | None:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        print(f"\n{colors['GREEN']}✅ Read {len(lines)} lines from '{filepath}'{colors['DARK_GREEN']}")
        return lines
    except FileNotFoundError:
        print(f"{colors['RED']}❌ Error: File not found at '{filepath}'{colors['DARK_GREEN']}")
        return None


def convert_to_uppercase(lines: list[str]) -> list[str]:
    return [line.upper() for line in lines]


def print_preview(lines: list[str], colors: dict, limit: int = 3) -> None:
    print(f"\n{colors['BLUE']}📋 Preview of output (first {limit} lines):{colors['DARK_GREEN']}")
    for line in lines[:limit]:
        print(f"   {line.rstrip()}")


def write_output(lines: list[str], filepath: str, colors: dict) -> bool:
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"\n{colors['GREEN']}✅ Output saved to '{filepath}'{colors['DARK_GREEN']}")
        return True
    except IOError as e:
        print(f"{colors['RED']}❌ Error writing file: {e}{colors['DARK_GREEN']}")
        return False


def main() -> None:
    colors = color_setup()
    print_header(colors)

    directory   = ask_directory(colors)
    input_path  = ask_input_filename(colors, directory)
    output_path = ask_output_filename(colors, directory)

    lines = read_lines(input_path, colors)

    if lines is not None:
        upper_lines = convert_to_uppercase(lines)
        print_preview(upper_lines, colors)
        write_output(upper_lines, output_path, colors)

    print(colors["RESET"])

#
# MAIN#

if __name__ == "__main__":
    main()

#
#
#