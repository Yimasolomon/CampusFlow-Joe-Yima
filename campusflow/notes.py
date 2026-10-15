def add_note(tickets, ticket_id, author, message):
    if not isinstance(author, str) or not author.strip():
        raise ValueError("Note author cannot be empty.")

    if not isinstance(message, str) or not message.strip():
        raise ValueError("Note message cannot be empty.")

    ticket = next(
        (item for item in tickets if item.get("id") == ticket_id),
        None,
    )

    if ticket is None:
        raise KeyError(f"Ticket {ticket_id} was not found.")

    if ticket.get("status") == "resolved":
        raise ValueError("Cannot add a note to a resolved ticket.")

    notes = ticket.setdefault("notes", [])

    highest_id = 0
    for note in notes:
        note_id = note.get("id", "")
        if note_id.startswith("N") and note_id[1:].isdigit():
            highest_id = max(highest_id, int(note_id[1:]))

    note = {
        "id": f"N{highest_id + 1:03d}",
        "author": author.strip(),
        "message": message.strip(),
    }

    notes.append(note)
    return note