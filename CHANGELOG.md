# Changelog

last_reviewed: 2026-03-27

## 2026-03-27

- Feature: Added MCP Prompts (`process-ticket`, `ticket-status`) and `prompts://list` resource to the ticket server for programmatic agent delegation prompt generation.
- Related ticket: TASK-VIB-009.

- Feature: Added MCP Resources (`ticket://READY`, `ticket://DONE`, `ticket://{ticket-id}`) for programmatic ticket data access.
- Security: Path traversal vulnerability fixed with defense-in-depth validation.
- Related ticket: TASK-VIB-008.
