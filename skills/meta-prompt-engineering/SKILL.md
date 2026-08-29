---
name: meta-prompt-engineering
description: Use when designing, auditing, refactoring, or evaluating a persistent instruction layer for an LLM system — agent/system/developer prompts, orchestrator and router prompts, tool-use policies, subagent delegation templates, planner/verifier/judge prompts, error-recovery prompts, output contracts, or a prompt that generates or repairs other prompts. Also use when an agent loops, picks wrong tools, invents capabilities, stops too early, leaks internal deliberation, obeys instructions found in retrieved content, or regresses after a model upgrade. Triggers on system prompt, meta-prompt, agent prompt, instruction hierarchy, prompt injection, prompt bloat, prompt regression, LLM-as-judge, delegation prompt, prompt eval.
---

# Meta-prompt engineering

## Overview

A **meta-prompt** is any reusable instruction layer that governs *how* a model interprets tasks, uses context, calls tools, delegates, verifies, recovers, and terminates. System/developer prompts, routers, tool policies, planner and verifier prompts, judge prompts, and prompt-repair prompts are all meta-prompts. A one-off user request is not.

**Core principle: a meta-prompt is a small executable specification for probabilistic software, not a persona description.** Write it like a versioned API contract with tests. The target is not the cleverest prompt — it is *the shortest maintainable instruction contract that holds across normal, edge, adversarial, long-context, tool-error, and model-upgrade conditions.*

## When to use

- Writing or refactoring a system/orchestrator prompt for an agent that will run unattended
- An agent misbehaves in a *structural* way: loops, wrong or excessive tool calls, hallucinated capabilities, premature "done", leaked internal chatter, schema drift, injection compliance
- Splitting one overloaded mega-prompt into planner / executor / verifier / judge
- Building the eval harness that decides whether a prompt change ships
- Designing subagent delegation, handoffs, or a judge rubric

**Not for:** writing a single copy-ready prompt for a human to paste into a chat UI — that is a task-prompt job. Hand off when the deliverable is one prompt, not a system.

## Layers — keep these distinct

| Layer | Job |
|---|---|
| Task input | What the user wants now |
| Context | Facts and data for that task (documents, retrieval, rows) |
| Meta-prompt | How the model behaves across tasks |
| Orchestration meta-prompt | Decomposition, delegation, verification, synthesis |
| Evaluation meta-prompt | Judges another model or agent |
| Optimizer meta-prompt | Produces or repairs prompts |

The highest-leverage fix is often *context architecture* — which tools, memories, schemas, and subagent results land in the window — not another paragraph of prose.

## The spine

Use one stable, unambiguous section order. XML tags, Markdown headers, or typed message objects all work; the separation matters, the syntax does not.

```text
identity → instruction_hierarchy → scope/authority → runtime (tools, state, budgets)
→ operating_policy → tool_policy → output_contract → failure_policy
→ completion_criteria → examples → dynamic_context (trust="untrusted")
```

## Hard rules

1. **Encode the trust ladder explicitly.** Platform policy > application policy > authenticated user > tool/retrieved/document content > content quoted inside those. Lower layers supply **facts**, never **authority**.
2. **A prompt is a steering mechanism, not an authorization boundary.** Every requirement gets exactly one *strongest* enforcement point; if a schema, permission layer, counter, or validator can enforce it, the prompt must not be the enforcer.
3. **Runtime truth is injected, never hand-maintained.** Tool names, schemas, budgets, and environment facts come from the live registry or config. A second, handwritten tool inventory is a bug waiting for a deploy.
4. **No rule without a test ID.** Every persistent instruction carries owner, rationale, test ID, priority, and token cost. One-in / one-out against a fixed budget. A clause with no plausible test is decoration — delete it.
5. **Termination must be machine-verifiable.** A sentinel action, tool call, or acceptance predicate the harness can check — never "finish when you're done."
6. **Recovery is a separate artifact.** Inject a dedicated error/format-recovery prompt on failure instead of growing the main prompt to anticipate every malformed state.
7. **Delegate with a schema, not a topic.** Objective, scope in/out, known facts, permitted tools, deliverable, acceptance criteria, effort ceiling. Bare topic labels produce duplicated and gap-ridden subagent work.
8. **Switch instruction sets on handoff; do not merge personas.** One active role's instructions at a time.
9. **The optimizer proposes; the evaluator decides.** Never let a prompt-writing model declare its own candidate better. Improvements must reproduce on a sealed holdout set.
10. **Never call a system injection-proof.** Indirect injection arrives through pages, files, and tool output; prompt-level defenses are necessary and insufficient. Pair with least privilege, sandboxing, and authorization gates.

## Enforcement placement

| Requirement | Strongest enforcement |
|---|---|
| Output parses as JSON | Structured output / schema validation |
| Agent may not call `delete` | Tool permission layer |
| Stop after N attempts | Orchestrator counter |
| No identical failed retry | State machine / dedup on `(goal, action, result)` |
| Budget not exceeded | Runtime budget controller |
| Retrieved text is untrusted | Context labeling + sandbox + prompt |
| Claims are cited | Prompt + citation validator |
| Be concise | Prompt (genuinely prompt-only) |

## Workflow — eval-first, never prompt-first

1. **Inventory and baseline.** Collect every system/router/tool/judge/recovery prompt and its model and tool dependencies. Measure current task success, cost, and failure classes. No baseline, no claim of improvement.
2. **Specify.** Convert prose into numbered requirements with precedence, authority, output and stop contracts. Assign requirement IDs.
3. **Build the corpus** before editing prose: normal, edge, failure-injection, adversarial, and stress cases (see `references/EVALUATION.md`).
4. **Refactor** into the spine — delete duplicates and conflicts, inject runtime truth, split phases whose success criteria differ.
5. **Harden the harness.** Move schema, permissions, retry and budget, dedup, and completion predicates into code.
6. **A/B the candidates**, minimum three: minimal patch, structural simplification, aggressive simplification.
7. **Red-team**: direct and indirect injection, unavailable tool, corrupted result, long-context positioning, model switch.
8. **Canary** with prompt-version metadata and a rollback path.

Run it as a loop — collect production failures, classify root cause, ask *"is this even a prompt problem?"* first, then apply the smallest change plus a regression test.

## Token budget

There is no universal optimum. Set a budget and defend it: instruction-following degrades as simultaneous constraint density rises, and long-context models use mid-context information less reliably than material near the edges. A useful starting envelope for a general orchestrator core is roughly **700–2,000 tokens** before task tools and context, with the production target being *the minimum that clears the regression suite*. Enforce it with `scripts/prompt_lint.py`, not with good intentions.

## References

- `references/ARCHITECTURE.md` — spine, trust model, phase separation, rule-writing standard, budget policy, control-loop patterns from production agent systems
- `references/TEMPLATES.md` — orchestrator, tool executor, multi-agent coordinator, injection-resistant analyst, recovery, judge, and prompt-optimizer meta-prompts
- `references/FAILURE-MODES.md` — fifteen structural failure modes with root cause, diagnosis signal, and correction
- `references/EVALUATION.md` — eval pyramid, metric set, test-class corpus, metamorphic tests, judge design, release gates
- `scripts/prompt_lint.py` — budget, duplicate-rule, capability-sync, and requirement/test-ID checks (`--selftest` runs offline)
