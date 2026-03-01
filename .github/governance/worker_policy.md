<!-- GOVERNANCE_VERSION: 9.0.0 -->

# Worker Policy

> **Governance Version:** 9.0.0
> **Source:** Extracted from ReaperOAK.agent.md §7, §15 (with unbounded scaling)
> **Scope:** Elastic worker pool model, worker lifecycle, one-ticket-one-worker
> rule, lock semantics, anti-one-shot guardrails, and auto-scaling algorithm.
>
> **CRITICAL:** Worker pools are **UNBOUNDED**. There is no maxSize or minSize
> field. Scaling is governed only by READY ticket count, dependency constraints,
> resource conflicts, and system compute capacity.

---

## 1. Elastic Pool Model — UNBOUNDED

Each agent role is backed by an **elastic pool** of workers. Workers are
spawned dynamically when tickets enter READY and terminated after completion
or idle timeout. Pools auto-scale based on ticket backlog with **no upper
bound**. There are no pre-allocated worker slots — every worker is created
on demand with a unique dynamic ID.

### Elastic Pool Registry Schema

```yaml
worker_pool_registry:
  # Default scaling policy (applies to all standard pools):
  #   scaleUpTrigger: "READY_tickets > currentActive"
  #   scaleDownTrigger: "idle_duration > 10min"
  #   cooldownPeriod: "2min"
  pools:
    # --- Standard pools (default scaling policy) ---
    - { role: Backend,                  currentActive: 0, activeWorkers: [] }
    - { role: Frontend Engineer,        currentActive: 0, activeWorkers: [] }
    - { role: QA Engineer,              currentActive: 0, activeWorkers: [] }
    - { role: Security Engineer,        currentActive: 0, activeWorkers: [] }
    - { role: DevOps Engineer,          currentActive: 0, activeWorkers: [] }
    - { role: Documentation Specialist, currentActive: 0, activeWorkers: [] }
    - { role: Validator,                currentActive: 0, activeWorkers: [] }
    - { role: CI Reviewer,              currentActive: 0, activeWorkers: [] }
    - { role: Research Analyst,         currentActive: 0, activeWorkers: [] }
    - { role: Product Manager,          currentActive: 0, activeWorkers: [] }
    - { role: Architect,                currentActive: 0, activeWorkers: [] }
    - { role: UIDesigner,               currentActive: 0, activeWorkers: [] }
    # --- Compliance pool (violation-aware scaling) ---
    - role: ComplianceWorker
      currentActive: 0
      scalingPolicy:
        scaleUpTrigger: "violation_backlog > currentActive"
        scaleDownTrigger: "idle_duration > 5min"
        cooldownPeriod: "1min"
      activeWorkers: []
```

---

## 2. Worker Instance Schema

Each dynamically spawned worker is tracked with this schema:

```yaml
worker_instance:
  id: "BackendWorker-a1b2c3"     # Dynamic, unique per spawn
  role: Backend                   # Agent role from pool
  agentName: "Backend"            # EXACT runSubagent name
  ticketId: "EWPE-BE001"         # Assigned ticket (exactly ONE)
  spawnedAt: "2026-02-28T14:30:00Z"
  status: active                  # spawned | active | completed | failed | terminated
  terminatedAt: null
```

Worker IDs use the format `{Role}Worker-{shortUuid}` — e.g.,
`BackendWorker-a1b2c3`, `FrontendWorker-d4e5f6`, `QAWorker-g7h8i9`.
IDs are generated at spawn time and are globally unique.

---

## 3. Worker Lifecycle

Workers progress through 5 states:

1. **spawned** — `runSubagent` called, worker instance created in pool registry
2. **active** — Worker is executing its assigned ticket
3. **completed** — Worker finished successfully, emitted TASK_COMPLETED
4. **failed** — Worker reported failure, emitted TASK_FAILED
5. **terminated** — Worker violated scope (multi-ticket) or timed out, forcibly killed

---

## 4. One-Ticket-One-Worker Rule (CRITICAL)

**A worker instance processes EXACTLY ONE ticket.** It has no memory
of previous tickets. It terminates after ticket completion. It NEVER picks up
another ticket. Each `runSubagent` call creates a fresh, stateless worker
instance dedicated to a single ticket.

- One worker → one ticket → one lifecycle → one commit → termination
- No worker reuse across tickets
- No shared state between worker instances of the same role
- If a ticket needs rework, a NEW worker is spawned — the original is gone

---

## 5. Lock Semantics

When a worker is assigned to a ticket:

```json
{
  "ticketId": "EWPE-BE001",
  "workerId": "BackendWorker-a1b2c3",
  "poolRole": "Backend",
  "lockedAt": "2026-02-28T14:30:00Z",
  "expiresAt": "2026-02-28T15:00:00Z",
  "status": "active"
}
```

Lock is acquired at READY → LOCKED, held through the lifecycle, released
at COMMIT → DONE or on timeout. Lock timeout: **30 minutes**.

### Lock Timeout & Stall Detection

| Signal | Threshold | Action |
|--------|-----------|--------|
| IMPLEMENTING without progress | > 45 min without event | Emit STALL_WARNING, query worker |
| Dependency chain blocked | 3+ tickets in chain all blocked | Escalate to user |
| IMPLEMENTING ↔ REWORK toggling | ≥ 3 times for same ticket | Ticket returns to READY, user notified |

### Failure Rollback Rules

| Failure Mode | State Transition | Recovery Action |
|--------------|-----------------|----------------|
| Worker reports failure | IMPLEMENTING → REWORK | Spawn new worker with findings; rework_count++ |
| QA/Validator rejects | QA_REVIEW → REWORK | Spawn new worker with rejection report; rework_count++ |
| CI Reviewer rejects | CI_REVIEW → REWORK | Spawn new worker with CI findings; rework_count++ |
| Lock expires (30 min) | LOCKED → READY | Worker terminated; ticket eligible for reassignment |
| Rework exhausted (> 3) | REWORK → READY | User notified for override or cancellation |

---

## 6. Anti-One-Shot Guardrails

Hard rules to prevent workers from producing low-quality single-pass output
or exceeding ticket scope.

### Scope Enforcement

- Worker must ONLY respond to its assigned ticket ID
- If worker output references unrelated tickets → REJECT
- If implementation exceeds ticket scope (modifies files not in the ticket's
  `file_paths`) → REJECT at QA_REVIEW
- If worker attempts to implement multiple tickets' work in one response →
  force stop and re-delegate

### Worker Termination on Multi-Ticket Violation (HARD KILL)

If a worker instance references, modifies, or attempts work on ANY ticket
other than its assigned ticket ID:

1. Worker is IMMEDIATELY TERMINATED (status → terminated)
2. Ticket moves to REWORK (rework_count++)
3. WORKER_TERMINATED event emitted with reason: "multi-ticket violation"
4. Validator independently verifies single-ticket scope at QA_REVIEW
5. If worker output contains multiple ticket IDs → Validator REJECTS

This is a **HARD KILL** — no warning, no retry within the same worker instance.
A fresh worker is spawned for the rework.

### Pre-Chain Scope Check

Before entering the post-execution chain, ReaperOAK verifies:

1. Modified files match the ticket's declared `file_paths`
2. No unrelated changes are included in the diff
3. Worker's response references only the assigned ticket ID
4. Implementation addresses all acceptance criteria from the ticket
5. No references to other ticket IDs appear in the worker's output
   (grep for `[A-Z]+-[A-Z]+\d{3}` patterns excluding the assigned ticket ID)

If ANY check fails → REJECT and re-delegate with specific findings.

### Iteration Requirement (4 Passes)

No single-pass implementations. Workers must demonstrate verification:

1. **First pass:** draft implementation
2. **Self-review:** check against acceptance criteria
3. **Fix pass:** address gaps found in self-review
4. **Final check:** confirm all criteria met

ReaperOAK verifies that worker output includes self-reflection evidence
before accepting TASK_COMPLETED events.

### Evidence Requirement for TASK_COMPLETED

Every TASK_COMPLETED event must include:
- Artifact paths (files created or modified)
- Test results (if applicable)
- Confidence level (HIGH/MEDIUM/LOW)
- Evidence that acceptance criteria are met

Missing evidence triggers DRIFT-007 and returns the ticket to IMPLEMENTING.

---

## 7. Auto-Scaling Algorithm — UNBOUNDED

```
function autoScale(pool):
  ready = countReadyTickets(pool.role)
  active = pool.currentActive

  # Scale UP — no cap, no delay
  if ready > active:
    scaleUp = ready - active
    log("POOL_SCALED_UP", pool.role, active, active + scaleUp)

  # Scale DOWN (idle workers only)
  for worker in pool.activeWorkers:
    if worker.status == idle and worker.idleDuration > 10min:
      terminate(worker)
      log("POOL_SCALED_DOWN", pool.role, active, active - 1)
```

**Key properties:**
- No upper bound on worker count — scaling is purely demand-driven
- `scaleUp = ready - active` — spawn exactly as many workers as there are
  unassigned READY tickets
- Scale-down is driven by idle timeout only (10 min default)
- ComplianceWorker pools use `violation_backlog > currentActive` as their
  scale trigger with a tighter 5-min idle timeout
