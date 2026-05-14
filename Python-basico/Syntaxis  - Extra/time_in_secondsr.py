#
# Time in Seconds program
# 

#
# Variables 
# 
seconds = 0;
missing = 0;

# Input
seconds = int(input("Enter a time in seconds: "));

TEN_MINUTES = 600;  # 10 minutes = 600 seconds
 
if seconds < TEN_MINUTES:
    missing = TEN_MINUTES - seconds;
    print(f"\n{seconds}s is less than 10 minutes.");
    print(f"Seconds missing to reach 10 minutes: {missing} seconds");
elif seconds > TEN_MINUTES:
    print(f"\n{seconds}s is Greater than 10 minutes.");
else:
    print(f"\n{seconds}s is Equal to 10 minutes.");
print(f"\n");
#
# End of program
#
