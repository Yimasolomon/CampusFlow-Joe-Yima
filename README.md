# CampusFlow-Joe-Yima# CampusFlow — Ticket Creation and Storage

## Feature Ownership: Engineer A

### Overview

CampusFlow is a Python command-line campus helpdesk ticket manager. Engineer A is responsible for ticket creation, input validation, priority calculation, automatic ticket ID generation, and JSON-based persistence.

### Ticket Creation

Users can create support tickets with the following information:

- Ticket ID generated automatically, such as `T001`.
- Title describing the issue.
- Category: Network, Hardware, Software, or Other.
- Urgency: low, medium, or high.
- Number of affected users.
- Calculated priority.
- Initial status of `open`.
- Assigned staff member, initially `None`.

### Validation

The ticket-creation module validates required fields and rejects blank titles, invalid categories, invalid urgency values, and affected-user counts that are not positive integers.

Valid category and urgency values are normalized to consistent formats.

### Priority Rules

Ticket priority is calculated as follows:

1. High urgency and at least 10 affected users: `critical`.
2. High urgency or at least 10 affected users: `high`.
3. Medium urgency or at least 3 affected users: `medium`.
4. Otherwise: `low`.

### Data Persistence

Tickets are stored in JSON using `campusflow/storage.py`.

- Existing ticket data is loaded when the application starts.
- A missing data file is treated as a fresh start.
- Malformed JSON produces a clear error instead of silently discarding saved data.
- Ticket IDs are generated using existing ticket data to avoid reuse after reload.

The application stores runtime data in `data/tickets.json`, which should normally be excluded from version control.

### Engineer A's Modules and Tests

- `campusflow/tickets.py` — ticket creation, validation, priority, and ID generation.
- `campusflow/storage.py` — saving and loading ticket data.
- `tests/test_ticket.py` — ticket validation, priority boundaries, normalization, and ID generation.
- `tests/test_storage.py` — save/reload, missing-file, and invalid-data behavior.

### Running the Tests

Run the complete project test suite from the repository root:

`python3 -m unittest discover -s tests -v`

Engineer A verifies the ticket and storage modules independently and contributes to final integration testing.