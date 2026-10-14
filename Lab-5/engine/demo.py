"""Run with: python -m engine.demo"""

from datetime import UTC, datetime, timedelta

from engine.core import IncidentEngine, Tier


def main():
    engine = IncidentEngine({"payments": [Tier("primary"), Tier("secondary", 120)]})
    start = datetime.now(UTC)
    incident = engine.ingest("payments", "P1", "Elevated error rate", start)
    engine.advance(incident.id, start + timedelta(minutes=5))
    engine.acknowledge(incident.id, "secondary", start + timedelta(minutes=6))
    engine.resolve(incident.id, "secondary", start + timedelta(minutes=7))
    report = engine.postmortem(incident.id)
    print("Incident:", incident.id, "Status:", incident.status.value)
    print("Notifications:", engine.notifications)
    print("Postmortem:", report)


if __name__ == "__main__":
    main()
