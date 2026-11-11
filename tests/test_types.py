"""Unit tests for transaction-type management in FinanceManager."""

import pytest

from core.exceptions import ValidationError, NotFoundError, TypeInUseError


def test_add_type_creates_unique_incremental_id(finance_manager):
    type_entry = finance_manager.add_type("Refund")
    assert type_entry["id"] == 4  # fixture already has IDs 1, 2, 3
    assert type_entry["name"] == "Refund"


def test_add_type_rejects_empty_name(finance_manager):
    with pytest.raises(ValidationError):
        finance_manager.add_type("   ")


def test_add_type_rejects_duplicate_case_insensitive(finance_manager):
    with pytest.raises(ValidationError):
        finance_manager.add_type("income")


def test_edit_type_renames_successfully(finance_manager):
    updated = finance_manager.edit_type(1, "Salary")
    assert updated["name"] == "Salary"
    assert finance_manager.get_type_name(1) == "Salary"


def test_edit_type_unknown_id_raises(finance_manager):
    with pytest.raises(NotFoundError):
        finance_manager.edit_type(999, "Anything")


def test_delete_type_in_use_is_blocked(finance_manager):
    # Type 2 (Expense) is referenced by a transaction in the fixture data.
    with pytest.raises(TypeInUseError):
        finance_manager.delete_type(2)


def test_delete_type_not_in_use_succeeds(finance_manager):
    type_entry = finance_manager.add_type("Unused Type")
    finance_manager.delete_type(type_entry["id"])
    with pytest.raises(NotFoundError):
        finance_manager.get_type_name(type_entry["id"])


def test_types_persist_across_reload(finance_manager, tmp_path):
    finance_manager.add_type("Refund")

    from core.finance_manager import FinanceManager
    reloaded = FinanceManager(str(tmp_path))
    names = [t["name"] for t in reloaded.get_types()]
    assert "Refund" in names


def test_new_type_follows_adjustment_style_sign_rules(finance_manager):
    """Custom types (not Income/Expense) keep whatever sign the user enters."""
    custom_type = finance_manager.add_type("Refund")
    transaction = finance_manager.add_transaction(
        type_id=custom_type["id"], category_id=1, amount="-15.00"
    )
    assert str(transaction.amount) == "-15.00"
