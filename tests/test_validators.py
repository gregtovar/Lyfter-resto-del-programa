"""Unit tests for core.validators.Validator."""

from decimal import Decimal

import pytest

from core.validators import Validator, TYPE_INCOME, TYPE_EXPENSE, TYPE_ADJUSTMENT
from core.exceptions import ValidationError


def test_validate_category_name_rejects_empty():
    with pytest.raises(ValidationError):
        Validator.validate_category_name("   ", existing_names=[])


def test_validate_category_name_rejects_case_insensitive_duplicate():
    with pytest.raises(ValidationError):
        Validator.validate_category_name("meal", existing_names=["Meal"])


def test_validate_category_name_accepts_new_name():
    assert Validator.validate_category_name("Groceries", existing_names=["Meal"]) == "Groceries"


def test_validate_amount_rejects_non_numeric():
    with pytest.raises(ValidationError):
        Validator.validate_amount("not-a-number")


def test_validate_amount_accepts_numeric_string():
    assert Validator.validate_amount("12.3") == Decimal("12.30")
    assert Validator.validate_amount("12.349") == Decimal("12.35")  # rounds to 2 decimals


def test_apply_sign_rules_income_is_always_positive():
    assert Validator.apply_sign_rules(Decimal("-50.00"), TYPE_INCOME) == Decimal("50.00")


def test_apply_sign_rules_expense_is_always_negative():
    assert Validator.apply_sign_rules(Decimal("50.00"), TYPE_EXPENSE) == Decimal("-50.00")


def test_apply_sign_rules_adjustment_keeps_sign():
    assert Validator.apply_sign_rules(Decimal("-10.00"), TYPE_ADJUSTMENT) == Decimal("-10.00")
    assert Validator.apply_sign_rules(Decimal("10.00"), TYPE_ADJUSTMENT) == Decimal("10.00")


def test_apply_sign_rules_rejects_zero():
    with pytest.raises(ValidationError):
        Validator.apply_sign_rules(Decimal("0.00"), TYPE_ADJUSTMENT)


def test_validate_category_id_rejects_unknown_id():
    with pytest.raises(ValidationError):
        Validator.validate_category_id(999, valid_ids=[1, 2, 3])


def test_validate_type_id_rejects_unknown_type():
    with pytest.raises(ValidationError):
        Validator.validate_type_id(99, valid_ids=[1, 2, 3])
