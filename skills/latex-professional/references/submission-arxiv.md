# arXiv Submission

Purpose: package a LaTeX project so arXiv's AutoTeX builds it on the first try — engine/TeX Live constraints, `.bib` vs `.bbl` rules, the `\include` write pitfall, minted, and `00README.json`.

## Pass / fail / unknown checklist (run before declaring "arXiv-ready")

| # | Check | Pass criterion |
|---|---|---|
| 1 | Main file identified | one root with `\documentclass`+`\begin{document}` (see `main-file-discovery.md`) |
| 2 | Engine chosen & declarable | pdfLaTeX default; know if Xe/Lua is required |
| 3 | No absolute paths | zero `C:\...`, `/home/...`, `/Users/...` in `\includegraphics`/`\input`/`\graphicspath` |
| 4 | No local-only fonts | fonts are TeX Live-bundled or embedded; no `\setmainfont{Some Local Font}` that isn't shipped |
| 5 | Bibliography strategy | either `.bib` present + correct backend, OR a `.bbl` named `<main>.bbl` |
| 6 | `.bbl` backend matches source | never a BibTeX `.bbl` for a Biber project or vice-versa |
| 7 | No top-level `\include{subdir/...}` write failures | use `\input` for subdir files (see below) |
| 8 | minted (if used) handled | `_minted` dir shipped + TeX Live version match + compiles WITHOUT shell escape |
| 9 | Case-correct filenames | arXiv is case-sensitive (Linux); `Fig1.PDF` ≠ `fig1.pdf` |
| 10 | Only needed sources | strip `.aux`/`.out`/`.synctex`/editor junk; keep `.bbl` if used |
| 11 | Compiles clean locally | `latexmk -pdf` (or the declared engine) with no fatal error |

Mark each **pass / fail / unknown**. Never claim "ready" with an unknown outstanding.

## Engine & TeX Live constraints

- arXiv currently supports **TeX Live 2023 and 2025**, with **2025 as the default**. Supported processors are exactly: **TeX (`tex`/`pdftex`), LaTeX in DVI mode (`latex`), pdfLaTeX (`pdflatex`), and XeLaTeX (`xelatex`)**. **LuaLaTeX is NOT supported by arXiv** — a project that requires `lualatex` must be adapted to compile under pdfLaTeX or XeLaTeX before submission. (Source: arXiv `help/faq/texlive.html` supported-processors list; re-check if arXiv bumps its TeX Live version.)
- **Choose pdfLaTeX when unsure** — most compatible.
- Processor decision:

```
Only EPS graphics, no PDF/raster   → LaTeX (classic latex+dvips route)
JPG / PNG / PDF graphics           → pdfLaTeX
Mixed EPS + raster/PDF             → XeLaTeX
Uses fontspec / unicode-math       → XeLaTeX  (LuaLaTeX is NOT accepted by arXiv)
Otherwise / unsure                 → pdfLaTeX
```

- Declare the processor explicitly via `00README.json` (below) so AutoTeX doesn't guess wrong.

## `.bib` vs `.bbl`

Two valid strategies — pick one:

1. **Ship the `.bib`** (+ correct `\bibliography`/`\addbibresource`): arXiv runs bibtex/biber for you. Simplest when the backend is standard.
2. **Ship a pre-generated `.bbl`**: arXiv uses it directly (no bib run). **The uploaded `.bbl` filename MUST equal the main `.tex` basename** — `main.tex` → `main.bbl`. A mismatched name means the bibliography silently vanishes.

Rules:
- **Never ship a `.bbl` produced by the wrong backend.** A Biber `.bbl` in a project arXiv processes with bibtex (or vice-versa) fails. If in doubt, ship the `.bbl` you compiled locally *and* keep the backend consistent.
- If shipping `.bbl`, you generally do **not** also need the `.bib` — but including it is harmless if the names are right.
- BibLaTeX+Biber: the safe move is to compile locally and ship the resulting `<main>.bbl`, since older arXiv biber versions can lag. Verify the `.bbl` was made by biber, not bibtex.

## `\include` top-level write pitfall

- `\include{chapters/intro}` makes LaTeX **write `chapters/intro.aux`** — and arXiv's build can restrict writes outside the top level, so this **fails** with a permission/`\openout` error.
- **Fix:** replace `\include{subdir/file}` with `\input{subdir/file}` for anything in a subdirectory. `\input` only reads; it writes no `.aux`.
- If you must keep `\include` (e.g. for `\includeonly`), flatten the layout so included files sit at the top level.

## minted (syntax highlighting)

`minted` shells out to Pygments, so it needs shell escape — which arXiv restricts. To make it work:

1. **Ship the cached `_minted` directory** (and any `*.pygtex`/`*.pygstyle` cache files) produced by a local `--shell-escape` compile. Newer `minted` (v3) caches under a `_minted` folder; include it.
2. **Match arXiv's TeX Live version** when generating the cache — a cache built on a different `minted`/`pygments`/TeX Live can be rejected or ignored.
3. **Verify it compiles WITHOUT shell escape** locally:
   ```bash
   pdflatex -no-shell-escape main.tex      # must succeed using only the cache
   ```
   If that fails, the cache is incomplete — regenerate with `--shell-escape`, then re-test.
4. Consider switching to `listings` (no shell escape, no cache) if highlighting fidelity isn't critical — it sidesteps the whole issue.

## `00README.json`

Tells arXiv AutoTeX the compiler and the top-level source(s). Put it at the archive root.

```json
{
  "process": {
    "compiler": "pdflatex"
  },
  "sources": [
    { "filename": "main.tex",   "usage": "toplevelfile" },
    { "filename": "intro.tex",  "usage": "ignore" }
  ]
}
```

- `compiler`: one of `pdflatex`, `latex`, `xelatex` (per the processor decision above).
- `usage: "toplevelfile"` marks the main file; `usage: "ignore"` excludes a file from being treated as a separate document (useful when multiple `.tex` files have `\documentclass`).
- Use `00README.json` whenever the project has more than one `\documentclass`-bearing file, or when you need a non-default compiler. (arXiv also honors the legacy `00README.XXX` directives, but JSON is current.)

## Remove absolute paths & local fonts

- Grep for absolute paths and fix to relative:
  ```bash
  grep -rnE '\\(includegraphics|input|include|graphicspath)[^\n]*(/home/|/Users/|[A-Za-z]:\\\\)' .
  ```
- `\graphicspath` must use relative dirs: `\graphicspath{{figures/}}` not an absolute root.
- Fonts: if the source uses `fontspec` with `\setmainfont{Local Font.otf}`, either switch to a TeX Live-bundled font (e.g. `TeX Gyre` families, `Latin Modern`) or **bundle the `.otf`/`.ttf` in the upload and reference it by path with `Path=`. Fonts not in TeX Live and not bundled will fail.

## Concrete step list an agent runs

```
1. find-main-tex.py → confirm the single root; note engine (% !TEX program / packages).
2. check-bib.py → confirm backend; decide ship-.bib vs ship-.bbl; if .bbl, rename to <main>.bbl.
3. check-latex-assets.py → fix absolute paths, missing/case-wrong assets, EPS-vs-engine issues.
4. Replace \include{subdir/...} with \input{subdir/...}.
5. If minted: rebuild cache on matching TeX Live, ship _minted/, verify -no-shell-escape compile.
6. Strip junk: rm *.aux *.log *.out *.synctex.gz *.fls *.fdb_latexmk (KEEP <main>.bbl if shipping it).
7. Write 00README.json with the chosen compiler + toplevelfile (if needed).
8. Clean-room compile: fresh dir, only the intended upload files, run the declared compiler twice.
9. Tar/zip the minimal source set. Confirm no absolute paths, no local fonts, no stray class files missing.
10. Report the pass/fail/unknown table. Resolve every FAIL/UNKNOWN before declaring arXiv-ready.
```

## Security reminders

- **Do not enable `--shell-escape` casually.** It lets TeX run arbitrary commands. For minted you need it *locally* to build the cache, but the arXiv build must succeed *without* it. Never enable it on a project you didn't inspect.
- Never run an unfamiliar `Makefile`, `arara` directive, or `latexmkrc` shell hook before reading it — a build script can execute anything. Inspect first.

## Common arXiv rejection causes (quick reference)

| Symptom on arXiv | Cause | Fix |
|---|---|---|
| "references empty / missing" | `.bbl` name ≠ main basename, or wrong backend | rename `<main>.bbl`; match backend |
| `\openout` / write permission error | `\include{subdir/...}` | use `\input` |
| minted fails | no `_minted` cache / needs shell escape | ship cache; verify `-no-shell-escape` |
| figure not found | absolute path / case mismatch | relative path; fix case |
| font error | local-only font | bundle or use TeX Live font |
| wrong compiler used | AutoTeX guessed | declare in `00README.json` |
