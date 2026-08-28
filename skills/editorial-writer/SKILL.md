---
name: editorial-writer
description: Use when researching, architecting, drafting, auditing, or revising a publication-grade long-form article, essay, analytical piece, thought-leadership post, or multi-part editorial series — where thesis, originality, evidence, argument quality, and citation integrity matter more than word count. Also use to audit citations in an existing draft, challenge a draft's argument, or plan a series. Not for social posts, captions, summaries, landing-page copy, or single-sentence copy edits.
---

# Editorial Writer

Run an editorial production system, not a one-shot copywriter. Convert a brief into a researched argument, hold a claim-and-evidence ledger, draft against an explicit architecture, audit against hard gates, then revise one failure class at a time.

Read [RUBRICS.md](references/RUBRICS.md) for the gates, scorecard, and grading prompts. Read [TEMPLATES.md](references/TEMPLATES.md) for copy-ready working forms. Load only what the current stage needs.

## 1. Non-negotiables

1. Never manufacture expertise, interviews, data, citations, quotations, statistics, or real-world examples.
2. Separate claims from evidence. A fluent unsupported claim is still a failure.
3. Distinguish sourced fact, author experience, interpretation, and inference — in the ledger and in the prose.
4. Do not begin full drafting before reader problem, thesis, novelty, authority basis, and evidence strategy exist.
5. Prefer primary sources. Record what a source actually says, not what the argument needs it to say.
6. Address the strongest opposing explanation and state boundary conditions.
7. Optimize for reader usefulness before search visibility.
8. Never imitate the phrasing, voice, or passages of a named publication or author. Target its editorial *properties*.
9. When the author's real expertise or observations are supplied, preserve them — do not smooth them into generic prose.

## 2. Modes

| Mode | Trigger | Deliverable |
|---|---|---|
| `article` | "write a long-form piece on…" | Brief → ledger → architecture → draft → diagnostics |
| `series` | "a three-part series on…" | Series thesis, part map, per-part contracts, then parts |
| `audit` | "check the citations / challenge this draft" | Diagnostics report + prioritized fix list, no rewrite |
| `refine` | "improve this draft" | Diagnosis first, then targeted passes only |

Default to `audit` when handed an existing draft with a vague "make it better." Diagnose before generating.

## 3. Pipeline

```
brief → evidence ledger → argument architecture → outline gate
      → draft → evidence audit → diagnostics → layered revision
      → search packaging → line edit → human approval
```

Never collapse stages into one pass. A style pass that runs before the evidence audit will silently launder unsupported claims into confident prose.

### 3.1 Brief

Establish, in the author's words wherever possible:

- **Reader problem** — a problem, not a topic. "AI strategy" is a topic; "leaders cannot tell which AI initiatives need central governance" is a problem.
- **Thesis** — one sentence the piece *argues*, debatable and falsifiable. Not a description of coverage.
- **Original insight** — what a sophisticated reader does not already believe.
- **Expertise basis** — research, operating experience, interviews, proprietary data, field observation.
- **Reader payoff** — the decision or behavior that changes after reading.

If thesis, originality, or authority basis is missing, **stop and ask**. Do not substitute model-generated platitudes. Offer 2–4 candidate theses explicitly labeled as hypotheses for the author to validate or reject.

If the author declines to supply an expertise basis, proceed but record an **originality ceiling** warning: the piece can be well-argued and well-sourced, but cannot claim first-hand authority.

### 3.2 Evidence ledger

Build the ledger *before* prose. One row per material factual claim — see [TEMPLATES.md](references/TEMPLATES.md).

For each claim record: id, claim text, importance (core / supporting / background), source ids, what the source actually supports, support status (`supported` / `partially_supported` / `disputed` / `unsupported`), and any contradicting source.

Match claim strength to evidence strength. This is the most common failure:

| Evidence | Supportable wording | Not supportable |
|---|---|---|
| One trial showed a gain | "In one trial, X increased" | "X increases productivity" |
| Several studies, mixed results | "Results are mixed; outcomes depend on Y" | "Studies show X works" |
| One company's experience | "At Acme, X produced Y" | "Companies that do X get Y" |

When sources conflict, record the dispute and write about *why* results differ. Never quietly drop the inconvenient source.

### 3.3 Argument architecture

Produce before outlining: thesis, reader stakes, 3–6 supporting claims each mapped to ledger rows, the mechanism that explains the problem, the strongest competing explanation, boundary conditions, and practical implications.

### 3.4 Outline gate

Paragraph-level outline. Every section states its argumentative job. Delete any section whose job is "restate the thesis." **Pause for approval here** unless the user explicitly waived gates — this is the cheapest place to catch a wrong article.

### 3.5 Draft

Open with tension: a concrete situation, a paradox, a surprising finding, or a consequential question. Ban generic throat-clearing ("In today's fast-paced world", "X has become increasingly important").

Each evidence section carries claim → evidence → warrant → example → implication. Examples must do argumentative work; a decorative anecdote is cut.

Close by returning to the opening tension and stating the broader implication. Do not summarize.

### 3.6 Evidence audit

Re-derive claims from the *drafted text*, not from the ledger — drafting introduces claims. For each: locate support, test whether the source entails the claim at the stated strength, then source it, weaken it, or cut it.

### 3.7 Diagnostics and revision

Score against the rubric in [RUBRICS.md](references/RUBRICS.md), then revise one failure class at a time, in this order:

**argument → evidence → structure → clarity → style → search packaging → line edit**

Do not fix a structure problem by rewriting the whole piece. Report what changed and why in a revision log.

## 4. Gates

**Hard gates** — block publication regardless of other scores:

- fabricated or unverifiable citation, quote, statistic, or example
- unsupported or disputed *core* claim written as established fact
- no identifiable thesis
- near-copy of a source beyond quotation
- contradicting evidence known and omitted
- explicit user constraint violated

**Optimization metrics** — readability, cohesion, pacing, section balance, title quality, search coverage, style. Improve these; never trade a hard gate for them. A citation-integrity failure is not offset by a high readability score.

Publishable requires: all hard gates pass **and** rubric score above the agreed threshold **and** a human has approved. Never self-declare a piece approved.

## 5. Series

Treat a series as one argument distributed through time, not several articles sharing a keyword.

Fix the series thesis and the reader transformation (what the reader believes before vs. after the whole series) first. Give each part a unique question, its own thesis, and an explicit **anti-repetition list** naming what it must not re-explain. Without that list, every installment regenerates the series premise and the set reads as five variants of one article.

Each part ends on an open loop the next part closes. Feedback from a published part may change later examples and emphasis; changing the series thesis requires updating the manifest and re-checking every remaining part.

## 6. Search packaging

Runs after the argument is sound, never before. Write an accurate, specific title; use the vocabulary readers actually search in headings and early paragraphs; write a meta description faithful to the piece; identify internal links with descriptive anchor text.

The packaging pass may not introduce a claim, change the thesis, or add keyword repetition that a reader would notice. Search distributes a good article; it does not decide what the article is allowed to argue.

## 7. Output

Deliver artifacts, not only prose: brief, ledger, argument architecture, article, diagnostics, warnings, revision log. Surface unresolved risks explicitly — an unavailable source is reported as unavailable, never quietly dropped and never invented.

For claim verification against live sources, pair with the `research-grounding` skill. For book-length projects, use `developing-nonfiction-books` instead.
