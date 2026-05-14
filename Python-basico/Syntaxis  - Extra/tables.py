#
#  Tables
# 
4
# variables
number = 0;
i = 0;

#
# input
#

number = int(input("Enter a number (1-10): "));

if number <= 10:   #will not manage anything above 10
    print(f"\nMultiplication table for {number}:\n");
    for i in range(1, 13):
        print(f"{number} x {i} = {number * i}");
    
else:
    print("Number too high, bigger than 10!");

# 
#  End of program
# 