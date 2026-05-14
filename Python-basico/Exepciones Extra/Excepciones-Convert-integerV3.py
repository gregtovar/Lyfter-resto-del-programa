#
#   Ejercicios extra de Excepciones:
#   Convertir a Entero
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


def convert_integer(p_list: list, colors: dict) -> None:
    print("--------- OUTPUT ----------")

    for counter, element in enumerate(p_list, start=1):
        try:
            num = int(element)
            print(f"Posicion {counter} - \"{element}\" convertido a {num}")
        except ValueError:
            label = "ESPACIO" if element == "" else f'"{element}"'
            print(f"{colors['YELLOW']}Posicion {counter} - No se pudo convertir: {label}{colors['DARK_GREEN']}")


def main() -> None:
    """Entry point of the program."""
    colors = color_setup()
    print(colors["DARK_GREEN"], end="")
    my_list = ask_for_list(colors)
    convert_integer(my_list, colors)
    print(f"{colors['RESET']}\n")

#
# Main
#
if __name__ == "__main__":
    main();

#
#
#
