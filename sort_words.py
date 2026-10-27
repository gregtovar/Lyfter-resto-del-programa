"""SORT WORDS - Sorts hyphen separated words alphabetically - Version 1.0

Developed by Greg Tovar

Example:  "python-variable-funcion-computadora-monitor"
      ->  "computadora-funcion-monitor-python-variable"
"""

SEPARATOR = "-"


# Accepts a string of words separated by hyphens and returns a string with
# the words sorted alphabetically.
#
#   1. Convert the string to a list   (split on the hyphen)
#   2. Sort the list                  (A-Z, ignoring upper/lower case)
#   3. Convert it back to a string    (join with the hyphen)
#
# Raises TypeError  when the input is not a string.
# Raises ValueError when the string is empty or has an empty word, for
#                   example "python--monitor" or "python-".
def sort_hyphen_words(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("sort_hyphen_words expects a string, got "
                        + type(text).__name__ + ".")

    # 1. String -> list
    words = text.split(SEPARATOR)

    # Spaces around a word are trimmed, then empty words are refused.
    clean_words = []
    for word in words:
        word = word.strip()
        if word == "":
            raise ValueError("Empty word found - check for a missing word "
                             "or a double / leading / trailing hyphen.")
        clean_words.append(word)

    # 2. Sort the list. key=str.lower makes "Python" and "python" sort the
    #    same, otherwise every capital word would come before any lowercase.
    clean_words.sort(key=str.lower)

    # 3. List -> string
    return SEPARATOR.join(clean_words)


# Asks for the words and keeps asking until they can be sorted.
def ask_words() -> str:
    while True:
        text = input("Type words separated by hyphens (e.g. python-monitor): ")
        try:
            sort_hyphen_words(text)
        except ValueError as problem:
            print("   " + str(problem))
            continue
        return text


# Runs the program.
def main() -> None:
    print("\n=== SORT WORDS ===   Developed by Greg Tovar\n")

    text = ask_words()
    result = sort_hyphen_words(text)

    print("\nOriginal: " + text)
    print("Sorted:   " + result + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Closing SORT WORDS.\n")
