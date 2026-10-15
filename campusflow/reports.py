def generate_report(tickets):
    statuses = ["open", "in_progress", "resolved"]
    priorities = ["critical", "high", "medium", "low"]
    categories = ["Network", "Hardware", "Software", "Other"]

    by_status = {
        status: sum(ticket["status"] == status for ticket in tickets)
        for status in statuses
    }

    by_priority = {
        priority: sum(
            ticket["priority"] == priority for ticket in tickets
        )
        for priority in priorities
    }

    by_category = {
        category: sum(
            ticket["category"] == category for ticket in tickets
        )
        for category in categories
    }

    total = len(tickets)
    resolved = by_status["resolved"]
    unresolved = by_status["open"] + by_status["in_progress"]

    resolution_percentage = (
        round((resolved / total) * 100, 2) if total else 0.0
    )

    return {
        "total": total,
        "by_status": by_status,
        "by_priority": by_priority,
        "by_category": by_category,
        "unresolved": unresolved,
        "resolved": resolved,
        "resolution_percentage": resolution_percentage,
    }


def print_report(tickets):
    report = generate_report(tickets)

    print("\n--- Ticket Report ---")
    print(f"Total tickets: {report['total']}")

    print("\nBy status:")
    for status, count in report["by_status"].items():
        print(f"  {status}: {count}")

    print("\nBy priority:")
    for priority, count in report["by_priority"].items():
        print(f"  {priority}: {count}")

    print("\nBy category:")
    for category, count in report["by_category"].items():
        print(f"  {category}: {count}")

    print(f"\nUnresolved tickets: {report['unresolved']}")
    print(f"Resolved tickets: {report['resolved']}")
    print(
        "Resolution percentage: "
        f"{report['resolution_percentage']:.2f}%"
    )
