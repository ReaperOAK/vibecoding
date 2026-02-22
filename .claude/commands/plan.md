Enter planning mode for the specified objective. Follow the spec-driven workflow from `docs/instructions/spec-driven-workflow-v1.instructions.md`.

## Planning Protocol

### Phase 1: ANALYZE

1. Read and understand the objective fully
2. Load relevant memory bank files (`.github/memory-bank/`)
3. Load relevant instruction files from `docs/instructions/`
4. Scan the codebase for existing patterns and conventions
5. Define requirements in EARS notation:
   - `WHEN [condition], THE SYSTEM SHALL [behavior]`
6. Identify dependencies and constraints
7. Assess confidence (0-100%)

### Phase 2: DESIGN

Based on confidence level:
- **High (>85%)**: Draft comprehensive implementation plan
- **Medium (66-85%)**: Propose proof-of-concept first
- **Low (<66%)**: Research phase first, then re-analyze

Document:
- Architecture decisions and rationale
- Data flow and interfaces
- Error handling strategy
- Testing strategy
- Implementation plan with dependency ordering

### Output Format

```markdown
## Plan: [Objective]

### Understanding
[Restate objective in own words]

### Assumptions
1. [Assumption with basis]

### Requirements (EARS)
1. WHEN [X] THE SYSTEM SHALL [Y]

### Approach
[Step-by-step plan with dependencies]

### Risk Assessment
| Risk | Probability | Impact | Mitigation |

### Confidence: [N]% ([level])
### Decision Points: [where human input needed]
```

**Rule:** Do NOT implement anything in plan mode. Output the plan and wait for approval.
