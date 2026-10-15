import unittest

from campusflow.notes import add_note


def make_ticket(status="open"):
    return {
        "id": "T001",
        "title": "Wi-Fi problem",
        "category": "Network",
        "urgency": "high",
        "affected_users": 12,
        "priority": "critical",
        "status": status,
        "assigned_to": None,
        "notes": [],
    }


class TestNotes(unittest.TestCase):
    def test_add_note(self):
        tickets = [make_ticket()]

        note = add_note(tickets, "T001", "Alex", "Router restarted")

        self.assertEqual(
            note,
            {
                "id": "N001",
                "author": "Alex",
                "message": "Router restarted",
            },
        )
        self.assertEqual(tickets[0]["notes"], [note])

    def test_note_ids_increase(self):
        tickets = [make_ticket()]

        first = add_note(tickets, "T001", "Alex", "First note")
        second = add_note(tickets, "T001", "Sam", "Second note")

        self.assertEqual(first["id"], "N001")
        self.assertEqual(second["id"], "N002")

    def test_unknown_ticket_raises_key_error(self):
        with self.assertRaises(KeyError):
            add_note([], "T999", "Alex", "A note")

    def test_resolved_ticket_rejects_note_without_mutation(self):
        tickets = [make_ticket(status="resolved")]
        original = [dict(tickets[0])]

        with self.assertRaises(ValueError):
            add_note(tickets, "T001", "Alex", "A note")

        self.assertEqual(tickets, original)

    def test_blank_author_rejected_without_mutation(self):
        tickets = [make_ticket()]
        original = [dict(tickets[0])]

        with self.assertRaises(ValueError):
            add_note(tickets, "T001", "  ", "A note")

        self.assertEqual(tickets, original)

    def test_blank_message_rejected_without_mutation(self):
        tickets = [make_ticket()]
        original = [dict(tickets[0])]

        with self.assertRaises(ValueError):
            add_note(tickets, "T001", "Alex", "  ")

        self.assertEqual(tickets, original)


if __name__ == "__main__":
    unittest.main()
