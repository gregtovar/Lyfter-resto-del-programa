"""
╔══════════════════════════════════════════════╗
║          Shape Calculator  🔷🔶🔵           ║
║   Abstract base class + Circle / Square /    ║
║   Rectangle implementations                  ║║
    Greg Tovar - 2026           ║
╚══════════════════════════════════════════════╝
"""

#
# Abstract 
#

from abc import ABC, abstractmethod
import math


# ─────────────────────────────────────────────
#  Abstract Base Class
# ─────────────────────────────────────────────

#
# Abstract base class for all 2-D shapes.
#


#
#    Abstract base class for all 2-D shapes.
#

class Shape(ABC):
 
    @abstractmethod
    def calculate_area(self) -> float:   
 
        @abstractmethod
        def calculate_perimeter(self) -> float:
            """ Return the perimeter (circumference) of the shape. """
    
    
        def describe(self) -> str:
            return (
                f"{self.__class__.__name__}\n"
                f"    Area      : {self.calculate_area():.4f}\n"
                f"    Perimeter : {self.calculate_perimeter():.4f}"
            )
 


# ─────────────────────────────────────────────
#  Concrete Shapes
# ─────────────────────────────────────────────

"""
A circle defined by its radius.

Area      = π r²
Perimeter = 2 π r  (circumference)
"""

class Circle(Shape):


    def __init__(self, radius: float):
        if radius <= 0:
            raise ValueError("Radius must be a positive number.")
        self.radius = radius

    def calculate_area(self) -> float:
        return math.pi * self.radius ** 2

    def calculate_perimeter(self) -> float:
        return 2 * math.pi * self.radius

    def __str__(self) -> str:
        return f"Circle(radius={self.radius})"


"""
A square defined by its side length.

Area      = s²
Perimeter = 4 s
"""

class Square(Shape):
    def __init__(self, side: float):
        if side <= 0:
            raise ValueError("Side length must be a positive number.")
        self.side = side

    def calculate_area(self) -> float:
        return self.side ** 2

    def calculate_perimeter(self) -> float:
        return 4 * self.side

    def __str__(self) -> str:
        return f"Square(side={self.side})"


class Rectangle(Shape):
    """
    A rectangle defined by its width and height.

    Area      = w × h
    Perimeter = 2 (w + h)
    """

    def __init__(self, width: float, height: float):
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive numbers.")
        self.width = width
        self.height = height

    def calculate_area(self) -> float:
        return self.width * self.height

    def calculate_perimeter(self) -> float:
        return 2 * (self.width + self.height)

    def __str__(self) -> str:
        return f"Rectangle(width={self.width}, height={self.height})"


# ─────────────────────────────────────────────
#  Console UI Helpers
# ─────────────────────────────────────────────

WIDTH = 52

BANNER = r"""
  ____  _
 / ___|| |__   __ _ _ __   ___  ___
 \___ \| '_ \ / _` | '_ \ / _ \/ __|
  ___) | | | | (_| | |_) |  __/\__ \
 |____/|_| |_|\__,_| .__/ \___||___/
                    |_|
       Shape Calculator by Greg Tovar 2026
"""

SHAPE_ICONS = {
    "Circle":    "🔵",
    "Square":    "🟦",
    "Rectangle": "🟩",
}


def divider(char="─"):
    print(char * WIDTH)


def header(title: str):
    print()
    divider("═")
    print(f"  {title}")
    divider("═")


def success(msg: str):
    print(f"  ✅  {msg}")


def error(msg: str):
    print(f"  ❌  {msg}")


def prompt_float(label: str) -> float:
    while True:
        try:
            val = float(input(f"    {label}: ").strip())
            return val
        except ValueError:
            error("Please enter a valid number.")


def prompt_int(label: str, lo: int, hi: int) -> int:
    while True:
        try:
            val = int(input(f"  {label}: ").strip())
            if lo <= val <= hi:
                return val
            error(f"Enter a number between {lo} and {hi}.")
        except ValueError:
            error("Please enter a whole number.")


# ─────────────────────────────────────────────
#  Shape Creation Wizards
# ─────────────────────────────────────────────

def build_circle() -> Circle:
    header("🔵  New Circle")
    r = prompt_float("Radius")
    return Circle(r)


def build_square() -> Square:
    header("🟦  New Square")
    s = prompt_float("Side length")
    return Square(s)


def build_rectangle() -> Rectangle:
    header("🟩  New Rectangle")
    w = prompt_float("Width")
    h = prompt_float("Height")
    return Rectangle(w, h)


BUILDERS = {1: build_circle, 2: build_square, 3: build_rectangle}


# ─────────────────────────────────────────────
#  Display Results
# ─────────────────────────────────────────────

def show_result(shape: Shape):
    icon = SHAPE_ICONS.get(shape.__class__.__name__, "🔷")
    name = shape.__class__.__name__
    header(f"{icon}  {name} Results")
    print(f"  Shape     : {shape}")
    print(f"  Area      : {shape.calculate_area():.4f}")
    print(f"  Perimeter : {shape.calculate_perimeter():.4f}")
    divider()


# ─────────────────────────────────────────────
#  Session History
# ─────────────────────────────────────────────

def show_history(history: list[Shape]):
    header("📋  Calculation History")
    if not history:
        print("  No shapes calculated yet.")
    else:
        for i, shape in enumerate(history, 1):
            icon = SHAPE_ICONS.get(shape.__class__.__name__, "🔷")
            print(f"  {i:>2}. {icon}  {shape}")
            print(f"       Area: {shape.calculate_area():.4f}  |  "
                  f"Perimeter: {shape.calculate_perimeter():.4f}")
    divider()


# ─────────────────────────────────────────────
#  Main Menu
# ─────────────────────────────────────────────

def main():
    print(BANNER)
    divider()
    print("  Calculate area & perimeter for any shape.\n")

    history: list[Shape] = []

    while True:
        header("Main Menu")
        print("    1.  🔵  Circle")
        print("    2.  🟦  Square")
        print("    3.  🟩  Rectangle")
        print("    4.  📋  View history")
        print("    5.  🚪  Exit")
        print()

        choice = prompt_int("Choose [1-5]", 1, 5)

        if choice in BUILDERS:
            try:
                shape = BUILDERS[choice]()
                show_result(shape)
                history.append(shape)
            except ValueError as e:
                error(str(e))

        elif choice == 4:
            show_history(history)

        else:
            header("Goodbye! 👋")
            print("  Thanks for using the Shape Calculator.\n")
            break


#
# Main Program
#


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Session ended. Goodbye! 👋\n")


#
# End of Main Program
#
