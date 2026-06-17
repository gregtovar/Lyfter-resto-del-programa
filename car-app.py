#
#    
# Application: Vehicle - Greg Tovar - V1
#
#

 

from abc import ABC
from datetime import datetime


# ============================================================
#  COLORS / UI HELPERS
# ============================================================
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'

#
#    
# Prints a sophisticated double-frame header with a rainbow border,
# an optional subtitle line, and a credit footer.
#
#

def print_header(title, subtitle=None):
    width = 56
    rainbow = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.MAGENTA]

    def rainbow_line(ch):
        return ''.join(rainbow[i % len(rainbow)] + ch for i in range(width)) + Colors.RESET

    # outer frame (double line)
    print('\n╔' + rainbow_line('═') + '╗')
    print('║' + Colors.DIM + '·' * width + Colors.RESET + '║')

    # title, bold + rainbow per-letter
    title_colored = ''.join(
        rainbow[i % len(rainbow)] + ch for i, ch in enumerate(title)
    ) + Colors.RESET
    padding = (width - len(title)) // 2
    print('║' + ' ' * padding + Colors.BOLD + title_colored +
          ' ' * (width - len(title) - padding) + '║')

    # optional subtitle, dimmed white, centered
    if subtitle:
        sub_padding = (width - len(subtitle)) // 2
        print('║' + ' ' * sub_padding + Colors.DIM + Colors.WHITE + subtitle +
              Colors.RESET + ' ' * (width - len(subtitle) - sub_padding) + '║')

    print('║' + Colors.DIM + '·' * width + Colors.RESET + '║')
    print('╚' + rainbow_line('═') + '╝')

    credit = 'Developed by Greg Tovar  -  June 2026  -  v1.0'
    print(Colors.DIM + Colors.WHITE + credit.center(width + 2) + Colors.RESET)


def pause():
    input("\nPress Enter to continue...")

#
#    
# Color-codes vehicle type labels for quick visual scanningder,
#
#

def color_type(label):
    if label.lower() == "car":
        return f"{Colors.BLUE}{Colors.BOLD}{label}{Colors.RESET}"
    return f"{Colors.MAGENTA}{Colors.BOLD}{label}{Colors.RESET}"


# ============================================================
#  BASE CLASS
# ============================================================
class Vehicle(ABC):

    def __init__(self, brand, year):
        self._brand = brand
        self._year = year

    @property
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, new_brand):
        if not new_brand.strip():
            raise ValueError("Brand cannot be empty.")
        self._brand = new_brand

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, new_year):
        if new_year < 1886:  # the year the first automobile was patented
            raise ValueError("Year is not valid.")
        self._year = new_year

    def get_info(self):
        return f"{self._brand} ({self._year})"

    def vehicle_type(self):
        return self.__class__.__name__


# ============================================================
#  SUBCLASSES
# ============================================================
class Car(Vehicle):
    def __init__(self, brand, year, doors):
        super().__init__(brand, year)
        self._doors = doors

    @property
    def doors(self):
        return self._doors

    @doors.setter
    def doors(self, new_doors):
        if new_doors <= 0:
            raise ValueError("Doors must be a positive number.")
        self._doors = new_doors

    def get_info(self):
        return f"{super().get_info()} - {self._doors} doors"


#
#    
# Motorcycle CLASS
#
#

class Motorcycle(Vehicle):
    def __init__(self, brand, year, m_type):
        super().__init__(brand, year)
        self._type = m_type

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, new_type):
        if not new_type.strip():
            raise ValueError("Type cannot be empty.")
        self._type = new_type

    def get_info(self):
        return f"{super().get_info()} - Type: {self._type}"


# ============================================================
#  FLEET MANAGEMENT (the "app" logic)
# ============================================================
def select_vehicle(vehicles):
    if not vehicles:
        print("\nNo vehicles yet. Add one first.")
        return None

    print("\nSelect a vehicle:")
    for i, v in enumerate(vehicles, start=1):
        print(f"  {i}. [{color_type(v.vehicle_type())}] {v.get_info()}")

    try:
        choice = int(input("Enter number: "))
        if 1 <= choice <= len(vehicles):
            return vehicles[choice - 1]
        print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")
    return None

#
#    
# Add Car
#
#
def add_vehicle(vehicles):
    print_header("Add Vehicle", "Register a new car or motorcycle")
    print("Vehicle type:")
    print("  1. Car")
    print("  2. Motorcycle")
    type_choice = input("Choose type: ").strip()

    if type_choice not in ("1", "2"):
        print(f"\n{Colors.RED}✘ Invalid vehicle type.{Colors.RESET}")
        return

    brand = input("Brand: ").strip()
    if not brand:
        print(f"\n{Colors.RED}✘ Brand cannot be empty.{Colors.RESET}")
        return

    try:
        year = int(input("Year: "))
    except ValueError:
        print(f"\n{Colors.RED}✘ Year must be a number.{Colors.RESET}")
        return

    try:
        if type_choice == "1":
            doors = int(input("Number of doors: "))
            vehicle = Car(brand, year, doors)
        else:
            m_type = input("Type (e.g. Sport, Cruiser, Touring): ").strip()
            vehicle = Motorcycle(brand, year, m_type)
    except ValueError as e:
        print(f"\n{Colors.RED}✘ Error: {e}{Colors.RESET}")
        return

    vehicles.append(vehicle)
    print(f"\n{Colors.GREEN}✔ Added: {vehicle.get_info()}{Colors.RESET}")

#
#    
# Edit CAR
#
#
def edit_vehicle(vehicles):
    print_header("Edit Vehicle", "Update brand, year, or specs")
    vehicle = select_vehicle(vehicles)
    if vehicle is None:
        return

    try:
        new_brand = input(f"New brand (leave blank to keep '{vehicle.brand}'): ").strip()
        if new_brand:
            vehicle.brand = new_brand

        new_year = input(f"New year (leave blank to keep '{vehicle.year}'): ").strip()
        if new_year:
            vehicle.year = int(new_year)

        if isinstance(vehicle, Car):
            new_doors = input(f"New door count (leave blank to keep '{vehicle.doors}'): ").strip()
            if new_doors:
                vehicle.doors = int(new_doors)
        elif isinstance(vehicle, Motorcycle):
            new_type = input(f"New type (leave blank to keep '{vehicle.type}'): ").strip()
            if new_type:
                vehicle.type = new_type

        print(f"\n{Colors.GREEN}✔ Updated: {vehicle.get_info()}{Colors.RESET}")
    except ValueError as e:
        print(f"\n{Colors.RED}✘ Error: {e}{Colors.RESET}")


#
#    
# Remove Car
#
#

def remove_vehicle(vehicles):
    print_header("Remove Vehicle", "Take a vehicle out of the fleet")
    vehicle = select_vehicle(vehicles)
    if vehicle is None:
        return

    confirm = input(f"Remove '{vehicle.get_info()}'? (y/n): ").strip().lower()
    if confirm == "y":
        vehicles.remove(vehicle)
        print(f"\n{Colors.GREEN}✔ Vehicle removed.{Colors.RESET}")
    else:
        print("\nCancelled.")


#
#    
# List Car
#
#
def list_vehicles(vehicles):
    print_header("Fleet List", "All registered vehicles")
    if not vehicles:
        print("No vehicles yet.")
    else:
        for i, v in enumerate(vehicles, start=1):
            print(f"  {i}. [{color_type(v.vehicle_type())}] {v.get_info()}")


# ============================================================
#  MAIN MENU
# ============================================================
def main():
    start_time = datetime.now()

    # seed with the example from the prompt
    vehicles = [Car("Toyota", 2020, 4), Motorcycle("Yamaha", 2022, "Sport")]

    menu = """
1. List vehicles
2. Add vehicle
3. Edit vehicle
4. Remove vehicle
5. Exit
"""

    while True:
        print_header("Vehicle Fleet Manager", "Cars & Motorcycles Registry")
        print(menu)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            list_vehicles(vehicles)
        elif choice == "2":
            add_vehicle(vehicles)
        elif choice == "3":
            edit_vehicle(vehicles)
        elif choice == "4":
            remove_vehicle(vehicles)
        elif choice == "5":
            print(f"\n{Colors.YELLOW}Goodbye, Thanks for Running the App!{Colors.RESET}")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Session ended: {timestamp}")

            elapsed = datetime.now() - start_time
            minutes = elapsed.total_seconds() / 60
            print(f"Total time running: {minutes:.2f} minutes")
            break
        else:
            print(f"\n{Colors.RED}Invalid option, try again.{Colors.RESET}")

        pause()


#
#    
# Main program
#
#
if __name__ == "__main__":
    main()

#
#    
# End of Main Program
#
#