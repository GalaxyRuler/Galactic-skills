# Vault System (optional, opinionated)

An anti-drift system for a vault that grows past a few hundred notes. It is **optional and prescriptive** — adopt the parts that fit. The whole thing rests on one rule:

> **Every note has exactly one correct home.** Drift = a note in the wrong folder, with the wrong frontmatter, or under the wrong name.

Everything below enforces that rule mechanically so the vault doesn't rot as it scales. Replace placeholder names (`<project>`, `project`, folder names) with your own conventions, then keep them consistent.

## 1. Pick your conventions once

| Choice | This guide uses | Yours |
|---|---|---|
| Board tag | `project` | … |
| Phase tag | `<project>-phase` | … |
| Literature type | `type: literature` | … |
| Top-level folders | `projects/`, `plans/`, `papers/`, `references/`, `_meta/`, `_templates/` | … |
| Vault branch | `main` | … |

Write these into your vault constitution (`CLAUDE.md` / `AGENTS.md` / `GEMINI.md`) so every agent and future-you routes the same way.

## 2. Frontmatter schemas (one per note family)

Consistency here is what makes Dataview/Bases work. A note with a divergent `type:`/fields silently disappears from the queries that depend on them.

**Project board** (`projects/active/<slug>.md`):
```yaml
---
tags: [project]
status: planning | building | review | blocked | done
where_now: 'One line: the next step in front of us'
progress: 'Phase A ✓ · Phase B in progress'
last_action: 'One line: what the last task did'
goal: 'High-level goal'
updated: 2025-01-15
repo: <path-or-url>   # omit if no code repo
---
```

**Phase plan** (`plans/<project>/phase-<L>-<slug>.md`):
```yaml
---
tags: [<project>-phase]
phase: A
status: pending | building | done
project: "[[<project>]]"
up: "[[<project>-implementation-plan]]"   # optional Breadcrumbs parent
updated: 2025-01-15
---
```

**Paper / manuscript section** (`papers/<project>/manuscript/<NN>-<slug>.md`):
```yaml
---
section: Introduction
order: 2
status: stub | drafting | complete
words: 0
depends_on: [00-abstract]
---
```

**Claim** (`papers/<project>/claims/C<N>-<slug>.md`):
```yaml
---
type: claim
id: C1
hypothesis: 'One-sentence testable claim'
status: confirmatory | exploratory | archived
---
```

**Literature note** (`references/<slug>.md`) — centralized and shared across projects, not per-paper:
```yaml
---
type: literature          # the queries filter on this exact value
title: "..."
authors: [Last1, Last2]
year: 2025
venue: arXiv
citekey: smith2025foo
url: https://...
tags: [topic]
status: to-read | read
relevance: 1-5
used_in: ["<project>"]    # which projects cite it
# optional comparison axes for a related-work matrix:
# axis_<dimension>: false
---
```

## 3. Note → folder routing table

Check this before creating or placing any note.

| Note type | Folder | Filename | Required frontmatter |
|---|---|---|---|
| Project board (active) | `projects/active/<slug>.md` | `<project>.md` | `tags: [project]` + board fields |
| Project board (archived) | `projects/archived/<slug>.md` | `<project>.md` | same |
| Phase plan | `plans/<project>/phase-<L>-<slug>.md` | `phase-a-foundations.md` | `tags: [<project>-phase]`, `phase:` |
| Implementation/decision/research doc | `plans/<project>/<slug>.md` | descriptive | `project:` link |
| Dated artifact (closeout, audit, ADR) | `plans/<project>/<YYYY-MM-DD>-<slug>.md` | date-prefixed | — |
| Literature note | `references/<slug>.md` | citekey slug | `type: literature` |
| Manuscript section | `papers/<project>/manuscript/<NN>-<slug>.md` | `01-introduction.md` | `section:`, `order:` |
| Claim | `papers/<project>/claims/C<N>-<slug>.md` | `C1-<slug>.md` | `type: claim`, `id:` |
| Canvas / visual map | `plans/<project>/<slug>.canvas` | — | — |
| Reusable prompt / lesson / rule | `_meta/<kind>/<slug>.md` | — | — |
| Template | `_templates/<slug>.md` | — | — |

### Red lines (these are bugs)

- A non-board `.md` in `projects/active/` — that folder is **only** for board notes tagged `project`. Research docs, diagrams, changelogs go to `plans/<project>/`.
- Any stray file directly under `projects/` — only `active/` and `archived/` subdirs live there.
- A new `.md` at the vault root — the root holds only your declared canonical files (constitutions, `HOME.md`, `README.md`, `.base` dashboards). Anything else is misplaced.
- A literature note without `type: literature` in `references/` — it vanishes from the related-work matrix.
- A shipped phase still marked `status: building` — update to `done` when it merges.

## 4. Self-routing templates (the mechanical fix for drift)

The #1 cause of drift is a template with no destination — Obsidian drops the new note at the default location (often the vault root) and relies on you to drag it. Add `tp.file.move()` to every Templater template that has a known home:

```javascript
// board template — always lands in projects/active/
<%* await tp.file.move("projects/active/" + tp.file.title) %>

// phase template — prompts for project, routes under plans/<project>/
<%*
  const project = await tp.system.prompt("Project slug")
  await tp.file.move("plans/" + project + "/phase-" + tp.file.title)
%>

// dated artifact — date-prefixed under plans/<project>/
<%*
  const project = await tp.system.prompt("Project slug")
  const date = tp.date.now("YYYY-MM-DD")
  await tp.file.move("plans/" + project + "/" + date + "-" + tp.file.title)
%>
```

If you find a template missing `tp.file.move()` and it has a well-known destination, add it.

## 5. Post-creation drift checklist

After creating or placing any note, verify:

1. Folder matches the routing table?
2. Filename matches the pattern?
3. Required frontmatter tag/fields present?
4. If a board: in `projects/active/` or `projects/archived/` — nowhere else?
5. Nothing new at the vault root that isn't a declared canonical file?

## 6. End-of-task board update (ritual)

When work for a project finishes and is committed, update that project's board note as the **final step** — and only that board:

1. **`## Plan`** — tick completed milestones `- [ ]` → `- [x]`.
2. **`progress`** (frontmatter) — update the human-readable progress line.
3. **`where_now`** — one line: the next step now in front of us.
4. **`last_action`** — one line: what this task did.
5. **`updated`** — today's date.
6. **`## History`** — append one dated line (newest last), e.g. derived from `git log --oneline -3`.
7. **`status`** — change only if it actually changed.

Do not edit any other project's board, and don't touch the `.base` dashboard source.

## 7. Literature & citation workflow

Keep literature notes **centralized** in `references/` and shared across projects (`used_in:` lists the consumers) rather than copied per-paper.

1. **Has a DOI / arXiv id** → use a citation plugin (BibLib / Zotero bridge) to auto-fill the schema, then add `tags`, `relevance`, and any comparison `axis_*` by hand.
2. **No identifier** → create from a `_templates/reference.md` that emits the exact `type: literature` schema above.
3. **Discovery** → Reference Map (a paper's own citations) + Smart Connections (semantically-related notes already in the vault) to seed links.

Cite in manuscript sections with `[@citekey]`; Pandoc resolves against the `.bib`.

**One schema per note family.** Before adding any creation template, confirm it emits the same `type:`/fields the existing notes and their queries depend on. A divergent template is a silent data-loss bug — the classic case is `type: reference` vs `type: literature` quietly dropping notes from the related-work matrix.
