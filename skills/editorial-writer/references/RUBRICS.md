# Rubrics, gates, and grading prompts

Load when scoring a draft, running an audit, or deciding whether a piece is publishable.

## 1. Scorecard

Score each dimension 0–4. Weight only to prioritize revision effort — never to average away a hard-gate failure.

| Dimension | Weight | What is being judged |
|---|---:|---|
| Argument strength | 22% | Do the reasons actually support the thesis? Is the inference chain visible? |
| Evidence quality | 22% | Citation coverage and correctness, source tier, contradiction handling, claim-strength match |
| Cohesion | 15% | Does each section advance the argument, and do concepts carry across paragraphs? |
| Originality | 13% | Is the contribution more than a restatement of consensus? |
| Clarity | 10% | Is it readable at the intended intellectual level? |
| Usefulness | 10% | Can the intended reader decide or act differently? |
| Search packaging | 8% | Accurate title, natural search vocabulary, faithful metadata |

Do **not** compute `publish = weighted_average >= threshold`.

```
publishable = all_hard_gates_pass
              AND weighted_score >= agreed_threshold
              AND human_approval == true
```

## 2. Hard gates

Each is a blocking failure. Report the specific location, not a summary verdict.

| Gate | Failure condition |
|---|---|
| Fabrication | Any citation, quote, statistic, interview, or example that cannot be traced to a supplied or retrieved source |
| Core-claim support | A `core` claim with status `unsupported` or `disputed` written as established fact |
| Thesis presence | No single sentence in the piece states what it argues |
| Citation correctness | A citation points to a source that does not support the sentence it is attached to |
| Suppressed contradiction | A known contradicting source is omitted rather than addressed |
| Near-copy | Extended overlap with a source beyond marked quotation |
| Constraint violation | An explicit user constraint (length, scope, prohibition) is broken |

A gate marked `not_run` (tool unavailable, source unreachable) is reported as `not_run`. Never score a gate you did not actually check.

## 3. Argument grading

Judge the argument, not the prose. Run this against the thesis, the ledger, and the draft together.

```
For every supporting claim:
1. State the inference that links it to the thesis.
2. Test whether that inference is warranted.
3. Name the hidden assumption it requires.
4. Name the strongest plausible competing explanation.
5. Score evidence fit 0–4 — does the source support the claim at the
   strength the sentence asserts?

Then score: cogency, relevance, counterargument quality,
boundary-condition awareness, practical implication.

Do not reward confident language.
Do not infer evidence that is absent.
Report the weakest link, not the average.
```

Checks that catch the common failures:

- Is a causal claim resting on correlational evidence?
- Is a single example being used as population evidence?
- Does every section advance the argument, or do some only restate it?
- Is the objection addressed the strongest one, or a convenient weak one?
- Are the conditions under which the recommendation fails stated anywhere?

## 4. Evidence grading

Per claim, record: id, claim, type (fact / interpretation / experience / inference), importance, sources, source tier, the exact span that supports it, support status, contradicting sources, and required qualification.

Then compute, by hand or by tool:

```
citation_coverage    = supported material claims / all material claims
citation_correctness = citations whose source entails the sentence / citations checked
primary_source_ratio = primary sources / evidentiary sources
```

Coverage and correctness are separate problems. A piece can cite everything and still be wrong: a reference attached to a sentence does not make the sentence true, and adding more references does not raise correctness.

Source tiers, highest first: primary research, original data or documents, first-hand observation and interviews, reputable secondary reporting, vendor or advocacy material, aggregator and content-farm pages. Prefer the highest tier available and say which tier is carrying a core claim.

## 5. Cohesion

Judge without scripts by reading for:

- **Entity carryover** — do the concepts a paragraph introduces reappear in the next, or does each paragraph start fresh?
- **Progression** — adjacent paragraphs that say nearly the same thing are repetition, not cohesion. Both extremes fail.
- **Heading fidelity** — does each section deliver what its heading promises?
- **Reference clarity** — every "this", "that", "it" resolves to one obvious antecedent.
- **Orphans** — a paragraph that could be deleted without loss is an orphan; cut it.
- **Frame closure** — does the conclusion engage the concepts the opening raised?

## 6. Clarity

Diagnose causes, not a single number. Useful signals: median and 90th-percentile sentence length, sentence-length variance (uniform length reads as machine cadence), paragraph-length distribution, passive-voice rate, nominalization rate, jargon density, and count of specialist terms used before being defined.

Do not force elementary readability on an expert audience. The target is **clarity at the intended intellectual level**, not minimum syllable count. A readability score improved by shortening sentences while destroying a qualification is a regression.

## 7. Originality

Two separate checks — textual and intellectual.

**Textual overlap:** longest matching phrase against each source, plus sentence-level nearest matches. Any extended match must be quoted and attributed or rewritten.

**Intellectual novelty:** low textual overlap does not prove an original idea — a model can rephrase consensus fluently. Grade the contribution:

| Score | Contribution |
|---:|---|
| 0 | Derivative restatement of consensus |
| 1 | Minor synthesis of known material |
| 2 | Useful reframing |
| 3 | Distinctive application, mechanism, or context |
| 4 | Genuinely novel framework, finding, or argument |

Name the closest pre-existing idea and state exactly what is new relative to it. **New terminology is not a new idea** — renaming a known concept scores 0.

If the author supplied no expertise basis, cap the reported originality claim and say why.

## 8. Diagnostics report format

Return diagnosis before any rewrite.

```
GATES        pass / fail (list each failure with location)

Argument     3/4    Evidence     2/4    Cohesion    3/4
Originality  2/4    Clarity      4/4    Usefulness  3/4
Search       3/4

ISSUES (ranked)
1. [gate] C7 "adoption doubled" — source S3 covers one segment only
2. [argument] Section 4 restates section 2; no new inference
3. [evidence] Strongest objection (cost of switching) never addressed
4. [originality] Thesis ≈ consensus + new label

RECOMMENDED PASSES  evidence → argument → structure
NOT RUN             textual-overlap check (sources S5, S6 unreachable)
```

Rank by severity, not by reading order. Say which pass fixes what, and stop — do not begin rewriting until the user picks.

## 9. Trigger discipline

This skill should fire on: long-form article requests, series planning, citation audits, argument challenges, draft diagnosis.

It should **not** fire on: single-sentence grammar fixes, social captions, five-bullet summaries, landing-page copy, release notes. A skill that produces excellent articles but activates on every writing request is defective. When the request is smaller than the machinery, say so and do the small thing.
