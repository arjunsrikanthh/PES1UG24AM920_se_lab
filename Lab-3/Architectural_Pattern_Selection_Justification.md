# Software Engineering Lab (SE Lab) — Lab 3 Report
## Component Modelling & Architectural Pattern Selection

**Department of Computer Science & Engineering**  
**PES University, Bengaluru**  

* **Student Name**: Arjun Srikanth  
* **SRN**: PES1UG24AM920  
* **Section**: CSE Section H  
* **Assigned Problem Statement**: #48 — Incident Escalation & On-Call Rotation Engine  
* **Handout Example Scenario**: Self-Service Coffee Kiosk System  
* **GitHub Repository**: [github.com/arjunsrikanthh/PES1UG24AM920_se_lab](https://github.com/arjunsrikanthh/PES1UG24AM920_se_lab)  

---

## 1. Comparative Analysis of Architectural Styles

Before selecting an architectural pattern, three candidate styles were evaluated against the functional and non-functional requirements of high-availability enterprise and embedded systems:

| Architectural Style | Structural Organization | Key Advantages (Pros) | Key Limitations (Cons) | Scenario Fit Evaluation |
| :--- | :--- | :--- | :--- | :--- |
| **Layered (N-Tier) Architecture** | Organized into horizontal layers (Presentation, Business/Application Logic, Persistence/Data). Communication flows unidirectionally downward. | • High separation of concerns.<br>• Simple mental model and straightforward testing.<br>• Low operational complexity. | • Performance overhead (sinkhole anti-pattern across layers).<br>• Monolithic deployment boundary.<br>• Tight coupling makes independent service scaling impossible. | Excellent for standalone, localized systems with clear sequential workflows (e.g., self-service hardware kiosks), but unsuitable for distributed, event-driven alerting. |
| **Microservices Architecture** | Loosely coupled, fine-grained autonomous services organized around distinct business capabilities, communicating via lightweight protocols (gRPC, REST, Message Brokers). | • Fault isolation prevents cascading outages.<br>• Independent component scaling (e.g., alert ingestion vs notification).<br>• Technology diversity and autonomous deployments. | • High operational and orchestration overhead.<br>• Network latency and eventual consistency complexities.<br>• Complex distributed tracing and telemetry required. | Best suited for Problem Statement #48 (DevOps Alerting Engine), where high ingestion bursts and strict 99.9% availability demand decoupled fault domains. |
| **Client-Server Architecture** | Centralized server nodes providing data and computation to multiple lightweight or rich client nodes over standard network protocols. | • Centralized state governance and security enforcement.<br>• Simplified updates on the server side.<br>• Straightforward client implementation. | • Central server is a Single Point of Failure (SPOF).<br>• Scalability bottleneck under heavy load.<br>• Network partition halts client operation unless offline caching exists. | Inadequate for fault-tolerant incident alerting where no single point of failure can be tolerated; sub-optimal for kiosks requiring localized hardware control. |

---

## 2. Deliverable A: Assigned Scenario (Problem Statement #48)
### Incident Escalation & On-Call Rotation Engine

### 2.1 Architecture Selection Statement
> **"We chose an Event-Driven Microservices Architecture for the Incident Escalation & On-Call Rotation Engine."**

### 2.2 Formal Justification

* **Architectural Choice**:
  An **Event-Driven Microservices Architecture** deployed as independent containerized modules communicating asynchronously via gRPC and high-throughput message queues (Kafka / RabbitMQ), backed by isolated transactional and state stores.

* **Two Specific Scenario-Related Reasons**:
  1. **Decoupled Fault Domains During Cascading Outages**: In major production outages (P1 incidents), monitoring platforms emit huge bursts of alerts ( $\ge 500$ alerts/second). If external telecom providers (Twilio SMS/Voice) experience throttling or high latency, the `Multi-Channel Notification Service` will buffer requests without blocking the `Webhook Ingestion Gateway` or delaying the `Escalation & Rules Engine`. A crash in one notification channel does not impair alert ingestion.
  2. **Independent Scaling Profiles for Ingestion vs. Scheduling**: Alert ingestion has highly volatile, bursty workloads, whereas shift rotation lookups and policy configuration have low-frequency, read-heavy workloads. Microservices allow horizontal scaling of only the Ingestion and Escalation nodes dynamically, satisfying **NFR-001** (initiating alert dispatch within 3 seconds) without wasting cluster compute.

* **Security Advantage**:
  **Fine-Grained Zero-Trust Network Architecture & Secrets Isolation**: The system separates external-facing components (`Webhook Ingestion Gateway`, `Triage Webhook`) from internal core business logic. All ingress payloads are cryptographically validated using HMAC-SHA256 signatures before entering the internal network. Communication across microservices occurs over mutual TLS (mTLS), and sensitive engineer contact records (phone numbers, personal emails) are restricted strictly to the `Multi-Channel Notification Service` with AES-256 field-level encryption, fulfilling **NFR-002**.

* **Performance Benefit**:
  **Sub-Second Asynchronous Ingestion & Event-Driven Escalation**: By utilizing asynchronous event queues between the `Webhook Ingestion Gateway` and the `Escalation & Rules Engine`, alert ingestion acknowledges external monitoring hooks within $< 100\text{ ms}$, while dispatch pipelines concurrently trigger secondary notifications and SLA timers. This ensures the system comfortably beats the 3-second SLA threshold mandated in **NFR-001**.

---

### 2.3 Component & Interface Specification (Problem Statement #48)

| Component Name | Stereotype | Primary Responsibility | Provided Interfaces (Ball) | Required Interfaces (Socket) | Interaction Protocols |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Webhook Ingestion Gateway** | `<<component>>` | Ingests monitoring alerts from Prometheus/Datadog, validates HMAC tokens, deduplicates bursts, and formats event envelopes. | `IAlertWebhook` | `IEscalationControl` | HTTPS POST, JSON, HMAC-SHA256 |
| **Rotation & Schedule Manager** | `<<component>>` | Manages recurring 24/7 engineer shift rotations, temporary overrides, holiday substitutions, and timezone-aware lookups. | `IScheduleLookup`, `IRotationConfig` | `ISqlPersistence` | gRPC, REST / HTTPS, SQL (TLS) |
| **Escalation & Rules Engine** | `<<component>>` | Evaluates multi-tier escalation ladders, runs the 5-minute SLA timer, and transitions incidents through Tier-1, Tier-2, and IC Exhaustion. | `IEscalationControl` | `IScheduleLookup`, `INotifyDispatch`, `ISqlPersistence` | Event Bus, gRPC, Redis Pub/Sub |
| **Multi-Channel Notification Service** | `<<component>>` | Dispatches urgent notifications across phone call (IVR), SMS, email, and mobile push within 3 seconds. | `INotifyDispatch` | `ITelecomGateway` | Twilio Voice/SMS API, SendGrid SMTP |
| **Triage & Incident Lifecycle Manager** | `<<component>>` | Processes engineer triage actions (ACK, Resolve, Reassign) from Web dashboard, SMS reply, and phone keypress, halting SLA timers. | `IDashboardAPI`, `IRemoteTriageWebhook` | `IEscalationControl`, `IPostMortemTrigger` | GraphQL, Twilio Webhook, Internal RPC |
| **Post-Mortem & Telemetry Store** | `<<component>>` | Aggregates incident timeline timestamps, MTTR metrics, and auto-generates structured post-mortem templates upon incident closure. | `IPostMortemTrigger` | `ISqlPersistence` | Internal Event Bus, PostgreSQL |

---

## 3. Deliverable B: Handout Scenario (Self-Service Coffee Kiosk System)
### Self-Service Coffee Kiosk in a Busy Café

### 3.1 Architecture Selection Statement
> **"We chose a Layered Component-Based Architecture for the Self-Service Coffee Kiosk System."**

### 3.2 Formal Justification

* **Architectural Choice**:
  A **Layered Component-Based Architecture** organized into Presentation (Touchscreen UI), Business Logic (Order Manager & Menu Catalog), and Hardware Abstraction / External Integration (Payment Service & Printer Controller), running on an embedded local runtime.

* **Two Specific Scenario-Related Reasons**:
  1. **Strict Hardware-Software Locality**: A coffee kiosk is a physically integrated terminal directly attached to dedicated hardware peripherals (touchscreen, EMV chip card reader, and ESC/POS thermal printer). A layered component architecture keeps hardware abstraction components locally resident, eliminating remote network latency and network partition risks when processing physical inputs and issuing serial print jobs.
  2. **Atomic Sequential Workflow Execution**: The coffee ordering lifecycle is strictly sequential: Select Beverage (Espresso/Americano/Latte) $\rightarrow$ Select Size (Small/Large) $\rightarrow$ Authorize Card $\rightarrow$ Print Receipt. The `Order Manager Component` orchestrates this flow with deterministic state transitions without the operational overhead, eventual consistency issues, or distributed transaction complexity of microservices.

* **Security Advantage**:
  **PCI-DSS Scope Minimization via Hardware Isolation**: The `Payment Service Component` acts as a secure, sandboxed subsystem interfacing directly with the EMV PIN-pad hardware via encrypted serial protocol (`ICardReaderDriver`) and communicating outward to the acquiring bank gateway over TLS 1.3 (`IBankGatewayAPI`). Raw card numbers and PIN blocks never enter the `Order Manager` or UI memory space, drastically reducing the PCI-DSS compliance scope of the kiosk software.

* **Performance Benefit**:
  **Zero-Latency Touch Interaction & Instant Receipt Printing**: The `Menu & Pricing Catalog` is cached in local memory, ensuring instantaneous response times ($< 16\text{ ms}$) on the touchscreen when customers browse coffee options. Furthermore, the `Printer Controller Component` directly buffers binary ESC/POS bytecode over USB/Serial, enabling receipt dispensing within $< 1$ second of bank payment authorization.

---

### 3.3 Component & Interface Specification (Coffee Kiosk System)

| Component Name | Stereotype | Primary Responsibility | Provided Interfaces (Ball) | Required Interfaces (Socket) | Protocol / Medium |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Touchscreen Kiosk UI** | `<<component>>` | Renders high-contrast interactive ordering screens, coffee selection, size modifiers, and payment prompts. | — | `IMenuQuery`, `IOrderPlacement` | Local GUI Event Bus, Touch API |
| **Order Manager Component** *(Given)* | `<<component>>` | Coordinates order state transitions, calculates item totals with tax, orchestrates payment, and triggers printing. | `IOrderPlacement` | `IMenuQuery`, `IPaymentProcess`, `IPrintJob` | Internal IPC / Shared Memory API |
| **Payment Service Component** *(Given)* | `<<component>>` | Interfaces with POS card terminal, encrypts cardholder data, executes authorization with bank gateway. | `IPaymentProcess` | `ICardReaderDriver`, `IBankGatewayAPI` | Serial EMV Driver, HTTPS TLS 1.3 |
| **Menu & Pricing Catalog** | `<<component>>` | Stores coffee types (Espresso, Latte, Americano), sizing options (Small, Large), and pricing rules. | `IMenuQuery` | `ILocalDataQuery` | In-Memory / SQLite Query |
| **Printer Controller Component** | `<<component>>` | Formats receipt text, timestamp, order ID, payment auth code, and issues ESC/POS print commands. | `IPrintJob` | `IESCPOSDriver` | USB / RS-232 Serial Byte Stream |

---

## 4. Verification & UML Compliance Checklist

- [x] **At least 5 components included**:
  - Problem Statement #48: **6 components** modeled (`IngestGW`, `RotaMgr`, `EscalateEngine`, `NotifySvc`, `TriageMgr`, `PostMortemSvc`).
  - Coffee Kiosk System: **5 components** modeled (`KioskUI`, `OrderMgr`, `PaymentSvc`, `MenuCatalog`, `PrinterCtrl`).
- [x] **At least 4 interfaces shown**:
  - Problem Statement #48: **8 interfaces** (`IAlertWebhook`, `IScheduleLookup`, `IRotationConfig`, `INotifyDispatch`, `IEscalationControl`, `IDashboardAPI`, `IRemoteTriageWebhook`, `IPostMortemTrigger`).
  - Coffee Kiosk System: **8 interfaces** (`IOrderPlacement`, `IMenuQuery`, `IPaymentProcess`, `IPrintJob`, `ICardReaderDriver`, `IBankGatewayAPI`, `IESCPOSDriver`, `ILocalDataQuery`).
- [x] **Standard UML 2.5 notation**: Ball (provided) and socket (required) symbols, explicit ports, and `<<component>>` stereotypes.
- [x] **Deliverable Formats**: PlantUML source (`.puml`), high-resolution PNG (`.png`), vector PDF (`.pdf`), Word document (`.docx`), and PDF submission report (`.pdf`).
