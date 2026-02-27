# Controlled Strategy Evolution (SDRs) — Execution Blocks

**Parent:** CAP-05 from vision.md
**Capability:** Controlled Strategy Evolution (SDRs)
**Created:** 2026-02-27T00:00:00Z
**Task Prefix:** WPAE

---

## SDR Concept Summary

Strategy Deviation Requests (SDRs) are versioned documents that enable controlled mid-execution strategy changes. Any agent may emit a strategic event (e.g., STRATEGIC_REVIEW_REQUIRED, ARCHITECTURE_RISK_DETECTED) when it detects that current execution direction needs reassessment. ReaperOAK triages the event, pauses ONLY the affected tickets (unaffected work continues), invokes Strategic Layer agents to produce a versioned SDR, and then delegates to TODO Agent to translate the SDR into roadmap changes (new tickets, deprecated tickets, adjusted dependencies). Roadmap versions increment (v1.0 → v1.1) and completed tickets are never invalidated.

The TODO Agent is restricted to a **translate-only** role: it may NOT invent capabilities or make architectural decisions. It translates SDR directives into capabilities → blocks → tickets. If required upstream artifacts are missing, it must emit REQUIRES_STRATEGIC_INPUT rather than guessing.

---

## BLK-01: SDR Schema & Strategic Event Definitions

**Description:** Define the foundational "language" for controlled strategy evolution. This block produces: (a) the SDR document schema — required fields, lifecycle states (PROPOSED → APPROVED → APPLIED → SUPERSEDED), version numbering rules, approval authority — and (b) the 5 strategic event types (STRATEGIC_REVIEW_REQUIRED, ARCHITECTURE_RISK_DETECTED, SCOPE_CONFLICT_DETECTED, MARKET_INSIGHT_UPDATE, SECURITY_RISK_UPDATE) with emission rules, payload schemas, severity levels, and which agents are authorized to emit each event type. The SDR schema is written into ReaperOAK.agent.md as the canonical source, and the strategic event types are added to _cross-cutting-protocols.md so all agents can reference them.

**Effort:** 2–3 days
**Depends On:** None
**UI Touching:** No

**Scope includes:**
- SDR document schema: fields (id, version, trigger_event, affected_tickets, proposed_changes, rationale, status, author, approved_by, created, applied)
- SDR lifecycle states: PROPOSED → APPROVED → APPLIED → SUPERSEDED
- SDR version numbering convention and approval authority rules
- 5 strategic event type definitions with payload schemas
- Event emission authorization matrix (which agents may emit which events)
- Event severity levels (ADVISORY, BLOCKING, CRITICAL) and triage rules

**Primary files:**
- `.github/agents/ReaperOAK.agent.md` — SDR schema definition (canonical source of truth)
- `.github/agents/_cross-cutting-protocols.md` — strategic event type definitions and emission rules

---

## BLK-02: SDR Orchestration Protocol

**Description:** Define how ReaperOAK handles the end-to-end SDR lifecycle once a strategic event is emitted. This block covers: event triage and deduplication, blast radius determination (which tickets are affected by the event), selective ticket pausing (affected tickets transition to a PAUSED hold-state while unaffected tickets continue execution), Strategic Layer agent invocation (Architect, ProductManager, Research as needed) to produce the SDR content, SDR approval flow, and ticket resumption protocol after SDR resolution. The orchestration protocol must guarantee that in-flight unaffected work is never interrupted and that completed tickets are never invalidated.

**Effort:** 2–3 days
**Depends On:** BLK-01
**UI Touching:** No

**Scope includes:**
- Event triage: deduplication, severity assessment, blast radius analysis
- Blast radius determination algorithm (map event to affected ticket set via file paths, capability IDs, dependency chains)
- Selective ticket pausing: PAUSED hold-state semantics, which states can be paused, resume triggers
- Strategic Layer invocation: which agents are called for which event types, SDR authoring delegation
- SDR approval flow: auto-approve for ADVISORY severity, human approval for BLOCKING/CRITICAL
- Ticket resumption: transition from PAUSED back to prior state, dependency re-validation
- Guard: completed (DONE) tickets are immutable — SDRs may not revert or invalidate them

**Primary file:** `.github/agents/ReaperOAK.agent.md`

---

## BLK-03: TODO Agent Restrictions & SDR Translation Protocol

**Description:** Codify the TODO Agent as a translate-only decomposition engine that may not originate strategic direction. This block adds: (a) explicit restrictions — TODO Agent may NOT invent capabilities, make architectural decisions, or create tickets without an upstream SDR or user directive as justification; (b) the SDR-to-roadmap translation protocol — given an APPROVED SDR, TODO Agent creates new tickets, marks outdated tickets as DEPRECATED, adjusts dependency graphs, and increments roadmap version; (c) the REQUIRES_STRATEGIC_INPUT event emission — when TODO Agent lacks required upstream artifacts (PRD, architecture decision, SDR), it halts and emits this event instead of guessing. Updates are made in both the agent definition file and the corresponding chunk files.

**Effort:** 2–3 days
**Depends On:** BLK-01
**UI Touching:** No

**Scope includes:**
- Translate-only restriction rules in TODO.agent.md (forbidden: invent capabilities, make architecture decisions, create tickets without upstream justification)
- SDR translation protocol: read APPROVED SDR → identify new capabilities/blocks/tickets → identify outdated tickets → generate roadmap delta
- REQUIRES_STRATEGIC_INPUT event definition and emission conditions
- Ticket deprecation marking: DEPRECATED status semantics (distinct from DONE), archival rules
- Dependency graph adjustment: re-link tickets when deprecated tickets are removed from chains
- Update `.github/vibecoding/chunks/TODO.agent/chunk-01.yaml` — SDR input protocol, translation steps
- Update `.github/vibecoding/chunks/TODO.agent/chunk-02.yaml` — DEPRECATED status, deprecation governance rules

**Primary files:**
- `.github/agents/TODO.agent.md` — restrictions and SDR translation protocol
- `.github/vibecoding/chunks/TODO.agent/chunk-01.yaml` — SDR input handling
- `.github/vibecoding/chunks/TODO.agent/chunk-02.yaml` — deprecation protocol and status updates

---

## BLK-04: Roadmap Versioning & Completed-Ticket Guards

**Description:** Define the roadmap versioning scheme and the immutability guards that protect completed work during strategy evolution. This block covers: (a) version numbering for the roadmap (v1.0 as baseline, minor bumps v1.1/v1.2 for SDR-driven changes, major bumps v2.0 for scope resets requiring human approval); (b) version metadata in TODO files (version header, changelog entries per SDR applied); (c) immutability rules for DONE tickets — completed tickets cannot be reopened, deprecated, or invalidated by any SDR; (d) roadmap diff reporting — a concise summary of what changed between versions (new tickets, deprecated tickets, re-prioritized tickets, adjusted dependencies) emitted as part of the SDR APPLIED confirmation. This block spans both ReaperOAK (versioning authority) and TODO Agent (version metadata in files).

**Effort:** 1–2 days
**Depends On:** BLK-02, BLK-03
**UI Touching:** No

**Scope includes:**
- Roadmap version numbering: v{major}.{minor} scheme, bump rules
- Minor version bump: triggered by each APPLIED SDR (automated)
- Major version bump: triggered by scope reset or capability-level restructure (requires human approval)
- Version metadata format in TODO files: `**Roadmap Version:** v1.1` header, changelog section
- Immutability guard: DONE tickets are read-only — no SDR may reopen, deprecate, or modify them
- Roadmap diff report: structured summary (added_tickets, deprecated_tickets, reprioritized, dependency_changes)
- Version history log: append-only record of all roadmap versions with SDR references

**Primary files:**
- `.github/agents/ReaperOAK.agent.md` — versioning authority, bump rules, diff report format
- `.github/agents/TODO.agent.md` — version metadata in TODO files
- `.github/vibecoding/chunks/TODO.agent/chunk-02.yaml` — versioning and immutability rules

---

## Block Dependency Graph

```
BLK-01 (SDR Schema & Strategic Event Definitions)
  │
  ├──► BLK-02 (SDR Orchestration Protocol)
  │         │
  │         └──► BLK-04 (Roadmap Versioning & Completed-Ticket Guards)
  │                ▲
  └──► BLK-03 (TODO Agent Restrictions & SDR Translation)
              │
              └────┘
```

**Critical path:** BLK-01 → BLK-02 + BLK-03 (parallel) → BLK-04

---

## Summary

| Block | Name | Effort | Depends On | Primary Files |
|-------|------|--------|------------|---------------|
| BLK-01 | SDR Schema & Strategic Event Definitions | 2–3 days | None | ReaperOAK.agent.md, _cross-cutting-protocols.md |
| BLK-02 | SDR Orchestration Protocol | 2–3 days | BLK-01 | ReaperOAK.agent.md |
| BLK-03 | TODO Agent Restrictions & SDR Translation | 2–3 days | BLK-01 | TODO.agent.md, TODO chunks (01, 02) |
| BLK-04 | Roadmap Versioning & Completed-Ticket Guards | 1–2 days | BLK-02, BLK-03 | ReaperOAK.agent.md, TODO.agent.md, TODO chunk-02 |

**Total estimated effort:** 7–11 days (BLK-01 sequential, BLK-02 + BLK-03 parallelizable, BLK-04 after both)
