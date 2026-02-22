Perform a comprehensive code review on the specified files or recent changes.

Follow the review protocol from `.github/agents/CIReviewer.agent.md` and `docs/instructions/gilfoyle-code-review.instructions.md`.

## Review Checklist

For each file or change, evaluate:

### Correctness
- Logic errors, off-by-one, null handling
- Edge cases and boundary conditions
- Error handling completeness

### Security
- OWASP Top 10 patterns (see `docs/instructions/security-and-owasp.instructions.md`)
- Input validation at system boundaries
- No hardcoded secrets or credentials
- SQL injection, XSS, command injection risks

### Performance
- N+1 query patterns
- Unnecessary re-renders or recomputation
- Memory leak potential
- Complexity analysis (cognitive <= 15, cyclomatic <= 10)

### Convention
- Follows patterns in `.github/memory-bank/systemPatterns.md`
- Consistent naming and style
- Appropriate use of types/interfaces

### Accessibility (if UI code)
- WCAG 2.2 AA compliance
- Semantic HTML, ARIA labels
- Keyboard navigation

### Completeness
- All requirements addressed
- Test coverage for changed code
- Documentation updated if needed

## Output Format

For each finding, report:
- **File:Line** — Location
- **Severity** — Critical / High / Medium / Low / Info
- **Category** — Correctness / Security / Performance / Convention / A11y
- **Description** — What the issue is
- **Suggestion** — How to fix it

Provide an overall assessment with a quality score (1-10).
