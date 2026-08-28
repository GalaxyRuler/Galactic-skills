# Copy-ready working forms

Load the form for the current stage only.

## 1. Editorial brief

```markdown
## Brief — {{working title}}

Reader:            {{who, and what they already know}}
Reader problem:    {{a problem, not a topic}}
Thesis:            {{one debatable sentence the piece argues}}
Original insight:  {{what a sophisticated reader does not already believe}}
Expertise basis:   {{research / experience / interviews / data / observation}}
Reader payoff:     {{what they decide or do differently}}
Stakes:            {{why now, what it costs to get wrong}}
Length:            {{min–target–max}}
Voice:             {{attributes}} | avoid: {{list}}
Constraints:       {{scope limits, prohibitions, house style}}

Assumptions made:  {{list — every gap filled without the author}}
Warnings:          {{e.g. originality ceiling: no first-hand basis supplied}}
```

## 2. Thesis triage

When handed a topic instead of an idea, return this rather than drafting:

```markdown
Diagnosis: the topic is defined; the editorial idea is not.

Questions for the author:
1. What do you believe about {{topic}} that a sophisticated reader may not?
2. What observation, data, or experience gives you authority to argue it?
3. What should the reader decide differently afterward?

Candidate theses — HYPOTHESES for you to validate or reject, not findings:
A. {{thesis}}
B. {{thesis}}
C. {{thesis}}
```

Distinguishing a topic from an idea is the point. Do not proceed on a topic alone.

## 3. Source card

```markdown
S{{n}} | {{title}} | {{author/org}} | {{date}} | {{locator}}
Type:        primary research / data / interview / reporting / vendor / notes
Tier:        1–6 (see RUBRICS.md §4)
Scope:       {{population, sector, sample, timeframe the source actually covers}}
Supports:    {{what it genuinely establishes}}
Does NOT:    {{the overreach this source will tempt}}
Conflicts:   {{source ids that disagree, and how}}
Access:      retrieved / supplied / UNAVAILABLE
```

Fill `Does NOT` for every source. It is the field that stops overclaiming.

## 4. Claim ledger

```markdown
| id | claim | type | importance | sources | status | qualification needed |
|----|-------|------|-----------|---------|--------|---------------------|
| C1 | {{claim as it will appear}} | fact | core | S1,S4 | supported | — |
| C2 | {{claim}} | inference | supporting | S2 | partially_supported | limit to {{scope}} |
| C3 | {{claim}} | fact | core | S3 vs S7 | disputed | state both, explain divergence |
```

`type`: factual / causal / forecast / comparative / regulatory / attribution / inference / judgment / illustration — each carries a different evidence requirement, see RUBRICS.md §4.
`status`: supported / partially_supported / disputed / unsupported.

Rebuild this from the drafted text after drafting — drafting invents claims.

### Disputed-claim resolution

```markdown
Claim:      "Four-day weeks consistently increase productivity."
Status:     disputed
Issue:      "consistently" exceeds the evidence; S7 finds no effect in its sector.
Revision:   "Some four-day-week trials report productivity gains; outcomes appear
             to depend on sector and implementation."
Action:     Explain what differs between the contexts. Do not drop S7.
```

## 5. Argument architecture

```markdown
Thesis:     {{one sentence}}
Stakes:     {{who is harmed by the status quo view, and how}}
Mechanism:  {{what actually produces the problem}}

Supporting claims
1. {{claim}} — evidence C1, C4 — warrant: {{why this supports the thesis}}
2. {{claim}} — evidence C2   — warrant: {{…}}
3. {{claim}} — evidence C5   — warrant: {{…}}

Strongest objection:  {{the best case against, stated fairly}}
Response:             {{where it is right; where it fails}}
Boundary conditions:  {{where the thesis does not apply}}
Implications:         {{3–5 concrete decisions that change}}
Narrative order:      {{section sequence and why}}
```

## 6. Section outline

One row per section. Approve this before drafting.

```markdown
| # | section | argumentative job | claims used | ~words |
|---|---------|-------------------|-------------|--------|
| 1 | {{heading}} | establish tension and stakes | — | 250 |
| 2 | {{heading}} | state thesis, name what convention misses | C1 | 400 |
| 3 | {{heading}} | show mechanism | C2,C4 | 600 |
```

Any section whose job is "restate the thesis" is deleted here, not later.

## 7. Article skeleton

```markdown
# {{title}}

**{{dek — one sentence stating the argument, not teasing it}}**

## {{Opening tension}}
Concrete situation, paradox, surprising finding, or consequential question.
Who has the problem · why now · which assumption may be wrong.

## {{The argument}}
The thesis, plainly. What the conventional view misses. Why this explanation
is more useful.

## {{Evidence and mechanism}}
Per major claim: claim · evidence · warrant · example · implication.

## {{What the conventional approach gets wrong}}
The strongest competing explanation, stated fairly. Where it succeeds, where
it fails.

## {{The framework}}
The usable model. No acronym unless it genuinely aids recall.

## {{Applying it}}
Decision rules · tradeoffs · failure modes.

## {{Boundary conditions}}
Where the thesis does not hold. What the evidence has not settled.

## {{What to do differently}}
3–5 concrete decisions.

## {{Close}}
Return to the opening tension. State the broader implication. Do not summarize.
```

## 8. Structure library

The skeleton in §7 is the default, not the only shape. Pick by the job the argument has to do.

| Format | Skeleton |
|---|---|
| Contrarian insight | conventional belief → anomaly → new thesis → mechanism → evidence → implications |
| Data-led analysis | finding → why it matters → method → drivers → alternative explanations → decisions |
| Executive playbook | decision → why the current process fails → principles → steps → examples → failure modes |
| Case-led | case → puzzle → diagnosis → generalized lesson → comparison → application |
| Explainer | question → answer → mechanism → evidence → misconceptions → implications |
| Opinion with evidence | thesis → stakes → evidence → strongest objection → response → recommendation |
| Trend analysis | what changed → magnitude → structural vs temporary drivers → winners and losers → indicators to watch |
| Series installment | minimal recap → new question → new insight → evidence → link to series → next question |

Every one of them still carries **claim → evidence → warrant → implication** inside its sections. A section that presents evidence without saying why it matters, or recommends without showing the mechanism, is defective in any format.

## 9. Reverse-outline pass

Run after drafting, before any line editing. Label every paragraph with a five-to-twelve-word description of the job it does, then interrogate the labels — not the prose. This exposes the actual argument skeleton, which is why it works where "make it flow better" does not.

```
Does every paragraph do exactly one useful job?
Does paragraph N create the need for paragraph N+1?
Does every section advance the thesis?
Does any section merely repeat an earlier one?
Does the conclusion introduce new substantive evidence?
Does each example actually prove the claim it is attached to?
Does every heading mark a distinct argumentative step?
```

Then apply the transformation the diagnosis calls for:

| Diagnosis | Transformation |
|---|---|
| Duplicate idea | Delete or consolidate |
| Orphan fact | State its implication, or remove it |
| Weak transition | Expose the causal or logical relation |
| Two concepts in one paragraph | Split |
| One concept across three paragraphs | Compress |
| Background before the hook | Move the background later |
| Recommendation before mechanism | Establish mechanism and evidence first |
| Tangent | Move to a note or sidebar, or cut |

## 10. Series manifest

```markdown
# Series: {{title}}

Series thesis:  {{the single argument distributed across parts}}
Before:         {{what the reader believes/does now}}
After:          {{what they believe/do having read all parts}}
Arc:            establish problem → explain mechanism → operating response → synthesis

## Part {{n}} — {{title}}
Unique question:     {{answered here and nowhere else}}
Part thesis:         {{this part's argument}}
Role in series:      {{what it contributes to the whole}}
Assumes from prior:  {{what the reader already has}}
New evidence:        {{claim ids introduced here}}
MUST NOT repeat:     {{concepts already established — the anti-repetition list}}
Open loop:           {{question left for the next part}}
Reader action:       {{what they can do after this part alone}}
```

The anti-repetition list is not optional. Without it each installment re-establishes the series premise and the set reads as variations on one article.

## 11. Revision log

```markdown
| rev | trigger | pass | sections changed | effect |
|----:|---------|------|------------------|--------|
| 1 | C7 unsupported | evidence | §3 | claim narrowed to one segment; S3 scope stated |
| 2 | §4 repeats §2 | structure | §2,§4 | §4 merged into §2; 180 words cut |
```

Record what changed and why. When revising, report both a text diff and a **semantic diff**: which claims changed, which evidence changed, whether confidence moved, and whether any qualification disappeared. A style pass that quietly deletes a hedge is an evidence regression, and only the semantic diff catches it.

## 12. Publish packet

Deliver this, not a bare article.

```yaml
publish_packet:
  article:
  title_primary:
  title_alternatives:      # scored per RUBRICS.md §8
  dek:
  executive_summary:
  author_byline:
  article_date:
  last_fact_checked:
  locale:
  depth_class:

  meta_title:
  meta_description:
  canonical_slug:
  internal_link_suggestions:
  image_brief:
  image_alt_text:

  source_ledger:
  claim_ledger:
  unresolved_items:        # every [SOURCE NEEDED] / [VERIFY] still open
  similarity_review:
  editorial_scores:
  human_approvals:         # named person, not a checkbox
```

`human_approvals` is a name. A packet without one is `ready_for_review`, never `approved`.

## 13. Corrections and freshness

Serious publishing corrects in public. Keep a record per article.

```yaml
article_history:
  published_at:
  research_ledger_version:
  last_checked_at:
  next_check_due:          # set for volatile content
  corrections:
    - date:
      original:
      corrected:
      reason:
      material: true       # material errors are disclosed, not silently edited
```

Schedule re-checks for articles carrying volatile content — statistics, regulation, prices, appointments, market conditions. Re-check means re-verify the claims; changing the displayed date without substantive change is a freshness claim the article has not earned.
