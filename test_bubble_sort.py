"""

Unit tests for BUBBLE SORT v1.1

Run from the folder that holds bubble_sort.py:

    pytest -v

Each test follows the Arrange / Act / Assert structure.
"""

import random

import pytest

from bubble_sort import bubble_sort_list


# 1. Small list (fewer than 6 elements)
def test_bubble_sort_list_sorts_small_list():
    # Arrange
    input_list = [42, 7, 999, 1, 15]

    # Act
    result = bubble_sort_list(input_list)

    # Assert
    assert result == [1, 7, 15, 42, 999]


# 2. Big list (500 elements)
def test_bubble_sort_list_sorts_big_list_of_500():
    # Arrange
    random.seed(2026)  # fixed seed so the test is repeatable
    input_list = []
    count = 0
    while count < 500:
        input_list.append(random.randint(1, 999))
        count = count + 1

    # Act
    result = bubble_sort_list(input_list)

    # Assert
    assert len(result) == 500
    assert result == sorted(input_list)


# 3. Empty list
def test_bubble_sort_list_returns_empty_list_for_empty_input():
    # Arrange
    input_list = []

    # Act
    result = bubble_sort_list(input_list)

    # Assert
    assert result == []


# 4. Anything that is not a list must be rejected
@pytest.mark.parametrize("not_a_list", [
    "5, 3, 1",          # a string
    531,                # a number
    None,               # nothing at all
    (5, 3, 1),          # a tuple
    {"a": 5, "b": 3},   # a dictionary
])
def test_bubble_sort_list_raises_type_error_when_input_is_not_a_list(not_a_list):
    # Arrange
    bad_input = not_a_list

    # Act + Assert
    with pytest.raises(TypeError):
        bubble_sort_list(bad_input)
