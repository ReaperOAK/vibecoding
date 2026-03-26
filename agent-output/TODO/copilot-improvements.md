# TODO Agent Summary — copilot-improvements

**Ticket:** copilot-improvements (ad-hoc decomposition)  
**Stage:** TODO (L1→L2→L3)  
**Agent:** TODO  
**Date:** 2026-03-26  
**Confidence:** HIGH

---

## Executive Summary

Performed full L1→L2→L3 decomposition of 10 VS Code + GitHub Copilot system improvements identified from March 2026 documentation research. All 10 improvement areas were mapped to the L1→L2 hierarchy. Gap analysis against 39 existing tickets identified **2 uncovered features** requiring new L3 tickets.

---

## Decomposition Tree

### L1 → L2 → L3 Full Chain

```
L1-01: Agent Tool Governance (P0)
  L2-01-A: Tool Loadout Audit per Agent Role
    → TASK-ARC-013 (CTO loadout)
    → TASK-ARC-014 (Ticketer loadout)
    → TASK-ARC-015 (Implementing agents loadout)
    → TASK-ARC-016 (Review agents loadout)
  L2-01-B: Tool Set Abstractions
    → TASK-SYS-029 (Tool sets)
  L2-01-C: Coordinator Agent Scoping (agents: property)
    → TASK-SYS-008 (CTO subagent scoping)
    → TASK-SYS-009 (Ticketer subagent scoping)
  L2-01-D: Agent Reference Modernization
    → TASK-ARC-017 (Markdown links)

L1-02: Lifecycle Hook Infrastructure (P1)
  L2-02-A: Hook Directory & Base Infrastructure
    → TASK-SYS-001 (Hook directory + policy-enforcement.json)
    → TASK-SYS-007 (VS Code workspace settings)
  L2-02-B: Guardian Stop Hook (guardian.json)
    → TASK-SYS-002 (Guardian stop hook)
  L2-02-C: Git Policy Enforcement Hook (git-policy.json)
    → TASK-SYS-003 (Scoped git enforcement hook)
  L2-02-D: Auto-Sync Hook (auto-sync.json)  ← GAP
    → TASK-SYS-036 [NEW] (Auto-sync tickets hook)
  L2-02-E: Additional Policy Enforcement Hooks
    → TASK-SYS-004 (Memory gate hook)
    → TASK-SYS-005 (Evidence rule hook)
    → TASK-SYS-006 (Destructive command blocking hook)
    → TASK-SYS-018 (PostToolUse lint hook)
    → TASK-SYS-019 (Ticketer code-modification blocker)

L1-03: Agent Visibility & Scoping (P1)
  L2-03-A: Non-User-Facing Agent Visibility Flags
    → TASK-SYS-030 (user-invocable: false on 12 agents)
  L2-03-B: Pattern-Scoped Instructions
    → TASK-SYS-022 (Python file scoping)
    → TASK-SYS-023 (Agent definition file scoping)
    → TASK-SYS-024 (Git-protocol scoping)

L1-04: SDLC Handoff Chain Completeness (P1)
  L2-04-A: Implementing Agent Handoffs
    → TASK-SYS-031 (Post-impl handoff chain)
    → TASK-SYS-011 (Earlier version — superseded by SYS-031)
  L2-04-B: Review Agent Handoffs (Forward + Rework)
    → TASK-SYS-032 (Review agent rework + forward handoffs)
    → TASK-SYS-012 (Earlier version — superseded by SYS-032)
  L2-04-C: Ticketer Dispatch Handoffs
    → TASK-SYS-033 (Ticketer dispatch handoffs)
    → TASK-SYS-010 (CTO→Ticketer handoff)

L1-05: Skills & Instructions Standards (P2)
  L2-05-A: agentskills.io Standard Frontmatter
    → TASK-SYS-034 (SKILL.md frontmatter)
  L2-05-B: Skills Directory & Migration
    → TASK-SYS-025 (First chunk migration)
    → TASK-SYS-026 (Remaining chunks migration)

L1-06: Cross-Tool Compatibility (P2)
  L2-06-A: CLAUDE.md Compatibility Layer
    → TASK-DOC-001 (CLAUDE.md)
  L2-06-B: Prompt File Agent Frontmatter
    → TASK-SYS-020 (agent: in prompt files)
  L2-06-C: Prompt File Tools Frontmatter
    → TASK-SYS-021 (tools: in prompt files)
  L2-06-D: Prompt File Model Frontmatter  ← GAP
    → TASK-SYS-037 [NEW] (model: in prompt files)

L1-07: Developer Experience (P3)
  L2-07-A: Plugin Architecture Research
    → TASK-RES-001 (Research plugin packaging)
  L2-07-B: Plugin Extension Architecture Design
    → TASK-ARC-018 (Plugin extension architecture)
  L2-07-C: Plugin Extension Scaffold
    → TASK-SYS-035 (Scaffold VS Code extension)
  L2-07-D: MCP Ticket Server
    → TASK-SYS-027 (MCP server architecture)
    → TASK-SYS-028 (MCP server implementation)

L1-08: Platform Distribution (P3)
  L2-08-A: Organization-Level Deployment Guide
    → TASK-DOC-002 (Org-level deployment guide)
```

---

## Gap Analysis

### Pre-existing Coverage

39 existing tickets cover all 10 improvement areas **except** two features:

| Gap | Improvement Area | Missing Feature |
|-----|-----------------|-----------------|
| L2-02-D | #3 Lifecycle hooks | `auto-sync.json` — tickets.py --sync on SessionStart |
| L2-06-D | #8 Prompt frontmatter | `model:` field in prompt files |

TASK-SYS-020 covers `agent:` and TASK-SYS-021 covers `tools:`, but no ticket covered `model:`.  
TASK-SYS-002 covers the guardian hook and TASK-SYS-003 covers git-policy, but auto-sync was absent.

### New Tickets Created

| Ticket ID | Title | Priority | Effort | Dependencies |
|-----------|-------|----------|--------|--------------|
| TASK-SYS-036 | Create auto-sync tickets hook (SessionStart) | high | S | TASK-SYS-001 |
| TASK-SYS-037 | Add model field to prompt files | medium | XS | TASK-SYS-020 |

Both new tickets were written to `TODO/tasks/TASK-SYS-036.json` and `TODO/tasks/TASK-SYS-037.json`.

**NOTE:** TASK-SYS-036 starts BLOCKED (depends on TASK-SYS-001). TASK-SYS-037 starts BLOCKED (depends on TASK-SYS-020). After CTO runs `python3 tickets.py --parse TODO/tasks/` and `--sync`, both will enter the correct initial state.

---

## Artifacts

| Artifact | Path |
|----------|------|
| L1 Decomposition | `TODO/tasks/L1-vscode-copilot-improvements.md` |
| L2 Decomposition | `TODO/tasks/L2-vscode-copilot-improvements.md` |
| New L3 Ticket — Auto-Sync Hook | `TODO/tasks/TASK-SYS-036.json` |
| New L3 Ticket — Model Frontmatter | `TODO/tasks/TASK-SYS-037.json` |
| This Summary | `agent-output/TODO/copilot-improvements.md` |

---

## Dependency Graph for New Tickets

```
TASK-SYS-001 (hook infrastructure) ──blocked──► TASK-SYS-036 (auto-sync hook)
TASK-SYS-020 (agent: in prompts)   ──blocked──► TASK-SYS-037 (model: in prompts)
```

---

## Notes for CTO / Next Agent

1. **Do NOT run `python3 tickets.py --parse`** — the new tickets are pre-formatted JSON, not markdown task files. They should be copied to `tickets/` and `ticket-state/` directories directly, or the CTO should parse them appropriately.

2. **Superseded tickets:** TASK-SYS-011 and TASK-SYS-012 appear to be earlier implementations that were superseded by TASK-SYS-031 and TASK-SYS-032. CTO may want to close/retire them to avoid duplicate work.

3. **Critical path:** L1-01 (Agent Tool Governance) and L1-02 (Lifecycle Hook Infrastructure) are entirely P0/P1. All 21 READY tickets in these epics should be prioritized by the Ticketer immediately.

4. **Total ticket count after this run:** 41 tickets (39 existing + 2 new gap tickets).
