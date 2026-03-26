# ADR: VS Code Agent Plugin Extension Architecture

## Status
Proposed

## Context
Based on TASK-RES-001 research findings, the vibecoding multi-agent system should be packagable as a VS Code extension for distribution via the marketplace.

## Decision

### Extension Entry Point

```typescript
// src/extension.ts
export function activate(context: vscode.ExtensionContext) {
    // 1. Scaffold .github/ structure on first activation
    // 2. Register commands for manual scaffold refresh
    // 3. No chat participant registration needed — .agent.md files handle this
}
```

**Activation Events**: `["onStartupFinished"]` — lightweight, non-blocking

### Agent Registration
- **Strategy**: Workspace-level `.agent.md` files (NOT extension-bundled)
- **Rationale**: Agents must be customizable per project (different stacks, conventions)
- **Scaffold**: Extension copies template agents to `.github/agents/` on first run
- **Update**: `vibecoding.refreshAgents` command re-scaffolds without overwriting user changes

### Skill Discovery
- **Strategy**: Workspace-level `.github/skills/` with `SKILL.md` files
- **Discovery**: VS Code auto-discovers skills in configured `chat.skillFilesLocations`
- **Scaffold**: Extension creates initial skills from templates

### Hook Registration
- **Strategy**: Workspace-level `.github/hooks/` JSON + shell scripts
- **Discovery**: VS Code reads `chat.hookFilesLocations` from `.vscode/settings.json`
- **Scaffold**: Extension creates policy-enforcement.json and scripts

### Settings Contribution Points

```json
{
  "contributes": {
    "configuration": {
      "title": "Vibecoding",
      "properties": {
        "vibecoding.autoScaffold": {
          "type": "boolean",
          "default": true,
          "description": "Auto-scaffold .github/ structure on new workspaces"
        },
        "vibecoding.enableHooks": {
          "type": "boolean",
          "default": false,
          "description": "Enable agent hooks (requires VS Code hooks Preview feature)"
        },
        "vibecoding.ticketSyncOnStart": {
          "type": "boolean",
          "default": true,
          "description": "Auto-sync tickets on session start"
        }
      }
    },
    "commands": [
      {
        "command": "vibecoding.scaffold",
        "title": "Vibecoding: Scaffold Agent Infrastructure"
      },
      {
        "command": "vibecoding.refreshAgents",
        "title": "Vibecoding: Refresh Agent Templates"
      },
      {
        "command": "vibecoding.syncTickets",
        "title": "Vibecoding: Sync Tickets"
      }
    ]
  }
}
```

### Build Pipeline

```yaml
# .github/workflows/build-extension.yml
steps:
  - uses: actions/setup-node@v4
  - run: npm ci
  - run: npm run compile
  - run: npx vsce package --out vibecoding.vsix
  - uses: actions/upload-artifact@v4
    with:
      path: vibecoding.vsix
```

### File Structure

```
vibecoding-extension/
├── package.json
├── tsconfig.json
├── src/
│   ├── extension.ts        # Entry point
│   ├── scaffolder.ts       # .github/ structure scaffolding
│   └── commands.ts         # Registered commands
├── templates/
│   ├── agents/             # 15 agent templates
│   ├── instructions/       # 7 instruction templates
│   ├── hooks/              # Hook config + scripts
│   ├── skills/             # Skill templates
│   ├── prompts/            # Prompt file templates
│   └── settings.json       # .vscode/settings.json template
├── README.md
├── CHANGELOG.md
├── LICENSE
└── icon.png
```

## Consequences

**Positive:**
- One-click installation of entire vibecoding infrastructure
- Marketplace distribution enables rapid adoption
- Template-based approach allows per-project customization

**Negative:**
- Maintenance of two codebases (system + extension)
- Template drift if system evolves faster than extension templates

## References
- [TASK-RES-001 Research](../../agent-output/Research/TASK-RES-001.md)
- [MCP Ticket Server ADR](../adr/mcp-ticket-server.md)
