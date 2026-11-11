"""Shared pytest fixtures: a FinanceManager backed by a disposable temp data dir."""

import pytest

from core.finance_manager import FinanceManager

CATEGORIES_CSV = "ID,Category\n1,Meal\n2,Transportation\n"
TYPES_CSV = "ID,Type\n1,Income\n2,Expense\n3,Adjustment\n"
TRANSACTIONS_CSV = (
    "ID,TimeStamp,Category,Amount,Type\n"
    "10000001,2026-01-01 08:00:00,1,-19.85,2\n"
    "10000002,2026-01-02 09:00:00,2,500.00,1\n"
)


@pytest.fixture
def finance_manager(tmp_path):
    """Return a FinanceManager pointed at a temporary copy of the CSV data."""
    (tmp_path / "categories.csv").write_text(CATEGORIES_CSV, encoding="utf-8")
    (tmp_path / "types.csv").write_text(TYPES_CSV, encoding="utf-8")
    (tmp_path / "transactions.csv").write_text(TRANSACTIONS_CSV, encoding="utf-8")
    return FinanceManager(str(tmp_path))
