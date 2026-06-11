# Work Intake

A backlog item is not agent-ready until it contains enough structured context for the agent to implement, test, document, and validate the change.

Background: DEEP backlogs are Detailed appropriately, Estimated, Emergent, and Prioritized. Definition of Ready (DoR) is the criteria for whether a task is ready to start.

## Agent-ready Definition of Ready

```yaml
definition_of_ready:
  problem_statement: required
  user_value: required
  acceptance_criteria: required
  non_goals: required
  affected_areas: required
  design_notes: optional
  dependencies: required_if_any
  data_migrations: required_if_any
  api_contract_changes: required_if_any
  security_privacy_risks: required_if_any
  test_expectations: required
  observability_expectations: optional
  rollback_plan: required_for_prod_changes
  changelog_required: true|false
  semver_impact: major|minor|patch|none|unknown
```

If a required field is missing, flag the gap and ask — do not guess.

## WSJF prioritization

```yaml
wsjf:
  business_value: 1-10
  time_criticality: 1-10
  risk_reduction_or_opportunity_enablement: 1-10
  cost_of_delay: business_value + time_criticality + risk_reduction_or_opportunity_enablement
  job_size: 1-10
  score: cost_of_delay / job_size
```

WSJF = relative Cost of Delay ÷ relative job size. Higher score = do sooner. Re-score continuously in flow-based systems.
