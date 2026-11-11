"""
Category entity

A Category represents a label that can be attached to a transaction
(e.g. "Meal", "Transportation", "Gift"). Categories are stored in
data/categories.csv and referenced by transactions through their ID.


All are dynamic values based on CSV file, nothing is hardcoded

"""


#
# Class definition
#


#
# Using Classes and Methods as requested
#

class Category:
    """Represents a single financial category."""

    def __init__(self, category_id: int, name: str):
        self.category_id = int(category_id)
        self.name = name.strip()

    def to_row(self) -> dict:
        """Return a dict ready to be written as a CSV row."""
        return {"ID": self.category_id, "Category": self.name}

    @classmethod
    def from_row(cls, row: dict) -> "Category":
        """Build a Category instance from a CSV row (dict of strings)."""
        return cls(category_id=row["ID"], name=row["Category"])

    def __repr__(self) -> str:
        return f"Category(id={self.category_id}, name={self.name!r})"
