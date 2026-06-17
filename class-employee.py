#
# 
#   Employee Class Exercise June 2026
# 
#   Greg Tovar
# 
#    @property and @setter


from datetime import datetime

class Employee:
    def __init__(self, name, salary):
        self._name = name
        self.salary = salary   

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if not new_name.strip():
            raise ValueError("Name cannot be empty.")
        self._name = new_name

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, new_salary):
        if new_salary < 0:
            raise ValueError("Salary cannot be negative.")
        self._salary = new_salary


    def promote(self, percentage):
        if percentage < 0:
            raise ValueError("Promotion percentage cannot be negative.")
        self.salary = self._salary * (1 + percentage)

    def __str__(self):
        return f"{self._name} - ${self._salary:,.2f}"


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


def pause():
    input("\nPress Enter to continue...")

#
#     Prints a colorful, character-art style header with a rainbow border
#     (Character based)
#

def print_header(title):
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

#
#     In case of edits in employees, select the employee 
#     based on a list
#
def select_employee(employees):
    if not employees:
        print("\nNo employees yet. Add one first.")
        return None

    print("\nSelect an employee:")
    for i, emp in enumerate(employees, start=1):
        print(f"  {i}. {emp}")

    try:
        choice = int(input("Enter number: "))
        if 1 <= choice <= len(employees):
            return employees[choice - 1]
        print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")
    return None

#
#     Add
#    
#
def add_employee(employees):
    print_header("Add Employee")
    name = input("Name: ").strip()
    try:
        salary = float(input("Starting salary: "))
        emp = Employee(name, salary)
        employees.append(emp)
        print(f"\n✔ {emp.name} added with salary ${emp.salary:,.2f}")
    except ValueError as e:
        print(f"\n✘ Error: {e}")

#
#     Increase salary
#     
#
def promote_employee(employees):
    print_header("Promote Employee")
    emp = select_employee(employees)
    if emp is None:
        return
    try:
        pct = float(input(f"Promotion % for {emp.name} (e.g. 10 for 10%): ")) / 100
        old_salary = emp.salary
        emp.promote(pct)
        print(f"\n✔ {emp.name}'s salary: ${old_salary:,.2f} → ${emp.salary:,.2f}")
    except ValueError as e:
        print(f"\n✘ Error: {e}")

#
#     Update Salary
#

def update_salary(employees):
    print_header("Update Salary")
    emp = select_employee(employees)
    if emp is None:
        return
    try:
        new_salary = float(input(f"New salary for {emp.name}: "))
        emp.salary = new_salary
        print(f"\n✔ {emp.name}'s salary updated to ${emp.salary:,.2f}")
    except ValueError as e:
        print(f"\n✘ Error: {e}")

#
#     List Salary
#
def list_employees(employees):
    print_header("Employee List")
    if not employees:
        print("No employees yet.")
    else:
        for i, emp in enumerate(employees, start=1):
            print(f"  {i}. {emp}")

#
# Registers time app was running
#

def print_session_duration(start_time):
    elapsed = datetime.now() - start_time
    minutes = elapsed.total_seconds() / 60
    print(f"Total time running: {minutes:.2f} minutes")


#
#     Menu Display
#
def main():
    start_time = datetime.now()
    employees = [Employee("John", 1000)]  # Add initial employee

    menu = """
1. List employees
2. Add employee
3. Promote employee
4. Update salary directly
5. Exit
"""

    while True:
        print_header("Employee Manager")
        print(menu)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            list_employees(employees)
        elif choice == "2":
            add_employee(employees)
        elif choice == "3":
            promote_employee(employees)
        elif choice == "4":
            update_salary(employees)
        elif choice == "5":
            print("\nGoodbye, Thanks for Running the App!")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Session ended: {timestamp}")
            print_session_duration(start_time)
            break
        else:
            print("\nInvalid option, try again.")

        pause()



#
#     Main Program
#

if __name__ == "__main__":
    main()


#
#     End of Main Program
#