
def generate_report(tickets):
    statuses = ["open", "in_progress", "resolved"]
    priorities = ["critical", "high", "medium", "low"]

    return {
        "total": len(tickets),
        "by_status": {
            status: sum(
                ticket["status"] == status for ticket in tickets
            )
            for status in statuses
        },
        "by_priority": {
            priority: sum(
                ticket["priority"] == priority for ticket in tickets
            )
            for priority in priorities
        },
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
