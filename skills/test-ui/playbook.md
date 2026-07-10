# UI Testing Playbook (portable)

> Stack-agnostic methodology. Pair runner: `SKILL.md` (same folder). Fill the **Project appendix** at the bottom per repo.

**Question:** is the interface visually correct, consistent, responsive, accessible, and correctly localized — in every state, breakpoint, theme, and locale?

**Guiding principle** (Testing Library): *"The more your tests resemble the way the software is used, the more confidence they give you."* Test user-visible behavior, not implementation details, so refactors don't break tests. ([testing-library.com](https://testing-library.com/docs/), [Kent C. Dodds](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library))

**Strategy framing:** shift-left (cheapest bug is caught before commit), risk-based (spend effort on high-traffic / high-blast-radius surfaces), Testing-Trophy shape (static base → focused unit → integration as the widest layer → thin E2E cap). ([testomat](https://testomat.io/blog/testing-pyramid-role-in-modern-software-testing-strategies/), [Testing Trophy](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications))

## The test surface = states × breakpoints × themes × locales

Don't test "the page." Test the matrix:
- **States:** default · hover · focus · active · disabled · loading/skeleton · empty · error · partial/low-data.
- **Breakpoints:** mobile (~375) · tablet (~768) · desktop (~1280) · wide (~1536).
- **Themes:** light · dark (+ high-contrast / forced-colors if supported).
- **Locales:** each language + text direction (LTR / RTL), plus a **pseudo-locale**.

---

## Phases (gate each before the next)

### 0 — Detect & inventory
Detect the stack (the skill does this: framework, test runner, e2e tool, a11y lib, i18n lib, styling). Inventory pages + reusable components; for each, list which matrix cells apply. Output: the matrix to drive the run.

### 1 — Static & build gates
Type-check, lint, and a production build must pass — type/build errors are UI bugs caught for free (shift-left). Check **design-token fidelity**: no hardcoded colors/spacing/type that bypass the token system — tokens are what make consistency structural. ([UXPin](https://www.uxpin.com/studio/blog/testing-react-ui-components-best-practices/), [OverlayQA design QA](https://overlayqa.com/blog/what-is-design-qa/))

### 2 — Component / DOM (user-centric)
Run the component suite. **Query priority:** `getByRole` → `getByLabelText` → `getByText` → (last resort) `getByTestId`/CSS. Role/label queries assert against the *accessibility tree*, so they double as an a11y smoke test and resist refactors. Reserve `testId` for cases semantic queries can't reach. Assert every state transition + the accessible name of each control. ([Kent C. Dodds](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library), [ByRole](https://testing-library.com/docs/queries/byrole/))

### 3 — Visual regression (only if it can be deterministic)
Capture across breakpoint × theme × locale on critical surfaces. **Determinism is mandatory or it's noise:**
- pin the browser version (bundled Chromium); stub/record network; **freeze time + timezone**; normalize/​preload fonts; disable animations (`prefers-reduced-motion` / CSS); `--force-device-scale-factor=1`.
- mask volatile regions (timestamps, live data, charts); for non-deterministic surfaces use **acceptance bands**, not pixel-equality.
- **per-branch baselines**; commit baseline images to VCS so diffs are reviewable in the PR. Capture baselines only from an intentionally-correct UI.
- Tooling ladder: framework-native snapshots (free) → managed/AI-perceptual diff (fewer false positives) when scale demands. ([VRT best-practices](https://bug0.com/knowledge-base/visual-regression-testing-tools), [Percy](https://percy.io/blog/visual-regression-testing/), [Playwright snapshots](https://playwright.dev/docs/test-snapshots))

### 4 — Responsive & cross-browser
Each breakpoint: no overflow / overlap / truncation / broken wrap; touch targets **≥24×24px** (WCAG 2.5.8). **Reflow** usable at 320px width and 400% zoom (1.4.10). Run the rendering engines that matter (Chromium / Gecko / WebKit) — same code renders differently per engine. ([BrowserStack UI automation](https://www.browserstack.com/guide/ui-automation-guide))

### 5 — Accessibility (WCAG 2.2 AA), layered
Automation finds only **~20–40%** of issues; **60–80% needs a human**. So:
1. **Automated** (axe-core or equiv) in CI as a required check on every PR, light + dark — clears the automatable share + catches regressions.
2. **Manual keyboard:** logical tab order, visible focus (2.4.7) + **focus appearance** (2.4.11/2.4.12), no traps, Esc closes overlays, modal focus, **dragging alternatives** (2.5.7).
3. **Contrast** (AA 4.5:1 / 3:1) in both themes; **forms** (programmatic labels, announced errors).
4. **Screen-reader** spot-check (NVDA/VoiceOver/TalkBack) on the primary flow — names, landmarks, ARIA widget operability, data-viz alternatives.
WCAG 2.2 added 9 SC over 2.1 (focus appearance, dragging, target size, accessible auth…). ([Vervali a11y 2026](https://www.vervali.com/blog/accessibility-testing-services-in-2026-the-complete-guide-to-wcag-2-2-ada-section-508-and-eaa-compliance/), [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [axe-core](https://github.com/dequelabs/axe-core))

### 6 — Internationalization / locale-integrity
The expensive, easily-missed layer. **Bundle-parity (en↔ar key match) is NOT enough** — it's blind to user-facing strings that come from the API / backend / data. Verify the **rendered output**:
- **Pseudo-locale in CI on every UI change**: a fake locale that lengthens strings, adds accents + brackets — catches truncation, clipping, encoding failures, and **hardcoded strings** before any translator is paid.
- **Rendered-output scan** in each target locale: fail on (a) raw identifier leakage (camelCase/snake_case shown as labels) and (b) any user-facing line with no target-script characters (untranslated source text), with a brand/units allowlist. *(This is the exact class bundle-parity misses.)*
- **RTL** is more than text reversal: bidi (mixed RTL/LTR in one line), layout mirroring, **icon directionality**, and number/currency/date formatting.
- **Expansion:** allow ~30% text growth (e.g. German +20–25%) — relative widths, not fixed px. UTF-8 end-to-end.
([aqua-cloud i18n](https://aqua-cloud.io/internationalization-testing/), [Bug0 i18n](https://bug0.com/knowledge-base/internationalization-testing), [pseudolocalization](https://www.transphere.com/pseudo-translation/))

### 7 — Interaction & data-viz states
Inline form validation, loading skeletons (no layout shift on resolve), error/empty states match design, charts render **and** carry a non-visual/non-color alternative, focus management on route change.

### 8 — Report
Findings table (see Conventions). Lead with a11y S0/S1, then i18n leaks, then visual regressions, then responsive/state issues. Tag each with its rule (WCAG SC / token / locale). Attach screenshots/diffs.

---

## Conventions (shared with test-ux)
**Severity:** S0 blocker · S1 critical · S2 major · S3 minor · S4 polish.
**Finding schema (every row):** `ID · Severity · Area/Location · Evidence · Rule · Recommendation`. Evidence = screenshot/diff/failing-test/repro. No evidence = hypothesis, not a finding.
**Anti-degraded-pass discipline:** if a live/visual/a11y/i18n pass can't run (no browser, server down), report that dimension as **NOT VERIFIED** — never silently "pass" — and emit screenshots of the deep, data-dense screens for human review. *(A degraded pass accepted as done is how real bugs ship.)*
**Report path:** `docs/testing/reports/<YYYY-MM-DD>-ui.md` if that dir exists, else `./ui-test-report-<YYYY-MM-DD>.md`.

---

## Project appendix (FILL PER REPO — the swappable layer)
- **Commands:** lint=`…` · build=`…` · component test=`…` · e2e=`…` · deterministic seed=`…`
- **Critical surfaces / components:** …
- **Themes / design-token source:** …
- **Locales + text direction; i18n lib; brand/units allowlist for the locale scan:** …
- **Visual-regression tool + baseline location:** …
- **Project-specific invariants** (e.g. "links render only sanitized URLs"): …

## References
[Testing Library](https://testing-library.com/docs/) · [Common RTL mistakes](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library) · [WCAG 2.2](https://www.w3.org/TR/WCAG22/) · [axe-core](https://github.com/dequelabs/axe-core) · [a11y 2026 coverage](https://www.vervali.com/blog/accessibility-testing-services-in-2026-the-complete-guide-to-wcag-2-2-ada-section-508-and-eaa-compliance/) · [Playwright snapshots](https://playwright.dev/docs/test-snapshots) · [VRT best practices](https://bug0.com/knowledge-base/visual-regression-testing-tools) · [i18n testing](https://aqua-cloud.io/internationalization-testing/) · [pseudolocalization](https://www.transphere.com/pseudo-translation/) · [Testing Trophy](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)
