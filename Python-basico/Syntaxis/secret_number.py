import random

# Generate a random number between 1 and 10
secret_number = random.randint(1, 10)
out_of_range = False;

print("********************************************")
print("Guess the secret number between 1 and 10!")
print("********************************************")

while True:
    guess_input = input("Enter your guess - 1-10: ")

    # Validate input
    if not guess_input.isdigit():
        print("Please enter a valid number.")
        continue

    guess = int(guess_input)
    #
    # For Debugging
    # print(guess);     Removed because is for debugging
    #
    #  Check the guess logic
    #
    out_of_range = False;
    if guess < 1:
        print("The number is out of range, less than 1!")
        out_of_range = True;
        break;
    if guess > 10:
        print("The number is out of range, bigger than 10!")
        out_of_range = True;
        break;
    if  out_of_range == False:  # The number is valid from 1 to 10
        if guess < secret_number:
            print("Too low, try again my friend!")
        elif guess > secret_number:
            print("Too high, try again! No worries!")
        else:
            print(" Congratulations User! You guessed the number correctly!")
            break
#
# End of program
#
