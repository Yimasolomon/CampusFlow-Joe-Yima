# Design Decisions — Engineer A

## 1. Responsibility

Engineer A is responsible for ticket creation, input validation, priority calculation, ticket ID generation, and JSON data persistence.

## 2. Ticket Creation and Validation

Tickets are represented as Python dictionaries. Each ticket contains the following fields:

- `id`
- `title`
- `category`
- `urgency`
- `affected_users`
- `priority`
- `status`
- `assigned_to`

A ticket must have a non-empty title, a valid category, a valid urgency level, and a positive integer for the number of affected users.

Valid categories are `Network`, `Hardware`, `Software`, and `Other`. Valid urgency levels are `low`, `medium`, and `high`. Valid case variations should be normalized consistently.

Invalid input must be rejected with a clear error message instead of creating an invalid ticket.

## 3. Priority Calculation

Ticket priority is calculated automatically using the following rules, in order:

1. **Critical:** urgency is high and at least 10 users are affected.
2. **High:** urgency is high or at least 10 users are affected.
3. **Medium:** urgency is medium or at least 3 users are affected.
4. **Low:** none of the previous conditions apply.

The rules are evaluated in this order so that a ticket matching a higher priority condition is not incorrectly classified as a lower priority.

## 4. Ticket ID Generation

Each ticket receives a unique ID using the format `T001`, `T002`, `T003`, and so on.

ID generation must account for existing tickets, including tickets loaded from saved JSON data, to prevent duplicate IDs after restarting the application.

## 5. JSON Persistence

Ticket data is stored in a JSON file so that tickets remain available between application runs.

The storage design follows these decisions:

- If the data file does not exist, the application starts with an empty ticket list.
- Valid saved ticket data is loaded when the application starts.
- Saving tickets writes the current ticket data to the JSON file.
- Malformed JSON must produce a clear error rather than silently replacing the file with empty data.
- Storage tests should use temporary files so they do not overwrite real application data.

## 6. Modules and Tests

Engineer A is responsible for:

- `campusflow/tickets.py` — ticket creation, validation, ID generation, and priority calculation.
- `campusflow/storage.py` — loading and saving JSON data.
- `tests/test_ticket.py` — tests for ticket creation, validation, IDs, and priority boundaries.
- `tests/test_storage.py` — tests for missing files, saving, loading, and malformed JSON.

## 7. Verification

Engineer A should run the relevant unit tests after making changes and run the full test suite before integration.

Commands:

```bash
python3 -m unittest tests.test_ticket -v
python3 -m unittest tests.test_storage -v
python3 -m unittest discover -s tests -v
```

The design decisions and test results should be updated if implementation behavior changes.

## 8. Ticket Notes and Extended Storage Validation

### Ticket Notes API

- Tickets may contain a `notes` list.
- Each note contains an `id`, `author`, and `message`.
- Note IDs are generated sequentially using the format `N001`, `N002`, and so on, within a ticket.
- Blank authors and messages are rejected.
- Notes cannot be added to resolved tickets.
- Attempting to add a note to an unknown ticket raises `KeyError`.

### Extended Storage Validation

- Loaded ticket records must contain the required ticket fields.
- Ticket IDs must follow the ticket ID format and must be unique.
- Ticket categories, urgency levels, priorities, and statuses must be valid.
- The affected-user count must be a positive integer.
- Notes must be a list of valid note records, with no duplicate note IDs within a ticket.
- Invalid saved data is rejected rather than silently accepted.
- Saving validates the data before writing and uses a temporary file before replacing the saved JSON file.

### Additional Tests

The test suite covers note creation, note ID generation, invalid note input, resolved tickets, unknown tickets, duplicate ticket IDs, invalid ticket records, and JSON persistence.
