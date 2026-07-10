# Test UX

Generic, stack-agnostic UX testing process for any product — runs expert heuristic evaluation, task-based walkthroughs, and content/localization review, then generates a real-user test plan for the parts that need actual humans.

## What it does

- Runs **Nielsen's 10 heuristics** evaluation per key screen with screenshot evidence and severity 0–4 ratings
- Drives **task-based cognitive walkthroughs** step-by-step against defined user goals, logging steps-vs-optimal, dead-ends, and hesitation
- Reviews **journey & state** coverage — empty/loading/low-data/error/first-run/returning states, error recovery, trust & provenance
- Checks **content + internationalization comprehension** — plain language, no raw technical identifiers shown to users, meaning parity and correct text direction per locale, no untranslated source text on the rendered page
- Generates a **real-user test-plan** — moderated + unmoderated scripts, screener, and a metrics sheet (task success, time, SEQ, SUS) for the dimensions an agent can't verify alone
- Never silently passes an un-run dimension — flags it `NOT VERIFIED` in the report instead

## When to use

Asked to UX-test, usability-test, run a UX audit, evaluate user experience, check novice-friendliness, assess whether users can complete a flow, or review content/localization clarity.

## What's inside

- [SKILL.md](SKILL.md) — the runbook: scoping, 7-phase execution order, report format
- [playbook.md](playbook.md) — the method: the 4 learnability questions, heuristic detail, test-plan generator format
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/test-ux ~/.claude/skills/`
**Codex:** `cp -r skills/test-ux $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\test-ux "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse skills\test-ux "$env:USERPROFILE\.codex\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex. Pairs well with [test-backend](../test-backend) and [test-ui](../test-ui) for full-stack coverage.
