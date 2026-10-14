"""Basic regression tests for the support-ticket tracker."""
import tempfile
import unittest
from pathlib import Path
import support_ticket_tracker as tracker


class TrackerTests(unittest.TestCase):
    def setUp(self):
        tracker.TICKETS.clear()

    def test_creation_and_assignment(self):
        ticket = tracker.create_ticket("Help", "Login", "user", "high")
        self.assertTrue(tracker.assign_ticket(ticket["id"], "agent"))
        self.assertEqual(tracker.search_tickets(priority="high"), [ticket])

    def test_unknown_id(self):
        self.assertFalse(tracker.assign_ticket("404", "agent"))
        self.assertFalse(tracker.is_open("404"))
        self.assertFalse(tracker.close_ticket("404"))

    def test_close_alias(self):
        tracker.create_ticket("Help", "A", "user")
        self.assertTrue(tracker.closeTicket("1"))

    def test_audit(self):
        entries = []
        tracker.create_ticket("Help", "A", "user", audit_log=entries)
        tracker.create_ticket("Other", "B", "user")
        self.assertEqual(entries, ["Created ticket 1 for user"])

    def test_save_and_load(self):
        tracker.create_ticket("Help", "A", "user")
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "tickets.json"
            tracker.save_tickets(target)
            tracker.TICKETS.clear()
            tracker.load_tickets(target)
        self.assertEqual(tracker.TICKETS["1"]["title"], "Help")

    def test_bad_json(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "tickets.json"
            target.write_text("[]", encoding="utf-8")
            with self.assertRaises(ValueError):
                tracker.load_tickets(target)

    def test_ticket_id_after_delete(self):
        tracker.create_ticket("A", "a", "user")
        tracker.create_ticket("B", "b", "user")
        del tracker.TICKETS["1"]
        self.assertEqual(tracker.create_ticket("C", "c", "user")["id"], "3")


if __name__ == "__main__":
    unittest.main()
