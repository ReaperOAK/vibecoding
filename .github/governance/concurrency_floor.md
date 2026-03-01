<!-- GOVERNANCE_VERSION: 9.1.0 -->

# Operational Concurrency Floor (OCF)

> **Governance Version:** 9.1.0
> **Authority:** `.github/instructions/core_governance.instructions.md`
> **Source:** ARCHITECTURE.instructions.md §34
> **Scope:** Minimum active worker enforcement, Class A/B work taxonomy,
> background ticket spawning, preemption rules, throttle safeguards,
> anti-recursion guards.

---

## 1. Constants

```
MIN_ACTIVE_WORKERS = 10
```

ReaperOAK enforces a **minimum of 10 active workers** at all times. When
fewer than 10 primary (Class A) tickets are in-flight, the scheduler spawns
background (Class B) workers to fill the remaining capacity.

---

## 2. Work Classes

| Class | Priority | Source | Preemptible |
|-------|----------|--------|-------------|
| **A** — Primary | High | Ticket backlog (L3 tasks) | No |
| **B** — Background | Low | Scheduler-generated | Yes — paused when Class A arrives |

Class B workers are ephemeral, follow the standard 9-state lifecycle, and
their commits are labeled `[BG-<TYPE>]`. They operate under stricter
resource constraints and **read-only** scope unless generating proposals.

---

## 3. Background Ticket Taxonomy (10 Types)

| Type | Agent | Scope |
|------|-------|-------|
| `BG-SEC-AUDIT` | Security Engineer | Scan codebase for OWASP/STRIDE gaps |
| `BG-ARCH-ALIGN` | Architect | Verify implementation matches ADRs |
| `BG-TECH-DEBT-SCAN` | Backend / Frontend | Identify code smells, complexity hotspots |
| `BG-QA-COVERAGE-CHECK` | QA Engineer | Find untested paths, coverage gaps |
| `BG-DOC-COMPLETENESS` | Documentation Specialist | Audit doc freshness, missing sections |
| `BG-MEMORY-COMPACTION` | Documentation Specialist | Compact stale memory bank entries |
| `BG-GOVERNANCE-DRIFT-CHECK` | Validator | Cross-check governance file consistency |
| `BG-FAILED-TICKET-ANALYSIS` | QA Engineer | Analyze REWORK/ESCALATED tickets for patterns |
| `BG-REFACTOR-SUGGESTION` | Architect | Propose scoped refactors (read-only analysis) |
| `BG-PERFORMANCE-ANALYSIS` | Backend / Frontend | Profile hot paths, identify bottlenecks |

Background ticket selection is **round-robin** across the 10 types, biased
toward types with the longest time since last execution.

---

## 4. Concurrency Floor Algorithm

Runs inside the scheduling loop AFTER the Class A assignment phase:

```
function enforceConcurrencyFloor():
  total_active = count_all_active_workers()    # Class A + Class B
  if total_active >= MIN_ACTIVE_WORKERS:
    return                                      # Floor satisfied

  deficit = MIN_ACTIVE_WORKERS - total_active
  bg_tickets = selectBackgroundTickets(deficit)  # Round-robin from §3

  for bg in bg_tickets:
    if no_conflict_with_primary(bg):
      worker = spawn_worker(bg.role)
      assign(worker, bg)
      emit(BG_WORKER_SPAWNED, worker, bg)
    else:
      skip(bg)                                  # Never block Class A
```

### Selection Priority

1. Types with longest time since last execution go first
2. Never spawn duplicate type if one is already active
3. If fewer than `deficit` conflict-free BG tickets available, accept
   partial fill — do NOT force-spawn conflicting workers

### Task Discovery

Before spawning Class B workers, the scheduler queries the actionable task
pool via `python3 todo_visual.py --ready --json`. This provides an
authoritative, post-resolution view of all non-blocked tasks, ensuring
background workers are only spawned for genuinely assignable work.

---

## 5. Preemption Rules

1. Class A tickets **ALWAYS** take priority over Class B
2. When new Class A ticket arrives and all workers are busy:
   pause lowest-priority Class B worker → reassign capacity to Class A
3. Paused Class B tickets return to BG-READY queue (resumable)
4. Class B workers **NEVER** block Class A file paths
5. Class B workers operate **read-only** unless generating scoped proposals
6. If Class B detects conflict with in-flight Class A → self-pause immediately

### Preemption Protocol

```
function preemptForClassA(classA_ticket):
  bg_workers = get_active_bg_workers(sorted_by=priority_asc)
  if bg_workers is empty:
    return false                                # No BG to preempt
  victim = bg_workers[0]                        # Lowest priority
  emit(BG_WORKER_PREEMPTED, victim, classA_ticket)
  pause(victim)                                 # Save partial state
  return true
```

---

## 6. Context Injection (Class B)

Background workers receive **minimal** context to avoid token bloat:

| Item | Included |
|------|----------|
| `governance/lifecycle.md` | Yes |
| `governance/worker_policy.md` | Yes |
| Role-specific agent chunks (2 files) | Yes |
| Scoped task description | Yes (< 500 tokens) |
| Targeted file subset | Yes (only files being analyzed) |
| Full repository context | **NO** |
| Extra governance files | **NO** |
| Full memory bank | **NO** |

**Token budget for Class B workers:** ≤ 20K tokens total injection
(approximately half of the standard ~38K Class A budget).

---

## 7. Commit Policy (Class B)

- Commits labeled `[BG-<TYPE>] description`
- Small, scoped — never mass-refactor
- Explicit `git add` only (scoped git rules apply, INV-3)
- Blocked if Class A is modifying the same files
- CHANGELOG entry format: `- [BG-<TYPE>] <summary>`

### Class B Commit Validation

```
function validateBGCommit(bg_ticket, staged_files):
  classA_files = union(worker.touched_files for worker in classA_workers)
  if intersection(staged_files, classA_files) is not empty:
    return BLOCKED                              # Wait for Class A
  if not bg_ticket.commit_msg.startsWith("[BG-"):
    return DRIFT-002                            # Wrong format
  return PASS
```

---

## 8. Throttle Safeguards

| Condition | Action |
|-----------|--------|
| Primary backlog > 20 tickets | Suspend all Class B spawning |
| Token usage > 80% budget | Reduce BG spawn rate by 50% |
| Token usage > 95% budget | Suspend all Class B |
| Class A rework rate > 30% | Suspend Class B, focus on primary quality |

When throttle is active, `enforceConcurrencyFloor()` is skipped entirely.
Throttle state is logged in `workflow-state.json` under `ocf_throttle`.

---

## 9. Anti-Recursion Guard

- Class B workers **CANNOT** spawn other Class B workers
- Class B workers **CANNOT** modify governance, instruction, or agent files
- Class B output is always a **report** or **improvement ticket proposal**
- Only ReaperOAK may promote a BG finding to a Class A ticket
- BG workers cannot create BG tickets or modify OCF configuration

### Forbidden Actions (Class B)

| Action | Result |
|--------|--------|
| Spawn a Class B worker | HARD KILL (INV-8 violation) |
| Modify `.github/governance/*` | HARD KILL |
| Modify `.github/agents/*` | HARD KILL |
| Modify `.github/instructions/*` | HARD KILL |
| Create a new BG ticket definition | HARD KILL |
| Self-promote finding to Class A | Report only — ReaperOAK decides |

---

## 10. Continuous Improvement Loop

When a Class B worker finds an actionable issue:

1. Create structured improvement ticket (typed, scoped, estimated)
2. Insert into roadmap as Class A ticket at appropriate priority
3. Do **NOT** attempt autonomous rewrite — report only
4. No recursive self-modification — BG workers cannot create BG tickets

### Report Format

```yaml
bg_finding:
  type: "<BG-TYPE>"
  worker_id: "<worker_id>"
  timestamp: "<ISO8601>"
  severity: "LOW | MEDIUM | HIGH"
  summary: "<one-line description>"
  details: "<detailed finding>"
  affected_files: ["<file paths>"]
  recommended_action: "<specific suggestion>"
  estimated_effort: "<hours>"
  proposed_ticket_priority: "P0 | P1 | P2 | P3"
```

---

## 11. Example Scenario

```
State: 1 Class A ticket in-flight (Backend), 9 idle slots
→ OCF spawns 9 Class B workers:
  BG-SEC-AUDIT, BG-ARCH-ALIGN, BG-TECH-DEBT-SCAN,
  BG-QA-COVERAGE-CHECK, BG-DOC-COMPLETENESS,
  BG-MEMORY-COMPACTION, BG-GOVERNANCE-DRIFT-CHECK,
  BG-FAILED-TICKET-ANALYSIS, BG-REFACTOR-SUGGESTION

Then: 3 new Class A tickets arrive (Frontend, QA, DevOps)
→ 3 lowest-priority BG workers paused → 3 Class A workers spawned
→ Active: 4 Class A + 6 Class B = 10 total

Then: 2 more Class A tickets arrive
→ 2 more BG workers paused → 2 Class A workers spawned
→ Active: 6 Class A + 4 Class B = 10 total
```
