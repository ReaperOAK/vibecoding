---
name: Terminal Management
applyTo: '**'
description: Named terminal protocol, terminal naming conventions, Copilot Terminal Tools integration, anti-spam rules.
---

# Terminal Management

## 1. Named Terminal Protocol

RULE: All agents MUST use **Copilot Terminal Tools** (`sendCommand`) for terminal operations.
RULE: Every terminal command MUST target a **named terminal** — never spawn anonymous terminals.
RULE: Use `sendCommand` as the primary tool — it creates the terminal if it doesn't exist and reuses it if it does.
PROHIBITED: Spawning anonymous/unnamed terminals via `execute/runInTerminal` when a named terminal exists for that purpose.
PROHIBITED: Creating a new terminal for every command — reuse existing named terminals.

## 2. Terminal Naming Convention

RULE: Terminal names are role-scoped. Each agent uses a fixed set of named terminals.
RULE: Terminal names are lowercase, hyphenated, and descriptive.

### Standard Terminal Names

| Terminal Name | Owner Agents | Purpose |
|---------------|-------------|---------|
| `git` | All agents | Git operations: pull, add, commit, push, rebase |
| `tickets` | ReaperOAK, TODO, Validator | `tickets.py` operations: sync, status, claim, advance, rework |
| `backend` | Backend | Build, test, run backend commands |
| `frontend` | Frontend | Build, test, dev-server, bundler commands |
| `qa` | QA | Test suites, coverage, mutation testing |
| `ci-review` | CI Reviewer | Lint, typecheck, complexity analysis |
| `security` | Security | Security scans, dependency audit, SBOM generation |
| `devops` | DevOps | Terraform, Docker, Kubernetes, infrastructure commands |
| `validator` | Validator | Verification commands (lint, typecheck, test runners) |

RULE: An agent MAY use multiple named terminals (e.g., Backend uses `git` AND `backend`).
RULE: An agent MUST NOT create terminals outside its assigned names.

## 3. Tool Usage

### Primary: `sendCommand`

Use for most operations. Auto-creates the terminal if it doesn't exist:

```
sendCommand(terminalName: "git", command: "git pull --rebase")
sendCommand(terminalName: "backend", command: "npm test")
sendCommand(terminalName: "tickets", command: "python3 .github/tickets.py --sync")
```

### Supporting Tools

| Tool | When to Use |
|------|------------|
| `listTerminals` | Before creating terminals — check what already exists |
| `createTerminal` | Only when you need a terminal with specific shell or working directory |
| `cancelCommand` | To interrupt a long-running or stuck process (Ctrl+C) |
| `deleteTerminal` | Cleanup after ticket completion — remove agent-specific terminals |

### Fallback: `execute/runInTerminal`

RULE: Use `execute/runInTerminal` ONLY when Copilot Terminal Tools are unavailable (tool load failure).
RULE: When falling back, document the reason in the agent summary.

## 4. Lifecycle

### On Agent Start (after boot sequence)
1. Call `listTerminals` to see existing terminals.
2. Reuse any matching named terminal from a previous agent in the same ticket chain.

### During Execution
1. Route commands to the correct named terminal per §2.
2. Git operations always go to the `git` terminal.
3. tickets.py operations always go to the `tickets` terminal.

### On Agent Completion (before work commit)
1. Clean up agent-specific terminals only if no downstream agent needs them.
2. Keep `git` terminal alive — it's shared across the chain.
3. Keep `tickets` terminal alive — ReaperOAK reuses it between dispatches.

## 5. Anti-Spam Rules

PROHIBITED: Creating more than 5 terminals per agent invocation.
PROHIBITED: Creating terminals with auto-generated or numeric names (e.g., `Terminal 1`, `zsh-3`).
PROHIBITED: Leaving orphaned terminals after ticket completion (except `git` and `tickets`).
RULE: If an agent needs a temporary terminal for a one-off command, use `sendCommand` with a named terminal — do not create a disposable terminal.

## 6. Concurrent Agent Safety

RULE: Terminal names do NOT include ticket IDs by default — agents run sequentially within a VS Code instance.
RULE: If multiple agents must run concurrently on the same machine (parallel dispatch), suffix terminals with ticket ID: `backend-{ticket-id}`.
RULE: The `git` and `tickets` terminals are never suffixed — they are singleton shared resources.
