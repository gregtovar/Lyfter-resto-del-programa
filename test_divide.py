"""

Unit tests for DIVIDE v1.0

DO NOT RUN from Visual Sudio Code!!! - Run from Terminal in MAC OS

Run from the folder that holds divide.py:

    python3 -m pytest -v test_divide.py

Each test follows the Arrange / Act / Assert structure.

Greg Tovar - OCT 28 2026
"""


#
# Import
#

import pytest

from divide import divide


#
# Class
#


class TestDivide:

    # 1. divide(10, 2) returns 5.0
    def test_divide_10_by_2_returns_5_point_0(self):
        # Arrange
        number1 = 10
        number2 = 2

        # Act
        result = divide(number1, number2)

        # Assert
        assert result == 5.0
        assert isinstance(result, float)  # "/" always gives a float in Python 3



    # 2. Dividing by zero raises ValueError
    def test_divide_by_zero_raises_value_error(self):
        # Arrange
        number1 = 10
        number2 = 0

        # Act + Assert - match= also checks the error message
        with pytest.raises(ValueError, match="division by zero is not possible"):
            divide(number1, number2)

    # 3. Passing a string raises TypeError - in either position
    @pytest.mark.parametrize("number1, number2", [
        ("10", 2),    # string as the first argument
        (10, "2"),    # string as the second argument
    ])
    def test_divide_with_a_string_raises_type_error(self, number1, number2):
        # Arrange - the values come from parametrize above

        # Act + Assert
        with pytest.raises(TypeError):
            divide(number1, number2)


#
#
# End
#
#
