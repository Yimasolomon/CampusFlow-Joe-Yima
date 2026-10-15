
import json
import tempfile
import unittest
from pathlib import Path

from campusflow.storage import load_tickets, save_tickets


class TestStorage(unittest.TestCase):

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            self.assertEqual(load_tickets(path), [])

    def test_save_and_reload_tickets(self):
        tickets = [
            {
                "id": "T001",
                "title": "Wi-Fi problem",
                "category": "Network",
                "urgency": "high",
                "affected_users": 12,
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
                "notes": [],
            }
        ]

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            save_tickets(tickets, path)
            self.assertEqual(load_tickets(path), tickets)

    def test_corrupted_json_raises_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text("[invalid JSON", encoding="utf-8")

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_json_must_contain_a_list(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text(
                json.dumps({"id": "T001"}),
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_duplicate_ticket_ids_are_rejected(self):
        tickets = [
            {
                "id": "T001",
                "title": "First",
                "category": "Network",
                "urgency": "low",
                "affected_users": 1,
                "priority": "low",
                "status": "open",
                "assigned_to": None,
                "notes": [],
            },
            {
                "id": "T001",
                "title": "Second",
                "category": "Hardware",
                "urgency": "low",
                "affected_users": 1,
                "priority": "low",
                "status": "open",
                "assigned_to": None,
                "notes": [],
            },
        ]

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text(json.dumps(tickets), encoding="utf-8")

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_invalid_ticket_record_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text(
                json.dumps([{"id": "T001", "title": ""}]),
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_save_and_reload_tickets_preserves_notes(self):
        tickets = [
            {
                "id": "T001",
                "title": "Wi-Fi problem",
                "category": "Network",
                "urgency": "high",
                "affected_users": 12,
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
                "notes": [
                    {
                        "id": "N001",
                        "author": "Alex",
                        "message": "Investigating the issue",
                    }
                ],
            }
        ]

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            save_tickets(tickets, path)

            loaded = load_tickets(path)

            self.assertEqual(loaded, tickets)


if __name__ == "__main__":
    unittest.main()
