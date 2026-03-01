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

1. Read memory-bank/workflow-state.json
2. Read active tickets
3. Read dependency graph
4. Read progress.md
5. Read decisionLog.md
6. Detect:
   - In-progress tickets
   - Blocked tickets
   - Failed tickets
   - Tickets missing SDLC loop
   - Tickets missing commit
   - Tickets missing validation
   - Tickets missing documentation

Generate:
CONTINUATION_STATUS_REPORT.md

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

Maintain minimum 10 active workers.
If fewer primary tickets exist, spawn background audits:
- Security scan
- Architecture alignment
- Tech debt detection
- Performance review

---

# STEP 3 — SELECT NEXT EXECUTABLE TICKETS

From dependency graph:

1. Identify READY tickets.
2. Exclude deprecated.
3. Exclude blocked.
4. Exclude tickets under review.
5. Sort by priority.
6. Spawn one worker per ticket.
7. Spawn multiple workers of same role if multiple tickets exist.
8. Respect file conflict locks.

No agent may take multiple tickets simultaneously.

---

# STEP 4 — STRICT PER-TICKET SDLC

For each ticket:

READY
→ LOCKED
→ IMPLEMENTATION
→ QA
→ VALIDATOR
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