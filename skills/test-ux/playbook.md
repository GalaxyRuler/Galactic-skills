# UX Testing Playbook (portable)

> Stack-agnostic methodology. Pair runner: `SKILL.md` (same folder). Fill the **Project appendix** per repo.

**Question:** can a real user accomplish the goal they came for — efficiently, correctly, and with confidence — without prior expertise?

UX testing is distinct from UI testing. UI asks "is the pixel/interaction correct?"; UX asks "did the human succeed, and how did it feel?" A flow can be pixel-perfect yet fail users. This playbook covers expert evaluation an agent can run (heuristics, cognitive walkthroughs) **and** generates the artifacts for the parts only real humans can validate.

## Choose methods deliberately (the taxonomy)
UX methods split on two axes ([MeasuringU](https://measuringu.com/taxonomy-ux-research-methods/), [Userlytics 2026](https://www.userlytics.com/resources/blog/ux-research-methods/)):
- **Exploratory** (what should we build / what's the mental model) vs **Evaluative** (does this design work). Most programs need both.
- **Empirical** (observe real users: usability test, field study, A/B, heatmaps/session replay) vs **Analytic** (expert inspection without users: heuristic evaluation, cognitive walkthrough).
- **Moderated** (a facilitator probes the *why* — deeper, costlier) vs **Unmoderated** (fast, scalable, answers a *specific* question / measures behavior). ([Contentsquare](https://contentsquare.com/guides/usability-testing/methods/))

An agent (Claude) can run the **analytic + evaluative** methods directly and **generate** the empirical ones for humans to run. Method menu to pull from: usability test, task-based test, tree testing (navigation/IA), card sort, five-second test, think-aloud, A/B, heatmaps/session replay, competitor review.

## Severity (Nielsen 0–4 → shared S-scale)
4 catastrophe → S0 · 3 major → S1 · 2 minor → S2–S3 · 1 cosmetic → S3–S4 · 0 not a problem. Rate each on **frequency × impact × persistence**.

---

## Phases

### 0 — Scope & journeys
Define primary user goals, 1–3 personas (≥1 novice), and the **top 3–5 tasks** as goals ("decide whether to buy X"), not features ("use the calculator"). Fix environments: viewport set, every supported locale + text direction, entry points (cold vs deep link). Output: task list + a one-line success criterion each.

### 1 — Heuristic evaluation (analytic)
Walk each key screen against **Nielsen's 10** (checklist below), two passes (free + structured). Record `heuristic# · screen · issue · Nielsen severity 0–4 · evidence (screenshot) · fix`. ([NN/g heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/), [how-to](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/))
> 1 Visibility of status · 2 Match real world · 3 User control/undo · 4 Consistency/standards · 5 Error prevention · 6 Recognition not recall · 7 Flexibility/efficiency · 8 Aesthetic/minimalist · 9 Help recognize/recover from errors · 10 Help/docs.

### 2 — Task-based cognitive walkthroughs (analytic/evaluative)
For each top task, drive the product step-by-step. At **every step** ask the four learnability questions:
1. Will the user try the right action? 2. Will they notice the control is available? 3. Will they connect the control to their goal? 4. After acting, will they see progress/feedback?
Log: steps-vs-optimal, dead-ends, backtracks, hesitation, where a novice would guess. Verdict per task: completed / friction / failed.

### 3 — Journey & state analysis
Exercise every **state** of each surface: empty, loading, partial/low-data, error, first-run, returning. Check **error recovery** (does a wrong input/failed fetch leave the user stuck or guided back?) and **trust & provenance** (is data sourced/timestamped? are limits honest? are outbound links safe + labeled?).

### 4 — Content & comprehension (incl. i18n)
- Microcopy: plain language, no unexplained jargon, consistent terms, honest/decision-support tone (no overpromising).
- **No raw technical identifiers** surfaced to users (field keys, codes) — they should read as human language.
- Per locale: meaning parity (not literal translation), correct reading direction, numbers/currency/date formats, and **no untranslated source text leaking** — verify on the *rendered* page, not just the resource files (this is where most i18n UX bugs hide). ([Bug0 i18n](https://bug0.com/knowledge-base/internationalization-testing))

### 5 — Real-user test-plan generator (empirical, for humans)
Produce a ready-to-run study for what an agent can't judge (real success, satisfaction, comprehension):
- **Moderated script** — intro, warm-up, top tasks as scenarios (not instructions), think-aloud prompts, post-task SEQ, wrap-up.
- **Unmoderated version** — same tasks self-service (Maze/UserTesting-style), with success/abandon definitions.
- **Screener** — recruit the target persona; exclude employees/experts.
- **Metrics sheet** — task success %, time-on-task, **SEQ** (1–7/task), **SUS** (10-item, end), plus verbatim-quote capture. Modern tools also auto-flag rage-clicks / high cognitive load. ([NN/g usability 101](https://www.nngroup.com/articles/usability-testing-101/))

### 6 — Report
Severity-sorted findings (schema below) + a short narrative: top 3 task blockers, top 3 quick wins, and the explicit **"validate with real users"** list (what expert evaluation could not settle).

---

## Conventions (shared with test-ui)
**Finding schema:** `ID · Severity · Area/Location · Evidence · Heuristic/Rule · Recommendation`.
**Anti-degraded-pass:** if the live walkthrough / bilingual review can't run, report it **NOT VERIFIED** (never "pass") and capture screenshots of the deep, data-dense screens for human review — the cheapest real-user review is a human glance at the actual rendered locale.
**Report path:** `docs/testing/reports/<YYYY-MM-DD>-ux.md` if that dir exists, else `./ux-test-report-<YYYY-MM-DD>.md`.

---

## Project appendix (FILL PER REPO — the swappable layer)
- **Primary goal + novice persona:** …
- **Top tasks to walk (with success criteria):** …
- **Surfaces + their states; the state contract if one exists:** …
- **Locales + text direction; trust/provenance elements to verify:** …
- **How to launch the app for live walkthroughs:** …

## References
[NN/g Usability Testing 101](https://www.nngroup.com/articles/usability-testing-101/) · [Nielsen's 10 Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) · [Conduct a heuristic eval](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/) · [MeasuringU method taxonomy](https://measuringu.com/taxonomy-ux-research-methods/) · [UX research methods 2026](https://www.userlytics.com/resources/blog/ux-research-methods/) · [usability testing methods](https://contentsquare.com/guides/usability-testing/methods/) · [i18n testing](https://bug0.com/knowledge-base/internationalization-testing)
