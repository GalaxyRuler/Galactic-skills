# Thesis skeleton (GENERIC, on the `report` class)

A starting point for a thesis or dissertation: a generic title page, abstract,
acknowledgements, table of contents, list of figures/tables, chapters via
`\input`, appendices, and a BibLaTeX bibliography.

## This is NOT an official university template

Most institutions mandate their own document class and title/declaration pages
with exact margins and wording. **Before submitting, swap in your institution's
official class** in place of `\documentclass{report}` and adapt (or replace) the
title page in `main.tex`. This skeleton simply lets you start writing chapters
now without waiting on the official class.

## Layout

```
thesis/
├── main.tex               # title page, front matter, \input chapters, appendices
├── chapters/
│   └── introduction.tex   # one chapter per file
├── refs.bib               # PLACEHOLDER bibliography (replace before real use)
├── latexmkrc              # build config: pdfLaTeX + Biber
└── figures/               # graphics referenced via \graphicspath{{figures/}}
```

## Build

- **Engine:** pdfLaTeX
- **Bibliography backend:** BibLaTeX + Biber

```sh
latexmk main.tex     # full build (LaTeX -> Biber -> LaTeX x2)
latexmk -c           # remove aux files (keeps the PDF)
```

By hand:

```sh
pdflatex main
biber main
pdflatex main
pdflatex main
```

## Notes

- Preliminary pages use roman numerals (`\pagenumbering{roman}`); the main
  text switches to arabic at `\pagenumbering{arabic}`.
- `\onehalfspacing` (from `setspace`) satisfies the common "1.5 line spacing"
  requirement; change to `\doublespacing` or `\singlespacing` as required.
- Unnumbered front-matter chapters are added to the ToC explicitly with
  `\addcontentsline`.
- Labels follow a consistent scheme: `ch:`, `sec:`, `fig:`, `tab:`, `eq:`.
