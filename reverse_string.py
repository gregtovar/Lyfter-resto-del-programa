"""REVERSE STRING - Flips a string back to front - Version 1.0

Developed by Greg Tovar

Example:  "House"  ->  "esuoH"
"""

# Limits for the length of the string the user can type.
MIN_LENGTH = 2
MAX_LENGTH = 100


# Returns the string flipped back to front.
#
# Takes one parameter (the string) and returns a new string.
# A plain loop is used instead of the text[::-1] shortcut so the work is
# visible: it walks from the last character down to the first.
#
# Raises TypeError  when the input is not a string.
# Raises ValueError when the string is shorter than MIN_LENGTH or longer
#                   than MAX_LENGTH characters.
def reverse_string(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("reverse_string expects a string, got "
                        + type(text).__name__ + ".")

    if len(text) < MIN_LENGTH or len(text) > MAX_LENGTH:
        raise ValueError("The string must be " + str(MIN_LENGTH) + " to "
                         + str(MAX_LENGTH) + " characters, got "
                         + str(len(text)) + ".")

    flipped = ""
    index = len(text) - 1
    while index >= 0:
        flipped = flipped + text[index]
        index = index - 1
    return flipped


# Asks for a string and keeps asking until it is between MIN_LENGTH and
# MAX_LENGTH characters long. Spaces count as characters.
def ask_text() -> str:
    while True:
        text = input("Type a string (" + str(MIN_LENGTH) + " to "
                     + str(MAX_LENGTH) + " characters): ")

        if len(text) < MIN_LENGTH:
            print("   Too short - you typed " + str(len(text))
                  + " character(s), the minimum is " + str(MIN_LENGTH) + ".")
            continue

        if len(text) > MAX_LENGTH:
            print("   Too long - you typed " + str(len(text))
                  + " characters, the maximum is " + str(MAX_LENGTH) + ".")
            continue

        return text


# Runs the program.
def main() -> None:
    print("\n=== REVERSE STRING ===   Developed by Greg Tovar\n")

    text = ask_text()
    flipped = reverse_string(text)

    print("\nOriginal: \"" + text + "\"")
    print("Flipped:  \"" + flipped + "\"\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Closing REVERSE STRING.\n")
