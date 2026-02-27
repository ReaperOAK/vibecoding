# Worker-Pool Adaptive Engine (WPAE) — Vision & Capabilities

**L0 Vision:** Upgrade the multi-agent vibecoding system from a cycle-batched, singleton-agent orchestration model (v7) to an adaptive, event-driven, worker-pool-based software agency engine (v8) with continuous scheduling, two-layer orchestration, and controlled mid-execution strategy evolution via Strategy Deviation Requests.

**Task Prefix:** WPAE
**Created:** 2026-02-27T00:00:00Z
**Source:** 13-part upgrade specification provided by user

---

## Capabilities (L1)

### CAP-01: Updated Ticket State Machine & Commit Enforcement
**Description:** Migrate the 9-state ticket machine to the new state vocabulary (READY→LOCKED→IMPLEMENTING→QA_REVIEW→VALIDATION→DOCUMENTATION→CI_REVIEW→COMMIT→DONE), enforce strict per-ticket atomic commits, and implement conflict detection rules across file paths, directories, DB schemas, infrastructure resources, and config files.
**Effort:** 1–2 weeks
**Status:** not_started
**Rationale:** Foundational — every other capability references the ticket state machine. The new state names, commit enforcement, and conflict detection must be defined first so all downstream files and protocols can align to them.
**Spec Parts:** 8 (updated ticket states), 9 (per-ticket commit enforcement), 13 (conflict detection rules)
**Primary Files:**
- `.github/agents/ReaperOAK.agent.md` — canonical state definitions
- `.github/agents/_cross-cutting-protocols.md` — state references in event protocol
- `.github/tasks/delegation-packet-schema.json` — state enum update
- `.github/agents/Validator.agent.md` — state references
- `agents.md` — boot protocol state references

### CAP-02: Worker Pool Architecture
**Description:** Replace the singleton-agent model with a worker-pool-based concurrency model where each agent role (Backend, Frontend, QA, etc.) is a pool of available workers, tracked via a global worker pool registry with capacity, availability, and assignment state per worker.
**Effort:** 1–2 weeks
**Status:** not_started
**Rationale:** The worker pool model is the core architectural shift enabling parallelism. Continuous scheduling and the two-layer model both depend on workers being pooled rather than locked as singletons.
**Spec Parts:** 1 (worker pool model), 11 (worker pool registry)
**Primary Files:**
- `.github/agents/ReaperOAK.agent.md` — pool definitions, registry schema
- `.github/ARCHITECTURE.md` — topology and authority matrix update
- `.github/sandbox/tool-acl.yaml` — worker pool notes

### CAP-03: Continuous Scheduling Engine
**Description:** Remove the global cycle concept and implement a continuous, event-driven scheduling loop with a parallel assignment algorithm, global event queue, and reactive dispatch — replacing batched cycle-based assignment with always-on scheduling that assigns tickets as soon as workers become available.
**Effort:** 1–2 weeks
**Status:** not_started
**Rationale:** Continuous scheduling is the execution backbone of v8. It replaces the cycle-batched model and drives the Execution Layer. Depends on worker pools being defined (CAP-02) so the scheduler knows what workers are available.
**Spec Parts:** 2 (remove global cycle), 4 (parallel assignment algorithm), 11 (global event queue, event-driven orchestration)
**Primary Files:**
- `.github/agents/ReaperOAK.agent.md` — scheduling loop, event queue, dispatch algorithm
- `.github/agents/_cross-cutting-protocols.md` — worker pool event types
- `.github/guardian/loop-detection-rules.md` — new stall/loop detection signals

### CAP-04: Two-Layer Orchestration Model
**Description:** Restructure orchestration into two interacting layers — a Strategic Layer (roadmap management, capability selection, priority adjustment) and an Execution Layer (ticket scheduling, worker dispatch, post-execution chain) — enabling discovery and execution to run concurrently with no phase barriers.
**Effort:** 1–2 weeks
**Status:** not_started
**Rationale:** The two-layer separation is the architectural backbone of the v8 orchestration philosophy. It decouples strategic planning from tactical execution, allowing both to operate simultaneously. Depends on worker pools (CAP-02) and scheduling (CAP-03) for the Execution Layer.
**Spec Parts:** 3 (two interacting layers), 6 (discovery and execution run concurrently)
**Primary Files:**
- `.github/agents/ReaperOAK.agent.md` — layer definitions, interaction protocol
- `.github/ARCHITECTURE.md` — full topology update for two-layer model
- `agents.md` — boot protocol update for two-layer model

### CAP-05: Controlled Strategy Evolution (SDRs)
**Description:** Implement Strategy Deviation Requests (SDRs) as the mechanism for controlled mid-execution strategy changes, restrict the TODO agent from initiating strategy (translate-only role), and introduce continuous adaptive planning with versioned roadmaps that allow priority and scope adjustments without halting execution.
**Effort:** 1–2 weeks
**Status:** not_started
**Rationale:** SDRs are the novel contribution of v8 — enabling the system to adapt its strategic direction without stopping in-flight work. Depends on the two-layer model (CAP-04) being defined since SDRs flow from the Strategic Layer to the Execution Layer.
**Spec Parts:** 5 (SDRs), 7 (TODO agent restrictions), 12 (continuous adaptive planning, versioned roadmaps)
**Primary Files:**
- `.github/agents/ReaperOAK.agent.md` — SDR protocol, versioned roadmap
- `.github/agents/TODO.agent.md` — restrictions, SDR translation role
- `.github/vibecoding/chunks/TODO.agent/chunk-01.yaml` — SDR input protocol
- `.github/vibecoding/chunks/TODO.agent/chunk-02.yaml` — updated states and governance

### CAP-06: UI/UX Enforcement Hardening
**Description:** Upgrade UI/UX gate enforcement from soft flagging to hard pipeline-blocking enforcement with Stitch design-system integration, ensuring no UI-touching ticket can proceed past QA_REVIEW without approved design artifacts from UIDesigner.
**Effort:** 1 week
**Status:** not_started
**Rationale:** Hard UI/UX enforcement closes a gap in the current system where UI-touching tasks could bypass design review. Stitch integration standardizes the design artifact contract. Relatively independent but references the new ticket states (CAP-01).
**Spec Parts:** 10 (UI/UX hard enforcement, Stitch integration)
**Primary Files:**
- `.github/agents/ReaperOAK.agent.md` — UI/UX gate hardening
- `.github/agents/TODO.agent.md` — UI flagging updates
- `.github/vibecoding/chunks/TODO.agent/chunk-02.yaml` — UI/UX flagging protocol updates

### CAP-07: Supporting Infrastructure Alignment
**Description:** Update all supporting infrastructure files — architecture documentation (v7→v8), agent chunk files, delegation packet schema, guardian loop-detection rules, sandbox ACLs, Validator state references, and cross-cutting protocol definitions — to align with the new v8 architecture defined by CAP-01 through CAP-06.
**Effort:** 1–2 weeks
**Status:** not_started
**Rationale:** This is the integration sweep that ensures every file in the system consistently reflects v8 semantics. It is deliberately last because it depends on all other capabilities being designed — it codifies the final state across all supporting files.
**Spec Parts:** Cross-cutting across all 13 parts
**Primary Files:**
- `.github/ARCHITECTURE.md` — full v7→v8 migration (1194 lines)
- `.github/vibecoding/chunks/Validator.agent/chunk-01.yaml` — new state references
- `.github/guardian/loop-detection-rules.md` — new detection signals
- `.github/sandbox/tool-acl.yaml` — worker pool annotations
- `.github/tasks/delegation-packet-schema.json` — state enum, SDR fields
- `.github/agents/_cross-cutting-protocols.md` — worker pool events, new protocol sections

---

## Dependency Graph (L1 Level)

```
CAP-01 (State Machine)  ──────────────────────────────────────────┐
    │                                                              │
    ▼                                                              │
CAP-02 (Worker Pool) ──► CAP-03 (Scheduling) ──► CAP-04 (Two-Layer) │
                                                       │           │
                                                       ▼           │
                                               CAP-05 (SDRs)      │
                                                                   │
CAP-06 (UI/UX) ◄── depends on CAP-01                              │
                                                                   │
CAP-07 (Infra Alignment) ◄── depends on CAP-01 through CAP-06 ────┘
```

**Critical Path:** CAP-01 → CAP-02 → CAP-03 → CAP-04 → CAP-05 → CAP-07

**Parallel Track:** CAP-06 can proceed in parallel with CAP-02–CAP-05 (only depends on CAP-01)

---

## Summary

| ID | Capability | Effort | Dependencies |
|----|-----------|--------|-------------|
| CAP-01 | Updated Ticket State Machine & Commit Enforcement | 1–2 weeks | None (foundational) |
| CAP-02 | Worker Pool Architecture | 1–2 weeks | CAP-01 |
| CAP-03 | Continuous Scheduling Engine | 1–2 weeks | CAP-01, CAP-02 |
| CAP-04 | Two-Layer Orchestration Model | 1–2 weeks | CAP-02, CAP-03 |
| CAP-05 | Controlled Strategy Evolution (SDRs) | 1–2 weeks | CAP-04 |
| CAP-06 | UI/UX Enforcement Hardening | 1 week | CAP-01 |
| CAP-07 | Supporting Infrastructure Alignment | 1–2 weeks | CAP-01–CAP-06 |
