# Lab 5 — Reflection

The faculty handout requests reflection answers but does not include four explicit numbered questions. These prompts are derived from the stated learning outcomes rather than presented as quotations.

**1. What did the tools contribute?** Pylint identified maintainability and correctness patterns, Flake8 highlighted style and unused code, and Bandit flagged unsafe Python constructs. Their different focuses helped identify more issues than any single tool.

**2. Which findings were most important?** The medium-severity unsafe `eval()` was unnecessary in a ticket tracker. A bare exception suppressed genuine errors. Shared mutable defaults could leak state between calls, and missing-ticket access could crash the application.

**3. How did the corrections improve the program?** Ticket creation, assignment, status updates, searching, closing and JSON persistence remain operational. Resource handling uses context managers, absent IDs are handled gracefully, and the code is easier to read. A `closeTicket` compatibility alias preserves the original interface.

**4. How were the corrections verified, and what are the limits of static analysis?** The same three scanners were run on the original and corrected files. Pylint improved from 5.00/10 to 9.71/10, Bandit issues decreased from two to zero, and Flake8 findings decreased from 12 to zero. Seven regression tests also passed in the earlier verification run. Static analysis cannot prove all behaviors or the absence of all security vulnerabilities.
