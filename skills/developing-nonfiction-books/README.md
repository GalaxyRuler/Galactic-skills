# Developing Nonfiction Books

Collaborate with a serious nonfiction author from first idea or existing draft through a coherent, evidence-aware manuscript — diagnosis before prose, claim-level source control, staged revision, and honest readiness labels.

## What it does

- Diagnoses the project first: entry state (concept, outline, chapter, or full manuscript), reader, promise, governing idea, scope, evidence supply, and risk
- Tests book-worthiness and selects an architecture intentionally (progressive argument, braided narrative, prescriptive journey, case-comparative, and more)
- Runs a claims-first research workflow: source cards, claim classes (verified fact → opinion), A–D confidence levels, and verification rules for quotes, numbers, studies, and cases
- Drafts one purposeful unit at a time against a chapter contract, preserving the author's voice from approved samples
- Separates seven revision modes (book-level developmental → final pre-publication QA) with explicit AI-authority vs author-approval boundaries
- Enforces quality gates and calibrated completion stages — "publication-ready" requires gate evidence, never just generated prose
- Hard safety rails: never fabricates sources, quotes, interviews, cases, data, or lived experience

## When to use

Planning, researching, drafting, revising, fact-checking, or quality-assuring a substantive nonfiction book or book-length manuscript — argument-driven, narrative, prescriptive, business, leadership, self-development, social science, history, culture, explanatory, or hybrid nonfiction. Not for fiction, poetry, textbooks, theses, memoir-dominant projects, or ghostwriting.

## What's inside

- [SKILL.md](SKILL.md) — core principles and the stage router, with short summaries of intake, output formats, quality gates, ethics, and the completion standard, each linking to its reference
- [references/INTAKE.md](references/INTAKE.md) — intake questionnaire and book-diagnosis tables
- [references/WORKFLOWS.md](references/WORKFLOWS.md) — stage workflows: architecture, research/evidence ledger, drafting, revision modes, chapter collaboration
- [references/GATES-AND-OUTPUTS.md](references/GATES-AND-OUTPUTS.md) — output formats, quality gates, ethics boundaries, completion standard
- [references/REFERENCE.md](references/REFERENCE.md) — the 34-source evidence base behind the skill (university writing centers, publisher guidelines, journalism and statistics standards, editorial-stage standards, copyright and AI-authorship guidance)
- [references/TEMPLATES.md](references/TEMPLATES.md) — copy-ready working forms: concept brief, positioning statement, annotated TOC, chapter contract, research plan, source card, claim ledger, revision memos, fact-check report, readiness report
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/developing-nonfiction-books ~/.claude/skills/`
**Codex:** `cp -r skills/developing-nonfiction-books $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\developing-nonfiction-books "$env:USERPROFILE\.claude\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
