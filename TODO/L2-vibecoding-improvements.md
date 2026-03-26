# L2 — Vibecoding System Improvements: Execution Blocks

**Date:** 2026-03-26  
**Source:** L1-vibecoding-improvements.md

---

## From L1.1 — Infrastructure Integrity

### BLOCK 1.1 — Fix Catalog Path (P0)

Create the missing `.github/vibecoding/` directory and a `catalog.yml` file that references or mirrors `.github/skills/catalog.yml`. This unblocks every agent's boot sequence step 4 which reads `.github/vibecoding/catalog.yml`.

- **Deliverable:** `.github/vibecoding/catalog.yml` exists and contains valid catalog index content derived from `.github/skills/catalog.yml`
- **Effort:** XS
- **L3 tickets:** TASK-VIB-001

### BLOCK 1.2 — Enable Governance Hooks (P0)

Update `.github/hooks/policy-enforcement.json` and `.github/hooks/auto-sync.json` to set `"enabled": true` on all hooks. The hook scripts are already correct; only the JSON config files need updating.

- **Deliverable:** All hooks set to `"enabled": true`; guardian check, git-add-all block, destructive-op block, evidence verification, and auto-sync all fire at runtime
- **Effort:** XS
- **L3 tickets:** TASK-VIB-002

---

## From L1.2 — MCP Server Core Transport

### BLOCK 2.1 — FastMCP Transport Implementation (P0)

Rewrite `.github/mcp-servers/ticket-server/server.py` using the `mcp` Python SDK (FastMCP pattern) with proper stdio transport. Keep all 7 existing tool definitions (syncTickets, getStatus, claimTicket, advanceTicket, releaseTicket, reworkTicket, validateIntegrity); wrap them with `@mcp.tool()` decorators and add the `mcp.run(transport="stdio")` entry point.

- **Deliverable:** `server.py` passes `mcp test` / can be invoked as a valid stdio MCP server; all 7 tools remain functional
- **Effort:** M
- **L3 tickets:** TASK-VIB-003
- **Dependencies (inter-block):** None (P0)

---

## From L1.3 — Agent Governance Configuration

### BLOCK 3.1 — Wire Tool-Sets to Agent Frontmatter (P1)

Add `tool-sets: [#universal]` (or appropriate role-specific tool-set names) to each agent's YAML frontmatter. Tool-set definitions in `.github/tool-sets/` are already correct. This requires updating all 15 agent `.agent.md` files.

- **Deliverable:** Every agent file has a `tool-sets:` property referencing at least `#universal`; role-specific agents (Research, Architect, Frontend) also reference their domain tool-set
- **Effort:** S
- **L3 tickets:** TASK-VIB-004
- **Dependencies (inter-block):** None (can run in parallel with P0 blocks but sequenced after P0 completes by priority)

### BLOCK 3.2 — Platform-Level Agent Restrictions (P1)

Two complementary changes:
1. Add `agents: [Research, ProductManager, Architect, DevOps, Backend, UIDesigner, Frontend, QA, Security, CIReviewer, Documentation, Validator, TODO]` to `Ticketer.agent.md` and a restricted subset to `CTO.agent.md`
2. Audit all worker agents and set `user-invocable: false` on any that are missing it (Backend, Frontend, QA, Security, DevOps, Documentation, UIDesigner, Validator, etc.)

- **Deliverable:** Ticketer and CTO have `agents:` property; all non-coordinator agents have `user-invocable: false`
- **Effort:** XS
- **L3 tickets:** TASK-VIB-005, TASK-VIB-006
- **Dependencies (inter-block):** None

### BLOCK 3.3 — Review-Chain Model Optimization (P1)

Update the `model:` field in CIReviewer, QA, Validator, and Documentation agent files from `Claude Opus 4.6 (copilot)` to `[claude-3-7-sonnet, claude-3-5-sonnet]` (model array with fallback). These agents perform structured review tasks that do not require the most capable model.

- **Deliverable:** 4 agent files use cheaper model array; zero breaking change to SDLC pipeline
- **Effort:** XS
- **L3 tickets:** TASK-VIB-007
- **Dependencies (inter-block):** None

---

## From L1.4 — MCP Server Feature Enhancements

### BLOCK 4.1 — MCP Resources Endpoints (P2)

Add MCP Resources implementation to `server.py`. Three resources:
- `ticket://READY` — JSON array of all READY ticket IDs and titles
- `ticket://{ticket-id}` — Full ticket JSON for a specific ticket
- `ticket://DONE` — JSON array of completed ticket IDs and completion timestamps

- **Deliverable:** `server.py` exposes 3 MCP Resource URIs; resources are accessible to any MCP client
- **Effort:** S
- **L3 tickets:** TASK-VIB-008
- **Dependencies (inter-block):** BLOCK 2.1 (TASK-VIB-003) must be DONE

### BLOCK 4.2 — MCP Prompts Endpoints (P2)

Add MCP Prompts implementation to `server.py`. Two prompt templates:
- `process-ticket` (argument: `ticket_id`) — generates the delegation prompt for the appropriate agent
- `ticket-status` (no arguments) — generates a formatted status report prompt

- **Deliverable:** `server.py` exposes 2 MCP Prompt templates; prompts return properly structured `GetPromptResult`
- **Effort:** S
- **L3 tickets:** TASK-VIB-009
- **Dependencies (inter-block):** BLOCK 2.1 (TASK-VIB-003) must be DONE

---

## From L1.5 — Extension Platform

### BLOCK 5.1 — MCP App Registration (P3)

Update `extension/src/extension.ts` to call `vscode.lm.registerMcpServerDefinitionProvider` with the ticket server path so the MCP server is registered workspace-wide. Update `extension/package.json` to declare the `contributes.mcpServerDefinitionProviders` contribution point.

- **Deliverable:** On extension activation, ticket MCP server is available in VS Code without `.vscode/mcp.json` entry
- **Effort:** S
- **L3 tickets:** TASK-VIB-010
- **Dependencies (inter-block):** BLOCK 4.1 + BLOCK 4.2 (TASK-VIB-008, TASK-VIB-009) must be DONE

### BLOCK 5.2 — Chat Participant (P3)

Create `extension/src/chatParticipant.ts` that registers a `@vibecoding` chat participant with `/status`, `/sync`, and `/next` slash commands. Update `extension/src/extension.ts` to activate it and `extension/package.json` to declare the `contributes.chatParticipants` contribution point.

- **Deliverable:** `@vibecoding` participant responds in VS Code chat; `/status` shows ticket dashboard, `/sync` runs `tickets.py --sync`, `/next` shows next READY ticket
- **Effort:** M
- **L3 tickets:** TASK-VIB-011
- **Dependencies (inter-block):** BLOCK 1.1 (TASK-VIB-001) must be DONE (ensures infrastructure is stable)

### BLOCK 5.3 — TreeView Ticket State Provider (P3)

Create `extension/src/ticketTreeProvider.ts` implementing `vscode.TreeDataProvider` showing tickets grouped by stage. Update `extension/src/extension.ts` to register the provider and `extension/package.json` with `contributes.views` and `contributes.viewsContainers`.

- **Deliverable:** Sidebar panel shows ticket state tree (READY / IN-PROGRESS / DONE groups with ticket titles); refreshes on command
- **Effort:** M
- **L3 tickets:** TASK-VIB-012
- **Dependencies (inter-block):** BLOCK 1.1 (TASK-VIB-001) must be DONE

---

## Inter-Block Dependency Graph

```
BLOCK 1.1 (VIB-001) ──────────────────────────────────┬──▶ BLOCK 5.2 (VIB-011)
BLOCK 1.2 (VIB-002)  ← P0, no deps                   ├──▶ BLOCK 5.3 (VIB-012)
BLOCK 2.1 (VIB-003)  ← P0, no deps                   │
BLOCK 3.1 (VIB-004)  ← P1, no hard deps               │
BLOCK 3.2 (VIB-005, VIB-006) ← P1, no hard deps       │
BLOCK 3.3 (VIB-007) ← P1, no hard deps                │
                                                       │
BLOCK 2.1 (VIB-003) ──▶ BLOCK 4.1 (VIB-008)           │
BLOCK 2.1 (VIB-003) ──▶ BLOCK 4.2 (VIB-009)           │
                                                       │
BLOCK 4.1 + 4.2 ──────▶ BLOCK 5.1 (VIB-010)           │
                                                       │
BLOCK 1.1 ─────────────────────────────────────────────┘
```

**Critical path:** VIB-003 → VIB-008 → VIB-010 (MCP server foundation to full MCP App)
**Independent path:** VIB-001 → VIB-011/012 (infrastructure to extension UI)
**Parallel path:** VIB-004, VIB-005, VIB-006, VIB-007 (all independent P1 config changes)
