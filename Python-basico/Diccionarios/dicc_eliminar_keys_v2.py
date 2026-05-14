#
#  Ejercicio 4:
#  eliminar keys de un diccionario. VERSION 2
#
#
# Variables
#
key = str;          # to be used in the loop to check
employee = {
    'name': 'Greg',
    'email': 'greg@abc.com',
    'access': 5,
    'age' : 30
}
#
# Declaracion de lista que se usara para eliminar los keys en el dicc.
#
# 
list_of_keys = ["access", "age" ];             
#
# Logic of the program
#
print();
print('------- program output -----------');
print();
print("Dictionary BEFORE removal of keys:");
print(employee)
print();
#
# Remove values with a loop looking for the keys in the list of keys to be removed.   
#
for key in list_of_keys:    # if the key is found in the employee dict, then delete it.
    if key in employee:   
        del employee[key]
# end of loop

#        

print("Dictionary AFTER removal of keys:");
print(employee);
print();
print('------- end of program -----------');

