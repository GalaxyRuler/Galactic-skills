# Bibliography Backends: Detect & Repair

Purpose: decide whether a project uses BibTeX/natbib or BibLaTeX/Biber, run the right build sequence, and fix the common bibliography failures — without ever inventing references.

## Never invent references

If a `\cite` key has no matching `.bib` entry, **flag the missing key to the user**. Do not fabricate an author/title/year to make the build clean. A silently-invented citation is worse than a build warning. Report: the key, the file/line citing it, and that no entry was found.

## Detection table

| Source signal (grep the main `.tex` + preamble) | System | Backend program | Print command |
|---|---|---|---|
| `\usepackage{natbib}` + `\bibliographystyle{...}` + `\bibliography{...}` | **BibTeX + natbib** | `bibtex` | `\bibliography{refs}` |
| `\bibliographystyle{...}` + `\bibliography{...}`, no biblatex | **BibTeX (plain)** | `bibtex` | `\bibliography{refs}` |
| `\usepackage[...]{biblatex}` + `\addbibresource{...}` + `\printbibliography` | **BibLaTeX** | `biber` (default) | `\printbibliography` |
| `\usepackage[backend=bibtex,...]{biblatex}` | **BibLaTeX w/ bibtex backend** | `bibtex` | `\printbibliography` |
| `\bibliography{...}` **and** `\usepackage{biblatex}` together | **INVALID mix** | — | fix first (see below) |
| No `\bibliography*`, references typed by hand as `\bibitem` | **manual `thebibliography`** | none | inline |

Quick detector commands:

```bash
grep -nE '\\usepackage(\[[^]]*\])?\{biblatex\}' main.tex   # → BibLaTeX if hit
grep -nE '\\addbibresource\{'                    main.tex   # → BibLaTeX
grep -nE '\\bibliographystyle\{|\\bibliography\{' main.tex  # → BibTeX (if no biblatex)
grep -noE 'backend=(biber|bibtex)'               main.tex   # → biblatex backend
```

Or run the helper: `python scripts/check-bib.py <main>.tex` — it reports the detected system, backend, `.bib` resources, and any mismatch/duplicate-key/missing-key findings. Prefer it over eyeballing.

## Citation commands per system (don't cross the streams)

| Intent | natbib | biblatex | plain |
|---|---|---|---|
| Parenthetical (Author, year) | `\citep{k}` | `\parencite{k}` | `\cite{k}` |
| Textual Author (year) | `\citet{k}` | `\textcite{k}` | — |
| Context-adaptive | — | `\autocite{k}` / `\autocites` | — |
| Author only | `\citeauthor{k}` | `\citeauthor{k}` | — |
| Year only | `\citeyear{k}` | `\citeyear{k}` | — |
| Bare / short | `\citealp{k}`, `\citealt{k}` | `\cite{k}` (no parens) | — |
| Page-qualified | `\citep[p.~5]{k}` | `\parencite[p.~5]{k}` | — |

- `\citep`/`\citet` belong to **natbib** — if you see them, the project is BibTeX+natbib (or `biblatex` with `natbib=true`).
- `\parencite`/`\textcite`/`\autocite` are **biblatex** — never usable under plain BibTeX.
- Mixing `\citep` into a biblatex doc without `natbib=true` throws `Undefined control sequence`.

## Build sequences

`latexmk` figures out the right sequence automatically (it inspects `.aux`/`.bcf` and runs biber or bibtex as needed):

```bash
latexmk -pdf main.tex        # pdfLaTeX + auto bib + reruns
latexmk -xelatex main.tex    # XeLaTeX pipeline
latexmk -lualatex main.tex   # LuaLaTeX pipeline
```

Manual sequences (when not using latexmk):

```bash
# BibTeX / natbib:
pdflatex main            # writes main.aux with \citation + \bibdata
bibtex   main            # reads main.aux + refs.bib → main.bbl
pdflatex main            # pulls in .bbl
pdflatex main            # resolves cross-refs

# BibLaTeX + Biber (default backend):
pdflatex main            # writes main.bcf (Biber control file)
biber    main            # reads main.bcf + refs.bib → main.bbl
pdflatex main
pdflatex main

# BibLaTeX + bibtex backend (backend=bibtex):
pdflatex main
bibtex   main
pdflatex main
pdflatex main
```

Key distinction: **BibLaTeX default reads `main.bcf` with `biber`; BibTeX reads `main.aux` with `bibtex`.** They produce *different, incompatible* `.bbl` files.

## Common failures → fixes

### Backend mismatch (ran the wrong program)

- **Symptom:** `Package biblatex Warning: File 'main.bbl' is wrong format version` / references missing / `biber` says "Cannot find control file 'main.bcf'".
- **Cause:** ran `bibtex` on a Biber project, or `biber` on a BibTeX project.
- **Fix:** delete `main.bbl` and `main.bcf`/`main.aux`, then run the **matching** program (biber for `\usepackage{biblatex}` default; bibtex only if `backend=bibtex`). Simplest: `latexmk -C && latexmk -pdf main` (clean then rebuild).

### Stale `.bbl`

- **Symptom:** edited `.bib` but the PDF shows old/removed entries; new citation "undefined."
- **Fix:** re-run the bib program (or `latexmk` which detects the change). If truly stuck, `latexmk -c` (clean aux) or delete `main.bbl` and rebuild.

### Missing `.bib` / `I couldn't open database file`

- **BibTeX:** `\bibliography{refs}` takes the name **without** `.bib`; the file must be findable (same dir or `BIBINPUTS`).
- **BibLaTeX:** `\addbibresource{refs.bib}` takes the name **with** `.bib`.
- **Fix:** correct the name/extension per system; confirm the file exists (`ls`).

### Duplicate keys

- **Symptom:** `Repeated entry` (BibTeX `.blg`) or `Duplicate entry key` (biber).
- **Fix:** find the two entries with the same `@type{key,` and rename or delete one. Never let two entries share a key — citations become nondeterministic.

### Unicode in fields (accents/CJK)

- **BibTeX (legacy):** classic 8-bit `bibtex` chokes on raw UTF-8. Either escape (`{\'e}`) or, better, use `biber` (full UTF-8) with `biblatex`.
- **BibLaTeX+Biber:** UTF-8 works natively; ensure the document engine can render the glyphs (Xe/Lua+fontspec for non-Latin).
- **Fix:** don't strip accents from names. Prefer Biber; if locked to BibTeX, escape the specific chars.

### Missing required fields

- **Symptom:** BibTeX warns `Warning--empty journal in key` / `missing publisher`.
- **Fix:** fill the required field per entry type (`@article` needs author/title/journal/year; `@book` needs author/editor + title + publisher + year; `@inproceedings` needs author/title/booktitle/year). If unknown, **flag to the user** — do not fabricate a journal/publisher.

### The illegal mix (`\bibliography` + `biblatex`)

- **Symptom:** `Package biblatex Error: '\bibliography' not allowed` or nothing prints.
- **Fix:** choose ONE. To stay BibLaTeX: replace `\bibliographystyle{...}`+`\bibliography{refs}` with `\usepackage[...]{biblatex}` (preamble) + `\addbibresource{refs.bib}` (preamble) + `\printbibliography` (where the list goes). To stay BibTeX: remove `\usepackage{biblatex}` and use `natbib`/plain.

## `.bbl` portability rule (submission)

Never ship a **BibTeX-produced `.bbl` for a Biber project** (or vice-versa) — the formats differ. For arXiv, if uploading a pre-generated `.bbl`, it must have been produced by the *same* backend the source declares, and its filename must match the main `.tex` basename. See `submission-arxiv.md`.

## Agent checklist

1. Detect system (table / `check-bib.py`). State it explicitly.
2. Confirm citation commands match the system (no `\citep` in a bare biblatex doc, etc.).
3. Run the correct sequence (prefer `latexmk`).
4. Resolve every `undefined citation` by fixing keys — never by inventing entries.
5. If a required field or key is genuinely missing, **report it**; stop and ask.
