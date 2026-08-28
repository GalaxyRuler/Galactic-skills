# Editorial Writer

Produce publication-grade long-form articles and multi-part series the way an editorial desk does — brief and thesis first, evidence ledger before prose, argument architecture before drafting, hard gates before polish. Ships an Arabic (Saudi/GCC) editorial layer for localized editions.

## What it does

- Refuses to confuse a **topic** with an **idea**: requires reader problem, thesis, original insight, and expertise basis before drafting, and returns labeled candidate theses instead of inventing authority when they're missing
- Builds a **claim-and-evidence ledger** before prose — claim type, importance, source tier, what each source actually supports, and what it does *not*
- Matches claim strength to evidence strength (the "one trial" vs. "consistently increases" failure) and records disputes instead of dropping the inconvenient source
- Produces an explicit **argument architecture** — thesis, mechanism, warrants, strongest objection, boundary conditions, implications — and gates on a paragraph-level outline before drafting
- Re-derives claims from the *drafted text* in an evidence audit, because drafting invents claims the ledger never had
- Separates **hard gates** (fabrication, unsupported core claim, wrong citation, suppressed contradiction, near-copy) from optimization metrics — a citation failure is never offset by a high readability score
- Revises one failure class at a time: argument → evidence → structure → clarity → style → search → line edit
- Treats a series as one argument distributed through time, with a per-part anti-repetition list so installments don't each re-explain the premise
- Puts search packaging last, and forbids it from changing the thesis or introducing claims
- Types every claim (factual, causal, forecast, comparative, regulatory, attribution, inference, judgment, illustration) because each carries a different evidence requirement — and demands a second independent source for high-risk claims not resting on primary evidence
- Leaves `[SOURCE NEEDED]` / `[VERIFY]` / `[EXAMPLE NEEDED]` / `[AUTHOR INPUT NEEDED]` markers instead of plausible filler, and blocks publication on an unresolved marker
- Scores headlines across six families and fails any headline asserting more than the body demonstrates
- Runs a **reverse-outline pass** on labels rather than prose — the diagnosis that works where "make it flow better" does not
- Treats a similarity score as a review trigger, never a plagiarism verdict, and separately tests originality against your own archive
- Ships an **Arabic (Saudi/GCC) layer**: native-authored MSA rather than calqued English, project termbase, verified official institution names, Arabic-appropriate readability (never an English formula), and a hard gate against widening Saudi evidence into a GCC claim
- Returns a full **publish packet** — ledgers, unresolved items, scores, metadata, named human approval — plus a corrections and freshness record
- Reports a **semantic diff** alongside the text diff — which claims moved, which qualification disappeared

## When to use

Researching, architecting, drafting, auditing, or revising a long-form article, essay, analytical piece, thought-leadership post, or multi-part editorial series — where thesis, originality, evidence, and citation integrity matter. Also for auditing citations in an existing draft, challenging a draft's argument, or planning a series.

Not for social posts, captions, five-bullet summaries, landing-page copy, release notes, or single-sentence edits. For book-length work use [developing-nonfiction-books](../developing-nonfiction-books); for verifying claims against live sources pair with [research-grounding](../research-grounding).

## What's inside

- [SKILL.md](SKILL.md) — non-negotiables and evidence markers, the five modes, the pipeline, depth-class routing, hard gates vs. optimization metrics, series rules, search packaging, output contract
- [references/RUBRICS.md](references/RUBRICS.md) — weighted scorecard, hard-gate table, claim-type taxonomy and corroboration rule, argument and evidence grading prompts, cohesion/clarity/originality diagnostics, headline scoring, similarity and archive-originality controls, diagnostics report format, trigger discipline
- [references/TEMPLATES.md](references/TEMPLATES.md) — brief, thesis triage, source card, claim ledger, disputed-claim resolution, argument architecture, section outline, article skeleton, structure library, reverse-outline pass, series manifest, revision log, publish packet, corrections log
- [references/LOCALE-AR-GCC.md](references/LOCALE-AR-GCC.md) — Arabic Saudi/GCC editorial layer: register, calque detection with before/after, geographic scoping gate, termbase format, institution names, numbers, local evidence routing, bilingual-edition rules
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/editorial-writer ~/.claude/skills/`
**Codex:** `cp -r skills/editorial-writer $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\editorial-writer "$env:USERPROFILE\.claude\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
