# QA & Governance

Every AI output is reviewed as if it came from a junior consultant: potentially useful, never automatically correct. Nothing reaches a client without passing the gates, clearing professional boundaries, and getting human approval.

## QA gates (run in order; a deliverable is client-ready only when all pass)

| Gate | Check | Pass standard |
|------|-------|---------------|
| 0 — Confidentiality & tool-use | Safe to process with this tool? | Data classified, redactions applied, client policy respected |
| 1 — Input sufficiency | Enough context? | Critical missing inputs flagged before drafting |
| 2 — Scope alignment | Matches SOW & objective? | No unapproved expansion, no omitted core deliverable |
| 3 — Logic & structure | Coherent, decision-oriented? | Clear issue structure, implications, recommendation |
| 4 — Evidence & claim audit | Facts sourced, current, proportionate? | Claims sourced, qualified, or removed |
| 5 — Specificity | Tailored to this client? | Uses client context, constraints, decision criteria |
| 6 — Actionability | Client can act? | Next steps, owners, sequencing, risks present |
| 7 — Professional boundaries | Avoids legal/financial/HR/regulatory overreach? | Sensitive advice framed as considerations or escalated |
| 8 — Executive communication | Concise, polished, audience-fit? | Clear headlines, no filler, no unexplained jargon |
| 9 — Version & delivery control | Right version going out? | File name, version, status, approval correct |

## Scoring rubric (1-5 per deliverable)

| Score | Meaning |
|-------|---------|
| 1 | Unsafe / unusable — major factual, confidentiality, or scope issue |
| 2 | Rough internal draft — useful direction, not client-ready |
| 3 | Solid draft — needs targeted revisions |
| 4 | Client-ready after human review — minor refinements only |
| 5 | High-quality executive deliverable — clear, sourced, specific, actionable |

**Do not send below 4** on scope, evidence, clarity, confidentiality, and actionability. QA flags and explains — it does **not** silently rewrite risky content.

## Anti-genericity test (fast pre-send check)

| Test | Failure signal |
|------|----------------|
| Client-replacement | Swap the client name for any other company and it still reads true → too generic |
| Decision | Reader can't tell what to decide next → incomplete |
| Evidence | A factual claim can't be traced to a source or client context → risky |
| Executive skim | Main answer isn't clear in 60 seconds → too dense |
| Action | No owners, next steps, or implications → not operational |

## Deliverable checklist

Objective fit · audience fit · scope fit · evidence sourced/qualified · assumptions explicit · clear recommendation · actionable next steps · specific to this client · professional tone · no legal/financial/HR/regulatory overreach · confidentiality respected · correct file name / version / status.

## Professional boundaries (Gate 7 detail)

The system may help with — and must **not** cross into:

| Allowed support | Not allowed without expert review |
|-----------------|-----------------------------------|
| Summarizing documents for internal understanding | Legal interpretation as final advice |
| Drafting questions for counsel / accountant / HR / regulator | Recommending legally binding action |
| Issue lists and risk flags | Tax, investment, audit, employment-law determinations |
| Plain-language options | Guaranteeing legal, financial, or regulatory outcomes |

Preferred wording:

| Risky | Safer |
|-------|-------|
| "You must comply by doing X." | "This appears to be a compliance consideration to validate with counsel." |
| "This clause means…" | "For administrative tracking, this clause appears to create the following obligation; legal interpretation should be confirmed." |
| "This will reduce costs 20%." | "Under the stated assumptions, the model suggests a potential 20% reduction scenario." |
| "Terminate this role." | "This is an HR-sensitive matter requiring review under applicable policy and employment law." |

Escalate to a qualified human for binding legal, tax, regulated-financial, audit, actuarial, or employment-law matters, regulated sectors, and any guaranteed outcome.

## Human approval points (mandatory before)

Sending any client email/proposal/report/deck · submitting pricing or commercial terms · interpreting legal/financial/HR/tax/regulatory matters · uploading or processing sensitive client data · issuing strategic recommendations · reusing client-derived material · changing scope/timeline/commitments · publishing case studies or proof points.

**AI drafts; the consultant approves. Never auto-send and never claim an action was taken that wasn't.**

## Draft → critique → revise → approve loop

For any client-facing output: (1) draft with the production module → (2) critique with QA + claim audit + scope-risk → (3) revise → (4) human approves → (5) store final + update engagement memory.

## Version control

- Consistent file names (see naming convention in [TEMPLATES.md](TEMPLATES.md)).
- Archive superseded versions; mark internal drafts clearly.
- Don't send files from working folders; keep source material separate from final outputs.
- Maintain a deliverable index with owner, status, approval date.

Status labels: **Internal · Draft · For Review · Client-Ready · Approved · Superseded · Archived.**

## AI-use disclosure (when client policy/procurement requires it)

Identify the AI's role → check client AI policy → state real data protections (never claim protection the tool/agreement doesn't support) → draft transparent disclosure → obtain approval. Be transparent without over-disclosing internal tooling or implying AI performed expert judgment.

→ All templates (QA checklist, engagement memory, naming) in [TEMPLATES.md](TEMPLATES.md).
