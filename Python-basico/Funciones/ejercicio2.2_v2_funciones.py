#
# Ejercicio 2.2 V2: 
# Intente acceder a una variable global desde una función y cambiar su valor.
#

#
# Function Declaration
#

def function_global_vars():
    age: int = 25;
    percentage_age: float = 0.15;
    percentage: float = 0.00;
    percentage = age * percentage_age;
    global_age = 80;        # Global variable modified
    global_days = 120;      # Global variable modified
    return;

#
# Variables
#  
global_age = 10;   #initial values
global_days = 30;    #initial values
#
#  Main Program
#  
print();
print("------ OUTPUT--------");
print("Variable global_age: ", global_age);
print("Variable global_days", global_days);
#
# Run Function
#
function_global_vars();         #make chages global vars
#
# Print values
#
print("Function Executed!, new values assigned to global vars:");
print("Variable global_age: ", global_age);
print("Variable global_days", global_days);
print();
print("------ END OF PROGRAM --------");
print();
#
#  End of Main Program
#  