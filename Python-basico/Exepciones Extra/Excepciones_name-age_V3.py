#
#   Ejercicios extra de Excepciones
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


def print_header(colors: dict) -> None:
    print(f"{colors['DARK_GREEN']}\n------- OUTPUT -----------\n")


def ask_name(colors: dict) -> str | None:
    try:
        user_name = input("🔷 Ingrese su nombre: ").strip()
        if not user_name:
            raise ValueError("El nombre no puede estar vacío")
        if user_name.isdigit():
            raise ValueError("El nombre no puede ser un número")
        return user_name
    except ValueError as e:
        print(f"{colors['RED']}❌ Error: {e}{colors['DARK_GREEN']}")
        return None


def ask_for_age(p_name: str | None, colors: dict) -> int | None:
    if p_name is None:
        return None
    try:
        age = int(input("🫵 Ingrese su edad: "))
        if age <= 0:
            raise ValueError("La edad debe ser un número positivo")
        return age
    except ValueError as e:
        print(f"{colors['RED']}❌ Error: {e}{colors['DARK_GREEN']}")
        return None


def say_hello(name: str | None, age: int | None, colors: dict) -> None:
    if name is not None and age is not None:
        print(f"\n{colors['GREEN']}🟢  Hola {name}, su edad es {age}{colors['DARK_GREEN']}")


def main() -> None:
    colors = color_setup();
    print_header(colors);
    name = ask_name(colors);
    age  = ask_for_age(name, colors);
    say_hello(name, age, colors);
    print(colors["RESET"]);

#
#
# MAIN PROGRAM
#

if __name__ == "__main__":
    main();

#
#

