"""
FinanceManager: the shared business-logic layer.

Every presentation layer (Console or GUI) must perform its work exclusively
through this class. It never touches CSV files directly (that is the
FileManager's job) and never prints or opens windows (that is the UI's job).

The idea is to ISOLATE the logic from the front end as request.

I creates a CONSOLE BASED and aldo GUI

"""



#
# Imports
#


import os
import random
from datetime import datetime, timedelta
from decimal import Decimal

from core.category import Category
from core.transaction import Transaction
from core.validators import Validator, TYPE_INCOME, TYPE_EXPENSE, TYPE_ADJUSTMENT
from core.exceptions import (
    NotFoundError, CategoryInUseError, TypeInUseError, ValidationError, FileOperationError,
)
from storage.file_manager import FileManager



#
# Format definition
# 


TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

#
# Coordinates category management, transactions and dashboard reporting.
#


class FinanceManager:
   

    def __init__(self, data_dir: str):
        self.file_manager = FileManager(data_dir)
        self.categories = self.file_manager.load_categories()
        self.types = self.file_manager.load_types()
        self.transactions = self.file_manager.load_transactions()

    # ------------------------------------------------------------------ #
    # Categories
    # ------------------------------------------------------------------ #
    def get_categories(self) -> list:
        """Return all categories, sorted by ID."""
        return sorted(self.categories, key=lambda c: c.category_id)

    def get_category_by_id(self, category_id) -> Category:
        """Return the Category with the given ID or raise NotFoundError."""
        for category in self.categories:
            if category.category_id == int(category_id):
                return category
        raise NotFoundError(f"Category ID {category_id} does not exist.")

    def _next_category_id(self) -> int:
        if not self.categories:
            return 1
        return max(category.category_id for category in self.categories) + 1

    def add_category(self, name: str) -> Category:
        """Validate and persist a new category. Returns the created Category."""
        existing_names = [category.name for category in self.categories]
        clean_name = Validator.validate_category_name(name, existing_names)

        category = Category(category_id=self._next_category_id(), name=clean_name)
        self.categories.append(category)
        self.file_manager.save_categories(self.categories)
        return category

    def edit_category(self, category_id, new_name: str) -> Category:
        """Rename an existing category."""
        category = self.get_category_by_id(category_id)

        other_names = [c.name for c in self.categories if c.category_id != category.category_id]
        clean_name = Validator.validate_category_name(new_name, other_names)

        category.name = clean_name
        self.file_manager.save_categories(self.categories)
        return category

    def delete_category(self, category_id) -> None:
        """Delete a category, unless it is still referenced by a transaction."""
        category = self.get_category_by_id(category_id)

        in_use = any(t.category_id == category.category_id for t in self.transactions)
        if in_use:
            raise CategoryInUseError(
                f"Category '{category.name}' cannot be deleted because it is used by "
                "existing transactions. Reassign those transactions first."
            )

        self.categories = [c for c in self.categories if c.category_id != category.category_id]
        self.file_manager.save_categories(self.categories)




    # ------------------------------------------------------------------ #
    # Types
    # ------------------------------------------------------------------ #


    def get_types(self) -> list:
        """Return the list of transaction types, sorted by ID."""
        return sorted(self.types, key=lambda t: t["id"])

    def get_type_name(self, type_id) -> str:
        """Return the display name for a type ID."""
        for type_entry in self.types:
            if type_entry["id"] == int(type_id):
                return type_entry["name"]
        raise NotFoundError(f"Transaction type {type_id} does not exist.")

    def _next_type_id(self) -> int:
        if not self.types:
            return 1
        return max(t["id"] for t in self.types) + 1

    def add_type(self, name: str) -> dict:
        """Validate and persist a new transaction type. Returns the created type dict."""
        existing_names = [t["name"] for t in self.types]
        clean_name = Validator.validate_type_name(name, existing_names)

        new_type = {"id": self._next_type_id(), "name": clean_name}
        self.types.append(new_type)
        self.file_manager.save_types(self.types)
        return new_type

    def edit_type(self, type_id, new_name: str) -> dict:
        """Rename an existing transaction type."""
        type_id = int(type_id)
        type_entry = next((t for t in self.types if t["id"] == type_id), None)
        if type_entry is None:
            raise NotFoundError(f"Transaction type {type_id} does not exist.")

        other_names = [t["name"] for t in self.types if t["id"] != type_id]
        clean_name = Validator.validate_type_name(new_name, other_names)

        type_entry["name"] = clean_name
        self.file_manager.save_types(self.types)
        return type_entry

    def delete_type(self, type_id) -> None:
        """Delete a transaction type, unless it is still referenced by a transaction."""
        type_id = int(type_id)
        type_entry = next((t for t in self.types if t["id"] == type_id), None)
        if type_entry is None:
            raise NotFoundError(f"Transaction type {type_id} does not exist.")

        in_use = any(t.type_id == type_id for t in self.transactions)
        if in_use:
            raise TypeInUseError(
                f"Type '{type_entry['name']}' cannot be deleted because it is used by "
                "existing transactions. Reassign those transactions first."
            )

        self.types = [t for t in self.types if t["id"] != type_id]
        self.file_manager.save_types(self.types)



    # ------------------------------------------------------------------ #
    # Transactions
    # ------------------------------------------------------------------ #


    def get_transactions(self, start=None, end=None) -> list:
        """
        Return transactions, most recent first.

        `start`/`end` are optional inclusive datetime bounds used to restrict
        the result to a time period (see `last_n_days_bounds`/`parse_date_range`).
        """
        transactions = self._filter_transactions(start, end)
        return sorted(transactions, key=lambda t: t.timestamp, reverse=True)

    def get_transaction_by_id(self, transaction_id) -> Transaction:
        """Return the Transaction with the given ID or raise NotFoundError."""
        for transaction in self.transactions:
            if transaction.transaction_id == int(transaction_id):
                return transaction
        raise NotFoundError(f"Transaction ID {transaction_id} does not exist.")

    def _next_transaction_id(self) -> int:
        """Generate a unique random 8-digit transaction ID."""
        existing_ids = {t.transaction_id for t in self.transactions}
        while True:
            candidate = random.randint(10_000_000, 99_999_999)
            if candidate not in existing_ids:
                return candidate



#
# Validate and create a new transaction
#

    """

    EXPLANATION: 

    `amount` should be the magnitude entered by the user; the correct
    sign is applied automatically based on the transaction type.
    `timestamp`, if given, must already be a "%Y-%m-%d %H:%M:%S" string
    (see `combine_date_time`); it defaults to the current date/time.


    """


    def add_transaction(self, type_id, category_id, amount, timestamp=None) -> Transaction:

        if not self.categories:
            raise NotFoundError(
                "No categories are available. Please create a category before "
                "adding a transaction."
            )

        valid_type_ids = [t["id"] for t in self.types]
        type_id = Validator.validate_type_id(type_id, valid_type_ids)

        valid_category_ids = [c.category_id for c in self.categories]
        category_id = Validator.validate_category_id(category_id, valid_category_ids)

        raw_amount = Validator.validate_amount(amount)
        signed_amount = Validator.apply_sign_rules(raw_amount, type_id)

        transaction = Transaction(
            transaction_id=self._next_transaction_id(),
            timestamp=timestamp or datetime.now().strftime(TIMESTAMP_FORMAT),
            category_id=category_id,
            amount=signed_amount,
            type_id=type_id,
        )
        self.transactions.append(transaction)
        self.file_manager.save_transactions(self.transactions)
        return transaction

#
# EDIT transaction
#



        """
        Update an existing transaction's category, amount, type and/or timestamp.

        The transaction's original ID is always preserved. Any parameter left
        as None keeps its current value (including the timestamp, by default).
        """




    def edit_transaction(self, transaction_id, category_id=None, amount=None, type_id=None,
                          timestamp=None) -> Transaction:

        transaction = self.get_transaction_by_id(transaction_id)

        new_type_id = transaction.type_id
        if type_id is not None:
            valid_type_ids = [t["id"] for t in self.types]
            new_type_id = Validator.validate_type_id(type_id, valid_type_ids)

        new_category_id = transaction.category_id
        if category_id is not None:
            valid_category_ids = [c.category_id for c in self.categories]
            new_category_id = Validator.validate_category_id(category_id, valid_category_ids)

        #
        # NOTE--------
        # 
        # Start from the current magnitude (sign-less) and overwrite it if the
        # caller supplied a new amount; the sign is then recomputed from the
        # (possibly new) transaction type.
        #
        #




        new_magnitude = Validator.validate_amount(amount) if amount is not None else abs(transaction.amount)
        new_amount = Validator.apply_sign_rules(new_magnitude, new_type_id)

        transaction.category_id = new_category_id
        transaction.type_id = new_type_id
        transaction.amount = new_amount
        if timestamp is not None:
            transaction.timestamp = timestamp

        self.file_manager.save_transactions(self.transactions)
        return transaction


#
# DELETE transaction
#


    def delete_transaction(self, transaction_id) -> None:
        """Delete a single transaction by ID, persisting the change."""
        transaction = self.get_transaction_by_id(transaction_id)
        self.transactions = [
            t for t in self.transactions if t.transaction_id != transaction.transaction_id
        ]
        self.file_manager.save_transactions(self.transactions)

    def erase_transactions(self) -> str:
        """
        Back up every current transaction to transaction_backup.csv, then
        erase transactions.csv (keeping only its header). Returns the path
        of the backup file that was written.
        """
        backup_path = self.file_manager.backup_transactions(self.transactions)
        self.transactions = []
        self.file_manager.save_transactions(self.transactions)
        return backup_path


#
# REPLACE transaction
#

    def replace_transactions_file(self, source_path: str) -> str:
        """
        Replace transactions.csv with the contents of `source_path`.

        The current transactions.csv is first backed up to
        transaction_backup.csv, then the new file is validated by loading it
        (raising FileOperationError if malformed) before it replaces the
        live data and in-memory transaction list. Returns the backup path.
        """
        if not os.path.isfile(source_path):
            raise FileOperationError(f"File not found: {source_path}")

        new_transactions = self.file_manager.load_transactions_from(source_path)

        backup_path = self.file_manager.backup_transactions(self.transactions)
        self.transactions = new_transactions
        self.file_manager.save_transactions(self.transactions)
        return backup_path



    # ------------------------------------------------------------------ #
    # Dashboard
    # ------------------------------------------------------------------ #



    @staticmethod
    def last_n_days_bounds(days: int):
        """Return (start, end) datetimes covering the trailing `days` days up to now."""
        end = datetime.now()
        start = end - timedelta(days=days)
        return start, end

    @staticmethod
    def day_bounds(days_ago: int = 0):
        """Return (start, end) datetimes covering a single calendar day,
        `days_ago` days before today (0 = today, 1 = yesterday)."""
        target = (datetime.now() - timedelta(days=days_ago)).date()
        start = datetime.combine(target, datetime.min.time())
        end = datetime.combine(target, datetime.max.time().replace(microsecond=0))
        return start, end

    @staticmethod
    def combine_date_time(date_str: str, time_str: str) -> str:
        """Validate a 'YYYY-MM-DD' date and 'HH:MM[:SS]' time and combine them
        into a single "%Y-%m-%d %H:%M:%S" timestamp string."""
        parsed_date = Validator.validate_date(date_str)
        parsed_time = Validator.validate_time(time_str)
        return datetime.combine(parsed_date, parsed_time).strftime(TIMESTAMP_FORMAT)

    def get_data_file_paths(self) -> dict:
        """Return the absolute paths of the CSV files currently in use."""
        return {
            "categories": self.file_manager.categories_path,
            "types": self.file_manager.types_path,
            "transactions": self.file_manager.transactions_path,
        }

    @staticmethod
    def parse_date_range(start_str: str, end_str: str):
        """
        Validate two 'YYYY-MM-DD' strings and return (start, end) datetimes
        covering the full inclusive range (00:00:00 to 23:59:59).
        """
        start_date = Validator.validate_date(start_str)
        end_date = Validator.validate_date(end_str)
        if start_date > end_date:
            raise ValidationError("The start date must be on or before the end date.")

        start = datetime.combine(start_date, datetime.min.time())
        end = datetime.combine(end_date, datetime.max.time().replace(microsecond=0))
        return start, end

    def _filter_transactions(self, start=None, end=None, category_id=None, type_id=None) -> list:
        """Return transactions whose timestamp falls within [start, end] (either
        bound optional), optionally further restricted to one category and/or
        one transaction type."""
        transactions = self.transactions
        if start is not None:
            transactions = [
                t for t in transactions
                if datetime.strptime(t.timestamp, TIMESTAMP_FORMAT) >= start
            ]
        if end is not None:
            transactions = [
                t for t in transactions
                if datetime.strptime(t.timestamp, TIMESTAMP_FORMAT) <= end
            ]
        if category_id is not None:
            transactions = [t for t in transactions if t.category_id == category_id]
        if type_id is not None:
            transactions = [t for t in transactions if t.type_id == type_id]
        return transactions


#
# DASHBOARD 
#



        """
        Compute the financial summary used by both the Console and GUI dashboards.

        `start`/`end` are optional datetime bounds (inclusive) used to restrict
        the summary to a time period, e.g. the last month or a custom range.
        `category_id`/`type_id` optionally restrict it further to a single
        category and/or transaction type. Leaving everything as None
        summarizes every transaction.

        Returns a dict with total income, total expenses (as a positive
        number), net balance, transaction count and per-category / per-type
        breakdowns.
        """



        
    def dashboard_summary(self, start=None, end=None, category_id=None, type_id=None) -> dict:

        transactions = self._filter_transactions(start, end, category_id, type_id)

        total_income = Decimal("0.00")
        total_expenses = Decimal("0.00")
        net_balance = Decimal("0.00")
        by_category = {}
        by_type = {}

        for transaction in transactions:
            net_balance += transaction.amount

            if transaction.type_id == TYPE_INCOME:
                total_income += transaction.amount
            elif transaction.type_id == TYPE_EXPENSE:
                total_expenses += abs(transaction.amount)

            by_category[transaction.category_id] = (
                by_category.get(transaction.category_id, Decimal("0.00")) + transaction.amount
            )
            by_type[transaction.type_id] = (
                by_type.get(transaction.type_id, Decimal("0.00")) + transaction.amount
            )

        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_balance": net_balance,
            "transaction_count": len(transactions),
            "by_category": by_category,
            "by_type": by_type,
        }

    def expenses_by_category(self, start=None, end=None) -> dict:
        """Return {category_id: positive total} for Expense transactions in the given period."""
        transactions = self._filter_transactions(start, end)
        totals = {}
        for transaction in transactions:
            if transaction.type_id != TYPE_EXPENSE:
                continue
            totals[transaction.category_id] = (
                totals.get(transaction.category_id, Decimal("0.00")) + abs(transaction.amount)
            )
        return totals

    def category_totals_abs(self, start=None, end=None, category_id=None, type_id=None) -> dict:
        """Return {category_id: absolute total} across every transaction type
        (Income, Expense, Adjustment, ...) in the given period/filters. Used
        to drive the "by category" pie chart on both front-ends."""
        transactions = self._filter_transactions(start, end, category_id, type_id)
        totals = {}
        for transaction in transactions:
            totals[transaction.category_id] = (
                totals.get(transaction.category_id, Decimal("0.00")) + abs(transaction.amount)
            )
        return totals
