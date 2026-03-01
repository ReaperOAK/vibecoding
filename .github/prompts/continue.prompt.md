---
name: continue
description: Controlled continuation protocol. Loads resume state, repairs incomplete SDLC chains using specialized agents, then resumes ticket processing with full governance enforcement.
---

We are resuming structured development.

Do NOT reinitialize the project.
Do NOT re-run the takeover prompt.
Do NOT regenerate PRD unless explicitly required.

This is controlled continuation mode.

---

# STEP 1 — STATE REALIGNMENT

Before calling `runSubagent` for ANY work, load full system state.

**1a.** Check for resume artifacts (produced by `stop.prompt.md`):

```
read_file(".github/memory-bank/RESUME_POINT.md")
read_file(".github/memory-bank/SESSION_SUMMARY.md")
read_file(".github/memory-bank/SYSTEM_SNAPSHOT.json")
```

If `RESUME_POINT.md` exists → use it as primary resume anchor (skip 1b).
If missing → fall through to 1b for full state scan.

**1b.** Full state scan (only if no RESUME_POINT.md):

```
read_file(".github/memory-bank/workflow-state.json")
read_file(".github/memory-bank/activeContext.md")
read_file(".github/memory-bank/progress.md")
read_file(".github/memory-bank/decisionLog.md")
read_file(".github/memory-bank/riskRegister.md")
```

**1c.** Get current ticket landscape:

```bash
python3 todo_visual.py --ready --json
```

**1d.** Detect anomalies — scan `workflow-state.json` for:

- Tickets stuck in: IMPLEMENTING, QA_REVIEW, VALIDATION, DOCUMENTATION, CI_REVIEW
  (these need SDLC chain completion in Step 2)
- Tickets in BLOCKED state (check if blocker is now resolved)
- Tickets in REWORK with `rework_count >= 3` (need escalation)
- Tickets marked DONE but missing:
  - Validator entry in `feedback-log.md` → needs Validator pass
  - Documentation entry → needs Documentation pass
  - Git commit with ticket ID → needs scoped commit

**1e.** Archive consumed resume artifacts:

```bash
# Move consumed artifacts to archive (do NOT delete — preserve history)
mkdir -p .github/memory-bank/archive
mv .github/memory-bank/RESUME_POINT.md .github/memory-bank/archive/RESUME_POINT-{date}.md
mv .github/memory-bank/SESSION_SUMMARY.md .github/memory-bank/archive/SESSION_SUMMARY-{date}.md
mv .github/memory-bank/SYSTEM_SNAPSHOT.json .github/memory-bank/archive/SYSTEM_SNAPSHOT-{date}.json
```

Do NOT write code yet. State alignment must complete first.

---

# STEP 2 — BACKLOG CLEANUP (PARALLEL)

For every ticket found in Step 1d with incomplete SDLC, dispatch the
appropriate agents to complete the chain. Use EXACT agent names below.

**Tickets stuck mid-SDLC (resume chain from current state):**

| Current State | Agent Calls Needed |
|---------------|-------------------|
| IMPLEMENTING (stalled) | Roll back to READY — reassign in Step 3 |
| QA_REVIEW (QA not run) | `runSubagent("QA Engineer", ...)` → then Validator → Doc → CI → Commit |
| QA_REVIEW (Validator not run) | `runSubagent("Validator", ...)` → then Doc → CI → Commit |
| VALIDATION | `runSubagent("Documentation Specialist", ...)` → then CI → Commit |
| DOCUMENTATION | `runSubagent("CI Reviewer", ...)` → then Commit |
| CI_REVIEW | Commit only: `git add {files} && git commit -m "[{TICKET-ID}] ..."` |

**Example: Ticket stuck at QA_REVIEW (Validator not yet run):**

```
runSubagent("Validator", prompt="
  Ticket ID: {TICKET-ID}
  Objective: Verify Definition of Done compliance for ticket {TICKET-ID}.
  Check all 10 DoD items (DOD-01 through DOD-10).
  Read the implementation artifacts at: {file_paths}
  Read prior QA feedback at: .github/memory-bank/feedback-log.md
  Write validation report to: docs/reviews/validation/{TICKET-ID}-validation.yaml
  Verdict: APPROVED or REJECTED with specific DOD-XX failures.
")
```

```
runSubagent("Documentation Specialist", prompt="
  Ticket ID: {TICKET-ID}
  Objective: Update documentation artifacts for ticket {TICKET-ID}.
  Read implementation at: {file_paths}
  Update: CHANGELOG.md, README.md (if interface changed), JSDoc/TSDoc.
  Confirm completion with artifact list.
")
```

```
runSubagent("CI Reviewer", prompt="
  Ticket ID: {TICKET-ID}
  Objective: Verify lint, type-check, and complexity for ticket {TICKET-ID}.
  Run: tsc --noEmit, eslint, complexity analysis.
  Report: PASS or REJECT with specific findings.
")
```

**DONE tickets missing chain steps:**

```
# Missing Validator pass
runSubagent("Validator", prompt="Retroactive DoD check for ticket {TICKET-ID}...")

# Missing Documentation
runSubagent("Documentation Specialist", prompt="Retroactive doc update for ticket {TICKET-ID}...")

# Missing commit
git add {declared_file_paths} CHANGELOG.md
git commit -m "[{TICKET-ID}] description"
```

Run all independent cleanup calls **in parallel** — tickets that don't
share file paths can be processed simultaneously.

---

# STEP 3 — SELECT NEXT EXECUTABLE TICKETS

**3a.** Get READY tickets:

```bash
python3 todo_visual.py --ready --json
```

**3b.** Filter and sort:

1. Exclude BLOCKED tickets (check `blocker_reason` in workflow-state.json)
2. Exclude tickets already in review stages (being handled by Step 2)
3. Sort by priority: P0 first, then P1, P2, etc.
4. Check file conflicts: no two tickets may modify the same file simultaneously

**3c.** For each selected ticket, run conflict detection:

```
For ticket in ready_tickets:
  ticket_files = ticket.file_paths
  active_files = union of all in-flight ticket file_paths
  if intersection(ticket_files, active_files) is empty:
    → eligible for dispatch
  else:
    → defer (wait for conflicting ticket to complete)
```

**3d.** Dispatch workers — one `runSubagent` per ticket:

```
# Example: Backend ticket
runSubagent("Backend", prompt="
  Ticket ID: {TICKET-ID}
  Worker ID: BackendWorker-{shortUuid}
  Objective: {task description from ticket file}
  Acceptance Criteria:
    - {criterion 1}
    - {criterion 2}
  Upstream Artifacts:
    - {path}: {description}
  Deliverables: {file_paths}
  Boundaries: Do NOT modify files outside declared paths
  Scope: THIS TICKET ONLY
  Chunks: Load .github/vibecoding/chunks/Backend.agent/
")

# Example: Frontend ticket
runSubagent("Frontend Engineer", prompt="
  Ticket ID: {TICKET-ID}
  Worker ID: FrontendWorker-{shortUuid}
  Objective: {task description}
  ...same delegation structure...
  Chunks: Load .github/vibecoding/chunks/Frontend.agent/
")
```

**Agent name reference (EXACT, case-sensitive):**

| Role | runSubagent name |
|------|-----------------|
| Backend | `"Backend"` |
| Frontend | `"Frontend Engineer"` |
| QA | `"QA Engineer"` |
| Security | `"Security Engineer"` |
| DevOps | `"DevOps Engineer"` |
| Documentation | `"Documentation Specialist"` |
| Validator | `"Validator"` |
| CI Review | `"CI Reviewer"` |
| Architecture | `"Architect"` |
| Research | `"Research Analyst"` |
| Product | `"Product Manager"` |
| UI Design | `"UIDesigner"` |
| Task Decomposition | `"TODO"` |

Launch ALL conflict-free tickets simultaneously.
One ticket → one worker → one lifecycle → one commit.

---

# STEP 4 — PER-TICKET SDLC CHAIN

For each dispatched ticket, enforce the full 9-state lifecycle:

```
READY → LOCKED → IMPLEMENTING → QA_REVIEW → VALIDATION → DOCUMENTATION → CI_REVIEW → COMMIT → DONE
```

After the implementing worker emits TASK_COMPLETED, run the mandatory
post-execution chain using these exact calls:

```
# Step 1: QA Review
runSubagent("QA Engineer", prompt="
  Review ticket {TICKET-ID}. Verify test coverage ≥80%.
  Run test suite. Check for console errors, unhandled promises.
  Verdict: PASS or REJECT.
")

# Step 2: Validator (DoD Compliance)
runSubagent("Validator", prompt="
  Verify DoD for ticket {TICKET-ID}. All 10 items (DOD-01 to DOD-10).
  Verdict: APPROVED or REJECTED with DOD-XX failures.
")

# Step 3: Documentation
runSubagent("Documentation Specialist", prompt="
  Update docs for ticket {TICKET-ID}.
  CHANGELOG, README (if interface changed), JSDoc/TSDoc.
")

# Step 4: CI Review
runSubagent("CI Reviewer", prompt="
  Check lint, types, complexity for ticket {TICKET-ID}.
  Verdict: PASS or REJECT.
")

# Step 5: Commit (ReaperOAK executes directly)
git add {declared_file_paths} CHANGELOG.md
git commit -m "[{TICKET-ID}] description"
```

**On rejection at any step:**
- Increment shared `rework_count` for the ticket
- If `rework_count < 3`: re-delegate to implementing agent with rejection report
- If `rework_count >= 3`: escalate to user

No skipping stages. No batching commits. No partial execution.

---

# STEP 5 — CONCURRENCY (OCF)

Maintain minimum **10 active workers** at all times.

If fewer than 10 Class A (primary) tickets are in-flight, spawn
Class B (background) workers to fill remaining capacity:

```
# Security audit
runSubagent("Security Engineer", prompt="
  Background task: BG-SEC-AUDIT. Scan codebase for OWASP/STRIDE gaps.
  Read-only analysis. Report findings as improvement ticket proposals.
")

# Architecture alignment
runSubagent("Architect", prompt="
  Background task: BG-ARCH-ALIGN. Verify implementation matches ADRs.
  Read-only analysis. Report drift as improvement ticket proposals.
")

# Tech debt scan
runSubagent("Backend", prompt="
  Background task: BG-TECH-DEBT-SCAN. Identify code smells, complexity hotspots.
  Read-only analysis. Report findings.
")

# QA coverage check
runSubagent("QA Engineer", prompt="
  Background task: BG-QA-COVERAGE-CHECK. Find untested paths, coverage gaps.
  Read-only analysis. Report findings.
")

# Documentation completeness
runSubagent("Documentation Specialist", prompt="
  Background task: BG-DOC-COMPLETENESS. Audit doc freshness. Find missing sections.
  Read-only analysis. Report findings.
")

# Performance analysis
runSubagent("Frontend Engineer", prompt="
  Background task: BG-PERFORMANCE-ANALYSIS. Profile hot paths, identify bottlenecks.
  Read-only analysis. Report findings.
")
```

**Preemption:** When new Class A tickets arrive, pause lowest-priority
Class B worker and reassign capacity to Class A.

**Throttle:** If primary backlog > 20 tickets, suspend all Class B spawning.

---

# STEP 6 — DRIFT CONTROL

If any agent:

- Skips a commit → DRIFT-005 (CHAIN_STEP_SKIPPED)
- Skips validation → DRIFT-005
- Uses `git add .` → DRIFT-002 (UNSCOPED_COMMIT)
- Modifies undeclared files → DRIFT-002
- Skips memory update → DRIFT-003 (MISSING_MEMORY_ENTRY)
- References other ticket IDs → DRIFT-006 (MULTI_TICKET_VIOLATION, HARD KILL)
- Emits TASK_COMPLETED without evidence → DRIFT-007 (UNVERIFIED_EVIDENCE)

Action per violation:
1. Emit `PROTOCOL_VIOLATION` event
2. Pause the affected ticket (other tickets continue)
3. Spawn repair agent if auto-repairable:
   - DRIFT-002 → re-stage with explicit file list, recommit
   - DRIFT-003 → append memory entry from ticket evidence
   - DRIFT-005 → run missing chain step(s)
   - DRIFT-007 → re-delegate to implementing worker with evidence requirement
4. DRIFT-006 → terminate worker immediately, spawn fresh worker for rework

---

# STEP 7 — STRATEGIC EVOLUTION (NON-DISRUPTIVE)

If during execution any agent detects:

- **ARCHITECTURE_RISK** → `runSubagent("Architect", prompt="Assess risk...")`
- **SECURITY_RISK** → `runSubagent("Security Engineer", prompt="Evaluate threat...")`
- **SCOPE_CONFLICT** → `runSubagent("Product Manager", prompt="Resolve ambiguity...")`
- **REQUIRES_STRATEGIC_INPUT** → route to appropriate strategic agent

Rules:
1. Pause ONLY affected tickets — all other execution continues
2. Strategic agents may propose SDRs (Strategy Deviation Records)
3. ReaperOAK evaluates SDR impact → approves/rejects
4. Approved SDRs: invoke `runSubagent("TODO", ...)` to regenerate affected tickets
5. Updated tickets enter READY when dependencies met
6. No global halt. No full re-decomposition. Minimal disruption.

---

# STEP 8 — SESSION END

Development continues until:

- All READY tickets processed through full SDLC
- No pending PROTOCOL_VIOLATION events
- No validation backlog (all DONE tickets have Validator + Doc + CI entries)
- No security backlog
- CI clean (`git status --porcelain` empty)

When ending the session, invoke the stop protocol to preserve state:

> Execute `.github/prompts/stop.prompt.md`

This will produce `RESUME_POINT.md`, `SESSION_SUMMARY.md`, and
`SYSTEM_SNAPSHOT.json` — consumed by this prompt's Step 1 on next run.

---

**Operating constraints:**

- Move forward — do not re-diagnose the entire repository
- Do not rewrite stable components
- Do not generate new roadmap unless an approved SDR requires it
- Do not reduce worker concurrency below 10 (OCF)
- Do not allow one-shot coding (enforce 4-step iteration per §9 anti-one-shot)
- Maintain velocity, governance, and parallelism