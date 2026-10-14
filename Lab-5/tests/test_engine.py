"""Unit and scenario tests for the incident escalation engine."""

import unittest
from datetime import UTC, datetime, timedelta

from engine.core import IncidentEngine, Status, Tier

NOW = datetime(2026, 10, 14, 8, 0, tzinfo=UTC)


class IncidentEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = IncidentEngine({"api": [Tier("alice", 300), Tier("bob", 120)]})
        self.alert = self.engine.ingest("api", "P1", "API unavailable", NOW)

    def test_ingest_and_primary_notification(self):
        self.assertEqual(self.alert.status, Status.OPEN)
        self.assertEqual(self.engine.notifications, [(self.alert.id, "alice", "P1")])

    def test_exact_escalation_boundary(self):
        self.assertEqual(
            self.engine.advance(self.alert.id, NOW + timedelta(seconds=299)), Status.OPEN
        )
        self.engine.advance(self.alert.id, NOW + timedelta(seconds=300))
        self.assertEqual(self.alert.tier_index, 1)
        self.assertEqual(self.engine.notifications[-1][1], "bob")

    def test_all_tiers_exhausted(self):
        result = self.engine.advance(self.alert.id, NOW + timedelta(seconds=420))
        self.assertEqual(result, Status.EXHAUSTED)
        self.assertIn("incident commander", self.alert.timeline[-1])

    def test_late_scheduler_catches_up(self):
        self.engine.advance(self.alert.id, NOW + timedelta(hours=1))
        self.assertEqual(len(self.engine.notifications), 2)
        self.assertEqual(self.alert.status, Status.EXHAUSTED)

    def test_acknowledgement_stops_escalation(self):
        self.engine.acknowledge(self.alert.id, "alice", NOW + timedelta(seconds=10))
        self.assertEqual(
            self.engine.advance(self.alert.id, NOW + timedelta(hours=1)), Status.ACKNOWLEDGED
        )
        self.assertEqual(len(self.engine.notifications), 1)

    def test_wrong_engineer_cannot_acknowledge(self):
        with self.assertRaises(PermissionError):
            self.engine.acknowledge(self.alert.id, "bob", NOW)

    def test_timeout_processed_before_late_ack(self):
        with self.assertRaises(PermissionError):
            self.engine.acknowledge(self.alert.id, "alice", NOW + timedelta(minutes=5))

    def test_resolve_and_postmortem(self):
        self.engine.acknowledge(self.alert.id, "alice", NOW)
        self.engine.resolve(self.alert.id, "alice", NOW + timedelta(minutes=1))
        report = self.engine.postmortem(self.alert.id)
        self.assertEqual(report["incident_id"], self.alert.id)
        self.assertEqual(report["acknowledged_by"], "alice")
        self.assertEqual(report["root_cause"], "TODO")

    def test_unacknowledged_cannot_resolve(self):
        with self.assertRaises(PermissionError):
            self.engine.resolve(self.alert.id, "alice", NOW)

    def test_postmortem_before_resolution_fails(self):
        with self.assertRaises(ValueError):
            self.engine.postmortem(self.alert.id)

    def test_invalid_alerts(self):
        for service, severity, description in [
            ("missing", "P1", "hi"),
            ("api", "P9", "hi"),
            ("api", "P1", ""),
        ]:
            with self.subTest(service=service, severity=severity), self.assertRaises(ValueError):
                self.engine.ingest(service, severity, description, NOW)

    def test_naive_time_rejected(self):
        with self.assertRaises(ValueError):
            self.engine.ingest("api", "P1", "test", datetime(2026, 10, 14))

    def test_bad_policies_rejected(self):
        with self.assertRaises(ValueError):
            IncidentEngine({"api": []})
        with self.assertRaises(ValueError):
            Tier("", 5)
        with self.assertRaises(ValueError):
            Tier("alice", 0)

    def test_time_cannot_reverse(self):
        with self.assertRaises(ValueError):
            self.engine.advance(self.alert.id, NOW - timedelta(seconds=1))


if __name__ == "__main__":
    unittest.main()
