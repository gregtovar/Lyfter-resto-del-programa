#
# Ejercicio 4.0: 
# Cree una función que le dé la vuelta a un string y lo retorne.
#

#
# Function Declaration - 
#
def invert_function(text_to_invert):
    return text_to_invert[::-1];

#
#  Variables
#  
my_string = "Hola Mundo";     
inverted_string = "";    

#
#  Main Program
#  
print();
print("------ OUTPUT--------");
inverted_string = invert_function(my_string);
print(inverted_string);                         
print();
#
#  End of Main Program
#  