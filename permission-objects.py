#
#
# Exercise: Inherirance - abstractmethod
#
#
#





from abc import ABC, abstractmethod
from datetime import datetime


# ============================================================
#  COLORS  
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
# Print - Front end
#

def print_header(title):
    """Prints a colorful, character-art style header with a rainbow border."""
    width = 50
    rainbow = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.MAGENTA]

    border = ''.join(rainbow[i % len(rainbow)] + '═' for i in range(width))
    print('\n╔' + border + Colors.RESET + '╗')
    print('║' + ' ' * width + '║')

    title_colored = ''.join(
        rainbow[i % len(rainbow)] + ch for i, ch in enumerate(title)
    ) + Colors.RESET
    padding = (width - len(title)) // 2
    print('║' + ' ' * padding + Colors.BOLD + title_colored +
          ' ' * (width - len(title) - padding) + '║')

    print('║' + ' ' * width + '║')
    print('╚' + border + Colors.RESET + '╝')

    credit = 'Developed by Greg Tovar  -  June 2026  -  v1.0'
    print(Colors.DIM + Colors.WHITE + credit.center(width + 2) + Colors.RESET)


def pause():
    input("\nPress Enter to continue...")


def color_role(role):
    if role.lower() == "admin":
        return f"{Colors.RED}{Colors.BOLD}{role}{Colors.RESET}"
    return f"{Colors.CYAN}{role}{Colors.RESET}"


# ============================================================
#  ABSTRACT BASE CLASS
# ============================================================
class User(ABC):

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if not new_name.strip():
            raise ValueError("Name cannot be empty.")
        self._name = new_name

    @abstractmethod
    def get_role(self):
        raise NotImplementedError

    @abstractmethod
    def has_permission(self, permission):
        raise NotImplementedError

    def __str__(self):
        return f"{self._name} ({self.get_role()})"


# ============================================================
#  CONCRETE CLASSES
# ============================================================
class AdminUser(User):
    """An administrator — always has every permission."""

    def get_role(self):
        return "Admin"

    def has_permission(self, permission):
        return True  # admins can do anything!!!


class RegularUser(User):

    ALLOWED_PERMISSIONS = {"read"}

    def get_role(self):
        return "Regular"

    def has_permission(self, permission):
        return permission.lower() in self.ALLOWED_PERMISSIONS


# ============================================================
#  USER MANAGEMENT (the "app" logic)
# ============================================================
def select_user(users):
    if not users:
        print("\nNo users yet. Add one first.")
        return None

    print("\nSelect a user:")
    for i, u in enumerate(users, start=1):
        print(f"  {i}. {u.name} - {color_role(u.get_role())}")

    try:
        choice = int(input("Enter number: "))
        if 1 <= choice <= len(users):
            return users[choice - 1]
        print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")
    return None


def add_user(users):
    print_header("Add User")
    name = input("Name: ").strip()
    if not name:
        print(f"\n{Colors.RED}✘ Name cannot be empty.{Colors.RESET}")
        return

    print("\nRole:")
    print("  1. Admin")
    print("  2. Regular")
    role_choice = input("Choose role: ").strip()

    if role_choice == "1":
        user = AdminUser(name)
    elif role_choice == "2":
        user = RegularUser(name)
    else:
        print(f"\n{Colors.RED}✘ Invalid role choice.{Colors.RESET}")
        return

    users.append(user)
    print(f"\n{Colors.GREEN}✔ {user.name} added as {color_role(user.get_role())}.{Colors.RESET}")


def edit_user(users):
    print_header("Edit User")
    user = select_user(users)
    if user is None:
        return

    new_name = input(f"New name for '{user.name}' (leave blank to keep): ").strip()
    if new_name:
        try:
            user.name = new_name
            print(f"\n{Colors.GREEN}✔ Name updated to {user.name}.{Colors.RESET}")
        except ValueError as e:
            print(f"\n{Colors.RED}✘ Error: {e}{Colors.RESET}")
    else:
        print("\nName unchanged.")


#
# Remove Users
#


def remove_user(users):
    print_header("Remove User")
    user = select_user(users)
    if user is None:
        return

    confirm = input(f"Remove '{user.name}' ({user.get_role()})? (y/n): ").strip().lower()
    if confirm == "y":
        users.remove(user)
        print(f"\n{Colors.GREEN}✔ {user.name} removed.{Colors.RESET}")
    else:
        print("\nCancelled.")

#
# List Users
#
def list_users(users):
    print_header("User List")
    if not users:
        print("No users yet.")
    else:
        for i, u in enumerate(users, start=1):
            print(f"  {i}. {u.name} - {color_role(u.get_role())}")

#
# Check Users
#
def check_permission(users):
    print_header("Check Permission")
    user = select_user(users)
    if user is None:
        return

    permission = input(f"Permission to check for {user.name} (e.g. 'read', 'delete'): ").strip()
    if not permission:
        print(f"\n{Colors.RED}✘ Permission cannot be empty.{Colors.RESET}")
        return

    allowed = user.has_permission(permission)
    color = Colors.GREEN if allowed else Colors.RED
    print(f"\n{user.name} has permission '{permission}': {color}{allowed}{Colors.RESET}")


# ============================================================
#  MAIN MENU
# ============================================================
def main():
    start_time = datetime.now()

    # seed with the example from the prompt
    users = [AdminUser("Carlos"), RegularUser("Andrea")]

    menu = """
1. List users
2. Add user
3. Edit user
4. Remove user
5. Check permission
6. Exit
"""

    while True:
        print_header("User Permission Manager")
        print(menu)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            list_users(users)
        elif choice == "2":
            add_user(users)
        elif choice == "3":
            edit_user(users)
        elif choice == "4":
            remove_user(users)
        elif choice == "5":
            check_permission(users)
        elif choice == "6":
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
# Main Program
#
if __name__ == "__main__":
    main()

#
# End of Main Program
#