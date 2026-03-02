---
name: Core Execution Protocol
applyTo: '**'
description: This file defines the Core Execution Protocol (CEP) for the vibecoding multi-agent system. It establishes the canonical execution pattern that all agents must follow when processing tickets. The CEP ensures a strict SDLC order, enforces single-ticket-single-worker rules, and mandates parallel processing of tickets by role. ReaperOAK orchestrates the execution flow but does not implement any stage logic or modify files directly. All agents must adhere to this protocol without deviation.
---

# CANONICAL EXECUTION PROTOCOL (CEP)

This file defines the ONLY valid execution pattern.

All agents must follow this protocol.

---

## 1. ReaperOAK Role

ReaperOAK does NOT implement.
ReaperOAK does NOT modify files.
ReaperOAK does NOT commit.

ReaperOAK ONLY:

1. Scans READY tickets.
2. Groups tickets by role.
3. Spawns parallel subagent workers.
4. Enforces no file conflicts.
5. Ensures full SDLC chain per ticket.
6. Repeats until no READY tickets remain.

---

## 2. Worker Model

Each worker:

- Handles ONE ticket only.
- Runs ONE stage only.
- Never handles multiple tickets.
- Never performs multiple SDLC stages in one invocation.

Workers are stateless.

---

## 3. Mandatory SDLC Order (Per Ticket)

Stage 1: Implementation Agent  
Stage 2: QA Agent  
Stage 3: Security Agent  
Stage 4: CI Agent  
Stage 5: Documentation Agent  
Stage 6: Validator Agent  

Only Validator may commit.

No stage skipping.
No stage merging.
No stage batching.

---

## 4. Parallelism Rule

For N READY tickets of same role:

Spawn N workers in parallel.

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

---

## 5. UI Special Case

If ticket type == FRONTEND:

Before Frontend stage:
Run UIDesigner stage.

UIDesigner must:
- Generate mockups
- Download assets
- Store artifacts

Then proceed to Frontend.

---

## 6. Commit Rules

Only Validator commits.
Commit must:
- Reference ticket ID
- Include file list
- Follow commit policy
- Stage only declared files

No `git add .`
No partial commits.

---

## 7. Error Handling

If any stage fails:

Return ticket to READY.
Log failure.
Spawn corrective worker.

Never skip forward.

---

## 8. Background Workers

If active workers < minimum threshold:

Spawn background audits:
- Security sweep
- Architecture alignment
- Tech debt scan
- Documentation sync

Background workers must not modify unrelated files.

---

## 9. Governance Lookup

Subagents know where to find:
- Best practices
- Security policies
- Architecture rules
- CI patterns

ReaperOAK does NOT repeat them.

---

## 10. System Invariant

Every ticket must end in:

DONE + COMMIT

No ticket may remain partially processed.

System halts only when:
- No READY tickets
- No active workers
- All SDLC chains complete