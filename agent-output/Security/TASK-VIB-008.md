# TASK-VIB-008 - Security Review

## Verdict
FAIL

## Key Finding
- High: path traversal in ticket resource. The handler joins caller-controlled ticket_id into tickets/{ticket_id}.json without allowlisting or canonical path checks.
- Exploit validated: read_ticket('../ticket-state/READY/TASK-VIB-009') returned TASK-VIB-009 from READY state.
- Safe failure is inconsistent: TASK-VIB-404 raises FileNotFoundError, but traversal payloads succeed.

## STRIDE
- Component: ticket resource.
- Boundary: MCP client -> read_ticket -> _load_ticket -> filesystem.
- Information Disclosure: HIGH, 4 x 4 = 16.
- Tampering: MEDIUM.
- Elevation of Privilege: MEDIUM.
- Other STRIDE categories: LOW.

## OWASP Top 10
- A01 Broken Access Control: FAIL.
- A03 Injection: FAIL, CWE-22 path traversal.
- A04 Insecure Design: FAIL.
- A02, A05, A08, A10: PASS.
- A06 Vulnerable Components: tooling gap only. requirements.txt declares mcp>=1.0.0, but pip_audit is unavailable.
- A07 and A09: N/A in scope.

## LLM Top 10
- N/A in scope.

## Secret Scan
- No hardcoded secrets found in .github/mcp-servers/ticket-server/**.

## SBOM Summary
- Dependency inventory: mcp>=1.0.0.
- Automated CVE audit and CycloneDX SBOM generation were not available in this environment.

## Tests
- python3 -m unittest discover -s .github/mcp-servers/ticket-server/tests -p test_server_resources.py
- Result: 12 passed.
- Gap: invalid ticket tests cover a missing ID, not traversal payloads.

## SARIF
```json
{"results":[{"ruleId":"SEC-TASK-VIB-008-001","level":"error","message":{"text":"Path traversal via unsanitized ticket_id"},"locations":[{"physicalLocation":{"artifactLocation":{"uri":".github/mcp-servers/ticket-server/server.py"},"region":{"startLine":42,"endLine":47}}},{"physicalLocation":{"artifactLocation":{"uri":".github/mcp-servers/ticket-server/server.py"},"region":{"startLine":113,"endLine":116}}}]},{"ruleId":"SEC-TASK-VIB-008-002","level":"warning","message":{"text":"Traversal regression test missing"},"locations":[{"physicalLocation":{"artifactLocation":{"uri":".github/mcp-servers/ticket-server/tests/test_server_resources.py"},"region":{"startLine":105,"endLine":107}}}]}]}
```

## Required Rework
1. Allowlist ticket IDs.
2. Resolve and verify canonical path containment under tickets/.
3. Make traversal attempts fail with the same not-found path as normal invalid IDs.
4. Add regression tests for traversal and malformed IDs.

## Confidence
HIGH
