
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
from core.exceptions import FileOperationError

CATEGORY_FIELDS = ["ID", "Category"]
TYPE_FIELDS = ["ID", "Type"]
TRANSACTION_FIELDS = ["ID", "TimeStamp", "Category", "Amount", "Type"]



# Reads and writes the three CSV files that back the application

class FileManager:

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.categories_path = os.path.join(data_dir, "categories.csv")
        self.types_path = os.path.join(data_dir, "types.csv")
        self.transactions_path = os.path.join(data_dir, "transactions.csv")
        self.transactions_backup_path = os.path.join(data_dir, "transaction_backup.csv")

    # ------------------------------------------------------------------ #
    # Generic helpers
    # ------------------------------------------------------------------ #


    # Read a CSV file and return a list of row dicts, skipping malformed rows.
    
    @staticmethod
    def _read_csv(path: str, required_fields: list) -> list:
        if not os.path.exists(path):
            raise FileOperationError(f"Required data file is missing: {path}")

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
        """Return all transaction types as a list of (id, name) dicts."""
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
        """Return all transactions found in an arbitrary CSV file as Transaction objects."""
        rows = self._read_csv(path, TRANSACTION_FIELDS)
        return [Transaction.from_row(row) for row in rows]

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
