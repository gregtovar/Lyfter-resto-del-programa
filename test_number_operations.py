"""

Unit tests for NUMBER OPERATIONS v1.0

WARINING!!!!   DO NOT RUN IT in Visual Studio!!!!!!

in MAC, go to TERMINAL then Run from the folder that holds number_operations.py:

    python3 -m pytest -v test_number_operations.py

All the tests live in one test class. pytest finds the class because its
name starts with "Test", and runs every method whose name starts with
"test_". Each test follows the Arrange / Act / Assert structure.
"""

#
# These imports are key!
#
#

import pytest

from number_operations import add_numbers, average_numbers, celsius_to_fahrenheit

#
#class definition 
#

class TestNumberOperations:

    # -----------------------------------------------------------------
    # 1. ADDITION
    # -----------------------------------------------------------------

    def test_add_numbers_with_positive_numbers(self):
        # Arrange
        first = 5
        second = 3

        # Act
        result = add_numbers(first, second)

        # Assert
        assert result == 8

    def test_add_numbers_with_negative_numbers(self):
        # Arrange
        first = -5
        second = -3

        # Act
        result = add_numbers(first, second)

        # Assert
        assert result == -8

    def test_add_numbers_with_zeros(self):
        # Arrange
        first = 0
        second = 0

        # Act
        result = add_numbers(first, second)

        # Assert
        assert result == 0

    # -----------------------------------------------------------------
    # 2. AVERAGING
    # -----------------------------------------------------------------

    def test_average_numbers_with_positive_numbers(self):
        # Arrange
        numbers = [2, 4, 6, 8]

        # Act
        result = average_numbers(numbers)

        # Assert
        assert result == 5

    def test_average_numbers_with_negative_numbers(self):
        # Arrange
        numbers = [-2, -4, -6, -8]

        # Act
        result = average_numbers(numbers)

        # Assert
        assert result == -5

    def test_average_numbers_with_zeros(self):
        # Arrange
        numbers = [0, 0, 0, 0]

        # Act
        result = average_numbers(numbers)

        # Assert
        assert result == 0

    # -----------------------------------------------------------------
    # 3. CONVERSION (Celsius -> Fahrenheit)
    # -----------------------------------------------------------------

    def test_celsius_to_fahrenheit_with_a_positive_number(self):
        # Arrange - water boils at 100 C
        celsius = 100

        # Act
        result = celsius_to_fahrenheit(celsius)

        # Assert
        assert result == 212

    def test_celsius_to_fahrenheit_with_a_negative_number(self):
        # Arrange - -40 is the point where both scales read the same
        celsius = -40

        # Act
        result = celsius_to_fahrenheit(celsius)

        # Assert
        assert result == -40

    def test_celsius_to_fahrenheit_with_zero(self):
        # Arrange - water freezes at 0 C
        celsius = 0

        # Act
        result = celsius_to_fahrenheit(celsius)

        # Assert
        assert result == 32

    # -----------------------------------------------------------------
    # Extra: inputs that must be rejected
    # -----------------------------------------------------------------

    def test_add_numbers_rejects_text(self):
        # Arrange
        first = "5"
        second = 3

        # Act + Assert
        with pytest.raises(TypeError):
            add_numbers(first, second)

    def test_average_numbers_rejects_an_empty_list(self):
        # Arrange
        numbers = []

        # Act + Assert
        with pytest.raises(ValueError):
            average_numbers(numbers)

    def test_celsius_to_fahrenheit_rejects_none(self):
        # Arrange
        celsius = None

        # Act + Assert
        with pytest.raises(TypeError):
            celsius_to_fahrenheit(celsius)
