<!-- GOVERNANCE_VERSION: 9.0.0 -->

# Memory Policy

> **Governance Version:** 9.0.0
> **Source:** Extracted from ReaperOAK.agent.md §24, part of §13
> **Scope:** Memory bank update rules, memory enforcement gate (INV-4),
> state management file schemas, and DRIFT-003 violation handling.

---

## 1. Memory Bank File Update Rules

Memory bank files are the persistent shared state for the multi-agent system.
All updates follow strict ownership and append-only rules.

### Ownership Matrix

| File | Owner | Write Access | Rules |
|------|-------|-------------|-------|
| `activeContext.md` | Shared | All agents (append) | Agents append timestamped entries only. ReaperOAK may archive. |
| `progress.md` | Shared | All agents (append) | Append milestone entries. Never delete. |
| `systemPatterns.md` | ReaperOAK | ReaperOAK only | Immutable to subagents. Append-only by ReaperOAK. |
| `productContext.md` | ReaperOAK | ReaperOAK only | Project vision. Updated only on scope changes. |
| `decisionLog.md` | ReaperOAK | ReaperOAK only | ADRs and trade-offs. Append-only. |
| `riskRegister.md` | Shared | ReaperOAK + Security | New threats appended. Never delete. |

### Update Rules

- **Append-only:** Never delete or modify existing entries in any memory file
- **Timestamped:** Every entry must include an ISO8601 timestamp
- **Attributed:** Every entry must include the writing agent's name
- **Focus shifts** → append to `activeContext.md`
- **Milestone completes** → append to `progress.md`
- **Significant trade-off** → append to `decisionLog.md` (ReaperOAK only)
- **New threat identified** → append to `riskRegister.md`

---

## 2. Memory Enforcement Gate (INV-4)

A ticket **CANNOT** transition from CI_REVIEW to COMMIT unless a memory bank
entry exists for that ticket. This gate enforces INV-4.

### 5 Required Fields per Memory Entry

| Field | Type | Description |
|-------|------|-------------|
| `ticket_id` | string | Ticket identifier (e.g., "EWPE-BE001") |
| `summary` | string | 1-2 sentence description of what was done |
| `artifacts` | string[] | List of files created or modified |
| `decisions` | string | Key architectural or implementation decisions made |
| `timestamp` | ISO8601 | When the entry was written |

### Memory Entry Format

Appended to `activeContext.md`:

```markdown
### [TICKET-ID] — Summary
- **Artifacts:** file1.ts, file2.ts
- **Decisions:** Chose X over Y because Z
- **Timestamp:** 2026-02-28T15:00:00Z
```

### DRIFT-003 Trigger

Missing or incomplete memory entries emit:

```yaml
event: PROTOCOL_VIOLATION
violation: DRIFT-003
invariant: INV-4
details: "No memory entry found for ticket {ticket_id}"
severity: MEDIUM
auto_repair: true
```

The ComplianceWorker generates the entry from ticket evidence when
`auto_repair: true`.

---

## 3. Gate Enforcement Pseudocode

```
function memoryGate(ticket):
  entry = search activeContext.md for ticket.id
  if entry is null:
    emit PROTOCOL_VIOLATION(DRIFT-003, ticket, "No memory entry found")
    spawn ComplianceWorker to generate entry from ticket evidence
    return BLOCK

  validate entry has all 5 required fields
  if any field missing:
    emit PROTOCOL_VIOLATION(DRIFT-003, ticket, "Incomplete memory entry: missing {fields}")
    return BLOCK

  return PASS
```

### Integration with Transition Table

The memory gate adds a guard condition to the CI_REVIEW → COMMIT transition:

| From | To | Trigger | Guard Condition |
|------|----|---------|----------------|
| CI_REVIEW | COMMIT | CI Reviewer PASS | Lint/types/complexity pass **AND** memoryGate(ticket) == PASS |

---

## 4. State Management Files

These files are updated at every state transition and form the operational
state layer of the system.

### workflow-state.json

Tracks ticket-level state:

```json
{
  "task_states": {
    "<TICKET_ID>": {
      "status": "READY | LOCKED | IMPLEMENTING | QA_REVIEW | VALIDATION | DOCUMENTATION | CI_REVIEW | COMMIT | DONE",
      "rework_count": 0,
      "blocker_reason": null,
      "locked_by": null,
      "worker_id": null,
      "locked_at": null,
      "last_transition": "2026-02-27T14:30:00Z"
    }
  }
}
```

**Update rules:**
- Set `status` to the new state at every transition
- Update `last_transition` timestamp
- Set `locked_by` and `worker_id` on LOCKED transition
- Clear lock fields on DONE or timeout transitions
- Increment `rework_count` on REWORK transitions

### artifacts-manifest.json

Records artifacts after each worker completes:
- Artifact path with SHA-256 hash
- `created_by` worker and ticket ID
- Build dependency graph (Frontend depends on UIDesigner specs, etc.)
- Track which ticket produced each artifact

### feedback-log.md

Append-only log of review feedback, rejection reasons, and rework context.
- Surface rejection entries to workers during rework
- Never delete existing entries
- Format: timestamped entries with agent attribution
