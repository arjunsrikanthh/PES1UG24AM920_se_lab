# Lab 5 — Static Code Analysis

**Student SRN:** PES1UG24AM920 · **Section:** H

Assigned starter: [SETAPESU26/L5_58_support-ticket-tracker](https://github.com/SETAPESU26/L5_58_support-ticket-tracker). The faculty handout was emailed on 14 October 2026.

## Submission

- `support_ticket_tracker.py`: corrected program.
- `support_ticket_tracker_original.py.txt`: exact original starter for baseline comparison.
- `issues.md`: issue table documenting nine classes of problems.
- `reflection.md`: four reflections derived from handout learning objectives.
- `tests/test_tracker.py`: seven regression tests.
- `reports/before/README.md`, `reports/after/README.md`: preliminary results and precise location of raw CI scanner reports.

## Execute and scan

```bash
cd Lab-5
python3 -m venv venv
source venv/bin/activate
pip install pylint bandit flake8
python support_ticket_tracker.py
python -m unittest discover -s tests -v
pylint support_ticket_tracker.py
bandit -r support_ticket_tracker.py
flake8 support_ticket_tracker.py
```

### Evidence

The `SE Lab 5 static analysis` workflow under GitHub Actions runs all three scanners on **both** the unmodified starter and corrected source; it uploads six actual raw report files in one `lab5-static-analysis-before-after` artifact. It also enforces Pylint >9.5 and zero Bandit/Flake8 findings on the corrected file.

Three successive commits distinguish Pylint improvements, Flake8 findings/documentation and the Bandit security cleanup. This work was published via GitHub, without touching the student's Mac after they asked for isolation.
