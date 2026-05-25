#
# main.py
# Entry point for the Student Management System (v2 — OOP edition).
# Students are stored as Student objects instead of plain dictionaries.
#
#

from colors import choose_theme, cprint, BOLD, RESET
from menu   import run_menu


def main() -> None:
    cprint(f"\n  {BOLD}  ✦  Student Management System  ✦{RESET}")
    choose_theme()

    students = []   # list of Student objects
    run_menu(students)


if __name__ == "__main__":
    main()
