"""Deterministic incident handling and on-call escalation logic.

All timestamps are timezone-aware UTC and are passed in explicitly to enable tests.
This is a teaching prototype, not a production paging service.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from uuid import uuid4


class Status(str, Enum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    EXHAUSTED = "exhausted"


@dataclass(frozen=True)
class Tier:
    engineer: str
    timeout_seconds: int = 300

    def __post_init__(self):
        if not self.engineer.strip() or self.timeout_seconds < 1:
            raise ValueError("Tier requires an engineer and positive timeout")


@dataclass
class Incident:
    id: str
    service: str
    severity: str
    description: str
    created_at: datetime
    tier_index: int = 0
    tier_started_at: datetime | None = None
    status: Status = Status.OPEN
    acknowledged_by: str | None = None
    resolved_at: datetime | None = None
    timeline: list[str] = field(default_factory=list)


class IncidentEngine:
    def __init__(self, policies: dict[str, list[Tier]]):
        if not policies or any(not tiers for tiers in policies.values()):
            raise ValueError("Each service must have an escalation policy")
        self.policies = policies
        self.incidents: dict[str, Incident] = {}
        self.notifications: list[tuple[str, str, str]] = []

    @staticmethod
    def _check_time(now: datetime) -> None:
        if now.tzinfo is None or now.utcoffset() is None:
            raise ValueError("Use timezone-aware timestamps")

    def _notify(self, incident: Incident) -> None:
        tiers = self.policies[incident.service]
        engineer = tiers[incident.tier_index].engineer
        self.notifications.append((incident.id, engineer, incident.severity))
        incident.timeline.append(f"tier {incident.tier_index + 1}: notify {engineer}")

    def ingest(self, service: str, severity: str, description: str, now: datetime) -> Incident:
        self._check_time(now)
        if service not in self.policies:
            raise ValueError("No on-call policy for service")
        if severity not in {"P1", "P2", "P3", "P4"} or not description.strip():
            raise ValueError("Invalid alert severity or description")
        incident = Incident(str(uuid4()), service, severity, description, now, tier_started_at=now)
        incident.timeline.append("alert ingested")
        self.incidents[incident.id] = incident
        self._notify(incident)
        return incident

    def advance(self, incident_id: str, now: datetime) -> Status:
        self._check_time(now)
        incident = self.incidents[incident_id]
        if incident.status != Status.OPEN:
            return incident.status
        if now < incident.tier_started_at:
            raise ValueError("Cannot move time backwards")
        tiers = self.policies[incident.service]
        # Account for multiple expired tiers, even when a scheduler runs late.
        while incident.status == Status.OPEN:
            deadline = incident.tier_started_at + timedelta(
                seconds=tiers[incident.tier_index].timeout_seconds
            )
            if now < deadline:
                break
            incident.timeline.append(f"tier {incident.tier_index + 1}: timeout")
            if incident.tier_index + 1 == len(tiers):
                incident.status = Status.EXHAUSTED
                incident.timeline.append("all tiers exhausted: notify incident commander")
            else:
                incident.tier_index += 1
                incident.tier_started_at = deadline
                self._notify(incident)
        return incident.status

    def acknowledge(self, incident_id: str, engineer: str, now: datetime) -> None:
        self._check_time(now)
        incident = self.incidents[incident_id]
        self.advance(incident_id, now)
        if incident.status != Status.OPEN:
            raise ValueError("Incident is not awaiting acknowledgment")
        if engineer != self.policies[incident.service][incident.tier_index].engineer:
            raise PermissionError("Only the active on-call engineer may acknowledge")
        incident.status = Status.ACKNOWLEDGED
        incident.acknowledged_by = engineer
        incident.timeline.append(f"acknowledged by {engineer}")

    def resolve(self, incident_id: str, engineer: str, now: datetime) -> None:
        self._check_time(now)
        incident = self.incidents[incident_id]
        if incident.status != Status.ACKNOWLEDGED or incident.acknowledged_by != engineer:
            raise PermissionError("Only the acknowledging engineer may resolve")
        if now < incident.created_at:
            raise ValueError("Resolution cannot predate creation")
        incident.status = Status.RESOLVED
        incident.resolved_at = now
        incident.timeline.append(f"resolved by {engineer}")

    def postmortem(self, incident_id: str) -> dict:
        incident = self.incidents[incident_id]
        if incident.status != Status.RESOLVED:
            raise ValueError("Resolve the incident before generating a postmortem")
        return {
            "incident_id": incident.id,
            "service": incident.service,
            "severity": incident.severity,
            "description": incident.description,
            "acknowledged_by": incident.acknowledged_by,
            "timeline": list(incident.timeline),
            "root_cause": "TODO",
            "action_items": [],
        }
