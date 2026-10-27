"""Unit tests for SORT WORDS v1.0

Run from the folder that holds sort_words.py:

    python3 -m pytest -v test_sort_words.py

Each test follows the Arrange / Act / Assert structure.
"""

import pytest

from sort_words import ask_words, sort_hyphen_words


# ---------------------------------------------------------------------------
# Strings that should be sorted
# ---------------------------------------------------------------------------

def test_sort_hyphen_words_sorts_the_example_from_the_exercise():
    # Arrange
    input_text = "python-variable-funcion-computadora-monitor"

    # Act
    result = sort_hyphen_words(input_text)

    # Assert
    assert result == "computadora-funcion-monitor-python-variable"


def test_sort_hyphen_words_works_with_two_words():
    # Arrange
    input_text = "zebra-apple"

    # Act
    result = sort_hyphen_words(input_text)

    # Assert
    assert result == "apple-zebra"


def test_sort_hyphen_words_returns_a_single_word_unchanged():
    # Arrange
    input_text = "python"

    # Act
    result = sort_hyphen_words(input_text)

    # Assert
    assert result == "python"


def test_sort_hyphen_words_keeps_an_already_sorted_string():
    # Arrange
    input_text = "alpha-bravo-charlie"

    # Act
    result = sort_hyphen_words(input_text)

    # Assert
    assert result == "alpha-bravo-charlie"


def test_sort_hyphen_words_keeps_repeated_words():
    # Arrange
    input_text = "monitor-python-monitor"

    # Act
    result = sort_hyphen_words(input_text)

    # Assert
    assert result == "monitor-monitor-python"


def test_sort_hyphen_words_ignores_case_but_keeps_the_original_spelling():
    # Arrange
    input_text = "Python-apple-Monitor"

    # Act
    result = sort_hyphen_words(input_text)

    # Assert
    assert result == "apple-Monitor-Python"


def test_sort_hyphen_words_trims_spaces_around_words():
    # Arrange
    input_text = " python - monitor "

    # Act
    result = sort_hyphen_words(input_text)

    # Assert
    assert result == "monitor-python"


# ---------------------------------------------------------------------------
# Inputs that must be rejected
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("bad_text", ["", "python--monitor", "-python", "python-"])
def test_sort_hyphen_words_rejects_empty_words(bad_text):
    # Arrange
    input_text = bad_text

    # Act + Assert
    with pytest.raises(ValueError):
        sort_hyphen_words(input_text)


@pytest.mark.parametrize("not_a_string", [12345, None, ["python", "monitor"], 3.14])
def test_sort_hyphen_words_rejects_input_that_is_not_a_string(not_a_string):
    # Arrange
    bad_input = not_a_string

    # Act + Assert
    with pytest.raises(TypeError):
        sort_hyphen_words(bad_input)


# ---------------------------------------------------------------------------
# ask_words - what the user types
# ---------------------------------------------------------------------------

def test_ask_words_refuses_bad_input_then_accepts_valid_words(monkeypatch):
    # Arrange - pretend the user types nothing, then "a--b", then valid words
    typed = iter(["", "a--b", "python-monitor"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(typed))

    # Act
    result = ask_words()

    # Assert
    assert result == "python-monitor"
