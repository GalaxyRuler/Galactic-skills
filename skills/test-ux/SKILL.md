---
name: test-ux
description: Use when asked to UX-test, usability-test, run a UX audit, evaluate user experience, check novice-friendliness, assess whether users can complete a flow, or review content/localization clarity — generic, stack-agnostic UX testing process for any product: expert heuristic evaluation (Nielsen's 10), task-based cognitive walkthroughs, journey/state analysis, content + internationalization comprehension, and a real-user test-plan generator (moderated + unmoderated, SUS/SEQ). Pairs with playbook.md in this skill folder.
---

# /test-ux — portable UX testing runner

Execute the **UX Testing Playbook** (`playbook.md`, same folder) against the current product and emit a findings report (and a real-user test plan). Read it first — it's the method; this is the runbook. Works for any web/app product; a project-level `test-ux` overrides this when present.

**Scope:** an argument narrows to a flow/screen (`/test-ux "signup flow"`). No argument = the top tasks from Phase 0.

## Phase 0 — Detect & scope
- Find how to launch the app (project `README`/`TESTING.md`, dev script in `package.json`, or ask). Identify supported locales + text direction.
- Read a project `TESTING.md` / `docs/testing/*` / the **Project appendix** in `playbook.md` and prefer its goals/tasks/personas.
- Define the top 3–5 tasks as user goals (not features) + a one-line success criterion each; pick ≥1 novice persona.

## Runbook (see playbook.md for the why)
1. **Scope & journeys** — goals, personas (≥1 novice), top tasks, environments (every locale + text direction, mobile + desktop).
2. **Heuristic evaluation** — Nielsen's 10 per key screen; screenshot evidence; `heuristic# · screen · issue · severity 0–4 · fix`.
3. **Task walkthroughs** — drive each task step-by-step; at each step apply the 4 learnability questions; log steps-vs-optimal, dead-ends, hesitation; verdict completed/friction/failed.
4. **Journey & states** — empty/loading/low-data/error/first-run/returning; error recovery; trust & provenance.
5. **Content & i18n comprehension** — plain language, no jargon, no **raw technical identifiers** shown to users, honest tone; per locale verify meaning parity + correct direction + **no untranslated source text on the rendered page** (not just resource files).
6. **Real-user test-plan generator** — moderated + unmoderated scripts, screener, metrics sheet (task success, time, SEQ, SUS). Save alongside the report.
7. **Report** — severity-sorted findings + top-3 blockers, top-3 quick wins, and the explicit **"validate with real users"** list.

## Tools to drive when available
- A browser/preview MCP or the project's dev server for live walkthroughs + screenshots; read components / i18n files via the filesystem for the content + heuristic passes.
- If no live browser is available, do the **analytic** passes (heuristics, content, i18n from source) and mark the **task-walkthrough** dimension **NOT VERIFIED** — never report an un-run walkthrough as passed.

## Always
- Walk the full flow in **every locale**, incl. one RTL — the deep, data-dense screens (results, settings, assumptions), not just the hero. Most i18n/content bugs hide there.
- **Anti-degraded-pass:** a dimension that couldn't run = NOT VERIFIED in the report, with screenshots of the deep screens for a human glance.

## Done when
Report written + real-user test plan saved; findings severity-sorted with evidence + heuristic + fix; severity counts + top blockers printed. Any un-run dimension flagged NOT VERIFIED, not passed.
