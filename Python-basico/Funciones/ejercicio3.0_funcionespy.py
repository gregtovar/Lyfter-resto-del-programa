#
# Ejercicio 3.0: 
# Cree una función que retorne la suma de todos los números de una lista.
#

#
# Function Declaration, 2 prameters - List and 
#
def function_add_list(my_list_local):
    sum = 0;   
    for index_value in my_list_local:
        sum = sum + index_value;
    return sum;
 
#
#  Variables
#  
my_global_list = [1,2,3,4,5,6,7,8,9,10];                # List Delaration
my_global_list_sum = 0;                                 # Sum of list

#
#  Main Program
#  
# print();
print("------ OUTPUT--------");
my_global_list_sum = function_add_list(my_global_list);
print();
print(my_global_list, "→", my_global_list_sum);
#
#  End of Main Program
#  