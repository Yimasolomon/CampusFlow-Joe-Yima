
PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}


def find_ticket(tickets, ticket_id):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket

    raise ValueError(f"Ticket {ticket_id} was not found.")


def assign_ticket(tickets, ticket_id, staff_name):
    ticket = find_ticket(tickets, ticket_id)
    staff_name = staff_name.strip()

    if not staff_name:
        raise ValueError("Staff name cannot be empty.")

    if ticket["status"] == "resolved":
        raise ValueError("Reopen the ticket before modifying it.")

    ticket["assigned_to"] = staff_name
    return ticket


def update_status(tickets, ticket_id, new_status):
    ticket = find_ticket(tickets, ticket_id)
    new_status = new_status.strip().lower()

    if new_status not in {"open", "in_progress", "resolved"}:
        raise ValueError("Invalid status.")

    current_status = ticket["status"]

    if current_status == "resolved":
        raise ValueError("Reopen the ticket before changing its status.")

    if current_status == "open" and new_status == "resolved":
        raise ValueError(
            "A ticket must be in progress before it can be resolved."
        )

    if current_status == "open" and new_status == "in_progress":
        if not ticket["assigned_to"]:
            raise ValueError("Assign the ticket before starting work.")

    if current_status == "in_progress" and new_status == "open":
        raise ValueError("Use the reopen operation only for resolved tickets.")

    ticket["status"] = new_status
    return ticket


def reopen_ticket(tickets, ticket_id):
    ticket = find_ticket(tickets, ticket_id)

    if ticket["status"] != "resolved":
        raise ValueError("Only resolved tickets can be reopened.")

    ticket["status"] = "open"
    return ticket


def get_queue(tickets):
    unresolved = [
        ticket for ticket in tickets
        if ticket["status"] != "resolved"
    ]

    return sorted(
        unresolved,
        key=lambda ticket: (
            PRIORITY_ORDER[ticket["priority"]],
            int(ticket["id"][1:]),
        ),
    )
