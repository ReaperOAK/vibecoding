# Updated Ticket State Machine & Commit Enforcement — Execution Blocks

**Parent:** CAP-01 from vision.md
**Capability:** Updated Ticket State Machine & Commit Enforcement
**Created:** 2026-02-27T00:00:00Z
**Task Prefix:** WPAE

---

## State Name Migration Reference

Current (v7) → New (v8):

| Current State | New State | Notes |
|---------------|-----------|-------|
| BACKLOG | *(removed from main 9)* | Tickets enter at READY; pre-READY filtering is implicit |
| READY | READY | Unchanged — initial eligible state |
| LOCKED | LOCKED | Unchanged — selected for execution |
| IMPLEMENTING | IMPLEMENTING | Unchanged — agent working |
| REVIEW | QA_REVIEW | Renamed — clarifies QA + Validator review stage |
| VALIDATED | VALIDATION | Renamed — noun form, review outcome stage |
| DOCUMENTED | DOCUMENTATION | Renamed — noun form, doc update stage |
| COMMITTED | CI_REVIEW | **New** — explicit CI review stage (was implicit) |
| *(new)* | COMMIT | **New** — atomic commit creation stage |
| DONE | DONE | Unchanged — terminal state |
| REWORK | REWORK | Unchanged — failure side-state |

**New canonical progression:**
```
READY → LOCKED → IMPLEMENTING → QA_REVIEW → VALIDATION → DOCUMENTATION → CI_REVIEW → COMMIT → DONE
```
**Failure path:** → REWORK → IMPLEMENTING (rework_count ≤ 3) | READY (rework_count > 3)

---

## BLK-01: Core State Machine Rewrite

**Description:** Rewrite the canonical 9-state ticket machine definition in `ReaperOAK.agent.md` — the single source of truth for state names, transition rules, guard conditions, failure paths, and timeout semantics. Add the new state vocabulary (READY through DONE), update all transition tables with renamed states, define the REWORK failure path, implement per-ticket atomic commit enforcement rules, and add conflict detection logic for file paths, directories, DB schemas, infrastructure resources, and config files. This block produces the authoritative state definition that all other blocks reference.

**Effort:** 2–3 days
**Depends On:** None
**UI Touching:** No

**Scope includes:**
- 9-state progression with new names (READY → ... → DONE)
- REWORK side-state with rework_count semantics
- Transition table (From → To → Trigger → Guard)
- Per-ticket atomic commit enforcement (one commit per ticket, format: `[TICKET-ID] description`)
- Conflict detection rules (file path, directory, DB schema, infra resource, config file overlap)
- Backward compatibility mapping (old state names → new)
- Lock timeout semantics (LOCKED → READY on timeout)

**Primary file:** `.github/agents/ReaperOAK.agent.md`

---

## BLK-02: Agent Definition Propagation

**Description:** Propagate the new state vocabulary across all agent definition files (`.agent.md`) and the boot protocol (`agents.md`). Every file that references ticket states — in prose, tables, ASCII diagrams, status enums, or event protocol definitions — must be updated to use the new names from BLK-01. This includes updating the mandatory post-execution chain description, event emission protocol (`TASK_STARTED`, `TASK_COMPLETED`, etc.), and the 9-state machine summary in the boot protocol.

**Effort:** 1–2 days
**Depends On:** BLK-01
**UI Touching:** No

**Scope includes:**
- `agents.md` — boot protocol state machine summary, status values, state descriptions
- `.github/agents/TODO.agent.md` — status enum, state references, backward compatibility table
- `.github/agents/_cross-cutting-protocols.md` — event protocol state references, post-execution chain states
- `.github/agents/Validator.agent.md` — state references in validation matrix and review protocol

**Not in scope:** Chunk YAML files (→ BLK-03), JSON schemas (→ BLK-04)

---

## BLK-03: Chunk Content Updates

**Description:** Update all YAML chunk files that contain state machine definitions, state value enums, transition tables, status validation rules, or backward compatibility mappings. Chunks are the sole source of truth for agent runtime guidance, so they must exactly mirror the canonical definitions established in BLK-01. This block covers TODO agent chunks and Validator agent chunks.

**Effort:** 1–2 days
**Depends On:** BLK-01
**UI Touching:** No

**Scope includes:**
- `.github/vibecoding/chunks/TODO.agent/chunk-01.yaml` — Format A status values, status enum list
- `.github/vibecoding/chunks/TODO.agent/chunk-02.yaml` — 9-state diagram, state table, transition rules, backward compatibility mapping, post-execution chain states, completion gates
- `.github/vibecoding/chunks/Validator.agent/chunk-01.yaml` — state matrix references, validation stage names

**Not in scope:** Agent `.md` files (→ BLK-02), JSON schemas (→ BLK-04)

---

## BLK-04: Schema & Infrastructure Alignment

**Description:** Update all supporting infrastructure files — JSON schemas, guardian loop-detection rules, sandbox ACLs, and definition-of-done templates — to reflect the new state vocabulary. These files are consumed by CI workflows, governance hooks, and agent tooling, so state enum values must be consistent with the canonical definition from BLK-01. This block also covers any references to state names in delegation packet schemas and task lifecycle documentation.

**Effort:** 1–2 days
**Depends On:** BLK-01
**UI Touching:** No

**Scope includes:**
- `.github/tasks/delegation-packet-schema.json` — state enum in JSON schema
- `.github/guardian/loop-detection-rules.md` — state references in stall/loop detection rules
- `.github/sandbox/tool-acl.yaml` — state references in ACL annotations
- `.github/tasks/definition-of-done-template.md` — state references in lifecycle checklist

**Not in scope:** Agent `.md` files (→ BLK-02), chunk YAML files (→ BLK-03)

---

## Block Dependency Graph

```
BLK-01 (Core State Machine Rewrite)
  │
  ├──► BLK-02 (Agent Definition Propagation)
  │
  ├──► BLK-03 (Chunk Content Updates)
  │
  └──► BLK-04 (Schema & Infrastructure Alignment)
```

**Critical path:** BLK-01 → any of {BLK-02, BLK-03, BLK-04} (parallel after BLK-01)

---

## Summary

| Block | Name | Effort | Depends On | Files |
|-------|------|--------|------------|-------|
| BLK-01 | Core State Machine Rewrite | 2–3 days | None | ReaperOAK.agent.md |
| BLK-02 | Agent Definition Propagation | 1–2 days | BLK-01 | agents.md, TODO.agent.md, _cross-cutting-protocols.md, Validator.agent.md |
| BLK-03 | Chunk Content Updates | 1–2 days | BLK-01 | TODO chunks (01, 02), Validator chunk-01 |
| BLK-04 | Schema & Infrastructure Alignment | 1–2 days | BLK-01 | delegation-packet-schema.json, loop-detection-rules.md, tool-acl.yaml, definition-of-done-template.md |

**Total estimated effort:** 5–9 days (BLK-01 sequential, BLK-02–04 parallelizable)
