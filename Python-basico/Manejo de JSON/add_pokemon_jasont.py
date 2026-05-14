import json
import os

# Default Directory & File
DEFAULT_DIR  = "/Users/gregoriotovar/Library/CloudStorage/GoogleDrive-gregtovar@gmail.com/My Drive/A_Lyfter/Programs/"
DEFAULT_FILE = "pokemon.json"


#
#
# Returns a dictionary with ANSI color codes.
#
#
def color_setup() -> dict:
    return {
        "GREEN":      "\033[92m",
        "DARK_GREEN": "\033[32m",
        "RED":        "\033[91m",
        "YELLOW":     "\033[93m",
        "BLUE":       "\033[94m",
        "PURPLE":     "\033[95m",
        "RESET":      "\033[0m",
    }


#
#
# Prints the program header.
#
#
def print_header(colors: dict) -> None:
    print(f"{colors['DARK_GREEN']}")
    print("=" * 55)
    print("      🐾 Pokémon Manager — Add & View Pokémon")
    print("=" * 55)


#
#
# Shows the default directory and lets the user keep it or enter a custom one.
#
#
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


#
#
# Loads and parses the JSON file. Returns None on error.
#
#
def load_json(filepath: str, colors: dict) -> dict | None:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        total = len(data.get("pokemon", []))
        print(f"\n{colors['GREEN']}✅ Loaded '{DEFAULT_FILE}' — {total} Pokémon found.{colors['DARK_GREEN']}")
        return data
    except FileNotFoundError:
        print(f"{colors['RED']}❌ Error: File not found at '{filepath}'{colors['DARK_GREEN']}")
        return None
    except json.JSONDecodeError as e:
        print(f"{colors['RED']}❌ Error: Could not parse JSON — {e}{colors['DARK_GREEN']}")
        return None


#
#
# Generates the next available Pokémon ID based on the existing list.
#
#
def generate_next_id(data: dict) -> int:
    existing = data.get("pokemon", [])
    if not existing:
        return 1
    return max(p["id"] for p in existing) + 1


#
#
# Asks the user for the new Pokémon details and returns them as a dict.
# The ID is auto-generated — the user only provides name, year, and generation.
#
#
def ask_new_pokemon(data: dict, colors: dict) -> dict:
    new_id = generate_next_id(data)

    print(f"\n{colors['BLUE']}{'=' * 55}")
    print(f"  ➕ Add a New Pokémon  (Auto ID: {colors['PURPLE']}#{new_id}{colors['BLUE']})")
    print(f"{'=' * 55}{colors['DARK_GREEN']}\n")

    # --- Name ---
    while True:
        name = input("🔷 Enter Pokémon name: ").strip()
        if not name:
            print(f"{colors['RED']}❌ Name cannot be empty. Try again.{colors['DARK_GREEN']}")
            continue
        if any(p["name"].lower() == name.lower() for p in data.get("pokemon", [])):
            print(f"{colors['YELLOW']}⚠️  '{name}' already exists. Try a different name.{colors['DARK_GREEN']}")
            continue
        break

    # --- Year ---
    while True:
        year_input = input("🔷 Enter release year (e.g. 2023): ").strip()
        if not year_input.isdigit() or not (1996 <= int(year_input) <= 2100):
            print(f"{colors['RED']}❌ Please enter a valid year (1996 or later).{colors['DARK_GREEN']}")
            continue
        year = int(year_input)
        break

    # --- Generation ---
    while True:
        gen_input = input("🔷 Enter generation number (e.g. 1–9): ").strip()
        if not gen_input.isdigit() or not (1 <= int(gen_input) <= 9):
            print(f"{colors['RED']}❌ Please enter a generation between 1 and 9.{colors['DARK_GREEN']}")
            continue
        generation = int(gen_input)
        break

    return {
        "id":         new_id,
        "name":       name,
        "year":       year,
        "generation": generation
    }


#
#
# Appends the new Pokémon to the data dict and saves it back to the JSON file.
#
#
def save_pokemon(new_pokemon: dict, data: dict, filepath: str, colors: dict) -> bool:
    data["pokemon"].append(new_pokemon)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"\n{colors['GREEN']}✅ '{new_pokemon['name']}' saved to '{DEFAULT_FILE}'.{colors['DARK_GREEN']}")
        return True
    except IOError as e:
        print(f"{colors['RED']}❌ Error saving file: {e}{colors['DARK_GREEN']}")
        return False


#
#
# Prints the full Pokémon list in a formatted table, highlighting the newest entry.
#
#
def print_full_list(data: dict, new_id: int, colors: dict) -> None:
    pokemon_list = data.get("pokemon", [])
    total        = len(pokemon_list)

    print(f"\n{colors['BLUE']}{'=' * 57}")
    print(f"  🐾  Complete Pokémon List — {total} Total")
    print(f"{'=' * 57}")
    print(f"  {'ID':<6} {'Name':<16} {'Year':<8} {'Gen':<6} {'Status'}")
    print(f"  {'-'*6} {'-'*16} {'-'*8} {'-'*6} {'-'*8}")
    print(f"{colors['DARK_GREEN']}")

    current_gen = None
    for p in pokemon_list:

        # Print a generation divider when the generation changes
        if p["generation"] != current_gen:
            current_gen = p["generation"]
            print(f"{colors['BLUE']}  ── Generation {current_gen} {'─' * 35}{colors['DARK_GREEN']}")

        # Highlight the newly added Pokémon
        if p["id"] == new_id:
            tag  = "⭐ NEW"
            row  = f"  {p['id']:<6} {p['name']:<16} {p['year']:<8} {p['generation']:<6} {tag}"
            print(f"{colors['PURPLE']}{row}{colors['DARK_GREEN']}")
        else:
            print(f"  {p['id']:<6} {p['name']:<16} {p['year']:<8} {p['generation']}")

    print(f"\n{colors['BLUE']}{'=' * 57}")
    print(f"  Total Pokémon: {colors['GREEN']}{total}{colors['BLUE']}  |  Newest: {colors['PURPLE']}{pokemon_list[-1]['name']} (#{pokemon_list[-1]['id']})")
    print(f"{'=' * 57}{colors['DARK_GREEN']}")


#
#
# Entry point of the program.
#
#
def main() -> None:
    colors = color_setup()
    print_header(colors)

    directory   = ask_directory(colors)
    filepath    = os.path.join(directory, DEFAULT_FILE)
    data        = load_json(filepath, colors)

    if data is None:
        print(colors["RESET"])
        return

    new_pokemon = ask_new_pokemon(data, colors)
    saved       = save_pokemon(new_pokemon, data, filepath, colors)

    if saved:
        print_full_list(data, new_pokemon["id"], colors)

    print(colors["RESET"])


if __name__ == "__main__":
    main()