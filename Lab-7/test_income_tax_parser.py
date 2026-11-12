"""Hypothesis fuzz tests for the three faculty-assigned input parsers."""
import pytest
from hypothesis import example, given, settings, strategies as st

from income_tax_parser import clean_pan, parse_amount, parse_tax_slab


@settings(max_examples=150, deadline=None)
@example(None)
@given(st.text() | st.none())
def test_clean_pan_no_crash(s):
    try:
        result = clean_pan(s)
    except Exception as exc:
        pytest.fail(f"clean_pan crashed on {s!r}: {exc!r}")
    assert isinstance(result, str)
    assert result == ("" if s is None else "".join(s.split()).upper())


@settings(max_examples=150, deadline=None)
@example(None)
@given(st.text() | st.none())
def test_parse_amount_no_crash(s):
    try:
        result = parse_amount(s)
    except Exception as exc:
        pytest.fail(f"parse_amount crashed on {s!r}: {exc!r}")
    assert result is None or (type(result) is int and result >= 0)


@settings(max_examples=150, deadline=None)
@example(None)
@given(st.text() | st.none())
def test_parse_tax_slab_no_crash(s):
    try:
        result = parse_tax_slab(s)
    except Exception as exc:
        pytest.fail(f"parse_tax_slab crashed on {s!r}: {exc!r}")
    assert result is None or (
        isinstance(result, tuple)
        and len(result) == 3
        and all(type(item) is int for item in result)
        and 0 <= result[0] <= result[1]
        and 0 <= result[2] <= 100
    )


@settings(max_examples=100, deadline=None)
@given(st.one_of(
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.binary(),
    st.lists(st.integers(), max_size=4),
    st.dictionaries(st.text(max_size=3), st.integers(), max_size=2),
    st.booleans(),
))
def test_non_string_types_never_crash(value):
    assert clean_pan(value) == ""
    assert parse_amount(value) is None
    assert parse_tax_slab(value) is None


@pytest.mark.parametrize(
    ("input_pan", "expected"),
    [
        ("abcde 1234f", "ABCDE1234F"),
        ("  abcde\t1234f \n", "ABCDE1234F"),
        ("", ""),
        (None, ""),
    ],
)
def test_clean_pan_examples(input_pan, expected):
    assert clean_pan(input_pan) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Rs 12,50,000", 1_250_000),
        ("rs. 1,234", 1234),
        ("₹ 2,50,000", 250_000),
        ("0", 0),
        ("  25  ", 25),
        ("Rs -50", None),
        ("1,2,3", None),
        ("", None),
        ("not money", None),
        (None, None),
    ],
)
def test_parse_amount_examples(value, expected):
    assert parse_amount(value) == expected


@settings(max_examples=100, deadline=None)
@given(st.integers(min_value=0, max_value=10**12))
def test_parse_amount_round_trip(amount):
    assert parse_amount(f"Rs {amount:,}") == amount


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("250000-500000:5", (250_000, 500_000, 5)),
        (" 0 - 250000 : 0 ", (0, 250_000, 0)),
        ("250000-500000:100", (250_000, 500_000, 100)),
        ("500000-250000:5", None),
        ("100-200:101", None),
        ("10-20:three", None),
        ("100 - 200", None),
        ("", None),
        (None, None),
    ],
)
def test_parse_tax_slab_examples(value, expected):
    assert parse_tax_slab(value) == expected


@settings(max_examples=100, deadline=None)
@given(
    low=st.integers(min_value=0, max_value=10**11),
    delta=st.integers(min_value=0, max_value=10**5),
    rate=st.integers(min_value=0, max_value=100),
)
def test_tax_slab_round_trip(low, delta, rate):
    assert parse_tax_slab(f"{low}-{low + delta}:{rate}") == (
        low, low + delta, rate
    )
