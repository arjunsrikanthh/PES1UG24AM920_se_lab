"""Small support ticket tracker with safer operations and JSON persistence."""

import json
import logging
from pathlib import Path

TICKETS = {}
LOGGER = logging.getLogger(__name__)


def create_ticket(
    title, description, reporter, priority="medium", category="general",
    audit_log=None,
):
    """Create a ticket and optionally append an audit entry."""
    if not title or not str(title).strip():
        return None
    if audit_log is None:
        audit_log = []
    ticket_id = str(
        max((int(key) for key in TICKETS if key.isdigit()), default=0) + 1
    )
    ticket = {
        "id": ticket_id,
        "title": title,
        "description": description,
        "priority": priority,
        "category": category,
        "status": "open",
        "reporter": reporter,
        "assignee": None,
    }
    TICKETS[ticket_id] = ticket
    audit_log.append(f"Created ticket {ticket_id} for {reporter}")
    return ticket


def assign_ticket(ticket_id, agent, notify=False):
    """Assign an existing ticket; return False if it is missing."""
    ticket = TICKETS.get(ticket_id)
    if ticket is None:
        return False
    ticket["assignee"] = agent
    if notify:
        LOGGER.info("Ticket %s assigned to %s", ticket_id, agent)
    return True


def update_status(ticket_id, status):
    """Set ticket status, returning None if no such ticket exists."""
    ticket = TICKETS.get(ticket_id)
    if ticket is None:
        return None
    ticket["status"] = status
    return ticket


def search_tickets(status=None, priority=None):
    """Find tickets matching optional filters."""
    return [
        ticket
        for ticket in TICKETS.values()
        if (status is None or ticket["status"] == status)
        and (priority is None or ticket["priority"] == priority)
    ]


def save_tickets(path="tickets.json"):
    """Write tickets as UTF-8 JSON."""
    with Path(path).open("w", encoding="utf-8") as stream:
        json.dump(TICKETS, stream, indent=2)


def load_tickets(path="tickets.json"):
    """Load JSON tickets and validate basic structure."""
    with Path(path).open("r", encoding="utf-8") as stream:
        data = json.load(stream)
    if not isinstance(data, dict) or any(
        not isinstance(item, dict) for item in data.values()
    ):
        raise ValueError("Ticket file must contain a mapping of tickets")
    TICKETS.clear()
    TICKETS.update(data)


def print_ticket_report():
    """Print the current ticket summary."""
    print("Support Tickets")
    if not TICKETS:
        print("No tickets yet")
    for ticket_id, ticket in TICKETS.items():
        print(ticket_id, ticket["title"], ticket["status"])


def close_ticket(ticket_id):
    """Close an existing ticket; return whether it was found."""
    return update_status(ticket_id, "closed") is not None


def closeTicket(ticket_id):  # pylint: disable=invalid-name
    """Keep compatibility with the original public function name."""
    return close_ticket(ticket_id)


def is_open(ticket_id):
    """Check whether a ticket is open or in progress."""
    ticket = TICKETS.get(ticket_id)
    return ticket is not None and ticket["status"] in {"open", "in_progress"}


def main():
    """Demonstrate basic support-ticket operations."""
    logging.basicConfig(level=logging.INFO)
    create_ticket(
        "Cannot sign in", "Password reset link fails", "alex@example.com"
    )
    create_ticket(
        "Billing question", "Charged twice", "lee@example.com", "high"
    )
    assign_ticket("1", "agent-01")
    update_status("1", "in_progress")
    print_ticket_report()
    LOGGER.info("Tickets created: %d", len(TICKETS))
    print("Ticket 1 open?", is_open("1"))
    ticket_id = input("Ticket id to close (Enter to skip): ").strip()
    if ticket_id and not close_ticket(ticket_id):
        print(f"Ticket {ticket_id} not found; nothing closed")
    save_tickets()


if __name__ == "__main__":
    main()
