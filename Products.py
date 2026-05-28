#
# Products
#


import random

# ── Colors ─────────────────────────────────────────────
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

c = colors()

#
# Class Products
#

class Product:
    def __init__(self, name: str, price: float, quantity: int):
        self.product_id = random.randint(10000, 99999)
        self.name       = name
        self.price      = price
        self.quantity   = quantity

    def total_value(self) -> float:
        return self.price * self.quantity

    def __str__(self) -> str:
        return (f"[#{self.product_id}]  {self.name:<20}  "
                f"${self.price:>9.2f}  x{self.quantity:<5}  "
                f"= ${self.total_value():>10.2f}")


#
# Class Inventory 
#

class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def find_by_id(self, product_id: int) -> Product | None:
        for p in self.products:
            if p.product_id == product_id:
                return p
        return None

    def remove_product(self, product_id: int) -> bool:
        product = self.find_by_id(product_id)
        if product:
            self.products.remove(product)
            return True
        return False

    def display_all(self) -> None:
        bar = "─" * 66
        print(f"\n  {c['BLUE']}{bar}{c['RESET']}")
        print(f"  {c['BOLD']}{c['PURPLE']}  📦  Inventory  "
              f"{c['DIM']}({len(self.products)} products){c['RESET']}")
        print(f"  {c['BLUE']}{bar}{c['RESET']}")

        if not self.products:
            print(f"  {c['DIM']}    No products in inventory.{c['RESET']}")
        else:
            print(f"  {c['DIM']}  {'ID':<9} {'Name':<20}  {'Price':>10}  {'Qty':<6}  {'Subtotal':>12}{c['RESET']}")
            print(f"  {c['DIM']}{bar}{c['RESET']}")
            for p in self.products:
                print(f"  {c['CYAN']}{p}{c['RESET']}")

        print(f"  {c['BLUE']}{bar}{c['RESET']}\n")

    def calculate_total_value(self) -> float:
        return sum(p.total_value() for p in self.products)


#
# Input
#

def ask_str(prompt: str) -> str:
    while True:
        value = input(f"  {c['YELLOW']}  {prompt} » {c['RESET']}").strip()
        if value:
            return value
        print(f"  {c['RED']}✖  This field cannot be empty.{c['RESET']}")

def ask_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(f"  {c['YELLOW']}  {prompt} » {c['RESET']}"))
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            print(f"  {c['RED']}✖  Enter a valid positive number.{c['RESET']}")

def ask_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(f"  {c['YELLOW']}  {prompt} » {c['RESET']}"))
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            print(f"  {c['RED']}✖  Enter a valid positive integer.{c['RESET']}")

def ask_id(prompt: str) -> int:
    while True:
        try:
            return int(input(f"  {c['YELLOW']}  {prompt} » {c['RESET']}"))
        except ValueError:
            print(f"  {c['RED']}✖  Enter a valid product ID.{c['RESET']}")

def section(title: str) -> None:
    print(f"\n  {c['BLUE']}{'─' * 44}{c['RESET']}")
    print(f"  {c['BOLD']}{c['PURPLE']}  {title}{c['RESET']}")
    print(f"  {c['BLUE']}{'─' * 44}{c['RESET']}\n")


#
# Menu
#

def action_add(inv: Inventory) -> None:
    section("➕  Add New Product")
    name     = ask_str("📦  Name    ")
    price    = ask_float("💲  Price   ")
    quantity = ask_int("🔢  Quantity")
    p = Product(name, price, quantity)
    inv.add_product(p)
    print(f"\n  {c['GREEN']}✔  Product added!  "
          f"{c['DIM']}ID: #{p.product_id}  |  {p.name}  |  ${p.price:.2f}  x{p.quantity}{c['RESET']}\n")


def action_edit(inv: Inventory) -> None:
    section("✏️   Edit Product")
    if not inv.products:
        print(f"  {c['DIM']}  No products to edit.{c['RESET']}\n")
        return

    inv.display_all()
    pid = ask_id("Enter product ID to edit")
    p   = inv.find_by_id(pid)
    if not p:
        print(f"\n  {c['RED']}✖  No product found with ID #{pid}.{c['RESET']}\n")
        return

    print(f"\n  {c['DIM']}  Editing: {p.name}  (leave blank to keep current value){c['RESET']}\n")

    new_name = input(f"  {c['YELLOW']}  📦  New name  [{p.name}] » {c['RESET']}").strip()
    if new_name:
        p.name = new_name

    new_price = input(f"  {c['YELLOW']}  💲  New price [{p.price:.2f}] » {c['RESET']}").strip()
    if new_price:
        try:
            val = float(new_price)
            if val >= 0:
                p.price = val
            else:
                print(f"  {c['RED']}✖  Price ignored (negative).{c['RESET']}")
        except ValueError:
            print(f"  {c['RED']}✖  Price ignored (invalid).{c['RESET']}")

    print(f"\n  {c['GREEN']}✔  Product updated!  {c['DIM']}{p}{c['RESET']}\n")


def action_display(inv: Inventory) -> None:
    inv.display_all()


def action_total(inv: Inventory) -> None:
    section("💰  Total Inventory Value")
    if not inv.products:
        print(f"  {c['DIM']}  No products in inventory.{c['RESET']}\n")
        return
    total = inv.calculate_total_value()
    print(f"  {c['BOLD']}  Total value:  {c['GREEN']}${total:,.2f}{c['RESET']}\n")


def action_remove(inv: Inventory) -> None:
    section("🗑️   Remove Product")
    if not inv.products:
        print(f"  {c['DIM']}  No products to remove.{c['RESET']}\n")
        return

    inv.display_all()
    pid = ask_id("Enter product ID to remove")
    p   = inv.find_by_id(pid)
    if not p:
        print(f"\n  {c['RED']}✖  No product found with ID #{pid}.{c['RESET']}\n")
        return

    confirm = input(f"\n  {c['RED']}  Remove \"{p.name}\"? (y/n) » {c['RESET']}").strip().lower()
    if confirm == "y":
        inv.remove_product(pid)
        print(f"\n  {c['GREEN']}✔  \"{p.name}\" removed from inventory.{c['RESET']}\n")
    else:
        print(f"\n  {c['DIM']}  Cancelled.{c['RESET']}\n")


def show_menu() -> str:
    print(f"\n  {c['BLUE']}{'─' * 44}{c['RESET']}")
    print(f"  {c['BOLD']}{c['PURPLE']}  🗂️   Inventory Manager{c['RESET']}")
    print(f"  {c['BLUE']}{'─' * 44}{c['RESET']}")
    options = [
        ("1", "➕  Add new product"),
        ("2", "✏️   Edit existing product"),
        ("3", "📋  Display all products"),
        ("4", "💰  Calculate total value"),
        ("5", "🗑️   Remove product"),
        ("6", "🚪  Exit"),
    ]
    for key, label in options:
        print(f"  {c['DIM']}  {key}.{c['RESET']}  {label}")
    print(f"  {c['BLUE']}{'─' * 44}{c['RESET']}")

    while True:
        choice = input(f"\n  {c['CYAN']}  Option » {c['RESET']}").strip()
        if choice in [o[0] for o in options]:
            return choice
        print(f"  {c['RED']}✖  Please choose 1–6.{c['RESET']}")


#
# Main
#

print(f"\n  {c['BOLD']}{c['PURPLE']}✦  Inventory Manager  ✦{c['RESET']}")

inv = Inventory()

while True:
    choice = show_menu()

    if   choice == "1": action_add(inv)
    elif choice == "2": action_edit(inv)
    elif choice == "3": action_display(inv)
    elif choice == "4": action_total(inv)
    elif choice == "5": action_remove(inv)
    elif choice == "6":
        print(f"\n  {c['PURPLE']}  Goodbye! 📦{c['RESET']}\n")
        break