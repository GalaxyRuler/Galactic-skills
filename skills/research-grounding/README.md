# Research Grounding

Forces a current web search before any recommendation, comparison, price, version, or "state-of-the-art" claim gets presented as solid — because training data lags reality and stale claims cost more rework than a search does.

## What it does

- Flags the moment a response is about to state a **recommendation, comparison, price, version number, or benchmark** from memory
- Runs the claim through a **search-and-cite workflow**: list stale-risk claims → search each (WebSearch for general facts, Context7 for library/SDK/API docs) → cite the source inline → check the page date
- Labels anything that couldn't be verified as **unverified** instead of stating it as fact
- Ships a **red-flags list** ("about to say best/latest/cheapest with no citation", "quoting a price or version from memory") to catch the moment before it happens
- Ships a **rationalizations table** ("I already know this" / "searching is slower" / "it probably hasn't changed") that names and rejects the exact excuses that skip grounding

## When to use

Giving recommendations, comparing or choosing a tool/library/model/service, estimating costs or pricing, proposing a plan or architecture the user will act on, or making version/benchmark/"state-of-the-art"/best-option/latest claims. Also triggers on "is this grounded?" or "are your suggestions online-search grounded?"

Does **not** trigger for pure reasoning about the user's own code/files, clearly-labeled opinion, or facts the user just supplied.

## What's inside

- [SKILL.md](SKILL.md) — when-to-use triggers, the search-and-cite workflow, red flags, rationalizations table, common mistakes
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/research-grounding ~/.claude/skills/`
**Codex:** `cp -r skills/research-grounding $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\research-grounding "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse skills\research-grounding "$env:USERPROFILE\.codex\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
