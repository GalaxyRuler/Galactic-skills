# Scoring, Risk & Anti-Patterns

One rubric governs scoring. It is weighted, but the weighted average **never** overrides a critical flaw in a high-importance CSF — that override is the whole reason a flat scorecard is dangerous on its own.

---

## Unified weighted rubric

Score each category 1-5. Weights are defaults summing to 100 — **re-weight toward the deal-specific CSFs** before scoring.

| Category | Wt | Strong (5) | Weak (1) | Key red flags |
|----------|---:|------------|----------|---------------|
| **Thesis fit & investor edge** | 8 | Fits stage/sector/geo/check/ownership/values; you can add unique value | Outside thesis; no edge; wrong stage or check | "Interesting" but not investable-for-you; no way to help or source follow-ons |
| **Founder / team** | 18 | Exceptional relevant skill, resilience, integrity, complementary roles, self-aware | Generic team; missing critical function; evasive or arrogant | Co-CEO/family/sole-founder risk unmitigated; no CTO in a technical company; blind to gaps |
| **Problem & customer pain** | 8 | Specific customer, urgent budgeted pain, strong "why now" | Vague pain; "everyone" customer; vitamin not painkiller | Founder describes features instead of pain; no customer specificity |
| **Product / tech / defensibility** | 12 | Live or appropriately advanced; core feature materially better; real moat | Demo-only; copycat risk; no technical depth | Easily copied; not compliant or not scalable in a regulated space |
| **Market / competition / timing** | 12 | Large, growing; credible beachhead; clear catalyst; nuanced competitor view | TAM inflation; no wedge; ignores funded rivals | "No competitors"; rivals all "bad"; premature exit talk |
| **Traction & customer proof** | 12 | Metrics fit stage; growth *with* retention; customers validate value | Vanity metrics; stalled/declining core metrics; no retention | Unexplained slowdown; high churn; GMV shown as revenue |
| **Go-to-market & business model** | 10 | Repeatable channel; credible CAC/payback; pricing tied to value | No acquisition method; manual-only; unrealistic funnel | "We just need more leads"; 100% conversion assumptions |
| **Financials, runway & use of funds** | 8 | Clear burn/runway; use of funds maps to milestones; credible next round | Short runway; vague use of funds; burn without growth | Raise only to survive; undisclosed debt; founder financial stress |
| **Cap table, ownership & terms** | 8 | Clean table; founders incentivized; ESOP adequate; fundable terms | Broken table; over-diluted founders; punitive prior rights | Prior-investor control; surprise warrants; wrong conversion math |
| **Legal / regulatory / IP** | 4 | Known structure, jurisdiction, regulatory path, IP assigned | Unknown incorporation; regulatory uncertainty; IP not assigned | Compliance ignored in fintech/health/energy; KYC/legal unknown |

*(8 + 18 + 8 + 12 + 12 + 12 + 10 + 8 + 8 + 4 = 100.)*

---

## Scoring method

1. Score each category 1-5; multiply by weight.
2. **Weighted score = Σ(score × weight) ÷ 100**; × 20 → a 0-100 scale.
3. **CSF override (applied after the average):**
   - Any **high-importance CSF** with skill **≤ 2/5** → mark **critical flaw**; cap the recommendation at **Pass** (or "investigate only if fixable").
   - Any **high-importance CSF** with skill **≥ 4.5/5** and no critical flaw → mark **superpower zone**.
4. A high total **never** clears a critical flaw. A 90 with a fatal team gap is still a pass.

### Thresholds (defaults, not verdicts)

| Weighted score | Default | Conditions |
|---:|---|---|
| **85-100** | Proceed to diligence / IC | No critical flaw; key claims at least partially validated |
| **70-84** | Investigate further | Strong but material questions remain |
| **55-69** | Usually pass / narrow diligence | Only proceed on strong thesis fit + fixable gaps |
| **< 55** | Pass | Weak evidence, weak CSFs, or poor fit |
| **Any score** | Pass / pause | Integrity issue, legal/regulatory impossibility, broken cap table, or unacceptable terms |

---

## Integrating the broader dimension menu

A longer list of evaluation dimensions exists (thesis, team, problem, product, market, traction, GTM, unit economics, defensibility, valuation, terms, risk, exit, investor fit). **Treat it as a menu to draw 3-7 deal-specific CSFs from — not a mandatory flat checklist.** Forcing every deal through 14 equal dimensions is exactly the failure the CSF override guards against.

Hard quantitative benchmarks are **evidence bars inside the relevant category, applied stage-gated** — never to pre-seed/MVP:

- **NRR > 120%** — strong compounding/retention signal (growth stage).
- **LTV:CAC > 3:1** — healthy acquisition economics.
- **CAC payback < 12 months** — early-stage efficiency target.
- **Customer concentration** — a single customer > **20-25%** of recurring revenue is a flag.
- **Burn multiple** — net burn ÷ net new ARR; lower is more capital-efficient.

---

## Risk taxonomy (15 areas)

Scan every deal across all fifteen; name the live ones in the memo's risk register.

1. **Founder** — friction, equity splits, leadership gaps.
2. **Market** — too small or inaccessible for a venture outcome.
3. **Product** — fails to deliver real value or solve the core pain.
4. **Technology** — instability, heavy technical debt, dangerous platform dependence.
5. **Execution** — can't hit milestones, ship, or close.
6. **GTM** — high CAC; no repeatable, positive-ROI channel.
7. **Financing** — runs out of cash before the next milestone.
8. **Valuation** — entry price so high it forces a down-round or kills the return.
9. **Legal / regulatory** — compliance, cross-border data, national-security screens.
10. **Governance** — weak oversight, undocumented board decisions, unvested founders.
11. **Cap table** — unverified ownership or large dead-equity blocks.
12. **Concentration** — reliance on a few customers, a single supplier, or one channel.
13. **Exit** — shallow M&A history; no logical acquirers.
14. **Macro** — downturns, supply shocks, shifting capital markets.
15. **Ethical / reputation** — product integrity, data security, management transparency.

---

## Critical red flags (flag immediately)

- **Evasive founders** — won't share raw ledgers, cap table, or customer references.
- **Metrics that don't reconcile** — deck numbers ≠ bank accounts or tax filings.
- **Vague customer definition** — poorly defined target, no real market research.
- **"No competition"** claims — direct or indirect.
- **Traction imbalance** — long operating history, flat or minimal recurring revenue.
- **Inflated top-down TAM** — a percentage of a generic industry report instead of bottom-up math.
- **Unrealistic projections** — revenue scaling with no matching spend or hiring.
- **Excessive entry valuation** — price or cap detached from stage and traction.
- **Messy cap table** — significant stock with inactive co-founders, advisors, contractors.
- **Unresolved IP ownership** — code/patents held personally by founders or an outside agency.
- **Heavy customer concentration** — one client > 25% of recurring revenue.
- **Regulatory exposure** — operating in a hard-compliance space with no counsel or mitigation.
- **Unclear use of funds** — no budget or milestone tied to the raise.
- **Poor data-room hygiene** — missing records, undocumented board approvals, chaotic reporting.
- **Artificial urgency** — manufactured deadlines to bypass standard diligence.

---

## Analyst anti-patterns (traps to avoid)

- Investing because the **pitch is polished** — design ≠ business value.
- Confusing **market size with market access** — a big TAM doesn't validate a beachhead.
- Mistaking **press for traction** — features and mentions aren't demand.
- Overvaluing **vanity metrics** — signups/waitlists without churn and active usage.
- Ignoring **dilution dynamics** — entry price without modeling SAFEs and option pools.
- Ignoring **structural terms** — accepting bad liq-pref/control because valuation looks cheap.
- Ignoring **customer concentration** — not flagging a single client > 25% of revenue.
- Relying on **founder charisma** — overlooking metric discrepancies for verbal fluency.
- Assuming **accelerator affiliation removes risk** — skipping your own diligence.
- Ignoring **exit pathways** — a niche with no M&A history or logical acquirers.
- **DCF-precision** for pre-revenue ventures — false precision.
- Treating **valuation as the only term** — ignoring cap-table complexity or unvested stock.
- Failing to **construct a portfolio** — concentrating into fewer than ~10 deals.
- **Skipping legal review** — closing priced rounds or custom notes without counsel.
- Investing under **manufactured urgency** — rushing diligence out of FOMO.
