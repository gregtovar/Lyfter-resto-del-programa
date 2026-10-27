"""Unit tests for PRIME FILTER v1.0

Run from the folder that holds prime_filter.py:

    python3 -m pytest -v test_prime_filter.py

Each test follows the Arrange / Act / Assert structure.
"""

import pytest

from prime_filter import ask_numbers, filter_primes, is_prime, parse_numbers


# ---------------------------------------------------------------------------
# filter_primes - lists that should be filtered
# ---------------------------------------------------------------------------

def test_filter_primes_returns_primes_from_the_example():
    # Arrange
    input_list = [1, 4, 6, 7, 13, 9, 67]

    # Act
    result = filter_primes(input_list)

    # Assert
    assert result == [7, 13, 67]


def test_filter_primes_keeps_every_number_when_all_are_prime():
    # Arrange
    input_list = [2, 3, 5, 7, 11]

    # Act
    result = filter_primes(input_list)

    # Assert
    assert result == [2, 3, 5, 7, 11]


def test_filter_primes_returns_empty_list_when_none_are_prime():
    # Arrange
    input_list = [1, 4, 6, 8, 9, 10]

    # Act
    result = filter_primes(input_list)

    # Assert
    assert result == []


def test_filter_primes_returns_empty_list_for_empty_input():
    # Arrange
    input_list = []

    # Act
    result = filter_primes(input_list)

    # Assert
    assert result == []


def test_filter_primes_drops_zero_one_and_negative_numbers():
    # Arrange
    input_list = [-7, -2, 0, 1, 2]

    # Act
    result = filter_primes(input_list)

    # Assert
    assert result == [2]


def test_filter_primes_keeps_order_and_duplicates():
    # Arrange
    input_list = [13, 4, 7, 13, 2]

    # Act
    result = filter_primes(input_list)

    # Assert
    assert result == [13, 7, 13, 2]


def test_filter_primes_does_not_change_the_original_list():
    # Arrange
    input_list = [1, 4, 7]

    # Act
    filter_primes(input_list)

    # Assert
    assert input_list == [1, 4, 7]


def test_filter_primes_works_with_large_numbers():
    # Arrange - 7919 is the 1000th prime, 7917 = 3 * 7 * 13 * 29
    input_list = [7917, 7919]

    # Act
    result = filter_primes(input_list)

    # Assert
    assert result == [7919]


# ---------------------------------------------------------------------------
# is_prime - the rule itself
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("prime", [2, 3, 5, 7, 11, 13, 67, 97])
def test_is_prime_returns_true_for_primes(prime):
    # Arrange
    number = prime

    # Act
    result = is_prime(number)

    # Assert
    assert result is True


@pytest.mark.parametrize("not_prime", [-5, 0, 1, 4, 9, 25, 49, 100])
def test_is_prime_returns_false_for_non_primes(not_prime):
    # Arrange
    number = not_prime

    # Act
    result = is_prime(number)

    # Assert
    assert result is False


# ---------------------------------------------------------------------------
# filter_primes - inputs that must be rejected
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("not_a_list", ["1, 4, 7", 7, None, (1, 4, 7)])
def test_filter_primes_rejects_input_that_is_not_a_list(not_a_list):
    # Arrange
    bad_input = not_a_list

    # Act + Assert
    with pytest.raises(TypeError):
        filter_primes(bad_input)


@pytest.mark.parametrize("bad_list", [[1, "7", 13], [7.5, 13], [True, 7], [None]])
def test_filter_primes_rejects_lists_with_non_whole_numbers(bad_list):
    # Arrange
    input_list = bad_list

    # Act + Assert
    with pytest.raises(TypeError):
        filter_primes(input_list)


# ---------------------------------------------------------------------------
# parse_numbers / ask_numbers - what the user types
# ---------------------------------------------------------------------------

def test_parse_numbers_turns_typed_text_into_a_list():
    # Arrange
    typed_text = "1, 4, 6, 7, 13, 9, 67"

    # Act
    result = parse_numbers(typed_text)

    # Assert
    assert result == [1, 4, 6, 7, 13, 9, 67]


@pytest.mark.parametrize("bad_text", ["", "1, , 7", "1, abc, 7", "1, 7,"])
def test_parse_numbers_rejects_bad_text(bad_text):
    # Arrange
    typed_text = bad_text

    # Act + Assert
    with pytest.raises(ValueError):
        parse_numbers(typed_text)


def test_ask_numbers_refuses_bad_input_then_accepts_valid_numbers(monkeypatch):
    # Arrange - pretend the user types "abc", then "1,,7", then valid numbers
    typed = iter(["abc", "1,,7", "1, 4, 7"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(typed))

    # Act
    result = ask_numbers()

    # Assert
    assert result == [1, 4, 7]
