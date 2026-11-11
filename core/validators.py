#
#
# VALUDATION
#
# Centralized input validation for the Personal Finance Manager.
#
#





"""
 
Keeping all validation rules in one `Validator` class means the Console UI
and the GUI never need to re-implement (or accidentally duplicate) a
business rule: they simply call `FinanceManager`, which calls `Validator`.
"""


#
# IMPORT
#

from datetime import date, datetime, time
from decimal import Decimal, InvalidOperation

from core.exceptions import ValidationError



# Well-known type IDs from data/types.csv. Kept as constants because, per the
# specification, transaction types are predefined and not user-editable.

#
# Types
#


TYPE_INCOME = 1
TYPE_EXPENSE = 2
TYPE_ADJUSTMENT = 3


class Validator:
    """Collection of static validation helpers used across the backend."""

    @staticmethod
    def validate_unique_name(name: str, existing_names: list, label: str = "Item") -> str:
        """Ensure a name is non-empty and not a duplicate (case-insensitive)."""
        if name is None or not name.strip():
            raise ValidationError(f"{label} name cannot be empty.")

        cleaned = name.strip()
        if cleaned.lower() in [existing.lower() for existing in existing_names]:
            raise ValidationError(f"{label} '{cleaned}' already exists.")

        return cleaned

    @staticmethod
    def validate_category_name(name: str, existing_names: list) -> str:
        """Ensure a category name is non-empty and not a duplicate (case-insensitive)."""
        return Validator.validate_unique_name(name, existing_names, label="Category")

    @staticmethod
    def validate_type_name(name: str, existing_names: list) -> str:
        """Ensure a transaction type name is non-empty and not a duplicate (case-insensitive)."""
        return Validator.validate_unique_name(name, existing_names, label="Type")

    @staticmethod
    def validate_category_id(category_id, valid_ids: list) -> int:
        """Ensure a category ID refers to an existing category."""
        try:
            category_id = int(category_id)
        except (TypeError, ValueError):
            raise ValidationError(f"Invalid category ID: {category_id!r}")

        if category_id not in valid_ids:
            raise ValidationError(f"Category ID {category_id} does not exist.")

        return category_id

    @staticmethod
    def validate_type_id(type_id, valid_ids: list) -> int:
        """Ensure a transaction type ID refers to a known type."""
        try:
            type_id = int(type_id)
        except (TypeError, ValueError):
            raise ValidationError(f"Invalid transaction type: {type_id!r}")

        if type_id not in valid_ids:
            raise ValidationError(f"Transaction type {type_id} does not exist.")

        return type_id

    @staticmethod
    def validate_amount(raw_amount) -> Decimal:
        """Convert user input into a Decimal, rejecting non-numeric values."""
        try:
            amount = Decimal(str(raw_amount))
        except (InvalidOperation, TypeError, ValueError):
            raise ValidationError(f"'{raw_amount}' is not a valid numeric amount.")

        return amount.quantize(Decimal("0.01"))



        """
        Apply the correct sign to an amount based on its transaction type.

        - Income (type 1) must be positive.
        - Expense (type 2) must be negative.
        - Adjustment and any other (user-defined) type must be non-zero,
          keeping whatever sign the user entered.
        """



        
    @staticmethod
    def apply_sign_rules(amount: Decimal, type_id: int) -> Decimal:

        if amount == 0:
            raise ValidationError("Transaction amount cannot be zero.")

        magnitude = abs(amount)

        if type_id == TYPE_INCOME:
            return magnitude
        if type_id == TYPE_EXPENSE:
            return -magnitude

        return amount

    @staticmethod
    def validate_transaction_id(transaction_id, valid_ids: list) -> int:
        """Ensure a transaction ID refers to an existing transaction."""
        try:
            transaction_id = int(transaction_id)
        except (TypeError, ValueError):
            raise ValidationError(f"Invalid transaction ID: {transaction_id!r}")

        if transaction_id not in valid_ids:
            raise ValidationError(f"Transaction ID {transaction_id} does not exist.")

        return transaction_id

    @staticmethod
    def validate_date(date_str: str) -> date:
        """Parse a 'YYYY-MM-DD' string into a date, raising ValidationError if malformed."""
        try:
            return datetime.strptime(str(date_str).strip(), "%Y-%m-%d").date()
        except (ValueError, TypeError):
            raise ValidationError(f"'{date_str}' is not a valid date (expected YYYY-MM-DD).")

    @staticmethod
    def validate_time(time_str: str) -> time:
        """Parse 'HH:MM' or 'HH:MM:SS' into a time, raising ValidationError if malformed."""
        cleaned = str(time_str).strip()
        for fmt in ("%H:%M:%S", "%H:%M"):
            try:
                return datetime.strptime(cleaned, fmt).time()
            except (ValueError, TypeError):
                continue
        raise ValidationError(f"'{time_str}' is not a valid time (expected HH:MM or HH:MM:SS).")
