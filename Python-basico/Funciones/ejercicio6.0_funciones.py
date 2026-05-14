#
# Ejercicio 6.0: 
# Cree una función que acepte un string con palabras separadas por un guion
#  y retorne un string igual pero ordenado alfabéticamente.
#

#
# Function Declaration,  
#
def sort_words(my_string_param):
    temp_string = my_string_param.split("-");       # convert to list
    temp_string.sort();                             # sort alphabetically
    string_added_dashes = "-".join(temp_string);    # convert back to string
    return string_added_dashes;

#
#  Variables
#  
my_global_string = "python-variable-funcion-computadora-monitor";
global_sorted_string = "";   

#
#  Main Program
#  
global_sorted_string = sort_words(my_global_string);
print();
print("------ OUTPUT--------");
print(my_global_string, "→", global_sorted_string);                      
print();
#
#  End of Main Program
#  