<!-- GOVERNANCE_VERSION: 9.1.0 -->

# Two-Commit Protocol (Distributed)

> **Governance Version:** 9.1.0
> **Scope:** Mandatory commit discipline for every agent in the distributed
> multi-machine multi-operator SDLC engine. Defines claim phase, work phase,
> safety rules, and failure recovery.

---

## 1. Protocol Overview

Every agent must commit and push **exactly twice** per ticket stage:

| Commit | Purpose | Contents | Timing |
|--------|---------|----------|--------|
| **Commit 1 — CLAIM** | Distributed lock acquisition | Ticket JSON move + metadata only | Before any work |
| **Commit 2 — WORK** | Deliver stage output | Code changes + summary file + ticket update | After work complete |

No agent may skip either commit. No agent may combine them.

---

## 2. Commit 1 — Claim Phase

### Pre-Conditions

1. `git pull --rebase` — MUST succeed before proceeding
2. Verify ticket exists in expected stage directory
3. Verify ticket is NOT claimed (or claim lease has expired)

### Actions

1. Update ticket JSON metadata:
   - `claimed_by`: agent worker ID
   - `machine_id`: hostname of executing machine
   - `operator`: human operator name (e.g., Owais, Sujal)
   - `lease_expiry`: current time + lease_duration_minutes
2. Append claim event to ticket `history` array
3. Save updated ticket JSON in its current state directory
4. Save updated master copy in `.github/tickets/`

### Commit Rules

```bash
# EXACT commit pattern — no deviations
git add .github/ticket-state/<STAGE>/<ticket-id>.json
git add .github/tickets/<ticket-id>.json
git commit -m "[<ticket-id>] CLAIM by <agent> on <machine-id> (<operator>)"
git push
```

### Forbidden During Claim Commit

- Code changes
- Summary file creation
- Any file outside ticket JSON paths
- `git add .` / `git add -A` / `git add --all`

### Push Failure

If `git push` fails after claim commit:

1. `git pull --rebase`
2. Check if another machine claimed first (conflict)
3. If conflict: **abort entirely** — do not proceed with work
4. If no conflict: retry push once
5. Second failure: abort and report

This is the **distributed lock mechanism**. Push success = lock acquired.

---

## 3. Commit 2 — Work Phase

### Pre-Conditions

1. Claim commit (Commit 1) successfully pushed
2. Agent has verified it holds the claim

### Actions

1. Execute agent task (implementation, QA, security review, etc.)
2. Modify only permitted files (within ticket `file_paths` scope)
3. Write summary file:

```
.github/agent-output/<AgentName>/<ticket-id>.md
```

4. Delete previous stage summary file (if exists):

```
.github/agent-output/<PreviousAgentName>/<ticket-id>.md
```

5. Update ticket JSON:
   - Clear claim fields (claimed_by, machine_id, operator, lease_expiry)
   - Update stage to next in SDLC flow
   - Append stage_completed event to history
6. Move ticket JSON to next stage directory

### Summary File Format

```markdown
# <ticket-id> — <Agent Name> Stage Summary

**Agent:** <agent-name>
**Machine:** <machine-id>
**Operator:** <operator>
**Timestamp:** <ISO8601>
**Stage:** <current-stage> → <next-stage>

## What Was Done
- ...

## Files Modified
- path/to/file1.ts
- path/to/file2.ts

## Tests Executed
- Test suite: result
- (or "N/A — not applicable for this stage")

## Issues Found
- (or "None")

## Notes for Next Stage
- ...
```

### Commit Rules

```bash
# EXACT commit pattern — no deviations
git add <all-modified-code-files>
git add .github/agent-output/<AgentName>/<ticket-id>.md
git add .github/ticket-state/<NextStage>/<ticket-id>.json
git add .github/tickets/<ticket-id>.json
# Delete old state file and previous summary
git rm .github/ticket-state/<OldStage>/<ticket-id>.json
git rm .github/agent-output/<PreviousAgent>/<ticket-id>.md  # if exists
git commit -m "[<ticket-id>] <STAGE> complete by <agent> on <machine-id>"
git push
```

### Forbidden During Work Commit

- `git add .` / `git add -A` / `git add --all`
- Files outside ticket scope
- Modifying other ticket JSON files
- Modifying summaries in other agent directories

---

## 4. Summary Handoff Chain

Context flows **strictly via filesystem**:

```
Agent A writes:  .github/agent-output/AgentA/<ticket-id>.md
Agent B reads:   .github/agent-output/AgentA/<ticket-id>.md
Agent B deletes: .github/agent-output/AgentA/<ticket-id>.md
Agent B writes:  .github/agent-output/AgentB/<ticket-id>.md
```

Rules:
- Each agent writes exactly **one** summary file per ticket
- Each agent reads **only** the previous stage's summary
- Each agent deletes the previous stage's summary after processing
- ReaperOAK does NOT inject context — context is file-derived only

---

## 5. Parallel Multi-Machine Safety

### Before Claim

```
git pull --rebase
python .github/tickets.py --sync   # optional but recommended
```

### Claim Conflict Resolution

- If `git push` fails with conflict on ticket JSON:
  - Another machine claimed first
  - Current machine MUST abort
  - Do NOT force push
  - Skip this ticket, try another

### Lease Expiry

- Default lease: 30 minutes
- If `lease_expiry < current_time`: ticket is reclaimable
- Any machine may reclaim an expired-lease ticket
- Run `python .github/tickets.py --release-expired` to clear stale claims

### Never

- Process a ticket you haven't successfully pushed a claim for
- Modify tickets in other stage directories
- Hold claims on multiple tickets simultaneously (per agent instance)

---

## 6. Stage Directory Rules

| Stage Dir | Processing Agent | Can Claim From |
|-----------|------------------|----------------|
| READY | (dispatch target) | Any agent per SDLC flow |
| ARCHITECT | Architect | READY |
| RESEARCH | Research | READY |
| BACKEND | Backend | READY or ARCHITECT |
| FRONTEND | Frontend or UIDesigner | READY or BACKEND |
| QA | QA | Implementation stage |
| SECURITY | Security | QA |
| CI | CIReviewer | SECURITY |
| DOCS | Documentation | CI |
| VALIDATION | Validator | DOCS |
| DONE | (terminal) | VALIDATION |

---

## 7. DRIFT Events

| Violation | DRIFT Code | Description |
|-----------|------------|-------------|
| Skipped claim commit | DRIFT-010 | Agent performed work without claim |
| Unscoped staging | DRIFT-002 | Used git add . or wildcard |
| Wrong stage claim | DRIFT-011 | Claimed ticket from wrong directory |
| Multi-ticket claim | DRIFT-012 | Agent holds claims on multiple tickets |
| Cross-stage modify | DRIFT-013 | Modified ticket in another stage dir |
| Missing summary | DRIFT-014 | No summary file written after work |
| Summary in wrong dir | DRIFT-015 | Summary written to wrong agent dir |

---

## 8. Failure Recovery

### Agent Crash After Claim (Before Work)

- Ticket remains in current stage with claim metadata
- Lease expiry protects against indefinite lock
- Another machine reclaims after lease expires

### Agent Crash During Work

- Partial work is uncommitted (lost)
- Claim remains until lease expires
- After lease expiry: ticket is reclaimed, work restarts

### Push Conflict on Work Commit

- Should be rare (claim provides lock)
- If it happens: investigate — may indicate protocol violation
- Emit `PROTOCOL_VIOLATION` event

---

## 9. Enforcement

This protocol is **mandatory** for all agents. Violations trigger:

1. `PROTOCOL_VIOLATION` event emission
2. Ticket returned to previous state
3. Agent worker terminated
4. ComplianceWorker spawned for repair

No exceptions. No overrides without human approval.

---

End of Two-Commit Protocol.
