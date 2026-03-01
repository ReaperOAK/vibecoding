---
name: continue
description: This prompt is used to continue structured development after a pause or interruption. It ensures that the development process remains disciplined, maintains velocity, and adheres to governance protocols while resuming work on active tickets and managing the backlog effectively.
---

We are resuming structured development.

Do NOT reinitialize.
Do NOT re-run legacy takeover.
Do NOT regenerate PRD unless explicitly required.

This is controlled continuation mode.

---

# STEP 1 — STATE REALIGNMENT

Before spawning any workers:

1. Check for `.github/memory-bank/RESUME_POINT.md`
   - If exists → use as primary resume anchor (skip broad re-analysis)
   - If missing → fall back to full state scan below
2. Read `.github/memory-bank/workflow-state.json`
3. Read `.github/memory-bank/activeContext.md`
4. Read `.github/memory-bank/progress.md`
5. Read `.github/memory-bank/decisionLog.md`
6. Read `.github/memory-bank/riskRegister.md`
7. Read `.github/memory-bank/SESSION_SUMMARY.md` (if exists)
8. Read `.github/memory-bank/SYSTEM_SNAPSHOT.json` (if exists)
9. Read active tickets and dependency graph
10. Run `python3 todo_visual.py --ready --json` for current READY ticket list
11. Detect:
    - In-progress tickets (IMPLEMENTING, QA_REVIEW, VALIDATION, DOCUMENTATION, CI_REVIEW)
    - Blocked tickets
    - Failed / escalated tickets
    - Tickets missing SDLC stages (incomplete post-execution chain)
    - Tickets missing scoped commit
    - Tickets missing validation (Validator never ran)
    - Tickets missing documentation update

Generate:
CONTINUATION_STATUS_REPORT.md

Archive prior session artifacts after reading:
- Delete or rename RESUME_POINT.md (consumed)
- Delete or rename SESSION_SUMMARY.md (consumed)
- Delete or rename SYSTEM_SNAPSHOT.json (consumed)

Do NOT code yet.

---

# STEP 2 — BACKLOG CLEANUP (PARALLEL)

If tickets skipped SDLC:

Spawn parallel workers to:

- Run QA on missed tickets
- Run Validator on missed tickets
- Run Documentation agent where missing
- Ensure commits exist and follow policy
- Fix minor validation issues

This must run in parallel with new development.

Maintain minimum 10 active workers (OCF — Operational Concurrency Floor).
If fewer primary (Class A) tickets exist, spawn Class B background audits:
- BG-SEC-AUDIT — Security scan (OWASP/STRIDE gaps)
- BG-ARCH-ALIGN — Architecture alignment (ADR conformance)
- BG-TECH-DEBT-SCAN — Tech debt detection (complexity hotspots)
- BG-PERFORMANCE-ANALYSIS — Performance review (hot paths)
- BG-QA-COVERAGE-CHECK — Test coverage gaps
- BG-DOC-COMPLETENESS — Documentation freshness audit

Class A tickets always preempt Class B. See governance/concurrency_floor.md.

---

# STEP 3 — SELECT NEXT EXECUTABLE TICKETS

From dependency graph:

1. Run `python3 todo_visual.py --ready` to identify READY tickets.
2. Exclude blocked tickets.
3. Exclude tickets under review (QA_REVIEW, VALIDATION, CI_REVIEW).
4. Sort by priority (P0 first).
5. Spawn one worker per ticket.
6. Spawn multiple workers of same role if multiple tickets exist.
7. Respect file conflict locks (no two workers on same file path).

No agent may take multiple tickets simultaneously.
One ticket → one worker → one lifecycle → one commit.

---

# STEP 4 — STRICT PER-TICKET SDLC

For each ticket:

READY
→ LOCKED
→ IMPLEMENTING
→ QA_REVIEW
→ VALIDATION
→ DOCUMENTATION
→ CI_REVIEW
→ COMMIT
→ DONE

No skipping stages.
No batching.
No one-shot execution.
No partial commits.

Each ticket must end with:

- Scoped commit
- Changelog update
- Memory update
- Observability update

---

# STEP 5 — CONTINUOUS PARALLELISM

ReaperOAK must:

- Continuously scan READY tickets
- Spawn workers immediately when safe
- Not wait for batches
- Not pause system-wide unless ARCHITECTURE_REWRITE_REQUIRED emitted
- Maintain minimum 10 active workers
- Use background agents if backlog low

Parallelism is ticket-level, not phase-level.

---

# STEP 6 — DRIFT CONTROL

If agent:

- Skips commit
- Skips validation
- Uses git add .
- Modifies undeclared files
- Skips memory update
- Attempts multi-ticket execution

Emit:
PROTOCOL_VIOLATION

Pause that ticket.
Generate mistake report.
Resume safely.

---

# STEP 7 — STRATEGIC EVOLUTION (NON-DISRUPTIVE)

If during execution:

- ARCHITECTURE_RISK detected
- SECURITY_RISK detected
- SCOPE_CONFLICT detected

Pause only affected tickets.
Invoke strategic layer.
Update roadmap version.
Regenerate affected tickets only.
Resume execution.

No global reset.

---

# STEP 8 — END STATE

Development continues until:

- All READY tickets processed
- No SDLC violations pending
- No validation backlog
- No security backlog
- CI clean

Then:

Generate DEVELOPMENT_STATUS_SUMMARY.md

When ending the session, invoke the stop protocol
(`.github/prompts/stop.prompt.md`) to produce RESUME_POINT.md
and preserve full state for the next continuation.

---

System must:

- Move forward
- Not re-diagnose entire repo
- Not rewrite stable components
- Not generate new roadmap unless required
- Not reduce worker concurrency
- Not allow one-shot coding

We are in disciplined continuation mode.

Maintain velocity.
Maintain governance.
Maintain parallelism.