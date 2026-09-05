# UX Engineering & Product Design

Authoritative, empirical, standards-based methodology for architecting, designing, testing, and deploying digital experiences.

## What it does

- Defines target markets by Job to be Done (JTBD) and the Universal Job Map, not demographics
- Structures information architecture via the three circles (Users, Content, Context)
- Builds from design tokens, maps UI components to semantic roles, applies ISO 9241-110 dialogue principles
- Integrates WCAG 2.2 AA accessibility via progressive enhancement
- Measures quality with the HEART framework and System Usability Scale (SUS)

## When to use

Designing user interfaces, conducting UX research, building design systems, reviewing accessibility compliance, planning usability testing, defining product metrics, writing JTBD statements, structuring information architecture, auditing contrast/target sizes, or evaluating design critiques. For test execution use the companion runners: [test-ui](../test-ui) for visual/responsive/a11y automation and [test-ux](../test-ux) for heuristic evaluation, walkthroughs, and SUS.

## What's inside

- [SKILL.md](SKILL.md) — operational workflow, JTBD research, information architecture, design/prototyping, accessibility, interaction design
- [TESTING-METRICS.md](TESTING-METRICS.md) — usability-testing methods, checklists, HEART/SUS measurement
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/ux-engineering ~/.claude/skills/`
**Codex:** `cp -r skills/ux-engineering $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\ux-engineering "$env:USERPROFILE\.claude\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
