# Test Backend

Generic, stack-agnostic back-end / API testing process for any service — detects the project's language and stack, then runs a phase-gated playbook covering unit/integration, contract, data invariants, resilience, security, and load.

## What it does

- Runs the **Testing Trophy** shape: static base → thin unit (pure logic) → integration as the widest layer (real deps via Testcontainers) → thin E2E cap
- Runs **API contract testing** — request+response schema for every endpoint, spec-driven provider tests (Schemathesis/Dredd), consumer-driven (Pact), breaking-change diff vs the committed spec
- Verifies **data invariants** — golden-master parity, deterministic IDs, ETL/sync idempotency, migration safety
- Runs **resilience + chaos** checks — kills/slows/garbles each dependency and asserts graceful degradation
- Covers the **OWASP API Security Top 10 (2023)**, including two-account BOLA testing, injection, SSRF, and rate-limiting
- Runs **load/SLO** testing with thresholds encoded from the service's SLOs
- Never silently passes an un-run phase — flags it `NOT VERIFIED` in the report instead

## When to use

Asked to test a backend or API, contract-test, security-test an API, load/performance-test, or chaos/resilience-test. Detects the project's language/framework/test-runner/DB/ORM automatically and degrades gracefully when a tool is absent.

## What's inside

- [SKILL.md](SKILL.md) — the runbook: stack detection, 10-phase execution order, safety rules, report format
- [playbook.md](playbook.md) — the method: why each phase exists, technique detail per phase
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/test-backend ~/.claude/skills/`
**Codex:** `cp -r skills/test-backend $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\test-backend "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse skills\test-backend "$env:USERPROFILE\.codex\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex. Pairs well with [test-ui](../test-ui) and [test-ux](../test-ux) for full-stack coverage.
