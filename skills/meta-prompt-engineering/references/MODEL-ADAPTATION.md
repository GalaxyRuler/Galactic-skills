# Model adaptation

Only the differences that actually change what you write. The universal parts — clear role, task,
context, constraints, output format, stated assumptions — are assumed and not repeated per model.

> **This file ages faster than anything else in the skill.** Model families, context limits, and
> API message roles change between releases. Verify against the vendor's current prompting guide
> before asserting a capability, especially anything about tools, roles, context length, or
> reasoning behavior — see the `research-grounding` skill. Prompting remains empirical and
> model-specific; vendors say so themselves.

## Quick routing

| Target | The one thing that matters most |
|---|---|
| GPT-4.1 / GPT-5 / o-series | Heading-structured sections; explicit output schema; do not instruct reasoning models *how* to think |
| Claude | XML-ish tags; rich context; rubric + "analyze first, show only the requested output" |
| Gemini | Explicit comparison dimensions; state which modality the output should be |
| Perplexity / search-enabled | Required source types, recency window, and what must *not* be a source |
| Llama / Mistral / open weights | Numbered steps, compact context, one task at a time, examples when format matters |
| Grok | Plain structure; specify tone explicitly if you want it less casual |
| Coding assistants | Exact language/framework/runtime versions, scope guards, output shape (full file vs diff) |
| Image / audio / video | Ordered attribute slots + negative constraints; earlier tokens weigh more |
| Unknown | Universal best practices, and say plainly that you are using them |

---

## GPT family (OpenAI)

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
