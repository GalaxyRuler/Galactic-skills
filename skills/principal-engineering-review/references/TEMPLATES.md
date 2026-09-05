# Templates

## Architecture Decisions

For significant decisions, propose or update an Architecture Decision Record. Use ADRs for architecture pattern changes, database strategy, state management, major dependencies, deployment strategy, API versioning, security model changes, and AI/model/provider choices.

```markdown
# ADR-XXX: <Decision Title>

## Status
Proposed | Accepted | Superseded

## Context
What problem are we solving?

## Decision
What did we decide?

## Alternatives Considered
What else was considered?

## Consequences
Benefits, trade-offs, risks.

## Verification
How will we know the decision worked?
```

## Trade-Off Analysis

When comparing tools, libraries, architectures, or strategies, use:

| Option | Pros | Cons | Best fit | Avoid when | Recommendation |
|---|---|---|---|---|---|

Then state the recommended option, why, assumptions, migration path if relevant, and verification plan.

## Review Output Format

When the user asks for a review, lead with findings:

```markdown
## Summary
Brief verdict.

## High-Priority Issues
| Issue | Severity | Evidence | Impact | Recommended Fix |
|---|---|---|---|---|

## Medium/Low-Priority Issues
...

## Security Notes
...

## Performance Notes
...

## Tests to Add
...

## Final Recommendation
Proceed / revise / block, with reason.
```

Severity:

- P0: breaks production or security-critical.
- P1: major correctness, reliability, or security risk.
- P2: maintainability or performance issue.
- P3: polish or future improvement.

## Implementation Report Format

When implementing changes, final response should include:

```markdown
## What Changed
- ...

## Files Changed
- ...

## Verification
- Command: ...
- Result: PASS/FAIL/Not run
- Notes: ...

## Risks / Follow-Up
- ...
```
