---
name: angel-investing
description: Use when acting as an angel or early-stage investor evaluating a startup opportunity — screening an inbound pitch deck, preparing or running a founder interview, planning or executing due diligence, sanity-checking valuation or SAFE/convertible/term-sheet terms, reading a cap table or modeling dilution, assessing portfolio fit, or writing an investment memo and go/no-go recommendation. Triggers on pitch deck review, due diligence, SAFE/KISS/convertible note, term sheet, valuation cap, cap table, dilution, critical success factor (CSF), LTV:CAC, NRR, burn multiple, pre-seed/seed/angel, investment memo, IC recommendation.
---

# Angel Investing

Investor-side evaluation OS for early-stage deals. The job is to **replace the pitch narrative with validated evidence** and decide where your time and capital go — not to reward a polished deck or a charismatic founder. Decision support, **not** investment advice.

> **Opposite chair from the `startup-consulting` skill.** That one builds the company (founder-side); this one evaluates inbound deals (investor-side). Same disciplines — TAM, unit economics, SAFEs — read from the buyer's seat. Founder-side request → use `startup-consulting`.

## Core principles

1. **Screen for rejection first** — a 5-minute pass answers "does this deserve more time?", never "should I invest?".
2. **Thesis-fit ≠ investable-for-you** — a strong company can still be wrong for your stage, check size, geography, or edge.
3. **Pick deal-specific CSFs** — identify the 3-7 critical success factors that actually drive *this* deal; don't apply a generic rubric blindly.
4. **Superpowers and fatal flaws don't add** — a critical flaw in a high-importance CSF kills the deal regardless of a high average.
5. **Separate evidence types** — facts, founder claims, assumptions, external data, and analyst judgment stay structurally distinct.
6. **Validate, don't trust** — the founder interview produces hypotheses; diligence tests them.
7. **Don't false-precision early valuation** — use ranges, comps, scorecards; label assumptions; never a single misleading point figure.
8. **Model ownership, dilution, terms — not just price** — liquidation preference, anti-dilution, and the cap table can outweigh the headline valuation.
9. **Portfolio construction underwrites outcomes** — returns are power-law; size every check inside a diversification and reserve plan.
10. **Escalate professional issues** — legal, tax, regulatory, IP, security, and audits require qualified experts.

## The three-tier funnel (reject ~90% per tier)

| Tier | Time | Purpose | Output |
|------|------|---------|--------|
| **1 — Assess** | 5 min | Screen for rejection: thesis fit, team/product/market sanity, evidence of pain | Reject / clarify / interview |
| **2 — Evaluate** | 45-60 min | Founder interview: score CSF skill, red/green flags, how they think | Pass / request data room / deeper diligence |
| **3 — Validate** | 3+ hr | Diligence: validate decision-drivers first, then standard, then lower-risk | Memo + recommendation |

Mechanics in [SCREENING.md](SCREENING.md) (Tiers 1-2) and [DILIGENCE.md](DILIGENCE.md) (Tier 3).

## CSF model + override

Pick 3-7 Critical Success Factors per deal; rate each importance 1-10; score founder/company skill 1-5.

- **Critical flaw** — skill ≤2 in a high-importance CSF → caps the recommendation at **Pass**, regardless of total score.
- **Superpower zone** — skill ≥4.5 in a high-importance CSF with no critical flaw → a real positive signal.

A high weighted average **never** overrides a critical flaw. Full rubric, thresholds, and risk taxonomy in [SCORING.md](SCORING.md).

## Stage calibration (ground every answer here)

| Stage | Primary investor question | Appropriate bar | Do NOT expect |
|-------|---------------------------|-----------------|---------------|
| **Idea / Pre-seed** | Why is *this* team uniquely positioned for this shift? | Customer-workflow insight; bottom-up TAM | Stable unit economics; low churn |
| **MVP / Pre-product** | Can they build a stable solution at high velocity? | Working prototype; delivery cadence; IP assigned | Scaled ARR; multi-channel funnels |
| **Commercial Traction / Early Seed** | Real demand and willingness to pay? | Signed contracts/pilots; MRR/ARR; references | Mature LTV:CAC; multi-cohort retention |
| **Scalable Traction / Series-A-ready** | Repeatable, predictable, capital-efficient to scale? | Multi-cohort retention; verified channels; NRR>120%; LTV:CAC>3:1 | Organic retention persisting without management |

Apply growth-stage bars only to growth-stage companies — never penalize a pre-seed team for lacking SaaS unit economics.

## Evaluation workflow

1. **Intake & label evidence** — capture the opportunity; tag each datum documented / founder-claimed / model-derived / external / unknown; state confidence.
2. **Tier 1 screen** — reject, clarify, or advance.
3. **Design CSFs** — 3-7, each with importance, evidence quality, a test question, and the evidence that validates it.
4. **Tier 2 interview** — score CSF skill; capture exact claims to validate; separate red/green flags.
5. **Tier 3 diligence** — staged validation, decision-drivers first.
6. **Valuation, terms & cap table** — stage-appropriate value; convertible/equity terms; dilution.
7. **Portfolio fit** — check size, ownership, reserves, concentration, edge.
8. **Memo & recommendation** — pass / investigate / proceed to diligence / proceed to IC / no recommendation, with confidence.

## Reference modules

| File | Covers |
|------|--------|
| [SCREENING.md](SCREENING.md) | Tier 1 screen, CSF design, Tier 2 interview, question bank, red/green-flag library |
| [DILIGENCE.md](DILIGENCE.md) | Tier 3 staged validation, evidence hierarchy + labeling, decision rules, external-verification gaps |
| [VALUATION-TERMS.md](VALUATION-TERMS.md) | Valuation by stage, SAFE/convertible math, priced-equity terms, cap table & dilution |
| [PORTFOLIO-FIT.md](PORTFOLIO-FIT.md) | Portfolio construction, investor thesis/fit, deal flow, syndicates, post-investment support |
| [SCORING.md](SCORING.md) | Weighted rubric + CSF override + thresholds, 15-area risk taxonomy, critical red flags, anti-patterns |
| [TEMPLATES.md](TEMPLATES.md) | Investment memo, screen/intake forms, founder brief, trackers, decision tree, prompt pack |

## When NOT to use — escalate, don't improvise

Issue a disclaimer and route to a human expert for: **legal** (term sheets, SAFEs, SPAs, IP assignment) → corporate counsel; **tax** (QSBS, cross-border, entity structuring) → CPA / tax attorney; **regulated financial advice** (telling anyone to buy/sell a security, managing assets) → licensed advisor; **guaranteed outcomes** — early-stage venture is speculative with high loss rates; **high-risk regulated domains** (medical/biotech, defense/aerospace, complex fintech) → independent expert technical + regulatory review.

**Mandatory disclaimer (include in all memos/recommendations):** *"This is analytical decision support based on available materials — not legal, tax, or regulated financial advice, and not a recommendation to buy or sell any security. Confirm all terms with qualified counsel and licensed advisors before committing capital."*

## Completion criteria

An evaluation is done only when: stage classified · evidence separated from founder claims · 3-7 CSFs set and scored · critical flaws surfaced · valuation, terms, and dilution modeled · portfolio fit assessed · recommendation issued with confidence level · data gaps disclosed · professional-review boundaries stated.
