# Hook Scripts

This directory contains shell scripts invoked by VS Code agent lifecycle hooks defined in `../*.json`.

## Architecture

```
.github/hooks/
├── policy-enforcement.json    # Hook definitions (SessionStart, PreToolUse, etc.)
└── scripts/
    ├── README.md              # This file
    ├── check-guardian.sh       # STOP_ALL circuit breaker check (SessionStart)
    └── check-git-policy.sh    # Block `git add .` / `-A` / `--all` (PreToolUse)
```

## Hook Lifecycle Events

| Event | When It Fires | Purpose |
|-------|---------------|---------|
| `SessionStart` | Agent session begins | Check guardian, sync tickets |
| `PreToolUse` | Before any tool call | Block prohibited commands |
| `PostToolUse` | After any tool call | Lint checks, validation |
| `SubagentStart` | Before subagent launch | Validate claim protocol |
| `SubagentStop` | After subagent completes | Memory gate enforcement |
| `Stop` | Agent session ends | Evidence rule verification |

## Status

Hooks are currently **disabled** (`"enabled": false`) because the VS Code agent hooks feature is in Preview. Enable them when the feature reaches stable.

## Adding New Hooks

1. Create a new shell script in this directory
2. Add a hook entry in `../policy-enforcement.json` under the appropriate lifecycle event
3. Set `"enabled": false` initially and test manually before enabling

## Script Contract

Each script must:
- Exit `0` on success (allow the action)
- Exit non-zero on policy violation (block the action)
- Write violation details to stderr for agent context
