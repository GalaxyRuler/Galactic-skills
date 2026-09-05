---
name: test-ui
description: Use when asked to UI-test, check accessibility/a11y, run visual-regression, responsive-test, audit the look and feel, verify components across themes/breakpoints/locales, or check localization/RTL rendering — generic, stack-agnostic UI testing process for any web project: visual regression, responsive + cross-browser, WCAG 2.2 AA accessibility (axe → manual → screen reader), component/state matrix, internationalization/locale-integrity (pseudo-locale + rendered-output scan), and design-token fidelity. Detects the project's stack and runs the matching commands. Pairs with playbook.md in this skill folder.
---

# /test-ui — portable UI testing runner

Execute the **UI Testing Playbook** (`playbook.md`, same folder) against the current project and emit a findings report. Read it first — it's the method; this is the runbook. Works in any web repo; a project-level `test-ui` overrides this when present.

**Scope:** an argument narrows to a component/page/flow (`/test-ui checkout`). No argument = the critical surfaces from Phase 0.

## Phase 0 — Detect the stack (do this first)
Read `package.json` (+ lockfile, config files) and pick commands. Detect:
- **Framework:** React / Vue / Svelte / Angular / Next / Vite / CRA / SvelteKit / Astro.
- **Test runner:** Vitest / Jest / (node:test). → component tests.
- **E2E / visual:** Playwright / Cypress / WebdriverIO. → e2e, visual snapshots.
- **a11y:** `@axe-core/*`, `jest-axe`, `axe-playwright` present? → automated a11y.
- **i18n:** i18next / react-intl / vue-i18n / next-intl / lingui? → locale list, pseudo-locale, RTL.
- **Styling/tokens:** Tailwind / CSS vars / styled-system / design-tokens.
Map these to: `lint`, `build`, component-test, e2e, and how to run a single spec. If a tool is **absent**, degrade that phase to a manual checklist + a one-line setup note — never fail the run, never silently pass it.
Read a project `TESTING.md` / `docs/testing/*` / the **Project appendix** in `playbook.md` if present and prefer its commands.

## Runbook (phase-gated — see playbook.md for the why)
1. **Inventory** — build the states × breakpoints × themes × locales matrix.
2. **Static & build** — type-check + lint + build; design-token fidelity (no hardcoded values).
3. **Component/DOM** — run the suite; assert states + accessibility tree; **query priority getByRole → getByLabelText → getByText → testId-last**.
4. **Visual regression** — across the matrix on critical surfaces; **determinism first** (pin browser, freeze time/tz, normalize fonts, disable animation, `--force-device-scale-factor=1`, mask volatile regions, per-branch baselines). Review every diff.
5. **Responsive & cross-browser** — breakpoints; targets ≥24px; reflow @320px/400%; engines (Chromium/Gecko/WebKit); RTL mirroring.
6. **Accessibility WCAG 2.2 AA, layered** — axe (light+dark, zero violations) → keyboard/focus(2.4.7, 2.4.11) → contrast → forms → screen-reader spot-check. (Automation ≈20–40%; the rest is manual — don't mark manual as auto-passed.)
7. **i18n / locale-integrity** — pseudo-locale pass (truncation/clipping/hardcoded strings); **rendered-output scan** per target locale for raw identifiers + untranslated source text (allowlist brand/units); RTL bidi + icon directionality; ~30% expansion headroom.
8. **Interaction & data-viz** — validation UI, skeleton no-shift, error/empty states, charts + non-color alternative, focus on route change.
9. **Report** — write to `docs/testing/reports/<date>-ui.md` (or `./ui-test-report-<date>.md`); lead with a11y S0/S1, then i18n leaks, then visual.

## Always
- Test **both** themes and **every** locale incl. one RTL + a pseudo-locale — not just the default.
- **Anti-degraded-pass:** a pass that couldn't run = **NOT VERIFIED** in the report, with screenshots of the deep/data-dense screens for human review.
- Tools to drive when available: the project's test/e2e CLIs (via Bash), `@axe-core`, a browser-preview/Chrome MCP for live screenshots, a Lighthouse/perf skill if performance comes up.

## Done when
Report written; a11y S0/S1 + i18n leaks triaged; visual diffs reviewed; severity counts + top findings printed. Any un-run dimension is flagged NOT VERIFIED, not passed.
