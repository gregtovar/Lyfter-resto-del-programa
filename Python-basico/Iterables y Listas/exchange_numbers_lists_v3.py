#
# App: Swap string 1st and last position only
#

#
# Variables
#

my_list = [4, 3, 6, 1, 7]; # original list
first = 0;
last = 0;

#
# Logic
#
print();
print("---- Program Output ---------");
print();
print(f"Original list: {my_list}")
#
# swap values
#
last = my_list[-1];   # Swap Value
first = my_list[0];   # Swap Value
my_list[-1] = first;
my_list[0] = last;

#
#  Print
#  
print(f"Swapped list:  {my_list}");
print();
print("---- End ---------");
print("--------------------------");
#
# End of program
#