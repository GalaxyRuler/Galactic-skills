---
name: ux-engineering
description: UX engineering and product design — JTBD research, information architecture, WCAG 2.2 AA accessibility, design systems, interaction design, and measurement (HEART/SUS). Use when designing user interfaces, conducting UX research, building design systems, reviewing accessibility compliance, planning usability testing, defining product metrics, writing JTBD statements, structuring information architecture, auditing contrast/target sizes, or evaluating design critiques.
---

# UX Engineering & Product Design

Authoritative, empirical, and standards-based methodology for architecting, designing, testing, and deploying digital experiences.

## Operational workflow

1. **Discovery & research** — define target market by Job to be Done (JTBD), not demographics. Map the Universal Job Map (Define, Locate, Prepare, Confirm, Execute, Monitor, Modify, Conclude).
2. **Information architecture** — organize via the three circles (Users, Content, Context). Build organization, labeling, navigation, and search systems.
3. **Design & prototyping** — build from foundational design tokens. Map UI components to semantic roles. Apply ISO 9241-110 dialogue principles.
4. **Accessibility integration** — WCAG 2.2 AA via progressive enhancement on all structures.
5. **Testing & iteration** — validate flows via qualitative usability testing with representative users.
6. **Measurement & optimization** — track quality with HEART framework and System Usability Scale (SUS).

## JTBD research

- **Outcomes, not features.** Formula: *"When [circumstance], I want to [job], so I can [outcome] without [pain point]"*.
- **Three customer roles:** Job Executor, Product Lifecycle Support Team, Buyer.
- **Solution-agnostic interviews:** ask about workarounds, prior solutions, and anxieties. Ignore your specific software during discovery.

## Information architecture

- **Clear labeling** — no internal jargon; use the user's domain terms.
- **Progressive disclosure** — hide complexity until requested. Improves "Suitability for Learning".
- **Content portability** — structure content flexibly for multi-platform delivery (responsive web, mobile, voice).

## Interaction design

- **Dialogue principles (ISO 9241-110):** suitability for task, self-descriptiveness, controllability, error tolerance.
- **Spatial hierarchy:** use Z-depth and materials (translucent Acrylic, Liquid Glass) to separate transient controls from base content. Never use heavy transparent materials in the primary content layer.
- **Motion:** provide feedback and context. Respect system accessibility settings — animations must be disableable (WCAG 2.3.3).

## Design systems

- **Design tokens** — all colors, typography, spacing via semantic tokens (e.g., `--p-color-text-subdued`, `color.text.brand`), never hardcoded hex.
- **Forms** — identify input purposes programmatically (WCAG 1.3.5) for browser auto-fill. Errors identified in text (3.3.1), with correction suggestions (3.3.3), reversible/confirmable for financial/legal data (3.3.4).
- **Focus states** — highly visible, contrast ratio >= 3:1 against adjacent pixels (WCAG 2.4.13).
- **Navigation** — consistent relative order across pages (WCAG 3.2.3, 3.2.6).

## Accessibility (WCAG 2.2 AA)

- **Contrast:** 4.5:1 minimum for standard text, 3:1 for large text and essential non-text UI components. Color never sole means of conveying information.
- **Target sizing:** >= 24x24 CSS px (AA minimum), 44x44 CSS px (AAA enhanced).
- **Authentication:** no sole reliance on cognitive function tests without alternatives or assistive mechanisms (password managers, object recognition).
- **Redundant entry:** auto-populate or provide selection for previously entered data within a process.
- **Reflow:** content scales to 400% (320px equivalent width) without two-dimensional scrolling.

## Anti-patterns

1. **Output over outcomes** — goals based on feature delivery rather than user behavioral changes.
2. **Generic AI audit trap** — unspecialized generative AI for heuristic evaluations yields ~80% false-positive rate and can actively harm conversions.
3. **Altering validated surveys** — modifying SUS question phrasing invalidates the test and prevents benchmarking.
4. **Persona abstraction** — demographic-heavy personas lacking functional/emotional/social job context.
5. **Conversion-only tracking** — binary business metrics without experiential correlation (task success, happiness).

## Design critiques

- No subjective visual preference arguments.
- Frame critiques around validated user needs using POV statements and HMW questions.
- Justify and document decisions, especially usability/security/performance trade-offs.

## Checklists, testing methods, metrics

Pre-design/pre-dev/pre-launch checklists, testing methodology (moderated, unmoderated, tree testing, A/B), HEART/GSM framework, SUS scoring, completion criteria: [TESTING-METRICS.md](TESTING-METRICS.md).

## Source gaps

- **Visual framework conflict (Apple HIG vs Google Material):** Material = bold physical metaphors, brand flexibility, cross-platform. HIG = content deference, minimalism, platform consistency. Use Material for cross-platform MVPs, HIG for iOS-native premium.
- **JTBD vs Personas:** industry disagreement on compatibility. Some treat JTBD as persona replacement, others as complementary ("JTBD Personas").
- **Mobile specifics:** sources lack granular component-level best practices for mobile tutorial flows, gestural onboarding, wearables, or foldables.
