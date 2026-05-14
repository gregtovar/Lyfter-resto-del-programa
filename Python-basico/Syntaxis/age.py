# Ask user for input - name and last name
#
first_name = input("Enter your first name: ")
last_name = input("Enter your last name: ")

#
#  Validate age input
#
age_input = input("Enter your age: ")

if age_input.isdigit():
    age = int(age_input)

    # Determine category based on the age
    if 0 <= age <= 2:
        category = "baby"
    elif 3 <= age <= 12:
        category = "child"
    elif 13 <= age <= 14:
        category = "preteen"
    elif 15 <= age <= 18:
        category = "teenager"
    elif 19 <= age <= 20:
        category = "young adult"
    elif 21 <= age <= 59:
        category = "adult"
    elif 60 <= age <= 100:
        category = "senior"
    else:
        category = "This Age out of range, cannot be processed"

    # Output result
    print(f"{first_name} {last_name} is classified as a {category}.")
else:
    print("Invalid age. Please enter a valid number.")


#
#  End of program
#

