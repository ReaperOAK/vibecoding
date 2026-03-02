---
name: CORE_GOVERNANCE
applyTo: '**'
description: Canonical governance kernel for the vibecoding multi-agent system. Defines precedence, invariants, drift types, integrity checks, and change protocol. Highest authority.
---

# Core Governance Kernel (Canonical Authority)

`GOVERNANCE_VERSION: 9.1.0`

This file is highest governance authority. No lower instruction may override it.

## 1) Authority Order

Apply first match only:
1. `core_governance.instructions.md` (this file)
2. `.github/governance/*`
3. `.github/agents/*.agent.md`
4. task/delegation prompts

Conflict unresolved => emit `NEEDS_INPUT_FROM` and halt affected ticket.

## 2) Canonical Governance Files

All are required and authoritative:
- `governance/lifecycle.md`
- `governance/commit_policy.md`
- `governance/worker_policy.md`
- `governance/memory_policy.md`
- `governance/ui_policy.md`
- `governance/security_policy.md`
- `governance/event_protocol.md`
- `governance/context_injection.md`
- `governance/performance_monitoring.md`
- `governance/concurrency_floor.md`
- `governance/two_commit_protocol.md`

If any missing/empty => emit `GOVERNANCE_DRIFT`, suspend new assignments.

## 3) Core Invariants (INV)

- `INV-1` Full 9-state lifecycle traversal; no state skips.
- `INV-2` Exactly one scoped atomic commit per ticket.
- `INV-3` Scoped git only; forbid `git add .`, `git add -A`, `git add --all`.
- `INV-4` Memory entry required for each ticket before/at completion gate.
- `INV-5` Docs update required for user-facing behavior changes.
- `INV-6` QA + Validator required; no self-validation substitution.
- `INV-7` Security review required for every ticket.
- `INV-8` Single-ticket worker scope only.
- `INV-9` Full post-execution chain required; no step skipping.
- `INV-10` Two-commit protocol mandatory; claim before work.
- `INV-11` Agent summary handoff via `.github/agent-output/` only.

Any INV breach => emit `PROTOCOL_VIOLATION` and trigger auto-repair workflow.

## 4) Drift Types (DRIFT)

- `DRIFT-001` LIFECYCLE_SKIP
- `DRIFT-002` UNSCOPED_COMMIT
- `DRIFT-003` MISSING_MEMORY_ENTRY
- `DRIFT-004` MISSING_DOCUMENTATION
- `DRIFT-005` CHAIN_STEP_SKIPPED
- `DRIFT-006` MULTI_TICKET_VIOLATION
- `DRIFT-007` UNVERIFIED_EVIDENCE
- `DRIFT-008` GOVERNANCE_VERSION_MISMATCH
- `DRIFT-009` OVERSIZED_INSTRUCTION
- `DRIFT-010` SKIPPED_CLAIM_COMMIT
- `DRIFT-011` WRONG_STAGE_CLAIM
- `DRIFT-012` MULTI_TICKET_CLAIM
- `DRIFT-013` CROSS_STAGE_MODIFY
- `DRIFT-014` MISSING_SUMMARY_FILE
- `DRIFT-015` SUMMARY_WRONG_DIRECTORY

Detected drift => emit drift event + isolate affected ticket + auto-repair attempt.

## 5) Version Rules

`GOVERNANCE_VERSION` appears only in:
- this file
- governance policy files

`GOVERNANCE_VERSION` MUST NOT appear in `.agent.md` frontmatter.

On mismatch:
1. emit `INSTRUCTION_MISALIGNMENT`
2. emit `DRIFT-008`
3. block downstream transitions until corrected

## 6) Hard Operational Rules

- Unbounded worker pools allowed; no artificial max cap.
- One worker handles one ticket; no reuse across tickets.
- Mandatory chain: `QA -> Security -> Validator -> Documentation -> CI -> Commit`.
- Max rework attempts per ticket: `3`, then escalate.
- No direct agent-to-agent messaging; route via orchestrator + artifacts/events.
- Evidence required for `TASK_COMPLETED` acceptance.
- Human approval required for destructive/irreversible operations.
- UI tickets require UI gate artifact before execution handoff.
- OCF required: `MIN_ACTIVE_WORKERS = 10` with Class A preempting Class B.
- Class B background workers: read-only by default, anti-recursion enforced.

## 7) Integrity Checks (every scheduling interval)

Must verify:
1. governance version alignment across all governance files + this file
2. required governance files present and non-empty
3. file size limits:
   - governance file `<= 250` lines
   - agent file `<= 300` lines
   - chunk file `<= 4000` tokens
4. no duplicated canonical policy domains

Failure => emit `GOVERNANCE_DRIFT`, suspend new assignments, continue monitoring.

## 8) Change Protocol (non-optional)

To change governance:
1. create SDR proposal
2. obtain ReaperOAK + human approval
3. update affected governance files
4. update `GOVERNANCE_VERSION` in all governance files + this file
5. run integrity check and emit result
6. append decision to `.github/memory-bank/decisionLog.md`

Partial governance updates are invalid and must trigger `DRIFT-008`.

End of kernel.
