#
#  Cree una calculadora por linea de comando. Esta debe de tener un número actual,
#  y un menú para decidir qué operación hacer con otro número
# 


def add(curr_num, num):
    return curr_num + num;

def substract(curr_num, num):
    return curr_num - num;

def multiply(curr_num, num):
    return curr_num * num;

def divide(curr_num, num):
    try:
        result = curr_num / num;
        return result
    except ZeroDivisionError:
        print("❌ Error: Cannot divide by zero!");
        print();
        return curr_num;

def display_menu(actual):
    print(PURPLE); 
    print("\n==============================");
    print(f"  Current number ➡️  {actual:.5f}");
    print("==============================");
    print();
    print(DARK_GREEN); 
    print();
    print("------- 🧮 Calculator Menu -----------");
    print("1. Addition ➕ ");
    print("2. Subtraction ➖ ");
    print("3. Multiplication ✖️");
    print("4. Division ➗");
    print("5. Clear result 🟢");
    print("6. Exit Application 👋");
    print("--------------------------------------");

def draw_calculator(current_number):
    print(YELLOW + "  ╔════════════════════╗")
    print(f"  ║🧮 Gregs CALCULATOR ║")
    print(  "  ╠════════════════════╣")
    print(f"  ║  {current_number:>15.5f}   ║")
    print(  "  ╠════════════════════╣")
    print(  "  ║  1. ➕  Addition   ║")
    print(  "  ║  2. ➖  Subtraction║")
    print(  "  ║  3. ✖️   Multiply   ║")
    print(  "  ║  4. ➗  Division   ║")
    print(  "  ╠════════════════════╣")
    print(  "  ║  5. 🔄  Clear      ║")
    print(  "  ║  6. 👋  Exit       ║")
    print(  "  ╚════════════════════╝", GREEN)
    print()



def ask_number():
    try:
        return float(input("Enter a number: ⌨️ "))
    except ValueError:
        print("❌ Error: Invalid number! Please enter a valid number. ℹ️ ");
        print();
        return None

#
# --- MAIN PROGRAM - MANAGES THE LOOP ------
#

#
# Color definition  - Global Variables
#
GREEN  = "\033[92m";
DARK_GREEN  = "\033[32m"    
RED    = "\033[91m";
YELLOW = "\033[93m";
BLUE   = "\033[94m";
PURPLE = "\033[95m";
RESET  = "\033[0m";
print(DARK_GREEN);   # Default Color

#
# Variables
#
current = 0;
current_number = 0.000000000;

#
# Main Loop
#
while True:
    draw_calculator(current);
    #display_menu(current);
    menu_opcion = input("Choose an option (1-6): ⌨️ ");

    if menu_opcion == "1":    # ADD
        current_number = ask_number();
        if current_number is not None:
            current = add(current, current_number);
            print(f"✅ Result: {current:.5f}");

    elif menu_opcion == "2":  # SUBSTRACTION
        current_number = ask_number();
        if current_number is not None:
            current = substract(current, current_number);
            print(f"✅ Result: {current:.5f}");

    elif menu_opcion == "3":   # MULTIPLY
        current_number = ask_number();
        if current_number is not None:
            current = multiply(current, current_number);
            print(f"✅ Result: {current:.5f}");

    elif menu_opcion == "4":  #DIVISION
        current_number = ask_number();
        if current_number is not None:
            current = divide(current, current_number);
            print(f"✅ Result: {current:.5f}");

    elif menu_opcion == "5":   # CLEAR VARIABLE
        current = 0;
        print("✅ Result cleared! 👍");

    elif menu_opcion == "6":   #EXIT
        print();
        print("Thanks for using the calculator - Goodbye! 👋");
        print();
        break;

    else:
        print("❌ Error: Invalid option! Please choose between 1 and 6. 👎");
        print();


#
# 
# 
# --- END OF MAIN PROGRAM - MANAGES THE LOOP ------
#
#