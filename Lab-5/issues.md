# Lab 5 — Static-analysis findings

**Assigned source:** [SETAPESU26/L5_58_support-ticket-tracker/support_ticket_tracker.py](https://github.com/SETAPESU26/L5_58_support-ticket-tracker/blob/main/support_ticket_tracker.py).

Original line numbers below refer to the faculty's assigned script, **not** to the corrected version. The original source is available in the linked starter repository and the [verification artifact](https://github.com/arjunsrikanthh/PES1UG24AM920_se_lab/actions/runs/38530383574).

| Finding | Tool / original line | Explanation | Fix |
| --- | --- | --- | --- |
| Unsafe dynamic evaluation | Bandit B307 (medium), line 92 | Unnecessary `eval()` | Removed the unsafe demo branch |
| Silent exception handling | Bandit B110 (low), Flake8 E722, line 24 | Bare `except` suppressed errors | Use a safe lookup and explicit False return |
| Shared mutable default argument | Pylint W0102, line 10 | `audit_log=[]` shared across calls | Use `None`, allocate a new list |
| Unmanaged file handles | Pylint R1732, lines 46, 53 | Manual `open` and `close` | Context managers and UTF-8 encoding |
| Unhandled unknown tickets | Behavioral review, lines 30, 67, 71 | Missing IDs caused `KeyError` | Guard accesses and return an explicit result |
| Unused imports and local variable | Flake8 F401/F841, lines 4–5, 84 | `sys`, `random` and `count` unused | Removed unused names |
| Non-idiomatic None comparison | Flake8 E711, line 37 | Uses `!= None` | Identity-aware filtering |
| Long lines | Flake8 E501, multiple lines | Violates PEP 8 formatting | Reflowed signature, conditionals, calls |
| Non-standard function name | Pylint C0103, line 66 | `closeTicket` is not snake_case | Added `close_ticket`, kept compatibility alias |

## Confirmed scanner results

| Scanner | Original | Corrected |
| --- | --- | --- |
| Pylint | 5.00/10 | 9.71/10 |
| Bandit | B307 medium, B110 low | No findings |
| Flake8 | 12 findings | No findings |

**Evidence:** The raw, unedited outputs from GitHub Actions are committed in `reports/before/` and `reports/after/`. The corrected Pylint score clears the faculty's **above 9.5** requirement. The remaining two Pylint notices concern the existing function's six-argument signature and were retained to preserve compatibility.
