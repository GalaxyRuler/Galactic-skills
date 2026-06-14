# Validation — Problem → Product-Market Fit

The pre-PMF discovery engine. Validate the problem, find the customer, size the market bottom-up, build the leanest MVP, prove retention.

## Problem validation

Keep founders validating the problem **before any code**.

- **Severity hierarchy:**
  - *Critical* — customer loses significant capital, violates a regulatory mandate, or suffers daily operational stoppages.
  - *Moderate* — clear friction or admin drag, but core workflows still run.
  - *Low* — minor inconvenience handled by manual workarounds.
- **Frequency & urgency** — how often (hourly/daily/monthly) and how fast it must be resolved when it hits.
- **Willingness to pay** — has the prospect allocated budget or spent money on a suboptimal workaround?
- **Existing alternatives** — a messy Excel sheet or manual workaround confirms real unmet need; *doing nothing* usually means the pain is too weak to sell against.
- **Buyer vs user** — separate who feels the daily pain (user) from who controls the budget (buyer).
- **Non-leading discovery** — focus entirely on historical behavior.

> **Protocol:** Ban hypotheticals like *"Would you buy a product that does X?"* Replace with backward-looking behavioral questions: *"How did you handle this the last time it happened?"*

- **Weak signals = failure** — polite affirmations, generic compliments, "this looks interesting" are validation failures. True validation = a commitment of time, data, or money.
- **Invalidation criteria** — define a walk-away threshold up front. Example: *if fewer than 5 of 20 prospects rate the pain as an immediate top-3 priority, the problem hypothesis is structurally invalidated.*

## Customer discovery

Design and critique discovery on strict behavioral criteria.

- **Target segment** — a specific cohort of early adopters who feel the pain most acutely, not a broad market.
- **Unbiased structure** — questions about daily workflows, bottlenecks, historical spend.
- **Hard behavioral evidence** — documented past behavior over stated future intent: budgets already deployed, teams assigned to build stop-gaps.
- **Quantify pain** — exact operational/financial cost: hours wasted, customers lost, fines incurred.
- **Jobs-To-Be-Done** — the functional, emotional, and social progress sought, independent of any tool.
- **Buyer journey** — every step from problem realization to purchase: discovery, evaluation, internal approvals.
- **Switching costs** — implementation, data-migration risk, retraining time, internal political drag.
- **Purchase triggers** — the events that force a search: regulatory change, system failure, leadership transition.
- **Buying center** — users, technical buyers, procurement, economic decision-makers; their priorities and veto power.
- **Disqualifying evidence** — long delays sharing basic workflow data; a history of never paying for software.

## Market research & sizing

Reject top-down shortcuts ("$10B market, we just need 1%"). Enforce bottom-up.

```
TAM = Total target accounts globally × Annual Contract Value (ACV)
SAM = Segment of TAM reachable within current geo, regulatory, and product capability
SOM = Portion of SAM realistically captured in 12–24 months given active GTM capacity
```

```
┌──────────────────────────────────────────────┐
│ TAM — global theoretical maximum revenue      │
│ ┌──────────────────────────────────────────┐ │
│ │ SAM — bounded by geo, features, tech      │ │
│ │ ┌──────────────────────────────────────┐ │ │
│ │ │ SOM — capturable via current capacity │ │ │
│ │ └──────────────────────────────────────┘ │ │
│ └──────────────────────────────────────────┘ │
└──────────────────────────────────────────────┘
```

- **Beachhead** — dominate one concentrated niche before expanding.
- **Market timing** — structural tailwinds (infrastructure shifts, tech changes) vs headwinds (tightening, consolidation).
- **Competitive landscape** — direct threats, indirect workarounds, future structural risks; their share, features, capital.
- **Substitutes & hidden competitors** — the toughest competitor is *doing nothing*; manual workarounds and legacy habits are friction to adoption.
- **"No competitors" is a red flag** — usually means no market, or the founder missed indirect workarounds. Genuine category creation carries high education cost and long cycles.
- **Entry strategy by market type** — clone a proven model into a localized region; resegment a mature market with a low-cost alternative; or enter a blue ocean.

## MVP & product strategy

Prevent engineering waste. Scope tightly, scope for learning.

- **True purpose** — an MVP is a process to test a core value hypothesis with minimum time, effort, and code. Not a bad version of the final product.
- **Prototype vs MVP** — a prototype tests technical feasibility or visual design; an MVP tests market demand and user behavior.
- **Archetypes:**
  - *Concierge* — deliver the value completely manually to individual customers; map the exact workflow before coding.
  - *Wizard of Oz* — automated-looking front end, humans executing the back end behind the scenes.
  - *Landing page / smoke test* — value statement + clear CTA (pre-order, waitlist) to measure intent before building.
- **Manual-first** — execute all back-end workflows by hand until human capacity breaks; don't automate until the manual process is optimized and repeatable.
- **Strict scope control** — remove any feature that doesn't test the primary value hypothesis.
- **Structured prioritization** — impact-vs-effort scoring ranked by ability to de-risk core assumptions.
- **Build-Measure-Learn** — attach an explicit tracking metric to every feature *before* development.

## Product-market fit

Keep founders honest; stop premature spend.

- **Qualitative signs** — customers demanding access, strong organic word-of-mouth, urgency during onboarding.
- **Quantitative signs** — flat, predictable cohort retention over 6–12 months + consistent unprompted usage growth.
- **Sean Ellis test** — ≥40% of active users would be *"very disappointed"* if the product vanished tomorrow = strong PMF baseline.
- **False positives** — total registrations, press, download spikes, relationship-driven pilots show interest, not retention.
- **Premature-scaling warning** — never raise S&M budget while 90-day retention cohorts decay.

→ Once retention stabilizes and unit economics clear the bar, move to [ECONOMICS-GTM.md](ECONOMICS-GTM.md) and the scaling gate in [CAPITAL-SCALE.md](CAPITAL-SCALE.md).
