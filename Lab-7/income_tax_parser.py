"""Validated parsers for PAN, rupee amounts, and income-tax slab descriptions.

The functions do not throw on unexpected inputs. Bad PAN values normalize to
an empty string; bad amount/slab values return None to distinguish them from
valid zeros.
"""

import re


_AMOUNT_RE = re.compile(
    r"(?:[0-9]+|[0-9]{1,3}(?:,[0-9]{3})+|[0-9]{1,3}(?:,[0-9]{2})+,[0-9]{3})"
)
_SLAB_RE = re.compile(
    r"\s*([0-9]{1,15})\s*-\s*([0-9]{1,15})\s*:\s*([0-9]{1,3})\s*"
)


def clean_pan(pan):
    """Remove whitespace and uppercase a PAN; return '' for non-string input.

    This helper normalizes text. It does not validate PAN letter/digit structure.
    """
    if not isinstance(pan, str):
        return ""
    return "".join(pan.split()).upper()


def parse_amount(text):
    """Return a nonnegative rupee amount, or None for malformed input.

    Supports plain digits, western/Indian comma grouping, and optional
    'Rs', 'Rs.', or '₹' prefixes. A length bound rejects extremely large inputs.
    """
    if not isinstance(text, str) or len(text) > 128:
        return None

    amount_text = re.sub(
        r"^(?:rs\.?\s*|₹\s*)", "", text.strip(), count=1, flags=re.IGNORECASE
    ).strip()
    if _AMOUNT_RE.fullmatch(amount_text) is None:
        return None

    digits = amount_text.replace(",", "")
    if len(digits) > 15:
        return None
    return int(digits)


def parse_tax_slab(line):
    """Parse 'LOW-HIGH:RATE' into a tuple, or None for an invalid slab.

    Limits must be nonnegative, ascending, and the rate must be 0 through 100.
    """
    if not isinstance(line, str) or len(line) > 128:
        return None

    match = _SLAB_RE.fullmatch(line)
    if match is None:
        return None
    low, high, rate = map(int, match.groups())
    if low > high or rate > 100:
        return None
    return low, high, rate


def main():
    """Demonstrate graceful handling of malformed console input."""
    print("==== Running clean_pan ====")
    value = input("Enter a PAN (e.g. abcde 1234f): ")
    print("Cleaned PAN:", clean_pan(value))

    print("\n==== Running parse_amount ====")
    value = input("Enter an amount (e.g. Rs 12,50,000): ")
    parsed_amount = parse_amount(value)
    print(
        "Amount in rupees:",
        parsed_amount if parsed_amount is not None else "Invalid amount",
    )

    print("\n==== Running parse_tax_slab ====")
    value = input(
        "Enter a tax slab as LOW-HIGH:RATE (e.g. 250000-500000:5): "
    )
    parsed_slab = parse_tax_slab(value)
    print(
        "Tax slab (low, high, rate):",
        parsed_slab if parsed_slab is not None else "Invalid tax slab",
    )


if __name__ == "__main__":
    main()
