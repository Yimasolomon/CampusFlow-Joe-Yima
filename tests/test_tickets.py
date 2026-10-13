from campusflow.tickets import (
    calculate_priority,
    create_ticket,
    generate_ticket_id,
)

import unittest

from campusflow.tickets import calculate_priority, create_ticket


class TestCalculatePriority(unittest.TestCase):

    def test_critical_priority(self):
        self.assertEqual(calculate_priority("high", 10), "critical")

    def test_high_priority(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_medium_priority(self):
        self.assertEqual(calculate_priority("medium", 1), "medium")

    def test_low_priority(self):
        self.assertEqual(calculate_priority("low", 1), "low")


class TestCreateTicket(unittest.TestCase):

    def test_create_ticket(self):
        ticket = create_ticket(
            "T001", "Wi-Fi problem", "Network", "high", 12
        )

        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])

    def test_reject_blank_title(self):
        with self.assertRaises(ValueError):
            create_ticket("T001", "   ", "Network", "high", 2)

    def test_reject_zero_affected_users(self):
        with self.assertRaises(ValueError):
            create_ticket("T001", "Wi-Fi problem", "Network", "high", 0)

    def test_reject_invalid_urgency(self):
        with self.assertRaises(ValueError):
            create_ticket("T001", "Wi-Fi problem", "Network", "urgent", 2)

if __name__ == "__main__":
    unittest.main()


class TestGenerateTicketId(unittest.TestCase):

    def test_first_ticket_id(self):
        self.assertEqual(generate_ticket_id([]), "T001")

    def test_next_ticket_id(self):
        tickets = [
            {"id": "T001"},
            {"id": "T002"}
        ]
        self.assertEqual(generate_ticket_id(tickets), "T003")

    def test_id_uses_highest_existing_number(self):
        tickets = [
            {"id": "T001"},
            {"id": "T007"},
            {"id": "T003"}
        ]
        self.assertEqual(generate_ticket_id(tickets), "T008")
