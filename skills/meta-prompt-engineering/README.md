# Meta-Prompt Engineering

Treat an agent's instruction layer as a small executable specification for probabilistic software —
a versioned contract with a trust model, a runtime contract, machine-verifiable stop conditions, a
token budget, and tests — instead of a persona paragraph that grows a clause after every bug.

## What it does

- Defines the **layered orchestration contract** that replaces a monolithic "be a smart helpful
  agent" prompt: mission → instruction hierarchy → scope/authority → runtime and tool contract →
  operating loop → output contract → failure policy → stop conditions → evaluation hooks
- Encodes an explicit **trust ladder** (platform > application > authenticated user > tool and
  retrieved content > content quoted inside it) so external text can supply facts without ever
  acquiring authority — the structural fix for indirect prompt injection, paired with the honest
  caveat that no prompt makes injection impossible
- Applies one governing principle — **every requirement gets exactly one strongest enforcement
  point** — with a placement table that moves schema, permissions, retry ceilings, dedup, and
  completion predicates out of prose and into code, then *deletes* the duplicated clause
- Catalogs **fifteen structural failure modes** (conflicting instructions, instruction overload,
  capability hallucination, vague delegation, premature completion, loops, schema drift, data
  mistaken for instructions, stale runtime assumptions, persona overfitting, judge drift, leakage,
  optimizer overfitting…) with the trace signal that identifies each and its correction
- Ships **eight ready meta-prompt templates**: compact orchestrator, tool-using executor,
  multi-agent coordinator, delegation payload schema, injection-resistant retrieval analyst,
  error-recovery prompt, judge rubric, and a prompt debugger whose last rule is that it may not
  declare its own candidate the winner
- Makes prompt work **eval-first**: an evaluation pyramid, trajectory-level metrics (not just final
  answer), a five-class test corpus with tool mocks that fail in ten distinct ways, metamorphic
  tests including long-context positioning, LLM-judge design, blind human A/B, and release gates
  where improvements must reproduce on a sealed holdout
- Sets a defensible **token budget** — roughly 700–2,000 tokens for a general orchestrator core —
  because instruction-following degrades as constraint density rises and long-context models use
  mid-context material less reliably than the edges

## When to use

Writing or refactoring a system/orchestrator prompt for an unattended agent; diagnosing structural
misbehavior (loops, wrong or excessive tool calls, invented capabilities, premature "done", leaked
internal deliberation, schema drift, obeying instructions found in retrieved content); splitting an
overloaded mega-prompt into planner / executor / verifier / judge; designing delegation, handoffs,
or a judge rubric; building the eval harness that decides whether a prompt change ships; or
recovering from a regression after a model upgrade.

**Not for** writing a single copy-ready prompt to paste into a chat UI — that is a task-prompt job,
not a system contract.

## What's inside

- [SKILL.md](SKILL.md) — layer taxonomy, the spine, ten hard rules, enforcement-placement table,
  the eval-first workflow, and the token-budget policy
- [references/ARCHITECTURE.md](references/ARCHITECTURE.md) — section-by-section contract with each
  section's common defect, trust model, phase-separation patterns from production agent systems,
  control-loop shape, rule-writing standard with metadata sidecar, budget table and CI checks,
  reference architecture diagram, implementation roadmap, repository layout
- [references/FAILURE-MODES.md](references/FAILURE-MODES.md) — the fifteen failure modes with root
  cause, trace signal, and correction, plus a triage order that checks runtime truth and
  deterministic controls *before* anyone edits prose
- [references/TEMPLATES.md](references/TEMPLATES.md) — the eight templates, with placeholders meant
  to be filled from runtime configuration
- [references/EVALUATION.md](references/EVALUATION.md) — eval pyramid, twenty-two metrics, test
  corpus and manifest format, tool-mock failure matrix, metamorphic tests, model and stochastic
  testing, judge design, human rubric, release gates, risk register
- [scripts/prompt_lint.py](scripts/prompt_lint.py) — stdlib-only CI linter: token budget,
  instruction density, near-duplicate rule detection, capability sync against a live tool registry
  (and it *rewards* a runtime-injected registry by skipping the check), and normative-rule → test-ID
  coverage. `--json` for pipelines, `--selftest` runs fully offline

## Install

**Claude Code:**

```bash
cp -r skills/meta-prompt-engineering ~/.claude/skills/
```

**Codex:**

```bash
cp -r skills/meta-prompt-engineering $CODEX_HOME/skills/
```

**Windows (PowerShell):**

```powershell
Copy-Item -Recurse skills\meta-prompt-engineering "$env:USERPROFILE\.claude\skills\"   # Claude Code
Copy-Item -Recurse skills\meta-prompt-engineering "$env:USERPROFILE\.codex\skills\"    # Codex
```

## Quick check on an existing prompt

```bash
python skills/meta-prompt-engineering/scripts/prompt_lint.py path/to/system_prompt.md \
    --budget 2000 --registry tools.json --require-test-ids
```

Exit code 1 means at least one gate failed — wire it into CI next to the prompt files it guards.
