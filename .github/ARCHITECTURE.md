# Vibecoding Multi-Agent System Architecture

> **Version:** 1.0.0
> **Owner:** ReaperOAK (CTO / Supervisor Orchestrator)
> **Last Updated:** 2026-02-21

---

## 1. System Overview

This architecture implements a **Supervisor Pattern** multi-agent vibecoding
system with ReaperOAK as the singular CTO and orchestrator. All subagents
operate within bounded scopes, follow Plan-Act-Reflect loops, and route
destructive operations through human approval gates.

### Design Principles

1. **Determinism over cleverness** — explicit state transitions, bounded loops
2. **Separation of concerns** — each agent owns one domain
3. **Least privilege** — minimal tool access per agent
4. **Zero hallucinated authority** — agents cannot claim capabilities they lack
5. **Immutable truth sources** — `systemPatterns.md` and `decisionLog.md` are
   controlled by ReaperOAK only
6. **Human-in-the-loop for destructive ops** — always

---

## 2. Agent Topology

```
ReaperOAK (Supervisor / CTO)
├── ProductManager    — Requirements, PRDs, user stories
├── Architect         — System design, API contracts, schemas
├── Backend           — Server-side code, APIs, DB logic
├── Frontend          — UI/UX, components, responsive design
├── QA                — Testing, E2E, boundary validation
├── Security          — Vulnerability scanning, OWASP, secrets
├── DevOps            — CI/CD, infrastructure, deployment
├── Documentation     — Docs, READMEs, ADRs, changelogs
├── Research          — Technical spikes, library evaluation
└── CIReviewer        — PR review, code diff analysis
```

### Agent Authority Matrix

| Agent | Can Read | Can Write | Can Execute | Cannot Do |
|-------|----------|-----------|-------------|-----------|
| **ReaperOAK** | Everything | systemPatterns, decisionLog, activeContext, progress | Delegate, validate, approve | Direct file edits in multi-agent mode |
| **ProductManager** | All memory bank | activeContext, progress | GitHub issues | Edit code, deploy, modify architecture |
| **Architect** | All memory bank, codebase | activeContext, progress | Analysis tools | Edit production code, deploy |
| **Backend** | Assigned files, systemPatterns | Source code (scoped dirs) | Terminal, tests | Frontend files, infra, security config |
| **Frontend** | Assigned files, systemPatterns | UI source (scoped dirs) | Terminal, browser | Backend files, infra, DB schemas |
| **QA** | All source, test dirs | Test files only | Terminal, browser | Production code, infra, deploy |
| **Security** | Everything (read-only audit) | riskRegister, activeContext | Scanners | Production code, deploy, merge |
| **DevOps** | Infra files, CI/CD configs | CI/CD, Dockerfiles, IaC | Terminal, deploy (staging) | Application code, merge to main |
| **Documentation** | All source, all docs | Documentation files only | Analysis tools | Code, infra, deploy |
| **Research** | External sources, codebase | activeContext, progress | Web fetch, search | Code, infra, deploy, merge |
| **CIReviewer** | PR diffs, codebase | PR comments only | Analysis tools | Merge, deploy, edit source |

---

## 3. Delegation Packet Format

Every task delegated from ReaperOAK to a subagent uses this canonical format:

```yaml
packet:
  taskId: "TASK-{timestamp}-{seq}"
  delegatedBy: "ReaperOAK"
  assignedTo: "{subagent-name}"
  objective: "Clear, measurable description of what must be accomplished"
  successCriteria:
    - "Criterion 1: specific, verifiable"
    - "Criterion 2: specific, verifiable"
  scopeBoundaries:
    included:
      - "files/dirs that CAN be touched"
    excluded:
      - "files/dirs that MUST NOT be touched"
  forbiddenActions:
    - "Action that is explicitly prohibited"
  requiredOutputFormat: "Description of expected deliverable shape"
  evidenceExpectations:
    - "Test results, screenshots, logs, etc."
  priority: "P0 | P1 | P2 | P3"
  dependencies:
    - "TASK-ID of prerequisite tasks"
  timeoutBudget: "max iterations or token budget"
```

---

## 4. Task State Machine

Every task follows this deterministic state flow:

```
┌─────────┐    ┌──────────────┐    ┌────────┐    ┌─────────┐
│ PENDING │───▶│ IN_PROGRESS  │───▶│ REVIEW │───▶│ MERGED  │
└─────────┘    └──────────────┘    └────────┘    └─────────┘
                     │                   │
                     ▼                   ▼
                ┌──────────┐      ┌───────────┐
                │ BLOCKED  │      │ REJECTED  │
                └──────────┘      └───────────┘
                     │                   │
                     ▼                   ▼
                ┌──────────┐      ┌──────────────┐
                │ ESCALATED│      │ IN_PROGRESS  │ (retry)
                └──────────┘      └──────────────┘
```

**State Definitions:**

| State | Description | Owner |
|-------|-------------|-------|
| PENDING | Task queued, dependencies not met | ReaperOAK |
| IN_PROGRESS | Subagent actively working | Assigned subagent |
| REVIEW | Work done, awaiting QA validation | ReaperOAK + QA |
| MERGED | Validated and integrated | ReaperOAK |
| BLOCKED | Cannot proceed, dependency issue | ReaperOAK |
| REJECTED | QA failed, needs rework | ReaperOAK |
| ESCALATED | Requires human intervention | Human |

---

## 5. Merge Protocol

1. Subagent completes work → signals REVIEW state
2. ReaperOAK's Reviewer lane validates:
   - Requirements coverage check
   - Correctness/syntax validation
   - No forbidden file modifications
   - Evidence expectations met
3. If validation passes → MERGED state
4. If validation fails → REJECTED state with fix delta → back to IN_PROGRESS
5. File conflict detection:
   - Before merge, diff analysis on all modified files
   - If parallel branches modified same file → sequential resolution
   - Conflicting changes escalated to ReaperOAK for manual merge

---

## 6. Parallel Execution Rules

### Parallel-Safe Operations

| Operation Type | Parallel-Safe? | Condition |
|---------------|---------------|-----------|
| Read-only analysis | ✅ Always | No conditions |
| Write to different files | ✅ Yes | Files don't share dependencies |
| Write to same file | ❌ Never | Must be sequential |
| Independent test suites | ✅ Yes | No shared state |
| External API calls | ✅ If idempotent | GET requests, read-only APIs |
| Database mutations | ❌ Never | Must be sequential |
| Infrastructure changes | ❌ Never | Must be sequential + approved |

### Concurrency Limit

- Maximum 4 parallel subagents at any time
- Each parallel batch requires pre-declared file ownership
- No two subagents may claim the same file in a parallel batch

---

## 7. Conflict Resolution Policy

1. **Intra-agent conflict** (subagent disagrees with its own prior output):
   → Re-run with explicit context of the contradiction
2. **Inter-agent conflict** (two subagents produce conflicting outputs):
   → ReaperOAK resolves using `systemPatterns.md` as canonical truth
   → If `systemPatterns.md` is insufficient → `decisionLog.md` entry + human gate
3. **Agent vs. instruction conflict** (subagent output contradicts instruction file):
   → Instruction file wins. Subagent re-runs constrained to instruction rules.
4. **Precedence hierarchy:**

   ```
   Human directive > ReaperOAK decision > systemPatterns.md >
   domain instruction > general instruction > agent default behavior
   ```

---

## 8. Human Approval Gate Triggers

The following operations **ALWAYS** halt and require explicit human approval:

| Trigger | Category |
|---------|----------|
| Database drops, mass deletions | Destructive |
| Force pushes, branch deletions | Destructive |
| Production deployments | Deployment |
| Firewall/network policy changes | Security |
| New external dependency introduction | Supply chain |
| Architecture pattern changes | Design |
| Security exception requests | Security |
| Privilege escalation for any agent | Governance |
| Merge to main/production branch | Release |
| Secret/credential rotation | Security |

---

## 9. Plan-Act-Reflect Loop (All Subagents)

Every subagent follows this cognitive loop:

```
┌──────────────────────────────────┐
│           PLAN                    │
│  1. State intended approach       │
│  2. Identify required tool calls  │
│  3. List file modifications       │
│  4. Declare assumptions           │
└──────────────┬───────────────────┘
               ▼
┌──────────────────────────────────┐
│            ACT                    │
│  1. Execute plan step-by-step     │
│  2. Constrain to declared scope   │
│  3. Make smallest valid changes   │
│  4. Collect evidence at each step │
└──────────────┬───────────────────┘
               ▼
┌──────────────────────────────────┐
│          REFLECT                  │
│  1. Review stdout/stderr          │
│  2. Summarize what succeeded      │
│  3. Summarize what failed         │
│  4. Determine: retry or complete  │
│  5. Update activeContext.md       │
└──────────────────────────────────┘
```

---

## 10. Memory Bank Integration

Located at `.github/memory-bank/`:

| File | Owner | Write Access | Purpose |
|------|-------|-------------|---------|
| `productContext.md` | ReaperOAK | ReaperOAK, ProductManager | Project vision, goals, constraints |
| `systemPatterns.md` | ReaperOAK | ReaperOAK ONLY | Architecture decisions, code conventions |
| `activeContext.md` | Shared | All subagents (append) | Current focus, recent changes |
| `progress.md` | Shared | All subagents (append) | Completed milestones, pending work |
| `decisionLog.md` | ReaperOAK | ReaperOAK ONLY | Trade-off records, rationale |
| `riskRegister.md` | Security | Security, ReaperOAK | Identified risks, mitigations |

**Immutability Rules:**

- `systemPatterns.md` and `decisionLog.md` are append-only by ReaperOAK
- No subagent may delete or overwrite entries in these files
- Subagents may only append timestamped entries to `activeContext.md` and `progress.md`

---

## 11. Security Guardrails

See `.github/security.agentic-guardrails.md` for full specification.

Key constraints:

- All subagents operate with least-privilege tool access
- External content is sanitized before processing
- Prompt injection patterns are detected and rejected
- Memory bank entries are validated before persistence
- Token runaway detection halts infinite loops
- MCP servers are treated as untrusted by default

---

## 12. CI/CD AI Integration

See `.github/workflows/ai-*.yml` for workflow definitions.

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ai-code-review.yml` | pull_request | Automated code review with findings as comments |
| `ai-test-validator.yml` | pull_request | Validate test coverage and quality |
| `ai-security-scan.yml` | pull_request | Security vulnerability detection |
| `ai-doc-sync.yml` | pull_request | Documentation freshness check |

All workflows:

- Use least-privilege tokens (read-only default)
- Never auto-merge
- Comment findings on PRs
- Require human approval for write operations
- Fail safely (no recursion, bounded execution)
