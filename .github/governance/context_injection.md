# Context Injection Architecture

> **GOVERNANCE_VERSION: 9.1.0**
> **Authority:** `.github/instructions/core_governance.instructions.md`
> **Scope:** Role-based injection, deterministic boot sequence, sliding window, file size limits

---

## 1. Role-Based Context Injection Protocol

When spawning a worker, inject ONLY the following — in this order:

### Inject (Mandatory)

| # | Context Item | Source Path | Purpose |
|---|-------------|-------------|---------|
| 1 | SDLC lifecycle rules | `governance/lifecycle.md` | 9-state machine, transitions, DoD |
| 2 | Commit rules | `governance/commit_policy.md` | Per-ticket commits, scoped git |
| 3 | Worker behavior rules | `governance/worker_policy.md` | One-ticket-one-worker, anti-one-shot |
| 4 | Role-specific agent file | `.github/agents/{Agent}.agent.md` | Agent identity, allowed paths, tools |
| 5 | Role-specific chunks | `.github/vibecoding/chunks/{Agent}.agent/` | Detailed protocols, templates (~2 files) |
| 6 | Ticket context | Delegation packet | Acceptance criteria, upstream artifacts, file_paths |
| 7 | Rework context (if rework) | Rejection report | QA/Validator/CI findings from prior attempt |
| 8 | Minimal memory slice | `activeContext.md` (filtered) | Only entries for dependency tickets |

### Do NOT Inject

- Entire TODO tree (only the assigned ticket's L3 task)
- Entire roadmap or vision document
- Full audit history or feedback-log.md
- Full governance directory (only the 3 mandatory policies above)
- Worked examples from ReaperOAK §27-§30
- Other agents' instruction files or chunks
- Unrelated memory bank entries
- Full file contents when excerpts suffice

### Rationale

Minimal injection reduces token waste, prevents hallucination from irrelevant
context, and keeps workers focused on their single assigned ticket.

---

## 2. Deterministic Worker Boot Sequence

Every worker follows this exact 7-step boot sequence. The order is strict
and must not be reordered.

```
Step 1: Load governance/lifecycle.md
        → Worker learns the 9-state machine, transitions, DoD
        
Step 2: Load governance/commit_policy.md
        → Worker learns scoped git rules, commit format
        
Step 3: Load governance/worker_policy.md
        → Worker learns one-ticket-one-worker, anti-one-shot, evidence rules
        
Step 4: Load role-specific .agent.md
        → e.g., .github/agents/Backend.agent.md
        → Worker learns its identity, allowed_read/write_paths, tools
        
Step 5: Load role-specific chunks
        → .github/vibecoding/chunks/{Agent}.agent/
        → Worker gets detailed protocols, templates (~8K tokens)
        
Step 6: Load ticket context (delegation packet)
        → Acceptance criteria, upstream artifacts, file_paths
        → Rework context if applicable (rejection report from prior attempt)
        → Minimal memory slice (only dependency ticket entries)
        
Step 7: Begin execution
        → One worker, one ticket, strict isolation
        → Emit TASK_STARTED event
```

### Boot Validation

At Step 4, the governance files injected into the worker context are checked
for GOVERNANCE_VERSION consistency. If any governance file has a mismatched
version compared to `core_governance.instructions.md`:
- Emit `INSTRUCTION_MISALIGNMENT` event
- Halt worker boot
- ReaperOAK corrects the mismatched governance file, then retries spawn

Agent `.agent.md` files do NOT carry governance version — they reference
governance policies by file path, not by version number.

---

## 3. Sliding Context Window Strategy

For long-running tickets or tickets requiring multiple checkpoints, manage
context to prevent token runaway.

### Working Memory Management

- Maintain working memory externally in the ticket's state management entry
  (workflow-state.json)
- At each checkpoint (state transition), summarize prior reasoning
- Inject the summary instead of raw logs on resume
- Decay stale memory: entries older than 3 state transitions are dropped

### Context Decay Rules

| Age (State Transitions) | Treatment |
|------------------------|-----------|
| Current state | Full context retained |
| 1 transition ago | Summarized to key decisions + artifacts |
| 2 transitions ago | Compressed to one-line summary |
| 3+ transitions ago | Dropped entirely |

### Auto-Summarize Trigger

If total context exceeds `SAFE_CONTEXT_THRESHOLD` (100K tokens):

1. Identify largest context segments (raw logs, full file contents)
2. Summarize: raw logs → bullet points, full files → relevant excerpts
3. Re-inject minimal state
4. Log summarization event with before/after token counts
5. If still > SAFE_CONTEXT_THRESHOLD after summarization → escalate to ReaperOAK

### Prevention

- Never inject full file contents when only a section is relevant
- Never inject full audit history — only the last 3 entries
- Never inject worked examples — they are reference material, not runtime context

---

## 4. File Size Limits

Strict limits prevent context bloat at the source level.

| Limit | Value | Enforcement |
|-------|-------|-------------|
| MAX_GOVERNANCE_FILE | 250 lines | If exceeded: auto-split into modular imports |
| MAX_AGENT_FILE | 300 lines | If exceeded: extract to chunks |
| MAX_CHUNK_FILE | 4000 tokens | If exceeded: split into chunk-01, chunk-02, etc. |
| SAFE_CONTEXT_THRESHOLD | 100K tokens per worker | If exceeded: auto-summarize, re-inject minimal state |
| CRITICAL_CONTEXT_THRESHOLD | 150K tokens per worker | If exceeded: mandatory auto-summarize, escalate if still over |

### Enforcement Mechanism

The Health Sweep (HEALTH checks) periodically verifies file sizes:

1. Scan all governance files — flag any > 250 lines
2. Scan all agent files — flag any > 300 lines
3. Scan all chunk files — flag any > 4000 tokens
4. If violations found → emit `GOVERNANCE_DRIFT` event with `drift_type: OVERSIZED_FILE`
5. Auto-correct: split the oversized file into modular parts

### Import Syntax for Split Files

When a governance file is split, the parent file references child modules:

```markdown
> **Imports:**
> - [Detail Section A](./security_policy_a.md)
> - [Detail Section B](./security_policy_b.md)
```

---

## 5. Context Budget Reference

Target token allocation per worker at boot:

| Category | Target Budget | Source |
|----------|--------------|--------|
| Governance files (lifecycle + commit + worker policies) | ~15K tokens | 3 governance files |
| Agent instructions (agent file + chunks) | ~8K tokens | .agent.md + chunks/ |
| Ticket context (delegation packet + upstream artifacts) | ~10K tokens | Delegation packet |
| Memory slice (relevant memory entries) | ~5K tokens | Filtered activeContext.md |
| **Total target per worker boot** | **~38K tokens** | — |
| SAFE_CONTEXT_THRESHOLD | 100K tokens | Hard warning limit |
| CRITICAL_CONTEXT_THRESHOLD | 150K tokens | Mandatory auto-summarize |

Workers should boot well under the SAFE threshold. If boot context alone
exceeds 60K tokens, review the delegation packet for unnecessary content.

---

## 6. Class B (Background Worker) Injection Profile

Class B workers spawned by the Operational Concurrency Floor (OCF) receive
a **minimal context injection** to conserve tokens and prevent bloat.
Full specification: `governance/concurrency_floor.md` §6.

### Class B Injection Table

| # | Context Item | Include | Rationale |
|---|-------------|---------|----------|
| 1 | `governance/lifecycle.md` | Yes | Required for 9-state awareness |
| 2 | `governance/worker_policy.md` | Yes | One-ticket-one-worker enforcement |
| 3 | `governance/commit_policy.md` | No | BG commit rules in concurrency_floor.md §7 |
| 4 | Agent-specific `.agent.md` | Yes | Role identity and scope |
| 5 | Agent-specific chunks (2 files) | Yes | Domain protocols |
| 6 | Scoped task description | Yes | < 500 tokens — generated by scheduler |
| 7 | Targeted file subset | Yes | Only files being analyzed |
| 8 | Full repository context | **No** | Forbidden for Class B |
| 9 | Extra governance files | **No** | Only lifecycle + worker_policy |
| 10 | Memory bank entries | **No** | BG work is read-only analysis |

### Class B Token Budget

| Category | Budget |
|----------|--------|
| Governance (2 files) | ~10K tokens |
| Agent instructions | ~8K tokens |
| Task description | < 500 tokens |
| Targeted files | ~2K tokens |
| **Total Class B boot** | **≤ 20K tokens** |

Class B workers that exceed 20K tokens at boot are rejected and re-generated
with a more focused file subset.
