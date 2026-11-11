"""Unit tests for transaction creation, editing and dashboard calculations."""

import os
from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from core.exceptions import ValidationError, NotFoundError
from core.validators import TYPE_INCOME, TYPE_EXPENSE, TYPE_ADJUSTMENT


def test_add_transaction_generates_8_digit_id(finance_manager):
    transaction = finance_manager.add_transaction(type_id=TYPE_INCOME, category_id=1, amount="100.00")
    assert 10_000_000 <= transaction.transaction_id <= 99_999_999


def test_add_income_transaction_is_always_positive(finance_manager):
    transaction = finance_manager.add_transaction(type_id=TYPE_INCOME, category_id=1, amount="-50.00")
    assert transaction.amount == Decimal("50.00")


def test_add_expense_transaction_is_always_negative(finance_manager):
    transaction = finance_manager.add_transaction(type_id=TYPE_EXPENSE, category_id=1, amount="50.00")
    assert transaction.amount == Decimal("-50.00")


def test_add_adjustment_transaction_rejects_zero(finance_manager):
    with pytest.raises(ValidationError):
        finance_manager.add_transaction(type_id=TYPE_ADJUSTMENT, category_id=1, amount="0")


def test_add_transaction_rejects_unknown_category(finance_manager):
    with pytest.raises(ValidationError):
        finance_manager.add_transaction(type_id=TYPE_EXPENSE, category_id=999, amount="10.00")


def test_add_transaction_rejects_non_numeric_amount(finance_manager):
    with pytest.raises(ValidationError):
        finance_manager.add_transaction(type_id=TYPE_EXPENSE, category_id=1, amount="abc")


def test_edit_transaction_preserves_id_and_timestamp(finance_manager):
    original = finance_manager.get_transaction_by_id(10000001)
    updated = finance_manager.edit_transaction(10000001, amount="30.00")

    assert updated.transaction_id == original.transaction_id
    assert updated.timestamp == original.timestamp
    assert updated.amount == Decimal("-30.00")  # still an Expense, sign re-applied


def test_edit_transaction_unknown_id_raises(finance_manager):
    with pytest.raises(NotFoundError):
        finance_manager.edit_transaction(99999999, amount="10.00")


def test_dashboard_summary_totals(finance_manager):
    # Fixture data: -19.85 (Expense), 500.00 (Income)
    summary = finance_manager.dashboard_summary()
    assert summary["total_income"] == Decimal("500.00")
    assert summary["total_expenses"] == Decimal("19.85")
    assert summary["net_balance"] == Decimal("480.15")
    assert summary["transaction_count"] == 2


def test_no_categories_blocks_transaction_creation(tmp_path):
    from core.finance_manager import FinanceManager

    (tmp_path / "categories.csv").write_text("ID,Category\n", encoding="utf-8")
    (tmp_path / "types.csv").write_text("ID,Type\n1,Income\n2,Expense\n3,Adjustment\n", encoding="utf-8")
    (tmp_path / "transactions.csv").write_text("ID,TimeStamp,Category,Amount,Type\n", encoding="utf-8")

    manager = FinanceManager(str(tmp_path))
    with pytest.raises(NotFoundError):
        manager.add_transaction(type_id=TYPE_INCOME, category_id=1, amount="10.00")


def test_erase_transactions_backs_up_and_clears(finance_manager, tmp_path):
    original_count = len(finance_manager.get_transactions())
    assert original_count == 2

    backup_path = finance_manager.erase_transactions()

    assert os.path.basename(backup_path) == "transaction_backup.csv"
    assert os.path.exists(backup_path)
    assert finance_manager.get_transactions() == []

    with open(backup_path, encoding="utf-8") as handle:
        backup_lines = handle.read().strip().splitlines()
    assert len(backup_lines) == original_count + 1  # +1 for the header row

    # The live transactions file should now only contain the header.
    with open(tmp_path / "transactions.csv", encoding="utf-8") as handle:
        live_lines = handle.read().strip().splitlines()
    assert len(live_lines) == 1


def test_dashboard_summary_can_be_filtered_by_date_range(finance_manager):
    # Fixture transactions are dated 2026-01-01 and 2026-01-02.
    start = datetime(2026, 1, 1, 0, 0, 0)
    end = datetime(2026, 1, 1, 23, 59, 59)

    summary = finance_manager.dashboard_summary(start=start, end=end)
    assert summary["transaction_count"] == 1
    assert summary["total_expenses"] == Decimal("19.85")


def test_last_n_days_bounds_excludes_older_transactions(finance_manager):
    # Fixture data is dated 2026-01-01/02, far outside "last 7 days" from now.
    start, end = finance_manager.last_n_days_bounds(7)
    assert start < end
    summary = finance_manager.dashboard_summary(start=start, end=end)
    assert summary["transaction_count"] == 0


def test_parse_date_range_rejects_start_after_end(finance_manager):
    with pytest.raises(ValidationError):
        finance_manager.parse_date_range("2026-02-01", "2026-01-01")


def test_parse_date_range_rejects_malformed_date(finance_manager):
    with pytest.raises(ValidationError):
        finance_manager.parse_date_range("not-a-date", "2026-01-01")
