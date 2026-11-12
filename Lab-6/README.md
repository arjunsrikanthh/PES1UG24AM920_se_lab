# Software Engineering Lab - Lab 6
**Code and Branch Coverage Analysis**

Arjun Srikanth | PES1UG24AM920 | Section H

Assigned program: [Income Tax Calculator](https://github.com/SETAPESU26/L6_L7_57_income_tax)

## Submission Files

| File | Description |
| --- | --- |
| [PES1UG24AM920.pdf](PES1UG24AM920.pdf) | Coverage report and results |
| [income_tax.py](income_tax.py) | Original application |
| [CodeCoverageTest_income_tax.py](CodeCoverageTest_income_tax.py) | Statement coverage tests |
| [BranchCoverageTest_income_tax.py](BranchCoverageTest_income_tax.py) | Branch coverage tests |
| [evidence](evidence) | Coverage output images and test logs |

## Results

| Test suite | Passed | Coverage |
| --- | ---: | ---: |
| Statement coverage | 14 | 100% (39/39 statements) |
| Branch coverage | 25 | 100% (28/28 branches) |

## Commands

```sh
python -m pip install -r requirements.txt
python -m coverage run --source=income_tax -m pytest CodeCoverageTest_income_tax.py
python -m coverage report -m
python -m coverage run --branch --source=income_tax -m pytest BranchCoverageTest_income_tax.py
python -m coverage report -m
```

The application source is unchanged. Statement and branch test cases were added in separate commits.

## Evidence

The two result images are genuine macOS Terminal.app window captures made on 12 November 2026, replacing the previous rendered terminal illustrations. `evidence/capture_manifest.json` records capture times and image hashes. Untouched raw captures are retained in the local working folder. The report uses the serif title, identity block and numbered sections of the earlier SE submissions.
