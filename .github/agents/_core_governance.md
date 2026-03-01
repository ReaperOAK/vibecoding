---
user-invokable: false
---

# Core Governance — Canonical Authority

> **GOVERNANCE_VERSION: 9.0.0**
>
> This is the **canonical governance authority** for the vibecoding multi-agent
> system. No agent may override these rules. All agent files must reference
> this document. Conflicts between agent instructions and this document are
> resolved in favor of this document.

---

## 1. Governance File Index

All governance policy files live in `.github/governance/`. Each is
self-contained and ≤ 250 lines. Together they define the complete operational
policy for the system.

| File | Purpose |
|------|---------|
| `governance/lifecycle.md` | SDLC 9-state machine, state transitions, Definition of Done, post-execution chain |
| `governance/commit_policy.md` | Per-ticket atomic commits, scoped git rules, DRIFT-002 enforcement |
| `governance/worker_policy.md` | Unbounded elastic pools, one-ticket-one-worker, anti-one-shot guardrails |
| `governance/memory_policy.md` | Memory gate (INV-4), 5 required fields, DRIFT-003 enforcement |
| `governance/ui_policy.md` | Stitch mockup gate for UI-touching tickets, UIDesigner artifact checklist |
| `governance/security_policy.md` | Human approval gates, INV-7 security review triggers, dual-layer security |
| `governance/event_protocol.md` | 24 event types, 20 routing rules, payload format, blocking protocol |
| `governance/context_injection.md` | Role-based injection, deterministic boot sequence, sliding context window |
| `governance/performance_monitoring.md` | Token budgets, auto-summarize protocol, drift correlation metrics |

---

## 2. Core Invariants (9)

From OIP §19. Every invariant is continuously monitored by the Health Sweep.
Violation emits `PROTOCOL_VIOLATION` and triggers auto-repair.

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| INV-1 | Every ticket completes full 9-state SDLC lifecycle — no state skips | Drift Detection, Health Sweep |
| INV-2 | Every ticket produces exactly one scoped atomic commit | Scoped Git, Commit Enforcement |
| INV-3 | No `git add .` / `git add -A` / `git add --all` — explicit file staging only | Scoped Git |
| INV-4 | Memory bank must update after every ticket reaches DONE | Memory Gate |
| INV-5 | Documentation must update when ticket touches user-facing behavior | Post-Execution Chain |
| INV-6 | QA Engineer AND Validator must run for every ticket — no self-validation | Post-Execution Chain |
| INV-7 | Security Engineer must review when ticket introduces new risk surface | Security Policy |
| INV-8 | Worker may only operate on its assigned ticket — single-ticket scope | Anti-One-Shot, Worker Termination |
| INV-9 | All post-execution chain steps must complete — no step skipping | Post-Execution Chain |

---

## 3. Drift Violation Types (9)

From OIP §20, extended with governance integrity violations.

| ID | Name | Detection Rule | Invariant |
|----|------|---------------|-----------|
| DRIFT-001 | LIFECYCLE_SKIP | Ticket advanced past a state without completing prior guard conditions | INV-1 |
| DRIFT-002 | UNSCOPED_COMMIT | `git add .` / `-A` / `--all` detected in commit command | INV-3 |
| DRIFT-003 | MISSING_MEMORY_ENTRY | Ticket at COMMIT but no memory bank entry for this ticket ID | INV-4 |
| DRIFT-004 | MISSING_DOCUMENTATION | Ticket at DOCUMENTATION but no artifact update produced | INV-5 |
| DRIFT-005 | CHAIN_STEP_SKIPPED | Ticket advanced without passing through all post-chain stages | INV-9 |
| DRIFT-006 | MULTI_TICKET_VIOLATION | Worker output references ticket IDs other than its assigned ticket | INV-8 |
| DRIFT-007 | UNVERIFIED_EVIDENCE | TASK_COMPLETED accepted without required evidence fields | INV-6 |
| DRIFT-008 | GOVERNANCE_VERSION_MISMATCH | Agent file declares governance_version ≠ system GOVERNANCE_VERSION | — |
| DRIFT-009 | OVERSIZED_INSTRUCTION | Governance file > 250 lines, agent file > 300 lines, or chunk > 4000 tokens | — |

---

## 4. Version Tracking Rule

GOVERNANCE_VERSION is tracked ONLY in governance policy files and this
authority file — NOT in `.agent.md` YAML frontmatter. Agent files must not
contain governance version fields.

### Enforcement

- At each scheduling interval, ReaperOAK checks that ALL governance files
  and `_core_governance.md` declare the same GOVERNANCE_VERSION
- If any governance file has a mismatched version:
  - Emit `INSTRUCTION_MISALIGNMENT` event
  - Emit DRIFT-008 (GOVERNANCE_VERSION_MISMATCH)
  - Auto-correct the mismatched file to the authoritative version
- Agent `.agent.md` files are version-agnostic — they reference governance
  policies by path, not by version number

---

## 5. Key Rules Summary

Compact reference for all agents. Each rule is enforced by the corresponding
governance policy file.

| Rule | Enforcement |
|------|-------------|
| Workers are unbounded — no maxSize cap on elastic pools | worker_policy.md |
| One ticket, one worker, no reuse across tickets | worker_policy.md |
| Scoped git only — no `git add .` or wildcards | commit_policy.md |
| Memory entry required before COMMIT state | memory_policy.md |
| Full post-execution chain mandatory (QA → Validator → Doc → CI → Commit) | lifecycle.md |
| No direct agent communication — all routing through ReaperOAK | event_protocol.md |
| Evidence required for every TASK_COMPLETED event | worker_policy.md |
| 3 rework max per ticket before escalation to user | lifecycle.md |
| Human approval for destructive operations | security_policy.md |
| Stitch mockup required before Frontend receives UI-touching tickets | ui_policy.md |
| Security review when ticket introduces new risk surface (INV-7) | security_policy.md |
| Context injection ≤ 100K tokens per worker (SAFE_CONTEXT_THRESHOLD) | context_injection.md |
| Governance files ≤ 250 lines, agent files ≤ 300 lines | context_injection.md |
| GOVERNANCE_VERSION tracked only in governance files + this authority | This file (§4) |

---

## 6. Governance Integrity

### Version Tracking

- Current: **GOVERNANCE_VERSION 9.0.0**
- All governance files declare the same version at their top
- Version bump requires updating ALL governance files + this authority file

### Integrity Checks (Health Sweep)

The Health Sweep periodically verifies governance integrity:

1. All governance files declare matching GOVERNANCE_VERSION
2. No governance file exceeds MAX_GOVERNANCE_FILE (250 lines)
3. No agent file exceeds MAX_AGENT_FILE (300 lines)
4. No chunk file exceeds MAX_CHUNK_FILE (4000 tokens)
5. No duplicate rule definitions across governance files
6. `_core_governance.md` declares matching GOVERNANCE_VERSION

Violations emit `GOVERNANCE_DRIFT` event and trigger auto-correction.

### Authority Hierarchy

```
_core_governance.md (THIS FILE)
    ├── governance/lifecycle.md
    ├── governance/commit_policy.md
    ├── governance/worker_policy.md
    ├── governance/memory_policy.md
    ├── governance/ui_policy.md
    ├── governance/security_policy.md
    ├── governance/event_protocol.md
    ├── governance/context_injection.md
    └── governance/performance_monitoring.md
```

This file is the root authority. Governance policy files provide detailed
rules. Agent files implement the policies. Chunks provide task-specific
guidance. In any conflict, authority flows top-down through this hierarchy.

---

## 7. Change Protocol

To modify governance rules:

1. Propose change via SDR (Strategic Decision Record)
2. ReaperOAK + human approve the SDR
3. Update the affected governance file(s)
4. Update `GOVERNANCE_VERSION` in ALL governance files + this authority file
5. Emit `GOVERNANCE_DRIFT` check to verify consistency across all governance files
7. Log the change in `.github/memory-bank/decisionLog.md`

No governance change may be applied without updating the version across
all files. Partial updates trigger DRIFT-008 on the next Health Sweep.
