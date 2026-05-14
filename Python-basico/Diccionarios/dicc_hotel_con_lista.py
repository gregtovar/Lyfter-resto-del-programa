#
#  Ejercicio 2:
#  Diccionario que guarde la siguiente información sobre un hotel 
# con lista
#
my_hotel = {
    "nombre": "Sheraton",
    "estrellas": 4,
    "habitaciones": [
        {"numero": 101, "piso": 1, "precio": 120},
        {"numero": 102, "piso": 1, "precio": 150},
        {"numero": 201, "piso": 2, "precio": 180},
        {"numero": 202, "piso": 2, "precio": 200},
    ]
}
print();
print('------- program output -----------');
print();
print(my_hotel);
print();
print(my_hotel["habitaciones"][1]["precio"]);
print('------- end of program -----------');