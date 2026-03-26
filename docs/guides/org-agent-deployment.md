# Organization-Level Agent Deployment Guide

## Prerequisites

- VS Code **1.100+** (Insiders recommended for latest agent features)
- GitHub Copilot extension with **agent mode** enabled
- Python 3.10+ (for `tickets.py` state machine)
- Git 2.40+ (for distributed locking protocol)

## 1. Enable Organization-Level Agent Settings

### GitHub Organization Settings

1. Navigate to **Organization Settings > Copilot > Policies**
2. Enable **"Allow Copilot Chat agents from .github/agents"**
3. Set **"Agent file locations"** to `.github/agents`
4. Enable **"Include referenced instructions"** for auto-loading

### VS Code Settings (Organization Policy)

Apply via MDM or `.vscode/settings.json` in shared repos:

```json
{
  "chat.agentFilesLocations": [{ "source": ".github/agents" }],
  "chat.promptFilesLocations": [{ "source": ".github/prompts" }],
  "chat.skillFilesLocations": [{ "source": ".github/skills" }],
  "chat.hookFilesLocations": [{ "source": ".github/hooks" }],
  "chat.instructionsFilesLocations": [{ "source": ".github/instructions" }],
  "chat.includeReferencedInstructions": true
}
```

## 2. Agent Distribution Workflow

### Initial Setup

```bash
# Clone the vibecoding system
git clone <repo-url>
cd vibecoding

# Verify agent infrastructure
ls .github/agents/    # 15 agent files
ls .github/skills/    # 20 skill directories
ls .github/hooks/     # Hook configurations

# Initialize ticket state
python3 tickets.py --sync
python3 tickets.py --status
```

### Multi-Operator Workflow

Multiple operators can work simultaneously on the same repository:

```bash
# Before starting work
git pull --rebase
python3 tickets.py --sync

# Ticketer dispatches agents
# Each claim is a git push (distributed lock)
# Push failure = another operator claimed first
```

### Adding Agents to a New Project

1. Copy `.github/` directory structure to target repo
2. Customize agent tool loadouts for project stack
3. Update `.vscode/settings.json` with file locations
4. Run `python3 tickets.py --validate` to verify integrity

## 3. Agent Architecture

| Agent Type | Count | Purpose |
|-----------|-------|---------|
| Dispatcher | 1 | Ticketer — stateless ticket routing |
| Orchestrator | 1 | CTO — pre-SDLC planning |
| Implementing | 5 | Backend, Frontend, DevOps, UIDesigner, Architect |
| Review | 5 | QA, Security, CIReviewer, Documentation, Validator |
| Planning | 3 | Research, ProductManager, TODO |

### SDLC Pipeline

```
READY → RESEARCH → PM → ARCHITECT → DevOps → BACKEND → UIDesigner → FRONTEND → QA → SECURITY → CI → DOCS → VALIDATION → DONE
```

## 4. Version Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| VS Code | 1.100.0 | Latest Insiders |
| GitHub Copilot | 0.30.0 | Latest |
| Python | 3.10 | 3.12+ |
| Git | 2.40 | 2.45+ |
| Node.js | 18.x | 22.x |

## 5. Troubleshooting

### Agents Not Appearing in Chat

- Verify `chat.agentFilesLocations` points to `.github/agents`
- Check agent files have valid YAML frontmatter with `name:` field
- Ensure `user-invocable: true` for agents you want to invoke directly
- Reload VS Code window after adding new agents

### Handoffs Not Working

- Verify `handoffs:` section in agent frontmatter is valid YAML
- Each handoff needs: `label`, `agent`, `prompt`, `send: false`
- Agent name in handoff must match an existing agent's `name:` field

### Ticket State Issues

```bash
# Full integrity check
python3 tickets.py --validate

# Release expired claims
python3 tickets.py --release-expired

# Sync dependencies
python3 tickets.py --sync
```

### MCP Server Not Connecting

- Verify `.vscode/mcp.json` exists with correct server path
- Check Python is available: `which python3`
- Test server manually: `echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python3 .github/mcp-servers/ticket-server/server.py`

### Git Push Conflicts

- This is expected behavior — another operator claimed the ticket first
- Run `git pull --rebase` and claim a different ticket
- Never force push — it breaks the distributed locking protocol
