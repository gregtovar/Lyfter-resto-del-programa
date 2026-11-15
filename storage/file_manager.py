
#
# 
# FILE MANAGER
# 
# 
# 




"""
DESCRIPTION:


FileManager centralizes every read/write operation against the application's
CSV "database" (categories.csv, types.csv and transactions.csv).

No other module should open these files directly. This keeps file-format
details (headers, encoding, safe-write strategy) in a single place.
"""


#
# IMPORTS
#

import csv
import os
import tempfile

from core.category import Category
from core.transaction import Transaction
from core.validators import Validator
from core.exceptions import FileOperationError, ValidationError

CATEGORY_FIELDS = ["ID", "Category"]
TYPE_FIELDS = ["ID", "Type"]
TRANSACTION_FIELDS = ["ID", "TimeStamp", "Title", "Category", "Amount", "Type"]

# Seeded the first time the app runs against a data directory that has no
# types.csv yet. IDs match the TYPE_INCOME/TYPE_EXPENSE/TYPE_ADJUSTMENT
# constants in core/validators.py, which the sign-rule logic depends on.
DEFAULT_TYPES = [
    {"id": 1, "name": "Income"},
    {"id": 2, "name": "Expense"},
    {"id": 3, "name": "Adjustment"},
]



# Reads and writes the three CSV files that back the application

class FileManager:

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.categories_path = os.path.join(data_dir, "categories.csv")
        self.types_path = os.path.join(data_dir, "types.csv")
        self.transactions_path = os.path.join(data_dir, "transactions.csv")
        self.transactions_backup_path = os.path.join(data_dir, "transaction_backup.csv")

        # First run (or the data/ folder was deleted): create an empty directory
        # so later saves can write their files without a missing-folder error.
        try:
            os.makedirs(data_dir, exist_ok=True)
        except OSError as error:
            raise FileOperationError(f"Could not create data directory {data_dir}: {error}")

    # ------------------------------------------------------------------ #
    # Generic helpers
    # ------------------------------------------------------------------ #


    # Read a CSV file and return a list of row dicts, skipping malformed rows.
    # A missing file is treated as "no data yet" rather than an error, so a
    # fresh/empty data directory starts the app with empty lists instead of
    # crashing.

    @staticmethod
    def _read_csv(path: str, required_fields: list) -> list:
        if not os.path.exists(path):
            return []

        rows = []
        try:
            with open(path, "r", newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                for line_number, row in enumerate(reader, start=2):
                    if any(row.get(field) in (None, "") for field in required_fields):
                        # Malformed / incomplete record: skip it rather than crash.
                        print(f"Warning: skipping malformed row {line_number} in {path}")
                        continue
                    rows.append(row)
        except OSError as error:
            raise FileOperationError(f"Could not read {path}: {error}")

        return rows



        """
        Safely write rows to a CSV file.

        Writes to a temporary file first and then atomically replaces the
        target file, which greatly reduces the risk of data corruption if
        the process is interrupted mid-write.
        """




    @staticmethod
    def _write_csv(path: str, fieldnames: list, rows: list) -> None:

        directory = os.path.dirname(path) or "."
        try:
            with tempfile.NamedTemporaryFile(
                "w", newline="", encoding="utf-8", dir=directory,
                delete=False, suffix=".tmp"
            ) as tmp_file:
                writer = csv.DictWriter(tmp_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
                temp_path = tmp_file.name
            os.replace(temp_path, path)
        except OSError as error:
            raise FileOperationError(f"Could not write {path}: {error}")

    # ------------------------------------------------------------------ #
    # Categories
    # ------------------------------------------------------------------ #

    def load_categories(self) -> list:
        """Return all categories as a list of Category objects."""
        rows = self._read_csv(self.categories_path, CATEGORY_FIELDS)
        return [Category.from_row(row) for row in rows]

    def save_categories(self, categories: list) -> None:
        """Persist the full list of Category objects, overwriting the file."""
        rows = [category.to_row() for category in categories]
        self._write_csv(self.categories_path, CATEGORY_FIELDS, rows)

    # ------------------------------------------------------------------ #
    # Types
    # ------------------------------------------------------------------ #

    def load_types(self) -> list:
        """
        Return all transaction types as a list of (id, name) dicts.

        If types.csv does not exist yet (first run / fresh data directory),
        seed the default Income/Expense/Adjustment types instead of starting
        with an empty list, since sign-rule logic depends on them existing.
        """
        if not os.path.exists(self.types_path):
            return [dict(t) for t in DEFAULT_TYPES]

        rows = self._read_csv(self.types_path, TYPE_FIELDS)
        return [{"id": int(row["ID"]), "name": row["Type"]} for row in rows]

    def save_types(self, types: list) -> None:
        """Persist the full list of type dicts ({'id': int, 'name': str}), overwriting the file."""
        rows = [{"ID": t["id"], "Type": t["name"]} for t in types]
        self._write_csv(self.types_path, TYPE_FIELDS, rows)

    # ------------------------------------------------------------------ #
    # Transactions
    # ------------------------------------------------------------------ #
    
    def load_transactions(self) -> list:
        """Return all transactions as a list of Transaction objects."""
        return self.load_transactions_from(self.transactions_path)

    def load_transactions_from(self, path: str) -> list:
        """
        Return all transactions found in an arbitrary CSV file as Transaction
        objects.

        Every row is validated as it is parsed: the ID must be a unique whole
        number, Category/Type must be whole numbers, the timestamp must match
        "YYYY-MM-DD HH:MM:SS", and the amount must be a finite number. Any
        violation raises FileOperationError with the offending row number, so
        a malformed or hand-edited CSV is rejected with a clear message
        instead of crashing deep inside Transaction/Decimal parsing.
        """
        rows = self._read_csv(path, TRANSACTION_FIELDS)

        transactions = []
        seen_ids = set()
        for line_number, row in enumerate(rows, start=2):
            try:
                transaction_id = int(row["ID"])
            except (TypeError, ValueError):
                raise FileOperationError(
                    f"Row {line_number} in {path}: invalid transaction ID '{row['ID']}'."
                )

            if transaction_id in seen_ids:
                raise FileOperationError(
                    f"Row {line_number} in {path}: duplicate transaction ID {transaction_id}."
                )
            seen_ids.add(transaction_id)

            try:
                category_id = int(row["Category"])
            except (TypeError, ValueError):
                raise FileOperationError(
                    f"Row {line_number} in {path}: invalid category ID '{row['Category']}'."
                )

            try:
                type_id = int(row["Type"])
            except (TypeError, ValueError):
                raise FileOperationError(
                    f"Row {line_number} in {path}: invalid type ID '{row['Type']}'."
                )

            try:
                timestamp = Validator.validate_timestamp(row["TimeStamp"])
            except ValidationError as error:
                raise FileOperationError(f"Row {line_number} in {path}: {error}")

            try:
                amount = Validator.validate_amount(row["Amount"])
            except ValidationError as error:
                raise FileOperationError(f"Row {line_number} in {path}: {error}")

            transactions.append(Transaction(
                transaction_id=transaction_id,
                timestamp=timestamp,
                title=row["Title"],
                category_id=category_id,
                amount=amount,
                type_id=type_id,
            ))

        return transactions

    def save_transactions(self, transactions: list) -> None:
        """Persist the full list of Transaction objects, overwriting the file."""
        rows = [transaction.to_row() for transaction in transactions]
        self._write_csv(self.transactions_path, TRANSACTION_FIELDS, rows)

    def backup_transactions(self, transactions: list) -> str:
        """
        Write the given transactions to transaction_backup.csv, overwriting any
        previous backup. Returns the backup file path.
        """
        rows = [transaction.to_row() for transaction in transactions]
        self._write_csv(self.transactions_backup_path, TRANSACTION_FIELDS, rows)
        return self.transactions_backup_path
