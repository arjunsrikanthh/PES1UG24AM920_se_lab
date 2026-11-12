"""Lab 6: exercise both outcomes of every decision in income_tax.py."""
import pytest

from income_tax import refund_status, tax_due, taxable_income


@pytest.mark.parametrize(
    ("gross", "regime", "investments", "expected"),
    [
        (1_000_000, "new", 0, 925_000),
        (75_000, "new", 0, 0),
        (74_999, "new", 0, 0),
        (500_000, "old", 0, 450_000),
        (500_000, "old", 150_000, 300_000),
        (500_000, "old", 150_001, 300_000),
    ],
)
def test_taxable_income_branches(gross, regime, investments, expected):
    assert taxable_income(gross, regime, investments) == expected


@pytest.mark.parametrize(
    ("gross", "regime", "message"),
    [(-1, "new", "invalid income"), (10_000, "other", "unknown regime")],
)
def test_taxable_income_errors(gross, regime, message):
    with pytest.raises(ValueError, match=message):
        taxable_income(gross, regime, 0)


@pytest.mark.parametrize(
    ("taxable", "age", "expected"),
    [
        (250_000, 30, 0),
        (250_001, 30, 0),
        (500_000, 30, 12_500),
        (500_001, 30, 12_500),
        (800_000, 30, 72_500),
        (300_000, 60, 0),
        (550_000, 60, 12_500),
        (500_000, 80, 0),
        (750_000, 80, 12_500),
        (800_000, 80, 22_500),
    ],
)
def test_tax_due_branches_and_boundaries(taxable, age, expected):
    assert tax_due(taxable, age) == expected


def test_tax_due_rejects_negative_input():
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-1, 30)


@pytest.mark.parametrize(
    ("paid", "owed", "filed", "status"),
    [
        (20_000, 10_000, True, "refund"),
        (20_000, 10_000, False, "refund delayed"),
        (9_999, 10_000, True, "pay balance"),
        (9_999, 10_000, False, "pay balance with penalty"),
        (10_000, 10_000, True, "settled"),
        (10_000, 10_000, False, "settled"),
    ],
)
def test_refund_status_branches(paid, owed, filed, status):
    assert refund_status(paid, owed, filed) == status
