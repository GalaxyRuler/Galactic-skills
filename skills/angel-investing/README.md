# Angel Investing

Investor-side evaluation OS for early-stage deals — systematically replacing the pitch narrative with validated evidence to decide where your time and capital go. The opposite chair from `startup-consulting`.

## What it does

- Runs the three-tier funnel: 5-minute screen → 45-60 min founder interview → 3+ hr diligence, rejecting ~90% per tier so time flows to the best candidates
- Picks 3-7 deal-specific Critical Success Factors and scores them with superpower-zone / critical-flaw override — a fatal gap in a high-importance CSF caps the deal regardless of the weighted average
- Calibrates the bar to stage (pre-seed → Series-A-ready) so a pre-seed team isn't judged on SaaS unit economics
- Sanity-checks valuation, SAFE/KISS/convertible math (cap, discount, conversion, the capitalization gotcha) and priced-equity terms; models cap-table dilution
- Sizes each deal inside a portfolio (power-law, 15-30 deals, follow-on reserves) and checks investor fit
- Produces copy-paste deliverables: investment memo, screen, founder brief, risk register, diligence tracker, and a 9-prompt pack

## When to use

Screening an inbound pitch deck, preparing or running a founder interview, planning or executing due diligence, sanity-checking valuation or SAFE/convertible/term-sheet terms, reading a cap table or modeling dilution, assessing portfolio fit, or writing an investment memo and go/no-go recommendation. Triggers on pitch deck review, due diligence, SAFE/KISS/convertible note, term sheet, valuation cap, cap table, dilution, CSF, LTV:CAC, NRR, pre-seed/seed/angel. Full trigger list in the `description` of [SKILL.md](SKILL.md).

**Not for:** binding legal/tax/regulated-financial advice, or a recommendation to buy or sell a security — the skill escalates those to qualified humans. Founder-side work (building the company) → use `startup-consulting`.

## What's inside

- [SKILL.md](SKILL.md) — router: core principles, three-tier funnel, CSF + override, stage table, 8-step workflow, escalation boundaries, completion gates
- [SCREENING.md](SCREENING.md) — Tier 1 screen, CSF design, Tier 2 interview, question bank, red/green-flag library
- [DILIGENCE.md](DILIGENCE.md) — Tier 3 staged validation, evidence hierarchy + labeling, decision rules, external-verification gaps
- [VALUATION-TERMS.md](VALUATION-TERMS.md) — valuation by stage, SAFE/convertible math, priced-equity terms, cap table & dilution
- [PORTFOLIO-FIT.md](PORTFOLIO-FIT.md) — portfolio construction, investor thesis/fit, deal flow, syndicates, post-investment support
- [SCORING.md](SCORING.md) — weighted rubric + CSF override + thresholds, 15-area risk taxonomy, critical red flags, anti-patterns
- [TEMPLATES.md](TEMPLATES.md) — investment memo, screen/intake forms, founder brief, trackers, decision tree, 9-prompt pack
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/angel-investing ~/.claude/skills/`
**Codex:** `cp -r skills/angel-investing $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\angel-investing "$env:USERPROFILE\.claude\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
