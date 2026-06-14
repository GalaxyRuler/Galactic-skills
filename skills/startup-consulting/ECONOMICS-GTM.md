# Economics & Go-to-Market

The money + market engine. Business model, GTM motion, pricing, sales, financial model, unit economics, stage metrics.

## Business model

Evaluate on repeatable unit-economic health and clear architecture.

- **Revenue architecture** — monetization must match the customer's core value metric (per seat, usage, transaction fee).
- **Cost structure** — split fixed overhead (admin salaries, office) from variable delivery cost (hosting, payment processing, onboarding).
- **Gross-margin minimums:** B2B SaaS **≥80%** · Marketplaces **≥60%** net take-rate · Hardware/physical **≥50%**.
- **Channel economics** — account for every partner/broker/reseller cost so final margins stay healthy.
- **Customer metrics:**
  - *CAC* = total sales + marketing spend ÷ net new customers in the period.
  - *LTV* = (ARPA × gross margin) ÷ churn rate.
  - *Payback* = CAC ÷ monthly gross profit per account. Target <12 mo mid-market B2B, <6 mo SMB/B2C.
- **Churn & retention** — track gross/net revenue retention across monthly cohorts; don't fill a leaking bucket.
- **Expansion revenue** — up-sell, cross-sell, usage growth inside existing accounts.
- **Marketplace dynamics** — balance buyer/seller liquidity; track the active ratio, search friction, take-rate, cross-side network effects.

## Go-to-market

Match the acquisition motion to account characteristics and contract value.

| Dimension | Product-Led (PLG) | Inside Sales / Mid-Market | Enterprise |
|-----------|-------------------|---------------------------|------------|
| **ACV** | $100–$5K/yr | $5K–$50K/yr | $50K+/yr |
| **Motion** | Self-serve / digital onboarding | Inside reps / demos | Field sales / custom procurement |
| **ICP** | Individual end-user | Dept head / VP | C-suite / enterprise IT |
| **Cycle** | <30 days | 30–90 days | 90–365+ days |
| **Onboarding** | Frictionless in-app | Guided training / CS | Custom integration / 90-day pro services |

- **Refine the ICP** — company size, vertical, tech stack, budget authority, internal pain.
- **Positioning** — speak to the buyer's business metric (cut cost 20%, save 15 hrs/week), not generic features.
- **Founder-led sales** — founders personally close the first 10–20 customers; never outsource early sales or hire expensive reps before the process is repeatable.
- **Funnel optimization** — track conversion at every stage (traffic → paying account); find the friction.
- **Structured experiments** — time-boxed channel tests (cold outbound, paid search, content) with budget ceilings and explicit conversion targets.

## Pricing

Pricing is a strategic lever reflecting delivered economic value.

- **Value-based** — price as a percentage of measurable value created (e.g., 10% of money saved or revenue generated), not internal cost.
- **Avoid cost-plus** — it caps profitability and ignores delivered value.
- **Avoid blind competitor-copying** — commoditizes the product and assumes the competitor optimized their pricing.
- **Value metric** — the consumption unit that scales with value (data processed, API calls, active users).
- **Packaging tiers** — Starter / Professional / Enterprise with clear feature gates and usage limits that drive expansion.
- **Freemium/trial discipline** — require a card or hard usage limits so you acquire serious buyers, not high-maintenance free users.
- **Enterprise discounts** — strict approval limits; tie any reduction to multi-year commitment or upfront payment.

## Sales

Treat early sales as structured, metric-driven discovery — not a pitch contest.

- **Qualification** — BANT / MEDDPICC adapted for early stage; drop low-probability deals fast.
- **Discovery calls** — understand current reality, bottlenecks, budget-approval process before any demo.
- **Pilots / PoCs** — never free and open-ended; require a signed agreement with explicit success criteria and a commit-to-buy if met.
- **Procurement** — prepare early for security reviews, compliance checks, legal terms, vendor onboarding.
- **Pipeline metrics** — win rate, average deal size, stage-by-stage conversion speed, open-opportunity volume.

## Financial modeling

A model is a dynamic operational toolkit built on explicit levers, not a static forecast.

- **Bottom-up revenue** — drive forecasts from operational inputs (outbound activity, conversion rates, active accounts, ACV), never arbitrary growth rates.
- **Opex completeness** — fully loaded payroll, onboarding cost, hosting that scales with usage, insurance, realistic channel spend.
- **Scenario & sensitivity** — Base / Stress / Upside; test survival when sales cycles double or churn spikes 50%.
- **Burn & runway:**
  ```
  Net Burn Rate = Total cash inflows − Total cash outflows (monthly)
  Runway        = Current cash balance ÷ Net burn rate
  ```
- **Milestone mapping** — the raise must buy runway to a valuation-inflection point (e.g., 50 active enterprise accounts, NRR >110%).

## Unit economics

Audit to true components; strip out blended or misleading math.

- **Fully loaded CAC:**
  ```
  Fully Loaded CAC = (sales + marketing spend incl. salaries, tooling, agency fees) ÷ net new customers
  ```
- **Gross-margin LTV** — reject top-line LTV; ground it in profit:
  ```
  LTV = (ARPA × Gross Margin %) ÷ Churn Rate
  ```
- **LTV/CAC efficiency:** early-stage target **≥3:1**. **<1.5:1 → halt marketing spend** and redesign pricing or acquisition.
- **Core indicators** — contribution margin and cohort-based payback; early customers must be profitable before scaling spend.

## Metrics by stage

Track the mandatory; ignore the premature.

| Stage | Track | Ignore |
|-------|-------|--------|
| **Discovery / Validation** | interview velocity; problem-severity scores; assumption-invalidation rate | cumulative traffic; followers; theoretical ARR |
| **MVP / Testing** | activation rate; D7/D30 retention; feature-usage density | CAC; total registrations; blended LTV |
| **Launch / Early Traction** | WoW revenue growth; paid-to-free conversion; onboarding drop-off | payback trends; NPS; cross-dept overhead |
| **PMF Search** | retention stabilization; Sean Ellis %; unprompted referral rate | GMV; media impressions; headcount growth |
| **Growth / Scaling** | fully loaded CAC; LTV/CAC; NRR; Burn Multiple; runway | top-line registration counts; cumulative impressions |
