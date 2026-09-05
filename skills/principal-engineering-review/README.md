# Principal Engineering Review

A discipline for production-grade software work: verify the real repository before claiming anything, make the smallest coherent change, and prove it with the strongest checks the project actually has.

## What it does

- Puts the agent in executor mode and the human in supervisor mode — no architecture claims that were not confirmed from files or commands
- Runs a discovery checklist first: repo instructions, package manager, framework conventions, test/build commands, schema and migrations, deployment, and security-sensitive surfaces
- Frames the problem (goal, blast radius, risks, assumptions, verification criteria) before any edit
- Enforces the smallest safe slice over broad rewrites, with staged delivery for risky work
- Names the stop conditions that require asking the human: data deletion, secret rotation, public API behavior changes, major product forks
- Carries frontend, backend, security, database-migration, and CI/CD standards to review against — including Expand-Migrate-Contract for schema changes
- Supplies an ADR template, a trade-off comparison table, a severity-ranked review format (P0–P3), and an implementation report format
- Closes against a completion bar: verification run, docs updated, trade-offs explicit, risks stated

## When to use

Architecture reviews, React/Next.js apps, API design and changes, database migrations, CI/CD and deployment hardening, security review, performance optimization, legacy refactors, and AI-assisted engineering workflows. Not for trivial edits, unless architecture or production-readiness review is explicitly requested.

## What's inside

- [SKILL.md](SKILL.md) — core principle, standard workflow, discovery checklist, problem framing, planning and implementation rules, verification, completion bar
- [references/STANDARDS.md](references/STANDARDS.md) — frontend, backend, security, database/migration, and CI/CD standards to review against
- [references/TEMPLATES.md](references/TEMPLATES.md) — ADR template, trade-off analysis table, review output format with severity levels, implementation report format
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/principal-engineering-review ~/.claude/skills/`
**Codex:** `cp -r skills/principal-engineering-review $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\principal-engineering-review "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse skills\principal-engineering-review "$env:USERPROFILE\.codex\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
