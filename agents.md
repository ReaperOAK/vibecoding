# Agent Execution Contract (LLM-Optimized)

Machine-priority protocol. Follow exactly. No interpretation layer.

## 0) Rule Precedence

When rules conflict, apply highest first:
1. `.github/instructions/core_governance.instructions.md`
2. `.github/governance/*`
3. `.github/agents/*.agent.md`
4. This file (`agents.md`)
5. Delegation prompt

If unresolved conflict remains: STOP and emit `NEEDS_INPUT_FROM: ReaperOAK`.

## 1) Required Boot Sequence (run in order, no skips)

1. Read `.github/memory-bank/activeContext.md`
2. Read `.github/memory-bank/progress.md`
3. Read `.github/memory-bank/systemPatterns.md`
4. Read `.github/memory-bank/productContext.md`
5. Read `.github/guardian/STOP_ALL`
6. Read `.github/instructions/core_governance.instructions.md`
7. Read all files in `.github/vibecoding/chunks/{YourAgent}.agent/`
8. Read `.github/vibecoding/catalog.yml`; load task-relevant chunks

Conditional reads:
- Read `.github/memory-bank/decisionLog.md` only for architecture decisions.
- Read `.github/memory-bank/riskRegister.md` only for security/risk tasks.

Hard gate:
- If `.github/guardian/STOP_ALL` contains `STOP`: perform zero file edits, zero execution actions, report blocked.

## 2) Identity and Scope Invariants

1. ReaperOAK is orchestrator-only: no implementation, no file edits, no direct build/test execution.
2. Worker handles exactly one ticket.
3. Worker handles exactly one SDLC stage per invocation.
4. Never reference or modify artifacts outside assigned ticket scope unless explicitly delegated.

Violation outcome: terminate task and report protocol violation.

## 3) Required Ticket Lifecycle

Canonical state machine:

`READY → LOCKED → IMPLEMENTING → QA_REVIEW → VALIDATION → DOCUMENTATION → CI_REVIEW → COMMIT → DONE`

No skip, no merge, no reorder.

On failure at any stage:
- Emit failure event with evidence.
- Return ticket to `READY`/`REWORK` per policy.
- Do not advance downstream.

## 4) Mandatory Stage Chain Constraints

- Execution chain always includes: QA → Validator → Documentation → CI Reviewer.
- Validator may reject completion; rejection blocks advancement.
- Only commit stage may finalize ticket.
- Max rework loop: 3 iterations, then escalate.

## 5) TODO Agent Constraints

- Only ReaperOAK may invoke TODO.
- Mandatory decomposition order for multi-step work:
  1. Strategic Mode (L0→L1)
  2. Planning Mode (L1→L2)
  3. Execution Planning Mode (L2→L3)
- TODO may emit `REQUIRES_STRATEGIC_INPUT`; pause until routed answer received.

## 6) Worker Pool/Parallelism Constraints

1. One ephemeral worker per ticket: `{Role}Worker-{shortUuid}`.
2. No worker reuse across tickets.
3. Dispatch all conflict-free READY tickets in parallel.
4. Parallelism is ticket-level, not state-skip.

## 7) Tooling and Discovery

Use actionable-task query before assignment-sensitive work:

`python3 todo_visual.py --ready`
`python3 todo_visual.py --ready --json`

Treat returned tasks as only immediately assignable tickets.

## 8) Human Approval Gate (must ask first)

Require explicit approval before:
- Database drops / mass deletions / force pushes
- Production deploys / merges to main
- New external dependencies
- Destructive schema migrations
- Any irreversible data-loss operation

## 9) Memory Bank Write Contract (append-only)

Update when applicable:
- Focus shift → `activeContext.md`
- Milestone completion → `progress.md`
- New threat → `riskRegister.md`
- Significant trade-off (ReaperOAK only) → `decisionLog.md`

Before COMMIT, ticket memory entry in `activeContext.md` is mandatory:

```markdown
### [TICKET-ID] — Summary
- **Artifacts:** file1.ts, file2.ts
- **Decisions:** Chose X over Y because Z
- **Timestamp:** 2026-02-28T15:00:00Z
```

Missing memory entry = DRIFT-003.

## 10) OIP Critical Invariants (non-negotiable)

- INV-3 Scoped Git: never `git add .`, `git add -A`, `git add --all`; stage explicit files only.
- INV-4 Memory Gate: no COMMIT without required memory entry.
- INV-6 Evidence: `TASK_COMPLETED` must include artifacts, tests, confidence.
- INV-8 Single-Ticket Scope: cross-ticket work is hard-stop termination.

ComplianceWorker behavior:
- Auto-spawn on protocol violation with `auto_repair: true`.
- Performs single targeted repair only.
- Blocks only affected ticket.

Health Sweep monitors and auto-corrects:
- stalled tickets
- expired locks
- missing memory
- incomplete chains
- scope drift

## 11) Required Event Emissions

Emit structured events at state boundaries:
- `TASK_STARTED`
- `TASK_COMPLETED`
- `TASK_FAILED`
- `NEEDS_INPUT_FROM`
- `BLOCKED_BY`

Evidence rule: every claim must be backed by artifacts, logs, or explicit file evidence.

## 12) Anti-Loop Rule

If same failed approach repeats (>=3 identical attempts), stop retrying and switch strategy or escalate.

## 13) Reference Index

- `.github/tasks/delegation-packet-schema.json`
- `.github/tasks/definition-of-done-template.md`
- `.github/tasks/initialization-checklist-template.md`
- `.github/agents/_cross-cutting-protocols.md`
- `.github/agents/ReaperOAK.agent.md` (OIP canonical)
