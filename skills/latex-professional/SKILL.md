---
name: latex-professional
description: Use when working with LaTeX/TeX projects — creating, editing, compiling, or debugging .tex/.bib/.bst/.sty/.cls files, fixing PDF build failures and compile-log errors, repairing bibliographies (BibTeX, BibLaTeX, Biber, natbib), formatting equations/tables/figures, converting Markdown or drafts to LaTeX, or packaging a paper for arXiv/IEEE/ACM/Springer/Elsevier/thesis submission. Triggers on latexmk, pdfLaTeX/XeLaTeX/LuaLaTeX, "Undefined control sequence", "Citation undefined", package option clash, and publisher templates.
license: MIT
compatibility: Claude and Claude Code. Optional scripts require Python 3.10+; compilation requires a local TeX distribution (TeX Live / MiKTeX) with latexmk when the user asks to build.
---

# LaTeX Professional Skill

<mission>
Help users create, edit, debug, compile, and package professional LaTeX documents while preserving mathematical, bibliographic, and scholarly meaning. Treat LaTeX source as valuable authored source code, not disposable output.
</mission>

<when_to_use>
Use for LaTeX, TeX, BibTeX, BibLaTeX, Biber, natbib, latexmk, arXiv packaging, academic papers, theses, books, reports, Beamer slides, equations, tables, figures, captions, labels, citations, publisher templates, .tex/.bib/.bst/.sty/.cls files, or LaTeX compile errors.
</when_to_use>

## Resources (progressive disclosure — load only what the task needs)

**Scripts** (`scripts/`, read-only, Python 3.10+; run with `python scripts/<name>`):
| Script | Use |
|---|---|
| `find-main-tex.py [root] [--json]` | Rank likely main `.tex` files. |
| `latex-project-inventory.py [root] [--json]` | Full read-only inventory: sources, engine hints, bib backend, assets, build systems, submission artifacts. |
| `parse-latex-log.py <file.log> [--json]` | Extract the first meaningful error + all findings from a build log. |
| `check-latex-assets.py [main.tex] [--json]` | Verify `\includegraphics`/`\input`/`\include`/bibliography files exist. |
| `check-bib.py [paths…] [--json]` | Lint `.bib` for duplicate keys, unbalanced braces, missing fields. |
| `build-latex-safe.sh` / `build-latex-safe.ps1` | Safe latexmk wrapper — **no shell escape unless explicitly flagged**. |

**Reference playbooks** (`references/`, load on demand):
| Playbook | Load when |
|---|---|
| `compile-error-playbook.md` | Diagnosing a build failure or `.log`. |
| `main-file-discovery.md` | Identifying the main file in an unfamiliar project. |
| `bibliography-backends.md` | Any citation / bibliography-backend work. |
| `math-preservation.md` | Editing equations or mathematical text. |
| `package-compatibility.md` | Option clashes, load-order errors, engine choice. |
| `tables-and-figures.md` | Building or fixing tables and figures. |
| `submission-arxiv.md` | Preparing an arXiv upload. |
| `journal-template-modes.md` | IEEE / ACM / Springer / Elsevier / RevTeX / thesis targets. |

**Templates** (`templates/`): generic starters — `article/`, `report/`, `book/`, `thesis/`, `beamer/`, `academic-paper/`, `latexmkrc/` configs, and `snippets/` for tables/equations/figures. Default bibliography is BibLaTeX + Biber. These are NOT substitutes for official venue class files.

<global_rules>
1. Preserve semantic meaning. Do not silently change theorem statements, mathematical claims, assumptions, experimental results, citation intent, or author conclusions.
2. Preserve labels, citations, macros, equations, cross-references, custom commands, and template-required structure unless the user explicitly asks for a refactor.
3. Do not invent citations, references, DOIs, data, theorem statements, proof steps, or experimental results.
4. Separate formatting/writing improvements from substantive scholarly changes.
5. Treat LaTeX compilation as executable-adjacent. Never enable shell escape on an untrusted project without explicit user approval.
6. Do not run unknown Makefiles, arara directives, build scripts, or cleanup scripts before inspecting them.
7. Do not delete source files or overwrite user-authored content without explicit approval or a clear diff.
8. Prefer minimal, reversible edits. When editing existing projects, explain what changed and why.
</global_rules>

<initial_triage>
For an existing LaTeX project, inspect before editing:
1. Identify the main `.tex` file:
   - Prefer files with `\documentclass` and `\begin{document}`.
   - Respect magic comments such as `% !TEX root` and `% !TEX program`.
   - Prefer existing build metadata (latexmkrc, Makefile, arara, CI, Overleaf root) when visible.
   - Use `scripts/find-main-tex.py` for a deterministic ranking.
2. Identify document class and template: article, report, book, memoir, beamer, IEEEtran, acmart, elsarticle, revtex, KOMA (scrartcl/scrreprt/scrbook), thesis, or a custom `.cls`.
3. Identify engine hints:
   - `fontspec`, `polyglossia`, `unicode-math`, or OpenType fonts → XeLaTeX or LuaLaTeX.
   - `inputenc`/`fontenc`/`babel` and many publisher templates → pdfLaTeX.
4. Identify bibliography backend:
   - `\bibliography` + `\bibliographystyle` → BibTeX/natbib.
   - `\usepackage{biblatex}`, `\addbibresource`, `\printbibliography` → BibLaTeX, usually Biber.
5. Identify figures, tables, appendices, indexes, glossaries, custom macros, `.sty`/`.cls`, generated files, and submission constraints.
6. `scripts/latex-project-inventory.py` produces the whole inventory in one read-only pass.
</initial_triage>

<new_document_workflow>
When creating a new document:
1. Ask for document type only if it changes the structure materially.
2. Choose a conservative base class: article (paper/note), report (long technical report), book/memoir (long-form), beamer (slides), KOMA variants; use IEEEtran/acmart/elsarticle/Springer/revtex ONLY when the user names the venue or supplies official files.
3. Create a sane structure: `main.tex`, `sections/`, `figures/`, `refs.bib`, `latexmkrc`, `README.md`. Reuse `templates/` as a starting point.
4. Use packages only when justified. Avoid large copied-in preambles.
5. Label consistently: `sec:`, `fig:`, `tab:`, `eq:`, `thm:`, `app:`.
6. Use booktabs-style tables for publication tables.
7. Default to BibLaTeX + Biber for new academic manuscripts; ask about citation style when the target venue implies BibTeX/natbib.
</new_document_workflow>

<safe_edit_protocol>
When editing existing LaTeX:
1. Read the source around the target. Do not rewrite unrelated sections.
2. Preserve macro boundaries. If a phrase contains `\cite`, `\ref`, `\label`, `\gls`, `\ac`, `\footnote`, math, or custom commands, edit around the command without breaking it.
3. Keep line wrapping and indentation consistent with the file.
4. For writing improvements, improve clarity, grammar, cohesion, and technical precision without changing meaning.
5. For structural refactors, keep labels stable unless renaming is explicitly requested and every reference is updated.
6. After edits, check for unbalanced braces, unmatched environments, duplicate labels, broken citations, missing assets (`scripts/check-latex-assets.py`), and compile impact.
</safe_edit_protocol>

<math_preservation>
For equations and mathematical text (see `references/math-preservation.md`):
1. Preserve semantic meaning over visual compactness.
2. Do not infer ambiguous formulas. Ask or flag ambiguity.
3. Use appropriate environments: `equation` (single numbered), `align` (multi-line aligned), `gather` (multiple centered), `split` (one numbered multi-line), `cases` (piecewise), `matrix`/`pmatrix`/`bmatrix`/`vmatrix`; theorem/proof only when the document defines them or the user asks.
4. Keep punctuation, numbering, and definitions clear.
5. Do not change variable names, quantifiers, domains, indices, or equality/inequality direction unless explicitly requested.
</math_preservation>

<table_figure_protocol>
See `references/tables-and-figures.md`.
Tables: booktabs (`\toprule`/`\midrule`/`\bottomrule`); `tabularx` for width-constrained text; `longtable` for multipage; `siunitx` S columns for numeric alignment; `multirow`/`multicolumn` only when needed; avoid vertical rules in publication tables unless the template requires them; keep captions informative and labels stable.
Figures: `\includegraphics` with robust relative paths (never absolute local paths); prefer `figures/`; captions and labels inside `figure`; for subfigures use the package already present (prefer `subcaption`) — don't introduce a conflicting one.
</table_figure_protocol>

<compile_debug_workflow>
See `references/compile-error-playbook.md`.
1. Establish the build command from project conventions (latexmkrc, Makefile, arara, CI, README, Overleaf). Inspect any Makefile/arara/script before running it.
2. If no convention exists, use a safe latexmk command WITHOUT shell escape:
   `latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex`
   Use `-pdfxe` (XeLaTeX) or `-pdflua` (LuaLaTeX) only when engine hints require it.
3. Parse the log for the FIRST meaningful error, not the final fatal message (`scripts/parse-latex-log.py`).
4. Classify the root cause: missing package/file; undefined control sequence; unbalanced brace/environment; runaway argument; package option clash; engine mismatch; Unicode/font; bibliography backend mismatch; missing citation/reference; figure/table path; overfull/underfull box.
5. Make the smallest fix that addresses the root cause.
6. Recompile after the fix when possible.
7. Report remaining warnings separately from blocking errors.
</compile_debug_workflow>

<bibliography_workflow>
See `references/bibliography-backends.md`.
1. Detect BibTeX/natbib vs BibLaTeX/Biber before editing citation commands.
2. Never mix a BibTeX-generated `.bbl` with a Biber/BibLaTeX workflow.
3. Do not invent references. If a key is missing, search project `.bib` files and text; if evidence is absent, flag it.
4. Preserve the venue's required style.
5. Normalize citation commands only within the existing system: natbib (`\citep`/`\citet`/`\citealp`), biblatex (`\parencite`/`\textcite`/`\autocite`), or plain `\cite`.
6. Check duplicate keys, missing required fields, malformed braces, Unicode issues, stale `.bbl` (`scripts/check-bib.py`).
</bibliography_workflow>

<submission_workflow>
See `references/submission-arxiv.md` and `references/journal-template-modes.md`.
1. Identify target venue and required template.
2. Build from clean source when possible.
3. Confirm main file, engine, bibliography backend, image formats, custom `.sty`/`.cls`, generated `.bbl`/`.ind`, included assets.
4. Check all included files exist and paths are portable; no absolute or local-only font paths.
5. For arXiv: confirm supported engine + TeX Live constraints; include required `.bib` or a matching `.bbl` (the `.bbl` filename must match the main `.tex`); avoid `\include{subdir/file}` (use `\input` for subdirectory sources); handle `minted` only with explicit shell-escape approval and a cached `_minted` strategy.
6. For publisher templates, do not override class formatting unless required for compilation.
7. Produce a pass/fail/unknown submission checklist and list unresolved risks.
</submission_workflow>

<conversion_workflow>
When converting Markdown, notes, Word-exported text, or rough drafts:
1. Preserve heading hierarchy, lists, equations, citations, tables, figures, and cross-references.
2. Produce maintainable LaTeX source, not one-off visual output.
3. Use semantic structure: `\section`, `\subsection`, theorem/table/figure environments, and bibliography commands.
4. Flag ambiguous citations, unknown figure paths, and equations that need human confirmation — do not invent them.
</conversion_workflow>

<output_expectations>
When responding:
1. State what you inspected.
2. State what you changed or recommend changing.
3. For compile errors: root cause, evidence, fix, and validation status.
4. For edits: summarize the semantic-preservation assumptions you made.
5. For submissions: a checklist with pass/fail/unknown status.
6. If validation could not be run, give the exact command the user should run and what remains unverified.
</output_expectations>

<quality_checklist>
Before finalizing:
- Main `.tex` identified.
- Engine choice justified.
- Build command identified or recommended.
- Bibliography backend detected.
- Citations and labels preserved.
- Math meaning preserved.
- Figures/assets checked.
- Shell escape avoided unless explicitly approved.
- No invented references or claims.
- Minimal diff for existing projects.
- Compile/check results reported (or the exact command to run stated).
</quality_checklist>
