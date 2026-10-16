# CampusFlow Baseline Check

## Engineer A — Baseline and Integration

### 1. Revision under review

- Repository: `https://github.com/Yimasolomon/CampusFlow-Joe-Yima`
- Branch: `main`
- Commit SHA: `42862b04c2b08a2571b291606285def8095a4ba9`
- Commit message: `Merge pull request #2 from Yimasolomon/feat/workflow-reporting`
- Python version: `Python 3.12.3`

### 2. Test execution

Command used:

```bash
python3 -m unittest discover -s tests -v
```

Actual result: **26 tests passed.**

- Failures: 0
- Errors: 0

Note: `python -m unittest discover -s tests -v` could not run because the `python` command was unavailable in the environment. Using `python3` worked.

### 3. CLI observations

- App launch: The menu displayed successfully after an accidental local edit to `main.py` was removed.
- Valid ticket creation: Previously tested; exact input and observed output still need to be recorded.
- Invalid input: Previously tested; exact input and observed output still need to be recorded.
- Priority queue: Previously tested; exact input and observed output still need to be recorded.

### 4. Baseline observations

- The existing automated test suite passed at the recorded revision.
- The application launched and displayed its menu after the local edit was removed.
- The existing tests provide a baseline for checking that new validation, notes, search, reporting, and storage changes do not break existing functionality.
- The three CLI scenarios above need their actual observations documented when the recorded details are available.

### 5. Audit status

This document records the current baseline evidence available to Engineer A. Before treating it as the final shared baseline, verify that the recorded commit is the designated revision under review and complete the missing CLI observations where possible.

No feature changes should be treated as part of the baseline revision unless they are committed and explicitly identified.



#### Engineer B

CampusFlow Baseline Check
Engineer B — Search, Reports and Understanding Check
1. Revision under review
Repository: https://github.com/Yimasolomon/CampusFlow-Joe-Yima

Branch: main

Commit SHA: 42862b04c2b08a2571b291606285def8095a4ba9

Commit message: Merge pull request #2 from Yimasolomon/feat/workflow-reporting

Python version: Python 3.12.3

2. Test execution
Command used:

python3 -m unittest discover -s tests -v
Actual result: 26 tests passed.

Tests passed: 26

Failures: 0

Errors: 0

The supplied test output shows successful tests covering reports, JSON storage, ticket priority calculation, ticket creation and ID generation, workflow assignment, status transitions, ticket lookup, and priority queue ordering.

3. CLI observations
App launch: Pending confirmation of Engineer B’s actual launch result and displayed output.

Valid ticket creation: Pending the exact input used and the observed result.

Invalid input: Pending the exact input used and the observed result.

Priority queue: The automated test test_queue_sorts_by_priority_then_ticket_number passed. The actual CLI inputs, displayed tickets, and observed ordering still need to be recorded.

4. Baseline observations
Automated tests
The supplied test output reports 26 successful tests and no failures or errors.

Existing reports
The following report tests passed:

test_empty_report

test_report_counts_tickets

These tests provide baseline evidence that empty-report handling and ticket-count reporting are covered by the existing test suite.

Existing storage
The following storage tests passed:

test_corrupted_json_raises_error

test_json_must_contain_a_list

test_missing_file_returns_empty_list

test_save_and_reload_tickets

These tests cover corrupted JSON, the expected top-level JSON structure, missing files, and saving and reloading tickets.

Existing ticket functionality
The supplied output confirms passing tests for:

Critical, high, medium, and low priority calculations.

Ticket creation and rejection of blank titles, invalid urgency, and zero affected users.

First ticket ID, next ticket ID, and ID generation using the highest existing number.

Assignment validation and successful assignment.

Rejection of unassigned tickets starting work.

Rejection of unknown ticket IDs.

Status-transition rules, including reopening resolved tickets and preventing skipped workflow stages.

Priority queue sorting by priority and ticket number.

Search and filtering
The supplied test output does not establish whether a dedicated title-search or combined-filter feature exists. Inspect the current application and record the observed behaviour before making claims.

Potential issues
No new defect is confirmed by the supplied test output. Any suspected issue should be recorded only after it has been reproduced.

5. Audit status
Engineer B’s supplied automated test output supports a baseline result of 26 passing tests, with zero failures and zero errors.

Before finalizing this record:

Confirm the audited commit SHA against the designated revision.

Record the actual CLI launch, valid ticket creation, invalid input, and priority queue observations.

Confirm search and filtering behaviour in the existing application.

Keep any unverified observations clearly identified as pending.

No feature changes should be treated as part of the baseline revision unless they are committed and explicitly identified.
