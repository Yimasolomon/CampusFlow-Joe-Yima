# AI Learning Log — Engineer A

**Responsibilities:** `campusflow/tickets.py`, `campusflow/storage.py`, `tests/test_ticket.py`, and `tests/test_storage.py`.

## Entry 1 — Ticket Validation and Priority Calculation

- **Task:** Improve ticket field validation and priority calculation.
- **AI assistance used:** I used AI to understand how to validate ticket titles, categories, urgency levels, and affected-user counts, and how to apply the project's priority rules in the correct order.
- **What I learned:** I learned that validating user input before creating a ticket helps prevent invalid data from entering the system. I also learned that the order of conditional statements matters when calculating priority. For example, a ticket with high urgency affecting at least 10 users must be classified as critical before the less restrictive high-priority condition is checked.
- **My decision:** I followed the project's specified priority rules and used input validation to reject invalid values. I also considered boundary cases, such as 2 versus 3 affected users and 9 versus 10 affected users, to check that priority changes at the correct thresholds.
- **Verification:** The full test suite was previously reported to pass 37 tests using `python3 -m unittest discover -s tests -v`. Before submitting this log, I will confirm that this result covers my final changes and record the latest test result.

## Entry 2 — JSON Persistence and Error Handling

- **Task:** Implement or review saving and loading tickets using JSON.
- **AI assistance used:** I used AI to understand how Python's JSON tools can save ticket dictionaries to a file and load them when the application starts.
- **What I learned:** I learned that a missing data file and a malformed JSON file are different situations. A missing file can be treated as a fresh start with an empty ticket list, whereas malformed JSON may indicate corrupted saved data and should produce a clear error. Silently replacing corrupted data with an empty list could cause data loss.
- **My decision:** I followed the requirement to preserve existing data when loading fails. The application should report the problem rather than automatically overwrite a malformed file. I also considered using temporary files in storage tests so that test runs do not interfere with the application's real ticket data.
- **Verification:** I will verify the storage behavior by testing a missing file, saving and reloading tickets, and loading malformed JSON. I will record the actual results after running the relevant storage tests.

## Entry 3 — Reviewing an AI Suggestion

- **Task:** Independently evaluate an AI-generated suggestion related to ticket validation or persistence.
- **AI suggestion:** I will record the specific suggestion I received from AI before finalizing this entry. For example, if AI suggested treating every file-loading error as an empty ticket list, I would evaluate whether that meets the requirement to preserve corrupted data.
- **My evaluation:** I would check the suggestion against the project requirements, particularly the requirement that malformed JSON must produce a clear error rather than silently erase or replace saved data.
- **Action taken:** If the suggestion was to treat malformed JSON as an empty list, I would reject that approach and retain clear error handling. I will use this example only if it reflects a suggestion I actually received and a decision I actually made; otherwise, I will document a different genuine correction, improvement, or rejection.
- **Verification:** I will run the relevant test or manual experiment and record the actual result, including whether malformed data is reported without being overwritten.