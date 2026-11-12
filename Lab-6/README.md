# Lab 6 — Code and Branch Coverage Analysis

**Student:** Arjun Srikanth · **SRN:** PES1UG24AM920 · **Section:** H

**Assigned repository:** https://github.com/SETAPESU26/L6_L7_57_income_tax

## Deliverables

| Requirement | File |
| --- | --- |
| Unchanged starter application | income_tax.py |
| Statement coverage tests | CodeCoverageTest_income_tax.py |
| Branch coverage tests | BranchCoverageTest_income_tax.py |
| Line coverage screenshot and log | evidence/SS1_code_coverage_terminal.png and .txt |
| Branch coverage screenshot and log | evidence/SS2_branch_coverage_terminal.png and .txt |

The PNG evidence is a legible rendering of captured, unedited terminal command output. The matching .txt files provide the raw test output.

## Verified results

- **Statement coverage:** 39/39 statements, **100%**, 14 tests passed.
- **Branch coverage:** 28/28 branches, **100%**, 25 tests passed.

## Reproduction

From the Lab-6 directory, install dependencies using `python -m pip install -r requirements.txt`, then run these commands:

```bash
python -m coverage run --source=income_tax -m pytest CodeCoverageTest_income_tax.py
python -m coverage report -m
python -m coverage run --branch --source=income_tax -m pytest BranchCoverageTest_income_tax.py
python -m coverage report -m
```

The branch tests cover invalid income, both tax regimes, investment cap, deductions, age cutoffs, tax slab boundaries, and all refund/balance outcomes. The application is kept unchanged to make coverage comparisons meaningful. The two stages are separate Git commits.
