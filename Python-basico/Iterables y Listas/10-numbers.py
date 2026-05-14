#
# App: 10 numbers - show max
#

#
# Variables
#
i=0;
numbers = [];
number = 0;
start = 1;
stop = 11;
highest_number = 0;

#
# Logic
#
print();
print("---- Program Output ---------");
print();
 
for i in range(start, stop):
    number = int(input(f"Enter number {i}: "));
    numbers.append(number);
 
highest_number = numbers[0];
for number in numbers:
    if number > highest_number:
        highest_number = number;
 
print(f"\nNumbers entered: {numbers}");
print(f"The highest number was: {highest_number}");
 
 
print();
print("---- End ---------");
print("--------------------------");
#
# End of program
#