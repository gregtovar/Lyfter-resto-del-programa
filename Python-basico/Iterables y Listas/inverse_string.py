#
#. App: Print String backwards
#

#
# Variables
#
space = " ";
start = 0;
stop = 0;
step = 0;
i = 0;
my_string = 'Pizza con piña';

 
#
# Logic
#
start = (len(my_string) - 1);
stop = -1;
step = -1;
print();
print("---- Program Output ---------");
print();
for i in range(start, stop, step):
    print(my_string[i], space)
 
print();
print("---- End ---------");
print("--------------------------");
#
# End of program
#