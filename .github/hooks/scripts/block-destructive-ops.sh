#!/usr/bin/env bash
# Hook: block-destructive-ops.sh
# Lifecycle: PreToolUse (toolNames: run_in_terminal, execute/runInTerminal)
# Purpose: Block destructive terminal commands that require human approval
# Exit 0 = allow, Exit 1 = deny, Exit 2 = ask for human approval

set -euo pipefail

COMMAND="${HOOK_TOOL_INPUT:-}"

if [[ -z "$COMMAND" ]]; then
    COMMAND=$(cat 2>/dev/null || true)
fi

# Patterns that are always denied (catastrophic)
DENY_PATTERNS=(
    'rm\s+-rf\s+/'
    'rm\s+-rf\s+\*'
    'rm\s+-rf\s+\.'
    'git\s+reset\s+--hard'
    'git\s+push\s+--force'
    'git\s+push\s+-f\b'
    'git\s+branch\s+-D'
    'DROP\s+DATABASE'
    'DROP\s+TABLE'
    'TRUNCATE\s+TABLE'
    'DELETE\s+FROM\s+\w+\s*;?\s*$'
)

for pattern in "${DENY_PATTERNS[@]}"; do
    if echo "$COMMAND" | grep -qEi "$pattern"; then
        echo "DESTRUCTIVE COMMAND BLOCKED: Prohibited operation detected." >&2
        echo "  Matched pattern: $pattern" >&2
        echo "  Command: $(echo "$COMMAND" | head -c 200)" >&2
        echo "  This operation requires explicit human approval." >&2
        exit 1
    fi
done

# Patterns that require human approval (ask)
ASK_PATTERNS=(
    'DROP\s+'
    'DELETE\s+FROM'
    'ALTER\s+TABLE.*DROP'
    'git\s+rebase'
    'npm\s+publish'
    'docker\s+rm'
    'docker\s+system\s+prune'
)

for pattern in "${ASK_PATTERNS[@]}"; do
    if echo "$COMMAND" | grep -qEi "$pattern"; then
        echo "APPROVAL REQUIRED: This command may be destructive." >&2
        echo "  Matched pattern: $pattern" >&2
        echo "  Command: $(echo "$COMMAND" | head -c 200)" >&2
        echo "  Please confirm you want to proceed." >&2
        exit 2
    fi
done

# Command is safe
exit 0
