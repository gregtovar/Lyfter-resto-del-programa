"""
trace_decorator.py

A simple decorator that prints the arguments passed to a function and
its return value, shown in green text. 

The idea of this App is understand the usage of decorators

"""



import functools

#
# It's not strictly required to uise "functools" for the script to run
# but is way cooler and more elegant
#

GREEN = "\033[32m"
RESET = "\033[0m"

# 
#  Print a function's arguments and its return value.
#

def trace(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"{GREEN}Calling {func.__name__} with args={args}, kwargs={kwargs}{RESET}")
        result = func(*args, **kwargs)
        print(f"{GREEN}{func.__name__} returned: {result}{RESET}")
        return result

    return wrapper


@trace # Decorator 
def add(a, b):
    return a + b
# Simple function


#
# MAIN PROGRAM
#

if __name__ == "__main__":
    print(f"{GREEN}=== Trace Decorator Demo ==={RESET}")
    a = int(input(f"{GREEN}Enter first number: {RESET}"))
    b = int(input(f"{GREEN}Enter second number: {RESET}"))
    add(a, b)

#
# END MAIN PROGRAM
#
