# Context Canary

A per-turn health signal for long agent sessions. The agent prefixes every reply with a byte-stable line — name, turn counter, self-assessed context state — so silent context degradation becomes visible the moment it happens, with a defined recovery protocol for when the canary trips.

## What it does

- Installs a **canary contract**: a fixed first line on every response, e.g. `**Julius · t14 · ctx ok**`, stated explicitly once and then followed
- Probes three failures at once — the **name** (standing instruction fell out of effective context), the **turn counter** (continuity broke, almost always compaction), and the **self-check** (`ctx ok` / `aging` / `thin`, the agent's honest estimate)
- Distinguishes the **session canary** (tests whether conversation context survives — the one that actually detects degradation) from a **standing canary** written into `CLAUDE.md` or memory, which survives compaction by design and therefore measures much less
- Sets **emission rules**: first line always, including short replies and post-tool-call responses; never guess a counter (emit `t?` and flag it); never report `ctx ok` by reflex; self-declare a trip when the contract can no longer be found in context
- Calibrates alarms — one miss is a warning, **two consecutive misses or a counter discontinuity is a confirmed trip** — to trade a little latency for far fewer false alarms
- Runs a five-step **trip protocol**: stop trusting drifted state, checkpoint durable state to a file, re-anchor on project instructions, recommend a deliberate reset seeded from the checkpoint, re-install the canary at `t1 (gen 2)`
- States the instrument's limit plainly: the test is **one-sided** — a missing canary is strong evidence of degradation, a present one is weak evidence of health. Smoke detector, not structural inspection
- Backs every design choice with published research on context rot, lost-in-the-middle position effects, instruction drift, and compaction loss

## When to use

Starting a long or high-stakes agent session; when the canary stops appearing and you want to know what happened; when an agent notices it can no longer find its own canary contract; or when you want to know how trustworthy the current context still is. Also triggers on "context canary", "canary check", "did you lose context", or "how degraded is your context".

## What's inside

- [SKILL.md](SKILL.md) — the canary contract and field semantics, session vs. standing canary, emission rules, trip protocol, what the canary does and doesn't tell you
- [references/research.md](references/research.md) — the evidence base: Chroma's context-rot study, Liu et al. "Lost in the Middle" (arXiv:2307.03172), instruction-stability research (arXiv:2402.10962), compaction as a step-function failure, Breunig's long-context failure taxonomy, prompt canaries as known-answer tests, and why this is *not* a security canary token
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/context-canary ~/.claude/skills/`
**Codex:** `cp -r skills/context-canary $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\context-canary "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse skills\context-canary "$env:USERPROFILE\.codex\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
