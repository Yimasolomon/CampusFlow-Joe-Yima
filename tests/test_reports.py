import unittest

from campusflow.reports import generate_report


class TestReports(unittest.TestCase):

    def test_empty_report(self):
        report = generate_report([])

        self.assertEqual(report["total"], 0)
        self.assertEqual(report["by_status"]["open"], 0)
        self.assertEqual(report["by_priority"]["critical"], 0)
        self.assertEqual(report["by_category"]["Network"], 0)
        self.assertEqual(report["unresolved"], 0)
        self.assertEqual(report["resolved"], 0)
        self.assertEqual(report["resolution_percentage"], 0.0)

    def test_report_counts_tickets(self):
        tickets = [
            {
                "id": "T001",
                "title": "Wi-Fi problem",
                "category": "Network",
                "urgency": "high",
                "affected_users": 12,
                "status": "open",
                "priority": "critical",
                "assigned_to": None,
            },
            {
                "id": "T002",
                "title": "Broken keyboard",
                "category": "Hardware",
                "urgency": "low",
                "affected_users": 1,
                "status": "resolved",
                "priority": "low",
                "assigned_to": "Alex",
            },
            {
                "id": "T003",
                "title": "App error",
                "category": "Software",
                "urgency": "high",
                "affected_users": 5,
                "status": "open",
                "priority": "high",
                "assigned_to": "Jordan",
            },
        ]

        report = generate_report(tickets)

        self.assertEqual(report["total"], 3)
        self.assertEqual(report["by_status"]["open"], 2)
        self.assertEqual(report["by_status"]["resolved"], 1)

        self.assertEqual(report["by_priority"]["critical"], 1)
        self.assertEqual(report["by_priority"]["high"], 1)
        self.assertEqual(report["by_priority"]["low"], 1)

        self.assertEqual(report["by_category"]["Network"], 1)
        self.assertEqual(report["by_category"]["Hardware"], 1)
        self.assertEqual(report["by_category"]["Software"], 1)
        self.assertEqual(report["by_category"]["Other"], 0)

        self.assertEqual(report["unresolved"], 2)
        self.assertEqual(report["resolved"], 1)
        self.assertAlmostEqual(
            report["resolution_percentage"], 33.33, places=2
        )


if __name__ == "__main__":
    unittest.main()
