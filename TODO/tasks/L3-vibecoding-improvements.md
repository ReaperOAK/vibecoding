# L3 — Vibecoding System Improvements: Delegatable Tickets

**Date:** 2026-03-26  
**Source L2:** L2-vibecoding-improvements.md  
**Parse command:** `python3 tickets.py --parse TODO/tasks/`

---

# TASK-VIB-001: Fix Catalog Path — Create .github/vibecoding/ Directory

**Type:** infra
**Priority:** critical
**Files:** .github/vibecoding/catalog.yml
**Tags:** p0, infrastructure, boot-sequence, catalog

## Description

All agent instruction files reference `.github/vibecoding/catalog.yml` in the boot sequence (step 4: "Read `.github/vibecoding/catalog.yml`"). This directory does not exist — it is `.github/skills/` that holds the catalog. Every agent silently fails to load catalog context on boot.

Fix: Create `.github/vibecoding/` directory and populate `catalog.yml` with the full catalog content from `.github/skills/catalog.yml` (copy content, not symlink, for portability). The catalog index must list all available skill chunk files so agents can locate and load task-relevant context.

## Acceptance Criteria

- [ ] Given the `.github/vibecoding/` directory does not exist, When the fix is applied, Then `.github/vibecoding/catalog.yml` exists and is a valid YAML file containing skill chunk index entries
- [ ] Given an agent reads `.github/vibecoding/catalog.yml` during boot sequence step 4, When the file is read, Then the agent receives a valid catalog index without error
- [ ] Given `.github/skills/catalog.yml` contains the authoritative skill index, When the vibecoding catalog is created, Then the content at `.github/vibecoding/catalog.yml` references all the same skill chunks available in `.github/skills/`

---

# TASK-VIB-002: Enable All Governance Hooks

**Type:** infra
**Priority:** critical
**Files:** .github/hooks/policy-enforcement.json, .github/hooks/auto-sync.json
**Tags:** p0, governance, hooks, security

## Description

All hooks in `.github/hooks/policy-enforcement.json` and `.github/hooks/auto-sync.json` are set to `"enabled": false`. The hook scripts exist and are correct, but they are never fired. This means guardian STOP checks, `git add .` blocking, destructive operation blocking, and evidence verification are all silently bypassed at runtime.

Fix: Update both JSON files to set `"enabled": true` on every hook entry. Remove or update the `"comment"` fields noting the Preview status — the feature is now stable.

## Acceptance Criteria

- [ ] Given `.github/hooks/policy-enforcement.json` has all hooks set to `"enabled": false`, When the fix is applied, Then every hook entry in the file has `"enabled": true`
- [ ] Given `.github/hooks/auto-sync.json` has the auto-sync hook set to `"enabled": false`, When the fix is applied, Then the SessionStart hook has `"enabled": true`
- [ ] Given an agent session starts with STOP_ALL containing "STOP", When the SessionStart hook fires, Then the guardian check script runs and blocks the session
- [ ] Given an agent attempts `git add .` or `git add -A`, When the PreToolUse hook fires, Then the block-git-add-all script runs and returns a non-zero exit code

---

# TASK-VIB-003: Rewrite MCP Ticket Server with FastMCP Transport

**Type:** backend
**Priority:** critical
**Files:** .github/mcp-servers/ticket-server/server.py, .github/mcp-servers/ticket-server/requirements.txt
**Tags:** p0, mcp-server, transport, fastmcp

## Description

`.github/mcp-servers/ticket-server/server.py` defines 7 tool schemas (syncTickets, getStatus, claimTicket, advanceTicket, releaseTicket, reworkTicket, validateIntegrity) but has NO JSON-RPC/stdio transport layer. The server cannot communicate as an MCP server — it has no `if __name__ == "__main__"` entry point and no protocol handling.

Fix: Rewrite `server.py` using the `mcp` Python SDK with FastMCP pattern. Keep all 7 tool definitions intact; wrap them with `@mcp.tool()` decorators. Add `mcp.run(transport="stdio")` as the entry point. Create `requirements.txt` with `mcp>=1.0.0` dependency.

The tool implementations must call `subprocess.run` against `tickets.py` (path: `../../../../tickets.py` relative to server.py) and return structured results.

## Acceptance Criteria

- [ ] Given the rewritten server.py, When invoked as `python server.py`, Then it starts a valid stdio MCP server without error
- [ ] Given a connected MCP client, When it calls `listTools`, Then all 7 tools (syncTickets, getStatus, claimTicket, advanceTicket, releaseTicket, reworkTicket, validateIntegrity) are returned with their correct input schemas
- [ ] Given a connected MCP client, When it calls `syncTickets`, Then the tool runs `tickets.py --sync` and returns the output as a text result
- [ ] Given a connected MCP client, When it calls `getStatus` with `{"format": "json"}`, Then the tool returns ticket state as structured JSON
- [ ] Given a connected MCP client, When it calls `claimTicket` with valid ticket ID/agent/machine/operator, Then the tool claims the ticket and returns success
- [ ] Given `requirements.txt` exists in the server directory, When `pip install -r requirements.txt` is run, Then `mcp` package installs without error

---

# TASK-VIB-004: Wire Tool-Sets to All Agent Frontmatter

**Type:** infra
**Priority:** high
**Files:** .github/agents/Architect.agent.md, .github/agents/Backend.agent.md, .github/agents/CIReviewer.agent.md, .github/agents/CTO.agent.md, .github/agents/DevOps.agent.md, .github/agents/Documentation.agent.md, .github/agents/Frontend.agent.md, .github/agents/ProductManager.agent.md, .github/agents/QA.agent.md, .github/agents/Research.agent.md, .github/agents/Security.agent.md, .github/agents/Ticketer.agent.md, .github/agents/TODO.agent.md, .github/agents/UIDesigner.agent.md, .github/agents/Validator.agent.md
**Tags:** p1, agent-config, tool-sets, cost-efficiency

## Description

`.github/tool-sets/universal.jsonc`, `research.jsonc`, and `code-editing.jsonc` define reusable tool set configurations but no agent file uses them via the `tool-sets:` frontmatter property. The `#universal` shorthand is unused.

Fix: Add `tool-sets: [#universal]` to all agent frontmatter. Additionally:
- Research agent: add `tool-sets: [#universal, #research]`
- Backend, Frontend, Architect agents: add `tool-sets: [#universal, #code-editing]`

Inspect each `.github/tool-sets/*.jsonc` file to understand which tool namespaces they declare, then add appropriate `tool-sets:` references to each agent.

## Acceptance Criteria

- [ ] Given all 15 agent files, When the fix is applied, Then every agent frontmatter contains a `tool-sets:` property with at least `[#universal]`
- [ ] Given the Research agent, When its frontmatter is read, Then `tool-sets` includes both `#universal` and `#research`
- [ ] Given code-editing agents (Backend, Frontend, Architect), When their frontmatter is read, Then `tool-sets` includes `#code-editing`
- [ ] Given the existing `tools:` property on each agent, When `tool-sets:` is added, Then the existing `tools:` property is preserved (not replaced)

---

# TASK-VIB-005: Add Agents Property to Coordinator Agent Files

**Type:** infra
**Priority:** high
**Files:** .github/agents/Ticketer.agent.md, .github/agents/CTO.agent.md
**Tags:** p1, agent-config, governance, coordinator

## Description

Ticketer and CTO agent files have `handoffs` defined but no `agents: [...]` property to restrict which subagents they can invoke. VS Code 1.100+ supports the `agents` frontmatter property for subagent restriction.

Fix:
- `Ticketer.agent.md`: Add `agents: [Research, ProductManager, Architect, DevOps, Backend, UIDesigner, Frontend, QA, Security, CIReviewer, Documentation, Validator, TODO]`
- `CTO.agent.md`: Add `agents: [Research, ProductManager, Architect, TODO, Ticketer]` (CTO only invokes planning agents and delegates execution to Ticketer)

## Acceptance Criteria

- [ ] Given `Ticketer.agent.md` frontmatter, When parsed by VS Code, Then it contains an `agents:` property listing all 13 worker/specialist agent names
- [ ] Given `CTO.agent.md` frontmatter, When parsed by VS Code, Then it contains an `agents:` property listing only the 5 agents CTO is authorized to invoke
- [ ] Given both files, When the `agents:` property is added, Then all existing frontmatter properties (name, description, tools, model, handoffs) are preserved

---

# TASK-VIB-006: Set user-invocable:false on All Worker Agents

**Type:** infra
**Priority:** medium
**Files:** .github/agents/Frontend.agent.md, .github/agents/QA.agent.md, .github/agents/Security.agent.md, .github/agents/DevOps.agent.md, .github/agents/Documentation.agent.md, .github/agents/UIDesigner.agent.md, .github/agents/Validator.agent.md, .github/agents/Architect.agent.md, .github/agents/ProductManager.agent.md, .github/agents/Research.agent.md, .github/agents/TODO.agent.md
**Tags:** p1, agent-config, security, user-invocable

## Description

Worker agents should not be directly invocable by users — they should only be dispatched by Ticketer or CTO. The `user-invocable: false` field must be set on all worker agents. Backend and CIReviewer already have this property set correctly; the remaining agents need it added or verified.

Fix: Audit all 15 agent files. For every agent that is NOT intended to be directly user-invocable (all except Ticketer and CTO), set `user-invocable: false` in frontmatter. Ticketer and CTO remain `user-invocable: true`.

## Acceptance Criteria

- [ ] Given all 15 agent files, When audited, Then every agent except Ticketer and CTO has `user-invocable: false` in frontmatter
- [ ] Given Ticketer and CTO agent files, When audited, Then both retain `user-invocable: true`
- [ ] Given Backend.agent.md and CIReviewer.agent.md which already have `user-invocable: false`, When the fix is applied, Then their existing value is preserved unchanged

---

# TASK-VIB-007: Update Review-Chain Agent Models to Cost-Efficient Arrays

**Type:** infra
**Priority:** medium
**Files:** .github/agents/CIReviewer.agent.md, .github/agents/QA.agent.md, .github/agents/Validator.agent.md, .github/agents/Documentation.agent.md
**Tags:** p1, agent-config, cost-efficiency, model

## Description

All agents currently use `` — the most expensive model. Review-chain agents (CIReviewer, QA, Validator, Documentation) perform structured, pattern-matching tasks that do not require the most capable model. Using a model array with preferred/fallback reduces cost.

Fix: Update the `model:` field in the 4 review-chain agents to `model: [claude-3-7-sonnet, claude-3-5-sonnet]`. This sets a cheaper preferred model with fallback. Keep Ticketer, CTO, Architect, Backend, Frontend, UIDesigner, Research, ProductManager, DevOps, Security, and TODO on the current or appropriate model.

## Acceptance Criteria

- [ ] Given CIReviewer.agent.md, When the fix is applied, Then `model:` is set to `[claude-3-7-sonnet, claude-3-5-sonnet]`
- [ ] Given QA.agent.md, When the fix is applied, Then `model:` is set to `[claude-3-7-sonnet, claude-3-5-sonnet]`
- [ ] Given Validator.agent.md, When the fix is applied, Then `model:` is set to `[claude-3-7-sonnet, claude-3-5-sonnet]`
- [ ] Given Documentation.agent.md, When the fix is applied, Then `model:` is set to `[claude-3-7-sonnet, claude-3-5-sonnet]`
- [ ] Given all other agent files (not in the review-chain), When audited after the fix, Then their model field is not modified by this ticket

---

# TASK-VIB-008: Add MCP Resources to Ticket Server

**Type:** backend
**Priority:** high
**Dependencies:** TASK-VIB-003
**Files:** .github/mcp-servers/ticket-server/server.py
**Tags:** p2, mcp-server, resources, ticket-state

## Description

The MCP ticket server (after TASK-VIB-003 makes it functional) exposes no MCP Resources. Resources allow agents and tools to read structured ticket data without calling a tool — they are accessible via `resources/read` RPC.

Fix: Add MCP Resources to `server.py` using the `@mcp.resource()` decorator pattern:
- `ticket://READY` — returns JSON array of all READY ticket summaries `[{id, title, type, priority}]`
- `ticket://{ticket-id}` — returns full ticket JSON for a specific ticket (404-style error if not found)
- `ticket://DONE` — returns JSON array of completed tickets with completion timestamps

Resource implementations read from `ticket-state/READY/` and `ticket-state/DONE/` directories.

## Acceptance Criteria

- [ ] Given the updated server.py, When a MCP client calls `resources/list`, Then `ticket://READY`, `ticket://DONE`, and `ticket://{ticket-id}` (as a URI template) are returned
- [ ] Given READY tickets exist, When `ticket://READY` resource is read, Then a JSON array of READY ticket summaries is returned
- [ ] Given a valid ticket ID, When `ticket://{ticket-id}` resource is read with that ID, Then the full ticket JSON is returned
- [ ] Given an invalid ticket ID, When `ticket://{ticket-id}` resource is read, Then an appropriate error response is returned (not a server crash)
- [ ] Given completed tickets, When `ticket://DONE` resource is read, Then a JSON array of done ticket summaries with completion timestamps is returned

---

# TASK-VIB-009: Add MCP Prompts to Ticket Server

**Type:** backend
**Priority:** medium
**Dependencies:** TASK-VIB-003
**Files:** .github/mcp-servers/ticket-server/server.py
**Tags:** p2, mcp-server, prompts, delegation

## Description

The MCP ticket server should expose canned prompt templates via the MCP Prompts API so Ticketer can generate delegation prompts for agents programmatically.

Fix: Add MCP Prompts to `server.py` using the `@mcp.prompt()` decorator pattern:
- `process-ticket` (argument: `ticket_id: str`) — reads the ticket JSON, determines the current stage and appropriate agent, generates the full delegation prompt including ticket context, acceptance criteria, and file scope
- `ticket-status` (no arguments) — calls `tickets.py --status` and formats the output as a structured status report prompt

## Acceptance Criteria

- [ ] Given the updated server.py, When a MCP client calls `prompts/list`, Then `process-ticket` and `ticket-status` are returned
- [ ] Given a valid ticket ID, When `process-ticket` prompt is called with that ID, Then a complete delegation prompt is returned including the ticket's title, description, acceptance criteria, file paths, and agent assignment
- [ ] Given no arguments, When `ticket-status` prompt is called, Then a formatted ticket dashboard is returned as prompt content
- [ ] Given an invalid ticket ID, When `process-ticket` is called, Then an informative error message is returned (not a server crash)

---

# TASK-VIB-010: Register MCP Ticket Server as MCP App via Extension

**Type:** backend
**Priority:** medium
**Dependencies:** TASK-VIB-008, TASK-VIB-009
**Files:** extension/src/extension.ts, extension/package.json
**Tags:** p3, extension, mcp-app, registration

## Description

The MCP ticket server should be registered as an MCP App using the VS Code extension's `contributes.mcpServerDefinitionProviders` mechanism so it is available workspace-wide without requiring users to manually edit `.vscode/mcp.json`.

Fix:
1. In `extension/package.json`, add `contributes.mcpServerDefinitionProviders` with a unique provider ID
2. In `extension/src/extension.ts`, import and call `vscode.lm.registerMcpServerDefinitionProvider` to register the ticket server with its Python script path and environment

The server definition should point to `.github/mcp-servers/ticket-server/server.py`, use `python3` as the command, and set the workspace root as the cwd.

## Acceptance Criteria

- [ ] Given the updated extension is activated, When VS Code starts, Then the ticket MCP server is registered and available in the MCP server list without manual `mcp.json` configuration
- [ ] Given `extension/package.json`, When audited, Then it contains a valid `contributes.mcpServerDefinitionProviders` entry with the extension's publisher ID
- [ ] Given `extension/src/extension.ts`, When audited, Then it calls `vscode.lm.registerMcpServerDefinitionProvider` with the correct server path and provider configuration
- [ ] Given the registered MCP server, When a MCP client connects, Then all 7 tools plus Resources and Prompts from TASK-VIB-008 and TASK-VIB-009 are accessible

---

# TASK-VIB-011: Add @vibecoding Chat Participant to VS Code Extension

**Type:** backend
**Priority:** medium
**Dependencies:** TASK-VIB-001
**Files:** extension/src/extension.ts, extension/src/chatParticipant.ts, extension/package.json
**Tags:** p3, extension, chat-participant, slash-commands

## Description

The VS Code extension has no chat participant. Adding a `@vibecoding` participant enables interactive ticket management from the chat panel without leaving VS Code.

Fix:
1. Create `extension/src/chatParticipant.ts` implementing the chat participant handler
2. Register the participant using `vscode.chat.createChatParticipant('vibecoding', handler)`
3. Implement three slash commands:
   - `/status` — run `tickets.py --status` and render the output as markdown in chat
   - `/sync` — run `tickets.py --sync` and report which tickets moved to READY
   - `/next` — find and display the highest-priority READY ticket with its title and acceptance criteria
4. Update `extension/package.json` with `contributes.chatParticipants` entry

## Acceptance Criteria

- [ ] Given the updated extension is activated, When a user types `@vibecoding` in VS Code chat, Then the vibecoding participant responds
- [ ] Given `@vibecoding /status`, When the slash command is invoked, Then a formatted ticket dashboard appears in chat showing all stage counts
- [ ] Given `@vibecoding /sync`, When the slash command is invoked, Then `tickets.py --sync` runs and chat reports how many tickets were moved to READY
- [ ] Given READY tickets exist, When `@vibecoding /next` is invoked, Then the highest-priority ticket details (title, type, acceptance criteria) are shown in chat
- [ ] Given no READY tickets, When `@vibecoding /next` is invoked, Then a "No READY tickets found" message is returned
- [ ] Given `extension/package.json`, When audited, Then it contains a valid `contributes.chatParticipants` entry with the `vibecoding` participant ID

---

# TASK-VIB-012: Add TreeView Provider for Ticket State

**Type:** backend
**Priority:** medium
**Dependencies:** TASK-VIB-001
**Files:** extension/src/extension.ts, extension/src/ticketTreeProvider.ts, extension/package.json
**Tags:** p3, extension, treeview, ticket-state, ui

## Description

The VS Code extension has no UI for ticket state. A TreeView provider showing tickets grouped by stage directory provides visual feedback on the pipeline.

Fix:
1. Create `extension/src/ticketTreeProvider.ts` implementing `vscode.TreeDataProvider<TicketTreeItem>`
2. The tree root shows stage groups: READY, IN_PROGRESS (all active stages), DONE
3. Each group expands to show individual ticket items (ticket ID + title, with type icon)
4. Register the provider with `vscode.window.createTreeView('vibecoding.tickets', {...})`
5. Update `extension/package.json` with `contributes.viewsContainers` (sidebar) and `contributes.views.vibecoding-sidebar`
6. Add a `vibecoding.refreshTickets` command that calls `provider.refresh()`

## Acceptance Criteria

- [ ] Given the updated extension is activated, When the VS Code sidebar is opened, Then a "Vibecoding Tickets" panel appears in the activity bar
- [ ] Given READY tickets exist in `ticket-state/READY/`, When the tree is expanded, Then a READY group shows individual ticket items with their IDs and titles
- [ ] Given DONE tickets exist in `ticket-state/DONE/`, When the tree is expanded, Then a DONE group shows completed ticket items
- [ ] Given a `vibecoding.refreshTickets` command is invoked, When executed, Then the TreeView re-reads all state directories and refreshes the displayed items
- [ ] Given `extension/package.json`, When audited, Then it contains valid `contributes.viewsContainers` and `contributes.views` entries for the sidebar panel
