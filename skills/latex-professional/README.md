# LaTeX Professional

Create, edit, debug, compile, and package professional LaTeX documents while preserving mathematical, bibliographic, and scholarly meaning — LaTeX source is treated as valuable authored code, not disposable output.

## What it does

- Creates and edits `.tex/.bib/.bst/.sty/.cls` files across article, report, book, thesis, and Beamer document classes
- Fixes PDF build failures by parsing `latexmk`/`pdfLaTeX`/`XeLaTeX`/`LuaLaTeX` compile logs into actionable errors
- Repairs bibliographies across BibTeX, BibLaTeX, Biber, and natbib backends
- Preserves math semantics — never silently changes theorem statements, mathematical claims, or assumptions while reformatting
- Formats equations, tables, and figures with copy-paste snippets
- Converts Markdown or plain drafts into LaTeX
- Packages a finished paper for arXiv, IEEE, ACM, Springer, Elsevier, or thesis submission

## When to use

Working with `.tex/.bib/.bst/.sty/.cls` files; running `latexmk`/`pdfLaTeX`/`XeLaTeX`/`LuaLaTeX`; hitting "Undefined control sequence" or "Citation undefined" errors; resolving package option clashes; formatting equations/tables/figures; converting a draft to LaTeX; or packaging a paper against a publisher template.

## What's inside

- [SKILL.md](SKILL.md) — router: workflow, compile-error triage, math-preservation rules, packaging checklist
- [references/compile-error-playbook.md](references/compile-error-playbook.md) — common LaTeX/BibTeX error signatures and fixes
- [references/bibliography-backends.md](references/bibliography-backends.md) — BibTeX vs BibLaTeX vs Biber vs natbib, when to use each
- [references/math-preservation.md](references/math-preservation.md) — rules for editing math without changing meaning
- [references/tables-and-figures.md](references/tables-and-figures.md) — formatting patterns and snippets
- [references/package-compatibility.md](references/package-compatibility.md) — known package clashes and load-order fixes
- [references/journal-template-modes.md](references/journal-template-modes.md) — working inside publisher-supplied templates
- [references/submission-arxiv.md](references/submission-arxiv.md) — arXiv packaging checklist
- [references/main-file-discovery.md](references/main-file-discovery.md) — locating the main `.tex` entry point in multi-file projects
- [scripts/](scripts/) — `build-latex-safe.sh` / `.ps1` (safe compile wrapper), `parse-latex-log.py`, `check-bib.py`, `check-latex-assets.py`, `find-main-tex.py`, `latex-project-inventory.py`
- [templates/](templates/) — ready-to-use `article`, `report`, `book`, `thesis`, `beamer`, and `academic-paper` scaffolds, plus shared `latexmkrc` variants and equation/table/figure snippets
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/latex-professional ~/.claude/skills/`
**Codex:** `cp -r skills/latex-professional $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\latex-professional "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse skills\latex-professional "$env:USERPROFILE\.codex\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex. Optional scripts require Python 3.10+; compilation requires a local TeX distribution (TeX Live / MiKTeX) with `latexmk`.
