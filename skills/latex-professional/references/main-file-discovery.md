# Main `.tex` File Discovery

Purpose: reliably identify the root/main `.tex` (the one you compile) in a multi-file project, honoring magic comments and build-config hints before guessing by filename.

## Decision tree

```
1. Is there a build-config hint that names a root?
     latexmkrc / .latexmkrc  → @default_files or $root
     Makefile                → the target passed to pdflatex/latexmk
     .arara / arara: directives
     00README.json (arXiv)   → "toplevelfile"
     .vscode/settings.json   → latex-workshop.latex.rootFile
     Overleaf                → main document set in project settings (often main.tex)
   → If yes and the file exists, that IS the root. Stop.

2. Does any .tex have a magic comment?
     % !TEX root = ../thesis.tex   → follow it (may be relative) to the TRUE root
     % !TEX root present on a chapter file points AWAY from that file.
   → Resolve the target; that is the root. Stop.

3. Score every .tex (see heuristic). Highest score wins.
     Strong signal = \documentclass AND \begin{document} in the same file.

4. Tie-break by conventional name (main/paper/manuscript/ms/thesis/...).

5. Still ambiguous? List top candidates and ASK — do not guess silently.
```

## Magic comments (TeX directives)

Editors (TeXShop, TeXworks, VS Code LaTeX Workshop, TeXstudio) read leading `%`-comments:

| Directive | Meaning | Example |
|---|---|---|
| `% !TEX root = FILE` | The real root to compile (relative to this file) | `% !TEX root = ../main.tex` |
| `% !TEX program = ENGINE` | Which engine to run | `% !TEX program = lualatex` |
| `% !TEX encoding = ...` | Source encoding | `% !TEX encoding = UTF-8` |
| `% !BIB program = ...` | biber vs bibtex | `% !BIB program = biber` |

Rules:
- A `% !TEX root` on a **sub-file points to the root** — never treat a file that *has* this directive as the root itself.
- `% !TEX program` overrides your engine guess. Prefer it over inferring from packages.
- These are typically only honored on the **first few lines** of a file — check the head.

## Scoring heuristic (matches `scripts/find-main-tex.py`)

The helper walks `*.tex` under the root (skipping `.git`, `node_modules`, `build`, `_minted`, `.latex-build`, etc.) and scores each:

| Signal | Points |
|---|---|
| Contains `\documentclass{...}` | +100 |
| Contains `\begin{document}` | +80 |
| Contains `% !TEX root =` directive | +20 |
| Contains `% !TEX program =` directive | +10 |
| Common main filename (`main.tex` +30; `paper.tex` +25; `manuscript.tex` +25; `thesis.tex` +25; `dissertation.tex` +25; `article.tex` +20; `ms.tex` +20; `report.tex` +20; `book.tex` +20) | as listed |
| Declares bibliography (`\bibliography{` or `\addbibresource{`) | +10 |
| Contains `\maketitle` or `\tableofcontents` | +5 |

The root almost always scores ≥180 (documentclass + begin{document} + name/bib bonuses). A file with `\documentclass` but **no** `\begin{document}` is usually a shared preamble, not the root.

### Invoke

```bash
# Human-readable ranking (top 10 with reasons):
python scripts/find-main-tex.py /path/to/project

# Machine-readable (use "best" then "candidates"):
python scripts/find-main-tex.py /path/to/project --json
```

Output shape (`--json`): `{ "root", "candidates": [{path, score, reasons}], "best": {...} }`. Trust `best` only when its score clearly leads; if the top two are close, inspect both.

## Conventional filenames (tie-break order)

`main.tex` › `paper.tex` › `manuscript.tex` / `thesis.tex` / `dissertation.tex` › `article.tex` › `ms.tex` › `report.tex` / `book.tex`.

Venue-specific hints: `sample-sigconf.tex`/`acmart-*` (ACM), `bare_jrnl.tex`/`*IEEEtran*` (IEEE), `sn-article.tex` (Springer Nature), `elsarticle-template*.tex` (Elsevier), `apssamp.tex` (RevTeX/APS). See `journal-template-modes.md`.

## Multi-file projects

- **The root is the only file with `\documentclass` + `\begin{document}`.** All others are pulled in via `\input`/`\include`/`\subfile`.
- **`\include{chapters/ch1}`** starts a new page and writes `chapters/ch1.aux` — can fail on write-restricted top level (arXiv). **`\input{chapters/ch1}`** just splices text and is safer. See `submission-arxiv.md`.
- `\includeonly{...}` in the preamble is a strong root signal — only the root carries it.
- Shared preamble files (`preamble.tex`, `packages.tex`, `macros.tex`) hold `\usepackage` lines but **no** `\begin{document}` — never the root.

## `subfiles` class (compile any chapter standalone)

Pattern where each chapter is *independently compilable* yet also part of a master:

```latex
% main.tex (the true root):
\documentclass{article}
\usepackage{subfiles}
\begin{document}
\subfile{chapters/intro}
\subfile{chapters/method}
\end{document}
```

```latex
% chapters/intro.tex (a subfile — also compiles alone):
\documentclass[../main.tex]{subfiles}   % <- points at the master's preamble
\begin{document}
...chapter body...
\end{document}
```

Discovery notes for `subfiles`:
- A subfile has `\documentclass[../main.tex]{subfiles}` and its own `\begin{document}` → it will **score high but is NOT the master**. The `[../main.tex]` option reveals the true root — follow it.
- The master is the file whose `\documentclass` is a *real* class (`article`, `report`, `book`), referenced by the subfiles' options.
- When in doubt, compile the **master**; it produces the full document.

## Build-config hints (where each declares the root)

| File | How the root is named | Example line |
|---|---|---|
| `.latexmkrc` / `latexmkrc` | `@default_files` array or `$root` | `@default_files = ('main.tex');` |
| `Makefile` | the target/basename fed to `pdflatex`/`latexmk` | `latexmk -pdf main.tex` |
| `.vscode/settings.json` | `latex-workshop.latex.rootFile` | `"latex-workshop.latex.rootFile": "main.tex"` |
| arara header | `% arara: pdflatex` sits in the **root** file | `% arara: pdflatex` |
| `00README.json` (arXiv) | `"usage": "toplevelfile"` | see `submission-arxiv.md` |
| Overleaf | project "Main document" setting (not in repo) | usually `main.tex` |

Quick grep sweep:

```bash
# Config-declared roots:
grep -RnE 'default_files|rootFile|toplevelfile' . 2>/dev/null
grep -RnE 'pdflatex|xelatex|lualatex|latexmk' Makefile .latexmkrc 2>/dev/null
# Magic comments across all .tex:
grep -RnE '%\s*!TEX\s+(root|program)' --include='*.tex' .
```

**Precedence when hints conflict:** explicit config (`00README.json`/`latexmkrc`/`rootFile`) > `% !TEX root` magic comment > score heuristic > filename convention. A config hint that names a non-existent file is stale — fall through to the next rule and note it.

## Worked example

```
project/
├── main.tex           # \documentclass, \begin{document}, \input{chapters/*}
├── preamble.tex       # only \usepackage lines
├── chapters/
│   ├── intro.tex      # % !TEX root = ../main.tex  ← points to main
│   └── method.tex
└── refs.bib
```

- `find-main-tex.py`: `main.tex` scores ~220 (documentclass 100 + begin{document} 80 + name 30 + bib 10), `preamble.tex` ~0 (no `\begin{document}`), chapter files get +20 for the `% !TEX root` directive but no documentclass.
- The chapters' `% !TEX root = ../main.tex` confirms `main.tex` — never treat a chapter as root.
- **Chosen root: `project/main.tex`.**

## Output an agent should produce

State: (1) chosen root path (absolute), (2) the single deciding signal (config hint / magic comment / score), (3) intended engine (from `% !TEX program`, `00README.json`, or inference), (4) any close runner-up you rejected and why. If no candidate is decisive, present the ranked list and ask.
