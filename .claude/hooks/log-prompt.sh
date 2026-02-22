#!/bin/bash

# Log user prompt submission for Claude Code sessions
#
# Adapted from .github/hooks/session-logger/log-prompt.sh for Claude Code hooks.

set -euo pipefail

if [[ "${SKIP_LOGGING:-}" == "true" ]]; then
  exit 0
fi

mkdir -p logs/claude-code

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "{\"timestamp\":\"$TIMESTAMP\",\"event\":\"userPromptSubmitted\",\"agent\":\"claude-code\",\"level\":\"${LOG_LEVEL:-INFO}\"}" >> logs/claude-code/prompts.log

exit 0
