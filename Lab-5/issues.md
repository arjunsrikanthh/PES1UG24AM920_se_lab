# Lab 5 — Static-analysis findings

Assigned starter: [SETAPESU26/L5_58_support-ticket-tracker](https://github.com/SETAPESU26/L5_58_support-ticket-tracker). The original source is preserved under `support_ticket_tracker_original.py.txt`. Line numbers refer to that file.

| Finding | Source / original line | Issue | Correction |
| --- | --- | --- | --- |
| Mutable audit default | Pylint W0102, line 10 | Shared list between calls | Use None and allocate a list |
| Bare except | Bandit B110 / Flake8 E722, lines 20–26 | All errors hidden | Safe ID lookup with explicit False |
| File handling | Pylint R1732, lines 44–54 | Handles opened without with | Context-managed UTF-8 files |
| Unsafe eval | Bandit B307 medium, line 93 | Unnecessary dynamic execution | Remove branch entirely |
| Missing ticket IDs | Manual finding, lines 30–32 and 66 | Possible KeyError | Guard access |
| Unused imports and count | Flake8 F401/F841, lines 4–5/84 | Dead code | Remove names |
| Comparing to None | Flake8 E711, line 37 | Style issue | Use identity-based conditions |
| Long lines | Flake8 E501, several lines | Unreadable expressions | Reformat to 79 columns |
| Inconsistent name | Pylint C0103, line 66 | CamelCase | Add snake_case, preserve alias |

### Evidence

Original preliminary scan: Pylint 5.00/10; Bandit B110 low and B307 medium; Flake8 12 findings. Earlier corrected preliminary scan: Pylint 9.71/10; no Bandit/Flake8 findings. Full actual scanner outputs for this published revision are generated and downloadable through the GitHub Actions workflow; summaries do not replace raw logs.
