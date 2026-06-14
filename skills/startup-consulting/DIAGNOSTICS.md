# Diagnostics — Stage, Intake, Evidence, Decisions

The "read the situation" toolkit. Run this before prescribing anything.

## Full stage classification

| Stage | Primary goal | Key question | Evidence required | Common risks | Key metrics | Next action |
|-------|--------------|--------------|-------------------|--------------|-------------|-------------|
| **1. Idea** | Formulate clear hypotheses | What is the problem, who has it, why does it matter? | Structured list of explicit assumptions on a canvas | Falling in love with an unverified solution | # documented assumptions | Draft a customer-discovery interview guide |
| **2. Problem Discovery** | Prove the problem is painful | Do customers recognize it and seek solutions? | ≥20 qualitative interview logs showing high severity | Leading questions; polite compliments as validation | interview volume; problem-severity score | Execute structured problem interviews |
| **3. Solution Discovery** | Validate the value proposition | Does the workflow solve the verified problem? | LOI, pre-orders, or high-fidelity prototype engagement | Over-engineering a prototype before verifying fit | click-through; feedback loops | Run solution-mapping with buyers |
| **4. MVP / Prototype** | Maximize learning, minimal code | Are early adopters using the basic mechanism? | Active usage logs of a low-code / manual-first build | Scope creep; architecting for millions too early | activation rate; core-feature retention | Build a concierge / manual-first MVP |
| **5. Launch** | Baseline market entry | Does it onboard and deliver value to cold users? | First cohort of unprompted paying users onboarding | Operational breakdown; broken onboarding | onboarding completion; initial conversion | Deploy targeted GTM channel launch |
| **6. Early Traction** | Prove value retention | Is there repeatable usage and payment in the core segment? | WoW / MoM growth in engagement or revenue | Vanity metrics; ignoring silent churn | retention cohorts; MoM revenue growth | Cohort retention analysis |
| **7. PMF Search** | Stabilize a retaining cohort | Can we find a segment where retention stabilizes? | Flat / stabilized retention cohort curves | Pivoting on outliers; expanding ICP too early | NPS; Sean Ellis >40% "very disappointed" | Narrow ICP to highest-retaining segment |
| **8. Growth** | Optimize acquisition channels | Can we acquire via repeatable, cost-effective channels? | Multiple channels yielding predictable acquisition | Spending more before fixing a leaking bucket | CAC; LTV/CAC; payback period | Run structured GTM channel experiments |
| **9. Scaling** | Build an execution engine | Can we scale spend/hiring/ops without degrading economics? | Documented playbooks; predictable margins | Process paralysis; management bloat; culture dilution | Burn Multiple; sales efficiency; NRR | Formalize departments & management cadences |
| **10. Maturity** | Defend position, maximize value | How do we extract value and resist disruption? | Dominant share; stable cash flows; optimized margins | Bureaucratic stagnation; failure to innovate | FCF margin; LTV ceiling | New R&D / expansion-stage discovery |

## 20-point intake checklist

Cross-examine available data against these before any tactical recommendation. Each gap is a flagged data omission.

1. **Founder/team** — technical, commercial, domain background; full-time commitment?
2. **Target customer** — explicit, granular ICP.
3. **Problem** — specific, quantifiable pain point.
4. **Existing alternatives** — current resolution (manual workarounds, spreadsheets, internal tools).
5. **Proposed solution** — functional workflow; how it alleviates the quantified pain.
6. **Market** — TAM/SAM/SOM via bottom-up methodology.
7. **Competitors** — direct, indirect, structural.
8. **Business model** — monetization mechanism (B2B SaaS, marketplace, usage-based).
9. **Pricing** — structure, tiering, value-metric logic.
10. **Traction** — absolute revenue, active users, organic growth, retention cohorts.
11. **Product status** — wireframe / prototype / live MVP / scaled production.
12. **GTM channels** — channels being tested or scaled.
13. **Sales cycle** — touchpoint-to-closed-won duration; internal stakeholders.
14. **Costs** — monthly burn split into fixed opex vs variable acquisition.
15. **Revenue** — MRR / ARR / gross transaction volume.
16. **Funding status** — raised to date, instruments (bootstrap/SAFE/priced), exact runway.
17. **Regulatory constraints** — governing frameworks (e.g., GDPR; regional regulators such as CITC/CMA/SAMA for Saudi/GCC).
18. **Strategic goals** — explicit 12-month milestone targets.
19. **Time horizon** — months of runway to zero-cash date.
20. **Geographic footprint** — primary entry point; cross-border expansion targets.

## Evidence standards

Sort every input. Never let an unverified claim become an analytical baseline.

| Classification | Definition | Treatment |
|----------------|------------|-----------|
| **Known Fact** | Verifiable metric from a source system | Accept as analytical baseline |
| **Founder Claim** | Unverified assertion or belief | Treat as hypothesis requiring an empirical test |
| **Customer Evidence** | Documented behavior, signed contracts, unprompted usage | Strong validation within that segment |
| **Market Evidence** | Third-party data, filings, bottom-up research | Validate sizing and timing |
| **Financial Assumption** | Forward-looking estimate | Link to operational variables; run sensitivity analysis |
| **Inference** | Conclusion the agent draws from multiple points | Label explicitly; explain the logic |
| **Recommendation** | Prescribed next step | Link to validated evidence or a high-priority risk |
| **Unresolved Risk** | Threat lacking a mitigation plan | Flag as critical; address in the roadmap |

## Decision rules

Apply mechanically when scenarios are ambiguous or unvalidated:

- **Weak validation but founders want to build** → stop product scoping; mandate a 2-week customer-interview sprint; pause all dev.
- **Low urgency in discovery** → reject the segment; pivot to a new ICP or a more painful problem.
- **Market large but inaccessible** → reject the broad model; force a beachhead niche with a channel advantage.
- **CAC unknown but spend scaling** → freeze incremental ad spend; install attribution; run small channel tests to find baseline CAC first.
- **Want to scale but retention cohorts dropping** → block all scaling; refocus roadmap on onboarding friction, value, and retention.
- **MVP scope too broad** → apply impact-vs-effort; cut features that don't test the primary hypothesis; reduce scope ≥50%.
- **Fundraising readiness weak** → postpone outreach; 30-day sprint for LOIs, pilots, or unit-economics stabilization.
- **Pricing untested** → ban free B2B rollouts; mandate a paid pilot or signed LOI with explicit pricing before access.
- **Unit economics negative** → stop acquisition spend; audit delivery cost, hosting, pricing; restructure before reopening channels.

## Anti-patterns to call out

- **Advising before diagnosing** — solutions before analyzing data or stage.
- **Generic "build an MVP"** — no hypothesis, type, or success metric specified.
- **Confusing users with buyers** — GTM aimed at the daily user, ignoring the budget owner.
- **Inflated TAM** — top-down billion-dollar reports detached from the actual model.
- **Copying competitors without strategy** — mirroring pricing/features without understanding their economics.
- **Vanity metrics** — celebrating downloads/registrations/press while retention rots.
- **Premature scaling** — capital and headcount before a repeatable model and stable retention.
- **Overbuilding** — months of code for edge cases before validating the core workflow manually.
- **Fundraising as validation** — treating a closed round as proof rather than a call to execute.
- **Weak ICP** — broad target → unfocused messaging, slow cycles, high churn.
- **No pricing logic** — prices from a guess or arbitrary markup, not delivered value.
- **No retention evidence** — expanding sales while cohorts die inside 60 days.
- **Ignoring bad unit economics** — assuming scale magically fixes negative contribution margin.
- **Mistaking activity for traction** — meetings, conferences, commits ≠ revenue or commitments.
- **Decks as cure** — treating a pitch deck as a fix for unvalidated demand or broken economics.
