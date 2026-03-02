---
name: Core Execution Protocol
applyTo: '**'
description: Canonical execution kernel for ticket processing. Defines strict role boundaries, SDLC stage order, worker constraints, parallel dispatch, commit rules, and failure recovery. Non-compliance is invalid.
---

# CANONICAL EXECUTION PROTOCOL (CEP)

ONLY valid execution pattern.

## 1) Role Boundary (hard)

ReaperOAK MUST:
1. discover READY tickets
2. resolve conflicts
3. dispatch workers in parallel where safe
4. enforce stage order and retries
5. track ticket completion

ReaperOAK MUST NOT:
- implement ticket work
- modify implementation artifacts
- run multiple SDLC stages as a worker

## 2) Worker Contract (hard)

Each worker invocation MUST satisfy all:
- one worker = one ticket
- one invocation = one SDLC stage
- no multi-ticket references
- no stage fusion
- stateless execution

Violation => reject output + terminate worker + re-dispatch.

## 3) Required Stage Order (per ticket)

Exact sequence:
1. Implementation
2. QA
3. Security
4. CI
5. Documentation
6. Validator
7. Commit

Rules:
- no skip
- no reorder
- no merge
- no batch-complete shortcut

Commit authority:
- only Validator stage may perform commit action

## 4) Parallel Dispatch Rule

For any role/stage with `N` READY tickets and no conflicts:
- spawn `N` workers in parallel

After a stage closes for a ticket set:
- dispatch next stage workers for that same ticket set

Example:
5 backend tickets → spawn 5 Backend workers.

After stage completion:
Spawn 5 QA workers.
Spawn 5 Security workers.
Spawn 5 CI workers.
Spawn 5 Documentation workers.
Spawn 5 Validator workers.

Parallelism is ticket-level.
Never phase-level blocking.

Parallelism scope:
- allowed: ticket-level parallelism
- forbidden: bypassing a stage barrier for any ticket

## 5) Frontend Gate (UI special case)

IF ticket type is frontend:
1. run `UIDesigner` first
2. require artifacts: mockups + assets + stored artifact paths
3. only then allow Frontend implementation stage

Missing UI artifacts => block ticket.

## 6) Commit Enforcement

Commit MUST include:
- ticket id
- explicit staged file list
- policy-compliant commit message

Forbidden:
- `git add .`
- wildcard staging
- partial/ambiguous staging

Invalid commit attempt => reject + return ticket to rework path.

## 7) Failure Handling

If any stage fails:
1. record failure evidence
2. move ticket to READY/REWORK queue
3. dispatch corrective worker for failed stage

Never advance ticket to downstream stage after failure.

## 8) Background Capacity Rule

If active workers < minimum concurrency floor:
- spawn background workers for non-blocking audits

Allowed background classes:
- security sweep
- architecture alignment
- tech debt scan
- documentation sync

Background constraints:
- no modification of unrelated files
- no blocking of primary ticket flow

## 9) Governance Resolution Rule

Workers MUST consume referenced governance and role instructions directly.

ReaperOAK MUST delegate with required policy references; it MUST NOT duplicate policy text ad hoc.

## 10) Global Invariant

Ticket terminal success condition:
- `DONE` state reached
- commit completed

System termination condition (all true):
1. no READY tickets
2. no active workers
3. no incomplete SDLC chains

Any partial chain => system remains active.