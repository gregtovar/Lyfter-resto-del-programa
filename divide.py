"""DIVIDE - Divides two numbers - Version 1.0

Developed by Greg Tovar

OCT 28 2026

"""

#
#
# Returns number1 divided by number2.
#
# Raises ValueError when number2 is zero.
# Raises TypeError  (from Python itself) when either argument is a string.
def divide(number1, number2):
    if number2 == 0:
        raise ValueError("division by zero is not possible")
    return number1 / number2


#
# End
#
