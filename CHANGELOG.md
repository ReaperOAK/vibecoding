# Changelog

last_reviewed: 2026-04-09

## 2026-04-09

- Feature: VS Code ticket tree now shows READY, IN_PROGRESS, and DONE root groups in the sidebar.
- Behavior: IN_PROGRESS now aggregates active SDLC directories (`RESEARCH`, `PM`, `ARCHITECT`, `DEVOPS`, `BACKEND`, `UIDESIGNER`, `FRONTEND`, `QA`, `SECURITY`, `CI`, `DOCS`, `VALIDATION`) and sorts tickets by ID.
- UX: `vibecoding.refreshTickets` now re-reads all grouped state directories on refresh.
- Related ticket: TASK-VIB-012.

## 2026-03-27

- Feature: Added MCP Prompts (`process-ticket`, `ticket-status`) and `prompts://list` resource to the ticket server for programmatic agent delegation prompt generation.
- Fix: Updated ticket ID regex docstring escaping in the ticket server (`\\d{3}` in source) to resolve SyntaxWarning without changing prompt behavior.
- Related ticket: TASK-VIB-009.

- Feature: Added MCP Resources (`ticket://READY`, `ticket://DONE`, `ticket://{ticket-id}`) for programmatic ticket data access.
- Security: Path traversal vulnerability fixed with defense-in-depth validation.
- Related ticket: TASK-VIB-008.
