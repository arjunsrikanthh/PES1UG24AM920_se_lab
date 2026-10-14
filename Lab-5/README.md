# Lab 5 — CI/CD and GitHub Workflow

**Student:** Arjun Srikanth · **SRN:** PES1UG24AM920 · **Section:** H
**Problem Statement 48:** Incident Escalation & On-Call Rotation Engine

## Objective

Build a small, testable Python feature from the assigned project and apply the course's
Git, unit testing, code coverage, lint, formatting, security, and GitHub Actions guidance.
The source is intentionally a deterministic domain prototype; it does **not** send real SMS,
expose an authenticated webhook, or provide 99.9% uptime, TLS, encryption at rest or deployment.
Those are requirements for the larger project, not capabilities of this lab demonstration.

## Scope and traceability

| Reference | Implemented part | Evidence |
| --- | --- | --- |
| FR-001 | Alert ingestion, Tier 1 notification, 5-min timeout and Tier 2 escalation | `engine/core.py`, `tests/test_engine.py` |
| FR-002 | Configurable tier timeout/engineer policy supplied at creation | `Tier`, `IncidentEngine` |
| FR-003 | Acknowledge and resolve through API methods (not SMS/web) | `acknowledge`, `resolve` |
| FR-005 | Structured postmortem placeholder on resolution | `postmortem` |
| NFR-001/002 | Not claimed; transport, performance, availability and encryption remain out of scope | Limitations above |

## Setup and execution

Requires Python 3.12+.

```bash
cd Lab-5
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m engine.demo
python -m pytest tests -v --cov=engine --cov-fail-under=80 --cov-report=term-missing
python -m ruff check engine tests
python -m black --check engine tests
python -m bandit -r engine -q
```

A dependency-free quick check also works: `python3 -m unittest discover -s tests -v`.

## CI/CD evidence

`../.github/workflows/se-lab5.yml` runs on changes under `Lab-5/` on push and PR. It checks
unit tests, minimum 80% coverage, Ruff, Black and Bandit, and uploads coverage XML.
The pipeline is a **CI** pipeline; deployment is deliberately not configured.
The workflow is contained inside this lab folder to keep previously accepted labs
unaltered, and lives at repository root (`../.github/workflows/se-lab5.yml`).

## Demonstrable scenarios

1. Ingest P1 alert → primary is notified immediately in the in-memory event log.
2. At exactly 5 minutes without ACK → secondary is notified.
3. At the next tier timeout → commander alert recorded as an event.
4. Only the current on-call engineer can ACK; ACK prevents further escalation.
5. Resolution produces a postmortem template containing the incident timeline.

## Limitations / follow-ups

This prototype is synchronous and in-memory (state is lost on restart), and its
notification events are not outbound messages. It does not implement rotation
calendars, multiple integration transports, or authentication. The project requirements
would need persistence, worker queues, secure ingress, and load testing before deployment.

**Course reference:** `RuthuHK/software-engineering-lab-material_sec_h/project_instruction_files`
(complete CI/CD instructions and companion troubleshooting guide). This is the
closest official project guide currently available; it is not a separately issued
numbered Lab 5 handout.
