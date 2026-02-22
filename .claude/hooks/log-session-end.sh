#!/bin/bash

# Log Claude Code session end event
#
# Adapted from .github/hooks/session-logger/log-session-end.sh for Claude Code hooks.

set -euo pipefail

if [[ "${SKIP_LOGGING:-}" == "true" ]]; then
  exit 0
fi

mkdir -p logs/claude-code

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "{\"timestamp\":\"$TIMESTAMP\",\"event\":\"sessionEnd\",\"agent\":\"claude-code\"}" >> logs/claude-code/session.log

echo "Session end logged"
exit 0
