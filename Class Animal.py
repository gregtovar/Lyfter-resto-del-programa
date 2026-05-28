#
# Ejercicios OPP - Parte 2 - Clase Animal
#
#


#
# Colors
#

def colors():
    return {
        "CYAN":   "\033[96m",
        "BLUE":   "\033[94m",
        "GREEN":  "\033[92m",
        "YELLOW": "\033[93m",
        "RED":    "\033[91m",
        "PURPLE": "\033[95m",
        "BOLD":   "\033[1m",
        "DIM":    "\033[2m",
        "RESET":  "\033[0m",
    }


#
#. Class Animal
#
#


class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return "Makes a sound"


class Dog(Animal):
    def speak(self) -> str:
        return "Guau"


class Cat(Animal):
    def speak(self) -> str:
        return "Miau"


#
# Input
#

ANIMAL_TYPES = {
    "1": ("🐶  Dog",  Dog,  "🐶"),
    "2": ("🐱  Cat",  Cat,  "🐱"),
}

def ask_animal(c: dict) -> Animal:
    print(f"\n  {c['BLUE']}{'─' * 40}{c['RESET']}")
    print(f"  {c['BOLD']}{c['PURPLE']}    Choose an animal type:{c['RESET']}")
    print(f"  {c['BLUE']}{'─' * 40}{c['RESET']}")
    for key, (label, _, _) in ANIMAL_TYPES.items():
        print(f"  {c['DIM']}  {key}.{c['RESET']}  {label}")
    print(f"  {c['BLUE']}{'─' * 40}{c['RESET']}")

    while True:
        choice = input(f"\n  {c['CYAN']}  Option » {c['RESET']}").strip()
        if choice in ANIMAL_TYPES:
            break
        print(f"  {c['RED']}✖  Please choose 1 or 2.{c['RESET']}")

    label, animal_class, _ = ANIMAL_TYPES[choice]
    name = input(f"\n  {c['YELLOW']}  👤  Name your {label.split()[1]} » {c['RESET']}").strip()
    if not name:
        name = "Unknown"

    return animal_class(name)


def print_result(animal: Animal, c: dict) -> None:
    emoji = "🐶" if isinstance(animal, Dog) else "🐱"
    kind  = type(animal).__name__

    print(f"\n  {c['BLUE']}{'─' * 40}{c['RESET']}")
    print(f"  {c['BOLD']}{c['PURPLE']}    {emoji}  {animal.name}  {c['DIM']}({kind}){c['RESET']}")
    print(f"  {c['BLUE']}{'─' * 40}{c['RESET']}")
    print(f"  {c['DIM']}  animal.speak()  →{c['RESET']}  "
          f"{c['GREEN']}{c['BOLD']}\"{animal.speak()}\"{c['RESET']}")
    print(f"  {c['BLUE']}{'─' * 40}{c['RESET']}")


#
# Menu
#

def show_menu(c: dict) -> str:
    print(f"\n  {c['DIM']}  1.{c['RESET']}  Add another animal")
    print(f"  {c['DIM']}  2.{c['RESET']}  Exit")

    while True:
        choice = input(f"\n  {c['CYAN']}  Option » {c['RESET']}").strip()
        if choice in ("1", "2"):
            return choice
        print(f"  {c['RED']}✖  Please choose 1 or 2.{c['RESET']}")


#
#  Main
# 


c = colors()
print(f"\n  {c['BOLD']}{c['PURPLE']}✦  Animal Kingdom  ✦{c['RESET']}")

while True:
    animal = ask_animal(c)
    print_result(animal, c)

    if show_menu(c) == "2":
        print(f"\n  {c['PURPLE']}  Goodbye! 🐾{c['RESET']}\n")
        break