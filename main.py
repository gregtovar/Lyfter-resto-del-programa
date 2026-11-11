"""
Personal Finance Manager.

Main PY

Lets the user choose between the Console interface and the FreeSimpleGUI
interface. Both share the same FinanceManager instance and the same CSV
files in the data/ directory.


Greg Tovar NOV11 2016

"""


#
# Imports
#

import os
import sys


#
# Imports Fuctions - modular based
#

from core.finance_manager import FinanceManager
from core.exceptions import FinanceManagerError
from ui.console_ui import ConsoleUI


#
# Path
#

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def print_startup_menu() -> None:
    print("=" * 40)
    print("       PERSONAL FINANCE MANAGER")
    print("=" * 40)
    print()
    print("Select the application interface:")
    print()
    print("1. Console Mode (Text-Based)")
    print("2. GUI Mode (FreeSimpleGUI)")
    print("0. Exit")
    print()


#
# Main App Starts here!
#

def main() -> None:
    try:
        finance_manager = FinanceManager(DATA_DIR)
    except FinanceManagerError as error:
        print(f"Fatal error: could not load application data.\n{error}")
        sys.exit(1)

    while True:
        print_startup_menu()
        choice = input("Enter your selection: ").strip()

        if choice == "1":
            # Exiting the Console UI returns here, back to the startup menu,
            # instead of quitting the whole application.
            ConsoleUI(finance_manager).run()
        elif choice == "2":
            try:
                from ui.gui_ui import GUIUI
            except ImportError as error:
                print(f"Could not start GUI mode: {error}")
                print("Make sure FreeSimpleGUI is installed (see requirements.txt).")
                continue
            try:
                # Closing the GUI window returns here, back to the startup menu.
                GUIUI(finance_manager).run()
            except Exception as error:  # Catch-all so a GUI failure never crashes the app.
                print(f"An unexpected error occurred in GUI mode: {error}")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.\n")



#
# Main App
#

if __name__ == "__main__":
    main()
