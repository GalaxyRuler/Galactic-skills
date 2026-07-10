# Journal Template Modes

Purpose: per-venue compatibility notes so an agent works *with* an official class file instead of fighting or "modernizing" it.

## Prime directive: the venue class is a USER-PROVIDED official input

- The class files (`IEEEtran.cls`, `acmart.cls`, `sn-jnl.cls`, `elsarticle.cls`, `revtex4-2.cls`, a university thesis class) are **the publisher's inputs**, not vendored by this skill. The user supplies them.
- **Respect the template. Do not modernize it blindly.** Don't swap a venue's bibliography style, font setup, or section macros for "better" ones. Reviewers/production check against the official class.
- Don't add packages that the class already provides or forbids. Read the class's own documentation/comments first.
- If the template looks dated (e.g. mandates pdfLaTeX, `inputenc`, `natbib`), that's usually intentional for the production pipeline — leave it.

## Detect the venue from `\documentclass`

Grep the main file's `\documentclass{...}` and the preamble to identify the venue before touching anything:

| `\documentclass` / signal | Venue | Confirming files nearby |
|---|---|---|
| `{IEEEtran}` | IEEE | `IEEEtran.cls`, `IEEEtran.bst` |
| `{acmart}` | ACM | `acmart.cls`, `ACM-Reference-Format.bst`, `\setcopyright` |
| `{sn-jnl}` | Springer Nature | `sn-jnl.cls`, `sn-*.bst`, `\begin{frontmatter}`-like `\author*` macros |
| `{elsarticle}` | Elsevier | `elsarticle.cls`, `elsarticle-num.bst`, `\begin{frontmatter}` |
| `{revtex4-2}` (or `revtex4-1`) | APS/AIP | `revtex4-2.cls`, `apsrev4-2.bst`, `\affiliation` |
| university `.cls` (e.g. `ucthesis`, `mitthesis`) | Thesis | school-supplied class + a formatting guide PDF |

```bash
grep -nE '\\documentclass(\[[^]]*\])?\{[^}]+\}' main.tex   # read the class + options
```

The **class options** carry the venue variant (conference vs journal, reference style, one/two-column). Read them — they change the required bib style and layout. Do not alter them without the venue's guidance.

## Quick venue matrix

| Venue | Class | Engine | Bib expectation | Watch out for |
|---|---|---|---|---|
| IEEE | `IEEEtran` | pdfLaTeX-friendly | `IEEEtran` BibTeX style (`\bibliographystyle{IEEEtran}`) | pick the right template variant (journal vs conference); `\IEEEauthorblock*` |
| ACM | `acmart` | pdfLaTeX (default) | BibTeX + `ACM-Reference-Format` | accessibility rules; correct `\documentclass` option (`sigconf`/`acmsmall`/…); CCS + rights block |
| Springer Nature | `sn-jnl` | often pdfLaTeX-only | their `sn-*.bst` BibTeX styles | no custom fonts; reference-style option must match target journal |
| Elsevier | `elsarticle` | pdfLaTeX | `elsarticle-num`/`-harv` BibTeX | Editorial Manager wants a flat bundle (no subfolders); verify the Overleaf PDF |
| APS/AIP | `revtex4-2` | pdfLaTeX | `\bibliographystyle{apsrev4-2}` (REVTeX + natbib) | `reprint`/`twocolumn` options; `\affiliation` semantics |
| Thesis | university-supplied | varies | university-specified | generic — follow the school's class + guide exactly |

## IEEE — `IEEEtran`

- **Class:** `\documentclass[conference]{IEEEtran}` (conference) or `[journal]`. There's an online IEEE **template selector** — match the exact publication.
- **Engine:** pdfLaTeX-friendly; no fontspec needed. Keep it pdfLaTeX unless you have a specific reason.
- **Bib:** `\bibliographystyle{IEEEtran}` + BibTeX (`IEEEtran.bst`). For BibLaTeX, `IEEEtranN`/`biblatex-ieee` exists but only if the submission allows it — default to the BibTeX style.
- **Structure:** author blocks via `\IEEEauthorblockN`/`\IEEEauthorblockA`; abstract via `\begin{abstract}`; keywords via `\IEEEkeywords`.
- **Gotchas:** don't switch to `hyperref`-heavy setups that clash with `IEEEtran`'s `\IEEEpeerreviewmaketitle`; two-column float placement is finicky — use `figure*`/`table*` for full-width.

## ACM — `acmart`

- **Class:** `\documentclass[sigconf]{acmart}` (also `acmsmall`, `acmlarge`, `manuscript`, `sigplan`, …). Use the ACM **Overleaf template**; the format option must match the venue (SIGCONF, TAPS, etc.).
- **Engine:** pdfLaTeX default. `acmart` supports Xe/Lua but the ACM production pipeline (TAPS) expects standard setups — don't deviate.
- **Bib:** BibTeX with `ACM-Reference-Format` (`\bibliographystyle{ACM-Reference-Format}`) — the class often sets this; don't override.
- **Accessibility (ACM enforces):**
  - **Do not encode information by color alone** — use labels/patterns/markers too (colorblind readers, B/W print).
  - Provide alt text (`\Description{...}`) for every figure.
  - Use real text, not images of text; keep tables machine-readable.
- **Gotchas:** the rights/CCS block (`\setcopyright`, `\ccsdesc`, `\keywords`) is mandatory; anonymous review via `\documentclass[...,anonymous]{acmart}` or `\settopmatter{authorsperrow=...}`.

## Springer Nature — `sn-jnl`

- **Class:** `\documentclass[pdflatex,sn-mathphys-num]{sn-jnl}` (options select the reference style: `sn-mathphys-num`, `sn-basic`, `sn-aps`, `sn-vancouver`, etc.). Use Springer's official template for the target journal.
- **Engine:** **some Springer flows require pdfLaTeX** — the class option `[pdflatex]` signals it. Don't switch to Xe/Lua unless the journal explicitly permits.
- **Fonts:** **no custom fonts** — use the class defaults. Springer production replaces fonts anyway.
- **Bib:** their `sn-*.bst` BibTeX styles chosen via the class option; keep `\bibliography{...}` + the matching style.
- **Gotchas:** the reference-style class option and the `.bst` must agree; equation/figure numbering conventions are class-controlled — don't override.

## Elsevier — `elsarticle`

- **Class:** `\documentclass[preprint,review]{elsarticle}` (also `1p`/`3p`/`5p`, `times`, `authoryear`/`number`).
- **Engine:** pdfLaTeX.
- **Bib:** `elsarticle-num` (numbered) or `elsarticle-harv` (author-year) BibTeX styles: `\bibliographystyle{elsarticle-num}`.
- **Editorial Manager packaging:**
  - **Bundle all source when requested; NO subfolders.** Editorial Manager's compiler expects a **flat** file set — move `figures/x.pdf` to top level and update paths, or the build fails to find assets.
  - Provide the `.bib` (or a correct `.bbl`), the class if not standard, and all figures at top level.
- **Overleaf caveat:** **verify the Overleaf-produced PDF** — Overleaf can emit a PDF *despite* compile errors (it shows the last good pages). Always open the log and confirm zero errors before submitting; a "PDF appeared" is not proof of a clean build.
- **Gotchas:** `\author`/`\affiliation`/`\ead` macros are Elsevier-specific; front matter via `\begin{frontmatter}`.

## APS / AIP — `revtex4-2`

- **Class:** `\documentclass[aps,prl,reprint]{revtex4-2}` (journal option: `prl`, `prd`, `rmp`, …; `aip` for AIP journals). Use `reprint` for two-column camera-ready, `preprint` for review.
- **Engine:** pdfLaTeX.
- **Bib:** `\bibliographystyle{apsrev4-2}` (or `aipnum4-2`) with **natbib** (REVTeX loads its own natbib-compatible citation). Use `\cite`; REVTeX handles the formatting.
- **Gotchas:** `\affiliation` must immediately follow the `\author` it applies to; `\collaboration`; footnote-style affiliations differ from other classes. Table/figure `*` variants for full-width in two-column. Don't load a conflicting citation package.

## Thesis / dissertation classes (generic)

- **Class is USER-SUPPLIED** by the university (e.g. `ucbthesis`, `mitthesis`, a department `.cls`). This skill does **not** ship one.
- **Engine:** whatever the class/guide specifies — often pdfLaTeX, sometimes Xe/Lua for fonts. Honor `% !TEX program`.
- **Bib:** per the graduate school's citation requirement (natbib+BibTeX or biblatex); don't change it to your preference.
- **Structure:** frontmatter (title page, abstract, ToC), chapters via `\input`/`\include` (mind the arXiv-style `\include` write note only if submitting elsewhere), appendices.
- **Gotchas:** margin/spacing rules are strict and format-checked by the school — do not "improve" margins, line spacing, or fonts. Follow the university guide literally.

## Minimal skeletons (for orientation — never replace the user's real template)

These show the shape each class expects so you recognize a broken one. Always keep the user's actual preamble; these are reference only.

```latex
% IEEE (conference)
\documentclass[conference]{IEEEtran}
\begin{document}
\title{...}
\author{\IEEEauthorblockN{Name}\IEEEauthorblockA{Affiliation}}
\maketitle
\begin{abstract}...\end{abstract}
\begin{IEEEkeywords}...\end{IEEEkeywords}
...
\bibliographystyle{IEEEtran}\bibliography{refs}
\end{document}
```

```latex
% ACM (sigconf)
\documentclass[sigconf]{acmart}
\setcopyright{acmlicensed}
\begin{document}
\title{...}
\author{Name}\affiliation{\institution{...}}
\begin{abstract}...\end{abstract}
\keywords{...}
\maketitle
...
\bibliographystyle{ACM-Reference-Format}\bibliography{refs}
\end{document}
```

```latex
% Elsevier
\documentclass[preprint,review]{elsarticle}
\begin{document}
\begin{frontmatter}
  \title{...}
  \author{Name}\affiliation{organization={...}}
  \begin{abstract}...\end{abstract}
  \begin{keyword}...\end{keyword}
\end{frontmatter}
...
\bibliographystyle{elsarticle-num}\bibliography{refs}
\end{document}
```

## General agent workflow for any venue

```
1. Identify the class (\documentclass{...}) and its options. Look up its official docs.
2. Confirm the engine the class expects (matrix above / % !TEX program). Default pdfLaTeX.
3. Use the venue's bib style — do not substitute a different .bst or switch BibTeX↔biblatex.
4. Keep the class's front-matter macros; don't replace them with generic ones.
5. Respect layout/accessibility mandates (ACM color rule, Springer no-fonts, Elsevier flat bundle).
6. Compile and READ THE LOG (Overleaf can show a PDF despite errors).
7. Do not modernize the template. If something must change, confirm the venue allows it.
```
