"""LETTER CASE - Counts uppercase and lowercase letters - Version 1.0

Developed by Greg Tovar

Example:  "I love Nación Sushi"
      ->  "There are 3 uppercase letters and 13 lowercase letters."

Accented letters (á, é, ó, ñ, Ñ ...) count as letters too. Spaces, digits
and symbols are not letters, so they are not counted.
"""


# Raises TypeError when the input is not a string.
def check_is_string(text) -> None:
    if not isinstance(text, str):
        raise TypeError("Expected a string, got " + type(text).__name__ + ".")


# Returns how many uppercase letters the string holds.
def count_uppercase(text: str) -> int:
    check_is_string(text)
    count = 0
    for character in text:
        if character.isupper():
            count = count + 1
    return count


# Returns how many lowercase letters the string holds.
def count_lowercase(text: str) -> int:
    check_is_string(text)
    count = 0
    for character in text:
        if character.islower():
            count = count + 1
    return count


# Builds the result sentence for a string.
def build_message(text: str) -> str:
    upper = count_uppercase(text)
    lower = count_lowercase(text)
    return ("There are " + str(upper) + " uppercase letters and "
            + str(lower) + " lowercase letters.")


# Prints the number of uppercase and lowercase letters in a string.
def print_letter_counts(text: str) -> None:
    print(build_message(text))


# Asks for a string and keeps asking until something is typed.
def ask_text() -> str:
    while True:
        text = input("Type a string: ")
        if text == "":
            print("   Please type at least one character.")
            continue
        return text


# Runs the program.
def main() -> None:
    print("\n=== LETTER CASE ===   Developed by Greg Tovar\n")

    text = ask_text()

    print()
    print_letter_counts(text)
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Closing LETTER CASE.\n")
