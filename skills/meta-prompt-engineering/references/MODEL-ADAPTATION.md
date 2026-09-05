# Model adaptation

Only the differences that actually change what you write. The universal parts — clear role, task,
context, constraints, output format, stated assumptions — are assumed and not repeated per model.

> **This file ages faster than anything else in the skill.** Model families, context limits, and
> API message roles change between releases. Verify against the vendor's current prompting guide
> before asserting a capability, especially anything about tools, roles, context length, or
> reasoning behavior — see the `research-grounding` skill. Prompting remains empirical and
> model-specific; vendors say so themselves.
>
> Last checked against vendor documentation: **2026-09-05**. Anything below that a vendor page now
> contradicts is wrong, not merely old — re-read the page before quoting this file.

## Quick routing

| Target | The one thing that matters most |
|---|---|
| GPT-6 Astra | Prompt the *behaviors*, not the task: autonomy, skill-precedence, prose style, delegation, test scope |
| GPT-4.1 / GPT-5.x / o-series | Heading-structured sections; explicit output schema; do not instruct reasoning models *how* to think |
| Claude | XML-ish tags; rich context; rubric + "analyze first, show only the requested output" |
| Gemini | Explicit comparison dimensions; state which modality the output should be |
| Perplexity / search-enabled | Required source types, recency window, and what must *not* be a source |
| Llama / Mistral / open weights | Numbered steps, compact context, one task at a time, examples when format matters |
| Grok | Plain structure; specify tone explicitly if you want it less casual |
| Coding assistants | Exact language/framework/runtime versions, scope guards, output shape (full file vs diff) |
| Image / audio / video | Ordered attribute slots + negative constraints; earlier tokens weigh more |
| Unknown | Universal best practices, and say plainly that you are using them |

---

## GPT-6 Astra (OpenAI)

Astra inverts the usual advice. Earlier models needed the *task* specified more sharply; Astra
follows instructions well enough that the leverage moves to specifying **behavior** — how autonomous
to be, whose instructions win, how much to test, how to write. OpenAI's own guidance names five
behaviors, each with the failure it causes when left unspecified.

| Behavior | Left unspecified, it… | Prompt the opposite |
|---|---|---|
| Initiative / follow-through | Asks a question where you wanted action | "bias towards action and carry the user's intended task to completion"; treat "can you…" / "I want to…" as instructions, not proposals; finish authorized work *before* asking for approval, so the user approves a concrete reviewable result |
| Instruction following | Pauses or diverges because a skill file said something | "The user's instructions take precedence over guidelines provided in a skill"; and when a skill does cause a pause, require it to name the exact `SKILL.md`, quote the instruction, and separate explicit requirements from its own interpretation |
| Personality / writing style | Defaults to lists, tables, jargon, stock phrases | "clear, concise paragraphs, each developing one main idea"; lists only when genuinely parallel or sequential; ban the slop list — "Bottom Line:", "delve", "leverage", "it's worth noting", "In short:", and contrastive "X, not Y" framing that introduces an alternative nobody asked about |
| Subagent delegation | Delegates less than a parallel workflow wants | "If at any point you can parallelize work by delegating tasks to another agent … you should do so"; add a legibility rule, since inter-agent messages reach humans |
| Testing / verification | Over-tests small reversible changes | "Do not write tests for reversible, low-impact changes that mirror the implementation"; stop once required checks pass unless new failures justify more |

Also worth prompting away explicitly: unsolicited warnings, disclaimers, approval flows, and
hypothetical risk checklists.

**Audit your skill files.** OpenAI strongly recommends reviewing skills and `AGENTS.md`-style files
for instructions that could steer the model, precisely because Astra follows them more faithfully
than its predecessors. That is this skill's hard rule 1 arriving as vendor guidance: a stronger
instruction-follower makes an unaudited instruction layer more dangerous, not less. Run the
`FAILURE-MODES.md` triage over every file the model loads before blaming the model.

API notes that change how prompts are packaged, not just worded:

- Model id `gpt-6-astra`, via the Responses API. Chat Completions works, but **tool calling requires
  Responses**.
- **Reasoning effort:** `none` is unsupported. Migrating from `none`/`minimal`, start at `low` and
  compare; otherwise preserve the effective level. `reasoning.effort` (Responses) /
  `reasoning_effort` (Chat Completions).
- **Change effort mid-conversation** with a `configuration_update` input item instead of rewriting
  the request — the prompt prefix stays intact, so the cache survives. Keep request-level
  `reasoning.effort` unchanged.
- **Remove** `temperature`, `top_p`, `top_logprobs` (plus `logprobs` on Chat Completions, and
  `message.output_text.logprobs` from `include` on Responses).
- **Prompt caching:** from GPT-5.5 or earlier, `prompt_cache_retention` → `prompt_cache_options.ttl`
  set to `"30m"`.
- **Async tool calling** (`async: true`, resolve by original `call_id`) lets the model keep reasoning
  while your application runs a tool — relevant to the executor loop in `TEMPLATES.md` §2, where
  CHECK no longer has to block.
- **Mid-turn steering** over a WebSocket delivers a correction into a run in progress while
  preserving completed work. A recovery prompt can now arrive *during* the turn, not only after it.
- Fast mode (`service_tier: "fast"` / `"priority"`) is unavailable with EU data residency.

## GPT-4.1 / GPT-5.x / o-series

- Structure with headings: `## Role`, `## Task`, `## Output`, `## Constraints`.
- Specify output shape explicitly — JSON, table, markdown, schema.
- Include evaluation criteria; ask for a concise rationale, never hidden chain-of-thought.
- Separate system-style instructions from the user task. Where the API supports it, split into
  System / Developer / User messages rather than one blob.
- **Reasoning models do their own thinking.** Keep the prompt on *what* and *why*; instructions
  about *how to reason* fight the model rather than help it.

## Claude

- Use XML-like sections: `<context>`, `<task>`, `<constraints>`, `<output_format>`, `<examples>`,
  `<source_material>`. They survive concatenation with arbitrary user and retrieved text, which is
  why they are the default for anything with untrusted input.
- Rich context pays off. Rubrics and revision criteria pay off for quality-critical work.
- "Analyze before drafting, but show only the requested output" is the reliable way to get
  deliberation without narration.
- Agentic tasks: explicit sub-task decomposition and stop conditions.

```xml
<role>You are a [role] with expertise in [domain].</role>
<context>[Background, audience, prior decisions, constraints.]</context>
<task>[Concrete goal in one or two sentences.]</task>
<constraints>
- [Constraint 1]
</constraints>
<output_format>[Exact structure, length, tone.]</output_format>
<quality_criteria>
Before responding, verify your answer against:
- [Criterion 1]
</quality_criteria>
```

## Gemini

- Frame the task up front; for analytical work, name the comparison dimensions rather than asking
  for "a comparison".
- Say whether the output should be visual, textual, code, or data.
- Long context is a strength — feeding source material is usually better than summarizing it first.
- Few-shot examples regulate formatting and scope well, but too many overfit the output to the
  demonstrations. Vary them deliberately.

## Perplexity and search-enabled models

- Name required source types (academic, primary, news, official docs) and excluded ones.
- Give a recency window, not the word "recent".
- Require citations per factual claim, and ask the model to separate facts, assumptions, and
  interpretation.
- Ask for source-quality evaluation, not just source presence.

## Llama / Mistral / open weights

- Direct instructions, numbered steps, explicit boundaries. Subtlety does not survive.
- Include examples whenever format matters.
- Do not rely on platform-specific tools unless availability is confirmed.
- 7B–13B: short, very direct, one task at a time. Larger or fine-tuned variants tolerate
  GPT/Claude-style structure.

## Grok

- Plain structured prompts work. Specify tone explicitly — the default register is casual.
- Real-time queries: request citations and timestamps.

## Coding assistants (Copilot, Cursor, Codex, Windsurf)

- State language version, framework version, runtime, and file boundaries.
- Say which verb applies: generate, refactor, debug, review, or explain. They produce different
  output shapes.
- Specify the deliverable: full file, patch/diff, function only, test suite, explanation.
- Ask for tests and edge cases; request minimal diffs where the codebase is established.
- Agentic coding: scope guards, explicit file paths, and a verification step. This is where a task
  prompt starts becoming a meta-prompt — if it will run unattended, use the contract in `SKILL.md`.

## Image / audio / video

- Separate the slots: subject, setting, style, composition, lighting, color, constraints.
- Include what must *not* appear.
- Say realistic vs illustrative vs cinematic vs technical vs stylized — the model will pick one
  regardless, so pick for it.
- Order matters; most models weight earlier tokens more heavily.

```text
[Subject] — [action/pose] — [setting] — [style/medium] — [composition/camera]
— [lighting] — [mood/color palette] — [aspect ratio / quality flags]

Negative: [what to avoid]
```

## Unknown model

Use universal best practices and say so:

> "I don't have specific knowledge of this model's behavior, so I'm using universal LLM best
> practices. Adapt based on what you observe."

Never invent a capability. If it is unclear whether the target supports tools, files, browsing, or
memory, say it is unclear rather than assuming either way.
