#
#  First, ask how many grades will be entered
#
n_input = input("How many grades will you enter? ")

#
#  Validate n - making sure the number is valid
#
if not n_input.isdigit() or int(n_input) <= 0:
    print("Invalid number of grades.")
else:
    n = int(n_input)

    grades = []
    
    #
    #  Collect grades with validation
    #
    for i in range(n):
        while True:
            grade_input = input(f"Enter grade #{i+1} (0-100): ")
            
            try:
                grade = float(grade_input)
                
                if 0 <= grade <= 100:
                    grades.append(grade)
                    break
                else:
                    print("Error: Grade must be between 0 and 100!!!.")
            except:
                print("Error: Please enter a valid number!.")

    #
    #  
    # Initialize variables to support the calculation
    #
    passing_count = 0
    failing_count = 0
    passing_sum = 0
    failing_sum = 0
    #
    # Process grades
    #
    for grade in grades:
        if grade >= 70:
            passing_count += 1
            passing_sum += grade
        elif grade < 70:
            failing_count += 1
            failing_sum += grade
   


    # Calculate averages
    total_average = sum(grades) / len(grades)

    passing_average = passing_sum / passing_count if passing_count > 0 else 0
    failing_average = failing_sum / failing_count if failing_count > 0 else 0

    # Display results
    print("\n--- Results ---")
    print(f"Total grades entered: {n}")
    print(f"Passing grades (>70): {passing_count}")
    print(f"Failing grades (<70): {failing_count}")
    print(f"Average of all grades: {total_average:.2f}")
    print(f"Average of passing grades: {passing_average:.2f}")
    print(f"Average of failing grades: {failing_average:.2f}")

    #
    # End of program
    #
