"""
user_age_decorator.py

Defines a User class with a date_of_birth attribute and an age
property, plus a decorator that checks any User passed to a function
is at least 18 years old.
"""


import functools
from datetime import date


#
#   A simple user with a date of birth and a computed age
#

class User:

    def __init__(self, name, date_of_birth):
        self.name = name
        self.date_of_birth = date_of_birth

    @property
    def age(self):
        today = date.today()
        years = today.year - self.date_of_birth.year  # Subtract a year if the birthday hasn't happened yet this year
        had_birthday_this_year = (today.month, today.day) >= (
            self.date_of_birth.month,
            self.date_of_birth.day,
        )
        if not had_birthday_this_year:
            years -= 1
        return years

    def __repr__(self):
        return f"User(name={self.name!r}, date_of_birth={self.date_of_birth!r})"


#
# Check every User argument passed to func; raise a PermissionError
# if any of them is under 18 years old.
#


def require_adult(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        candidates = list(args) + list(kwargs.values())
        for value in candidates:
            if isinstance(value, User) and value.age < 18:
                raise PermissionError(
                    f"Access denied: {value.name} is {value.age} years old "
                    f"and must be at least 18."
                )
        return func(*args, **kwargs)

    return wrapper


@require_adult
def open_account(user):
    return f"Account created for {user.name}."



#
# Main program
#

if __name__ == "__main__":
    adult = User("Greg", date(1990, 5, 20))      # Hardcoded Values for Demo Purposes
    minor = User("Sam", date(2015, 1, 1))        # Hardcoded Values for Demo Purposes

    print(open_account(adult))

    try:
        open_account(minor)
    except PermissionError as e:       # Exception Management
        print(f"Error: {e}")


#
# End of Main program
#