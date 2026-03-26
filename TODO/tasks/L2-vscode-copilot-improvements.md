# L2 Decomposition: VS Code + GitHub Copilot System Improvements (March 2026)

**Project:** vibecoding multi-agent system — 10 targeted improvements  
**Decomposition Level:** L2 (Epics → Features)  
**Date:** 2026-03-26  
**Author:** TODO Agent  

---

## L1-01: Agent Tool Governance

### L2-01-A: Tool Loadout Audit per Agent Role
**Description:** Audit every `.github/agents/*.agent.md` file and reduce the `tools:` array to only the tools authorized in that agent's `Assigned Tool Loadout` section. Remove the current 240+ kitchen-sink list.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-ARC-013 | Audit and tighten CTO tool loadout | READY |
| TASK-ARC-014 | Audit and tighten Ticketer tool loadout | READY |
| TASK-ARC-015 | Audit and tighten implementing agent tool loadouts | READY |
| TASK-ARC-016 | Audit and tighten review agent tool loadouts | READY |

### L2-01-B: Tool Set Abstractions
**Description:** Create named tool sets (e.g., `universal-tools`, `cto-tools`, `backend-tools`) to replace repeating individual tool listings across agent files. Reduces maintenance surface.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-SYS-029 | Create tool sets for common tool groupings | READY |

### L2-01-C: Coordinator Agent Scoping (`agents:` property)
**Description:** Add `agents: [...]` frontmatter to CTO and Ticketer to restrict which subagents they may invoke via `runSubagent`. Prevents unauthorized agent dispatch.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-SYS-008 | Add subagent scoping to CTO agent | READY |
| TASK-SYS-009 | Add subagent scoping to Ticketer agent | READY |

### L2-01-D: Agent Reference Modernization
**Description:** Convert all inline agent cross-references in `.agent.md` files to Markdown links pointing to canonical agent files.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-ARC-017 | Convert all agent reference sections to Markdown links | READY |

---

## L1-02: Lifecycle Hook Infrastructure

### L2-02-A: Hook Directory & Base Infrastructure
**Description:** Create `.github/hooks/` directory with base `policy-enforcement.json` configuration and `scripts/` subdirectory. Establish the hook registry schema.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-SYS-001 | Create hook infrastructure directory and base configuration | READY |
| TASK-SYS-007 | Configure VS Code workspace settings for hooks and agent features | BLOCKED (dep: SYS-001) |

### L2-02-B: Guardian Stop Hook (`guardian.json`)
**Description:** Implement `guardian.json` hook that reads `.github/guardian/STOP_ALL` on SessionStart and PreToolUse. Returns `permissionDecision: "deny"` when STOP is present.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-SYS-002 | Implement guardian stop hook (SessionStart + PreToolUse) | BLOCKED (dep: SYS-001) |

### L2-02-C: Git Policy Enforcement Hook (`git-policy.json`)
**Description:** Implement `git-policy.json` hook that intercepts PreToolUse for shell commands and blocks `git add .`, `git add -A`, `git add --all`. Enforces explicit staging per the git protocol.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-SYS-003 | Implement scoped git enforcement hook (PreToolUse) | BLOCKED (dep: SYS-001) |

### L2-02-D: Auto-Sync Hook (`auto-sync.json`)
**Description:** Implement `auto-sync.json` hook that runs `python3 tickets.py --sync` on SessionStart to automatically resolve dependencies and move unblocked tickets to READY before each agent session begins.

| Ticket | Title | Status |
|--------|-------|--------|
| **TASK-SYS-036** | **Create auto-sync tickets hook (SessionStart)** | **NEW TICKET NEEDED** |

### L2-02-E: Additional Policy Enforcement Hooks
**Description:** Implement remaining hook types: memory gate enforcement (SubagentStop), evidence rule enforcement (Stop), destructive command blocking (PreToolUse), PostToolUse lint, and Ticketer code-modification blocker.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-SYS-004 | Implement memory gate enforcement hook (SubagentStop) | BLOCKED (dep: SYS-001) |
| TASK-SYS-005 | Implement evidence rule enforcement hook (Stop) | BLOCKED (dep: SYS-001) |
| TASK-SYS-006 | Implement destructive command blocking hook (PreToolUse) | BLOCKED (dep: SYS-001) |
| TASK-SYS-018 | Add agent-scoped PostToolUse lint hook to implementing agents | BLOCKED |
| TASK-SYS-019 | Add agent-scoped PreToolUse hook to Ticketer to block code modifications | BLOCKED |

---

## L1-03: Agent Visibility & Scoping

### L2-03-A: Non-User-Facing Agent Visibility Flags
**Description:** Add `user-invocable: false` to the frontmatter of all 12 dispatch-only agents (Backend, Frontend, QA, Security, DevOps, Documentation, CIReviewer, Validator, Architect, Research, ProductManager, UIDesigner). These agents should only be invoked by Ticketer/CTO.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-SYS-030 | Set non-user-facing visibility on dispatch-only agents | READY |

### L2-03-B: Pattern-Scoped Instructions
**Description:** Add `applyTo` pattern scoping to instruction files so they only activate in relevant file/directory contexts. Reduces noise and context consumption.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-SYS-022 | Create pattern-scoped instruction for Python files | READY |
| TASK-SYS-023 | Create pattern-scoped instruction for agent definition files | READY |
| TASK-SYS-024 | Review and optimize git-protocol instruction scoping | READY |

---

## L1-04: SDLC Handoff Chain Completeness

### L2-04-A: Implementing Agent Handoffs
**Description:** Add `handoffs:` frontmatter to all implementing agents (Backend, Frontend, UIDesigner, DevOps, Architect, Research, ProductManager) declaring their post-work destination (QA stage).

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-SYS-031 | Add complete post-impl handoff chain to implementing agents | READY |
| TASK-SYS-011 | Add SDLC stage handoffs to implementing agents | BLOCKED (superseded by SYS-031) |

### L2-04-B: Review Agent Handoffs (Forward + Rework)
**Description:** Add `handoffs:` frontmatter to all review agents (QA, Security, CIReviewer, Validator) with both forward (pass) and rework (fail) destinations. QA→Security on pass, QA→REWORK on fail.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-SYS-032 | Add rework and forward handoffs to all review agents | READY |
| TASK-SYS-012 | Add rework handoffs to review agents | BLOCKED (superseded by SYS-032) |

### L2-04-C: Ticketer Dispatch Handoffs
**Description:** Add `handoffs:` frontmatter to Ticketer mapping each SDLC stage to its corresponding agent. Enables Ticketer to route tickets without manual agent selection.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-SYS-033 | Add Ticketer dispatch handoffs for all stage agents | READY |
| TASK-SYS-010 | Add CTO to Ticketer handoff | BLOCKED (dep: SYS-009) |

---

## L1-05: Skills & Instructions Standards

### L2-05-A: agentskills.io Standard Frontmatter
**Description:** Update all `.github/skills/*/SKILL.md` files to include proper `name`, `description`, `user-invocable`, and `disable-model-invocation` frontmatter per the agentskills.io standard.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-SYS-034 | Add agentskills.io standard frontmatter to all SKILL.md files | BLOCKED (dep: SYS-025) |

### L2-05-B: Skills Directory & Migration
**Description:** Create the `.github/skills/` directory structure following the agentskills.io layout and migrate vibecoding knowledge chunks into skill format.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-SYS-025 | Create skills directory and migrate first chunk | READY |
| TASK-SYS-026 | Migrate remaining vibecoding chunks to skills format | BLOCKED (dep: SYS-025) |

---

## L1-06: Cross-Tool Compatibility

### L2-06-A: CLAUDE.md Compatibility Layer
**Description:** Create `CLAUDE.md` at workspace root (and optionally `.claude/agents/` symlinks) pointing to `.github/agents/` and `.github/instructions/` so the vibecoding system works with Claude-based workflows without duplication.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-DOC-001 | Create CLAUDE.md for cross-tool compatibility | READY |

### L2-06-B: Prompt File Agent Frontmatter
**Description:** Add `agent:` field to all 6 `.github/prompts/*.prompt.md` files so invoking a prompt automatically selects the correct agent. `/start` → CTO, `/continue` → Ticketer, etc.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-SYS-020 | Add agent field to all prompt files | READY |

### L2-06-C: Prompt File Tools Frontmatter
**Description:** Add `tools:` field to prompt files to scope tool availability per workflow. `/start` uses research/planning tools; `figma-to-code` uses Figma MCP tools.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-SYS-021 | Add tools field to prompt files | BLOCKED (dep: SYS-020) |

### L2-06-D: Prompt File Model Frontmatter
**Description:** Add `model:` field to prompt files to specify the preferred LLM model for each workflow. Ensures consistent execution context especially for compute-intensive workflows.

| Ticket | Title | Status |
|--------|-------|--------|
| **TASK-SYS-037** | **Add model field to prompt files** | **NEW TICKET NEEDED** |

---

## L1-07: Developer Experience

### L2-07-A: Plugin Architecture Research
**Description:** Research VS Code agent plugin packaging requirements — what goes in `package.json`, how agents/skills/hooks are declared as extension assets, and VSIX distribution model.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-RES-001 | Research VS Code agent plugin packaging requirements | READY |

### L2-07-B: Plugin Extension Architecture Design
**Description:** Design the VS Code extension architecture: `package.json` manifest structure, activation events, contribution points for agents/skills/hooks, and bundled MCP server declarations.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-ARC-018 | Design VS Code agent plugin extension architecture | BLOCKED (dep: RES-001) |

### L2-07-C: Plugin Extension Scaffold
**Description:** Scaffold the `vibecoding-copilot-plugin/` directory with `package.json`, `src/extension.ts`, `tsconfig.json`, and build config based on ARC-018 design.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-SYS-035 | Scaffold VS Code extension for agent plugin | BLOCKED (dep: ARC-018) |

### L2-07-D: MCP Ticket Server
**Description:** Design and implement an MCP server that wraps `tickets.py` functionality as MCP tools, enabling agents to query ticket state through the standard MCP protocol.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-SYS-027 | Design MCP ticket server architecture | READY |
| TASK-SYS-028 | Implement MCP ticket server | BLOCKED (dep: SYS-027) |

---

## L1-08: Platform Distribution

### L2-08-A: Organization-Level Deployment Guide
**Description:** Document how to distribute the vibecoding agent system at GitHub organization level via `github.copilot.chat.codeGeneration.instructions` org policy and team-level configuration.

| Ticket | Title | Status |
|--------|-------|--------|
| TASK-DOC-002 | Create organization-level agent deployment guide | BLOCKED (dep: SYS-035) |

---

## Gap Summary

Two gaps identified requiring new tickets:

| New Ticket | L2 Feature | Description |
|------------|------------|-------------|
| TASK-SYS-036 | L2-02-D | Auto-sync hook (`auto-sync.json`) — run `tickets.py --sync` on SessionStart |
| TASK-SYS-037 | L2-06-D | Add `model:` frontmatter field to all prompt files |

All other improvement areas are fully covered by the 39 existing tickets.
