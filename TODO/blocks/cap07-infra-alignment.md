# Supporting Infrastructure Alignment — Execution Blocks

**Parent:** CAP-07 from vision.md
**Capability:** Supporting Infrastructure Alignment
**Created:** 2026-02-27T00:00:00Z
**Task Prefix:** WPAE

---

## Context

CAP-07 is the final integration sweep. After CAP-01 through CAP-06 define the
new v8 architecture (updated ticket states, worker pools, continuous scheduling,
two-layer orchestration, SDRs, and hard UI/UX enforcement), this capability
ensures every supporting file in the system consistently reflects the complete
v8 design. The primary deliverable is ARCHITECTURE.md v8.0.0 — a comprehensive
rewrite capturing the full architectural evolution. Secondary deliverables are
consistency verification, metadata updates, and memory bank recording.

**Depends On (L1):** CAP-01, CAP-02, CAP-03, CAP-04, CAP-05, CAP-06 (all
must have their L2→L3 designs complete before CAP-07 blocks execute).

---

## BLK-01: ARCHITECTURE.md v7→v8 Rewrite

**Description:** Perform a full rewrite of `.github/ARCHITECTURE.md` from v7 to v8.0.0, incorporating all architectural concepts introduced by CAP-01 through CAP-06. The rewrite must capture: the updated 9-state ticket machine with new state vocabulary (READY→COMMIT→DONE), worker-pool-based concurrency model with global registry, continuous event-driven scheduling replacing cycle-batched dispatch, two-layer orchestration (Strategic Layer + Execution Layer), Strategy Deviation Requests (SDRs) as controlled mid-execution strategy evolution, hard UI/UX pipeline-blocking enforcement with Stitch design-system integration, per-ticket atomic commit enforcement, and conflict detection rules. The topology diagram, authority matrix, and system interaction flows must all reflect v8 semantics.

**Effort:** 2–3 days
**Depends On:** None (within CAP-07; all L1 dependencies are external)
**UI Touching:** No

**Scope includes:**
- System topology diagram update (worker pools, two-layer model)
- Authority matrix revision (Strategic Layer vs. Execution Layer ownership)
- Component interaction flows (event queue, continuous scheduling, SDR pipeline)
- Capability summary table reflecting v8 feature set
- Version bump to v8.0.0 with migration notes from v7
- Cross-references to canonical definitions in ReaperOAK.agent.md

**Primary file:** `.github/ARCHITECTURE.md`

---

## BLK-02: Supporting File Consistency Sweep

**Description:** Audit and update all supporting infrastructure files to ensure consistent v8 terminology and semantics after CAP-01–CAP-06 changes have landed. This is a difference-check pass: verify that every file referencing ticket states, orchestration model, scheduling approach, agent roles, or enforcement gates uses the v8 vocabulary and concepts. Files that were partially updated by earlier capabilities get a final consistency pass; files not directly touched by CAP-01–CAP-06 are updated here. Resolve any semantic drift, stale v7 references, or cross-file inconsistencies.

**Effort:** 2–3 days
**Depends On:** BLK-01
**UI Touching:** No

**Scope includes:**
- `.github/agents/_cross-cutting-protocols.md` — verify worker pool event types, two-layer references, SDR event schema are present and consistent
- `.github/guardian/loop-detection-rules.md` — verify stall detection signals reference v8 states and continuous scheduling semantics
- `.github/sandbox/tool-acl.yaml` — verify worker pool annotations and any new tool entries
- `.github/tasks/delegation-packet-schema.json` — verify state enum, SDR fields, worker assignment fields
- `.github/tasks/definition-of-done-template.md` — verify lifecycle checklist matches v8 states
- `.github/vibecoding/chunks/Validator.agent/chunk-01.yaml` — verify state references in validation matrix
- Any other files with stale v7 references discovered during audit

---

## BLK-03: Context Index & Catalog Update

**Description:** Update the vibecoding context infrastructure to reflect all files created or modified during the v7→v8 upgrade. Update `.github/vibecoding/index.json` with current SHA hashes for every file modified by CAP-01 through CAP-07. Update `.github/vibecoding/catalog.yml` with new semantic tags introduced by v8 concepts (e.g., `worker-pool:`, `continuous-scheduling:`, `two-layer:`, `sdr:`, `conflict-detection:`) and map them to the relevant chunk files. Ensure the chunk discovery system can surface v8-specific guidance when agents query by domain tag.

**Effort:** 1–2 days
**Depends On:** BLK-01, BLK-02
**UI Touching:** No

**Scope includes:**
- `.github/vibecoding/index.json` — recompute hashes for all modified files across CAP-01–CAP-07
- `.github/vibecoding/catalog.yml` — add new semantic tags for v8 concepts, map to chunk paths
- Verify chunk file `hash` fields in YAML frontmatter match recomputed values
- Validate that `catalog.yml` tag→chunk mappings resolve to existing files

---

## BLK-04: Memory Bank & Progress Recording

**Description:** Record the v7→v8 infrastructure upgrade as a completed milestone in the memory bank. Append a session entry to `activeContext.md` summarizing the CAP-07 alignment work. Append a milestone entry to `progress.md` marking the v8.0.0 upgrade as complete with references to all modified files. All updates are append-only per memory bank governance rules.

**Effort:** 0.5–1 day
**Depends On:** BLK-01, BLK-02, BLK-03
**UI Touching:** No

**Scope includes:**
- `.github/memory-bank/activeContext.md` — append session entry for CAP-07 alignment work
- `.github/memory-bank/progress.md` — append milestone entry for v8.0.0 upgrade completion
- Reference list of all files modified across CAP-01–CAP-07 for traceability

---

## Block Dependency Graph

```
BLK-01 (ARCHITECTURE.md v7→v8 Rewrite)
  │
  └──► BLK-02 (Supporting File Consistency Sweep)
         │
         └──► BLK-03 (Context Index & Catalog Update)
                │
                └──► BLK-04 (Memory Bank & Progress Recording)
```

**Critical path:** BLK-01 → BLK-02 → BLK-03 → BLK-04 (sequential — each
block depends on the prior block stabilizing the file set it audits or indexes)

---

## Summary

| Block | Name | Effort | Depends On | Primary Files |
|-------|------|--------|------------|---------------|
| BLK-01 | ARCHITECTURE.md v7→v8 Rewrite | 2–3 days | None (external: CAP-01–CAP-06) | ARCHITECTURE.md |
| BLK-02 | Supporting File Consistency Sweep | 2–3 days | BLK-01 | _cross-cutting-protocols.md, loop-detection-rules.md, tool-acl.yaml, delegation-packet-schema.json, definition-of-done-template.md, Validator chunk-01 |
| BLK-03 | Context Index & Catalog Update | 1–2 days | BLK-01, BLK-02 | index.json, catalog.yml |
| BLK-04 | Memory Bank & Progress Recording | 0.5–1 day | BLK-01, BLK-02, BLK-03 | activeContext.md, progress.md |

**Total estimated effort:** 5.5–9 days (sequential critical path)
