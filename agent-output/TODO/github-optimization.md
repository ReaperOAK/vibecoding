# TODO Agent Summary — GitHub Folder Optimization

**Date:** 2026-04-09
**Ticket:** N/A (decomposition task, not SDLC ticket)
**Mode:** Full pipeline (L0→L1→L2→L3)

---

## Decomposition Tree

```
L0: Optimize .github/ folder structure for VS Code + Copilot primitives
│
├── L1.1 Context Window Optimization (P0)
│   ├── L2 BLOCK 1.1 → TASK-GHO-SYS001: Remove applyTo from instruction files [READY]
│   └── L2 BLOCK 1.2 → TASK-GHO-SYS002: Consolidate workspace instruction files [BLOCKED→SYS001]
│
├── L1.2 Catalog & Reference Hygiene (P1)
│   ├── L2 BLOCK 2.1 → TASK-GHO-SYS003: Clean ghost references from catalog [READY]
│   └── L2 BLOCK 2.2 → TASK-GHO-SYS004: Delete duplicate skills catalog [BLOCKED→SYS003]
│
├── L1.3 Agent File Optimization (P1)
│   ├── L2 BLOCK 3.1 → TASK-GHO-SYS005: Extract shared agent rules [BLOCKED→SYS002]
│   └── L2 BLOCK 3.2 → TASK-GHO-SYS006: Trim agent files to 80 lines [BLOCKED→SYS005]
│
├── L1.4 Tool Configuration Cleanup (P2)
│   ├── L2 BLOCK 4.1 → TASK-GHO-SYS007: Remove tool-sets directory [READY]
│   ├── L2 BLOCK 4.2 → TASK-GHO-SYS008: Resolve tool-acl enforcement [READY]
│   └── L2 BLOCK 4.3 → TASK-GHO-SYS009: Fix hook toolNames [READY]
│
└── L1.5 Skills & Directory Cleanup (P2-P3)
    ├── L2 BLOCK 5.1 → TASK-GHO-DOC001: Audit and consolidate shallow skills [READY]
    └── L2 BLOCK 5.2 → TASK-GHO-SYS010: Remove unused infrastructure directories [READY]
```

## Generated Ticket IDs

| Ticket ID | Title | Type | Priority | Effort | State |
|-----------|-------|------|----------|--------|-------|
| TASK-GHO-SYS001 | Remove applyTo from instruction files | infra | critical | S | READY |
| TASK-GHO-SYS002 | Consolidate workspace instruction files | infra | critical | M | BLOCKED |
| TASK-GHO-SYS003 | Clean ghost references from catalog | infra | high | XS | READY |
| TASK-GHO-SYS004 | Delete duplicate skills catalog | infra | high | XS | BLOCKED |
| TASK-GHO-SYS005 | Extract shared agent rules into instruction file | infra | high | M | BLOCKED |
| TASK-GHO-SYS006 | Trim agent files to 80 lines | infra | high | L | BLOCKED |
| TASK-GHO-SYS007 | Remove tool-sets directory | infra | medium | XS | READY |
| TASK-GHO-SYS008 | Resolve tool-acl enforcement | infra | medium | S | READY |
| TASK-GHO-SYS009 | Fix hook toolNames to match VS Code | infra | medium | XS | READY |
| TASK-GHO-DOC001 | Audit and consolidate shallow skills | docs | medium | L | READY |
| TASK-GHO-SYS010 | Remove unused infrastructure directories | infra | low | XS | READY |

## Dependency Graph

```
TASK-GHO-SYS001 ──→ TASK-GHO-SYS002 ──→ TASK-GHO-SYS005 ──→ TASK-GHO-SYS006
TASK-GHO-SYS003 ──→ TASK-GHO-SYS004
TASK-GHO-SYS007 (independent)
TASK-GHO-SYS008 (independent)
TASK-GHO-SYS009 (independent)
TASK-GHO-DOC001 (independent)
TASK-GHO-SYS010 (independent)
```

**Critical path:** SYS001 → SYS002 → SYS005 → SYS006 (4 tickets, longest chain)

## Artifacts Created

- `TODO/L1-github-optimization.md` — L1 capability breakdown (5 capabilities)
- `TODO/L2-github-optimization.md` — L2 execution blocks (10 blocks)
- `TODO/tasks/L3-github-optimization.md` — L3 ticket definitions (11 tickets)
- `tickets/TASK-GHO-*.json` — 11 ticket JSON files
- `ticket-state/READY/TASK-GHO-*.json` — 7 tickets in READY state
- `agent-output/TODO/github-optimization.md` — This summary

## Confidence Level

**HIGH** — All 10 CTO audit findings are mapped to specific tickets with testable acceptance criteria, accurate file paths verified against the filesystem, and dependency chains validated by `tickets.py --sync`.

## Notes

- Parser quirk: `**Dependencies:**` with empty value caused `_extract_field` regex to capture across newlines. Fixed by omitting the field for independent tickets (parser correctly defaults to `[]`).
- All TASK-GHO-* tickets use `infra` type except TASK-GHO-DOC001 which uses `docs` type. Per SDLC flow, infra tickets route through DevOps stage.
- 7 of 11 tickets are immediately actionable in READY state; 4 are correctly BLOCKED on dependency chains.
