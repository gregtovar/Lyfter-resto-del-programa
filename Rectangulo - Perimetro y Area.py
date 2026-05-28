#
# 
#  Ejercicios OPP - Parte 2 - Rectangulo - Perimetro y Area
# 
# 


# 
# Color definition
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
# Class: Rectangle
#

class Rectangle:
    def __init__(self, width: float, height: float):
        if width < 0:
            raise ValueError(f"Width cannot be negative (got {width}).")
        if height < 0:
            raise ValueError(f"Height cannot be negative (got {height}).")
        self.width  = width
        self.height = height

    def get_area(self) -> float:    # Area
        return self.width * self.height

    def get_perimeter(self) -> float:   # Perimeter
        return 2 * (self.width + self.height)


#
# Input
#
def ask_dimension(label: str, c: dict) -> float:
    while True:
        try:
            value = float(input(f"  {c['YELLOW']}  {label} » {c['RESET']}"))
            if value < 0:
                raise ValueError(f"{label} cannot be negative.")
            return value
        except ValueError as e:
            print(f"\n  {c['RED']}✖  {e}  Try again.{c['RESET']}\n")


#
# Menu
#

def show_menu(c: dict) -> str:
    print(f"\n  {c['BLUE']}{'─' * 40}{c['RESET']}")
    print(f"  {c['BOLD']}{c['PURPLE']}    What would you like to calculate?{c['RESET']}")
    print(f"  {c['BLUE']}{'─' * 40}{c['RESET']}")
    print(f"  {c['DIM']}  1.{c['RESET']}  📐  Area")
    print(f"  {c['DIM']}  2.{c['RESET']}  📏  Perimeter")
    print(f"  {c['DIM']}  3.{c['RESET']}  ✨  Both")
    print(f"  {c['DIM']}  4.{c['RESET']}  🔄  New rectangle")
    print(f"  {c['DIM']}  5.{c['RESET']}  🚪  Exit")
    print(f"  {c['BLUE']}{'─' * 40}{c['RESET']}")

    while True:
        choice = input(f"\n  {c['CYAN']}  Option » {c['RESET']}").strip()
        if choice in ("1", "2", "3", "4", "5"):
            return choice
        print(f"  {c['RED']}✖  Please choose 1–5.{c['RESET']}")


def print_result(rect: Rectangle, choice: str, c: dict) -> None:
    bar = "─" * 40
    print(f"\n  {c['BLUE']}{bar}{c['RESET']}")
    print(f"  {c['BOLD']}{c['PURPLE']}    📦  Rectangle  "
          f"{c['DIM']}({rect.width} × {rect.height}){c['RESET']}")
    print(f"  {c['BLUE']}{bar}{c['RESET']}")

    if choice in ("1", "3"):
        print(f"  {c['DIM']}  Area      {c['RESET']}"
              f"  {c['GREEN']}{c['BOLD']}{rect.get_area():.4f}{c['RESET']}"
              f"  {c['DIM']}units²{c['RESET']}")
    if choice in ("2", "3"):
        print(f"  {c['DIM']}  Perimeter {c['RESET']}"
              f"  {c['GREEN']}{c['BOLD']}{rect.get_perimeter():.4f}{c['RESET']}"
              f"  {c['DIM']}units{c['RESET']}")

    print(f"  {c['BLUE']}{bar}{c['RESET']}")


def ask_rectangle(c: dict) -> Rectangle:
    print(f"\n  {c['DIM']}  Enter the rectangle dimensions:{c['RESET']}\n")
    width  = ask_dimension("📐  Width ", c)
    height = ask_dimension("📏  Height", c)
    return Rectangle(width, height)


#
# Main
#
c = colors()

print(f"\n  {c['BOLD']}{c['PURPLE']}✦  Rectangle Calculator  ✦{c['RESET']}")

rect = ask_rectangle(c)

while True:
    choice = show_menu(c)

    if choice in ("1", "2", "3"):
        print_result(rect, choice, c)

    elif choice == "4":
        rect = ask_rectangle(c)

    elif choice == "5":
        print(f"\n  {c['PURPLE']}  Goodbye! 👋{c['RESET']}\n")
        break