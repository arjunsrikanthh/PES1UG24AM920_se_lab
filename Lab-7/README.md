# Software Engineering Lab - Lab 7
**Fuzzing for Input Validation Bugs**

Arjun Srikanth | PES1UG24AM920 | Section H

Assigned program: [Income Tax Parser](https://github.com/SETAPESU26/L6_L7_57_income_tax/tree/main/LAB7)

## Submission Files

| File | Description |
| --- | --- |
| [PES1UG24AM920_ARJUN_SRIKANTH_LAB7.pdf](PES1UG24AM920_ARJUN_SRIKANTH_LAB7.pdf) | Lab report with four result images and reflection |
| [income_tax_parser.py](income_tax_parser.py) | Corrected application |
| [test_income_tax_parser.py](test_income_tax_parser.py) | Hypothesis and regression tests |
| [evidence](evidence) | Test output records and images |

## Results

The original program raised exceptions for malformed or missing inputs. Fuzzing and regression tests exposed failures in the PAN, amount and tax slab parsers.

| Program | Passed | Failed |
| --- | ---: | ---: |
| Original | 10 | 19 |
| Corrected | 29 | 0 |

## Commands

```sh
python -m pip install -r requirements.txt
python income_tax_parser.py
python -m pytest -q test_income_tax_parser.py
```

Invalid amount and tax slab inputs return `None`. Invalid PAN input types return an empty string. Test logs are provided with the result images.
