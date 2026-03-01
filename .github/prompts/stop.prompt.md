---
name: stop
description: This prompt defines the structured shutdown protocol for the vibecoding multi-agent system. It outlines the step-by-step process to cleanly halt all development activity while preserving state integrity. This is not abandonment; it is a structured freeze to ensure a safe and orderly pause in operations.
---

We are entering SYSTEMATIC SHUTDOWN MODE.

Goal:
Cleanly pause all development activity while preserving full state integrity.

This is not abandonment.
This is structured freeze.

No new feature work allowed.
No new tickets allowed.
No architectural changes allowed.

---

# STEP 1 — HALT NEW SPAWNS

ReaperOAK must:

1. Stop spawning new workers.
2. Stop scheduling new tickets.
3. Allow currently active workers to complete their current SDLC stage.
4. Do NOT abruptly terminate active ticket flows.

---

# STEP 2 — COMPLETE ACTIVE TICKETS SAFELY

For each ticket past READY:

If in LOCKED or IMPLEMENTING:
→ Complete QA_REVIEW → VALIDATION → DOCUMENTATION → CI_REVIEW → COMMIT

If in QA_REVIEW:
→ Complete VALIDATION → DOCUMENTATION → CI_REVIEW → COMMIT

If in VALIDATION:
→ Complete DOCUMENTATION → CI_REVIEW → COMMIT

If in DOCUMENTATION:
→ Complete CI_REVIEW → COMMIT

If in CI_REVIEW:
→ Complete COMMIT

No ticket may remain mid-SDLC.

Each active ticket must end in:
DONE or BLOCKED (explicitly marked).

No partial states.

---

# STEP 3 — RECONCILE TICKET STATES

Scan all tickets:

1. Ensure no ticket is stuck in:
   - LOCKED
   - IMPLEMENTING
   - QA_REVIEW
   - VALIDATION
   - DOCUMENTATION
   - CI_REVIEW

2. Convert any unresolved ticket to:
   READY (if incomplete but safe)
   BLOCKED (if dependency missing or ticket invalid)

3. Regenerate dependency graph.
4. Verify no circular dependencies.
5. Verify no dangling locks.

---

# STEP 4 — LOCK FILE & RESOURCE CLEANUP

1. Release all file locks.
2. Clear temporary lock files.
3. Validate no resource conflicts remain.
4. Validate task-lock-schema consistency.

---

# STEP 5 — MEMORY CONSOLIDATION

Update memory-bank:

- activeContext.md → summarize current project state
- progress.md → reflect ticket completion percentage
- decisionLog.md → append session decisions
- riskRegister.md → update open risks
- workflow-state.json → reflect all ticket states
- artifacts-manifest.json → verify artifact integrity
- feedback-log.md → append session QA/Validator/CI feedback

Generate:
`.github/memory-bank/SESSION_SUMMARY.md`

Include:
- Tickets completed this session
- Tickets remaining
- Tickets blocked
- Strategic decisions made
- Architecture changes
- Security updates
- Tech debt introduced or reduced

---

# STEP 6 — OBSERVABILITY SNAPSHOT

Generate:
`.github/memory-bank/SYSTEM_SNAPSHOT.json`

Must include:
- Active ticket count
- READY ticket count
- BLOCKED ticket count
- DONE ticket count
- Worker utilization summary
- Average SDLC time
- Violations detected this session
- Background audit results
- CI status

This becomes resume anchor.

---

# STEP 7 — GOVERNANCE VERIFICATION

Before final stop:

Verify:

- No ticket skipped commit
- No ticket skipped validator
- No ticket skipped documentation
- No policy violation unresolved
- No git add . used
- No uncommitted changes exist
- CI passing
- Hooks executed properly

If violation found:
Resolve before shutdown.

---

# STEP 8 — CLEAN RESUME MARKER

Create:
`.github/memory-bank/RESUME_POINT.md`

Contents:

- Last completed ticket ID
- Last roadmap version
- Current branch
- Next 5 READY tickets (from `python3 todo_visual.py --ready --json`)
- Current GOVERNANCE_VERSION
- Ticket statistics (total, DONE, READY, BLOCKED)
- Known risks (from riskRegister.md)
- Known strategic flags / active SDRs
- Session artifacts produced (SESSION_SUMMARY.md, SYSTEM_SNAPSHOT.json)

This file is the primary resume anchor for `continue.prompt.md`.
The continuation prompt reads it FIRST and skips broad re-analysis if present.

---

# STEP 9 — SYSTEM STATUS

Final state must be:

No active workers
No partial SDLC tickets
No dangling locks
Clean git state
Updated memory
Updated observability
Clear resume point

Then emit:

SYSTEM_STATUS: SAFE_TO_RESUME

Stop.

No further execution.