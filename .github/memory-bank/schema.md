---
id: memory-bank-schema
version: "2.0"
locked_by: ReaperOAK
immutable: true
---

# Memory Bank Schema & Access Control

## File Schemas

### systemPatterns.md
```yaml
header:
  version: string (semver)
  hash: string (sha256 of body)
  locked_by: "ReaperOAK"
  immutable: true
writers: ["ReaperOAK"]
append_only: true
change_requires: ["decisionLog.md entry", "human approval PR"]
```

### productContext.md
```yaml
entry_format: JSON Lines
fields:
  ts: string (ISO8601)
  author_agent: string (agent id)
  summary: string (max 256 chars)
  payload_hash: string (sha256)
  payload_loc: string (file reference)
writers: ["ProductManager"]
append_only: true
```

### activeContext.md
```yaml
entry_format: JSON Lines
fields:
  ts: string (ISO8601)
  source_agent: string
  source_chunks: list[string] (hashes)
  summary_128: string (max 128 tokens)
  predecessor_hash: string (sha256 of previous entry)
writers: ["all agents"]
append_only: true
compaction: "session end -> compress to decisionLog.md"
```

### decisionLog.md
```yaml
entry_format: JSON Lines
fields:
  id: string (DEC-YYYYMMDD-NNN)
  ts: string (ISO8601)
  proposer_agent: string
  rationale: string
  diff_hash: string (sha256)
  tests_passed: boolean
  predecessor_hash: string (sha256 of previous entry)
writers: ["ReaperOAK"]
append_only: true
immutable: true
```

### progress.md
```yaml
entry_format: Markdown table
fields:
  task_id: string
  status: enum [PENDING, IN_PROGRESS, REVIEW, DONE, BLOCKED]
  agent: string
  milestone_severity: enum [LOW, MEDIUM, HIGH]
  updated_at: string (ISO8601)
writers: ["all agents"]
milestone_done_approvers: ["CIReviewer", "ReaperOAK"]
```

### riskRegister.md
```yaml
entry_format: JSON Lines
fields:
  risk_id: string (RISK-YYYYMMDD-NNN)
  ts: string (ISO8601)
  reporter_agent: string
  threat_type: string (STRIDE category)
  severity: enum [CRITICAL, HIGH, MEDIUM, LOW]
  description: string
  mitigation: string
  status: enum [OPEN, MITIGATED, ACCEPTED, CLOSED]
  predecessor_hash: string (sha256)
writers: ["Security"]
append_only: true
```

## Integrity Rules

- REQUIRE: Every append computes SHA-256 of payload
- REQUIRE: Every append stores predecessor_hash (chain integrity)
- REQUIRE: memory_verify workflow checks chain on every PR
- DENY: Direct edit of systemPatterns.md or decisionLog.md body
- DENY: Deletion of any memory bank entry
- VERIFY: Chain integrity before any agent reads memory
