# Lab 7 — Fuzzing for Input Validation Bugs

**Student:** Arjun Srikanth · **SRN:** PES1UG24AM920 · **Section:** H

**Assigned starter:** https://github.com/SETAPESU26/L6_L7_57_income_tax (LAB7).

## Required submission

| File | Purpose |
| --- | --- |
| [income_tax_parser.py](income_tax_parser.py) | Hardened PAN, rupee amount, and tax slab parsers |
| [test_income_tax_parser.py](test_income_tax_parser.py) | Completed Hypothesis tests and deterministic regression tests |
| [PES1UG24AM920_ARJUN_SRIKANTH_LAB7.pdf](PES1UG24AM920_ARJUN_SRIKANTH_LAB7.pdf) | Screenshots SS1–SS4 and three reflection answers |
| [evidence/](evidence/) | Original terminal logs, screenshots, and cropped display preview |

## Verified before-and-after results

- Faculty starter with invalid rupee input: **ValueError and abnormal exit**.
- Completed test suite against the faculty starter: **19 failed, 10 passed**.
- Corrected application with the same invalid input: **no crash**, explicit invalid-input messages.
- Completed test suite against the corrected module: **29 passed**.

### What changed

- `clean_pan`: non-strings return an empty string; all whitespace is removed before uppercasing.
- `parse_amount`: accepts standard digits, western/Indian comma grouping, and Rs / Rs. / ₹ prefixes. Rejects malformed or excessive input with `None` instead of throwing.
- `parse_tax_slab`: safely parses LOW-HIGH:RATE; rejects malformed strings, reversed bounds, or rates outside 0–100 with `None`.
- The CLI now reports invalid amounts/slabs without terminating.

## Reproduce

```bash
python -m pip install -r requirements.txt
python -m pytest -q test_income_tax_parser.py
printf 'abcde 1234f\nnot money\ninvalid slab\n' | python income_tax_parser.py
```

The four PNG files are legible renders of captured terminal output, **not native screenshots**. Full command outputs accompany them as raw text; the SS2 preview is cropped to keep failures readable in the PDF.

**Faculty handout:** Lab 7 Fuzzing for Input Validation Bugs, Section H.
