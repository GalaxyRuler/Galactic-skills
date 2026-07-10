# Test UI

Generic, stack-agnostic UI testing process for any web project — detects the project's framework and stack, then runs a phase-gated playbook covering visual regression, responsiveness, accessibility, and localization.

## What it does

- Builds a **states × breakpoints × themes × locales** inventory before testing anything
- Runs **visual regression** with determinism-first settings (pinned browser, frozen time/timezone, disabled animation, masked volatile regions)
- Covers **responsive + cross-browser** — breakpoints, ≥24px targets, reflow at 320px/400% zoom, Chromium/Gecko/WebKit, RTL mirroring
- Runs **WCAG 2.2 AA accessibility** in layers: automated (axe, light+dark) → keyboard/focus → contrast → forms → manual screen-reader spot-check
- Runs **internationalization / locale-integrity** checks — pseudo-locale pass for truncation/hardcoded strings, plus a rendered-output scan per locale for untranslated source text and raw identifiers
- Checks **design-token fidelity** — flags hardcoded values that should be tokens
- Never silently passes an un-run dimension — flags it `NOT VERIFIED` in the report instead

## When to use

Asked to UI-test, check accessibility/a11y, run visual-regression, responsive-test, audit the look and feel, verify components across themes/breakpoints/locales, or check localization/RTL rendering. Detects the project's framework/test-runner/e2e-tool/a11y-tool/i18n-library automatically and degrades gracefully when a tool is absent.

## What's inside

- [SKILL.md](SKILL.md) — the runbook: stack detection, 9-phase execution order, report format
- [playbook.md](playbook.md) — the method: why each phase exists, technique detail per phase
- [templates/i18n-integrity.spec.template.ts](templates/i18n-integrity.spec.template.ts) — starter spec for the rendered-output locale scan
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/test-ui ~/.claude/skills/`
**Codex:** `cp -r skills/test-ui $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\test-ui "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse skills\test-ui "$env:USERPROFILE\.codex\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex. Pairs well with [test-backend](../test-backend) and [test-ux](../test-ux) for full-stack coverage.
