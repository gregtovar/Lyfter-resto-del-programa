"""Unit tests for category management in FinanceManager."""

import pytest

from core.exceptions import ValidationError, NotFoundError, CategoryInUseError


def test_add_category_creates_unique_incremental_id(finance_manager):
    category = finance_manager.add_category("Entertainment")
    assert category.category_id == 3  # fixture already has IDs 1 and 2
    assert category.name == "Entertainment"


def test_add_category_rejects_empty_name(finance_manager):
    with pytest.raises(ValidationError):
        finance_manager.add_category("   ")


def test_add_category_rejects_duplicate_case_insensitive(finance_manager):
    with pytest.raises(ValidationError):
        finance_manager.add_category("meal")


def test_edit_category_renames_successfully(finance_manager):
    updated = finance_manager.edit_category(1, "Food & Dining")
    assert updated.name == "Food & Dining"
    assert finance_manager.get_category_by_id(1).name == "Food & Dining"


def test_edit_category_unknown_id_raises(finance_manager):
    with pytest.raises(NotFoundError):
        finance_manager.edit_category(999, "Anything")


def test_delete_category_in_use_is_blocked(finance_manager):
    # Category 1 is referenced by a transaction in the fixture data.
    with pytest.raises(CategoryInUseError):
        finance_manager.delete_category(1)


def test_delete_category_not_in_use_succeeds(finance_manager):
    category = finance_manager.add_category("Unused Category")
    finance_manager.delete_category(category.category_id)
    with pytest.raises(NotFoundError):
        finance_manager.get_category_by_id(category.category_id)


def test_categories_persist_across_reload(finance_manager, tmp_path):
    finance_manager.add_category("Hobbies")

    from core.finance_manager import FinanceManager
    reloaded = FinanceManager(str(tmp_path))
    names = [c.name for c in reloaded.get_categories()]
    assert "Hobbies" in names
