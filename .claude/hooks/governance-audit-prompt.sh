#!/bin/bash

# Governance Audit: Scan user prompts for threat signals before Claude Code processing
#
# Adapted from .github/hooks/governance-audit/audit-prompt.sh for Claude Code hooks.
# Claude Code pipes the user prompt via stdin.
#
# Environment variables:
#   GOVERNANCE_LEVEL - "open", "standard", "strict", "locked" (default: standard)
#   BLOCK_ON_THREAT  - "true" to exit non-zero on threats (default: false)
#   SKIP_GOVERNANCE_AUDIT - "true" to disable (default: unset)

set -euo pipefail

if [[ "${SKIP_GOVERNANCE_AUDIT:-}" == "true" ]]; then
  exit 0
fi

PROMPT=$(cat)

mkdir -p logs/claude-code/governance

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
LEVEL="${GOVERNANCE_LEVEL:-standard}"
BLOCK="${BLOCK_ON_THREAT:-false}"
LOG_FILE="logs/claude-code/governance/audit.log"

# Threat detection patterns organized by category
THREATS_FOUND=()

check_pattern() {
  local pattern="$1"
  local category="$2"
  local severity="$3"
  local description="$4"

  if echo "$PROMPT" | grep -qiE "$pattern"; then
    THREATS_FOUND+=("$category	$severity	$description")
  fi
}

# Data exfiltration signals
check_pattern "send\s+(all|every|entire)\s+\w+\s+to\s+" "data_exfiltration" "0.8" "Bulk data transfer"
check_pattern "export\s+.*\s+to\s+(external|outside|third[_-]?party)" "data_exfiltration" "0.9" "External export"
check_pattern "curl\s+.*\s+-d\s+" "data_exfiltration" "0.7" "HTTP POST with data"
check_pattern "upload\s+.*\s+(credentials|secrets|keys)" "data_exfiltration" "0.95" "Credential upload"

# Privilege escalation signals
check_pattern "(sudo|as\s+root|admin\s+access|runas\s+/user)" "privilege_escalation" "0.8" "Elevated privileges"
check_pattern "chmod\s+777" "privilege_escalation" "0.9" "World-writable permissions"
check_pattern "add\s+.*\s+(sudoers|administrators)" "privilege_escalation" "0.95" "Adding admin access"

# System destruction signals
check_pattern "(rm\s+-rf\s+/|del\s+/[sq]|format\s+c:)" "system_destruction" "0.95" "Destructive command"
check_pattern "(drop\s+database|truncate\s+table|delete\s+from\s+\w+\s*(;|\s*$))" "system_destruction" "0.9" "Database destruction"
check_pattern "wipe\s+(all|entire|every)" "system_destruction" "0.9" "Mass deletion"

# Prompt injection signals
check_pattern "ignore\s+(previous|above|all)\s+(instructions?|rules?|prompts?)" "prompt_injection" "0.9" "Instruction override"
check_pattern "you\s+are\s+now\s+(a|an)\s+(assistant|ai|bot|system|expert|language\s+model)\b" "prompt_injection" "0.7" "Role reassignment"
check_pattern "(^|\n)\s*system\s*:\s*you\s+are" "prompt_injection" "0.6" "System prompt injection"

# Credential exposure signals
check_pattern "(api[_-]?key|secret[_-]?key|password|token)\s*[:=]\s*['\"]?\w{8,}" "credential_exposure" "0.9" "Possible hardcoded credential"
check_pattern "(aws_access_key|AKIA[0-9A-Z]{16})" "credential_exposure" "0.95" "AWS key exposure"

# Agent manipulation signals
check_pattern "bypass\s+(security|guardrail|safety|restriction)" "agent_manipulation" "0.95" "Guardrail bypass attempt"
check_pattern "disable\s+(logging|audit|monitoring)" "agent_manipulation" "0.9" "Observability suppression"
check_pattern "act\s+as\s+(root|admin|superuser)" "agent_manipulation" "0.85" "Privilege assumption"

# Supply chain signals
check_pattern "install\s+.*\s+--force\s+--no-verify" "supply_chain" "0.8" "Forced unverified install"
check_pattern "npm\s+install\s+.*\s+--ignore-scripts" "supply_chain" "0.6" "Script bypass install"

# Log and report
if [[ ${#THREATS_FOUND[@]} -gt 0 ]]; then
  MAX_SEVERITY="0.0"
  LOG_ENTRY="{\"timestamp\":\"$TIMESTAMP\",\"event\":\"threat_detected\",\"governance_level\":\"$LEVEL\",\"threat_count\":${#THREATS_FOUND[@]},\"agent\":\"claude-code\",\"threats\":["
  FIRST=true
  for threat in "${THREATS_FOUND[@]}"; do
    IFS=$'\t' read -r category severity description <<< "$threat"
    if [[ "$FIRST" != "true" ]]; then
      LOG_ENTRY+=","
    fi
    FIRST=false
    LOG_ENTRY+="{\"category\":\"$category\",\"severity\":$severity,\"description\":\"$description\"}"
    if command -v bc &>/dev/null; then
      if (( $(echo "$severity > $MAX_SEVERITY" | bc -l 2>/dev/null || echo 0) )); then
        MAX_SEVERITY="$severity"
      fi
    fi
  done
  LOG_ENTRY+="]}"
  echo "$LOG_ENTRY" >> "$LOG_FILE"

  echo "WARNING: Governance: ${#THREATS_FOUND[@]} threat signal(s) detected (max severity: $MAX_SEVERITY)" >&2
  for threat in "${THREATS_FOUND[@]}"; do
    IFS=$'\t' read -r category severity description <<< "$threat"
    echo "  [$category] $description (severity: $severity)" >&2
  done

  if [[ "$BLOCK" == "true" ]] || [[ "$LEVEL" == "strict" ]] || [[ "$LEVEL" == "locked" ]]; then
    echo "BLOCKED: Prompt blocked by governance policy (level: $LEVEL)" >&2
    exit 1
  fi
else
  echo "{\"timestamp\":\"$TIMESTAMP\",\"event\":\"prompt_scanned\",\"governance_level\":\"$LEVEL\",\"agent\":\"claude-code\",\"status\":\"clean\"}" >> "$LOG_FILE"
fi

exit 0
