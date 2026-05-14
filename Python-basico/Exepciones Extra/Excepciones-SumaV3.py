#
#   Ejercicios extra de Excepciones:
#   Cree una función add_values(lista)
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


def ask_for_list(colors: dict) -> list:
    print("Ingrese los valores separados por coma 🐖")
    print("Ejemplo: 4, hola, 10, 5.2")

    while True:
        list_input = input("🔷 Ingrese su lista: ")

        if "," not in list_input:
            print(f"{colors['RED']}❌ Error: Debe separar los valores con comas. Intente de nuevo.")
            print(colors["DARK_GREEN"], end="")
            continue

        local_list = [element.strip() for element in list_input.split(",")]

        if len(local_list) < 2:
            print(f"{colors['YELLOW']}❌ Error: Debe ingresar al menos 2 valores. Intente de nuevo.")
            print(colors["DARK_GREEN"], end="")
            continue

        return local_list


def add_values(p_list: list, colors: dict) -> float:
    total = 0.0
    for element in p_list:
        try:
            num = float(element)
            total += num
            print(f"{colors['GREEN']}{num}{colors['DARK_GREEN']} sumado correctamente")
        except ValueError:
            label = "Espacio" if element == "" else element
            print(f"{colors['YELLOW']}Elemento inválido: {label}{colors['DARK_GREEN']}")
    print("----------------------------------")
    print(f"{colors['BLUE']}Total de la suma: {total}{colors['DARK_GREEN']}")
    return total


def main():
    colors = color_setup();
    print(f"\n{colors['DARK_GREEN']}------------ OUTPUT -----------------");
    my_list = ask_for_list(colors);
    add_values(my_list, colors);
    print(colors["RESET"]);
#
# Main Program
#
if __name__ == "__main__":
    main();
#
#
#
