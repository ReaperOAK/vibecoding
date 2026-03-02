---
name: Orchestration Rules
applyTo: '**'
description: Canonical machine-enforceable orchestration rules for task lifecycle, DAG execution, confidence gates, concurrency, validation, rollback, and escalation.
---

# Orchestration Rules Kernel (LLM-Optimized)

Version: 2.1.0
Owner: ReaperOAK
Mode: Deterministic, enforcement-first

## 0) Rule Priority

Apply first match only:
1. `.github/core_governance.instructions.md`
2. `.github/governance/*`
3. this file
4. delegation packet

Conflict unresolved => emit `NEEDS_INPUT_FROM` and halt affected task.

## 1) Task State Machine (non-skippable)

Canonical states:
`PENDING -> IN_PROGRESS -> REVIEW -> MERGED`

Failure/side states:
`BLOCKED`, `REJECTED`, `FAILED`, `ESCALATED`

Allowed transitions only:
- `PENDING -> IN_PROGRESS` (dependencies satisfied + agent assigned)
- `IN_PROGRESS -> REVIEW` (deliverable + required evidence)
- `IN_PROGRESS -> BLOCKED` (external blocker)
- `IN_PROGRESS -> FAILED` (retry limit hit)
- `REVIEW -> MERGED` (validation pass)
- `REVIEW -> REJECTED` (validation fail)
- `REJECTED -> IN_PROGRESS` (fix delta + retry <= 3)
- `REJECTED -> FAILED` (retry > 3)
- `BLOCKED -> PENDING` (blocker resolved)
- `BLOCKED -> ESCALATED` (cannot unblock autonomously)
- `FAILED -> ESCALATED` (human intervention required)
- `ESCALATED -> PENDING` (human resolution provided)

Forbidden:
- any transition not listed above
- state skipping
- silent retry without rejection reason

## 2) DAG Construction Contract

For every multi-step objective, ReaperOAK MUST build a DAG before delegation.

DAG must satisfy:
- acyclic graph (no cycles)
- every node has assigned agent
- every dependency references valid node
- no orphan nodes
- critical path identified
- token estimate per node

Batching rules:
- only dependency-free nodes may execute in same batch
- same-batch nodes must not share write scope
- conflict => serialize conflicting nodes

Checkpoint after each batch:
- completed tasks
- remaining tasks
- blockers
- tokens burned/remaining
- confidence level
- next batch id

## 3) Confidence-Gated Progression

Before phase transitions (`Analysis`, `Design`, `Implementation`, `Validation`), assess confidence.

Scale:
- `HIGH` 90-100 => proceed
- `MEDIUM` 70-89 => proceed with explicit risks
- `LOW` 50-69 => halt + gather context
- `INSUFFICIENT` <50 => escalate

Minimum go-forward threshold: `>= 70` unless explicit human override.

Confidence declaration must include:
- overall score
- factor scores
- risks
- mitigation actions
- decision (`PROCEED` | `HALT` | `ESCALATE`)

## 4) RUG Discipline (mandatory)

Before generation:
1. `READ` required context
2. `UNDERSTAND` objective, assumptions, unknowns, confidence
3. `GENERATE` scoped output grounded in loaded context

RUG violation signals:
- claims about unread files
- undeclared assumptions
- missing confidence
- unverifiable/hallucinated assertions

Violation response:
- reject output
- attach violation reason
- re-delegate with fix guidance

## 5) Concurrency Contract

Parallel-safe:
- read-only tasks
- write tasks on disjoint file scopes
- isolated test suites

Non-parallel-safe (must serialize):
- shared file writes
- shared schema/database mutations
- infra state mutations

Pre-batch requirements:
- declare owned file scopes per agent
- verify zero scope overlap
- reject batch on overlap

Post-batch enforcement:
- diff modified files vs owned scope
- out-of-scope write => `REJECTED` + rework

## 6) Integration Validation Gate (required after each batch)

Run all checks:
1. file conflict scan
2. interface/contract alignment
3. relevant tests
4. syntax/parse validity
5. convention compliance
6. dependency/import integrity
7. confidence reassessment

Outcomes:
- all pass => next batch
- conflict => re-run conflicting tasks sequentially
- test/syntax/convention fail => route to originator for fix
- confidence drops below 70 => halt DAG and reassess

## 7) Token Budget Rules

Per-DAG token budget is mandatory.

Threshold actions:
- `>= 70%` warn + re-plan remaining work
- `>= 85%` compress scope to critical tasks
- `>= 95%` execute critical path only
- `>= 100%` checkpoint and handoff

Track:
- allocated by role/task
- consumed by role/task
- remaining total
- burn rate
- overrun risk flag

## 8) Rollback Policy

Task-level rollback:
- identify modified artifacts
- revert scoped changes (git/file restore)
- block dependent tasks until recovery

Batch-level rollback:
- revert all batch writes
- convert failed parallel batch to sequential plan
- rerun with gate after each task

System-level rollback:
- halt active tasks
- snapshot state to memory
- escalate with recovery recommendation

## 9) Loop Detection + Breakers

Loop signals:
- retries > 3
- same error fingerprint 3x
- no measurable progress across 2 cycles
- token overrun for single task
- timeout threshold exceeded
- circular delegation chain
- confidence regression after retries

On loop detect:
1. halt task
2. mark `FAILED`
3. emit diagnostics
4. escalate or re-plan with different strategy

## 10) Delegation Protocol

### 10.1 Pre-Delegation Requirements

ReaperOAK MUST ensure:
- objective is measurable
- acceptance criteria are testable
- include/exclude scope is explicit
- forbidden actions listed
- output format specified
- evidence expectations specified
- dependencies merged
- ownership (for parallel tasks) declared
- timeout set
- confidence >= 70 or justified override

### 10.2 Post-Delegation Acceptance Gate

Accept output only if:
- format valid
- all criteria satisfied
- evidence verifiable
- no forbidden actions/files
- no hallucinated capability claims
- quality/self-check present where required
- token usage within acceptable envelope

Else => reject + rework delta.

## 11) Communication Rules

Allowed communication paths:
- structured delegation output
- event emissions
- approved memory append entries

Forbidden:
- direct worker-to-worker communication
- hidden/unlogged coordination

Error report minimum fields:
- task id
- agent
- error type
- error message
- attempted fix
- retry count
- confidence
- recommended next action

## 12) Governance Hooks + Modes

Hooks (if configured) may enforce audit/blocking at runtime.

Governance modes:
- `open`: log
- `standard`: log + warn
- `strict`: log + block on threat signals
- `locked`: log + block + require human approval

Mode is externally configured; agents must comply with active mode.

## 13) Escalation Rules

Escalate when:
- confidence < 50
- retry budget exhausted
- unresolved conflict with higher-priority policy
- destructive operation requires approval
- blocked state cannot be autonomously resolved

Escalation packet must include:
- current state
- attempted paths
- blockers
- evidence
- recommended options

End of orchestration kernel.
