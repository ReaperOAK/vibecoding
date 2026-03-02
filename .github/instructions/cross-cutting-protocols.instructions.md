---
name: Cross-Cutting Protocols
applyTo: '**'
description: Machine-enforceable cross-cutting protocol kernel for all agents. Defines mandatory execution discipline, evidence gates, event emissions, anti-scope controls, and OIP response rules.
---
# Cross-Cutting Protocol Kernel (ALL Agents)

Highest-priority shared behavior contract for all agents.

## 0) Applicability

- Applies to every subagent and role.
- Enforced by ReaperOAK.
- Violations may trigger reject, rework, worker termination, or escalation.

## 1) Mandatory RUG Discipline

Before action, perform in order:
1. `READ` required context artifacts
2. `UNDERSTAND` objective + assumptions + confidence
3. `GENERATE` output grounded in loaded context

If output is not grounded in loaded context => reject as hallucination.

Orchestrator constraint:
- ReaperOAK delegates implementation via `runSubagent`; it does not implement directly.

## 2) Self-Reflection Gate

Before submission, score 1-10 for:
- correctness
- completeness
- convention alignment
- clarity
- impact/regression safety

Submission gate:
- all dimensions must be `>= 7`
- else self-iterate up to `3` loops
- after loop limit, escalate with honest scores

## 3) Confidence Gate

- `HIGH`: 90-100 => proceed
- `MEDIUM`: 70-89 => proceed with explicit risks
- `LOW`: 50-69 => pause + request review
- `INSUFFICIENT`: <50 => block + escalate unknowns

Confidence must include evidence.

## 4) Evidence Contract

Claims require proof:
- read claim => specific file pattern cited
- test claim => test output summary
- convention claim => named project convention
- security claim => mapped OWASP category/check

No evidence => claim invalid.

## 5) Context Loading Priority

- `P1` always: system patterns, delegation packet, target files
- `P2` if relevant: tests, API contracts, types
- `P3` summarize-only: large structural files
- `P4` skip: unrelated/generated/vendor assets

Before edits, create internal context map: primary files, dependencies, tests, change order.

## 6) File-Based Handoff Only

- No direct agent-to-agent communication.
- Coordination path is ReaperOAK + artifacts + events.
- Worker must read upstream artifacts before starting.
- Worker must follow upstream schemas/contracts.
- Missing/inconsistent upstream artifacts => stop and emit blocking event.

## 7) Required Event Emissions

Every ticket execution must emit:
- `TASK_STARTED` at start
- one terminal event: `TASK_COMPLETED` or `TASK_FAILED`

Blocking/coordination events:
- `NEEDS_INPUT_FROM`
- `BLOCKED_BY`
- `REQUEST_RESEARCH`
- `REQUIRES_UI_DESIGN`
- `ESCALATE_TO_PM`
- `REQUIRES_STRATEGIC_INPUT`

Long-task visibility:
- emit `PROGRESS_UPDATE` for effort > 30 min

`TASK_COMPLETED` required evidence fields:
- artifact paths
- test results (or justified `N/A`)
- confidence level

Missing evidence => reject completion.

## 8) Worker Pool Events (recognized)

- `WORKER_FREE`
- `WORKER_ASSIGNED`
- `WORKER_SPAWNED`
- `WORKER_TERMINATED`
- `POOL_SCALED_UP`
- `POOL_SCALED_DOWN`

Worker id format: `{Role}Worker-{shortUuid}`.

## 9) Anti-One-Shot + Scope Guardrails

Hard scope rules:
- output must reference assigned ticket only
- files modified must remain in ticket write scope
- no multi-ticket implementation in one response

Iteration rule for tasks > 30 min:
- minimum 2 passes
- recommended flow: draft -> self-review -> gap-fix -> final check

Pre-submission checks:
1. modified files in write scope
2. single assigned ticket reference only
3. all acceptance criteria addressed
4. self-reflection evidence present

Any scope breach => reject and re-delegate.

## 10) Strategic Event Restrictions

Strategic-only events:
- `SDR_PROPOSED`
- `SDR_APPROVED`
- `SDR_APPLIED`
- `STRATEGIC_REVIEW_REQUIRED`
- `ARCHITECTURE_RISK_DETECTED`
- `SCOPE_CONFLICT_DETECTED`

Execution-layer agents must not emit strategic-only events except escalation requests explicitly allowed by delegation.

Affected-ticket pause only; unaffected tickets continue.

## 11) OIP Response Rules (ALL Agents)

Recognize and respond to:
- `PROTOCOL_VIOLATION`
- `INSTRUCTION_MISALIGNMENT`
- `GOVERNANCE_DRIFT`
- `REPAIR_COMPLETED`
- `REPAIR_FAILED`

ComplianceWorker behavior:
- spawned with `auto_repair: true`
- single targeted repair action
- emits repair result event
- terminates after single action

## 12) Scoped Git Rules (hard)

Forbidden:
- `git add .`
- `git add -A`
- `git add --all`
- wildcard/glob staging

Required:
- explicit file list staging only
- staged files must match ticket scope
- `CHANGELOG.md` allowed when policy permits

Violation => `DRIFT-002`.

## 13) Memory Entry Gate

Before COMMIT, ensure entry exists in `.github/memory-bank/activeContext.md`:

```markdown
### [TICKET-ID] — {summary}
- **Artifacts:** {comma-separated file paths}
- **Decisions:** {key decisions made}
- **Timestamp:** {ISO8601}
```

Missing entry => `DRIFT-003` + rework/repair.

## 14) Single-Ticket Hard Kill

If output references other ticket IDs beyond assignment:
1. terminate worker
2. spawn replacement worker for rework
3. no same-instance retry

## 15) Health Sweep Awareness

Continuous checks may requeue/terminate affected work for:
- stalled tickets
- expired locks
- missing memory entries
- incomplete post-chain audit
- scope drift

This is expected governance behavior.

End of protocol kernel.
