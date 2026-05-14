#
#  Ejercicio 3:
#  cree un diccionario usando dos listas del mismo tamaño, usando una 
#  para sus keys, y la otra para sus values.
#
list_a = ['first_name', 'last_name', 'role'];
list_b = ['Greg', 'Tovar', 'Software Engineer'];

#usando la instruccion ZIP para crear el diccionario
my_dict = dict(zip(list_a, list_b));  

print();
print('------- program output -----------');
print();
print(my_dict)
print();
print('------- end of program -----------');

