"""Lab 6: line-coverage tests for the assigned income tax calculator.

Run: python -m coverage run --source=income_tax -m pytest CodeCoverageTest_income_tax.py
"""
import pytest

from income_tax import refund_status, tax_due, taxable_income


def test_new_regime_taxable_income():
    assert taxable_income(1_000_000, "new", 0) == 925_000


def test_old_regime_investment_deduction_is_capped():
    assert taxable_income(500_000, "old", 200_000) == 300_000


def test_gross_income_smaller_than_deduction():
    assert taxable_income(40_000, "new", 0) == 0


def test_negative_gross_is_rejected():
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-1, "new", 0)


def test_unknown_tax_regime_is_rejected():
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(500_000, "other", 0)


def test_negative_taxable_amount_is_rejected():
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-1, 30)


def test_super_senior_exemption():
    assert tax_due(450_000, 80) == 0


def test_senior_citizen_first_slab():
    assert tax_due(550_000, 60) == 12_500


def test_non_senior_higher_slab():
    assert tax_due(800_000, 30) == 72_500


@pytest.mark.parametrize(
    ("paid", "owed", "on_time", "expected"),
    [
        (11_000, 10_000, True, "refund"),
        (11_000, 10_000, False, "refund delayed"),
        (9_000, 10_000, True, "pay balance"),
        (9_000, 10_000, False, "pay balance with penalty"),
        (10_000, 10_000, False, "settled"),
    ],
)
def test_refund_statuses(paid, owed, on_time, expected):
    assert refund_status(paid, owed, on_time) == expected
