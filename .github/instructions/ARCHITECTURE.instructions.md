---
name: ARCHITECTURE
applyTo: '**'
description: Canonical machine-enforceable architecture contract for the Vibecoding multi-agent system. Deterministic lifecycle, orchestration, governance, OIP, and OCF.
---

# Vibecoding Architecture Contract (LLM-Optimized)

Version: 9.1.0
Owner: ReaperOAK
Mode: Deterministic, event-driven, enforcement-first

## 0) Rule Hierarchy (strict)

When rules conflict, apply first match only:
1. `.github/instructions/core_governance.instructions.md`
2. `.github/governance/*`
3. `.github/agents/*.agent.md`
4. This file
5. Delegation packet

Unresolved conflict => emit `NEEDS_INPUT_FROM` and halt affected ticket.

## 1) System Identity

- System type: multi-agent, ticket-driven orchestration.
- Primary invariant: `ONE TICKET -> FULL LIFECYCLE -> COMMIT -> DONE`.
- ReaperOAK is orchestrator-only; no implementation work.
- Scheduling is continuous and event-driven.
- Strategic and execution layers run concurrently.

## 2) Agent Topology

### 2.1 Strategic Layer
- Research Analyst
- Product Manager
- Architect
- Security Engineer (threat modeling)
- UIDesigner (conceptual)
- DevOps Engineer (planning)
- TODO (decomposition, ReaperOAK-only invocation)

### 2.2 Execution Layer
- Backend
- Frontend Engineer
- DevOps Engineer (execution)
- QA Engineer
- Security Engineer (execution)
- Documentation Specialist
- Validator
- CI Reviewer

### 2.3 Hard Topology Constraints
- No direct worker-to-worker communication.
- Cross-agent communication occurs via artifacts + events only.
- All workers are ephemeral and single-ticket scoped.

## 3) Lifecycle Contract (non-skippable)

Canonical lifecycle:

`READY -> LOCKED -> IMPLEMENTING -> QA_REVIEW -> VALIDATION -> DOCUMENTATION -> CI_REVIEW -> COMMIT -> DONE`

Rules:
- no skip
- no merge
- no reorder
- failed stage => `REWORK`
- `REWORK` max = 3, then `ESCALATED`

## 4) Mandatory Post-Execution Chain

After IMPLEMENTING success, enforce exact order:
1. QA
2. Security
3. Validator
4. Documentation
5. CI Reviewer
6. Commit (Validator authority)

Any rejection returns ticket to `REWORK`.

## 5) Delegation Contract

Every worker dispatch requires a packet matching `.github/tasks/delegation-packet-schema.json`.

Required fields:
- `ticket_id`
- `assigned_to`
- `role`
- `priority`
- `task_summary`
- `acceptance_criteria`
- `upstream_artifacts`
- `expected_outputs`
- `constraints`
- `context_chunks`
- `governance_chunks`
- `timeout`
- `rework_budget`

Missing field => reject dispatch.

## 6) Worker Model + Parallelism

- Worker id format: `{Role}Worker-{shortUuid}`
- one worker = one ticket
- one invocation = one SDLC stage
- no worker reuse across tickets
- dispatch all conflict-free READY tickets in parallel
- conflicted tickets stay READY and are retried next cycle

Conflict classes:
- file overlap
- schema overlap
- endpoint overlap
- exclusive infra overlap
- dependency lock overlap
- branch/merge overlap

## 7) Scheduler Loop (deterministic)

```text
LOOP:
  governance_integrity_check()
  health_sweep()
  autoscale_pools()
  assign_conflict_free_ready_tickets()
  enforce_concurrency_floor()
  parallel_dispatch_locked_tickets()
  await_next_event()
```

Health sweep checks:
- stalled tickets
- expired locks
- missing memory entries
- incomplete post-chain
- scope drift

## 8) Event Protocol (required)

Core events:
- `TASK_STARTED`
- `TASK_COMPLETED`
- `TASK_FAILED`
- `NEEDS_INPUT_FROM`
- `BLOCKED_BY`
- `QA_PASS` / `QA_REJECT`
- `VALIDATOR_PASS` / `VALIDATOR_REJECT`
- `DOCS_UPDATED`
- `CI_PASS` / `CI_REJECT`
- `COMMITTED`
- `REWORK_TRIGGERED`
- `ESCALATED`
- `PROTOCOL_VIOLATION`
- `GOVERNANCE_DRIFT`
- `WORKER_SPAWNED` / `WORKER_TERMINATED`

Evidence requirement:
- completion/failure events must include artifact paths, execution output, confidence.

## 9) State + Memory Files

Canonical shared files:
- `.github/memory-bank/workflow-state.json`
- `.github/memory-bank/artifacts-manifest.json`
- `.github/memory-bank/feedback-log.md`
- `.github/memory-bank/activeContext.md`
- `.github/memory-bank/progress.md`

Write discipline:
- append-only where specified
- no destructive rewrites of history
- authority boundaries from agent definitions are binding

## 10) Human Approval Gates

Explicit user approval required before:
- destructive database operations
- mass deletions / force pushes
- production deploys / merges to protected branches
- new external dependency introduction
- destructive schema migrations
- irreversible operations

No implicit approval allowed.

## 11) TODO Decomposition Contract

Only ReaperOAK may invoke TODO.

Mandatory order for multi-step work:
1. Strategic Mode (L0->L1)
2. Planning Mode (L1->L2)
3. Execution Planning Mode (L2->L3)

Rules:
- L3 tasks become tickets in READY state.
- TODO may emit `REQUIRES_STRATEGIC_INPUT`; decomposition pauses until routed response received.
- TODO cannot self-initiate strategic decisions.

## 12) Two-Layer Concurrency + SDR

Strategic and execution layers run simultaneously.

SDR lifecycle:
`PROPOSED -> APPROVED -> APPLIED -> ARCHIVED`

SDR rules:
- only strategic-layer agents may propose
- only ReaperOAK may approve/reject
- approved SDR increments roadmap minor version
- non-blocking SDRs do not halt unaffected execution
- blocking SDRs halt only affected tickets
- rejected SDRs are archived with reason

## 13) OIP Invariants (non-negotiable)

Core invariants:
- lifecycle traversal required
- scoped git only
- memory gate before COMMIT
- evidence required for completion
- single-ticket worker scope

Drift handling:
- violation => emit `PROTOCOL_VIOLATION`
- spawn ComplianceWorker (`auto_repair: true`)
- isolate repair to affected ticket
- do not halt unrelated tickets

## 14) Commit Enforcement

- two-commit protocol per ticket per stage (claim + work)
- Commit 1 (CLAIM): ticket JSON only, distributed lock via push
- Commit 2 (WORK): code + summary + ticket advance
- message begins with `[TICKET-ID]`
- explicit file staging only
- forbidden: `git add .`, `git add -A`, `git add --all`

Scoped git violation => drift event + block commit.

## 15) UI Gate

For frontend-affecting tickets:
- require UI design artifact before READY->LOCKED transition
- artifact path is governed by UI policy

No UI ticket starts without gate satisfaction.

## 16) Governance Integrity Check

Every scheduler cycle verifies:
- governance version alignment
- required governance files exist and are non-empty
- canonical policy domains are not duplicated
- instruction file size limits respected by policy

Integrity failure:
- emit `GOVERNANCE_DRIFT`
- suspend new assignments
- continue monitoring + recovery

## 17) Operational Concurrency Floor (OCF)

Constant:
- `MIN_ACTIVE_WORKERS = 10`

Work classes:
- Class A: primary tickets (non-preemptible)
- Class B: background tickets (preemptible)

Rules:
- if active workers < floor, spawn Class B until floor met
- Class A always preempts Class B
- Class B must not block Class A file paths
- Class B defaults to read-only analysis + scoped proposals
- throttle/suspend Class B under backlog/token/rework pressure

## 18) Security + Observability Baseline

Security:
- least privilege
- no authority hallucination
- policy-first execution

Observability:
- all state transitions evented
- audit trail retained in canonical state files
- confidence recorded with completion claims

## 19) Definition of Done Gate

A ticket is DONE only if all are true:
1. reached lifecycle state `DONE`
2. post-execution chain passed
3. memory gate satisfied
4. commit enforcement satisfied
5. artifacts registered
6. completion event includes evidence

If any condition fails: ticket is not DONE.

## 20) Boot Sequence (worker-level requirement)

Before action, workers must load in order:
1. required memory files
2. STOP_ALL gate
3. core governance
4. two-commit protocol (`governance/two_commit_protocol.md`)
5. role agent chunks
6. task-relevant catalog chunks
7. upstream summary from `.github/agent-output/` (if exists)

If STOP gate active: no edits, no execution actions.

## 21) Canonical References

- `.github/instructions/core_governance.instructions.md`
- `.github/instructions/distributed-execution.instructions.md`
- `.github/governance/lifecycle.md`
- `.github/governance/worker_policy.md`
- `.github/governance/event_protocol.md`
- `.github/governance/context_injection.md`
- `.github/governance/memory_policy.md`
- `.github/governance/commit_policy.md`
- `.github/governance/security_policy.md`
- `.github/governance/ui_policy.md`
- `.github/governance/performance_monitoring.md`
- `.github/governance/two_commit_protocol.md`
- `.github/tasks/delegation-packet-schema.json`
- `.github/tickets/ticket-schema.json`
- `.github/tickets.py`
- `.github/agent-runner.py`

End of contract.
