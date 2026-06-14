# Repository Stewardship

Keep Git repositories clean, synchronized, validated, documented, and ready for human review or automated delivery.

## What it does

- Builds a Repo Profile (root, remotes, default branch, working-tree state, CI provider, test/lint commands, risk level) before touching anything
- Enforces permission tiers from read-only inspection to destructive/admin with explicit confirmation
- Runs safe sync (detect default branch, `--ff-only`, controlled merge/rebase) and structured conflict handling
- Gates work behind quality checks (format → lint → type → test → coverage → security → secret scan → build → E2E), cheapest first
- Maintains changelog/SemVer discipline and produces a PR readiness report before publishing

## When to use

Cloning/forking repos, syncing feature branches with trunk, resolving merge conflicts, cleaning stale branches, setting up CI gates or pre-commit hooks, triaging CI failures, preparing changelogs/release notes/SemVer bumps, or making a repo "AI-agent ready".

## What's inside

- [SKILL.md](SKILL.md) — operating rules, permission tiers, discovery-first, safe sync, quality gates, adaptive behavior
- [ACQUISITION.md](ACQUISITION.md) — Repo Profile schema and detection commands
- [GIT-HYGIENE.md](GIT-HYGIENE.md) — sync workflow, conflict handling, rerere, branch models, repo-maturity levels
- [QUALITY-GATES.md](QUALITY-GATES.md) — gate design, local hooks, agentic E2E guardrails, CI failure triage
- [RELEASE.md](RELEASE.md) — changelog rules, SemVer mapping, PR readiness report, PR body template
- [WORK-INTAKE.md](WORK-INTAKE.md) — Definition of Ready schema and WSJF prioritization
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/repo-stewardship ~/.claude/skills/`
**Codex:** `cp -r skills/repo-stewardship $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\repo-stewardship "$env:USERPROFILE\.claude\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
