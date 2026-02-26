---
id: active-context
version: "1.0"
owner: Shared
write_access: [ALL]
append_only: true
compaction_threshold: 50
---

# Active Context

> **Schema Version:** 1.0
> **Owner:** Shared
> **Write Access:** All subagents may APPEND entries. ReaperOAK may also edit.
> **Lock Rules:** Subagents may only append timestamped entries. They may NOT
> delete, modify, or overwrite existing entries. Only ReaperOAK may archive or
> compact old entries.
> **Update Protocol:** Append new entry with timestamp, agent name, and content.
> Entries older than 50 items may be archived by ReaperOAK to
> `activeContext.archive.md`.

---

## Current Focus

<!-- What is the system currently working on? Updated per-session. -->

### [2026-02-23T00:00:00Z] Claude Code

- **Focus:** Claude Code integration — dual-agent vibecoding support
- **Status:** Claude Code fully configured alongside GitHub Copilot
- **Next Steps:** Test hooks and slash commands, begin project work

### [2026-02-21T00:00:00Z] ReaperOAK

- **Focus:** Initial vibecoding system setup
- **Status:** Building multi-agent infrastructure
- **Next Steps:** Generate subagent files, create orchestration rules

---

## Recent Changes

<!-- Reverse chronological log of significant changes -->

### [2026-02-23T00:00:00Z] Claude Code

- Created `CLAUDE.md` — primary Claude Code instruction file (equivalent to
  ReaperOAK.agent.md for Claude Code)
- Created `.claude/settings.json` — hooks configuration for governance audit,
  prompt logging, and session tracking
- Created `.claude/hooks/` — 3 hook scripts adapted from Copilot hooks:
  governance-audit-prompt.sh, log-prompt.sh, log-session-end.sh
- Created `.claude/commands/` — 5 slash commands: memory-bank-read,
  memory-bank-update, review, plan, security-audit, debug
- System now supports both GitHub Copilot and Claude Code as vibecoding agents

### [2026-02-21T00:00:00Z] ReaperOAK

- Created `.github/ARCHITECTURE.md` — full system architecture
- Created `.github/memory-bank/` — persistent state system
- Performed full repository intelligence sweep (170+ instructions, 150+ agents,
  55+ skills catalogued)

---

## Active Decisions

<!-- Decisions currently under consideration -->

- _None pending_

---

## Blockers

<!-- Current blockers preventing progress -->

- _None_

---

## Session Notes

<!-- Per-session working notes. Append only. -->

### [2026-02-21] Session 1

- Initialized vibecoding multi-agent system
- Completed Phase 1 (intelligence sweep), Phase 2 (architecture design),
  Phase 3 (memory bank)

### [2026-02-23] Session 2

- Integrated Claude Code as a vibecoding agent alongside GitHub Copilot
- Created CLAUDE.md, .claude/settings.json, hooks, and slash commands
- Full dual-agent support now operational
### [2026-02-24] Sessions 3-5 — Context Bloat Fix

- Completed all 11 hardening phases (A-K): subagent files, orchestration rules,
  security guardrails, chunk system, catalog, cross-cutting protocols,
  guardian, locks, sandbox, observability, hooks, workflows
- Created boot files: `.github/copilot-instructions.md` (45 lines) +
  `agents.md` at repo root (80 lines) — auto-load chain for all sessions
- User deleted `.github/instructions/` folder — chunks are sole source of truth
- Cleaned `catalog.yml` of stale references to deleted instruction files
- **Context bloat diagnosed:** agent files were 585-1,052 lines each, consuming
  too much context window, preventing delegation behavior
- **All 12 agent files slimmed** (total: 7,787 → 826 lines, ~89% reduction):
  - ReaperOAK: 1,052 → 84 lines
  - Architect: 666 → 61 | Backend: 711 → 68 | Frontend: 716 → 64
  - QA: 774 → 66 | Security: 769 → 65 | DevOps: 780 → 69
  - Documentation: 807 → 68 | Research: 704 → 68 | ProductManager: 585 → 67
  - CIReviewer: 614 → 65 | _cross-cutting-protocols: 493 → 81
- Each slim file preserves: YAML frontmatter, identity, scope, ALL forbidden
  actions (safety-critical), key protocols as summary table, chunk pointer
- Backups of all originals at `.bak` files in `.github/agents/`

### [2026-02-25] Session 6 — Force Delegation

- ReaperOAK still self-implementing instead of delegating — root cause: agent
  file said "Self-execute quick tasks (< 5 min)" which the model used as escape
  hatch to do everything itself
- Rewrote ReaperOAK.agent.md (84 → 102 lines) with CARDINAL RULE section:
  "YOU DO NOT IMPLEMENT" — zero self-implementation, mandatory parallel
  delegation via `runSubagent`
- Explicit whitelist of what ReaperOAK MAY do (read files, memory bank, git
  status) vs what it MUST delegate (all code, tests, docs, architecture, etc.)
- Added delegation workflow: Read → Plan → Delegate (parallel) → Validate →
  Report
- Reinforced in `agents.md` boot file: "ReaperOAK is a PURE ORCHESTRATOR"

### [2026-02-26] Session 7 — Cross-Agent Communication

- Tested Kanban build: ReaperOAK successfully delegated to 4 agents in parallel
  but (a) did all the thinking itself (architecture, API contracts, DB schema)
  instead of letting Architect do it, (b) agents couldn't see each other's
  output — Backend didn't read Architect's contracts, QA didn't read Backend's code
- **Root cause:** No dependency model — all agents launched flat in parallel with
  specs baked into the prompt by ReaperOAK, bypassing domain expertise
- **Fix: Phased Delegation with File-Based Handoff**
  - ReaperOAK now uses dependency phases (SPEC → BUILD → VALIDATE → DOCUMENT)
  - Within each phase: all agents run in parallel (no cap)
  - Between phases: ReaperOAK validates, then launches next phase
  - Each phase's files on disk become the next phase's input
  - Delegation prompt template now includes "Upstream artifacts" field
- All 10 subagent MANDATORY FIRST STEPS updated: step 3 = "Read upstream
  artifacts listed in delegation prompt BEFORE starting"
- Cross-cutting protocols: added §6 "Cross-Agent Communication (File-Based
  Handoff)" — agents must read upstream, align with prior contracts, write
  clean deliverables, and stop+report if upstream is missing
- **Next:** Fresh ReaperOAK session, re-test with Kanban prompt — expect phased
  execution with Architect/PM first, then Backend/Frontend/DevOps, then QA/Security

## Session 8 — Self-Improving System Migration (2025-07-25)

### Current Focus
- Completed full migration to self-improving multi-agent architecture
- All 6 subsystems designed and implemented

### Changes Made
1. **Shared Context Layer** — Created workflow-state.json, artifacts-manifest.json, feedback-log.md in memory bank
2. **UIDesigner Agent** — New agent with Google Stitch integration, Playwright visual validation, component specs
3. **Self-Improvement System** — Proposals directory, RETROSPECTIVE phase, auto-reject rules
4. **ReaperOAK Upgrade** — 6-phase SDLC (added RETROSPECTIVE), state management obligations, proposal handling
5. **Schema Extensions** — Delegation packet: phase, upstream_artifacts, mcp_grants, fix_loop_context, output_contract fields
6. **Architecture Update** — ARCHITECTURE.md v4.0.0 with UIDesigner, shared context layer, §18 self-improvement
7. **Catalog + ACL** — UIDesigner entries in catalog.yml, tool-acl.yaml, design: tag

### Validation Results
- QA: PASS (1 MEDIUM fixed, 2 LOW noted)
- Security: CONDITIONAL PASS (5 MEDIUM — 2 fixed, 3 accepted as design-level, 3 LOW — 1 fixed)
- CI: PASS (2 warnings fixed, 1 suggestion noted)
- Fix loop: 1 iteration — all actionable findings resolved

### Files Created (7)
- `.github/agents/UIDesigner.agent.md`
- `.github/vibecoding/chunks/UIDesigner.agent/chunk-01.yaml`
- `.github/vibecoding/chunks/UIDesigner.agent/chunk-02.yaml`
- `.github/proposals/.gitkeep`
- `.github/memory-bank/workflow-state.json`
- `.github/memory-bank/artifacts-manifest.json`
- `.github/memory-bank/feedback-log.md`

### Files Modified (7)
- `.github/agents/ReaperOAK.agent.md` — RETROSPECTIVE, UIDesigner, state mgmt, proposals
- `.github/vibecoding/catalog.yml` — UIDesigner + design tag
- `.github/sandbox/tool-acl.yaml` — UIDesigner section
- `.github/tasks/delegation-packet-schema.json` — UIDesigner + 5 new fields
- `.github/memory-bank/schema.md` — 3 new file schemas + riskRegister writers fix
- `.github/ARCHITECTURE.md` — v4.0.0, UIDesigner, shared context, self-improvement
- `.github/copilot-instructions.md` — updated repo structure

### Architecture Document
- Full design at `docs/architecture/self-improving-system.md` (1,466 lines)