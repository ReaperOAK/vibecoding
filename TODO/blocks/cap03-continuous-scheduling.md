# Continuous Scheduling Engine — Execution Blocks

**Parent:** CAP-03 from vision.md
**Capability:** Continuous Scheduling Engine
**Created:** 2026-02-27T00:00:00Z
**Task Prefix:** WPAE
**Dependencies (L1):** CAP-01 (Updated Ticket State Machine), CAP-02 (Worker Pool Architecture)

---

## Design Context

CAP-03 replaces the cycle-batched orchestration model with a continuous, event-driven scheduling loop. The current system operates in discrete cycles — ReaperOAK selects a batch of READY tickets, delegates them, waits for the full batch to complete, then runs another cycle. The v8 model eliminates this: ReaperOAK continuously polls for READY tickets and assigns them the moment workers become available. This requires three interlocking systems: a scheduling algorithm that runs without batch boundaries, a global event queue that drives reactive dispatch, and updated safeguards that detect stalls in a continuous (non-cycled) environment.

**Spec Parts covered:** 2 (remove global cycle), 4 (parallel assignment algorithm), 11 (global event queue, event-driven orchestration)

---

## BLK-01: Continuous Scheduling Loop & Parallel Assignment Algorithm

**Description:** Design and define the continuous scheduling loop that replaces the cycle-batched model in `ReaperOAK.agent.md`. Define the parallel assignment algorithm that runs on every scheduling tick: scan the ticket registry for READY tickets, check dependency satisfaction, detect file-path and resource conflicts against currently-IMPLEMENTING tickets, query the worker pool registry for available workers, and assign the highest-priority non-conflicting ticket to the best-fit available worker. The loop runs continuously — no batch boundaries, no waiting for all in-flight tickets to complete before scheduling more. This block produces the canonical scheduling algorithm definition that all other blocks reference.

**Effort:** 2–3 days
**Depends On:** None (within CAP-03)
**UI Touching:** No

**Scope includes:**
- Continuous scheduling loop definition (replace cycle-batched SELECT/DELEGATE/WAIT)
- Parallel assignment algorithm: priority ordering → dependency check → conflict detection → worker matching → dispatch
- Scheduling tick semantics (event-triggered, not timer-based — fires on: ticket becomes READY, worker becomes available, REWORK re-entry)
- Conflict detection integration (reuse conflict rules from CAP-01 BLK-01 at scheduling time)
- Worker pool query interface (consume registry defined by CAP-02)
- Single-ticket-per-worker constraint enforcement at assignment time
- Ticket lock acquisition as part of assignment (READY → LOCKED → IMPLEMENTING as atomic transition)

**Primary file:** `.github/agents/ReaperOAK.agent.md`

---

## BLK-02: Global Event Queue & Reactive Dispatch

**Description:** Define the global event queue architecture and the reactive dispatch mechanism that drives the continuous scheduling loop. Specify event types (ticket state transitions, worker availability changes, REWORK re-entry, stall signals), event payload schemas, queue ordering semantics (priority-aware FIFO), and the consumption model (ReaperOAK as sole consumer). Define how agent-emitted events (`TASK_COMPLETED`, `TASK_FAILED`, `NEEDS_INPUT_FROM`, `BLOCKED_BY`) feed into the event queue and trigger scheduling ticks. Update the cross-cutting event protocol to include new event types for worker pool state changes.

**Effort:** 2–3 days
**Depends On:** BLK-01
**UI Touching:** No

**Scope includes:**
- Global event queue schema: event types, payload structure, ordering semantics
- Event types: `TICKET_READY`, `WORKER_AVAILABLE`, `TASK_COMPLETED`, `TASK_FAILED`, `REWORK_ENTRY`, `STALL_DETECTED`, `CONFLICT_RESOLVED`
- Reactive dispatch: each event consumption triggers a scheduling tick (BLK-01 algorithm)
- Event emission protocol for agents: how implementing agents emit events that reach the queue
- Worker pool event types: `WORKER_FREED`, `WORKER_ASSIGNED`, `WORKER_STALLED`
- Ticket registry event types: `TICKET_PROMOTED` (BACKLOG→READY), `TICKET_DONE`
- Queue consumption model: ReaperOAK is the sole consumer; single-threaded processing per tick

**Primary files:** `.github/agents/ReaperOAK.agent.md`, `.github/agents/_cross-cutting-protocols.md`

---

## BLK-03: Cycle Concept Removal

**Description:** Remove all references to the global cycle concept from agent definitions and the boot protocol. Replace cycle-based language ("per cycle", "cycle budget", "cycle SELECT", "next cycle", "zero-progress cycle") with continuous scheduling terminology. This is a systematic find-and-replace across prose, tables, ASCII diagrams, and governance rules. The cycle concept is deeply embedded in `agents.md` (boot protocol), `ReaperOAK.agent.md` (orchestration rules), and `_cross-cutting-protocols.md` (governance), so this block must be thorough. Where cycle-based governance existed (e.g., "max 1 task per agent per cycle"), replace with the v8 equivalent (e.g., "max 1 task per agent concurrently via worker pool constraint").

**Effort:** 1–2 days
**Depends On:** BLK-01
**UI Touching:** No

**Scope includes:**
- `agents.md` — remove cycle references in boot protocol, ticket lifecycle, governance rules
- `.github/agents/ReaperOAK.agent.md` — remove cycle-batched loop, replace with continuous loop reference
- `.github/agents/_cross-cutting-protocols.md` — cycle-based stall detection, per-cycle budget rules
- Semantic replacement mapping: "cycle" → "scheduling tick" or "continuous", "per cycle" → "concurrently" or "per scheduling window"
- Update all governance thresholds that referenced cycle counts (e.g., "blocked for > 3 cycles" → time-based or tick-based equivalent)

**Not in scope:** Chunk YAML files (→ BLK-04), ARCHITECTURE.md (→ BLK-05)

---

## BLK-04: Scheduling Safeguards & Stall Detection

**Description:** Define stall detection signals, fairness rules, starvation prevention, and loop detection rules specific to the continuous scheduling model. The current stall detection references cycle counts ("in IMPLEMENTING for > 2 cycles"); these must be replaced with time-based or tick-based thresholds appropriate for continuous operation. Add new safeguard categories: scheduling starvation (low-priority tickets perpetually deferred), hot-loop detection (scheduler firing ticks without making assignments), and worker saturation (all workers busy, READY tickets accumulating). Update guardian loop-detection rules.

**Effort:** 1–2 days
**Depends On:** BLK-01, BLK-02
**UI Touching:** No

**Scope includes:**
- Time-based stall detection thresholds (replace cycle-count-based thresholds)
- Scheduling fairness: priority aging (tickets waiting too long auto-escalate)
- Starvation prevention: P3 tickets guaranteed minimum scheduling attention
- Hot-loop guard: if scheduler fires N ticks without any assignment, pause and log diagnostics
- Worker saturation monitoring: backpressure signal when all workers busy
- Thrashing detection: ticket toggling IMPLEMENTING↔REWORK within time window
- Zero-progress detection: no ticket reaches DONE within configurable time window

**Primary files:** `.github/guardian/loop-detection-rules.md`, `.github/agents/ReaperOAK.agent.md`

---

## BLK-05: Architecture Documentation Alignment

**Description:** Update `ARCHITECTURE.md` with a comprehensive continuous scheduling section that documents the new scheduling model, event queue topology, and how the scheduling loop interacts with the worker pool and ticket registry. This block captures the architectural rationale (why continuous over batched), documents the scheduling algorithm at a system-design level, and ensures the topology diagram reflects the event-driven flow. This is the final integration block that references the canonical definitions from BLK-01 through BLK-04.

**Effort:** 1 day
**Depends On:** BLK-01, BLK-02, BLK-03, BLK-04
**UI Touching:** No

**Scope includes:**
- `.github/ARCHITECTURE.md` — new "Continuous Scheduling Engine" section
- Scheduling architecture diagram (event queue → scheduler → worker pool → ticket registry)
- Rationale documentation: why continuous scheduling replaces cycle-batched
- Interaction with Two-Layer Model (CAP-04): scheduling engine as the Execution Layer backbone
- System topology update reflecting event-driven flow

**Not in scope:** Agent definition files (→ BLK-01, BLK-02, BLK-03), guardian rules (→ BLK-04)

---

## Block Dependency Graph

```
BLK-01 (Scheduling Loop & Assignment Algorithm)
  │
  ├──► BLK-02 (Event Queue & Reactive Dispatch)
  │       │
  │       ├──► BLK-04 (Scheduling Safeguards & Stall Detection)
  │       │       │
  ├──► BLK-03 (Cycle Concept Removal)
  │       │       │
  │       ▼       ▼
  └────────► BLK-05 (Architecture Documentation Alignment)
```

**Critical path:** BLK-01 → BLK-02 → BLK-04 → BLK-05

**Parallel track:** BLK-03 can proceed in parallel with BLK-02 (both depend only on BLK-01)

---

## Summary

| Block | Name | Effort | Depends On | Primary Files |
|-------|------|--------|------------|---------------|
| BLK-01 | Scheduling Loop & Assignment Algorithm | 2–3 days | None | ReaperOAK.agent.md |
| BLK-02 | Event Queue & Reactive Dispatch | 2–3 days | BLK-01 | ReaperOAK.agent.md, _cross-cutting-protocols.md |
| BLK-03 | Cycle Concept Removal | 1–2 days | BLK-01 | agents.md, ReaperOAK.agent.md, _cross-cutting-protocols.md |
| BLK-04 | Scheduling Safeguards & Stall Detection | 1–2 days | BLK-01, BLK-02 | loop-detection-rules.md, ReaperOAK.agent.md |
| BLK-05 | Architecture Documentation Alignment | 1 day | BLK-01–BLK-04 | ARCHITECTURE.md |

**Total estimated effort:** 7–11 days (BLK-01 sequential; BLK-02+BLK-03 parallelizable; BLK-04 after BLK-02; BLK-05 last)
