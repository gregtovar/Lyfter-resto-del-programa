#
# Ejercicio 5.0: 
# Cree una función que imprima el número de mayúsculas y el número de minúsculas en un string.
#

#
# Function Declaration,  
#
def count_characters(my_string):
    upper = 0
    lower = 0
    for character in my_string:
        if character.isupper():
            upper += 1
        elif character.islower():
            lower += 1
    return upper, lower;

#
#  Variables
#  
my_global_string = "I love Nación Sushi";     
global_upper = 0;
global_lower = 0;
global_count = 0;
#
#  Main Program
#  
global_upper, global_lower = count_characters(my_global_string);
print();
print("------ OUTPUT--------");
print("There's", global_upper, "upper cases and", global_lower ,"lower cases");                      
print();
#
#  End of Main Program
#  