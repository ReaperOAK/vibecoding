# Event Protocol

> **GOVERNANCE_VERSION: 9.0.0**
> **Authority:** `.github/instructions/core_governance.instructions.md`
> **Source:** ReaperOAK §13 (event types + routing), §20 (PROTOCOL_VIOLATION)
> **Scope:** All event types, routing rules, payload format, blocking protocol

---

## 1. Complete Event Types Table (24 Events)

### Core Lifecycle Events

| # | Event Type | When Emitted | Emitter | Payload |
|---|-----------|-------------|---------|---------|
| 1 | `TASK_STARTED` | Agent begins work on assigned ticket | Implementing worker | ticket_id, worker_id, timestamp |
| 2 | `TASK_COMPLETED` | Agent finishes with evidence | Implementing worker | ticket_id, evidence, artifacts, confidence, timestamp |
| 3 | `TASK_FAILED` | Agent cannot complete | Implementing worker | ticket_id, error_details, suggested_action, timestamp |
| 4 | `NEEDS_INPUT_FROM` | Agent needs output from another agent | Any worker | ticket_id, target_agent, question, context |
| 5 | `BLOCKED_BY` | Agent blocked by external dependency | Any worker | ticket_id, blocker_description, blocker_type |
| 6 | `PROGRESS_UPDATE` | Periodic status during long tasks | Any worker | ticket_id, percent_complete, current_step, timestamp |

### Worker Pool Events

| # | Event Type | When Emitted | Emitter | Payload |
|---|-----------|-------------|---------|---------|
| 7 | `WORKER_FREE` | Worker completes ticket and is released | Worker pool | worker_id, pool_role, timestamp |
| 8 | `WORKER_ASSIGNED` | Worker assigned to ticket | Scheduler | worker_id, pool_role, ticket_id, timestamp |
| 9 | `WORKER_SPAWNED` | New worker dynamically created | Scheduler | worker_id, pool_role, ticket_id, timestamp |
| 10 | `WORKER_TERMINATED` | Worker removed from pool | Scheduler | worker_id, pool_role, reason, timestamp |
| 11 | `POOL_SCALED_UP` | Elastic pool expanded (unbounded) | Scheduler | pool_role, old_count, new_count, trigger |
| 12 | `POOL_SCALED_DOWN` | Elastic pool contracted | Scheduler | pool_role, old_count, new_count, reason |

### Scheduling & Conflict Events

| # | Event Type | When Emitted | Emitter | Payload |
|---|-----------|-------------|---------|---------|
| 13 | `CONFLICT_DETECTED` | File/resource conflict between tickets | Scheduler | ticket_id, conflict_type, blocking_ticket |
| 14 | `REWORK_TRIGGERED` | QA/Validator/CI rejects ticket | QA/Validator/CI | ticket_id, reason, rework_count |
| 15 | `STALL_WARNING` | Worker unresponsive > 45 min | Scheduler | ticket_id, worker_id, duration |
| 16 | `LOCK_EXPIRED` | Lock held > 30 min | Scheduler | ticket_id, worker_id |

### Strategic Events

| # | Event Type | When Emitted | Emitter | Payload |
|---|-----------|-------------|---------|---------|
| 17 | `SDR_PROPOSED` | Strategic agent proposes strategy change | Strategic agent | sdr_id, proposer, impact_assessment |
| 18 | `SDR_APPROVED` | ReaperOAK approves SDR | ReaperOAK | sdr_id, roadmap_version |

### OIP / Governance Events

| # | Event Type | When Emitted | Emitter | Payload |
|---|-----------|-------------|---------|---------|
| 19 | `PROTOCOL_VIOLATION` | Drift detected during state transition | Drift Detector | ticket_id, violation_id, invariant_id, severity, auto_repair |
| 20 | `REPAIR_COMPLETED` | ComplianceWorker finishes repair | ComplianceWorker | ticket_id, violation_id, repair_action, status |
| 21 | `REPAIR_FAILED` | ComplianceWorker cannot repair | ComplianceWorker | ticket_id, violation_id, failure_reason |

### New Governance Integrity Events

| # | Event Type | When Emitted | Emitter | Payload |
|---|-----------|-------------|---------|---------|
| 22 | `REQUEST_RESEARCH` | Agent needs research before proceeding | Any worker | ticket_id, research_question |
| 23 | `INSTRUCTION_MISALIGNMENT` | Governance file version ≠ system GOVERNANCE_VERSION | Boot sequence / Health Sweep | file_path, declared_version, expected_version, timestamp |
| 24 | `GOVERNANCE_DRIFT` | Governance integrity check detects duplication, oversized files, or misalignment | Health Sweep | drift_type, affected_files, details, timestamp |

---

## 2. Event Routing Rules (20 Routes)

When ReaperOAK receives an event, it routes as follows:

| # | Event | Routing Action |
|---|-------|---------------|
| 1 | `TASK_COMPLETED` | Advance ticket to QA_REVIEW, assign QA worker |
| 2 | `TASK_FAILED` | Move ticket to REWORK, check rework_count |
| 3 | `WORKER_FREE` | Trigger scheduling loop for next READY ticket |
| 4 | `NEEDS_INPUT_FROM` | Pause ticket, invoke requested agent, resume on response |
| 5 | `BLOCKED_BY` | Mark ticket as blocked, wait for blocker resolution |
| 6 | `SDR_PROPOSED` | Evaluate SDR, request human approval if scope expansion |
| 7 | `CONFLICT_DETECTED` | Hold conflicting ticket in READY until conflict resolves |
| 8 | `REWORK_TRIGGERED` | Route ticket to REWORK, include rejection report |
| 9 | `STALL_WARNING` | Query worker status, escalate if unresponsive |
| 10 | `LOCK_EXPIRED` | Release lock, return ticket to READY, free worker |
| 11 | `WORKER_SPAWNED` | Log spawn, update pool registry |
| 12 | `WORKER_TERMINATED` | Release resources, check if rework needed |
| 13 | `POOL_SCALED_UP` | Log scaling event, update pool capacity |
| 14 | `POOL_SCALED_DOWN` | Log scaling event, verify idle workers terminated |
| 15 | `PROTOCOL_VIOLATION` | Block ticket transition, spawn ComplianceWorker if auto-repairable |
| 16 | `REPAIR_COMPLETED` | Verify repair, unblock ticket, advance lifecycle |
| 17 | `REPAIR_FAILED` | Flag for human attention, escalate |
| 18 | `REQUEST_RESEARCH` | Pause ticket, invoke Research Analyst, resume on findings |
| 19 | `INSTRUCTION_MISALIGNMENT` | **Halt agent immediately**, re-sync governance version, re-inject updated governance files before resuming |
| 20 | `GOVERNANCE_DRIFT` | **Pause new scheduling**, run auto-correct (split oversized files, deduplicate, realign versions), resume after correction |

---

## 3. PROTOCOL_VIOLATION Event Schema

```yaml
event: PROTOCOL_VIOLATION
ticket: "{ticket_id}"
worker: "{worker_id}"
violation: "{DRIFT-NNN}"
invariant: "{INV-N}"
details: "{description of the violation}"
timestamp: "{ISO8601}"
severity: "CRITICAL | HIGH | MEDIUM"
auto_repair: true | false
```

### Severity Rules

| Severity | Criteria | Response |
|----------|----------|----------|
| CRITICAL | Data integrity at risk, security boundary crossed | Block all transitions, alert human |
| HIGH | Lifecycle violation, scope drift, missing chain step | Block affected ticket, auto-repair if possible |
| MEDIUM | Missing documentation, stale memory entry | Block affected ticket, auto-repair via ComplianceWorker |

---

## 4. No Direct Agent Communication

Workers must NOT call each other directly. ALL inter-agent communication is
routed through ReaperOAK. This ensures:

- Single point of coordination and audit trail
- No circular dependencies between workers
- ReaperOAK maintains full visibility of system state
- Every interaction is logged for observability

Violation of this rule triggers `PROTOCOL_VIOLATION` with severity HIGH.

---

## 5. Blocking Event Handling Protocol

When ReaperOAK receives a blocking event from a worker:

1. **Pause** current ticket (state remains IMPLEMENTING — worker is waiting)
2. **Invoke** the requested agent with context from the blocking ticket
3. **Wait** for resolution from the invoked agent
4. **Pass** resolution artifacts back to the original worker
5. **Resume** original ticket execution

Blocking events: `NEEDS_INPUT_FROM`, `BLOCKED_BY`, `REQUEST_RESEARCH`,
`REQUIRES_UI_DESIGN`, `ESCALATE_TO_PM`, `REQUIRES_STRATEGIC_INPUT`.

---

## 6. Event Payload Format

Emit events as structured markdown in agent output:

```markdown
**Event:** {EVENT_TYPE}
**Ticket:** {TICKET-ID}
**Agent:** {agent_name}
**Worker:** {worker_id}
**Timestamp:** {ISO8601}
**Details:** {description of what happened}
**Evidence:** {artifact paths, test results, confidence level}
```

### Required Fields by Event Type

| Event Type | Required Fields |
|-----------|----------------|
| `TASK_COMPLETED` | Event, Ticket, Agent, Worker, Timestamp, Details, Evidence (artifacts + confidence) |
| `TASK_FAILED` | Event, Ticket, Agent, Worker, Timestamp, Details (error + suggested_action) |
| `TASK_STARTED` | Event, Ticket, Agent, Worker, Timestamp |
| `PROTOCOL_VIOLATION` | Full YAML schema (§3) |
| `INSTRUCTION_MISALIGNMENT` | Agent, declared_version, expected_version, Timestamp |
| `GOVERNANCE_DRIFT` | drift_type, affected_files, details, Timestamp |

---

## 7. Emission Rules

1. Every agent MUST emit `TASK_STARTED` at the beginning and either
   `TASK_COMPLETED` or `TASK_FAILED` at the end of every ticket execution
2. Blocking events pause the current ticket — ReaperOAK handles routing
3. `PROGRESS_UPDATE` should be emitted for tasks with effort > 30 min
4. `TASK_COMPLETED` MUST include evidence — events without evidence are
   rejected (triggers DRIFT-007)
5. `INSTRUCTION_MISALIGNMENT` is emitted at boot if version mismatch detected
6. `GOVERNANCE_DRIFT` is emitted by the Health Sweep on integrity violations
