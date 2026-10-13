
import unittest

from campusflow.workflow import (
    assign_ticket,
    update_status,
    reopen_ticket,
    get_queue,
    find_ticket,
)


def sample_tickets():
    return [
        {
            "id": "T001",
            "title": "Wi-Fi failure",
            "category": "Network",
            "urgency": "high",
            "affected_users": 12,
            "priority": "critical",
            "status": "open",
            "assigned_to": None,
        },
        {
            "id": "T002",
            "title": "Broken keyboard",
            "category": "Hardware",
            "urgency": "low",
            "affected_users": 1,
            "priority": "low",
            "status": "open",
            "assigned_to": None,
        },
    ]


class TestWorkflow(unittest.TestCase):

    def test_find_ticket(self):
        tickets = sample_tickets()
        self.assertEqual(find_ticket(tickets, "T001")["title"], "Wi-Fi failure")

    def test_unknown_ticket_is_rejected(self):
        with self.assertRaises(ValueError):
            find_ticket(sample_tickets(), "T999")

    def test_assignment_requires_staff_name(self):
        with self.assertRaises(ValueError):
            assign_ticket(sample_tickets(), "T001", "   ")

    def test_assignment_succeeds(self):
        tickets = sample_tickets()
        assign_ticket(tickets, "T001", "Ada")
        self.assertEqual(tickets[0]["assigned_to"], "Ada")

    def test_unassigned_ticket_cannot_start(self):
        with self.assertRaises(ValueError):
            update_status(sample_tickets(), "T001", "in_progress")

    def test_assigned_ticket_can_start(self):
        tickets = sample_tickets()
        assign_ticket(tickets, "T001", "Ada")
        update_status(tickets, "T001", "in_progress")
        self.assertEqual(tickets[0]["status"], "in_progress")

    def test_ticket_cannot_skip_in_progress(self):
        with self.assertRaises(ValueError):
            update_status(sample_tickets(), "T001", "resolved")

    def test_resolved_ticket_must_be_reopened(self):
        tickets = sample_tickets()
        assign_ticket(tickets, "T001", "Ada")
        update_status(tickets, "T001", "in_progress")
        update_status(tickets, "T001", "resolved")

        with self.assertRaises(ValueError):
            assign_ticket(tickets, "T001", "Sam")

        reopen_ticket(tickets, "T001")
        self.assertEqual(tickets[0]["status"], "open")

    def test_queue_sorts_by_priority_then_ticket_number(self):
        tickets = sample_tickets()
        tickets.extend([
            {
                "id": "T004",
                "title": "Another critical issue",
                "category": "Network",
                "urgency": "high",
                "affected_users": 10,
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
            },
            {
                "id": "T003",
                "title": "Resolved issue",
                "category": "Software",
                "urgency": "low",
                "affected_users": 1,
                "priority": "low",
                "status": "resolved",
                "assigned_to": "Ada",
            },
        ])

        queue = get_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T001", "T004", "T002"],
        )


if __name__ == "__main__":
    unittest.main()
