
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
                "status": "open",
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


if __name__ == "__main__":
    unittest.main()
