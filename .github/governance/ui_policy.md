<!-- GOVERNANCE_VERSION: 9.0.0 -->

# UI/UX Enforcement Policy

> **Governance Version:** 9.0.0
> **Source:** Extracted from ReaperOAK.agent.md §14
> **Scope:** Hard gate for UI-touching tickets, Stitch artifact checklist,
> enforcement rules, detection heuristics, and override protocol.

---

## 1. Hard Gate — Not Soft Flagging

Before any Frontend worker receives a UI-touching ticket, UIDesigner MUST
have produced Stitch design-system mockups. This is a **blocking gate** —
not a warning or suggestion.

---

## 2. Stitch Artifact Checklist

Before a UI-touching ticket transitions from READY → LOCKED for a Frontend
worker, ALL of these items must be verified:

| # | Checklist Item | Verification |
|---|---------------|-------------|
| 1 | Stitch mockup file exists at `docs/uiux/mockups/{ticket-id}.md` | File presence check |
| 2 | Mockup approved by UIDesigner (status: APPROVED) | Status field in mockup |
| 3 | Component inventory listed in mockup | Section presence check |
| 4 | Responsive breakpoints defined | Section presence check |
| 5 | Accessibility annotations present | Section presence check |

---

## 3. Enforcement Rules

- If **ANY** checklist item is missing → ticket is **BLOCKED** — it cannot
  transition from READY to LOCKED for Frontend workers
- If UIDesigner reports completion but artifacts are missing on disk →
  REJECT UIDesigner completion and re-delegate with specific missing files
- Backend tickets that are NOT UI-touching skip this gate entirely
- Override requires explicit user approval (logged in `decisionLog.md`)

---

## 4. UI-Touching Detection

A ticket is classified as UI-touching if:

1. Its metadata includes `UI Touching: yes`, OR
2. Its description contains UI keywords:
   - `UI`, `frontend`, `screen`, `portal`
   - `dashboard`, `component`, `layout`

Detection is applied at scheduling time when evaluating READY tickets
for Frontend worker assignment.

---

## 5. Verification Command

```bash
ls docs/uiux/mockups/<ticket-id>.md
```

This command is run as part of the READY → LOCKED guard for Frontend
workers. If the file does not exist, the transition is blocked.

---

## 6. Override Protocol

If design artifacts are intentionally deferred or the ticket is a
non-visual frontend change (e.g., state management refactor):

1. User must explicitly approve the override
2. Override is logged in `decisionLog.md` with:
   - Ticket ID
   - Reason for override
   - User who approved
   - Timestamp
3. The ticket proceeds without the Stitch artifact gate
4. This is the ONLY way to bypass the UI hard gate

---

## 7. Gate Integration

This gate operates at the READY → LOCKED transition in the lifecycle
(see `lifecycle.md`). It is an **additional guard** on top of the standard
transition guards (dependency check, conflict check) — specific to tickets
assigned to Frontend Engineer workers that are classified as UI-touching.

| Condition | Gate Result | Action |
|-----------|-------------|--------|
| Not UI-touching | SKIP | Gate does not apply |
| UI-touching + all 5 items present | PASS | Proceed to LOCKED |
| UI-touching + any item missing | BLOCK | Ticket stays in READY |
| UI-touching + user override | PASS (override) | Log override, proceed |
