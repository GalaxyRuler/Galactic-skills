# Structural failure modes

Fifteen ways meta-prompts fail. Each row is a *structural* defect — one that rewording will not
fix. Diagnose from the signal column before editing prose; several of these are not prompt
problems at all.

| # | Failure mode | Root cause | Signal in traces | Correction |
|---|---|---|---|---|
| 1 | **Conflicting instructions** | Rules accumulated by patch, no precedence; style goals fight task goals | Model hedges, alternates between two behaviors run to run, or explains the conflict in its output | Maintain a precedence table; delete redundant rules; for unavoidable tension write explicit priority, e.g. `correctness > safety > format > brevity` |
| 2 | **Instruction overload** | Prompt grew after every bug | Later rules obeyed less than earlier ones; adherence drops as the rule count climbs | Static prompt budget + one-in/one-out review; move deterministic checks to code |
| 3 | **Capability hallucination** | Prompt names a tool or action the runtime does not expose | Agent reports an action "was not in its action set", or narrates a call that never appears in the trace | Generate the capability section from the live tool registry; never keep a second handwritten inventory |
| 4 | **Wrong or excessive tool use** | Overlapping tool descriptions, "be exhaustive" language, no cost or stop model | High redundant-call rate; repeated near-identical queries | Give each tool a discriminating *use when / do not use when* contract; add tool-cost and stopping rules |
| 5 | **Vague delegation** | Subagents receive a topic, not a contract | Subagents duplicate work, search different interpretations of the same phrase, and leave gaps | Fixed delegation schema: objective, boundaries, inputs, source/tool scope, deliverable, acceptance criteria |
| 6 | **Premature completion** | No acceptance criteria; conversational "done" confused with task completion | Final message asserts success with required artifacts absent | Verifiable completion predicates plus a distinct finalization action or sentinel |
| 7 | **Infinite or repetitive loops** | "Keep trying" with no progress test, retry budget, or memory of failed paths | Same `(action, args)` repeated after identical errors | Track `(goal, action, result)`; forbid exact retries unless state changed; cap retries; require a strategy change after repeated failure |
| 8 | **Schema drift** | Output format exists only as prose; instructions and examples disagree | Parse failures, extra prose around JSON, fields renamed under load | Provider-native structured output or application-side validation; the prompt describes semantics only |
| 9 | **Data mistaken for instructions** | Retrieved, web, or file content shares a channel with control text | Agent follows text found inside a page or tool result | Label external content untrusted, isolate it structurally, minimize privileges, enforce permissions outside the prompt |
| 10 | **Runtime assumptions become false** | Prompt hard-codes environment properties that deployment later changes | Behavior correct in staging, wrong in production; agent reasons from a stale premise | Generate environment facts from runtime state; treat environment claims as typed configuration, not static prose |
| 11 | **Persona overfitting** | Elaborate role and backstory crowd out objective and procedure | Stylish output that misses requirements; role language quoted back instead of results | One or two functional sentences: expertise, objective, authority. No fiction |
| 12 | **Examples teach the wrong thing** | A demonstration carries accidental stylistic or procedural correlations | Outputs mimic an example's structure on inputs where it does not fit | Include representative *and* edge/counterexample behavior; ablate each example to discover what the prompt actually depends on |
| 13 | **Self-critique without external signal** | Generator, critic, and judge share one blind spot | Self-assessed quality rises while task success does not | Use independent evidence: tests, tools, an alternate judge, ground truth, or human review for consequential decisions |
| 14 | **Optimization overfitting** | The optimizer saw the cases it is later judged on | Large development-set gains, flat or negative holdout | Development / regression / sealed holdout sets; rotate adversarial tests |
| 15 | **Internal discussion leakage** | Finalizer receives raw internal traces with no clean output contract | User-facing answers narrate deliberation, tool plumbing, or subagent chatter | Pass structured summaries across agent boundaries; instruct the finalizer to return a standalone response |

## Triage order

When a trace looks wrong, work down this list before touching prompt text:

1. **Did the runtime actually offer what the prompt assumes?** (modes 3, 10) — compare the injected
   tool set and environment facts against the registry. A prompt edit cannot fix a missing tool.
2. **Could a deterministic control have caught this?** (modes 6, 7, 8) — schema validation, a retry
   counter, a dedup guard, a completion predicate. If yes, that is the fix; a prompt clause is the
   weaker duplicate.
3. **Is this a trust boundary problem?** (mode 9) — the prompt clause is necessary but never
   sufficient; the permission layer is the real fix.
4. **Is the instruction set self-contradictory or simply too dense?** (modes 1, 2) — measure before
   assuming; count rules and check for duplicated intent.
5. **Only then** consider wording, examples, and structure (modes 5, 11, 12, 15).

## The one design principle behind all of these

**Every requirement should have exactly one strongest enforcement point.**

A prompt is a probabilistic steering mechanism, not an authorization boundary. Anything a schema,
permission layer, counter, state machine, or validator can guarantee should be guaranteed there —
and then removed from the prompt, not duplicated into it. Duplicated enforcement is not defense in
depth; it is instruction density spent on a rule that was already enforced.
