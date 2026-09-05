# Distinctive Design Gates

A pre-presentation deny-gate for design work: five checks a UI, page, or mockup must pass before it is shown, so generic AI-default aesthetics get caught and iterated on instead of presented.

## What it does

- Blocks the **generic-design tell**: uniform card grids, gradient hero + three feature columns, stock icon rows, purple-on-dark SaaS defaults — all fail unless deliberately subverted
- Applies the **recognizability test**: would this design stand out among ten AI-generated sites for the same brief? If it could be anyone's site, it does not ship
- Requires each new iteration to differ from rejected ones in **layout structure AND type system AND visual concept** — a recolor or reskin of a rejected skeleton fails
- Keeps a **written list of rejected directions** and what was rejected about each, checked before every presentation
- Demands **full rendered pages, top to bottom** — cropped hero sections and isolated components hide the overall impression the reviewer actually judges by
- Protects **identity and required content**: a beautiful page that erases stated positioning or content requirements fails
- Requires **grounded direction** — anchoring each concept in distinctive real-world references rather than the model's default aesthetic
- Layers on top of whatever design skill produced the work; it is a gate, not a design method

## When to use

Presenting any web/UI design, mockup, landing page, or redesign; iterating after a design rejection; or reviewing design work another agent produced before it reaches the user. Especially valuable after a previous design was rejected as generic or template-like.

## What's inside

- [SKILL.md](SKILL.md) — the five deny-gates, the five-step workflow, verification checklist, common failure modes
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/distinctive-design-gates ~/.claude/skills/`
**Codex:** `cp -r skills/distinctive-design-gates $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\distinctive-design-gates "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse skills\distinctive-design-gates "$env:USERPROFILE\.codex\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
