---
id: loop-detection-rules
version: "1.0"
locked_by: ReaperOAK
---

# Loop Detection & Token Budget Rules

## Loop Detection

### Signal: Repeated Tool Calls
- DETECT: Same tool called with identical arguments ≥ 3 times within 10 steps
- ACTION: Halt agent, log loop signature, set task status to STALLED
- ESCALATE: Notify ReaperOAK with loop evidence (tool name, args, step numbers)

### Signal: Identical Output Cycles
- DETECT: Agent produces functionally identical output ≥ 2 consecutive times
- ACTION: Halt agent, set task status to STALLED
- ESCALATE: Notify ReaperOAK for re-scoping or alternative approach

### Signal: Retry Exhaustion
- DETECT: Task retried 3 times with same failure class
- ACTION: Set task status to BLOCKED, stop retries
- ESCALATE: Notify ReaperOAK → human escalation if unresolvable

### Signal: Oscillating State
- DETECT: Task status oscillates between two states ≥ 3 times (e.g. IN_PROGRESS → REVIEW → REJECTED → IN_PROGRESS)
- ACTION: Halt, force BLOCKED status
- ESCALATE: Root cause analysis required before retry

## Token Budget Enforcement

### Per-Task Budgets
- Each delegation packet declares `max_token_budget`
- Agents MUST track cumulative token usage against budget

### Threshold Actions

| Budget Used | Action |
|-------------|--------|
| 0-69% | Normal operation |
| 70-79% | WARNING: Agent warned, must prioritize completion |
| 80-89% | RESTRICT: Essential operations only — no exploration |
| 90-94% | URGENT: Wrap up, deliver partial results if needed |
| 95-100% | HARD STOP: Force completion, return partial output |
| >100% | VIOLATION: Task killed, escalate to ReaperOAK |

### Session-Level Budgets
- Total session budget tracked across all agents
- ReaperOAK monitors aggregate burn rate
- If session budget exceeds 80%, no new delegations permitted
- At 95%, all agents must wrap up current tasks


## Circuit Breaker: STOP_ALL

- File: `.github/guardian/STOP_ALL`
- Format: `STATUS TIMESTAMP` (first line)
- Values: `CLEAR` (normal), `STOP` (halt all), `PAUSE` (finish current, no new)
- All agents MUST check STOP_ALL before:
  - Starting a new task
  - Making write operations
  - Delegating to subagents
- Only ReaperOAK or human may set/clear STOP_ALL

## Human Notification

### Notification Triggers
- Any agent enters STALLED state
- Token budget exceeds 80% for any task
- Session budget exceeds 70%
- Loop detected
- 3 consecutive task failures
- Guardian STOP activated

### Notification Content
```yaml
notification:
  type: "LOOP_DETECTED | BUDGET_WARNING | STALL | FAILURE"
  agent: "<agent name>"
  task_id: "<packet_id>"
  evidence: "<specific evidence>"
  recommendation: "<suggested action>"
  urgency: "LOW | MEDIUM | HIGH | CRITICAL"
```
