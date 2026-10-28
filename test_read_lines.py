"""Unit tests for READ LINES v1.0

DO NOT RUN from Visual Studio!! Run on the Terminal Mac OS


Run from the folder that holds read_lines.py:

    python3 -m pytest -v test_read_lines.py

No real files are created or read: unittest.mock replaces Python's
built-in open() with a fake one for the length of each test.

Each test follows the Arrange / Act / Assert structure.


"""


#
# Import
#

from unittest.mock import mock_open, patch

import pytest

from read_lines import read_lines


#
# Class
#


class TestReadLines:

    # 1. Returns the expected lines from a simulated file
    def test_read_lines_returns_the_lines_of_a_simulated_file(self):
        # Arrange - fake file contents, three lines
        fake_contents = "line one\nline two\nline three\n"
        fake_open = mock_open(read_data=fake_contents)

        # Act - while inside "with patch", every open() call uses fake_open
        with patch("builtins.open", fake_open):
            result = read_lines("fake_file.txt")

        # Assert
        assert result == ["line one\n", "line two\n", "line three\n"]

#
#
    # 2. Proves the function opened the right file, in read mode, and that
    #    the real open() was never used
#
#
#


    def test_read_lines_opens_the_given_path_in_read_mode(self):
        # Arrange
        fake_open = mock_open(read_data="hello\n")

        # Act
        with patch("builtins.open", fake_open):
            read_lines("reports/inventory.txt")

        # Assert
        fake_open.assert_called_once_with("reports/inventory.txt", "r")


#
#
#

    # 3. A simulated empty file returns an empty list
    #
#
#

    def test_read_lines_returns_empty_list_for_an_empty_file(self):
        # Arrange
        fake_open = mock_open(read_data="")

        # Act
        with patch("builtins.open", fake_open):
            result = read_lines("empty.txt")

        # Assert
        assert result == []

#
#
#

    # 4. Raises FileNotFoundError when the file does not exist
    #
#
#



    def test_read_lines_raises_file_not_found_error_for_a_missing_file(self):
        # Arrange - make the fake open() fail the same way the real one does
        fake_open = mock_open()
        fake_open.side_effect = FileNotFoundError("No such file: missing.txt")

        # Act + Assert
        with patch("builtins.open", fake_open):
            with pytest.raises(FileNotFoundError):
                read_lines("missing.txt")

#
#
#
# End
#
#
