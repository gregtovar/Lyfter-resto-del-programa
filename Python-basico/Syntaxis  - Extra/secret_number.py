#
# Secret Number 
# 
# 
import random
#
# Vars
#
secret_number = 0;
attempts = 0;

# read Variable
secret_number = random.randint(1, 10)
# print("Secret:",secret_number); - used for debugging
 
print("🎯 Guess the secret number between 1 and 10!")
 
#logic
#

while True:
    guess = int(input("\nEnter your guess: "))
    attempts += 1;
 

    if guess < secret_number:
        print(" Too low! Try again.");
    elif guess > secret_number:
        print(" Too high! Try again.");
    else:
        print(f"\n Correct! The secret number was {secret_number}.");
        print(f"You guessed it in {attempts} attempt(s)!");
        if attempts > 5:
            print(f"Too many attempts! need to get better!");
        else:
            print(f"Attempts not that bad!");
        print(f"\n ");
        break;
 

 #
 # End of program
 #