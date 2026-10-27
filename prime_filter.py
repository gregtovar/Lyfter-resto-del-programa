"""PRIME FILTER - Keeps only the prime numbers of a list - Version 1.0

Developed by Greg Tovar

Example:  [1, 4, 6, 7, 13, 9, 67]  ->  [7, 13, 67]

A prime number is a whole number greater than 1 that can only be divided
evenly by 1 and by itself. So 0, 1 and negative numbers are never prime.
"""


# Returns True when the number is prime.
#
# Only divisors up to the square root need checking: if n = a * b, one of
# a or b is always <= the square root of n. 'divisor * divisor <= number'
# is that check without needing the math library.
def is_prime(number: int) -> bool:
    if number < 2:
        return False

    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor = divisor + 1

    return True


# Accepts a list of numbers and returns a NEW list containing only the
# prime numbers, in the same order they appeared. The list passed in is
# left untouched.
#
# Raises TypeError when the input is not a list, or holds something that
#                  is not a whole number.
def filter_primes(numbers: list) -> list:
    if not isinstance(numbers, list):
        raise TypeError("filter_primes expects a list, got "
                        + type(numbers).__name__ + ".")

    primes = []
    for number in numbers:
        # True/False are technically whole numbers in Python, but not here.
        if isinstance(number, bool) or not isinstance(number, int):
            raise TypeError("'" + str(number) + "' is not a whole number.")

        if is_prime(number):
            primes.append(number)

    return primes


# Turns "1, 4, 6, 7" into [1, 4, 6, 7].
#
# Raises ValueError when something typed is not a whole number.
def parse_numbers(text: str) -> list:
    numbers = []
    for piece in text.split(","):
        piece = piece.strip()
        if piece == "":
            raise ValueError("Empty value found - check for a missing number "
                             "or an extra comma.")
        try:
            numbers.append(int(piece))
        except ValueError:
            raise ValueError("'" + piece + "' is not a whole number.")
    return numbers


# Asks for the numbers and keeps asking until they are all whole numbers.
def ask_numbers() -> list:
    while True:
        text = input("Type whole numbers separated by commas "
                     "(e.g. 1, 4, 7, 13): ")
        try:
            return parse_numbers(text)
        except ValueError as problem:
            print("   " + str(problem))


# Runs the program.
def main() -> None:
    print("\n=== PRIME FILTER ===   Developed by Greg Tovar\n")

    numbers = ask_numbers()
    primes = filter_primes(numbers)

    print("\nList:   " + str(numbers))
    print("Primes: " + str(primes))
    if len(primes) == 0:
        print("        (none of these numbers are prime)")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Closing PRIME FILTER.\n")
