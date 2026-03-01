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
├── ARCHITECTURE.instructions.md      # Full system topology and authority matrix
├── orchestration.rules.instructions.md  # DAG protocol, confidence gates, token tracking
└── security.agentic-guardrails.instructions.md  # Threat models, MCP isolation
TODO/                    # Task decomposition artifacts (managed by TODO Agent)
docs/
├── uiux/                # UI/UX design artifacts (wireframes, mockups, specs)
```

## Architecture

- **Supervisor pattern**: ReaperOAK orchestrates all subagents
- **13 specialized agents**: Architect, Backend, Frontend, QA, Security,
  DevOps, Documentation, Research, ProductManager, CIReviewer, UIDesigner,
  TODO (task decomposition), Validator (SDLC compliance reviewer)
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
