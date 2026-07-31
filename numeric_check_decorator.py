"""
numeric_check_decorator.py

A decorator that checks whether all arguments passed to a function
are numeric (int or float). If any argument isn't a number, it raises
a TypeError with a clear message for the user.

This is an exercise to practice it.

"""


import functools
#
# It's not strictly required to uise "functools" for the script to run
# but is way cooler and more elegant
#


def numeric_only(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for value in list(args) + list(kwargs.values()):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(
                    f"Invalid argument: {value!r} is not a number. "
                    f"All arguments to '{func.__name__}' must be int or float."
                )
        return func(*args, **kwargs)

    return wrapper


@numeric_only
def add(a, b):
    return a + b



#
# Try to convert user input into an int or float; if it can't be
# converted, just return the raw string so numeric_only can catch it.
#

def to_number(text):

    try:
        return int(text)
    except ValueError:
        try:
            return float(text)
        except ValueError:
            return text

#
# Main Program
#

if __name__ == "__main__":
    first = to_number(input("Enter the first parameter: "))
    second = to_number(input("Enter the second parameter: "))

    try:
        print(add(first, second))
    except TypeError as e:
        print(f"Error: {e}")

#
# End Main Program
#
