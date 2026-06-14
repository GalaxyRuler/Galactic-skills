# Templates & Prompt Pack

Copy-paste deliverables and reusable prompts. Every output keeps verified facts, founder claims, and analyst inferences visibly separate (see the labeling system in [DILIGENCE.md](DILIGENCE.md)), and every memo carries the disclaimer from [SKILL.md](SKILL.md).

---

## Investment memo (IC format)

```markdown
# Investment Memo: [Company]

## 1. Executive recommendation
- Recommendation: Pass / Investigate further / Proceed to diligence / Proceed to IC
- Confidence: Low / Medium / High
- One-sentence thesis: [why this could be venture-scale]
- One-sentence concern: [the main way it dies]
- Decision ask: [what decision is needed now]

## 2. Company overview
Sector / model · geography · stage · product status · customer · founded · headcount

## 3. Deal summary
Instrument (SAFE/KISS/note/priced) · round size · cap/discount/pre-money · post-money ·
check · estimated ownership · existing investors · use of funds · runway after round · key terms

## 4. Thesis & portfolio fit
External + internal thesis fit · investor edge / ability to help · check vs budget ·
reserve implications · concentration

## 5. Founder / team
Backgrounds · founder-market fit · coverage (tech/product/sales/ops) · missing skills ·
integrity & coachability · references · red/green flags

## 6. Problem & customer pain
Target customer · pain · urgency evidence · budget owner · current alternatives · why now

## 7. Market
Beachhead vs vision market · growth drivers · timing catalyst · competitive intensity ·
exit landscape · evidence quality

## 8. Product & technology
Status / demo notes · core value-driving feature · architecture/defensibility · IP/data moat ·
risks · validation needed

## 9. Business model & GTM
Pricing · revenue type · channel · funnel · sales cycle · CAC/payback · LTV/retention · unit economics

## 10. Traction
Revenue · users · growth · retention/churn · NPS · pipeline · cohorts · evidence quality

## 11. Financials
Cash · burn · runway · gross margin · history · forecast · hiring plan · next-round need · risks

## 12. Valuation & ownership
Proposed value/cap · comps baseline · scorecard adj · implied multiple · ownership at check ·
dilution sensitivity · does ownership support target returns?

## 13. Deal terms
Convertible: cap · discount · capitalization def · trigger · maturity · MFN · info rights · pro rata · change-of-control
Equity: liq pref · participation · seniority · anti-dilution · board · protective provisions · ESOP · drag-along · info/pro rata

## 14. Cap table review
Founder ownership · ESOP granted/available/proposed · convertibles/notes · warrants ·
prior rights · pro forma after round · who pays for ESOP increase · issues

## 15. Risk register
| Risk | Severity | Evidence | Mitigation | Owner |
|------|----------|----------|------------|-------|

## 16. Diligence findings
| Claim | Evidence received | Status | Next step |
|-------|-------------------|--------|-----------|

## 17. Open questions
1. … 2. … 3. …

## 18. Recommendation
Decision · why now · what must be true · what would change the decision · next steps

_Analytical decision support based on available materials — not legal, tax, or regulated
financial advice, and not a recommendation to buy or sell a security._
```

---

## Quick screen output

```text
Company: [Name]          Stage / round: [Stage]
Recommendation: Pass / Interview / Request info        Confidence: Low / Med / High
Thesis fit: [1-2 lines]
Green flags: [bullets]   Red flags: [bullets]
Missing evidence: [bullets]
Next action: [specific]
```

## Founder meeting brief

```text
Top CSFs:
1. [CSF] — why it matters — test question — evidence needed
2. [CSF] — …
3. [CSF] — …

Meeting plan: 0-5 story/problem · 5-15 team · 15-25 product/market/competition ·
25-35 traction/GTM/unit econ · 35-42 financials/ask/cap table · 42-45 next steps + data-room ask
```

## Red-flag audit table

```text
| Area | Red flag | Severity | Why it matters | Evidence to clear |
```

## Diligence tracker

```text
| Claim | Evidence requested | Owner | Priority | Status | Decision impact |
```

## Evidence table

```text
| Claim | Source | Evidence quality | Validation needed |
```

## Minimal intake form

```text
Company · website · sector/model · geography · stage · round type · amount raising ·
valuation/cap/discount · check requested · product status · target customer · revenue ·
users · growth · retention/churn · CAC/LTV/payback · burn/runway · team · prior funding ·
cap table available? · key docs · thesis fit
```

## One-page screen

```text
[Company] — Initial Screen
1 What they do  2 Customer & pain  3 Why now  4 Team advantage  5 Product status
6 Market & competitors  7 Traction  8 Business model  9 Fundraise & terms  10 Thesis fit
11 Top 3 CSFs  12 Green flags  13 Red flags  14 Missing info  15 Initial recommendation
```

---

## Pass / Investigate / Proceed — decision tree

- **Pass now if** — no thesis fit with no exceptional reason; integrity doubt; vague customer/problem; no strong CSF; a fatal flaw in a high-importance CSF; broken cap table or prior rights; impossible/ignored regulatory issue; valuation/terms make the return implausible; portfolio budget/reserves can't support the check.
- **Investigate further if** — strong thesis fit but key evidence missing; strong founders but unvalidated traction; promising product but uncertain defensibility; big market but unclear wedge; valuation reasonable *if* claims validate; terms need clarification but aren't clearly unacceptable.
- **Proceed to diligence if** — Tier 1 passed; the interview showed credible skill in the top CSFs; early red flags are explainable/fixable; enough signal to justify data-room time; valuation/terms are in a negotiable range.
- **Proceed to IC if** — critical claims validated; team strong in deal-specific CSFs; product/market/traction support the thesis; terms and ownership understood; cap table clean enough; portfolio fit clear; remaining risks known and acceptable for the stage.

---

## Reusable prompt pack

```text
PITCH-DECK REVIEW
Review this pitch deck as a Tier 1 + Tier 2-ready screen. Separate facts, founder claims,
assumptions, and analyst judgment. Extract overview, sector, stage, ask, valuation/instrument,
team, problem, product, market, traction, GTM, financials, risks, and missing evidence.
Identify 3-7 critical success factors. Score against the rubric. Do not recommend investment;
recommend pass / investigate / proceed to diligence with confidence and exact follow-ups.
```

```text
INVESTMENT MEMO
Draft a professional investment memo for [Company] using only the provided materials.
Label every unverified founder claim. Include all 18 memo sections, a risk register, and an
evidence table. End with a recommendation and confidence level.
```

```text
FOUNDER MEETING PREP
Prepare a founder-meeting plan for [Company]. Define the top CSFs for this model/stage/market,
then a 45-minute interview with prioritized questions, follow-ups, and what evidence each
question surfaces. List likely red/green flags and the data-room docs to request if it passes.
```

```text
DUE-DILIGENCE QUESTION LIST
Build a diligence request list for [Company] from the specific unresolved claims and risks.
Group by product/tech, market/customer, team, finance, cap table, legal/regulatory, IP, terms.
For each: the claim it validates, the evidence needed, the risk if unvalidated, and must-have-
before-IC vs nice-to-have.
```

```text
RED-FLAG AUDIT
Run a red-flag audit on these materials using the red-flag library. Cover founder/team, market,
product, traction, GTM, financial, valuation, cap table, legal/regulatory, and behavioral flags.
Classify each critical / high / medium / low and state what evidence would clear it.
```

```text
VALUATION SANITY-CHECK
Sanity-check valuation for [Company]: round type, proposed value/cap/discount, scale metric,
implied multiple, ownership at the proposed check, dilution, and stage-appropriate method. Use
comps + scorecard only if comps are provided; do not invent comps. For convertibles, compute
discount price, cap price, conversion price, estimated shares, and capitalization sensitivity.
```

```text
PORTFOLIO-FIT
Assess whether [Company] fits my portfolio: budget, horizon, target size, target check, reserve
%, thesis, and existing exposure. Evaluate check size, concentration, ownership target, reserve
implications, support burden, and whether I have an edge. Recommend pass / investigate / proceed
from a portfolio-construction view only.
```

```text
RECOMMENDATION SYNTHESIS
Synthesize the analysis into: 1) one-paragraph answer, 2) weighted score, 3) CSF heat map,
4) critical red flags, 5) green flags, 6) open diligence items, 7) valuation/terms view,
8) portfolio-fit view, 9) what would change the recommendation, 10) confidence level.
Do not give personalized financial advice or tell me to invest.
```

```text
CAP TABLE & TERMS REVIEW
Review this cap table / pro forma / convertible / term sheet. Extract ownership, valuation,
conversion, liquidation, anti-dilution, ESOP, board, protective provisions, info rights,
pro rata/ROFO, MFN, and side letters. Check conversion math is consistent. Identify who pays
for the ESOP increase. Flag terms that impair future fundraising. Escalate legal issues to counsel.
```

---

## Compact response templates

```markdown
### Pitch-Deck Critique: [Company]
- Core mission clarity: …
- Isolated unverified claims: …
- Missing slides (vs standard structure): …
- Anti-patterns flagged (vanity metrics / top-down TAM): …
```

```markdown
### Investment Screen: [Company]
- Stage & metric alignment (Ladder of Proof): …
- Mandate fit (check / sector / geography): …
- Upside potential: …
- Next action: Pass / advance to diligence
```

```markdown
### Financial Model Review: [Company]
- Ledger reconciliation vs deck: …
- Runway under 30% and 50% revenue haircuts: …
- Expense disconnects (flat marketing/hiring): …
```

```markdown
### Valuation & Terms Review: [Company]
- Instrument mechanics (SAFE/note conversion): …
- Post-round dilution / investor ownership: …
- Protective-clause vulnerabilities (liq pref / pro rata): …
```
