# Changelog

last_reviewed: 2026-04-10

## 2026-04-10

- Fix: Removed phantom tool ID `execute/runInTerminal` from `toolNames` in `.github/hooks/policy-enforcement.json`; only the valid VS Code tool ID `run_in_terminal` remains.
- Related ticket: TASK-GHO-SYS009.

## 2026-04-09

- Feature: Registered the ticket MCP server as a VS Code MCP app using `contributes.mcpServerDefinitionProviders` and `vscode.lm.registerMcpServerDefinitionProvider`.
- Behavior: The ticket server is now available workspace-wide without manual `.vscode/mcp.json` setup.
- Runtime config: Extension provider now launches `.github/mcp-servers/ticket-server/server.py` with `python3`, workspace-root cwd, and `VIBECODING_WORKSPACE_ROOT` environment context.
- Related ticket: TASK-VIB-010.

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
