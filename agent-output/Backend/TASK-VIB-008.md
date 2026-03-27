# TASK-VIB-008 - Backend Rework Summary

## Scope
- .github/mcp-servers/ticket-server/server.py
- .github/mcp-servers/ticket-server/tests/test_server_resources.py

## Security Rework Addressed
- Added strict ticket ID allowlist validation before path construction.
- Added canonical path containment check under tickets/ as defense-in-depth.
- Ensured traversal and malformed IDs fail with the same FileNotFoundError path as invalid IDs.
- Added regression tests for traversal and separator-bearing malformed IDs.

## TDD Evidence
1. RED
- Added `test_traversal_ticket_ids_raise_file_not_found` and `test_separator_bearing_ticket_ids_raise_file_not_found`.
- Ran tests and observed failure for traversal payload (`../ticket-state/READY/TASK-VIB-009`) because `FileNotFoundError` was not raised.

2. GREEN
- Implemented `_validate_ticket_id()` using a strict allowlist regex: `TASK-[A-Z]+-\d{3}`.
- Added canonical containment guard using `Path.resolve()` + `relative_to()` against `tickets/`.
- Kept error behavior consistent by raising `FileNotFoundError` for invalid, malformed, traversal, and missing IDs.

3. REFACTOR
- Kept validation isolated in `_validate_ticket_id()` for single-responsibility and readability.
- Added a concise defense-in-depth comment on containment check.

## Verification
- Command: `python3 -m unittest discover -s .github/mcp-servers/ticket-server/tests -p test_server_resources.py`
- Result: 14 passed, 0 failed.

## Acceptance Criteria Mapping
1. `resources/list` still exposes the registered resources: PASS
2. Valid ticket IDs still return the correct document: PASS
3. Invalid IDs, including traversal payloads, fail safely with normal not-found behavior: PASS
4. Tests now cover malformed IDs and traversal attempts: PASS

## Confidence
HIGH
