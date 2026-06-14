# Valuation, Terms & Cap Table

Price is one variable. Ownership, dilution, and the structural terms around the price often matter more. This module covers stage-appropriate valuation, the math behind convertibles and priced rounds, and how to read a cap table for dilution.

> Early-stage valuation is **mostly judgment, lightly science.** Use ranges, comps, and scorecards; label every assumption; never present a single-point figure as precise. The point of the math below is sanity-checking, not false precision.

---

## Valuation by stage

| Stage | Primary method | Sanity check |
|-------|----------------|--------------|
| **Pre-seed / seed** | Fixed range + scorecard; limited comps | Does the implied ownership fit a venture return at all? |
| **Early** | Market comps + scorecard | VC method, *if* assumptions exist |
| **Later** | Robust market comps | DCF / VC method where the data genuinely supports it |

Match the method to the evidence available. A discounted-cash-flow model built on pre-revenue guesses is precision theater — flag it as an anti-pattern.

### Core formulas

- **Post-money valuation = pre-money valuation + new investment.**
- **Ownership ≈ investment ÷ post-money valuation** — before option-pool, convertible, and warrant dilution.
- **Scorecard valuation = market-comps baseline × total scorecard result.**

---

## Convertibles (SAFE / KISS / notes)

**Instrument shapes:**

- **SAFE — post-money** fixes the investor's ownership *before* the priced round; dilution from *other* outstanding instruments lands on the founders.
- **SAFE — pre-money** shares that dilution with the founders.
- **KISS / convertible notes** add note mechanics: maturity date, interest accrual, and a conversion trigger (usually the next priced round).

**Terms to extract on every convertible:** valuation cap, discount, capitalization definition, conversion trigger, MFN, information rights, pro rata / ROFO, corporate-transaction (change-of-control) treatment.

**The math:**

- **Conversion price = the *lower* of** the discounted-round price **or** the cap-implied price.
- **Cap-implied price per share = valuation cap ÷ the applicable capitalization definition.**
- **Shares issued = investment ÷ conversion price.**

**Capitalization-definition gotcha:** a lower cap does **not** automatically mean better ownership. The cap is divided by a "capitalization" denominator, and what counts in that denominator (option pool? other convertibles? unissued shares?) can move the per-share price more than the cap itself. Always check *what the cap is divided by* before concluding one term is better than another.

---

## Priced-equity terms

**Economic terms:**

- **Valuation & capitalization** — pre/post-money and what's in the share count.
- **Liquidation preference** — **1× non-participating is the standard.** Flag 2×+ multiples or participating preferences as founder-unfriendly and return-distorting.
- **Participation** — does the preferred take its preference *and* share the remainder? ("double dip").
- **Anti-dilution** — **broad-based weighted-average is standard.** Flag full ratchet as aggressive.
- **Pro rata** — the right to keep your ownership by investing in later rounds.

**Protective / control terms:**

- Board composition; protective provisions (veto rights); founder vesting; drag-along; voting thresholds.

**Information rights** — regular financial reporting and cap-table access.

**Professional-legal-review mandate:** term sheets, SAFEs, KISS, and stock purchase agreements must be reviewed by qualified corporate counsel before signing. This module helps you *read* terms, not *finalize* them.

---

## Cap table & dilution

- **Founder-equity health** — do the active operators still hold enough to stay motivated through multiple future rounds? Over-diluted founders are a financing risk.
- **ESOP** — an unallocated option pool (typically **10-20%**) is usually carved into the *pre-money*, which dilutes existing holders rather than the new investor. Confirm **who pays** for any increase.
- **Outstanding-security aggregation** — every SAFE, note, warrant, and promised option converts when the priced round closes. Model them together, not one at a time.
- **Standard vs pro-forma cap table** — the standard table shows today; the **pro forma** shows post-round, post-conversion. Decisions live in the pro forma.
- **Pro-forma dilution modeling** — project ownership across Series A and B to see the investor's long-term trajectory, not just the entry snapshot.
- **Dead-equity flag** — large stakes held by inactive co-founders, advisors, or past contractors are a structural problem; surface them early and expect a clean-up before the round.
