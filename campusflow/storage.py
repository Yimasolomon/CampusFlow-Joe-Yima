import json
import os
import tempfile
from pathlib import Path


REQUIRED_FIELDS = {
    "id",
    "title",
    "category",
    "urgency",
    "affected_users",
    "priority",
    "status",
    "assigned_to",
}

CATEGORIES = {"Network", "Hardware", "Software", "Other"}
URGENCIES = {"low", "medium", "high"}
PRIORITIES = {"low", "medium", "high", "critical"}
STATUSES = {"open", "in_progress", "resolved"}


def validate_tickets(tickets):
    if not isinstance(tickets, list):
        raise ValueError("Ticket file must contain a list of tickets.")

    seen_ids = set()

    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError("Each ticket must be an object.")

        if not REQUIRED_FIELDS.issubset(ticket):
            raise ValueError("Ticket is missing required fields.")

        ticket_id = ticket["id"]
        if (
            not isinstance(ticket_id, str)
            or len(ticket_id) < 2
            or not ticket_id.startswith("T")
            or not ticket_id[1:].isdigit()
        ):
            raise ValueError("Ticket ID must use the format T001.")

        if ticket_id in seen_ids:
            raise ValueError(f"Duplicate ticket ID: {ticket_id}")
        seen_ids.add(ticket_id)

        if not isinstance(ticket["title"], str) or not ticket["title"].strip():
            raise ValueError("Ticket title cannot be empty.")

        if ticket["category"] not in CATEGORIES:
            raise ValueError("Invalid ticket category.")

        if ticket["urgency"] not in URGENCIES:
            raise ValueError("Invalid ticket urgency.")

        affected = ticket["affected_users"]
        if isinstance(affected, bool) or not isinstance(affected, int) or affected <= 0:
            raise ValueError("Affected users must be a positive integer.")

        if ticket["priority"] not in PRIORITIES:
            raise ValueError("Invalid ticket priority.")

        if ticket["status"] not in STATUSES:
            raise ValueError("Invalid ticket status.")

        if ticket["assigned_to"] is not None and not isinstance(
            ticket["assigned_to"], str
        ):
            raise ValueError("Assigned staff must be a name or None.")

        notes = ticket.get("notes", [])
        if not isinstance(notes, list):
            raise ValueError("Ticket notes must be a list.")

        note_ids = set()
        for note in notes:
            if not isinstance(note, dict):
                raise ValueError("Each note must be an object.")
            if not {"id", "author", "message"}.issubset(note):
                raise ValueError("Note is missing required fields.")
            if not all(
                isinstance(note[field], str) and note[field].strip()
                for field in ("id", "author", "message")
            ):
                raise ValueError("Note ID, author, and message cannot be empty.")
            if note["id"] in note_ids:
                raise ValueError(f"Duplicate note ID: {note['id']}")
            note_ids.add(note["id"])


def load_tickets(path):
    path = Path(path)

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ValueError(f"Ticket file contains invalid JSON: {error}") from error

    validate_tickets(tickets)
    return tickets


def save_tickets(tickets, path):
    validate_tickets(tickets)

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=path.parent,
            delete=False,
        ) as file:
            temporary_path = Path(file.name)
            json.dump(tickets, file, indent=4)
            file.write("\n")

        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()
