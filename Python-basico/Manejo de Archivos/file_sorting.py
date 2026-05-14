#
# Reads a file, and sort the lines (in this case songs)
#
#
#
#   To make it work Update these variables  
#       INPUT_FILE  = "Users/gregoriotovar/Library/CloudStorage/GoogleDrive-gr.........t"
#       OUTPUT_FILE = "Users/gregoriotovar/Library/CloudStorage/GoogleDrive-gregtov......."
#
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


def read_songs(filepath: str, colors: dict) -> list[str] | None:    # reads song from txt file
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            songs = [line.strip() for line in f if line.strip()]
        print(f"{colors['GREEN']}✅ {len(songs)} canciones leídas desde '{filepath}'{colors['DARK_GREEN']}")
        return songs
    except FileNotFoundError:
        print(f"{colors['RED']}❌ Error: No se encontró el archivo, revise el path '{filepath}'{colors['DARK_GREEN']}")
        return None


def sort_songs(songs: list[str]) -> list[str]:    # sort song from txt file
    return sorted(songs, key=lambda s: s.lower())


def save_songs(songs: list[str], filepath: str, colors: dict) -> bool:   #writes file
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(songs) + "\n")
        print(f"{colors['GREEN']}✅ Canciones guardadas en '{filepath}'{colors['DARK_GREEN']}")
        return True
    except IOError as e:
        print(f"{colors['RED']}❌ Error al guardar el archivo: {e}{colors['DARK_GREEN']}")
        return False


def print_preview(songs: list[str], colors: dict, limit: int = 40) -> None:    # print an preview of 40 sogs
    print(f"\n{colors['BLUE']}--- Vista previa cancines ORDENADAS (primeras {limit} canciones) ---{colors['DARK_GREEN']}")
    for i, song in enumerate(songs[:limit], start=1):
        print(f"  {i}. {song}")
    print(f"  ... ({len(songs)} canciones en total)")

def green_output(colors) -> None:
    print(f"{colors['DARK_GREEN']}\n------- OUTPUT -----------\n")

def output_reset(colors) -> None:
    print(colors["RESET"]);

def main() -> None:
    INPUT_FILE  = "Users/gregoriotovar/Library/CloudStorage/GoogleDrive-gregtovar@gmail.com/My Drive/A_Lyfter/Programs/top_100_rock_songs.txt"
    OUTPUT_FILE = "Users/gregoriotovar/Library/CloudStorage/GoogleDrive-gregtovar@gmail.com/My Drive/A_Lyfter/Programs/top_100_rock_songs_sorted.txt"
    colors = color_setup()
    green_output(colors);
    songs = read_songs(INPUT_FILE, colors)
    if songs is not None:
        sorted_songs = sort_songs(songs)
        print_preview(sorted_songs, colors)
        save_songs(sorted_songs, OUTPUT_FILE, colors)
    output_reset(colors);

#
# Main Program
#

if __name__ == "__main__":
    main();

#
# End Main Program
#