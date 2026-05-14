#
# 
#  Sum of 30
# 
n1 = 0;
n2 = 0;
n3 = 0;

#
# Input
#
n1 = int(input("Enter the first number: "))
n2 = int(input("Enter the second number: "))
n3 = int(input("Enter the third number: "))
 
#
# Logic
#

if ((n1 == 30 or n2 == 30 or n3 == 30) or (n1 + n2 + n3)==30):
    print("\n✅ Correct!");
else:
    print("\n❌ Incorrect.");

#
# End of program
#
