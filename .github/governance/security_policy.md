# Security Policy

> **GOVERNANCE_VERSION: 9.0.0**
> **Authority:** `.github/instructions/core_governance.instructions.md`
> **Scope:** Human approval gates, security review triggers, dual-layer security model

---

## 1. Human Approval Required Gates

The following operations are **destructive or irreversible**. No agent may
execute them without explicit user confirmation. Violations are protocol
failures logged in `decisionLog.md`.

### Destructive Operations List

| Operation | Risk Category | Approval Required |
|-----------|--------------|-------------------|
| Database drops | Data loss | User confirmation |
| Mass deletions (bulk row/document removal) | Data loss | User confirmation |
| Force pushes (`git push --force`) | History loss | User confirmation |
| Production deployments | Service impact | User confirmation |
| Merges to `main` branch | Release impact | User confirmation |
| New external dependency introduction | Supply chain risk | User confirmation |
| Schema migrations (ALTER/DROP columns) | Data integrity | User confirmation |
| API breaking changes (removed endpoints, changed signatures) | Consumer impact | User confirmation |
| Any operation with irreversible data loss potential | Data loss | User confirmation |

### Approval Protocol

1. Agent detects a destructive operation is required
2. Agent emits `BLOCKED_BY` event with `blocker_type: HUMAN_APPROVAL_GATE`
3. ReaperOAK surfaces the request to the user with full context
4. User explicitly confirms (YES) or rejects (NO)
5. Decision is logged in `.github/memory-bank/decisionLog.md`
6. If approved, agent proceeds; if rejected, ticket is re-scoped or cancelled

### Override Logging

Any override of a human approval gate MUST be recorded:

```markdown
### [TICKET-ID] — Human Approval Override
- **Operation:** {description}
- **Risk Category:** {category}
- **Decision:** APPROVED / REJECTED
- **Justification:** {user-provided reason}
- **Timestamp:** {ISO8601}
```

---

## 2. Security Review Trigger (INV-7)

**Invariant INV-7:** Security Engineer must review when a ticket introduces
a new risk surface.

### Risk Surface Triggers

A ticket introduces a new risk surface if it:
- Adds authentication or authorization logic
- Exposes a new API endpoint (public or internal)
- Handles user-supplied input (forms, file uploads, query params)
- Modifies access control or permission models
- Introduces cryptographic operations
- Adds external service integrations (OAuth, payment, third-party API)
- Modifies network configuration (CORS, CSP, firewall rules)
- Handles sensitive data (PII, credentials, tokens)

### Review Protocol

1. At QA_REVIEW, Validator checks if the ticket matches any risk surface trigger
2. If matched, Security Engineer is added to the post-execution chain
3. Security Engineer reviews BEFORE ticket advances past VALIDATION
4. Security PASS → ticket continues; Security REJECT → REWORK

---

## 3. Security Engineer Dual-Layer Role

Security Engineer operates in **two distinct modes** depending on the
orchestration layer:

### Strategic Layer (Threat Modeling)

- **Activities:** STRIDE analysis, OWASP Top 10 mapping, threat model creation
- **Outputs:** Threat model documents, risk assessments, security ADRs
- **Invocation:** By ReaperOAK during strategic planning phase
- **Scope:** System-wide security posture, architecture-level risks

### Execution Layer (Security Scanning)

- **Activities:** SBOM generation, dependency vulnerability scanning, code review
- **Outputs:** SBOM reports, vulnerability findings, scan results
- **Invocation:** As part of post-execution chain when INV-7 triggers
- **Scope:** Ticket-specific security verification

---

## 4. Violation Handling

Security policy violations are logged as follows:

| Violation | Severity | Response |
|-----------|----------|----------|
| Destructive op without approval | CRITICAL | Block immediately, alert user |
| Security review skipped (INV-7) | HIGH | REWORK — add security review |
| Sensitive data in logs/commits | CRITICAL | Block, purge, alert user |
| Unvalidated external dependency | HIGH | Block until reviewed |

All violations are appended to `.github/memory-bank/decisionLog.md` with
full context, severity, and remediation action taken.
