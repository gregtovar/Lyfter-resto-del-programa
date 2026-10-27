"""Unit tests for SUM LIST v1.0

Run from the folder that holds sum_list.py:

    python3 -m pytest -v test_sum_list.py

Each test follows the Arrange / Act / Assert structure.
"""

import pytest

from sum_list import ask_element_count, sum_list_elements


# ---------------------------------------------------------------------------
# sum_list_elements - lists that should work
# ---------------------------------------------------------------------------

def test_sum_list_elements_returns_result_with_small_numbers():
    # Arrange
    input_list = [5, 6, 7, 8, 2, 4, 5, 9]

    # Act
    result = sum_list_elements(input_list)

    # Assert
    assert result == 46


def test_sum_list_elements_returns_result_with_big_numbers():
    # Arrange
    input_list = [500, 700, 800]

    # Act
    result = sum_list_elements(input_list)

    # Assert
    assert result == 2000


def test_sum_list_elements_works_with_the_minimum_of_two_elements():
    # Arrange
    input_list = [10, 15]

    # Act
    result = sum_list_elements(input_list)

    # Assert
    assert result == 25


def test_sum_list_elements_works_with_negative_numbers():
    # Arrange
    input_list = [10, -4, -6, 3]

    # Act
    result = sum_list_elements(input_list)

    # Assert
    assert result == 3


def test_sum_list_elements_works_with_decimals():
    # Arrange
    input_list = [1.5, 2.25, 0.25]

    # Act
    result = sum_list_elements(input_list)

    # Assert
    assert result == pytest.approx(4.0)  # approx avoids float rounding noise


def test_sum_list_elements_works_with_a_big_list_of_500():
    # Arrange
    input_list = list(range(1, 501))  # 1, 2, 3 ... 500

    # Act
    result = sum_list_elements(input_list)

    # Assert
    assert result == 125250  # 500 * 501 / 2


def test_sum_list_elements_does_not_change_the_original_list():
    # Arrange
    input_list = [3, 1, 2]

    # Act
    sum_list_elements(input_list)

    # Assert
    assert input_list == [3, 1, 2]


# ---------------------------------------------------------------------------
# sum_list_elements - inputs that must be rejected
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("too_short", [[], [7]])
def test_sum_list_elements_rejects_lists_with_zero_or_one_element(too_short):
    # Arrange
    input_list = too_short

    # Act + Assert
    with pytest.raises(ValueError):
        sum_list_elements(input_list)


@pytest.mark.parametrize("not_a_list", ["5, 3, 1", 531, None, (5, 3, 1)])
def test_sum_list_elements_rejects_input_that_is_not_a_list(not_a_list):
    # Arrange
    bad_input = not_a_list

    # Act + Assert
    with pytest.raises(TypeError):
        sum_list_elements(bad_input)


@pytest.mark.parametrize("bad_list", [[1, "2", 3], [1, None], [True, 4]])
def test_sum_list_elements_rejects_lists_with_non_numbers(bad_list):
    # Arrange
    input_list = bad_list

    # Act + Assert
    with pytest.raises(TypeError):
        sum_list_elements(input_list)


# ---------------------------------------------------------------------------
# ask_element_count - the "at least 2" rule for what the user types
# ---------------------------------------------------------------------------

def test_ask_element_count_refuses_zero_and_one_then_accepts_three(monkeypatch):
    # Arrange - pretend the user types 0, then 1, then 3
    typed = iter(["0", "1", "3"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(typed))

    # Act
    result = ask_element_count()

    # Assert
    assert result == 3


def test_ask_element_count_refuses_text_and_negatives(monkeypatch):
    # Arrange - pretend the user types abc, then -5, then 2
    typed = iter(["abc", "-5", "2"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(typed))

    # Act
    result = ask_element_count()

    # Assert
    assert result == 2
