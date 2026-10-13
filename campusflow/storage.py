import json
from pathlib import Path


def load_tickets(path):
    path = Path(path)

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Ticket file contains invalid JSON: {error}"
        ) from error

    if not isinstance(tickets, list):
        raise ValueError("Ticket file must contain a list of tickets.")

    return tickets


def save_tickets(tickets, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)
