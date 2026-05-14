#
#  Sum of Numbers
# 

# Vars
number: int = 0;
total: int = 0;
join: str = "";

# Input
number = int(input("Enter a number: "));
 
# logic
for i in range(1, number + 1):
    total += i;
sequence = " + ".join(str(i) for i in range(1, number + 1));
print(f"\n{number} → {total} ({sequence})");
print(f"\n");
print(f"\n");
#
# End of program
#




