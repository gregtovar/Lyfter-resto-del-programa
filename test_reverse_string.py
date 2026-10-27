"""Unit tests for REVERSE STRING v1.0

Run from the folder that holds reverse_string.py:

    python3 -m pytest -v test_reverse_string.py

Each test follows the Arrange / Act / Assert structure.
"""

import pytest

from reverse_string import ask_text, reverse_string


# ---------------------------------------------------------------------------
# reverse_string - strings that should be flipped
# ---------------------------------------------------------------------------

def test_reverse_string_flips_a_simple_word():
    # Arrange
    input_text = "House"

    # Act
    result = reverse_string(input_text)

    # Assert
    assert result == "esuoH"


def test_reverse_string_works_with_the_minimum_of_two_characters():
    # Arrange
    input_text = "ab"

    # Act
    result = reverse_string(input_text)

    # Assert
    assert result == "ba"


def test_reverse_string_works_with_the_maximum_of_100_characters():
    # Arrange
    input_text = "abcdefghij" * 10  # 100 characters

    # Act
    result = reverse_string(input_text)

    # Assert
    assert len(result) == 100
    assert result == "jihgfedcba" * 10


def test_reverse_string_keeps_spaces_numbers_and_symbols():
    # Arrange
    input_text = "Hello World 2026!"

    # Act
    result = reverse_string(input_text)

    # Assert
    assert result == "!6202 dlroW olleH"


def test_reverse_string_keeps_upper_and_lower_case():
    # Arrange
    input_text = "PyTest"

    # Act
    result = reverse_string(input_text)

    # Assert
    assert result == "tseTyP"


def test_reverse_string_returns_the_same_text_for_a_palindrome():
    # Arrange
    input_text = "racecar"

    # Act
    result = reverse_string(input_text)

    # Assert
    assert result == "racecar"


def test_reverse_string_twice_gives_back_the_original():
    # Arrange
    input_text = "Greg Tovar"

    # Act
    result = reverse_string(reverse_string(input_text))

    # Assert
    assert result == input_text


# ---------------------------------------------------------------------------
# reverse_string - inputs that must be rejected
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("bad_length", ["", "a", "x" * 101])
def test_reverse_string_rejects_strings_outside_2_to_100_characters(bad_length):
    # Arrange
    input_text = bad_length

    # Act + Assert
    with pytest.raises(ValueError):
        reverse_string(input_text)


@pytest.mark.parametrize("not_a_string", [12345, None, ["H", "o"], 3.14])
def test_reverse_string_rejects_input_that_is_not_a_string(not_a_string):
    # Arrange
    bad_input = not_a_string

    # Act + Assert
    with pytest.raises(TypeError):
        reverse_string(bad_input)


# ---------------------------------------------------------------------------
# ask_text - the 2 to 100 rule for what the user types
# ---------------------------------------------------------------------------

def test_ask_text_refuses_too_short_then_accepts_a_valid_string(monkeypatch):
    # Arrange - pretend the user types nothing, then "H", then "House"
    typed = iter(["", "H", "House"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(typed))

    # Act
    result = ask_text()

    # Assert
    assert result == "House"


def test_ask_text_refuses_too_long_then_accepts_a_valid_string(monkeypatch):
    # Arrange - pretend the user types 101 characters, then "Hi"
    typed = iter(["x" * 101, "Hi"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(typed))

    # Act
    result = ask_text()

    # Assert
    assert result == "Hi"
