---
name: SDLC Lifecycle
applyTo: '**'
description: 9-state lifecycle, post-execution chain, rework rules, Definition of Done, stage transitions.
---

# SDLC Lifecycle

## 1. 9-State Machine

RULE: Every ticket traverses 9 states in strict order. No exceptions.

```
READY -> LOCKED -> IMPLEMENTING -> QA_REVIEW -> VALIDATION -> DOCUMENTATION -> CI_REVIEW -> COMMIT -> DONE
```

PROHIBITED: Skipping any state.
PROHIBITED: Merging states.
PROHIBITED: Reordering states.

## 2. State Definitions

| State | Description | Owner |
|-------|-------------|-------|
| READY | Dependencies met, eligible for claim | System (tickets.py) |
| LOCKED | Worker claimed ticket via push | Agent (claim commit) |
| IMPLEMENTING | Agent executing work | Assigned agent |
| QA_REVIEW | QA + Security + Validator reviewing | QA, Security, Validator |
| VALIDATION | All reviews passed | Validator (confirmation) |
| DOCUMENTATION | Docs being updated | Documentation Specialist |
| CI_REVIEW | Lint, types, complexity check | CI Reviewer |
| COMMIT | Final commit being created | Agent (work commit) |
| DONE | Lifecycle complete | System |

## 3. Post-Execution Chain

REQUIRED: After implementation success, execute in strict order:
1. QA Engineer
2. Security Engineer
3. Validator
4. Documentation Specialist
5. CI Reviewer
6. Commit (by Validator)

RULE: Any rejection returns ticket to REWORK.
PROHIBITED: Skipping any step in the chain.
PROHIBITED: Reordering the chain.

## 4. Rework Rules

RULE: REWORK is a side-state entered on rejection by QA, Security, Validator, or CI.
RULE: Maximum 3 combined rework attempts per ticket.
RULE: After 3 reworks => ESCALATED to human.
RULE: Rework re-enters at IMPLEMENTING with rejection evidence attached.

## 5. Definition of Done (10 Items)

REQUIRED: Every ticket must satisfy ALL items. Validator verifies independently.

1. Code implemented (all acceptance criteria met)
2. Tests written (>=80% coverage for new code)
3. Lint passes (zero errors, zero warnings)
4. Type checks pass
5. CI passes (all workflow checks green)
6. Docs updated (JSDoc/TSDoc, README if applicable)
7. Reviewed by Validator (independent review)
8. No console errors (structured logger only)
9. No unhandled promises
10. No TODO comments in code

## 6. Stage Transition Guards

| From | To | Guard |
|------|----|-------|
| READY | LOCKED | Claim commit pushed successfully |
| LOCKED | IMPLEMENTING | Work begins |
| IMPLEMENTING | QA_REVIEW | Agent emits completion with evidence |
| QA_REVIEW | VALIDATION | QA PASS + Security PASS + Validator APPROVED |
| QA_REVIEW | REWORK | Any reviewer rejects |
| VALIDATION | DOCUMENTATION | Validator confirmation |
| DOCUMENTATION | CI_REVIEW | Doc update confirmed |
| CI_REVIEW | COMMIT | CI pass + memory gate pass |
| CI_REVIEW | REWORK | Lint/type/complexity failure |
| COMMIT | DONE | Scoped commit success |
| REWORK | IMPLEMENTING | Rework count < 3 |
| REWORK | ESCALATED | Rework count >= 3 |

## 7. TODO Agent Decomposition

RULE: Only ReaperOAK may invoke TODO agent.
REQUIRED: Decomposition order for multi-step work:
1. Strategic Mode (L0->L1): Vision to capabilities
2. Planning Mode (L1->L2): Capabilities to execution blocks
3. Execution Planning Mode (L2->L3): Blocks to actionable tickets

RULE: L3 tasks become tickets in READY state (after dependency check).
PROHIBITED: Jumping from L0 to L3 directly.
