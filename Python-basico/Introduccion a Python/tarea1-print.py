#
# program Homework 1
#

# imports
import random;
import math;

# Variables Definition
hw = "Hello World! String Var";
age = 25;
numbers = [1, 2, 3, 4];
is_student = True
name = "Greg";
R_num = random.random();
R_num2 = random.random();
count_while = 1;
ONE_HUNDRED = 100;

# Program
age = age +3;

# Printing Values
print("Hello World!");
print(hw);
print(age);
print(is_student);
print(numbers);
print("\n");
print("\n");
print("My name is {name} and I am {age} years old")

# Printing Math Ops
print("The number 10: ",5+5);
print("The number 10: ",5+5);
print("Random Number is :", R_num);


while count_while <= 5:
    R_num = round(random.random(), 4);
    print("Random:", R_num);
    count_while += 1;
    print("Random 2:",math.floor(round((R_num * R_num2*ONE_HUNDRED),0)));


print("\n");
print("****** End of Execution ******* ");
print("\n");
print("\n");

# end

