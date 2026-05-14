import csv
import os


DEFAULT_DIR = "/Users/gregoriotovar/Library/CloudStorage/GoogleDrive-gregtovar@gmail.com/My Drive/A_Lyfter/Programs/"


#
#  Function: color_setup - Returns a dictionary with ANSI color codes.
#
def color_setup() -> dict:
    return {
        "GREEN":      "\033[92m",
        "DARK_GREEN": "\033[32m",
        "RED":        "\033[91m",
        "YELLOW":     "\033[93m",
        "BLUE":       "\033[94m",
        "RESET":      "\033[0m",
    }


C = color_setup()


#
#  Function: ask_directory - Prompts the user for a directory. If the user enters '1', the default directory is used.
#
def ask_directory(default_dir: str) -> str:
    print(f"\n{C['BLUE']}Enter the directory where the CSV file is stored "
          f"(or type '1' to use the default value: "
          f"'{default_dir}'):{C['RESET']}")
    entry = input(f"{C['BLUE']}Directory: {C['RESET']}").strip()

    if entry == "1" or entry == "":
        print(f"{C['YELLOW']}Notice: the default directory will be used.{C['RESET']}")
        return default_dir
    return entry


#
#  Function: ask_file_name - Prompts the user for the CSV file name. If the user enters '1', the default name is used.
#
def ask_file_name(default_name: str) -> str:
    print(f"\n{C['BLUE']}Enter the CSV file name "
          f"(or type '1' to use the default value: "
          f"'{default_name}'):{C['RESET']}")
    entry = input(f"{C['BLUE']}File name: {C['RESET']}").strip()

    if entry == "1" or entry == "":
        print(f"{C['YELLOW']}Notice: the default name "
              f"'{default_name}' will be used.{C['RESET']}")
        return default_name

    # Make sure it ends with .csv
    if not entry.lower().endswith(".csv"):
        entry += ".csv"
    return entry


#
#  Function: detect_delimiter - Sniffs the file to detect whether it uses tab or comma as delimiter.
#
def detect_delimiter(text: str) -> str:
    try:
        dialect = csv.Sniffer().sniff(text, delimiters=",\t;|")
        return dialect.delimiter
    except csv.Error:
        # Fallback heuristic: pick whichever appears more often in the first line.
        first_line = text.splitlines()[0] if text else ""
        return "\t" if first_line.count("\t") > first_line.count(",") else ","


#
#  Function: read_csv_rows - Reads a CSV file trying multiple encodings and auto-detecting the delimiter.
#
def read_csv_rows(file_path: str) -> list:
    encodings = ["utf-8-sig", "utf-8", "mac_roman", "cp1252", "latin-1"]
    text = None
    for enc in encodings:
        try:
            with open(file_path, mode="r", newline="", encoding=enc) as f:
                text = f.read()
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        # Final safety net: replace any byte that still cannot be decoded.
        with open(file_path, mode="r", newline="", encoding="utf-8", errors="replace") as f:
            text = f.read()

    delimiter = detect_delimiter(text)
    reader = csv.reader(text.splitlines(), delimiter=delimiter)
    return list(reader)


#
#  Function: print_csv_fancy - Reads a CSV file with csv.reader and prints its contents to the console as a fancy formatted table.
#
def print_csv_fancy(file_path: str) -> None:
    rows = read_csv_rows(file_path)

    if not rows:
        print(f"{C['RED']}The file is empty.{C['RESET']}")
        return

    # Capitalize the first letter of each header (e.g., "nombre" -> "Nombre").
    field_names = [h[:1].upper() + h[1:] for h in rows[0]]
    data_rows = rows[1:]

    # One column per field, with a row-number column on the left.
    headers = ["#"] + field_names
    numbered_rows = [[str(i + 1)] + row for i, row in enumerate(data_rows)]

    # Calculate the maximum width for each column.
    col_widths = [len(h) for h in headers]
    for row in numbered_rows:
        for i, cell in enumerate(row):
            if i < len(col_widths) and len(cell) > col_widths[i]:
                col_widths[i] = len(cell)

    # Total inner width (between the two outer ║), used by the title bar.
    total_inner_width = sum(w + 2 for w in col_widths) + (len(col_widths) - 1)

    # Build double-line borders for outer frame and single-line for column separators.
    top_border      = "╔" + "═" * total_inner_width + "╗"
    title_separator = "╠" + "╦".join("═" * (w + 2) for w in col_widths) + "╣"
    middle_border   = "╠" + "╬".join("═" * (w + 2) for w in col_widths) + "╣"
    bottom_border   = "╚" + "╩".join("═" * (w + 2) for w in col_widths) + "╝"

    title = "Video Games Catalog"
    title_padded = title.center(total_inner_width)

    def format_row(row, color):
        cells = [
            f" {color}{(row[i] if i < len(row) else '').ljust(col_widths[i])}{C['RESET']} "
            for i in range(len(col_widths))
        ]
        return f"{C['BLUE']}║{C['RESET']}" + f"{C['BLUE']}║{C['RESET']}".join(cells) + f"{C['BLUE']}║{C['RESET']}"

    print()
    print(f"{C['BLUE']}{top_border}{C['RESET']}")
    print(f"{C['BLUE']}║{C['RESET']}{C['DARK_GREEN']}{title_padded}{C['RESET']}{C['BLUE']}║{C['RESET']}")
    print(f"{C['BLUE']}{title_separator}{C['RESET']}")
    print(format_row(headers, C['DARK_GREEN']))
    print(f"{C['BLUE']}{middle_border}{C['RESET']}")
    for row in numbered_rows:
        print(format_row(row, C['GREEN']))
    print(f"{C['BLUE']}{bottom_border}{C['RESET']}")

    # Footer: record count, file name, and directory.
    file_only = os.path.basename(file_path)
    dir_only = os.path.dirname(os.path.abspath(file_path))
    print(f"{C['YELLOW']}Total records: {C['RESET']}{len(data_rows)}")
    print(f"{C['YELLOW']}File:          {C['RESET']}{file_only}")
    print(f"{C['YELLOW']}Directory:     {C['RESET']}{dir_only}")


#
#  Function: main - Entry point. Asks the user for the directory and file name, then reads and displays the CSV file.
#
def main():
    print(f"{C['DARK_GREEN']}=== Video Game CSV Reader ==={C['RESET']}\n")

    directory = ask_directory(DEFAULT_DIR)
    file_name = ask_file_name("videojuegos.csv")

    # Fall back to the current directory if the chosen one does not exist.
    if not os.path.isdir(directory):
        print(f"\n{C['YELLOW']}Notice: the directory '{directory}' does not exist. "
              f"Trying the current directory instead.{C['RESET']}")
        directory = "."

    file_path = os.path.join(directory, file_name)

    if not os.path.isfile(file_path):
        print(f"\n{C['RED']}Error: the file '{file_path}' does not exist.{C['RESET']}")
        return

    print_csv_fancy(file_path)


if __name__ == "__main__":
    main()