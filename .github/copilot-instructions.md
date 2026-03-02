# Project Context

This repository implements a **multi-agent vibecoding system** — a hardened,
AI-first development infrastructure where specialized AI agents collaborate
under a supervisor orchestrator (ReaperOAK).

## Repository Structure

```
.github/
├── agents/              # 14 agent definitions (*.agent.md) — includes UIDesigner, TODO, Validator
├── memory-bank/         # Persistent shared state (9 files + schema)
│                        # Includes workflow-state.json, artifacts-manifest.json, feedback-log.md
├── proposals/           # Self-improvement proposals (PROP-*.md)
├── tasks/               # Delegation schemas, claim schemas, merge protocol
├── tickets/             # Ticket JSON files + ticket-schema.json
├── ticket-state/        # File-based state machine (11 stage directories)
│   ├── READY/           # Tickets awaiting assignment
│   ├── ARCHITECT/       # Architecture stage
│   ├── RESEARCH/        # Research stage
│   ├── BACKEND/         # Backend implementation stage
│   ├── FRONTEND/        # Frontend implementation stage
│   ├── QA/              # QA review stage
│   ├── SECURITY/        # Security review stage
│   ├── CI/              # CI review stage
│   ├── DOCS/            # Documentation stage
│   ├── VALIDATION/      # Validator stage
│   └── DONE/            # Completed tickets
├── agent-output/        # Summary handoff chain (14 agent directories)
│   └── {AgentName}/     # Each agent writes {ticket-id}.md summaries here
├── vibecoding/          # Context index, catalog, chunks, specs
│   ├── index.json       # Master file index (57+ entries with hashes)
│   ├── catalog.yml      # Semantic tag → chunk mapping (15 domains)
│   └── chunks/          # Token-budgeted YAML chunks (35 dirs, ~93 files)
├── guardian/             # Circuit breaker (STOP_ALL), loop detection rules
├── locks/               # File lock schema
├── sandbox/             # Tool ACLs per agent
├── observability/       # Agent trace event schema
├── workflows/           # CI: task runner, sandbox merge, memory verify
├── hooks/               # Governance audit, session logger, auto-commit
├── tickets.py           # Distributed ticket state machine manager CLI
├── agent-runner.py      # Two-commit protocol execution runner CLI
├── ARCHITECTURE.instructions.md      # Full system topology and authority matrix
├── orchestration.rules.instructions.md  # DAG protocol, confidence gates, token tracking
├── distributed-execution.instructions.md  # Distributed multi-machine protocol
└── security.agentic-guardrails.instructions.md  # Threat models, MCP isolation
TODO/                    # Task decomposition artifacts (managed by TODO Agent)
docs/
├── uiux/                # UI/UX design artifacts (wireframes, mockups, specs)
```

## Architecture

- **Supervisor pattern**: ReaperOAK orchestrates all subagents
- **Distributed execution**: Multiple operators (Owais, Sujal) on multiple machines
- **Git-native locking**: Two-commit protocol (claim + work) with push-based distributed locks
- **File-based state machine**: Ticket state = directory location under `.github/ticket-state/`
- **13 specialized agents**: Architect, Backend, Frontend, QA, Security,
  DevOps, Documentation, Research, ProductManager, CIReviewer, UIDesigner,
  TODO (task decomposition), Validator (SDLC compliance reviewer)
- **Summary handoff chain**: Context flows via `.github/agent-output/{Agent}/{ticket-id}.md`
- **Memory bank**: Git-tracked markdown files for cross-session persistence
- **Shared context layer**: Pipeline state, artifact tracking, feedback log
- **Self-improvement loop**: Agents propose infrastructure improvements
- **Chunk system**: All instruction content pre-chunked to ≤4000 tokens;
  original instruction files removed — chunks in `vibecoding/chunks/` are the
  sole source of truth

## Key Conventions

- All infrastructure lives inside `.github/`
- Agent files use canonical YAML frontmatter schemas
- Domain guidance is stored as chunks, loaded on demand via `catalog.yml`
- Memory bank files are append-only with ownership rules
- Destructive operations require human approval
- Distributed execution uses `tickets.py` for state management and `agent-runner.py` for two-commit protocol
- Every agent commits twice per stage: Commit 1 (CLAIM) then Commit 2 (WORK)
