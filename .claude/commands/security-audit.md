Perform a security audit on the specified files or the entire codebase.

Follow the security protocols from:
- `.github/security.agentic-guardrails.md` — STRIDE threat model
- `.github/agents/Security.agent.md` — Security agent domain expertise
- `docs/instructions/security-and-owasp.instructions.md` — OWASP Top 10

## Audit Scope

### OWASP Top 10 Check

1. **Injection** — SQL, NoSQL, OS command, LDAP injection
2. **Broken Authentication** — Weak credentials, session management
3. **Sensitive Data Exposure** — Unencrypted data, leaked secrets
4. **XML External Entities** — XXE injection
5. **Broken Access Control** — Privilege escalation, IDOR
6. **Security Misconfiguration** — Default configs, verbose errors
7. **Cross-Site Scripting (XSS)** — Reflected, stored, DOM-based
8. **Insecure Deserialization** — Object injection
9. **Using Components with Known Vulnerabilities** — Outdated deps
10. **Insufficient Logging & Monitoring** — Missing audit trails

### STRIDE Threat Analysis

| Threat | Check |
|--------|-------|
| **Spoofing** | Authentication, identity verification |
| **Tampering** | Data integrity, input validation |
| **Repudiation** | Audit trails, logging |
| **Information Disclosure** | Data exposure, error messages |
| **Denial of Service** | Rate limiting, resource exhaustion |
| **Elevation of Privilege** | Authorization, access control |

### Additional Checks

- Hardcoded secrets or credentials in code
- Exposed API keys or tokens
- Insecure dependencies (check for known CVEs)
- Missing rate limiting on public endpoints
- Improper error handling revealing internals
- Missing CSRF protections
- Insecure cookie configuration

## Output Format

Report findings in the risk register format:

```
### RISK-{number}: {title}
- **Severity:** Critical | High | Medium | Low
- **Category:** [OWASP category or STRIDE category]
- **Location:** [file:line]
- **Description:** [What the vulnerability is]
- **Impact:** [What could happen if exploited]
- **Remediation:** [How to fix it]
```

Append new risks to `.github/memory-bank/riskRegister.md`.
