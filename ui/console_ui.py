#
#
# CONSOLE FRONT END
#
#




"""

DESCRIPTION

Console (text-based) interface for the Personal Finance Manager.

This module only handles displaying menus, collecting user input and
printing results. All business rules live in FinanceManager; this file
never touches CSV files directly.
"""

#
#
# IMPORTS
#
#

import os
from datetime import datetime
from decimal import Decimal

from core.exceptions import FinanceManagerError

ABOUT_TEXT = """
Personal Finance Manager ver 1.15b
License Number: JFKWDWNN6488HHKTY654
November 2016
App developed as part of the LYTFER Stack Developer Certification.
Developer: Greg Tovar
Frond End Designer and Back end Architect: Greg Tovar

Regulatory Certification
\u2122 and \u00a9 2026
All Rights Reserved
"""


def _ascii_bar(value, max_value, width=30) -> str:
    """Render `value` as a block-character bar scaled against `max_value`."""
    if not max_value:
        filled = 0
    else:
        filled = int(round((float(value) / float(max_value)) * width))
    filled = max(0, min(width, filled))
    return "█" * filled + "░" * (width - filled)


class ConsoleUI:
    """Text-based menu system driving a FinanceManager instance."""

    def __init__(self, finance_manager):
        self.finance_manager = finance_manager

    # ------------------------------------------------------------------ #
    # Main loop
    # ------------------------------------------------------------------ #
    def run(self) -> None:
        """Display the main menu loop until the user chooses to exit."""
        while True:
            print("\n" + "=" * 42)
            print("       PERSONAL FINANCE MANAGER")
            print("=" * 42)
            print("1. Admin (Manage Categories)")
            print("2. Create a New Transaction")
            print("3. Edit an Existing Transaction")
            print("4. Erase a Transaction")
            print("5. Dashboard (Summary & Reports)")
            print("6. About Personal Finance Manager")
            print("0. Exit")
            print("-" * 42)
            choice = input("Select an option: ").strip()

            if choice == "1":
                self.admin_menu()
            elif choice == "2":
                self.create_transaction()
            elif choice == "3":
                self.edit_transaction()
            elif choice == "4":
                self.erase_transaction()
            elif choice == "5":
                self.dashboard_menu()
            elif choice == "6":
                self.show_about()
            elif choice == "0":
                print("Returning to the startup menu...")
                break
            else:
                print("Invalid option. Please try again.")

    def show_about(self) -> None:
        print(ABOUT_TEXT)

    # ------------------------------------------------------------------ #
    # Admin
    # ------------------------------------------------------------------ #
    def admin_menu(self) -> None:
        while True:
            print("\n--- Admin ---")
            print("1. Manage Categories")
            print("2. Manage Types")
            print("3. Initialize Transaction File")
            print("4. Upload CSV File")
            print("\n" * 3)
            print("0. Leave Admin")
            choice = input("Select an option: ").strip()

            if choice == "1":
                self.category_menu()
            elif choice == "2":
                self.type_menu()
            elif choice == "3":
                self._erase_transactions()
            elif choice == "4":
                self._upload_csv_file()
            elif choice == "0":
                break
            else:
                print("Invalid option. Please try again.")

    # --- Categories -----------------------------------------------------
    def category_menu(self) -> None:
        while True:
            print("\n--- Manage Categories ---")
            self._print_categories()
            print("1. Add Category")
            print("2. Edit Category")
            print("3. Delete Category")
            print("0. Back")
            choice = input("Select an option: ").strip()

            if choice == "1":
                self._add_category()
            elif choice == "2":
                self._edit_category()
            elif choice == "3":
                self._delete_category()
            elif choice == "0":
                break
            else:
                print("Invalid option. Please try again.")

    def _print_categories(self) -> None:
        categories = self.finance_manager.get_categories()
        if not categories:
            print("(No categories yet.)")
            return
        for category in categories:
            print(f"  {category.category_id:>3}. {category.name}")

    def _add_category(self) -> None:
        name = input("New category name: ").strip()
        try:
            category = self.finance_manager.add_category(name)
            print(f"Category '{category.name}' created with ID {category.category_id}.")
        except FinanceManagerError as error:
            print(f"Error: {error}")

    def _edit_category(self) -> None:
        self._print_categories()
        category_id = input("Enter the ID of the category to edit: ").strip()
        new_name = input("New name: ").strip()
        try:
            category = self.finance_manager.edit_category(category_id, new_name)
            print(f"Category {category.category_id} renamed to '{category.name}'.")
        except FinanceManagerError as error:
            print(f"Error: {error}")

    def _delete_category(self) -> None:
        self._print_categories()
        category_id = input("Enter the ID of the category to delete: ").strip()
        try:
            self.finance_manager.delete_category(category_id)
            print("Category deleted.")
        except FinanceManagerError as error:
            print(f"Error: {error}")

    # --- Types ------------------------------------------------------------
    def type_menu(self) -> None:
        while True:
            print("\n--- Manage Types ---")
            self._print_types()
            print("1. Add Type")
            print("2. Edit Type")
            print("3. Delete Type")
            print("0. Back")
            choice = input("Select an option: ").strip()

            if choice == "1":
                self._add_type()
            elif choice == "2":
                self._edit_type()
            elif choice == "3":
                self._delete_type()
            elif choice == "0":
                break
            else:
                print("Invalid option. Please try again.")

    def _print_types(self) -> None:
        types = self.finance_manager.get_types()
        if not types:
            print("(No transaction types yet.)")
            return
        for type_entry in types:
            print(f"  {type_entry['id']:>3}. {type_entry['name']}")

    def _add_type(self) -> None:
        name = input("New type name: ").strip()
        try:
            type_entry = self.finance_manager.add_type(name)
            print(f"Type '{type_entry['name']}' created with ID {type_entry['id']}.")
        except FinanceManagerError as error:
            print(f"Error: {error}")

    def _edit_type(self) -> None:
        self._print_types()
        type_id = input("Enter the ID of the type to edit: ").strip()
        new_name = input("New name: ").strip()
        try:
            type_entry = self.finance_manager.edit_type(type_id, new_name)
            print(f"Type {type_entry['id']} renamed to '{type_entry['name']}'.")
        except FinanceManagerError as error:
            print(f"Error: {error}")

    def _delete_type(self) -> None:
        self._print_types()
        type_id = input("Enter the ID of the type to delete: ").strip()
        try:
            self.finance_manager.delete_type(type_id)
            print("Type deleted.")
        except FinanceManagerError as error:
            print(f"Error: {error}")

    # --- Erase transactions ------------------------------------------------
    def _erase_transactions(self) -> None:
        count = len(self.finance_manager.get_transactions())
        if count == 0:
            print("There are no transactions to erase.")
            return

        confirm = input(
            f"This will erase all {count} transactions and save a backup to "
            "transaction_backup.csv. Continue? (y/n): "
        ).strip().lower()
        if confirm != "y":
            print("Cancelled.")
            return

        try:
            backup_path = self.finance_manager.erase_transactions()
            print(f"All transactions erased. Backup saved to: {backup_path}")
        except FinanceManagerError as error:
            print(f"Error: {error}")

    def _upload_csv_file(self) -> None:
        source_path = input("Enter the full path of the CSV file to upload: ").strip()
        if not source_path:
            print("Cancelled.")
            return
        if not os.path.isfile(source_path):
            print(f"Error: file not found: {source_path}")
            return

        confirm = input(
            "The current transactions.csv will be backed up to transaction_backup.csv "
            "before it is replaced. Continue? (y/n): "
        ).strip().lower()
        if confirm != "y":
            print("Cancelled.")
            return

        try:
            backup_path = self.finance_manager.replace_transactions_file(source_path)
            print(f"transactions.csv replaced successfully. Previous data backed up to: {backup_path}")
        except FinanceManagerError as error:
            print(f"Error: {error}")

    # ------------------------------------------------------------------ #
    # Create transaction
    # ------------------------------------------------------------------ #
    def create_transaction(self) -> None:
        print("\n--- Create a New Transaction ---")

        if not self.finance_manager.get_categories():
            print("No categories are available. Please create a category before adding a transaction.")
            return

        print("Transaction types:")
        self._print_types()
        type_id = input("Select a Type ID: ").strip()

        self._print_categories()
        category_id = input("Category ID: ").strip()
        amount = input("Amount: ").strip()

        now = datetime.now()
        date_str = input(f"Date (YYYY-MM-DD) [{now.strftime('%Y-%m-%d')}]: ").strip() or now.strftime("%Y-%m-%d")
        time_str = input(f"Time (HH:MM:SS) [{now.strftime('%H:%M:%S')}]: ").strip() or now.strftime("%H:%M:%S")

        try:
            timestamp = self.finance_manager.combine_date_time(date_str, time_str)
            transaction = self.finance_manager.add_transaction(
                type_id=type_id, category_id=category_id, amount=amount, timestamp=timestamp
            )
            print(f"Transaction {transaction.transaction_id} saved: {transaction.amount}")
        except FinanceManagerError as error:
            print(f"Error: {error}")

    # ------------------------------------------------------------------ #
    # Edit transaction
    # ------------------------------------------------------------------ #
    def edit_transaction(self) -> None:
        print("\n--- Edit an Existing Transaction ---")
        self._print_transactions(self.finance_manager.get_transactions())
        transaction_id = input("Enter the transaction ID to edit: ").strip()

        try:
            transaction = self.finance_manager.get_transaction_by_id(transaction_id)
        except FinanceManagerError as error:
            print(f"Error: {error}")
            return

        print(f"Current category: {transaction.category_id}, "
              f"amount: {transaction.amount}, type: {transaction.type_id}")
        print("Leave a field blank to keep its current value.")

        category_id = input("New category ID: ").strip() or None
        amount = input("New amount: ").strip() or None
        self._print_types()
        type_id = input("New Type ID: ").strip() or None
        date_str = input("New date (YYYY-MM-DD): ").strip() or None
        time_str = input("New time (HH:MM:SS): ").strip() or None

        try:
            timestamp = None
            if date_str or time_str:
                current = datetime.strptime(transaction.timestamp, "%Y-%m-%d %H:%M:%S")
                timestamp = self.finance_manager.combine_date_time(
                    date_str or current.strftime("%Y-%m-%d"),
                    time_str or current.strftime("%H:%M:%S"),
                )
            updated = self.finance_manager.edit_transaction(
                transaction_id, category_id=category_id, amount=amount, type_id=type_id,
                timestamp=timestamp,
            )
            print(f"Transaction {updated.transaction_id} updated: {updated.amount}")
        except FinanceManagerError as error:
            print(f"Error: {error}")

    # ------------------------------------------------------------------ #
    # Erase a single transaction
    # ------------------------------------------------------------------ #
    def erase_transaction(self) -> None:
        print("\n--- Erase a Transaction ---")
        self._print_transactions(self.finance_manager.get_transactions())
        transaction_id = input("Enter the transaction ID to erase: ").strip()

        try:
            transaction = self.finance_manager.get_transaction_by_id(transaction_id)
        except FinanceManagerError as error:
            print(f"Error: {error}")
            return

        confirm = input(
            f"This will permanently erase transaction ID {transaction.transaction_id}. "
            "Continue? (y/n): "
        ).strip().lower()
        if confirm != "y":
            print("Cancelled.")
            return

        try:
            self.finance_manager.delete_transaction(transaction.transaction_id)
            print(f"Transaction ID {transaction.transaction_id} was erased.")
        except FinanceManagerError as error:
            print(f"Error: {error}")

    def _print_transactions(self, transactions) -> None:
        if not transactions:
            print("(No transactions yet.)")
            return
        print(f"{'ID':<10}{'TimeStamp':<21}{'Category':<15}{'Type':<14}{'Amount':>10}")
        for transaction in transactions:
            try:
                category_name = self.finance_manager.get_category_by_id(transaction.category_id).name
            except FinanceManagerError:
                category_name = "(deleted)"
            try:
                type_name = self.finance_manager.get_type_name(transaction.type_id)
            except FinanceManagerError:
                type_name = "(deleted)"
            print(f"{transaction.transaction_id:<10}{transaction.timestamp:<21}"
                  f"{category_name:<15}{type_name:<14}{transaction.amount:>10}")

    # ------------------------------------------------------------------ #
    # Dashboard
    # ------------------------------------------------------------------ #
    def dashboard_menu(self) -> None:
        print("\n--- Dashboard ---")
        print("1. All Time")
        print("2. Last 30 Days")
        print("3. Last 2 Weeks")
        print("4. Last Week")
        print("5. Yesterday")
        print("6. Today")
        print("7. Custom Range")
        print("0. Back to Main Menu")
        choice = input("Select an option: ").strip()

        start = end = None
        label = "All Time"

        if choice == "1":
            label = "All Time"
        elif choice == "2":
            start, end = self.finance_manager.last_n_days_bounds(30)
            label = "Last 30 Days"
        elif choice == "3":
            start, end = self.finance_manager.last_n_days_bounds(14)
            label = "Last 2 Weeks"
        elif choice == "4":
            start, end = self.finance_manager.last_n_days_bounds(7)
            label = "Last Week"
        elif choice == "5":
            start, end = self.finance_manager.day_bounds(1)
            label = "Yesterday"
        elif choice == "6":
            start, end = self.finance_manager.day_bounds(0)
            label = "Today"
        elif choice == "7":
            start_str = input("Start date (YYYY-MM-DD): ").strip()
            end_str = input("End date (YYYY-MM-DD): ").strip()
            try:
                start, end = self.finance_manager.parse_date_range(start_str, end_str)
            except FinanceManagerError as error:
                print(f"Error: {error}")
                return
            label = f"Custom Range ({start_str} to {end_str})"
        elif choice == "0":
            return
        else:
            print("Invalid option. Please try again.")
            return

        self.show_dashboard(start=start, end=end, label=label)

    def show_dashboard(self, start=None, end=None, label="All Transactions") -> None:
        print(f"\n--- Dashboard: {label} ---")
        summary = self.finance_manager.dashboard_summary(start=start, end=end)

        print(f"Total Income:     {summary['total_income']:>12}")
        print(f"Total Expenses:   {summary['total_expenses']:>12}")
        print(f"Net Balance:      {summary['net_balance']:>12}")
        print(f"Transactions:     {summary['transaction_count']:>12}")

        print("\n--- Income vs Expenses ---")
        max_val = max(summary["total_income"], summary["total_expenses"], Decimal("0.01"))
        print(f"  Income   {_ascii_bar(summary['total_income'], max_val)}  {summary['total_income']}")
        print(f"  Expenses {_ascii_bar(summary['total_expenses'], max_val)}  {summary['total_expenses']}")

        print("\n--- By Category (share of total) ---")
        category_totals = self.finance_manager.category_totals_abs(start=start, end=end)
        total_categorized = sum(category_totals.values()) if category_totals else Decimal("0.00")
        ranked = sorted(category_totals.items(), key=lambda kv: kv[1], reverse=True)
        if not ranked:
            print("  (no transactions in this view)")
        else:
            for category_id, amount in ranked:
                try:
                    name = self.finance_manager.get_category_by_id(category_id).name
                except FinanceManagerError:
                    name = f"(deleted #{category_id})"
                pct = (amount / total_categorized * 100) if total_categorized else Decimal("0")
                print(f"  {name:<18} {_ascii_bar(amount, total_categorized)}  {amount:>10}  {pct:5.1f}%")
            print(f"  {'Total':<18} {' ' * 30}  {total_categorized:>10}  100.0%")

        print("\nBy Type:")
        for type_id, total in summary["by_type"].items():
            try:
                name = self.finance_manager.get_type_name(type_id)
            except FinanceManagerError:
                name = f"(deleted #{type_id})"
            print(f"  {name:<20} {total}")

        print("\nTransactions:")
        self._print_transactions(self.finance_manager.get_transactions(start=start, end=end))
