
def calculate_priority(urgency, affected_users):
    if urgency == "high" and affected_users >= 10:
        return "critical"
    elif urgency == "high" or affected_users >= 10:
        return "high"
    elif urgency == "medium" or affected_users >= 3:
        return "medium"
    else:
        return "low"


def create_ticket(ticket_id, title, category, urgency, affected_users):
    title = title.strip()

    if not title:
        raise ValueError("Ticket title cannot be empty.")

    allowed_categories = ["Network", "Hardware", "Software", "Other"]
    category = category.strip().capitalize()

    if category not in allowed_categories:
        raise ValueError("Invalid ticket category.")

    urgency = urgency.strip().lower()

    if urgency not in ["low", "medium", "high"]:
        raise ValueError("Urgency must be low, medium, or high.")

    if isinstance(affected_users, bool) or not isinstance(affected_users, int):
        raise ValueError("Affected users must be an integer.")

    if affected_users <= 0:
        raise ValueError("Affected users must be greater than zero.")

    priority = calculate_priority(urgency, affected_users)

    return {
        "id": ticket_id,
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
    }


def generate_ticket_id(tickets):
    highest_id = 0

    for ticket in tickets:
        number = int(ticket["id"][1:])

        if number > highest_id:
            highest_id = number

    return f"T{highest_id + 1:03d}"


if __name__ == "__main__":
    ticket = create_ticket(
        "T001",
        "Wi-Fi not working",
        "Network",
        "high",
        12,
    )

    print(ticket)
