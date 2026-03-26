# CLAUDE.md

Project conventions for Claude Code, Cursor, Windsurf, and other AI coding tools.

## Project Identity

Multi-agent vibecoding system — a ticket-driven AI development infrastructure
where specialized agents collaborate under a stateless dispatcher (Ticketer).

## Repository Structure

```
.github/
  agents/              # 15 agent definitions (*.agent.md)
  instructions/        # 6 canonical instruction files (sole authority)
  memory-bank/         # Persistent shared state (append-only)
  tickets/             # Ticket JSON files
  ticket-state/        # File-based state machine (stage directories)
  agent-output/        # Summary handoff chain
  vibecoding/          # Context chunks and catalog
  guardian/            # Circuit breaker (STOP_ALL)
tickets.py             # Distributed ticket state machine manager
TODO/                  # Task decomposition artifacts (L0→L1→L2→L3)
```

## Tech Stack

- **Language**: TypeScript (strict mode)
- **Framework**: Node.js with Express/Fastify
- **Database**: MongoDB/PostgreSQL
- **Testing**: Jest (TDD red-green-refactor)
- **Linting**: ESLint + Prettier
- **CI/CD**: GitHub Actions
- **Containerization**: Docker

## Coding Standards

- SOLID principles mandatory
- No `any` types — explicit typing required
- Structured logging with JSON output (no `console.log`)
- Repository pattern for data access
- Dependency injection via constructor
- Domain errors with typed exceptions
- 80%+ test coverage for new code
- No TODO comments in committed code
- No unhandled promises

## Key Conventions

- All infrastructure lives inside `.github/`
- 6 instruction files in `.github/instructions/` are the sole source of system rules
- Agent files define: role, stage, scope, forbidden actions, tool loadout
- Memory bank files are append-only with ownership rules
- Destructive operations require human approval
- `tickets.py` handles dependency resolution — agents never compute dependencies
- Git scoped commits only — never use `git add .` or `git add -A`

## Agent System

15 agents with defined SDLC stages:
- **CTO**: Strategic orchestrator (pre-SDLC)
- **Ticketer**: Stateless dispatcher
- **Research, ProductManager, Architect**: Planning pipeline
- **Backend, Frontend, DevOps, UIDesigner**: Implementation
- **QA, Security, CIReviewer**: Review chain
- **Documentation, Validator**: Post-review

## Detailed Rules

For complete system rules, see:
- `.github/instructions/core.instructions.md` — Identity, halt gate, boot sequence, security
- `.github/instructions/sdlc.instructions.md` — Stage lifecycle, Definition of Done
- `.github/instructions/ticket-system.instructions.md` — State machine, dependencies
- `.github/instructions/git-protocol.instructions.md` — Commit protocol, scoped git
- `.github/instructions/agent-behavior.instructions.md` — Worker model, scope enforcement
