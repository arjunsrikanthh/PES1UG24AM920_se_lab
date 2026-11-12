# Software Engineering Lab - Lab 7
**Fuzzing for Input Validation Bugs**

Arjun Srikanth | PES1UG24AM920 | Section H

Assigned program: [Income Tax Parser](https://github.com/SETAPESU26/L6_L7_57_income_tax/tree/main/LAB7)

## Submission Files

| File | Description |
| --- | --- |
| [PES1UG24AM920.pdf](PES1UG24AM920.pdf) | Lab report with SS1-SS4, a focused failure traceback and reflection |
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

## Evidence and reproducibility

The report and `evidence/` contain genuine macOS Terminal.app captures made on 12 November 2026. The images replace the previous rendered terminal illustrations. PNG hashes, raw-capture hashes and capture times are recorded in `evidence/capture_manifest.json`; untouched raw captures remain in the local working folder.

The faculty original is preserved in `evidence/original/income_tax_parser.py`. To rerun the unchanged test suite against it:

```sh
cd evidence/original
python -m pytest --import-mode=importlib ../../test_income_tax_parser.py --hypothesis-seed=920
cd ../..
python -m pytest -q test_income_tax_parser.py --hypothesis-seed=920
```

The expected original result is 19 failed and 10 passed (exit code 1); the corrected result is 29 passed (exit code 0). `original_full_test_run.txt` preserves a separate full verification run with tracebacks. `@example(None)` is an explicit regression example; the report does not attribute it to random discovery.

The starter requests `SRN_NAME_LAB7.pdf`. This package uses the student’s standing filename convention, `PES1UG24AM920.pdf`. The current course handout does not list the three reflection questions referenced in the starter README; the prior report’s three prompts are retained and their answers revised to match the verified run.
