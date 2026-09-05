---
name: principal-engineering-review
description: Use when the user asks the agent to design, review, refactor, secure, optimize, or implement production-grade software, especially architecture reviews, React/Next.js apps, APIs, database migrations, CI/CD or deployment hardening, security review, performance optimization, legacy refactors, and AI-assisted engineering workflows. Do not use for trivial edits unless the user explicitly asks for architecture or production-readiness review.
---

# Principal Engineering Review

## Core Principle

Treat the agent as executor and the human as supervisor. Verify the real repository before making meaningful claims or changes, then make the smallest coherent change that moves the system toward production quality.

Do not assume architecture, framework, package manager, test commands, deployment model, database shape, or repo conventions. Confirm them from files or commands first.

## Standard Workflow

For non-trivial work, proceed in this order:

1. Discover the repository.
2. Frame the problem.
3. Plan the change.
4. Implement the smallest safe slice.
5. Verify with the strongest available checks.
6. Report changes, evidence, risks, and follow-up.

Stop and ask only when the change requires deleting data, rotating secrets, changing public API behavior, choosing between major product directions, or when unrelated failures block safe progress.

## Discovery Checklist

Before architecture advice or code changes, inspect the relevant subset of:

- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, README, docs, and repo instructions.
- Folder structure and application boundaries.
- Package manager files and scripts.
- Framework conventions and frontend/backend entrypoints.
- Build, lint, typecheck, test, and smoke-test commands.
- Existing state management, API patterns, and error handling.
- Database schema, migrations, seed data, and ORM/query layer.
- Deployment, CI/CD, infrastructure, and environment config.
- Security-sensitive surfaces: auth, secrets, CORS, webhooks, uploads, logging, and external calls.

If something remains unknown, state what is unknown and which file or command would confirm it.

## Problem Framing

Before editing, restate briefly:

- User goal.
- Affected components.
- Likely correctness, security, performance, migration, or delivery risks.
- Assumptions.
- Verification criteria.

Ask only essential clarifying questions. Otherwise proceed with labeled assumptions.

## Planning Rules

Use a concise plan for non-trivial work:

- Files to inspect.
- Files likely to change.
- Tests or checks to run.
- Rollback or safety considerations.
- Expected output.

For risky work, use staged delivery instead of one broad rewrite.

## Implementation Rules

Preserve existing style and conventions. Avoid unrelated cleanup.

Prefer:

- Readable code and explicit data flow.
- Small modules and clear names.
- Minimal abstractions.
- Tests around critical behavior.
- Backward-compatible changes.

Avoid:

- Clever abstractions without demonstrated need.
- Premature microservices or heavy layering.
- New production dependencies without clear value.
- Broad rewrites when targeted refactors are enough.
- Hiding business logic in UI components.
- Skipping tests after generated changes.

Use SOLID, DRY, KISS, and YAGNI pragmatically. Repo conventions and simplicity win over mechanical pattern application.

## Verification

Run the strongest relevant checks available:

- Typecheck.
- Lint.
- Unit tests.
- Integration tests.
- Build.
- Relevant smoke tests.
- Security or dependency checks where feasible.

If a check cannot be run, say why and provide the exact command to run.

## References (load on demand)

| Need | File |
|---|---|
| Frontend / backend / security / database-migration / CI-CD standards to review against | [references/STANDARDS.md](references/STANDARDS.md) |
| ADR template, trade-off analysis, review output format, implementation report format | [references/TEMPLATES.md](references/TEMPLATES.md) |

## Completion Bar

Treat work as complete only when:

- The code works.
- The change is minimal and coherent.
- Tests or verification were run.
- Docs were updated if behavior changed.
- Security and performance risks were considered.
- Trade-offs are explicit.
- The user can understand what changed and why.
