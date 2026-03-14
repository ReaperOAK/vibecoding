# Vibecoding

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
git add .github/ agents.md todo_visual.py
git commit -m "chore: sync vibecoding infrastructure"
```

---

## How it works

**Ticketer** is a stateless dispatcher. It scans `.github/ticket-state/READY/`, performs a CLAIM commit (distributed lock via git push), then dispatches a subagent to do the work. The subagent performs one WORK commit and exits.

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
| Product Manager | PM | PRD, user stories, acceptance criteria |
| Architect | ARCHITECT | System design, ADRs, API contracts, DB schema |
| DevOps Engineer | BACKEND (infra) | IaC, CI/CD, Docker, monitoring |
| Backend | BACKEND | APIs, business logic, database operations |
| UIDesigner | UIDesigner | Stitch mockups, design tokens, component specs |
| Frontend Engineer | FRONTEND | UI components, WCAG 2.2 AA, Core Web Vitals |
| QA Engineer | QA | Tests ≥80% coverage, mutation testing, E2E |
| Security Engineer | SECURITY | STRIDE, OWASP Top 10, SBOM |
| CI Reviewer | CI | Lint, type checks, complexity, SARIF findings |
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
  agents/          14 agent definitions (*.agent.md)
  instructions/    6 canonical instruction files (system rules)
  tickets/         Ticket JSON + schema
  ticket-state/    File-based state machine (READY → DONE)
  agent-output/    Stage handoff summaries ({Agent}/{ticket-id}.md)
  memory-bank/     Persistent shared state (append-only)
  vibecoding/      Token-budgeted YAML instruction chunks + catalog
  guardian/        Circuit breaker (STOP_ALL)
  tickets.py       Ticket state manager (--sync --claim --advance --status)
  agent-runner.py  Dispatcher-claim protocol runner

agents.md          Boot protocol — loaded on every agent interaction
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
#   - Delegate to Research Analyst, Product Manager, Architect
#   - Run TODO agent to generate tickets
#   - Sync ticket state: python3 .github/tickets.py --sync
#
# 3. Once tickets exist in READY, run Ticketer:
#    "You are Ticketer. Process all READY tickets."

# Check ticket status anytime
python3 .github/tickets.py --status
python3 todo_visual.py
```

---

## Prerequisites

- VS Code with GitHub Copilot (Agent Mode enabled)
- Git with commit permissions on the target repo
- Python 3 (for `tickets.py`)

---

## License

See [LICENSE](LICENSE) for details.
