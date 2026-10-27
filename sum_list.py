"""SUM LIST - Adds up all the numbers in a list - Version 1.0

Developed by Greg Tovar
"""

# The list must have at least this many elements.
MIN_ELEMENTS = 2


# Returns the sum of all the numbers in the list.
#
# Takes one parameter (the list) and returns one number (the total).
# A plain loop is used instead of the built-in sum() so the work is visible.
#
# Raises TypeError  when the input is not a list, or holds something that
#                   is not a number.
# Raises ValueError when the list has fewer than MIN_ELEMENTS elements.
def sum_list_elements(numbers: list):
    if not isinstance(numbers, list):
        raise TypeError("sum_list_elements expects a list, got "
                        + type(numbers).__name__ + ".")

    if len(numbers) < MIN_ELEMENTS:
        raise ValueError("The list needs at least " + str(MIN_ELEMENTS)
                         + " elements, got " + str(len(numbers)) + ".")

    total = 0
    for number in numbers:
        # True/False are technically numbers in Python, but not here.
        if isinstance(number, bool) or not isinstance(number, (int, float)):
            raise TypeError("'" + str(number) + "' is not a number.")
        total = total + number
    return total


# Asks how many elements the list should have, refusing 0, 1 or anything
# that is not a whole number.
def ask_element_count() -> int:
    while True:
        value = input("How many elements do you want? (at least "
                      + str(MIN_ELEMENTS) + "): ").strip()

        # A leading sign is allowed so a negative answer gets the range
        # message rather than the "not a whole number" message.
        body = value
        if body != "" and (body[0] == "-" or body[0] == "+"):
            body = body[1:]

        if not body.isdigit():
            print("   '" + value + "' is not a whole number. Try again.")
            continue

        count = int(value)
        if count < MIN_ELEMENTS:
            print("   The list needs at least " + str(MIN_ELEMENTS)
                  + " elements. Zero and one are not accepted.")
            continue

        return count


# Asks for one number. Whole numbers stay whole, decimals are accepted too.
def ask_number(position: int):
    while True:
        value = input("   Element " + str(position) + ": ").strip()

        try:
            return int(value)
        except ValueError:
            pass

        try:
            return float(value)
        except ValueError:
            print("   '" + value + "' is not a number. Try again.")


# Builds the list by asking the user for each value.
def build_list(count: int) -> list:
    numbers = []
    position = 1
    while position <= count:
        numbers.append(ask_number(position))
        position = position + 1
    return numbers


# Runs the program.
def main() -> None:
    print("\n=== SUM LIST ===   Developed by Greg Tovar\n")

    count = ask_element_count()

    print("\nEnter the " + str(count) + " numbers:")
    numbers = build_list(count)

    total = sum_list_elements(numbers)

    print("\nList: " + str(numbers))
    print("Sum:  " + str(total) + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Closing SUM LIST.\n")
