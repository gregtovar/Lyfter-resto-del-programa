"""

NUMBER OPERATIONS - Small operations on numbers - Version 1.0

Developed by Greg Tovar - OCT 28 2026

  1. add_numbers            - adds two numbers
  2. average_numbers        - averages a list of numbers
  3. celsius_to_fahrenheit  - converts a temperature
"""


#
# 
# Raises TypeError when the value is not a number.
# True/False are technically numbers in Python, but not here.
#
#

def check_is_number(value) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("'" + str(value) + "' is not a number.")


# 1. ADDITION - returns the sum of two numbers.
def add_numbers(first, second):
    check_is_number(first)
    check_is_number(second)
    return first + second

#
#
# 2. AVERAGING - returns the average of a list of numbers.
#
# Raises TypeError  when the input is not a list or holds a non number.
# Raises ValueError when the list is empty (there is nothing to average).
#
#

def average_numbers(numbers: list) -> float:
    if not isinstance(numbers, list):
        raise TypeError("average_numbers expects a list, got "
                        + type(numbers).__name__ + ".")

    if len(numbers) == 0:
        raise ValueError("Cannot average an empty list.")

    total = 0
    for number in numbers:
        check_is_number(number)
        total = total + number

    return total / len(numbers)


#
# #
# # 3. CONVERSION - converts degrees Celsius to degrees Fahrenheit.
#
#   F = C * 9 / 5 + 32   Formula
#

def celsius_to_fahrenheit(celsius):
    check_is_number(celsius)
    return celsius * 9 / 5 + 32
