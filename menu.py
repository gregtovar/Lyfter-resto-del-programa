##
##menu.py
##All logic related to displaying the menu and validating user option input.
##

from colors import cprint, cinput

MENU_OPTIONS = {
    "1": "Enter student information",
    "2": "View all students",
    "3": "View top 3 students (by average)",
    "4": "View overall average grade",
    "5": "Export data to CSV",
    "6": "Import data from CSV",
    "7": "Delete a student",
    "8": "View failed students",
    "9": "View worst students sorted by average",
    "0": "Exit",
}

# Print the main menu to the console. 
def display_menu() -> None:
    cprint("\n" + "═" * 45)
    cprint("       STUDENT GRADE MANAGER")
    cprint("═" * 45)
    for key, description in MENU_OPTIONS.items():
        cprint(f"  [{key}]  {description}")
    cprint("═" * 45)


#  
#    Prompt the user to choose a menu option and keep asking
#    until a valid key is entered.
#
#    Returns the validated option string (e.g. '1', '0').
#     

def get_valid_option() -> str:
  
    valid_keys = set(MENU_OPTIONS.keys())
    while True:
        choice = cinput("Select an option: ").strip()
        if choice in valid_keys:
            return choice
        cprint(f"  ✗ '{choice}' is not a valid option. Please choose from: {', '.join(sorted(valid_keys))}.")
