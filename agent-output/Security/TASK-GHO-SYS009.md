# TASK-GHO-SYS009 — Security Review

## Verdict: PASS

**Confidence:** HIGH

## Change Summary

Removed phantom tool ID `execute/runInTerminal` from `toolNames` array in `.github/hooks/policy-enforcement.json`. Retained only `run_in_terminal`, which is the actual VS Code Copilot tool ID. This is a security **improvement** — fixing a broken policy enforcement mapping.

## STRIDE Threat Model

**Trust boundary:** LLM Agent → VS Code Hook System → Shell Script → git CLI

| Category | Threat | Score | Mitigation |
|----------|--------|-------|------------|
| Spoofing | Agent sends command via unmonitored tool | L:3 × I:3 = 9 (LOW) | Hook targets correct tool ID; see advisory below |
| Tampering | Agent modifies hook config to disable enforcement | L:2 × I:4 = 8 (LOW) | File under git VCS; changes require commit review |
| Repudiation | Agent denies prohibited command attempt | L:2 × I:2 = 4 (LOW) | Hook outputs clear stderr violation message |
| Info Disclosure | Error messages leak sensitive data | L:1 × I:1 = 1 (LOW) | Messages contain only policy rule text |
| DoS | Hook causes terminal delay | L:1 × I:1 = 1 (LOW) | Grep-based check; near-zero latency |
| Elevation | Agent bypasses git-add restriction | L:2 × I:3 = 6 (LOW) | Deterministic regex enforcement via shell |

**No Critical or High threats identified.** All scores < 10 (LOW).

## OWASP Top 10 Checklist

| # | Risk | Result | Notes |
|---|------|--------|-------|
| A01 | Broken Access Control | N/A | No access control in scope |
| A02 | Cryptographic Failures | N/A | No cryptographic operations |
| A03 | Injection | PASS | Shell script uses `set -euo pipefail`; regex matching only |
| A04 | Insecure Design | PASS | Deterministic hook enforcement; correct tool ID |
| A05 | Security Misconfiguration | PASS | This change fixes a misconfiguration |
| A06 | Vulnerable Components | N/A | No dependencies introduced |
| A07 | Auth Failures | N/A | No authentication in scope |
| A08 | Data Integrity | PASS | JSON schema link present; config under VCS |
| A09 | Logging Failures | PASS | Violation messages written to stderr |
| A10 | SSRF | N/A | No network calls |

## LLM Top 10

N/A — No AI/agent features modified. Hook is a deterministic shell script.

## Dependency Audit / SBOM

N/A — No dependencies introduced. Infrastructure JSON configuration change only.

## Secret Scanning

PASS — No secrets, tokens, keys, or credentials in modified file.

## SARIF Findings

```json
{
  "version": "2.1.0",
  "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
  "runs": [
    {
      "tool": {
        "driver": {
          "name": "SecurityAgent",
          "version": "1.0.0",
          "rules": [
            {
              "id": "SEC-ADVISORY-001",
              "shortDescription": { "text": "Stale comment in hook script" },
              "defaultConfiguration": { "level": "note" },
              "helpUri": "https://cwe.mitre.org/data/definitions/546.html"
            },
            {
              "id": "SEC-ADVISORY-002",
              "shortDescription": { "text": "send_to_terminal not covered by hook" },
              "defaultConfiguration": { "level": "warning" },
              "helpUri": "https://cwe.mitre.org/data/definitions/862.html"
            }
          ]
        }
      },
      "results": [
        {
          "ruleId": "SEC-ADVISORY-001",
          "level": "note",
          "message": { "text": "Comment in block-git-add-all.sh still references 'execute/runInTerminal' which was removed from the hook config. Stale comment; no functional impact." },
          "locations": [{ "physicalLocation": { "artifactLocation": { "uri": ".github/hooks/scripts/block-git-add-all.sh" }, "region": { "startLine": 3 } } }]
        },
        {
          "ruleId": "SEC-ADVISORY-002",
          "level": "warning",
          "message": { "text": "Pre-existing gap: 'send_to_terminal' tool is not included in the hook's toolNames array. An agent could potentially bypass the git-add block by sending commands to an existing terminal session. Not a regression from this change — recommend a follow-up ticket." },
          "locations": [{ "physicalLocation": { "artifactLocation": { "uri": ".github/hooks/policy-enforcement.json" }, "region": { "startLine": 27 } } }]
        }
      ]
    }
  ]
}
```

## Finding Details

### SEC-ADVISORY-001 — Stale Comment (NOTE)
- **Severity:** Note / Informational
- **File:** `.github/hooks/scripts/block-git-add-all.sh:3`
- **Description:** Comment `# Lifecycle: PreToolUse (toolNames: run_in_terminal, execute/runInTerminal)` still references the removed tool ID. No functional impact.
- **Recommendation:** Update comment to match current config.

### SEC-ADVISORY-002 — send_to_terminal Not Covered (MEDIUM, Pre-existing)
- **Severity:** Medium (CWE-862: Missing Authorization)
- **File:** `.github/hooks/policy-enforcement.json:27`
- **Description:** The `toolNames` array only contains `run_in_terminal`. The `send_to_terminal` tool can also execute terminal commands but is not covered by the hook, creating a theoretical bypass path. **This is pre-existing and NOT introduced by this change.**
- **Recommendation:** Create a follow-up ticket to add `send_to_terminal` to the hook's `toolNames` array and update the shell script to handle its input format.

## Artifacts

- `.github/hooks/policy-enforcement.json` — reviewed, correct tool ID
- `.github/hooks/scripts/block-git-add-all.sh` — reviewed, enforcement logic sound
- `.github/hooks/scripts/check-guardian-stop.sh` — reviewed, no issues
- `.github/hooks/scripts/verify-evidence.sh` — reviewed, no issues
- `.github/hooks/scripts/verify-memory-gate.sh` — reviewed, no issues

## Timestamp

2026-04-10T17:05:00Z
