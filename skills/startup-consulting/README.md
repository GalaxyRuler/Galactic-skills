# Startup Consulting

Rigorous, evidence-based startup advisory from idea validation through fundraising and scaling — systematically replacing founder assumptions with validated market facts.

## What it does

- Classifies a venture into one of 10 operational stages and tailors all advice to it
- Separates founder claims from facts, customer evidence, and inferences before recommending anything
- Runs a 12-step consulting workflow: clarify → stage → facts/assumptions → diagnose → framework → risks → options → 30/60/90 actions → validation tests → metrics → deliverable
- Applies tactical modules: problem validation, customer discovery, bottom-up TAM/SAM/SOM, MVP strategy, PMF, business model, GTM, pricing, sales, financial modeling, unit economics, fundraising, pitch-deck review, scaling gate
- Produces copy-paste deliverables (diagnostic memos, discovery plans, MVP scopes, GTM plans, pitch-deck critiques, 30/60/90 roadmaps)

## When to use

Evaluating a startup idea, validating a problem, reviewing a business model, scoping an MVP, planning go-to-market, critiquing a pitch deck, preparing to fundraise, auditing unit economics, or assessing readiness to scale. Triggers on TAM/SAM/SOM, product-market fit, runway/burn, cohort retention, CAC/LTV, SAFE/cap table, churn. Full trigger list in the `description` of [SKILL.md](SKILL.md).

**Not for:** binding legal/tax/regulated-financial advice, or guaranteed fundraising outcomes — the skill escalates those to qualified humans.

## What's inside

- [SKILL.md](SKILL.md) — router: 11 operating laws, 12-step workflow, 10-stage table, operating mode, escalation boundaries, completion gates
- [DIAGNOSTICS.md](DIAGNOSTICS.md) — full stage table, 20-point intake, evidence standards, decision rules, anti-patterns
- [VALIDATION.md](VALIDATION.md) — problem validation, customer discovery, bottom-up market sizing, MVP strategy, product-market fit
- [ECONOMICS-GTM.md](ECONOMICS-GTM.md) — business model, GTM matrix, pricing, sales, financial modeling, unit economics, metrics by stage
- [CAPITAL-SCALE.md](CAPITAL-SCALE.md) — fundraising, 13-slide pitch-deck rubric, scaling gate, operations, hiring, governance
- [TEMPLATES.md](TEMPLATES.md) — deliverable catalog, 8 response templates, readiness checklists
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/startup-consulting ~/.claude/skills/`
**Codex:** `cp -r skills/startup-consulting $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\startup-consulting "$env:USERPROFILE\.claude\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
