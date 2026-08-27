# Use-Case Flow Specification — UC-01: Ingest Incident Alert

**Student**: Arjun Srikanth (PES1UG24AM920)  
**Problem Statement**: #48 — Incident Escalation & On-Call Rotation Engine  

---

## Use Case: Ingest Incident Alert & Notify On-Call Engineer

| Field | Details |
|-------|---------|
| **Use Case ID** | UC-01 |
| **Use Case Name** | Ingest Incident Alert |
| **Primary Actor** | Monitoring System (external) |
| **Secondary Actors** | On-Call Engineer, Incident Commander |
| **Description** | The system receives an incident alert from an external monitoring tool, identifies the currently active on-call engineer from the rotation schedule, and dispatches notifications through the configured escalation channels. If the alert is not acknowledged within the defined timeout, it is escalated to the next tier. |

---

### Preconditions
1. At least one on-call rotation schedule is active with engineers assigned.
2. An escalation policy with at least one tier is configured for the relevant service/team.
3. The monitoring system integration (webhook endpoint) is active and authenticated.

### Postconditions
1. The incident is recorded in the system with a unique Incident ID, severity, and timestamp.
2. The on-call engineer has been notified via the configured channels (phone/SMS/email/webhook).
3. The incident status is updated to either **"Acknowledged"** or **"Escalated"** depending on the engineer's response.

---

### Main Success Scenario

| Step | Actor | Action |
|------|-------|--------|
| 1 | Monitoring System | Sends an incident alert payload (severity, service name, description) to the system's webhook endpoint. |
| 2 | System | Validates the alert payload format and authenticates the source. |
| 3 | System | Creates a new incident record with a unique ID, timestamps the event, and classifies severity (P1–P4). |
| 4 | System | Queries the active on-call rotation schedule to identify the Tier-1 on-call engineer for the affected service. |
| 5 | System | Retrieves the escalation policy for the service and determines the notification channels and timeout for Tier-1. |
| 6 | System | Dispatches notifications to the Tier-1 on-call engineer via configured channels (e.g., phone call + SMS + email) within 3 seconds. |
| 7 | On-Call Engineer | Receives the notification and acknowledges the incident (via dashboard click, SMS reply "ACK", or phone keypress "1"). |
| 8 | System | Records the acknowledgement timestamp, updates incident status to **"Acknowledged"**, and stops the escalation timer. |
| 9 | System | Displays the incident on the On-Call Engineer's dashboard with full alert details for investigation. |
| 10 | — | Use case ends successfully. |

---

### Alternate Flow — Acknowledgement Timeout & Escalation

| Step | Actor | Action |
|------|-------|--------|
| 7a | System | The Tier-1 escalation timeout (5 minutes) expires without acknowledgement from the on-call engineer. |
| 7a.1 | System | Marks the incident as **"Escalated — Tier 2"** and logs the timeout event. |
| 7a.2 | System | Queries the escalation policy for Tier-2 and identifies the secondary on-call engineer. |
| 7a.3 | System | Dispatches notifications to the Tier-2 engineer via configured channels. |
| 7a.4 | System | Simultaneously notifies the Incident Commander that a Tier-1 escalation timeout has occurred. |
| 7a.5 | On-Call Engineer (Tier-2) | Receives the notification and acknowledges the incident. |
| 7a.6 | System | Records acknowledgement, updates status to **"Acknowledged (Tier-2)"**, and stops further escalation. Flow resumes at Step 9. |
| 7a.5a | System | If Tier-2 also times out, the system notifies the Incident Commander directly with a **"Critical — All Tiers Exhausted"** alert for manual intervention. |

---
