#
#
#main.py
#Entry point for the Student Grade Manager CLI application.
#Run with:
#    python main.py
# 

from colors import choose_theme, cprint
from typography import choose_size, choose_type
from menu import display_menu, get_valid_option
from actions import (
    enter_students,
    view_all_students,
    view_top3,
    view_overall_average,
    delete_student,
    view_failed_students,
    view_worst_students,
)
from data import export_to_csv, import_from_csv


def main() -> None:
    """Main program loop."""
    students: list[dict] = []

    cprint("\nWelcome to the Student Grade Manager!")
    choose_theme()
    choose_size()
    choose_type()

    while True:
        display_menu()
        choice = get_valid_option()

        if choice == "1":
            enter_students(students)
        elif choice == "2":
            view_all_students(students)
        elif choice == "3":
            view_top3(students)
        elif choice == "4":
            view_overall_average(students)
        elif choice == "5":
            export_to_csv(students)
        elif choice == "6":
            import_from_csv(students)
        elif choice == "7":
            delete_student(students)
        elif choice == "8":
            view_failed_students(students)
        elif choice == "9":
            view_worst_students(students)
        elif choice == "0":
            cprint("\nGoodbye! 👋\n")
            break


if __name__ == "__main__":
    main()
