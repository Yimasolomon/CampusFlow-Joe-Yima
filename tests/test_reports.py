
import unittest

from campusflow.reports import generate_report


class TestReports(unittest.TestCase):

    def test_empty_report(self):
        report = generate_report([])

        self.assertEqual(report["total"], 0)
        self.assertEqual(report["by_status"]["open"], 0)
        self.assertEqual(report["by_priority"]["critical"], 0)

    def test_report_counts_tickets(self):
        tickets = [
            {"status": "open", "priority": "critical"},
            {"status": "resolved", "priority": "low"},
            {"status": "open", "priority": "high"},
        ]

        report = generate_report(tickets)

        self.assertEqual(report["total"], 3)
        self.assertEqual(report["by_status"]["open"], 2)
        self.assertEqual(report["by_status"]["resolved"], 1)
        self.assertEqual(report["by_priority"]["critical"], 1)
        self.assertEqual(report["by_priority"]["high"], 1)
        self.assertEqual(report["by_priority"]["low"], 1)


if __name__ == "__main__":
    unittest.main()
