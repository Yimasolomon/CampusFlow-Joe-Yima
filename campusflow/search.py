PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}

VALID_CATEGORIES = {"network", "hardware", "software", "other"}
VALID_STATUSES = {"open", "in_progress", "resolved"}
VALID_PRIORITIES = {"critical", "high", "medium", "low"}


def search_tickets(
    tickets,
    title=None,
    category=None,
    status=None,
    priority=None,
):
    """Return matching tickets without changing the original collection."""

    title = (title or "").strip().casefold()
    category = (category or "").strip().casefold()
    status = (status or "").strip().casefold()
    priority = (priority or "").strip().casefold()

    if category and category not in VALID_CATEGORIES:
        raise ValueError("Invalid category filter.")

    if status and status not in VALID_STATUSES:
        raise ValueError("Invalid status filter.")

    if priority and priority not in VALID_PRIORITIES:
        raise ValueError("Invalid priority filter.")

    results = []

    for ticket in tickets:
        if title and title not in ticket["title"].casefold():
            continue

        if category and ticket["category"].casefold() != category:
            continue

        if status and ticket["status"].casefold() != status:
            continue

        if priority and ticket["priority"].casefold() != priority:
            continue

        results.append(ticket.copy())

    return results


def sort_search_results(tickets):
    """Sort search results by priority, then numeric ticket ID."""

    return sorted(
        tickets,
        key=lambda ticket: (
            PRIORITY_ORDER[ticket["priority"].casefold()],
            int(ticket["id"][1:]),
        ),
    )


def print_search_results(tickets):
    if not tickets:
        print("No matching tickets found.")
        return

    print("\n--- Search Results ---")

    for ticket in tickets:
        print(
            f"{ticket['id']} | "
            f"{ticket['title']} | "
            f"{ticket['category']} | "
            f"{ticket['priority']} | "
            f"{ticket['status']} | "
            f"Assigned to: {ticket.get('assigned_to') or 'Unassigned'}"
        )
