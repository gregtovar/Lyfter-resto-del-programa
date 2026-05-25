#
# Menu.py
#All logic related to displaying the menu and dispatching user choices
# ##
# 
# 


from actions import (add_student, view_all_students, view_top3,
                     view_overall_average, view_worst_students)
from data    import export_to_csv, import_from_csv
from colors  import cprint, cinput, BOLD, DIM, RESET

_OPTIONS = {
    "1": "Add a student",
    "2": "View all students",
    "3": "View top 3 students",
    "4": "View overall class average",
    "5": "View students by lowest average",
    "6": "Export to CSV",
    "7": "Import from CSV",
    "8": "Exit",
}


def show_menu() -> str:
    """Print the menu and return the user's validated choice."""
    cprint(f"\n  {'─' * 44}")
    cprint(f"  {BOLD}  🎓  Student Manager{RESET}")
    cprint(f"  {'─' * 44}")
    for key, label in _OPTIONS.items():
        cprint(f"  {DIM}  {key}.{RESET}  {label}")
    cprint(f"  {'─' * 44}")

    while True:
        choice = cinput("\n  Option » ").strip()
        if choice in _OPTIONS:
            return choice
        print(f"  ✖  Invalid option. Please choose 1–{len(_OPTIONS)}.")


def run_menu(students: list) -> None:
    """Main loop: show menu, dispatch action, repeat until Exit."""
    while True:
        choice = show_menu()

        if   choice == "1": add_student(students)
        elif choice == "2": view_all_students(students)
        elif choice == "3": view_top3(students)
        elif choice == "4": view_overall_average(students)
        elif choice == "5": view_worst_students(students)
        elif choice == "6": export_to_csv(students)
        elif choice == "7": import_from_csv(students)
        elif choice == "8":
            cprint(f"\n  {BOLD}  Goodbye! 👋{RESET}\n")
            break
