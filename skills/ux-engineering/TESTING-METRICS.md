# Testing & Metrics

## Checklists

### Pre-design (discovery)

- [ ] Target JTBD defined in a single, solution-free statement
- [ ] Quantitative and qualitative data identify the user's struggling moments
- [ ] Information architecture built around users, content, and context

### Pre-development (UI/UX)

- [ ] All text meets WCAG 4.5:1 (normal) or 3:1 (large) contrast
- [ ] Primary touch targets >= 24x24 CSS px (preferably 44x44)
- [ ] Forms use semantic labels, inline validation, and programmatic purpose identifiers
- [ ] Progressive enhancement used (core functions work with basic HTML before JS/CSS)
- [ ] Design evaluated against cognitive principles (error tolerance, self-descriptiveness)

### Pre-launch (testing)

- [ ] Qualitative usability testing conducted with >= 5 representative users
- [ ] Mechanism exists to capture attitudinal feedback (SUS or equivalent)
- [ ] No components entirely hidden by author-created content when receiving keyboard focus

## Testing methods

### Qualitative usability testing (moderated)

For early-stage wireframes, complex flows, deep-dive exploratory research. Use think-aloud protocol to uncover mental models and behavioral reasoning.

### Unmoderated remote testing

For polished designs, simple tasks, post-launch content validation. Users complete tasks independently.

### Tree testing & card sorting

Early design phase — evaluate information architecture and navigation hierarchy effectiveness.

### Specialized AI heuristic auditing

Domain-trained AI tools (e.g., Baymard UX-Ray) with ~95% accuracy against validated heuristic guidelines. Use for rapid structural interface error detection. Avoid generic unspecialized AI (~80% false-positive rate).

### A/B testing (CRO)

Test hypotheses when traffic is sufficient (>5,000 visitors/week). Test big ideas, unique value propositions, trust signals against existing designs.

## HEART framework & GSM model

Define success using HEART categories mapped to Goals, Signals, Metrics:

| Dimension | Measures | Example metrics |
|-----------|----------|-----------------|
| **Happiness** | Attitudinal | SUS, CSAT, NPS |
| **Engagement** | Interaction depth/frequency | Actions per session |
| **Adoption** | New user uptake | Onboarding completion rate |
| **Retention** | Continued usage | 30-day active users |
| **Task Success** | Effectiveness/efficiency | Error rates, task completion time |

## System Usability Scale (SUS)

Range 0-100, average = 68. Do NOT alter the 10 standard questions — rewording invalidates the test.

**Completion criterion:** SUS score >= 80.3 (Grade A, top 10%) = minimal user friction.

## Accessibility completion

**Completion criterion:** full WCAG 2.2 Level AA compliance.
