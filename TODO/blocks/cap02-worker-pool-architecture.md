# Worker Pool Architecture — Execution Blocks

**Parent:** CAP-02 from vision.md
**Capability:** Worker Pool Architecture
**Created:** 2026-02-27T00:00:00Z
**Task Prefix:** WPAE

---

## Context

CAP-02 replaces the singleton-agent orchestration model with a scalable worker-pool-based concurrency model. In the current (v7) system, each agent role is a singleton — one Backend agent, one Frontend agent, etc. — and only one ticket can be assigned per role at a time. The worker pool model (v8) treats each role as a pool of N ephemeral worker instances. Each worker handles exactly one ticket, then returns to the pool. Multiple workers of the same role can operate in parallel, limited only by the dependency graph, file/resource conflicts, and available worker capacity.

**Key architectural concepts:**
- Each agent role is a pool of configurable size (e.g., Backend × 3)
- One ticket per worker instance (worker-level locking, not role-level)
- Workers are ephemeral — assigned on ticket selection, released on completion/failure
- Pool size is configurable per role
- Parallelism bounded by: dependency DAG, file/resource conflict detection, worker capacity

**Depends On:** CAP-01 (Updated Ticket State Machine & Commit Enforcement) — the state machine, conflict detection rules, and lock semantics defined in CAP-01 are prerequisites for worker pool assignment logic.

---

## BLK-01: Core Worker Pool Data Model & Registry Schema

**Description:** Define the canonical worker pool registry as the single source of truth in `ReaperOAK.agent.md`. This includes: the global pool registry structure (per-role pool definitions with role name, max pool size, min pool size, current active count), the worker instance schema (worker ID format, role, lifecycle state, currently assigned ticket, assignment/release timestamps), and pool configuration defaults for each of the 13 agent roles. The registry schema is the foundational data model that all other blocks reference — it establishes *what* a pool is, *what* a worker is, and *how* they are tracked.

**Effort:** 2–3 days
**Depends On:** None (within CAP-02; CAP-01 is a capability-level dependency)
**UI Touching:** No

**Scope includes:**
- Global worker pool registry structure (role → pool metadata mapping)
- Per-role pool definition fields: `role`, `max_workers`, `min_workers`, `active_count`
- Worker instance schema: `worker_id`, `role`, `state` (IDLE | ASSIGNED | COOLDOWN), `current_ticket`, `assigned_at`, `released_at`
- Worker ID format convention (e.g., `{ROLE}-W{NNN}`, parseable by tooling)
- Default pool size configuration for each of the 13 agent roles
- Pool sizing rationale (which roles need more parallelism, which are naturally serial)
- Registry as an in-memory model (ReaperOAK tracks, not persisted to disk)

**Primary file:** `.github/agents/ReaperOAK.agent.md`

---

## BLK-02: Worker Assignment & Lifecycle Protocol

**Description:** Define the worker assignment algorithm and lifecycle protocol in `ReaperOAK.agent.md`. This replaces the singleton model's "one agent = one ticket" assignment with "select an IDLE worker from the role's pool, bind it to the ticket, release it on completion." The block covers: the parallel assignment algorithm (how ReaperOAK selects READY tickets and matches them to available workers across all pools), worker-level lock semantics (replacing role-level locks), one-ticket-per-worker binding rules, worker release on DONE/REWORK/timeout, pool exhaustion handling (all workers busy → ticket remains READY), and the explicit migration path from singleton to pool model.

**Effort:** 2–3 days
**Depends On:** BLK-01
**UI Touching:** No

**Scope includes:**
- Parallel assignment algorithm: scan READY tickets → check available workers → check file/resource conflicts → assign
- Worker-level locking: lock is on worker instance, not on role — multiple workers of same role can hold locks simultaneously
- One-ticket-per-worker invariant: a worker in ASSIGNED state handles exactly one ticket
- Worker release protocol: worker returns to IDLE on ticket DONE, REWORK, or lock timeout
- COOLDOWN state: optional brief pause between assignments (prevents thrashing)
- Pool exhaustion semantics: if all workers for a role are ASSIGNED, tickets requiring that role stay READY
- Parallelism constraints: dependency DAG edges, file-path conflict rules (from CAP-01), worker capacity
- Migration notes: how existing singleton references map to pool-of-1 (backward compatible default)

**Primary file:** `.github/agents/ReaperOAK.agent.md`

---

## BLK-03: Cross-Cutting Protocol & Boot Protocol Updates

**Description:** Propagate the worker pool model into cross-cutting protocol definitions and the agent boot protocol. Update `_cross-cutting-protocols.md` with worker identity semantics — every event emission, trace record, and delegation packet must carry a worker ID (not just a role name). Define new pool lifecycle event types (WORKER_ASSIGNED, WORKER_RELEASED, POOL_EXHAUSTED, POOL_SCALED) for the global event queue. Update `agents.md` to describe the worker pool model in the boot protocol so all agents understand they are instantiated as workers within a pool, not as singleton agents.

**Effort:** 1–2 days
**Depends On:** BLK-01, BLK-02
**UI Touching:** No

**Scope includes:**
- `.github/agents/_cross-cutting-protocols.md` — worker identity in structured event emissions (add `worker_id` field)
- `.github/agents/_cross-cutting-protocols.md` — new event types: `WORKER_ASSIGNED`, `WORKER_RELEASED`, `POOL_EXHAUSTED`, `POOL_SCALED`
- `.github/agents/_cross-cutting-protocols.md` — worker-level trace event schema (extend observability)
- `agents.md` — boot protocol section describing worker pool model (agents are pools, instances are workers)
- `agents.md` — update delegation description to reference worker-level assignment
- Worker ID inclusion in delegation packet envelope (worker identity travels with the task)

**Primary files:** `.github/agents/_cross-cutting-protocols.md`, `agents.md`

---

## BLK-04: Architecture Documentation & Infrastructure Alignment

**Description:** Update the system architecture documentation and supporting infrastructure files to reflect the worker pool model. `ARCHITECTURE.md` requires a new section describing the pool topology, the shift from singleton to pooled workers, the authority matrix update (ReaperOAK manages pools, workers inherit role permissions), and pool sizing guidance. `tool-acl.yaml` requires annotations clarifying that ACLs apply at the role level and are inherited by all worker instances of that role — no per-worker ACL differentiation.

**Effort:** 1–2 days
**Depends On:** BLK-01, BLK-02
**UI Touching:** No

**Scope includes:**
- `.github/ARCHITECTURE.md` — new "Worker Pool Architecture" section: pool topology diagram, singleton→pool migration narrative
- `.github/ARCHITECTURE.md` — authority matrix update: ReaperOAK as pool manager, workers as ephemeral executors
- `.github/ARCHITECTURE.md` — pool sizing guidance table (recommended defaults per role, rationale)
- `.github/ARCHITECTURE.md` — concurrency model description: how parallelism is bounded by DAG + conflicts + capacity
- `.github/sandbox/tool-acl.yaml` — worker pool annotations: ACLs are role-level, inherited by worker instances
- `.github/sandbox/tool-acl.yaml` — clarification that worker instances do NOT get distinct ACL entries

**Primary files:** `.github/ARCHITECTURE.md`, `.github/sandbox/tool-acl.yaml`

---

## Block Dependency Graph

```
BLK-01 (Core Worker Pool Data Model & Registry Schema)
  │
  ├──► BLK-02 (Worker Assignment & Lifecycle Protocol)
  │       │
  │       ├──► BLK-03 (Cross-Cutting Protocol & Boot Protocol Updates)
  │       │
  │       └──► BLK-04 (Architecture Documentation & Infrastructure Alignment)
  │
  └────────────────────────────────────────────────────────────────────────
```

**Critical path:** BLK-01 → BLK-02 → {BLK-03, BLK-04} (parallel after BLK-02)

---

## Summary

| Block | Name | Effort | Depends On | Files |
|-------|------|--------|------------|-------|
| BLK-01 | Core Worker Pool Data Model & Registry Schema | 2–3 days | None | ReaperOAK.agent.md |
| BLK-02 | Worker Assignment & Lifecycle Protocol | 2–3 days | BLK-01 | ReaperOAK.agent.md |
| BLK-03 | Cross-Cutting Protocol & Boot Protocol Updates | 1–2 days | BLK-01, BLK-02 | _cross-cutting-protocols.md, agents.md |
| BLK-04 | Architecture Documentation & Infrastructure Alignment | 1–2 days | BLK-01, BLK-02 | ARCHITECTURE.md, tool-acl.yaml |

**Total estimated effort:** 6–10 days (BLK-01 → BLK-02 sequential, BLK-03 + BLK-04 parallelizable after BLK-02)
