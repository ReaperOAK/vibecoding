# Vibecoding

last_reviewed: 2026-04-09

A ticket-driven multi-agent SDLC system for GitHub Copilot. Decomposes work into tickets, routes them through 14 specialized agents (Research → Architect → Backend → Frontend → QA → Security → CI → Docs → Validator), and enforces scoped git commits at every stage.

---

## Install into your project

Run this once from your project root to pull the latest agent infrastructure:

```bash
# One-liner: download and run the sync script
curl -fsSL https://raw.githubusercontent.com/ReaperOAK/vibecoding/main/scripts/sync-vibecoding.sh | bash
```

Or if you already have the script locally:

```bash
bash scripts/sync-vibecoding.sh          # sync from main
bash scripts/sync-vibecoding.sh <branch>  # sync from a specific branch
DRY_RUN=1 bash scripts/sync-vibecoding.sh  # preview changes without writing
```

**What it does:** Merges `.github/` agent infrastructure into your project. Never deletes local files — only adds or overwrites files that exist in upstream. Protected paths that are never touched: `memory-bank/`, `tickets/`, `ticket-state/`, `agent-output/`, `copilot-instructions.md`.

After syncing, commit the changes:

```bash
git add .github/ AGENTS.md todo_visual.py
git commit -m "chore: sync vibecoding infrastructure"
```

---

## How it works

**Ticketer** is a stateless dispatcher. It scans `ticket-state/READY/`, performs a CLAIM commit (distributed lock via git push), then dispatches a subagent to do the work. The subagent performs one WORK commit and exits.

```
READY → [impl stage] → QA → SECURITY → CI → DOCS → VALIDATION → DONE
```

| Ticket type | Flow |
|-------------|------|
| backend | READY → BACKEND → QA → SECURITY → CI → DOCS → VALIDATION → DONE |
| frontend | READY → UIDesigner → FRONTEND → QA → SECURITY → CI → DOCS → VALIDATION → DONE |
| fullstack | READY → BACKEND → FRONTEND → QA → SECURITY → CI → DOCS → VALIDATION → DONE |
| research | READY → RESEARCH → DOCS → VALIDATION → DONE |
| architecture | READY → ARCHITECT → DOCS → VALIDATION → DONE |
| docs | READY → DOCS → VALIDATION → DONE |

Max 3 rework attempts (shared across QA/Security/CI/Validator) before escalation to operator.

---

## Agents

| Agent | Stage | Role |
|-------|-------|------|
| CTO | pre-SDLC | Reads docs, delegates Research/PM/Architect/TODO to build ticket backlog |
| Ticketer | dispatcher | Scans READY tickets, performs CLAIM commits, dispatches subagents |
| TODO | pre-SDLC | Decomposes vision → L1 capabilities → L2 blocks → L3 tickets |
| Research Analyst | RESEARCH | Evidence-based research, PoC, tech comparison |
| ProductManager | PM | PRD, user stories, acceptance criteria |
| Architect | ARCHITECT | System design, ADRs, API contracts, DB schema |
| DevOps | BACKEND (infra) | IaC, CI/CD, Docker, monitoring |
| Backend | BACKEND | APIs, business logic, database operations |
| UIDesigner | UIDesigner | Stitch mockups, design tokens, component specs |
| Frontend  | FRONTEND | UI components, WCAG 2.2 AA, Core Web Vitals |
| QA | QA | Tests ≥80% coverage, mutation testing, E2E |
| Security | SECURITY | STRIDE, OWASP Top 10, SBOM |
| CIReviewer | CI | Lint, type checks, complexity, SARIF findings |
| Documentation | DOCS | JSDoc/TSDoc, README, Diataxis structure |
| Validator | VALIDATION | Independent 10-item Definition of Done verification |

---

## Definition of Done

Every ticket must pass all 10 items before reaching DONE:

1. All acceptance criteria implemented
2. Tests written (≥80% coverage for new code)
3. Lint passes (zero errors, zero warnings)
4. Type checks pass
5. CI passes
6. Docs updated (JSDoc/TSDoc, README if applicable)
7. Validator independently reviewed
8. No console errors (structured logger only)
9. No unhandled promises
10. No TODO comments in code

---

## Repository structure

```
.github/
  agents/          14 agent definitions (*.agent.md) — each has tool-sets: frontmatter
  instructions/    6 canonical instruction files (system rules)
  tickets/         Ticket JSON + schema
  ticket-state/    File-based state machine (READY → DONE)
  agent-output/    Stage handoff summaries ({Agent}/{ticket-id}.md)
  memory-bank/     Persistent shared state (append-only)
  vibecoding/      catalog.yml — skill chunk index loaded by agents during boot
  hooks/           Governance hooks (policy-enforcement, auto-sync) — all enabled
  tool-sets/       Reusable tool-set configs (universal, research, code-editing)
  mcp-servers/     MCP server wrappers (ticket-server for typed ticket ops)
  guardian/        Circuit breaker (STOP_ALL)
  tickets.py       Ticket state manager (--sync --claim --advance --status)

AGENTS.md          Boot protocol — loaded on every agent interaction
todo_visual.py     CLI dashboard for ticket state
scripts/
  sync-vibecoding.sh  Merge upstream agent infrastructure into your project
TODO/              Task decomposition artifacts (vision → capabilities → blocks → tasks)
```

---

## Starting a new project

```bash
# 1. Sync infrastructure
bash scripts/sync-vibecoding.sh

# 2. Open GitHub Copilot in Agent Mode and invoke CTO:
#    "You are CTO. Initialize this project: <your vision>"
#
# CTO will:
#   - Read existing docs/code
#   - Delegate to Research Analyst, ProductManager, Architect
#   - Run TODO agent to generate tickets
#   - Sync ticket state: python3 tickets.py --sync
#
# 3. Once tickets exist in READY, run Ticketer:
#    "You are Ticketer. Process all READY tickets."

# Check ticket status anytime
python3 tickets.py --status
python3 todo_visual.py
```

---

## Prerequisites

- VS Code with GitHub Copilot (Agent Mode enabled)
- Git with commit permissions on the target repo
- Python 3 (for `tickets.py`)

---

## VS Code Ticket Tree

The extension contributes a sidebar view named `Vibecoding Tickets` (view id: `vibecoding.tickets`).

It renders three root groups:

- `READY` — tickets from `ticket-state/READY/`
- `IN_PROGRESS` — aggregated tickets from active stage directories (`RESEARCH`, `PM`, `ARCHITECT`, `DEVOPS`, `BACKEND`, `UIDESIGNER`, `FRONTEND`, `QA`, `SECURITY`, `CI`, `DOCS`, `VALIDATION`)
- `DONE` — tickets from `ticket-state/DONE/`

Run `vibecoding.refreshTickets` from the Command Palette to reload all groups from disk.

---

## MCP Ticket Server

An MCP server wraps `tickets.py` for typed access via the Model Context Protocol. Located at `.github/mcp-servers/ticket-server/server.py`, it provides 7 tools and 3 resources over stdio transport.

Last reviewed: 2026-04-09

When the VS Code extension is installed, the ticket MCP server is auto-registered through `contributes.mcpServerDefinitionProviders` and `vscode.lm.registerMcpServerDefinitionProvider`.
You do not need to manually create `.vscode/mcp.json` for this server in normal usage.

### Tools

| Tool | Purpose |
|------|---------|
| `syncTickets` | Release expired claims, resolve deps, move unblocked to READY |
| `getStatus` | Dashboard view (text or JSON) |
| `claimTicket` | Claim a READY ticket for an agent |
| `advanceTicket` | Move ticket to next SDLC stage |
| `releaseTicket` | Release a stale claim |
| `reworkTicket` | Send back for rework with reason |
| `validateIntegrity` | Full integrity check |

### Resources

| Resource | Returns |
|----------|---------|
| `ticket://READY` | JSON array of READY ticket summaries (`id`, `title`, `type`, `priority`) |
| `ticket://DONE` | JSON array of DONE ticket summaries with `completed_at` |
| `ticket://{ticket_id}` | Full ticket JSON for a valid ticket ID |

Invalid ticket resource IDs return a not-found error. Ticket IDs are validated against the server allowlist format before file access.

Setup: `pip install -r .github/mcp-servers/ticket-server/requirements.txt`

Server registration details:

- Provider ID: `vibecoding.ticket-server`
- Command: `python3`
- Script path: `.github/mcp-servers/ticket-server/server.py`
- Working directory: workspace root
- Environment: `VIBECODING_WORKSPACE_ROOT` and `PYTHONUNBUFFERED=1`

---

## Agent Configuration

Each agent's `.agent.md` file includes frontmatter properties that control behavior:

- **`tool-sets:`** — References reusable tool configurations from `.github/tool-sets/` (e.g., `#universal`, `#research`, `#code-editing`)
- **`agents:`** — Restricts which subagents a coordinator can invoke (Ticketer dispatches all 13 workers; CTO invokes 5 strategic agents)
- **`user-invocable:`** — Only Ticketer and CTO are `true`; all workers are `false` (dispatched by coordinators only)
- **`model:`** — Review-chain agents (QA, CI, Validator, Documentation) use cost-efficient model arrays `[claude-3-7-sonnet, claude-3-5-sonnet]`; implementation agents use the default model

---

## License

See [LICENSE](LICENSE) for details.
