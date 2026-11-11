#
#
# Transaction entity 
#
#


"""

A Transaction represents a single financial movement (income, expense or
adjustment). Amounts are stored using Decimal to avoid floating-point
rounding errors when dealing with money.

Make it MODULAR
"""


#
#
# Import
#
#

from decimal import Decimal


class Transaction:
    """Represents a single financial transaction."""

    def __init__(self, transaction_id: int, timestamp: str, category_id: int,
                 amount: Decimal, type_id: int):
        self.transaction_id = int(transaction_id)
        self.timestamp = timestamp
        self.category_id = int(category_id)
        self.amount = Decimal(amount).quantize(Decimal("0.01"))
        self.type_id = int(type_id)

    def to_row(self) -> dict:
        """Return a dict ready to be written as a CSV row."""
        return {
            "ID": self.transaction_id,
            "TimeStamp": self.timestamp,
            "Category": self.category_id,
            "Amount": f"{self.amount:.2f}",
            "Type": self.type_id,
        }

    @classmethod
    def from_row(cls, row: dict) -> "Transaction":
        """Build a Transaction instance from a CSV row (dict of strings)."""
        return cls(
            transaction_id=row["ID"],
            timestamp=row["TimeStamp"],
            category_id=row["Category"],
            amount=row["Amount"],
            type_id=row["Type"],
        )

    def __repr__(self) -> str:
        return (f"Transaction(id={self.transaction_id}, timestamp={self.timestamp!r}, "
                f"category={self.category_id}, amount={self.amount}, type={self.type_id})")
