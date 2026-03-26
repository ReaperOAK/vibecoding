# Agent Output: TODO — Vibecoding System Improvements

**Agent:** TODO  
**Date:** 2026-03-26T00:00:00Z  
**Decomposition Mode:** Full Pipeline (L1 → L2 → L3)  
**Source:** CTO delegation — vibecoding system improvements (12 items, P0–P3)

---

## Decomposition Tree

### L0 Vision
> Upgrade the vibecoding multi-agent SDLC system to leverage the latest VS Code/GitHub Copilot platform APIs, fix critical infrastructure bugs, and improve agent governance quality and cost efficiency.

### L1 Capabilities (5 domains)
1. **Infrastructure Integrity** — Fix catalog path bug + enable governance hooks (P0)
2. **MCP Server Core Transport** — FastMCP stdio transport layer (P0)
3. **Agent Governance Configuration** — Tool-sets wiring, agents property, user-invocable, model optimization (P1)
4. **MCP Server Feature Enhancements** — Resources + Prompts API (P2)
5. **Extension Platform** — MCP App registration, chat participant, TreeView (P3)

### L2 Execution Blocks (11 blocks)
- BLOCK 1.1: Fix catalog path (VIB-001)
- BLOCK 1.2: Enable governance hooks (VIB-002)
- BLOCK 2.1: FastMCP transport (VIB-003)
- BLOCK 3.1: Wire tool-sets (VIB-004)
- BLOCK 3.2: Platform agent restrictions (VIB-005, VIB-006)
- BLOCK 3.3: Model optimization (VIB-007)
- BLOCK 4.1: MCP Resources (VIB-008)
- BLOCK 4.2: MCP Prompts (VIB-009)
- BLOCK 5.1: MCP App registration (VIB-010)
- BLOCK 5.2: Chat participant (VIB-011)
- BLOCK 5.3: TreeView provider (VIB-012)

### L3 Tickets (12 tickets)

| Ticket ID | Title | Type | Priority | Status | Depends On |
|-----------|-------|------|----------|--------|------------|
| TASK-VIB-001 | Fix Catalog Path — Create .github/vibecoding/ Directory | infra | critical | READY | — |
| TASK-VIB-002 | Enable All Governance Hooks | infra | critical | READY | — |
| TASK-VIB-003 | Rewrite MCP Ticket Server with FastMCP Transport | backend | critical | READY | — |
| TASK-VIB-004 | Wire Tool-Sets to All Agent Frontmatter | infra | high | READY | — |
| TASK-VIB-005 | Add Agents Property to Coordinator Agent Files | infra | high | READY | — |
| TASK-VIB-006 | Set user-invocable:false on All Worker Agents | infra | medium | READY | — |
| TASK-VIB-007 | Update Review-Chain Agent Models to Cost-Efficient Arrays | infra | medium | READY | — |
| TASK-VIB-008 | Add MCP Resources to Ticket Server | backend | high | BLOCKED | TASK-VIB-003 |
| TASK-VIB-009 | Add MCP Prompts to Ticket Server | backend | medium | BLOCKED | TASK-VIB-003 |
| TASK-VIB-010 | Register MCP Ticket Server as MCP App via Extension | backend | medium | BLOCKED | TASK-VIB-008, TASK-VIB-009 |
| TASK-VIB-011 | Add @vibecoding Chat Participant to VS Code Extension | backend | medium | BLOCKED | TASK-VIB-001 |
| TASK-VIB-012 | Add TreeView Provider for Ticket State | backend | medium | BLOCKED | TASK-VIB-001 |

---

## Artifacts Created

- `TODO/L1-vibecoding-improvements.md` — L1 capability breakdown (5 domains)
- `TODO/L2-vibecoding-improvements.md` — L2 execution blocks (11 blocks, dependency graph)
- `TODO/tasks/L3-vibecoding-improvements.md` — L3 tickets in parseable format
- `tickets/TASK-VIB-001.json` through `tickets/TASK-VIB-012.json` — 12 ticket JSON files
- `ticket-state/READY/TASK-VIB-001.json` through `ticket-state/READY/TASK-VIB-007.json` — 7 READY state copies

---

## Dependency Graph

```
TASK-VIB-001 ──────────────────────────┬──▶ TASK-VIB-011 (BLOCKED)
TASK-VIB-002  [READY, no deps]         ├──▶ TASK-VIB-012 (BLOCKED)
TASK-VIB-003  [READY, no deps]         │
TASK-VIB-004  [READY, no deps]         │
TASK-VIB-005  [READY, no deps]         │
TASK-VIB-006  [READY, no deps]         │
TASK-VIB-007  [READY, no deps]         │
                                       │
TASK-VIB-003 ──▶ TASK-VIB-008 ─────┐  │
TASK-VIB-003 ──▶ TASK-VIB-009 ─┬──┴──▶ TASK-VIB-010 (BLOCKED)
                                └──────▶ (unblocks TASK-VIB-010 when DONE)
```

**Critical path:** VIB-003 → VIB-008+009 → VIB-010  
**Infrastructure path:** VIB-001 → VIB-011 + VIB-012  

---

## Test Results

N/A — TODO agent does not execute code. Tickets parsed successfully via `python3 tickets.py --parse TODO/tasks/`. Sync confirmed 7 READY, 5 blocked with valid dependency references. Integrity check passed.

---

## Confidence Level

**HIGH** — All 12 items from the research brief are covered. Dependency graph is logically correct (P0→P1→P2→P3 ordering encoded as hard deps where technically required). File paths are accurate based on workspace exploration. SDLC types match agent capabilities.
