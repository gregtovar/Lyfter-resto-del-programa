#
# Ejercicio 1: Cree dos funciones que impriman dos 
# cosas distintas, y haga que la primera llame la segunda.
#

#
# Function Declaration
#

def function_2():
    print("¡Es muy chévere aprender Python!");
    return;

def function_1():
    print("¡Hola Mundo!");
    function_2();
    return;
 
#
#  Main Program
#  
print();
print("------ OUTPUT--------");
function_1();
print();
#
#  End of Main Program
#  