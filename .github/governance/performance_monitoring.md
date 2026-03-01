# Performance Monitoring

> **GOVERNANCE_VERSION: 9.1.0**
> **Authority:** `.github/instructions/core_governance.instructions.md`
> **Scope:** Context size logging, token usage, drift correlation, auto-summarize protocol

---

## 1. Context Size Logging

Log the total tokens injected per worker at two points:

### At Boot

When a worker is spawned, log:

```markdown
### Context Injection — {worker_id}
- **Ticket:** {ticket_id}
- **Role:** {pool_role}
- **Governance tokens:** {count}
- **Agent instruction tokens:** {count}
- **Ticket context tokens:** {count}
- **Memory slice tokens:** {count}
- **Total boot tokens:** {total}
- **Timestamp:** {ISO8601}
```

### At Each Checkpoint (State Transition)

When a ticket transitions state, log the cumulative context:

```markdown
### Context Checkpoint — {worker_id} — {state}
- **Ticket:** {ticket_id}
- **Cumulative tokens:** {total}
- **Delta since last checkpoint:** {delta}
- **Timestamp:** {ISO8601}
```

All context size logs are appended to `.github/memory-bank/feedback-log.md`.

---

## 2. Token Usage Monitoring

Track cumulative tokens consumed per ticket across its full lifecycle:

| Metric | Description | Logged At |
|--------|-------------|-----------|
| Boot tokens | Total tokens at worker spawn | LOCKED → IMPLEMENTING |
| Implementation tokens | Tokens consumed during IMPLEMENTING | IMPLEMENTING → QA_REVIEW |
| Post-chain tokens | Tokens consumed during QA/Validator/Doc/CI | QA_REVIEW → COMMIT |
| Total lifecycle tokens | Sum of all above | COMMIT → DONE |

### Per-Ticket Token Summary

Logged at DONE state:

```markdown
### Token Summary — {ticket_id}
- **Boot:** {count}
- **Implementation:** {count}
- **Post-chain:** {count}
- **Total:** {count}
- **Rework cycles:** {rework_count}
- **Timestamp:** {ISO8601}
```

---

## 3. Drift Correlation Metrics

Correlate `PROTOCOL_VIOLATION` frequency with context injection size to
identify whether oversized context causes procedural drift.

### Correlation Data Points

| Data Point | Source | Purpose |
|-----------|--------|---------|
| Violation count per ticket | Event queue (PROTOCOL_VIOLATION events) | Drift frequency |
| Boot context size per ticket | Context size log | Injection bloat detection |
| Rework count per ticket | Ticket metadata | Quality correlation |
| Time in IMPLEMENTING per ticket | State timestamps | Efficiency metric |

### Analysis Rules

- If tickets with boot context > 60K tokens have 2x+ violation rate → flag
  context injection as a contributing factor
- If rework_count correlates with boot context size → tighten injection policy
- Log correlation findings in feedback-log.md monthly

---

## 4. Oversized Injection Warnings

### Warning Thresholds

| Threshold | Level | Action |
|-----------|-------|--------|
| < 38K tokens | NOMINAL | No action — within target budget |
| 38K–60K tokens | ADVISORY | Log advisory, no blocking |
| 60K–100K tokens | WARNING | Log warning, review delegation packet |
| 100K–150K tokens (SAFE_CONTEXT_THRESHOLD) | ALERT | Emit warning event, auto-summarize triggered |
| > 150K tokens (CRITICAL_CONTEXT_THRESHOLD) | CRITICAL | Mandatory auto-summarize, escalate if still over |

### Warning Event Format

```markdown
**Event:** OVERSIZED_CONTEXT_WARNING
**Worker:** {worker_id}
**Ticket:** {ticket_id}
**Context Size:** {token_count} tokens
**Threshold:** {threshold_name}
**Recommended Action:** {action}
**Timestamp:** {ISO8601}
```

---

## 5. Context Budget per Worker

Reference budget for optimal worker performance:

| Category | Target Budget | Notes |
|----------|--------------|-------|
| Governance files | ~15K tokens | lifecycle.md + commit_policy.md + worker_policy.md |
| Agent instructions | ~8K tokens | .agent.md file + vibecoding chunks |
| Ticket context | ~10K tokens | Delegation packet + upstream artifacts |
| Memory slice | ~5K tokens | Relevant activeContext.md entries only |
| **Total target** | **~38K tokens** | Optimal for focused execution |
| SAFE_CONTEXT_THRESHOLD | 100K tokens | Auto-summarize trigger |
| CRITICAL_CONTEXT_THRESHOLD | 150K tokens | Mandatory auto-summarize |

---

## 6. Auto-Summarize Protocol

Triggered when worker context exceeds SAFE_CONTEXT_THRESHOLD (100K tokens).

### Summarization Steps

1. **Identify** largest context segments (raw logs, full file contents, verbose history)
2. **Summarize** raw logs → bullet-point key decisions and outcomes
3. **Summarize** full file contents → relevant excerpts with line references
4. **Summarize** verbose history → last 3 entries only
5. **Re-inject** minimal state into worker context
6. **Log** summarization event:

```markdown
### Auto-Summarize — {worker_id}
- **Ticket:** {ticket_id}
- **Before:** {token_count_before} tokens
- **After:** {token_count_after} tokens
- **Reduction:** {percentage}%
- **Segments summarized:** {list}
- **Timestamp:** {ISO8601}
```

### Post-Summarize Validation

- If context still > SAFE_CONTEXT_THRESHOLD after summarization → escalate
  to ReaperOAK for manual review
- If context > CRITICAL_CONTEXT_THRESHOLD → force-terminate worker, create
  new worker with aggressively minimal context

---

## 7. Health Dashboard Integration

Context performance metrics are logged to `.github/memory-bank/feedback-log.md`.

### Per-Scheduling-Interval Aggregates

```markdown
### Performance Metrics — {ISO8601}
- **Workers active:** {count}
- **Avg boot context:** {tokens} tokens
- **Max boot context:** {tokens} tokens ({worker_id})
- **Auto-summarize events:** {count}
- **Oversized warnings:** {count}
- **PROTOCOL_VIOLATION count:** {count}
- **Drift correlation flag:** {yes/no}
```

### Retention

- Keep per-ticket token summaries for 30 days
- Keep aggregate metrics indefinitely
- Keep auto-summarize logs for 30 days

---

## 8. Class B (Background Worker) Metrics

Background workers spawned by the Operational Concurrency Floor (OCF) are
tracked separately from Class A workers. Full OCF spec:
`governance/concurrency_floor.md`.

### Per-Scheduling-Interval BG Metrics

```markdown
### OCF Metrics — {ISO8601}
- **Class A active:** {count}
- **Class B active:** {count}
- **Total active:** {count}
- **MIN_ACTIVE_WORKERS:** 10
- **Floor deficit:** {count}  (0 = satisfied)
- **BG preemptions this interval:** {count}
- **BG findings this interval:** {count}
- **BG token budget used:** {tokens} / {MAX_BG_TOKENS}
```

### BG Token Budget

| Category | Budget |
|----------|--------|
| Class B boot context (per worker) | ≤ 20K tokens |
| Class B total (all BG workers) | ≤ 80K tokens per interval |

### Throttle Monitoring

| Condition | Metric | Action |
|-----------|--------|--------|
| Primary backlog > 20 | `classA_backlog_count` | Suspend all Class B |
| Token usage > 80% | `session_token_pct` | Reduce BG spawn rate 50% |
| Token usage > 95% | `session_token_pct` | Suspend all Class B |
| Class A rework > 30% | `classA_rework_rate` | Suspend Class B |
