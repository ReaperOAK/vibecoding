# Security Review - TASK-VIB-010

- Ticket: TASK-VIB-010
- Stage: SECURITY
- Scope: extension/src/extension.ts, extension/package.json, MCP provider path/cwd/env safety
- Verdict: FAIL
- Confidence: HIGH

## Preconditions
- STOP gate: CLEAR in .github/guardian/STOP_ALL.
- Claim metadata: present in ticket-state/SECURITY/TASK-VIB-010.json before rework.
- Upstream QA summary: expected file agent-output/QA/TASK-VIB-010.md was not present.

## STRIDE Threat Model

### Boundary 1: Extension host -> MCP stdio server process
- Code evidence: extension/src/extension.ts lines 120-138.
- Spoofing: Low (static provider id/label), score 2x1=2.
- Tampering: Low (path.join with fixed path segments, no shell string interpolation), score 2x2=4.
- Repudiation: Low (no explicit security event logging added), score 2x3=6.
- Information Disclosure: Low (only VIBECODING_WORKSPACE_ROOT and PYTHONUNBUFFERED env vars), score 2x2=4.
- DoS: Low (missing server.py can cause availability issue), score 3x3=9.
- Elevation of Privilege: Low (argv execution with python3 + script argument; no shell), score 2x1=2.

### Boundary 2: Extension manifest contribution -> VS Code framework
- Code evidence: extension/package.json lines 62-67.
- STRIDE classes: all Low for this delta (static contribution metadata; no new network/auth boundary).

## OWASP Top 10 Checklist
- A01 Broken Access Control: PASS
- A02 Cryptographic Failures: PASS
- A03 Injection: PASS (no shell-based command construction)
- A04 Insecure Design: PASS
- A05 Security Misconfiguration: PASS (cwd explicitly set)
- A06 Vulnerable Components: FAIL
- A07 Identification/Auth Failures: PASS
- A08 Software/Data Integrity Failures: PASS
- A09 Security Logging/Monitoring Failures: PASS (no regression in scope)
- A10 SSRF: PASS

## LLM Top 10
- LLM01 Prompt Injection: N/A for this delta
- LLM02 Insecure Output Handling: N/A for this delta
- LLM06 Sensitive Info Disclosure: PASS
- LLM08 Excessive Agency: PASS

## Dependency Audit + SBOM
- npm audit command: npm audit --audit-level=high --json (run in extension/)
- Audit result: high=1, moderate=1, critical=0
  - High: lodash GHSA-r5fr-rjxr-66jc, CWE-94, CVSS 8.1
  - Moderate: brace-expansion GHSA-f886-m6hf-6m8v, CWE-400, CVSS 6.5
- SBOM command: npx --yes @cyclonedx/cyclonedx-npm --output-format JSON --output-file ../agent-output/Security/TASK-VIB-010.sbom.json
- SBOM summary: CycloneDX 1.6, components=541, dependencies=651

## Secret Scan
- Command: grep patterns for api key/secret/token/password/private key in scoped files.
- Result: no matches in extension/src/extension.ts or extension/package.json.

## MCP Path/CWD/Env Safety
- Path safety: PASS (fixed subpath under workspace root, no shell interpolation).
- CWD safety: PASS (server.cwd explicitly set to workspace root URI).
- Env safety: PASS (only non-secret env vars set in registration).

## SARIF Findings
```json
{
  "version": "2.1.0",
  "runs": [
    {
      "tool": {
        "driver": {
          "name": "Security Review",
          "rules": [
            {
              "id": "SEC-DEP-001",
              "name": "High severity vulnerable component present",
              "properties": { "tags": ["OWASP-A06", "CWE-94"], "security-severity": "8.1" }
            },
            {
              "id": "SEC-DEP-002",
              "name": "Moderate vulnerable component present",
              "properties": { "tags": ["OWASP-A06", "CWE-400"], "security-severity": "6.5" }
            }
          ]
        }
      },
      "results": [
        {
          "ruleId": "SEC-DEP-001",
          "level": "error",
          "message": { "text": "lodash GHSA-r5fr-rjxr-66jc detected by npm audit" },
          "locations": [
            { "physicalLocation": { "artifactLocation": { "uri": "extension/package.json" }, "region": { "startLine": 98 } } }
          ]
        },
        {
          "ruleId": "SEC-DEP-002",
          "level": "warning",
          "message": { "text": "brace-expansion GHSA-f886-m6hf-6m8v detected by npm audit" },
          "locations": [
            { "physicalLocation": { "artifactLocation": { "uri": "extension/package.json" }, "region": { "startLine": 98 } } }
          ]
        }
      ]
    }
  ]
}
```

## Decision
REJECT / FAIL.

Reason: Security gate requires FAIL on any high finding; dependency audit returned one high advisory.

## Rework Requested
- Upgrade or override vulnerable transitive dependencies to remove lodash <=4.17.23.
- Re-run npm audit with zero high/critical findings before re-entering SECURITY.
