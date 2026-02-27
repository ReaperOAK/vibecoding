# UI/UX Enforcement Hardening — Execution Blocks

**Parent:** CAP-06 from vision.md
**Capability:** UI/UX Enforcement Hardening
**Created:** 2026-02-27T00:00:00Z
**Task Prefix:** WPAE

---

## Design Artifact Contract Reference

CAP-06 upgrades UI/UX enforcement from soft flagging to hard pipeline-blocking enforcement. The core invariant: **no UI-touching ticket may advance past QA_REVIEW without a complete, approved design artifact set in `/docs/uiux/<feature>/`.**

Required artifacts per UI-touching feature (produced by UIDesigner):

| # | Artifact | Format | Purpose |
|---|----------|--------|---------|
| 1 | Stitch mockup source | `.stitch` or equivalent | Design-system-compliant mockup |
| 2 | Mockup raster export | `.png` | Visual reference for Frontend |
| 3 | Mockup HTML export | `.html` | Interactive preview / handoff |
| 4 | Interaction spec | `.md` | User flows, state transitions, edge cases |
| 5 | Accessibility checklist | `.md` | WCAG compliance verification |

Directory convention: `/docs/uiux/<feature-slug>/` — one directory per feature, all 5 artifacts present before ticket resumes.

---

## BLK-01: UI Artifact Contract & UIDesigner Pipeline

**Description:** Define the canonical UI artifact contract — the complete manifest of design deliverables that UIDesigner must produce for every UI-touching feature. Establish the `/docs/uiux/<feature-slug>/` directory convention, specify required file types (Stitch mockup source, PNG export, HTML export, interaction spec, accessibility checklist), define artifact completeness validation rules, and update the UIDesigner agent definition (`.github/agents/UIDesigner.agent.md`) with the Stitch-based production pipeline. This block produces the authoritative artifact contract that all other blocks reference — ReaperOAK's gate checks it, Frontend validates against it, and Validator enforces it.

**Effort:** 1–2 days
**Depends On:** None
**UI Touching:** No

**Scope includes:**
- Canonical artifact manifest (5 required files per feature, with naming conventions)
- `/docs/uiux/<feature-slug>/` directory structure specification
- UIDesigner agent definition update: Stitch mockup generation workflow, PNG/HTML export steps, interaction spec template, accessibility checklist template
- UIDesigner chunk updates (if chunks exist) to embed artifact production protocol
- Artifact completeness validation rules (machine-checkable: all 5 files present, non-empty, correct extensions)
- `DESIGN_COMPLETE` event definition emitted by UIDesigner when all artifacts are stored

**Not in scope:** ReaperOAK gate logic (→ BLK-02), Validator/Frontend enforcement (→ BLK-03), Guardian bypass detection (→ BLK-04)

---

## BLK-02: ReaperOAK Hard Gate Enforcement

**Description:** Implement the hard UI/UX gate in ReaperOAK's orchestration loop — the pipeline-blocking mechanism that detects UI-touching tickets, checks for artifact completeness, and pauses/resumes tickets based on UIDesigner output. When a UI-touching ticket is selected for execution, ReaperOAK must: (1) check `/docs/uiux/<feature-slug>/` for the complete artifact set defined in BLK-01, (2) if any artifact is missing, emit a `REQUIRES_UI_DESIGN` event, pause the ticket (hold in LOCKED, do not advance to IMPLEMENTING), and auto-invoke UIDesigner as a worker, (3) resume the ticket only after UIDesigner emits `DESIGN_COMPLETE` and all artifacts are verified on disk. This replaces the current soft-flag model with a hard block — no ticket proceeds without artifacts.

**Effort:** 2–3 days
**Depends On:** BLK-01
**UI Touching:** No

**Scope includes:**
- ReaperOAK agent definition update (`.github/agents/ReaperOAK.agent.md`): UI gate section rewrite
- `REQUIRES_UI_DESIGN` event definition and emission protocol
- Ticket pause semantics: hold in LOCKED state, do not advance to IMPLEMENTING while artifacts missing
- Auto-invocation of UIDesigner worker with delegation packet containing feature slug and artifact manifest
- Resume protocol: listen for `DESIGN_COMPLETE`, re-verify artifact directory, advance ticket
- Edge case handling: UIDesigner failure (retry once, then escalate to user), partial artifact set (reject, require all 5)
- Integration with continuous scheduling: paused tickets do not consume worker pool capacity

**Not in scope:** UIDesigner's internal production pipeline (→ BLK-01), Validator/Frontend enforcement (→ BLK-03), Guardian bypass detection (→ BLK-04)

---

## BLK-03: Validator & Frontend Defense-in-Depth Enforcement

**Description:** Add defense-in-depth enforcement layers so that even if ReaperOAK's hard gate (BLK-02) is somehow bypassed, UI-touching tickets cannot complete without design artifacts. Two independent enforcement points: (1) **Frontend self-enforcement** — the Frontend agent must independently check for design artifacts in `/docs/uiux/<feature-slug>/` before starting any UI-touching task; if artifacts are missing, Frontend emits `BLOCKED_BY: missing UI artifacts` and refuses execution. (2) **Validator UI compliance check** — Validator's Definition of Done checklist gains a mandatory UI artifact verification item; any UI-touching ticket at VALIDATION without complete artifacts is REJECTED with a specific rejection code. Update Validator agent definition, Validator chunk-01.yaml, and Frontend agent protocols.

**Effort:** 1–2 days
**Depends On:** BLK-01
**UI Touching:** No

**Scope includes:**
- Validator agent definition update (`.github/agents/Validator.agent.md`): add UI artifact completeness to DoD checklist
- Validator chunk update (`.github/vibecoding/chunks/Validator.agent/chunk-01.yaml`): add UI artifact verification protocol with specific check steps (file existence, non-empty, correct extensions)
- Validator rejection code for missing UI artifacts (distinct from other DoD failures)
- Frontend agent self-enforcement protocol: pre-execution artifact check for UI-touching tasks
- Frontend `BLOCKED_BY` event emission when artifacts are missing
- Cross-cutting protocol update if needed (`.github/agents/_cross-cutting-protocols.md`): document the UI artifact enforcement chain

**Not in scope:** Artifact contract definition (→ BLK-01), ReaperOAK gate logic (→ BLK-02), Guardian bypass detection (→ BLK-04)

---

## BLK-04: Guardian UI Bypass Detection Rules

**Description:** Add loop-detection and bypass-detection rules to the Guardian subsystem that catch UI enforcement violations — tickets that somehow reach IMPLEMENTING or later states without proper design artifacts. These rules act as a final safety net beyond ReaperOAK's gate (BLK-02) and Validator/Frontend enforcement (BLK-03). Detection patterns include: UI-touching tickets advancing past LOCKED without `DESIGN_COMPLETE` event, repeated `REQUIRES_UI_DESIGN` emissions for the same ticket without resolution, Frontend executing UI-touching tasks without prior UIDesigner completion, and UI-touching tickets reaching DONE without artifact directory on disk.

**Effort:** 1 day
**Depends On:** BLK-01, BLK-02
**UI Touching:** No

**Scope includes:**
- Guardian loop-detection rules update (`.github/guardian/loop-detection-rules.md`): add UI bypass detection patterns
- Detection pattern: UI-touching ticket in IMPLEMENTING without `DESIGN_COMPLETE` in event log
- Detection pattern: `REQUIRES_UI_DESIGN` emitted ≥ 3 times for same ticket (stall signal)
- Detection pattern: Frontend agent starting UI-touching task without UIDesigner task in dependency chain marked DONE
- Detection pattern: UI-touching ticket reaching DONE without `/docs/uiux/<feature-slug>/` directory containing all required artifacts
- Remediation actions: emit alert, halt ticket advancement, escalate to ReaperOAK/user
- Integration with existing stall detection signals (complement, not replace)

**Not in scope:** Artifact contract definition (→ BLK-01), ReaperOAK gate logic (→ BLK-02), Validator/Frontend enforcement (→ BLK-03)

---

## Block Dependency Graph

```
BLK-01 (UI Artifact Contract & UIDesigner Pipeline)
  │
  ├──► BLK-02 (ReaperOAK Hard Gate Enforcement)
  │        │
  │        └──► BLK-04 (Guardian UI Bypass Detection)
  │
  └──► BLK-03 (Validator & Frontend Defense-in-Depth)
```

**Critical path:** BLK-01 → BLK-02 → BLK-04
**Parallel track:** BLK-03 can run in parallel with BLK-02 (both depend only on BLK-01)

---

## Summary

| Block | Name | Effort | Depends On | Primary Files |
|-------|------|--------|------------|---------------|
| BLK-01 | UI Artifact Contract & UIDesigner Pipeline | 1–2 days | None | UIDesigner.agent.md, UIDesigner chunks |
| BLK-02 | ReaperOAK Hard Gate Enforcement | 2–3 days | BLK-01 | ReaperOAK.agent.md |
| BLK-03 | Validator & Frontend Defense-in-Depth | 1–2 days | BLK-01 | Validator.agent.md, Validator chunk-01.yaml, Frontend protocols |
| BLK-04 | Guardian UI Bypass Detection Rules | 1 day | BLK-01, BLK-02 | loop-detection-rules.md |

**Total estimated effort:** 5–8 days (BLK-01 sequential, BLK-02 + BLK-03 parallelizable, BLK-04 after BLK-02)
