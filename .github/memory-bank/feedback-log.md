---
id: feedback-log
version: "1.0"
owner: Shared
write_access: [ALL]
append_only: true
---

# Feedback Log

> Inter-agent quality signals. All agents may append entries during VALIDATE phase.
> Each entry captures one feedback item from one agent about another agent's output.
> Format: timestamp, from agent → to agent, session, phase, artifact, type, severity, signal, evidence, resolution.

---

## Entries

<!-- Append entries below in reverse chronological order -->
<!-- Entry format:
### [ISO8601-TIMESTAMP] SourceAgent → TargetAgent
- **Session:** SESSION-ID
- **Phase:** VALIDATE
- **Subject Artifact:** file/path
- **Feedback Type:** defect | vulnerability | convention_violation | performance | praise | suggestion
- **Severity:** critical | high | medium | low | info
- **Signal:** description of the issue
- **Evidence:** link to report
- **Resolution:** pending | fixed | wontfix | deferred
-->
