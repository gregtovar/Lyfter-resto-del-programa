"""Unit tests for LETTER CASE v1.0

Run from the folder that holds letter_case.py:

    python3 -m pytest -v test_letter_case.py

Each test follows the Arrange / Act / Assert structure.
"""

import pytest

from letter_case import (ask_text, build_message, count_lowercase,
                         count_uppercase, print_letter_counts)


# ---------------------------------------------------------------------------
# The example from the exercise
# ---------------------------------------------------------------------------

def test_print_letter_counts_prints_the_expected_sentence(capsys):
    # Arrange
    input_text = "I love Nación Sushi"

    # Act
    print_letter_counts(input_text)
    printed = capsys.readouterr().out

    # Assert
    assert printed == "There are 3 uppercase letters and 13 lowercase letters.\n"


def test_build_message_returns_the_expected_sentence():
    # Arrange
    input_text = "I love Nación Sushi"

    # Act
    result = build_message(input_text)

    # Assert
    assert result == "There are 3 uppercase letters and 13 lowercase letters."


# ---------------------------------------------------------------------------
# count_uppercase / count_lowercase
# ---------------------------------------------------------------------------

def test_count_uppercase_counts_only_capital_letters():
    # Arrange
    input_text = "I love Nación Sushi"

    # Act
    result = count_uppercase(input_text)

    # Assert
    assert result == 3


def test_count_lowercase_counts_accented_letters():
    # Arrange - the ó in Nación must be counted
    input_text = "ación"

    # Act
    result = count_lowercase(input_text)

    # Assert
    assert result == 5


def test_counts_include_accented_capitals():
    # Arrange
    input_text = "ÑANDÚ"

    # Act
    upper = count_uppercase(input_text)
    lower = count_lowercase(input_text)

    # Assert
    assert upper == 5
    assert lower == 0


def test_spaces_digits_and_symbols_are_not_counted():
    # Arrange
    input_text = "123 !@# $%^ 456"

    # Act
    result = build_message(input_text)

    # Assert
    assert result == "There are 0 uppercase letters and 0 lowercase letters."


def test_all_uppercase_string():
    # Arrange
    input_text = "HELLO WORLD"

    # Act
    result = build_message(input_text)

    # Assert
    assert result == "There are 10 uppercase letters and 0 lowercase letters."


def test_all_lowercase_string():
    # Arrange
    input_text = "hello world"

    # Act
    result = build_message(input_text)

    # Assert
    assert result == "There are 0 uppercase letters and 10 lowercase letters."


def test_empty_string_gives_zero_and_zero():
    # Arrange
    input_text = ""

    # Act
    result = build_message(input_text)

    # Assert
    assert result == "There are 0 uppercase letters and 0 lowercase letters."


# ---------------------------------------------------------------------------
# Inputs that must be rejected
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("not_a_string", [12345, None, ["A", "b"], 3.14])
def test_print_letter_counts_rejects_input_that_is_not_a_string(not_a_string):
    # Arrange
    bad_input = not_a_string

    # Act + Assert
    with pytest.raises(TypeError):
        print_letter_counts(bad_input)


# ---------------------------------------------------------------------------
# ask_text - what the user types
# ---------------------------------------------------------------------------

def test_ask_text_refuses_empty_then_accepts_a_string(monkeypatch):
    # Arrange - pretend the user presses ENTER, then types a sentence
    typed = iter(["", "I love Nación Sushi"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(typed))

    # Act
    result = ask_text()

    # Assert
    assert result == "I love Nación Sushi"
