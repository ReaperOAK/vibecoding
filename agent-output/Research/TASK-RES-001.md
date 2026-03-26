# TASK-RES-001 — VS Code Agent Plugin Packaging Requirements

## 1. Extension Manifest (package.json)

Requirements for a distributable `.vsix` plugin:
- `engines.vscode`: Minimum `^1.99.0` (agent mode GA in 1.99, hooks in Preview)
- `categories`: `["AI", "Chat"]`
- `extensionDependencies`: `["github.copilot-chat"]`
- `contributes.chatParticipants`: Register agents as chat participants
- `activationEvents`: `["onChatParticipant:*"]` or specific participant IDs
- Agent files (`.agent.md`) are workspace-level, not bundled in vsix — the extension scaffolds them

## 2. Skill and Hook Bundling

- **Skills** (`.github/skills/`): Workspace-level markdown files with YAML frontmatter. Not bundled in vsix.
- **Hooks** (`.github/hooks/`): JSON config + shell scripts. Workspace-level, not bundled.
- **Instructions** (`.github/instructions/`): Pattern-scoped markdown. Workspace-level.
- **Strategy**: Extension uses `postInstall` or activation to scaffold `.github/` structure into workspace
- **Alternative**: Ship as a VS Code workspace template via `yo code` generator

## 3. Marketplace Requirements

- Publisher account on Visual Studio Marketplace
- `vsce package` to build `.vsix`
- `vsce publish` to publish
- README.md with screenshots/animated GIFs
- CHANGELOG.md
- LICENSE file
- Icon (128x128 PNG)
- Repository URL in package.json

## 4. Minimum VS Code Version

- **1.99+**: Agent mode, `.agent.md` files, chat participants
- **1.100+** (estimated): Hooks feature GA, `applyTo` scoping for instructions
- **Recommendation**: Target `^1.99.0` with hooks features behind feature flag

## 5. Recommended Extension Scaffold

```
vibecoding-extension/
├── package.json           # Extension manifest
├── src/
│   └── extension.ts       # Activation: scaffold .github/ on first use
├── templates/
│   ├── agents/            # Agent definition templates
│   ├── instructions/      # Instruction file templates
│   ├── hooks/             # Hook config + script templates
│   ├── skills/            # Skill templates
│   └── prompts/           # Prompt file templates
├── README.md
├── CHANGELOG.md
├── LICENSE
└── icon.png
```

## 6. Key Decisions

| Decision | Rationale |
|----------|-----------|
| Workspace-level scaffolding | Agent/hook files must be in `.github/` per VS Code spec |
| Template-based | Each project customizes agents for their stack |
| No runtime code bundling | Agents are markdown-based, no JS runtime needed |
| `yo code` generator optional | Alternative to vsix for teams that want template-only |

## Confidence: HIGH
