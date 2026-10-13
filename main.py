
from pathlib import Path

from campusflow.tickets import create_ticket, generate_ticket_id
from campusflow.storage import load_tickets, save_tickets
from campusflow.workflow import (
    assign_ticket,
    update_status,
    reopen_ticket,
    get_queue,
    find_ticket,
)
from campusflow.reports import print_report


DATA_FILE = Path("data/tickets.json")


def show_ticket(ticket):
    print(
        f"\n{ticket['id']} | {ticket['title']}\n"
        f"Category: {ticket['category']} | "
        f"Urgency: {ticket['urgency']} | "
        f"Priority: {ticket['priority']}\n"
        f"Status: {ticket['status']} | "
        f"Assigned to: {ticket['assigned_to'] or 'Unassigned'}\n"
        f"Affected users: {ticket['affected_users']}"
    )


def create_new_ticket(tickets):
    title = input("Title: ")
    category = input("Category (Network/Hardware/Software/Other): ")
    urgency = input("Urgency (low/medium/high): ")

    try:
        affected_users = int(input("Number of affected users: "))
        ticket_id = generate_ticket_id(tickets)

        ticket = create_ticket(
            ticket_id, title, category, urgency, affected_users
        )
        tickets.append(ticket)
        save_tickets(tickets, DATA_FILE)
        print(f"Ticket {ticket_id} created successfully.")
    except ValueError as error:
        print(f"Error: {error}")


def list_tickets(tickets):
    if not tickets:
        print("No tickets found.")
        return

    for ticket in tickets:
        show_ticket(ticket)


def assign_existing_ticket(tickets):
    ticket_id = input("Ticket ID: ").strip().upper()
    staff_name = input("Staff member name: ")

    try:
        assign_ticket(tickets, ticket_id, staff_name)
        save_tickets(tickets, DATA_FILE)
        print("Ticket assigned successfully.")
    except ValueError as error:
        print(f"Error: {error}")


def change_ticket_status(tickets):
    ticket_id = input("Ticket ID: ").strip().upper()
    status = input("New status (open/in_progress/resolved): ")

    try:
        update_status(tickets, ticket_id, status)
        save_tickets(tickets, DATA_FILE)
        print("Ticket status updated.")
    except ValueError as error:
        print(f"Error: {error}")


def reopen_resolved_ticket(tickets):
    ticket_id = input("Ticket ID to reopen: ").strip().upper()

    try:
        reopen_ticket(tickets, ticket_id)
        save_tickets(tickets, DATA_FILE)
        print("Ticket reopened.")
    except ValueError as error:
        print(f"Error: {error}")


def display_queue(tickets):
    queue = get_queue(tickets)

    if not queue:
        print("No unresolved tickets.")
        return

    print("\n--- Priority Queue ---")
    for ticket in queue:
        show_ticket(ticket)


def main():
    try:
        tickets = load_tickets(DATA_FILE)
    except (ValueError, OSError) as error:
        print(f"Could not load saved tickets: {error}")
        print("Fix the ticket file before restarting. No data was overwritten.")
        return

    actions = {
        "1": ("Create ticket", lambda: create_new_ticket(tickets)),
        "2": ("List all tickets", lambda: list_tickets(tickets)),
        "3": ("Assign ticket", lambda: assign_existing_ticket(tickets)),
        "4": ("Update ticket status", lambda: change_ticket_status(tickets)),
        "5": ("Reopen resolved ticket", lambda: reopen_resolved_ticket(tickets)),
        "6": ("View priority queue", lambda: display_queue(tickets)),
        "7": ("View reports", lambda: print_report(tickets)),
    }

    while True:
        print("\n=== CampusFlow Helpdesk ===")
        for number, (description, _) in actions.items():
            print(f"{number}. {description}")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye.")
            break

        action = actions.get(choice)
        if action is None:
            print("Invalid choice. Select an option from the menu.")
            continue

        try:
            action[1]()
        except (ValueError, KeyError, OSError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
