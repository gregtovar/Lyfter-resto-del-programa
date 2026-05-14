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
#  Function: ask_positive_integer - Prompts the user for a positive integer until a valid value is given.
#
def ask_positive_integer(message: str) -> int:
    while True:
        try:
            value = int(input(f"{C['BLUE']}{message}{C['RESET']}"))
            if value <= 0:
                print(f"{C['RED']}Please enter a number greater than 0.{C['RESET']}\n")
                continue
            return value
        except ValueError:
            print(f"{C['RED']}Invalid input. You must enter an integer.{C['RESET']}\n")


#
#  Function: ask_text - Prompts the user for non-empty text.
#
def ask_text(message: str) -> str:
    while True:
        value = input(f"{C['BLUE']}{message}{C['RESET']}").strip()
        if value:
            return value
        print(f"{C['RED']}This field cannot be empty.{C['RESET']}\n")


#
#  Function: ask_esrb_rating - Prompts the user for an ESRB rating and validates it against the allowed values.
#
def ask_esrb_rating(message: str) -> str:
    valid_ratings = ["E", "E10+", "T", "M", "AO", "RP"]
    while True:
        value = input(f"{C['BLUE']}{message}{C['RESET']}").strip()
        if value != value.upper():
            print(f"{C['RED']}The ESRB rating must be in uppercase "
                  f"(all caps).{C['RESET']}\n")
            continue
        if value in valid_ratings:
            return value
        print(f"{C['RED']}Invalid ESRB rating. Allowed values are: "
              f"{', '.join(valid_ratings)}.{C['RESET']}\n")


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
#  Function: print_csv_fancy - Reads a CSV file and prints its contents to the console as a nicely formatted table.
#
def print_csv_fancy(file_path: str) -> None:
    with open(file_path, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        rows = list(reader)

    if not rows:
        print(f"{C['RED']}The file is empty.{C['RESET']}")
        return

    # Capitalize the first letter of each header (e.g., "nombre" -> "Nombre").
    headers = [h[:1].upper() + h[1:] for h in rows[0]]
    data_rows = rows[1:]

    # Calculate the maximum width for each column.
    col_widths = [len(h) for h in headers]
    for row in data_rows:
        for i, cell in enumerate(row):
            if i < len(col_widths) and len(cell) > col_widths[i]:
                col_widths[i] = len(cell)

    # Build box-drawing borders.
    top_border    = "┌" + "┬".join("─" * (w + 2) for w in col_widths) + "┐"
    middle_border = "├" + "┼".join("─" * (w + 2) for w in col_widths) + "┤"
    bottom_border = "└" + "┴".join("─" * (w + 2) for w in col_widths) + "┘"

    def format_row(row, color):
        cells = [
            f" {color}{(row[i] if i < len(row) else '').ljust(col_widths[i])}{C['RESET']} "
            for i in range(len(col_widths))
        ]
        return f"{C['BLUE']}│{C['RESET']}" + f"{C['BLUE']}│{C['RESET']}".join(cells) + f"{C['BLUE']}│{C['RESET']}"

    print(f"\n{C['DARK_GREEN']}=== CSV Contents ==={C['RESET']}")
    print(f"{C['BLUE']}{top_border}{C['RESET']}")
    print(format_row(headers, C['DARK_GREEN']))
    print(f"{C['BLUE']}{middle_border}{C['RESET']}")
    for row in data_rows:
        print(format_row(row, C['GREEN']))
    print(f"{C['BLUE']}{bottom_border}{C['RESET']}")

    # Print the file name and directory below the table.
    file_only = os.path.basename(file_path)
    dir_only = os.path.dirname(os.path.abspath(file_path))
    print(f"{C['YELLOW']}File:      {C['RESET']}{file_only}")
    print(f"{C['YELLOW']}Directory: {C['RESET']}{dir_only}")


#
#  Function: main - Entry point. Collects video game data from the user and saves it to a CSV file.
#
def main():
    print(f"{C['DARK_GREEN']}=== Video Game Registry ==={C['RESET']}\n")

    n = ask_positive_integer("How many video games would you like to register? ")

    games = []
    for i in range(1, n + 1):
        print(f"\n{C['YELLOW']}--- Video Game #{i} ---{C['RESET']}")
        nombre = ask_text("Name: ")
        genero = ask_text("Genre: ")
        desarrollador = ask_text("Developer: ")
        clasificacion = ask_esrb_rating("ESRB Rating (E, E10+, T, M, AO, RP): ")

        games.append({
            "nombre": nombre,
            "genero": genero,
            "desarrollador": desarrollador,
            "clasificacion": clasificacion,
        })

    # Ask for the file name (with option to use the default value).
    file_name = ask_file_name("videojuegos.csv")

    # Save to the default directory if it exists; otherwise use the current directory.
    if os.path.isdir(DEFAULT_DIR):
        file_path = os.path.join(DEFAULT_DIR, file_name)
    else:
        file_path = file_name
        print(f"\n{C['YELLOW']}Notice: the default directory does not exist. "
              f"Saving to the current directory.{C['RESET']}")

    fields = ["nombre", "genero", "desarrollador", "clasificacion"]

    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(games)

    print(f"\n{C['GREEN']}File created successfully with {n} video game(s).{C['RESET']}")
    print(f"{C['GREEN']}Location: {file_path}{C['RESET']}")

    # Print the CSV contents with fancy formatting.
    print_csv_fancy(file_path)


if __name__ == "__main__":
    main()