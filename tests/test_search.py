import unittest

from campusflow.search import search_tickets, sort_search_results


def make_ticket(
    ticket_id,
    title,
    category,
    priority,
    status,
    assigned_to=None,
):
    return {
        "id": ticket_id,
        "title": title,
        "category": category,
        "urgency": "high",
        "affected_users": 10,
        "priority": priority,
        "status": status,
        "assigned_to": assigned_to,
    }


class TestTicketSearch(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            make_ticket(
                "T003", "WiFi not working", "Network",
                "high", "open",
            ),
            make_ticket(
                "T001", "Laptop will not start", "Hardware",
                "critical", "in_progress", "Ada",
            ),
            make_ticket(
                "T002", "WiFi connection slow", "Network",
                "medium", "resolved", "Ben",
            ),
            make_ticket(
                "T010", "Install software", "Software",
                "low", "open",
            ),
        ]

    def test_search_by_title_is_case_insensitive(self):
        results = search_tickets(self.tickets, title="WIFI")

        self.assertEqual(
            {ticket["id"] for ticket in results},
            {"T003", "T002"},
        )

    def test_search_by_category(self):
        results = search_tickets(self.tickets, category="network")

        self.assertEqual(
            {ticket["id"] for ticket in results},
            {"T003", "T002"},
        )

    def test_search_combines_filters_with_and(self):
        results = search_tickets(
            self.tickets,
            title="wifi",
            category="Network",
            status="open",
        )

        self.assertEqual([ticket["id"] for ticket in results], ["T003"])

    def test_no_matching_ticket_returns_empty_list(self):
        results = search_tickets(self.tickets, title="printer")

        self.assertEqual(results, [])

    def test_empty_filters_return_all_tickets(self):
        results = search_tickets(self.tickets)

        self.assertEqual(len(results), 4)

    def test_invalid_category_is_rejected(self):
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, category="Furniture")

    def test_invalid_status_is_rejected(self):
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, status="pending")

    def test_invalid_priority_is_rejected(self):
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, priority="urgent")

    def test_search_does_not_change_original_collection(self):
        original_ids = [ticket["id"] for ticket in self.tickets]

        search_tickets(self.tickets, category="Network")

        self.assertEqual(
            [ticket["id"] for ticket in self.tickets],
            original_ids,
        )

    def test_search_results_can_be_sorted_by_priority_then_id(self):
        results = search_tickets(self.tickets)
        sorted_results = sort_search_results(results)

        self.assertEqual(
            [ticket["id"] for ticket in sorted_results],
            ["T001", "T003", "T002", "T010"],
        )

    def test_sorting_does_not_change_original_ticket_order(self):
        original_ids = [ticket["id"] for ticket in self.tickets]

        sort_search_results(self.tickets)

        self.assertEqual(
            [ticket["id"] for ticket in self.tickets],
            original_ids,
        )


if __name__ == "__main__":
    unittest.main()
