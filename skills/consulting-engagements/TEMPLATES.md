# Templates

Copy-paste scaffolds. Fill the brackets. Keep client data segregated by engagement (see [QA-GOVERNANCE.md](QA-GOVERNANCE.md)).

## File naming convention

```
YYYY-MM-DD_Client_Project_Artifact_vX.Y_Status
```

Example: `2026-06-14_Acme_AI-Governance_Proposal_v1.0_Client-Ready`
Status ∈ Internal · Draft · For Review · Client-Ready · Approved · Superseded · Archived.

## Engagement control file (one per client engagement)

```
# <Client> — <Project>  (control file)
Client profile:        org, sector, business model, stakeholders, terminology
Engagement scope:      objective, deliverables, timeline, in/out of scope
Decision context:      what decision, by whom, by when
Success criteria:      what "good" looks like, measurably
Confidentiality:       data class, approved tools, redaction rules, client AI policy
Assumptions register:  assumption | confidence | owner | validation step
Source ledger:         (see below)
Decision log:          decision | by whom | when | implication
Action register:       task | owner | due | status | dependency
Deliverable index:     artifact | version | status | approval date
Client preferences:    tone, format, cadence, visual style, terminology
```

## Intake brief

```
Client / project:
Trigger & context:
Problem statement:        (what's happening, why it matters, what's been tried)
Decision to support:      (what / who / by when)
Objectives & success:     (measurable)
Stakeholders:             sponsor | decision-maker | influencers | blockers | users
Scope:                    in / out / constraints / assumptions
Deliverables:             format | audience | detail | deadline
Data & access:            available materials | quality | limits
Risks:                    legal / financial / HR / regulatory / confidentiality / political
Missing critical inputs:  (ranked by delivery risk)
Safe to proceed?          yes / no — why
```

## Proposal / SOW

```
1. Executive summary       (client's problem & desired outcome, their words)
2. Understanding of need   (the decision being supported)
3. Proposed approach       (phases tied to outcomes)
4. Deliverables            (each with acceptance criteria — incl. what it will NOT include)
5. Timeline & milestones   (with client dependencies)
6. Responsibilities        (consultant / client / when)
7. Assumptions             (every premise price & timeline depend on)
8. Exclusions              (explicitly out of scope)
9. Pricing & terms         (plain commercial language — not legal advice)
10. Next steps             (one clear action)
```

## Source ledger

```
| # | Claim supported | Source (name + locator) | Date | Tier | Confidence | Notes |
|---|-----------------|-------------------------|------|------|-----------|-------|
```

A claim with no row does not appear as fact. Tier per the source hierarchy; Confidence = High/Med/Low. Model memory is not a source.

## Claim audit

```
| Claim | Type | Source | Date | Confidence | Action (keep / qualify / reframe / escalate / mark unverified) |
|-------|------|--------|------|-----------|----------------------------------------------------------------|
```

## Decision memo (answer-first, one page)

```
Decision requested:    (the ask, up top)
Recommendation:        (your answer first)
Why:                   (2-4 sourced evidence points)
Options considered:    (briefly, with why-not)
Risks & assumptions:   (including what's unverified)
Next steps:            (owner | date)
```

## Weekly status update

```
Period:                
Completed this week:   
In progress:           
Next week:             
Decisions needed:      (the ask)
Risks / blockers:      (incl. client-owned dependencies & delays)
Scope changes:         (included / clarification / paid add-on / out of scope)
```

## QA checklist (run before any client delivery)

```
[ ] Gate 0 Confidentiality classified, redactions applied
[ ] Gate 1 Critical inputs present (or flagged)
[ ] Gate 2 Within SOW / objective
[ ] Gate 3 Logic coherent, decision-oriented
[ ] Gate 4 Claim audit done — every external fact sourced/qualified/removed; no invented stats or citations
[ ] Gate 5 Specific to this client (anti-genericity)
[ ] Gate 6 Next steps / owners present
[ ] Gate 7 No legal/financial/HR/regulatory overreach; sensitive items escalated
[ ] Gate 8 Concise, executive, no filler
[ ] Gate 9 File name / version / status correct
Score (1-5) on scope, evidence, clarity, confidentiality, actionability: ___  (send only at 4+)
Human approval obtained: ___
```

## Client engagement memory (segregated; one per client/engagement)

```yaml
client: { name, sector, business_model, geography, key_terms, style_preferences }
engagement:
  project_name, objective, decision_supported, sponsor, stakeholders,
  start_date, end_date, deliverables, scope_in, scope_out, success_criteria
confidentiality:
  data_classification, approved_tools, restricted_materials, redaction_rules, client_ai_policy
working_context:
  known_facts, assumptions, open_questions, risks, dependencies, constraints
evidence:
  client_sources, external_sources, source_ledger, confidence_notes
project_control:
  action_register, decision_log, issue_log, milestone_tracker, deliverable_versions
closeout:
  final_outputs, lessons_learned, reusable_assets_sanitized, case_study_permission
```

## Reusable prompt-asset format (for the consultant's own library)

```
Skill / task name:
Purpose:
When to use / do not use when:
Required inputs · optional inputs · client context required:
Confidentiality classification · source policy:
Workflow:
Output format · quality bar:
Failure modes to avoid · guardrails:
Human approval required when:
Memory update instructions:
```

Sanitize aggressively before anything enters a reusable library — no client names, metrics, quotes, or proprietary processes without permission.
