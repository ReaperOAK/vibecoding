---
name: Distributed Execution Protocol
applyTo: '**'
description: Machine-enforceable protocol for distributed multi-operator multi-machine ticket execution. Defines the Git-native state machine, two-commit protocol, tickets.py rules, and parallel safety constraints.
---

# Distributed Execution Protocol (DEP)

Version: 1.0.0
Owner: ReaperOAK
Mode: Deterministic, git-native, multi-machine

## 0) Scope

This protocol governs distributed execution across:
- Multiple human operators (e.g., Owais, Sujal)
- Multiple machines running agents concurrently
- Git as the sole synchronization mechanism
- File-based state machine (no external database)

All agents and operators MUST comply. No exceptions.

## 1) Distributed Ticket State Machine

### 1.1 State = Directory Location

Ticket state is determined by which directory contains the ticket JSON:

```
.github/ticket-state/
    READY/          # Unblocked, available for claim
    ARCHITECT/      # Being processed by Architect
    RESEARCH/       # Being processed by Research
    BACKEND/        # Being processed by Backend
    FRONTEND/       # Being processed by Frontend or UIDesigner
    QA/             # Being processed by QA
    SECURITY/       # Being processed by Security
    CI/             # Being processed by CIReviewer
    DOCS/           # Being processed by Documentation
    VALIDATION/     # Being processed by Validator
    DONE/           # Completed
```

### 1.2 Ticket Files

Each ticket exists as:
- Master copy: `.github/tickets/<ticket-id>.json`
- State copy: `.github/ticket-state/<STAGE>/<ticket-id>.json`

Both must be kept in sync. Master is source of truth for metadata.
State directory is source of truth for current stage.

### 1.3 SDLC Flows by Type

| Type | Flow |
|------|------|
| backend | READY → BACKEND → QA → SECURITY → CI → DOCS → VALIDATION → DONE |
| frontend | READY → UIDESIGNER → FRONTEND → QA → SECURITY → CI → DOCS → VALIDATION → DONE |
| fullstack | READY → BACKEND → FRONTEND → QA → SECURITY → CI → DOCS → VALIDATION → DONE |
| infra | READY → BACKEND → QA → SECURITY → CI → DOCS → VALIDATION → DONE |
| security | READY → SECURITY → QA → CI → DOCS → VALIDATION → DONE |
| docs | READY → DOCS → VALIDATION → DONE |
| research | READY → RESEARCH → DOCS → VALIDATION → DONE |
| architecture | READY → ARCHITECT → DOCS → VALIDATION → DONE |

No stage may be skipped. Order is enforced by `tickets.py`.

## 2) Two-Commit Protocol (Mandatory)

Every agent executes exactly two git commits per ticket stage.
Full specification: `.github/governance/two_commit_protocol.md`

### 2.1 Commit 1 — CLAIM (Distributed Lock)

```
1. git pull --rebase
2. Verify ticket in expected stage directory
3. Update claim metadata (claimed_by, machine_id, operator, lease_expiry)
4. git add <ticket JSON files only>
5. git commit -m "[TICKET-ID] CLAIM by AGENT on MACHINE (OPERATOR)"
6. git push
```

**Push success = lock acquired.**
**Push failure = another machine claimed first → ABORT.**

No code changes during claim commit. Period.

### 2.2 Commit 2 — WORK

```
1. Execute agent work
2. Write summary: .github/agent-output/<AgentName>/<ticket-id>.md
3. Delete previous stage summary
4. Move ticket to next stage directory
5. git add <explicit file list>
6. git commit -m "[TICKET-ID] STAGE complete by AGENT on MACHINE"
7. git push
```

## 3) Agent Summary Handoff

Context flows strictly via filesystem. ReaperOAK does NOT inject context.

```
Agent A writes:  .github/agent-output/AgentA/<ticket-id>.md
Agent B reads:   .github/agent-output/AgentA/<ticket-id>.md
Agent B deletes: .github/agent-output/AgentA/<ticket-id>.md
Agent B writes:  .github/agent-output/AgentB/<ticket-id>.md
```

Summary directories:
```
.github/agent-output/
    Architect/
    Research/
    Backend/
    Frontend/
    QA/
    Security/
    CIReviewer/
    Documentation/
    Validator/
    TODO/
    DevOps/
    ProductManager/
    UIDesigner/
```

Rules:
- One summary file per agent per ticket
- Filename: `<ticket-id>.md`
- Agent reads ONLY previous stage summary
- Agent deletes previous stage summary after processing
- No cross-agent summary reading outside chain

## 4) tickets.py Contract

Location: `.github/tickets.py`

### 4.1 Authorized Callers

- TODO agent (after L1→L2→L3 decomposition)
- Validator agent (before final DONE commit, to unblock freed tasks)
- Human operators (via CLI)

**No other agent may execute tickets.py.**

### 4.2 Operations

| Command | Purpose |
|---------|---------|
| `--sync` | Evaluate deps, move unblocked to READY, release expired claims |
| `--parse <dir>` | Parse L3 markdown into ticket JSON |
| `--status` | Dashboard view of all tickets |
| `--claim <id> <agent> <machine> <operator>` | Claim ticket |
| `--release <id>` | Release stale claim |
| `--advance <id> <agent>` | Move to next SDLC stage |
| `--rework <id> <agent> <reason>` | Send back for rework |
| `--validate` | Full integrity check |
| `--release-expired` | Clear all expired claims |

### 4.3 Sync Behavior

1. Release all expired claims
2. Evaluate dependency graph for all tickets
3. Move newly unblocked tickets to READY
4. Fix duplicates (ticket in multiple state dirs)
5. Validate integrity

## 5) Parallel Multi-Machine Rules

### 5.1 Before Any Work

```
git pull --rebase
```

### 5.2 Claim Protocol

1. Attempt claim commit + push
2. If push fails (conflict): skip ticket, try another
3. Never process a ticket without successful claim push
4. Never hold claims on multiple tickets per agent instance

### 5.3 Lease Mechanism

- Default lease: 30 minutes
- Expired lease: ticket becomes reclaimable
- Any machine may reclaim expired-lease ticket
- `tickets.py --release-expired` clears stale claims

### 5.4 Forbidden Actions

- Processing unclaimed tickets
- Modifying tickets in other stage directories
- Modifying summaries in other agent directories
- Using `git add .` / `git add -A` / `git add --all`
- Force pushing

## 6) Agent Execution Rules

### 6.1 Stage Ownership

| Agent | Processes Stage |
|-------|----------------|
| Architect | ARCHITECT |
| Research | RESEARCH |
| Backend | BACKEND |
| Frontend | FRONTEND |
| UIDesigner | FRONTEND (UI phase) |
| QA | QA |
| Security | SECURITY |
| CIReviewer | CI |
| Documentation | DOCS |
| Validator | VALIDATION |

### 6.2 Context Derivation

Agents derive context ONLY from:
1. Ticket JSON (`claimed_by`, `file_paths`, `acceptance_criteria`)
2. Previous stage summary file
3. Codebase files within ticket scope

ReaperOAK does NOT provide context. Context is file-derived.

### 6.3 One Ticket Per Agent

- Each agent instance handles exactly one ticket
- No batching within a single agent
- Parallelism = multiple agent instances on separate tickets

## 7) Failure Recovery

| Failure | Recovery |
|---------|----------|
| Crash after claim, before work | Lease expires → another machine reclaims |
| Crash during work | Uncommitted work lost → reclaim + restart |
| Push conflict on work | Investigate → likely protocol violation |
| Rework count > 3 | Escalate to human |

## 8) Safety Rules (Hard)

Agents MUST NEVER:
- `git add .` / `git add -A` / `git add --all`
- Modify unrelated tickets
- Modify tickets outside their stage
- Modify summaries in other agent directories
- Skip claim commit
- Skip work commit
- Hold multiple ticket claims

Violation of any rule → `PROTOCOL_VIOLATION` event + worker termination.

## 9) Operator Workflow (For example lets consider two operators, Owais and Sujal, working simultaneously on different machines)

### For Owais on Machine A:
```bash
cd /path/to/repo
python .github/tickets.py --sync
python .github/agent-runner.py --agent Backend --operator Owais --list-claimable
python .github/agent-runner.py --agent Backend --operator Owais --claim-only
# ... do agent work via Copilot ...
# ... commit work phase manually with explicit file list ...
```

### For Sujal on Machine B (simultaneously):
```bash
cd /path/to/repo
python .github/tickets.py --sync
python .github/agent-runner.py --agent QA --operator Sujal --list-claimable
python .github/agent-runner.py --agent QA --operator Sujal --claim-only
# ... do agent work via Copilot ...
```

Both operate on the same repository. Git push/pull is the only synchronization.

## 10) Integration with Existing Governance

This protocol extends (does not replace):
- `core_governance.instructions.md` — remains highest authority
- `governance/lifecycle.md` — canonical lifecycle states
- `governance/commit_policy.md` — scoped git rules (now includes two-commit)
- `governance/two_commit_protocol.md` — full two-commit specification
- `governance/worker_policy.md` — worker model
- `governance/event_protocol.md` — event types

New files introduced:
- `.github/tickets.py` — state machine manager
- `.github/agent-runner.py` — distributed execution runner
- `.github/tickets/ticket-schema.json` — ticket JSON schema
- `.github/ticket-state/` — state directories
- `.github/agent-output/` — summary handoff directories
- `.github/governance/two_commit_protocol.md` — protocol spec

End of Distributed Execution Protocol.
