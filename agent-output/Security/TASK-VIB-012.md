# TASK-VIB-012 — Security Stage Report

## Agent: Security | Stage: SECURITY | Machine: dispatcher | Operator: reaperoak
## Timestamp: 2026-03-27T09:40:00Z

---

## Scope

Modified files under review:
- `extension/src/ticketTreeProvider.ts` — new file
- `extension/src/extension.ts` — modified (TreeView registration)
- `extension/package.json` — modified (contributions)

---

## 1. STRIDE Threat Model

### Trust Boundaries
- **User Workspace FS → Extension Host**: ticketTreeProvider reads `ticket-state/{READY,DONE}/*.json` from workspace root.
- **Extension Host → VS Code UI**: Data rendered in TreeView sidebar (read-only).

| Threat | STRIDE Category | Score (I×L) | Finding |
|--------|----------------|-------------|---------|
| Malformed JSON ticket file causes uncaught exception | DoS | 2×2=4 (Low) | `JSON.parse()` in `readTicketFile()` lacks try/catch — unhandled exception crashes tree provider. Limited to extension host restart. |
| Symlinked JSON file pointing outside workspace | Information Disclosure | 2×1=2 (Low) | `fs.readFileSync` follows symlinks. Attacker needs pre-existing write access to workspace. Theoretical only. |
| Path traversal via filename `../` | Tampering | 2×1=2 (Low) | `path.join(stagePath, name)` where `name` from `fs.readdirSync` — readdir returns basenames only on Linux. No practical vector. |
| Spoofing / EoP | Spoofing/EoP | N/A | TreeView is read-only; no auth, no remote calls. N/A. |
| Repudiation | Repudiation | N/A | Display-only UI, no write actions. N/A. |

**Maximum STRIDE score: 4 (Low). No Critical (>=20) or High (>=15) findings.**

---

## 2. OWASP Top 10 Checklist

| # | Category | Result | Evidence |
|---|---------|--------|---------|
| A01 | Broken Access Control | PASS | Read-only local FS. No auth endpoints. |
| A02 | Cryptographic Failures | PASS | No sensitive data stored/transmitted. |
| A03 | Injection | PASS | Stage is TypeScript `'READY' | 'DONE'` literal — compile-time constrained. `path.join` for all paths. No shell exec, no eval. |
| A04 | Insecure Design | PASS | Purely presentational TreeView; no destructive actions. |
| A05 | Security Misconfiguration | PASS | No debug flags; activationEvents workspace-scoped. |
| A06 | Vulnerable Components | PASS* | npm audit: 0 critical, 0 high CVEs. 22 moderate all in dev toolchain (jest/@vscode/vsce), not runtime bundle. |
| A07 | Auth Failures | N/A | No authentication surface. |
| A08 | Data Integrity | LOW | `JSON.parse()` without try/catch in `readTicketFile()` (line 57). Malformed local ticket file crashes provider. Not a remote/untrusted deserialization vector. |
| A09 | Logging Failures | PASS | Zero console.* calls in ticketTreeProvider.ts. No PII logged. |
| A10 | SSRF | PASS | No network calls. Local FS only. |

---

## 3. LLM Top 10

Not applicable — TASK-VIB-012 introduces no AI/LLM features.

---

## 4. Dependency Audit (SBOM Summary)

```
Command: npm audit --audit-level=high (from extension/)

  0 critical
  0 high
 22 moderate  [dev/build toolchain: brace-expansion via jest + @vscode/vsce]
  0 low

Runtime impact: NONE — affected packages not bundled in vsix artifact.
Remediation: npm audit fix (non-breaking) resolves most issues.
```

Runtime SBOM: `vscode` API (host-provided), `fs`, `path` (Node.js stdlib).
No third-party runtime dependencies introduced by TASK-VIB-012.

---

## 5. Secret Scanning

```
Pattern: hardcode|password|secret|token|api[_-]?key|private[_-]?key|Bearer
Scanned: extension/src/ticketTreeProvider.ts, extension/src/extension.ts, extension/package.json

Result: 0 matches in scope files.
```

No hardcoded secrets found.

---

## 6. Auth / AuthZ Review

No auth required. `rootPath` derived from `vscode.workspace.workspaceFolders?.[0]?.uri.fsPath`
(VS Code controlled). Stage names are TypeScript literals. No user-injectable path components.

---

## 7. SARIF Findings

```json
{
  "version": "2.1.0",
  "runs": [{
    "tool": { "driver": { "name": "Vibecoding Security Scanner", "version": "1.0.0",
      "rules": [{
        "id": "SEC-A08-001", "name": "UncheckedJsonParse",
        "shortDescription": { "text": "JSON.parse without error handling" },
        "helpUri": "https://cwe.mitre.org/data/definitions/20.html",
        "properties": { "severity": "low", "cwe": "CWE-20" }
      }]
    }},
    "results": [{
      "ruleId": "SEC-A08-001", "level": "note",
      "message": { "text": "JSON.parse() in readTicketFile() line 57 lacks try/catch. Malformed local ticket JSON crashes TreeView provider. Suggest try/catch with fallback TicketRecord." },
      "locations": [{ "physicalLocation": {
        "artifactLocation": { "uri": "extension/src/ticketTreeProvider.ts" },
        "region": { "startLine": 57 }
      }}]
    }]
  }]
}
```

---

## 8. Verdict

**PASS**

### Justification
- 0 Critical findings
- 0 High findings
- 1 Low finding (unchecked JSON.parse — local file only, no remote attack path)
- npm audit: 0 critical/high CVEs in runtime bundle
- No hardcoded secrets
- No injection vectors (TypeScript literal types enforce stage at compile time)
- No network calls; no SSRF surface
- No PII in logs

### Risk Acceptance
- **SEC-A08-001 (Low)**: Malformed local ticket file causes tree provider crash. Acceptable —
  files are machine-generated by tickets.py under trusted local control.

---

## Confidence Level: HIGH
