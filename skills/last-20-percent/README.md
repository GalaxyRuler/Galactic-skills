# The Last 20%

Agents reliably ship the first 80% of a build — ingestion, endpoints, schema, pipeline — and skip the 20% that makes it something a person would love. This skill finds that residue, specs it as concretely as the plumbing, and finishes it.

## What it does

- Names **why the 20% gets skipped** — tasks come from decomposing the noun, "done" is defined by what's testable, taste feels like overreach, and experiential work scheduled last is what gets cut — then counters each with a phase
- Enforces the **cardinal rule**: never call a solution done until you have consumed its output the way the end user will. Reading your own code isn't consuming the output; passing tests isn't either
- **Phase 1 — write the magic moment**: one concrete scene with a named person and a real task, not a feature list. If you can't write it, that gap *is* the missing 20%
- **Phase 2 — decompose the scene, not just the noun**: build both lists; the last 20% is the scene list minus the noun list
- **Phase 3 — spec at plumbing fidelity**: convert every vague quality goal into done-criteria as checkable as "endpoint returns 200", and **hand-craft golden artifacts before building the generator** — the ideal output doubles as spec, test fixture, and quality bar (never with placeholder content)
- **Phase 4 — front-load, never append**: golden artifacts first, experience decisions threaded through the build, and a visible finish list where an unchecked item is treated exactly like a failing test
- **Phase 5 — the walk**: become the end user cold, perform the magic moment literally, judge against the golden artifacts, fix, walk again — ending either in delivered magic with evidence, or in an explicit list of human product decisions each with a recommendation
- Ships **plan mode and audit mode** for "shape this build" versus "is this actually done?"
- Draws hard boundaries: depth on the core scene never breadth, bring a take instead of a questionnaire, don't gold-plate working plumbing, and **a solution is allowed to pass** — manufacturing gaps to look thorough is its own kind of slop

## When to use

Planning any build, so the magic gets specced as concretely as the plumbing; before calling any build "done"; when a solution works but feels like a demo; or when someone says "finish this", "make it actually good", "is this actually done", or "why does this feel flat".

## What's inside

- [SKILL.md](SKILL.md) — why the 20% gets skipped, the cardinal rule, five phases, plan/audit modes, boundaries
- [references/last-20-catalog.md](references/last-20-catalog.md) — the eight recurring categories the residue falls into (content and voice, information architecture, first-run and empty states, opinionated defaults, the golden path, the failure experience, naming and microcopy, the second visit), each with a probe question and worked examples across wikis, dashboards, CLIs, APIs, SaaS apps, and libraries
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/last-20-percent ~/.claude/skills/`
**Codex:** `cp -r skills/last-20-percent $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\last-20-percent "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse skills\last-20-percent "$env:USERPROFILE\.codex\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
