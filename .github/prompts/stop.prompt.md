---
name: stop
description: Structured shutdown protocol. Drains active tickets through their remaining SDLC stages using specialized agents, consolidates memory, and produces resume artifacts for continue.prompt.md.
---

We are entering SYSTEMATIC SHUTDOWN MODE.

Goal: Cleanly pause all development while preserving full state for resumption.

No new feature work. No new tickets. No architectural changes.

---

# STEP 1 — HALT NEW SPAWNS

Immediate actions:

1. Do NOT call `runSubagent` for any new ticket implementation.
2. Do NOT invoke the TODO Agent for decomposition.
3. Do NOT accept or process new SDR proposals.
4. Allow currently active workers to complete their current SDLC stage only.

---

# STEP 2 — DRAIN ACTIVE TICKETS

Read `.github/memory-bank/workflow-state.json` to find all non-terminal tickets.
Run `python3 todo_visual.py --ready --json` to see full ticket landscape.

For each ticket past READY, complete its remaining SDLC chain using the
exact `runSubagent` calls below. Do NOT skip any stage.

**If in LOCKED or IMPLEMENTING:**

1. Let implementing worker finish (or roll back to READY if stalled >30min)
2. Then run the full post-execution chain:

```
runSubagent("QA Engineer", prompt="Review ticket {TICKET-ID}. Run tests, verify coverage ≥80%...")
runSubagent("Validator", prompt="Verify DoD compliance for ticket {TICKET-ID}. Check all 10 items...")
runSubagent("Documentation Specialist", prompt="Update docs for ticket {TICKET-ID}...")
runSubagent("CI Reviewer", prompt="Check lint, types, complexity for ticket {TICKET-ID}...")
```

3. Commit: `git add {declared file_paths} CHANGELOG.md && git commit -m "[{TICKET-ID}] description"`

**If in QA_REVIEW:** Run from Validator onward.
**If in VALIDATION:** Run from Documentation Specialist onward.
**If in DOCUMENTATION:** Run from CI Reviewer onward.
**If in CI_REVIEW:** Commit only.

Each ticket must end in DONE or be explicitly set to READY/BLOCKED.
No ticket may remain in an intermediate state.

---

# STEP 3 — RECONCILE TICKET STATES

Use `read_file` to scan ticket files in `TODO/tasks/`:

1. Any ticket stuck in LOCKED/IMPLEMENTING/QA_REVIEW/VALIDATION/DOCUMENTATION/CI_REVIEW
   that was NOT drained in Step 2 → set to READY (if safe) or BLOCKED (if invalid).
2. Update `workflow-state.json` with final states for all tickets.
3. Verify no circular dependencies in the DAG.
4. Verify no dangling locks remain.

---

# STEP 4 — LOCK & RESOURCE CLEANUP

1. Delete any lock files in `.github/locks/` that reference terminated workers.
2. Validate remaining locks against `task-lock-schema.json`.
3. Run `git status` to confirm no unexpected staged/unstaged changes.

---

# STEP 5 — MEMORY CONSOLIDATION

Use `read_file` then `replace_string_in_file` or append to update each file:

| File | Action |
|------|--------|
| `.github/memory-bank/activeContext.md` | Append session summary: what was worked on, current state |
| `.github/memory-bank/progress.md` | Append: tickets completed this session, completion percentage |
| `.github/memory-bank/decisionLog.md` | Append: session decisions and trade-offs (ReaperOAK only) |
| `.github/memory-bank/riskRegister.md` | Append: new risks identified, resolved risks |
| `.github/memory-bank/workflow-state.json` | Overwrite: reflect final ticket states from Step 3 |
| `.github/memory-bank/artifacts-manifest.json` | Verify: all DONE ticket artifacts have SHA-256 hashes |
| `.github/memory-bank/feedback-log.md` | Append: QA/Validator/CI feedback from this session |

Then use `create_file` to generate:

**`.github/memory-bank/SESSION_SUMMARY.md`**

```markdown
# Session Summary — {date}

## Tickets Completed
- {TICKET-ID}: {description}

## Tickets Remaining (READY)
- {TICKET-ID}: {description} (priority: P{n})

## Tickets Blocked
- {TICKET-ID}: {reason}

## Tickets In Rework/Escalated
- {TICKET-ID}: {reason}, rework_count: {n}

## Strategic Decisions
- {SDR-ID}: {title} — {status}

## Architecture Changes
- {description}

## Security Updates
- {description}

## Tech Debt Delta
- Introduced: {items}
- Reduced: {items}
```

---

# STEP 6 — OBSERVABILITY SNAPSHOT

Use `create_file` to generate:

**`.github/memory-bank/SYSTEM_SNAPSHOT.json`**

```json
{
  "timestamp": "{ISO8601}",
  "tickets": {
    "total": 0,
    "done": 0,
    "ready": 0,
    "blocked": 0,
    "implementing": 0,
    "in_review": 0
  },
  "session_metrics": {
    "tickets_completed_this_session": 0,
    "average_sdlc_duration_minutes": 0,
    "rework_count": 0,
    "violations_detected": 0
  },
  "worker_utilization": {
    "peak_concurrent_workers": 0,
    "total_worker_spawns": 0,
    "class_a_tickets_processed": 0,
    "class_b_tickets_processed": 0
  },
  "governance": {
    "governance_version": "9.1.0",
    "ci_status": "passing|failing|unknown",
    "unresolved_violations": []
  },
  "background_audit_results": {
    "security": "not_run|clean|findings",
    "architecture": "not_run|aligned|drift",
    "tech_debt": "not_run|low|medium|high",
    "coverage": "not_run|sufficient|gaps"
  }
}
```

---

# STEP 7 — GOVERNANCE VERIFICATION

Before final stop, verify ALL of these. Use `run_in_terminal` for commands:

```bash
# Check for uncommitted changes
git status --porcelain

# Check for unscoped commits (git add . violations)
git log --oneline -20

# Verify no TODO/FIXME in recently changed files
git diff --name-only HEAD~5 | xargs grep -l 'TODO\|FIXME\|HACK\|XXX' 2>/dev/null || echo "Clean"
```

Checklist:
- [ ] No ticket skipped commit (cross-check workflow-state.json DONE tickets vs git log)
- [ ] No ticket skipped Validator (check feedback-log.md for Validator entries per DONE ticket)
- [ ] No ticket skipped documentation (check feedback-log.md for Doc entries per DONE ticket)
- [ ] No unresolved PROTOCOL_VIOLATION events
- [ ] No `git add .` in recent commits
- [ ] No uncommitted changes (`git status --porcelain` is empty)
- [ ] CI passing (check last workflow run)

If any violation found:
- Spawn the appropriate agent to fix it:
  - Missing QA → `runSubagent("QA Engineer", ...)`
  - Missing validation → `runSubagent("Validator", ...)`
  - Missing docs → `runSubagent("Documentation Specialist", ...)`
  - Missing commit → execute scoped `git add` + `git commit`
- Then re-verify.

---

# STEP 8 — CLEAN RESUME MARKER

Run: `python3 todo_visual.py --ready --json` to get current READY tickets.
Read `.github/memory-bank/riskRegister.md` for open risks.

Use `create_file` to generate:

**`.github/memory-bank/RESUME_POINT.md`**

```markdown
# Resume Point — {date}

## Last Completed Ticket
{TICKET-ID}

## Roadmap Version
v{X.Y}

## Branch
{current branch from `git branch --show-current`}

## GOVERNANCE_VERSION
9.1.0

## Ticket Statistics
- Total: {n}
- DONE: {n}
- READY: {n}
- BLOCKED: {n}

## Next READY Tickets (Priority Order)
1. {TICKET-ID}: {title} (P{n}, owner: {role})
2. {TICKET-ID}: {title} (P{n}, owner: {role})
3. {TICKET-ID}: {title} (P{n}, owner: {role})
4. {TICKET-ID}: {title} (P{n}, owner: {role})
5. {TICKET-ID}: {title} (P{n}, owner: {role})

## Known Risks
- {risk from riskRegister.md}

## Active SDRs
- {SDR-ID}: {title} — {status}

## Session Artifacts
- `.github/memory-bank/SESSION_SUMMARY.md`
- `.github/memory-bank/SYSTEM_SNAPSHOT.json`
- `.github/memory-bank/RESUME_POINT.md` (this file)

## Cross-Reference
This file is consumed by `continue.prompt.md` Step 1.
```

---

# STEP 9 — FINAL STATUS

Verify final state:
- No active workers (no pending `runSubagent` calls)
- No partial SDLC tickets (all DONE, READY, or BLOCKED)
- No dangling locks (`.github/locks/` clean)
- Clean git state (`git status --porcelain` empty)
- Memory bank updated (Step 5 complete)
- Observability snapshot written (Step 6 complete)
- Resume point created (Step 8 complete)

Then report to user:

```
SYSTEM_STATUS: SAFE_TO_RESUME

Session complete.
- Tickets completed: {n}
- Tickets remaining: {n}
- Resume point: .github/memory-bank/RESUME_POINT.md
- Next continuation: invoke continue.prompt.md
```

Stop. No further execution.