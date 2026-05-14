#
# Ejercicio 2.1: 
# Intente acceder a una variable definida dentro de una función desde afuera.
#

#
# Function Declaration
#

def function_01():
    age: int = 25;
    percentage_age: float = 0.15;
    percentage: float = 0.00;
    percentage = age * percentage_age;
    print (percentage);
    return;

 
#
#  Main Program
#  
print();
print("------ OUTPUT--------");
print(age);
function_01();
print();
#
#  End of Main Program
#  