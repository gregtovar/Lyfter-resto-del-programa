#
#  Ask user for input
#

num1 = float(input("Enter first number: "));
num2 = float(input("Enter second number: "));
num3 = float(input("Enter third number: "));

#
# # Find the largest number
#
largest = num1;

if num2 > largest:
    largest = num2;

if num3 > largest:
    largest = num3;

# Output result
print(f"The largest number is: {largest}");

#
# End of program
#
