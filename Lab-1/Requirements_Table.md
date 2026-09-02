# Requirements Table — Problem Statement #48

## Incident Escalation & On-Call Rotation Engine

**Student**: Arjun Srikanth (PES1UG24AM920)  
**Problem Statement**: #48 — Developer Tools & IT Operations  

---

## System Overview

A DevOps on-call management system organizing team shift rotations, routing inbound monitoring alerts through multi-tiered phone/SMS escalation ladders, and tracking incident post-mortems.

---

## Functional Requirements

| Req ID | Type | Description | Priority | Acceptance Criteria | Rationale |
|--------|------|-------------|----------|---------------------|-----------|
| FR-001 | Functional | The system shall ingest incident alerts, identify the active on-call engineer from the rotation schedule, and escalate to the secondary engineer if unacknowledged within 5 minutes. | High | **Pass:** Escalation step triggered upon timeout. **Fail:** Unacknowledged P1 incident drops without escalation. | Core alerting and escalation functionality ensures that no critical incident goes unattended, directly reducing mean time to respond (MTTR). |
| FR-002 | Functional | The system shall allow the Incident Commander to define and modify multi-tiered escalation policies specifying notification channels (phone, SMS, email, webhook) and timeout durations per tier. | High | **Pass:** Updated escalation policy is reflected in the next alert routing cycle. **Fail:** Old policy is still used after the Incident Commander saves changes. | Customisable escalation ladders enable teams to adapt notification workflows to varying team sizes, SLA requirements, and incident severity levels. |
| FR-003 | Functional | The system shall enable on-call engineers to acknowledge, reassign, or resolve incidents through the web dashboard, SMS reply, or phone keypress. | High | **Pass:** Status change (acknowledge/reassign/resolve) is reflected within 10 seconds across all channels. **Fail:** Incident status remains "Open" after a valid acknowledgement action. | Multi-channel acknowledgement reduces MTTR by allowing engineers to respond from any device, even when away from a workstation. |
| FR-004 | Functional | The system shall support creation and management of recurring on-call rotation schedules with configurable shift durations, manual overrides, and holiday substitutions. | Medium | **Pass:** The correct on-call engineer is identified for any queried timestamp, including during override windows. **Fail:** Wrong engineer is assigned during an override or holiday substitution period. | Automated rotation scheduling eliminates manual assignment errors and ensures uninterrupted 24/7 incident coverage. |
| FR-005 | Functional | The system shall generate a post-mortem report template upon incident resolution, capturing an event timeline, root-cause fields, and action items, and store it linked to the incident record. | Medium | **Pass:** Post-mortem template is auto-populated with incident timeline data and linked to the resolved incident. **Fail:** Template is missing, empty, or unlinked to the incident. | Structured post-mortems drive continuous improvement, knowledge sharing, and reduction of repeat incidents. |

## Non-Functional Requirements

| Req ID | Type | Description | Priority | Acceptance Criteria | Rationale |
|--------|------|-------------|----------|---------------------|-----------|
| NFR-001 | Non-Functional (Performance & Security) | Alert dispatch via webhook, SMS, and email must initiate within 3 seconds of alert ingestion. | High | **Pass:** Benchmarking tests confirm target latency and security standards under simulated peak load (≥ 500 concurrent alerts). **Fail:** Dispatch latency exceeds 3 seconds or security audit reveals unencrypted dispatch channels. | Rapid notification is critical for SLA compliance during P1/P2 incidents; delayed alerts directly increase incident impact. |
| NFR-002 | Non-Functional (Availability & Security) | The system shall maintain 99.9% uptime with automatic failover, and all data in transit and at rest shall be encrypted using TLS 1.2+ and AES-256 respectively. | High | **Pass:** Uptime logs over a 30-day period show ≥ 99.9% availability; penetration test confirms no unencrypted data paths. **Fail:** Downtime exceeds 0.1% in any 30-day window, or an unencrypted communication channel is discovered. | On-call management systems must remain available when other systems are failing; encryption protects sensitive engineer contact information and incident data. |

---
