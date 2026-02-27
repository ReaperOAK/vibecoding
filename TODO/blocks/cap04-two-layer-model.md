# Two-Layer Orchestration Model — Execution Blocks

**Parent:** CAP-04 from vision.md
**Capability:** Two-Layer Orchestration Model
**Created:** 2026-02-27T00:00:00Z
**Task Prefix:** WPAE

---

## Layer Reference

CAP-04 introduces two concurrent, interacting orchestration layers:

**Layer A — Strategic Layer (Adaptive Council):**
- Members: Research, ProductManager, Architect, Security (strategic mode), UIDesigner (conceptual mode), DevOps (infra planning mode)
- Produces Strategic Decision Records (SDRs) and versioned strategic artifacts
- May run at ANY time — no phase barriers, no ticket dependency
- Never implements tickets; only produces artifacts that influence the Execution Layer

**Layer B — Execution Layer (Parallel Ticket Engine):**
- Members: Backend, Frontend, DevOps (exec mode), QA, Security (exec mode), Documentation, Validator, CIReviewer
- Executes exactly ONE ticket per worker instance
- Follows strict SDLC lifecycle (READY → ... → DONE)
- Consumes SDRs from Layer A to adjust priority/scope of in-flight work

**Dual-mode agents:** Security, DevOps, and UIDesigner operate in both layers with distinct mode constraints. Mode determines capabilities, write paths, and event types.

---

## BLK-01: Core Two-Layer Model Definition

**Description:** Define the canonical two-layer orchestration model in `ReaperOAK.agent.md` — the single source of truth for Layer A (Strategic) and Layer B (Execution). This block establishes: layer membership rules (which agents belong to each layer), layer responsibilities and constraints, the interaction protocol between layers (how SDRs flow from Strategic to Execution, how Execution results feed back to Strategic), concurrent operation semantics (no phase barriers — both layers run simultaneously), and the dual-mode protocol for agents that operate in both layers (Security, DevOps, UIDesigner). This is the foundational block that all other blocks reference.

**Effort:** 2–3 days
**Depends On:** None
**UI Touching:** No

**Scope includes:**
- Layer A definition: membership, responsibilities, artifact types (SDRs, versioned roadmaps)
- Layer B definition: membership, responsibilities, ticket-only execution constraint
- Interaction protocol: SDR submission → ingestion, priority adjustment, scope change propagation
- Concurrent operation rules: no phase barriers, both layers active simultaneously
- Dual-mode agent protocol: mode-specific capabilities, switching rules, isolation constraints
- ReaperOAK's role as the bridge between layers (routes SDRs, adjusts ticket priorities)

**Primary file:** `.github/agents/ReaperOAK.agent.md`

---

## BLK-02: Agent Layer Assignment & Boot Protocol Update

**Description:** Propagate layer assignments across all agent definition files and the boot protocol (`agents.md`). Each agent file must declare its layer membership (A, B, or both with mode qualifiers). Dual-mode agents (Security, DevOps, UIDesigner) need explicit mode definitions — what each mode allows, what it forbids, and how mode selection is determined (via delegation packet from ReaperOAK). The boot protocol must be updated so that agents know their layer context on session start, including which artifacts they read/write per layer and how they interact with the opposite layer.

**Effort:** 1–2 days
**Depends On:** BLK-01
**UI Touching:** No

**Scope includes:**
- `agents.md` — layer assignment table, boot sequence additions for layer context
- `.github/agents/TODO.agent.md` — position in the model (translate-only, not strategic initiator)
- Individual agent `.md` files — layer membership declaration in frontmatter/metadata
- Dual-mode agent definitions: Security (strategic-mode vs exec-mode), DevOps (infra-planning vs exec), UIDesigner (conceptual vs implementation)
- Mode selection mechanism: how ReaperOAK communicates mode via delegation packet

**Not in scope:** Event protocol updates (→ BLK-03), architecture documentation (→ BLK-04)

---

## BLK-03: Layer-Aware Event Protocol

**Description:** Update `_cross-cutting-protocols.md` to add layer-specific event types, emission rules, and interaction handoff semantics. Layer A agents emit strategic events (SDR creation, artifact versioning, priority recommendation) while Layer B agents emit execution events (the existing TASK_STARTED, TASK_COMPLETED, etc.). New event types are needed for cross-layer communication: SDR submission, SDR ingestion, priority adjustment propagation, and strategic artifact publication. Event routing rules must distinguish intra-layer events from cross-layer events.

**Effort:** 1–2 days
**Depends On:** BLK-01
**UI Touching:** No

**Scope includes:**
- Layer A event types: `SDR_CREATED`, `SDR_SUBMITTED`, `ARTIFACT_PUBLISHED`, `PRIORITY_RECOMMENDATION`
- Layer B event types: existing execution events (no changes needed, already defined)
- Cross-layer events: `SDR_INGESTED`, `PRIORITY_ADJUSTED`, `SCOPE_CHANGED`, `STRATEGIC_FEEDBACK`
- Event routing rules: which events flow within a layer vs across layers
- ReaperOAK as event router: how it mediates cross-layer event delivery
- Updated event emission protocol section in `_cross-cutting-protocols.md`

**Not in scope:** Agent file updates (→ BLK-02), architecture documentation (→ BLK-04)

---

## BLK-04: Architecture Documentation Update

**Description:** Update `ARCHITECTURE.md` to reflect the full two-layer orchestration topology. This includes a new architecture diagram showing Layer A and Layer B as concurrent subsystems under ReaperOAK, an updated authority matrix that maps agents to layers with mode qualifiers, an interaction flow diagram showing SDR lifecycle, and documentation of the concurrency model (no phase barriers, discovery and execution running simultaneously). This block captures the conceptual architecture for human readers and downstream agent reference.

**Effort:** 1–2 days
**Depends On:** BLK-01
**UI Touching:** No

**Scope includes:**
- Two-layer topology diagram (Layer A ↔ ReaperOAK ↔ Layer B)
- Authority matrix update: agent → layer mapping with mode qualifiers
- SDR lifecycle flow diagram: creation → submission → ingestion → effect on tickets
- Concurrency model documentation: no phase barriers, continuous operation
- Interaction patterns: how strategic decisions influence execution without blocking it
- v7→v8 migration notes for the orchestration model section

**Primary file:** `.github/ARCHITECTURE.md`

---

## Block Dependency Graph

```
BLK-01 (Core Two-Layer Model Definition)
  │
  ├──► BLK-02 (Agent Layer Assignment & Boot Protocol Update)
  │
  ├──► BLK-03 (Layer-Aware Event Protocol)
  │
  └──► BLK-04 (Architecture Documentation Update)
```

**Critical path:** BLK-01 → any of {BLK-02, BLK-03, BLK-04} (parallel after BLK-01)

---

## Summary

| Block | Name | Effort | Depends On | Primary Files |
|-------|------|--------|------------|---------------|
| BLK-01 | Core Two-Layer Model Definition | 2–3 days | None | ReaperOAK.agent.md |
| BLK-02 | Agent Layer Assignment & Boot Protocol Update | 1–2 days | BLK-01 | agents.md, agent .md files, TODO.agent.md |
| BLK-03 | Layer-Aware Event Protocol | 1–2 days | BLK-01 | _cross-cutting-protocols.md |
| BLK-04 | Architecture Documentation Update | 1–2 days | BLK-01 | ARCHITECTURE.md |

**Total estimated effort:** 5–9 days (BLK-01 sequential, BLK-02–04 parallelizable)
