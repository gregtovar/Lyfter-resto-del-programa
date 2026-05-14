#
# App: Remove odds
#

#
# Variables
#

# Lists
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ,13, 14];
even_list = [];
number = 0;

#
# Logic
#
print();
print("---- Program Output ---------");
print();
print(f"Original list: {my_list}");
print();
for number in my_list:
    if number % 2 == 0:
        even_list.append(number)
 
print(f"Even list:     {even_list}")
 
print();
print("---- End ---------");
print("--------------------------");
#
# End of program
#