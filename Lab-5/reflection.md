# Lab 5 — Reflection

The handout requests reflections but does not include four literal reflection questions. These four student-formulated prompts follow its learning outcomes.

**1. What does each tool contribute?** Pylint reviews maintainability and Python correctness patterns; Flake8 checks style and some errors; Bandit identifies insecure patterns. Together they cover different concerns.

**2. What issues were highest priority?** The unsafe dynamic evaluation was Bandit's medium-severity finding. The suppressed exception hid failures, and a mutable default list could carry state between independent calls.

**3. What improved after fixing the program?** The program retains ticket creation, assignment, updating, searching, closing and JSON persistence. Missing IDs now have explicit behavior and file streams use context managers.

**4. How did you verify results?** Preliminary static scans recorded Pylint increasing from 5.00 to 9.71, with no remaining Bandit/Flake8 findings. Seven additional Python behavioral tests passed in an isolated environment. GitHub Actions independently reruns Pylint, Bandit and Flake8 on the final committed code and uploads full reports. Static analysis alone cannot guarantee complete security.
