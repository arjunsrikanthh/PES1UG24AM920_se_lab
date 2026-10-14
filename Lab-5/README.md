# Lab 5 — Static Code Analysis

**SRN:** PES1UG24AM920 · **Section:** H

**Assigned program:** [L5_58_support-ticket-tracker](https://github.com/SETAPESU26/L5_58_support-ticket-tracker) · **Faculty handout:** 14 October 2026

## Files

| File | Purpose |
| --- | --- |
| [support_ticket_tracker.py](support_ticket_tracker.py) | Cleaned Python program |
| [issues.md](issues.md) | Static-analysis issue register and fixes |
| [reflection.md](reflection.md) | Reflection answers |
| [reports/before](reports/before) | Original Pylint, Bandit and Flake8 reports |
| [reports/after](reports/after) | Corrected Pylint, Bandit and Flake8 reports |

The six report files are **actual outputs of the completed GitHub Actions run** for the original faculty starter and the corrected program. An empty `reports/after/flake8_report.txt` is expected: Flake8 found no issues.

## Reproduce

```bash
cd Lab-5
python3 -m venv venv
source venv/bin/activate
pip install pylint bandit flake8
python support_ticket_tracker.py
pylint support_ticket_tracker.py
bandit -r support_ticket_tracker.py
flake8 support_ticket_tracker.py
```

| Scanner | Before | After |
| --- | --- | --- |
| Pylint | 5.00/10 | 9.71/10 |
| Bandit | Two findings (one medium, one low) | Zero findings |
| Flake8 | 12 findings | Zero findings |

**Source history:** The three preceding Lab 5 commits document corrections by analysis category. The unmodified starter remains available through the faculty's assigned repository; it is not duplicated in this submission. The [successful verification run](https://github.com/arjunsrikanthh/PES1UG24AM920_se_lab/actions/runs/38530383574) retains the original and corrected code and scan artifact.
