# Report template (generic `report` class)

A longer document using the standard `report` class, which provides
`\chapter`. Chapters are split into separate files under `sections/` and
pulled in with `\input`.

## Layout

```
report/
├── main.tex          # master file: title, ToC, \input chapters, appendix
├── sections/
│   └── intro.tex     # one chapter per file
├── refs.bib          # PLACEHOLDER bibliography (replace before real use)
├── latexmkrc         # build config: pdfLaTeX + Biber
└── figures/          # graphics referenced via \graphicspath{{figures/}}
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

- Add a new chapter by creating `sections/<name>.tex` (starting with
  `\chapter{...}`) and adding `\input{sections/<name>}` to `main.tex`.
- Chapter files must NOT contain `\documentclass` or `\begin{document}`.
- Appendices come after `\appendix`; chapter numbering switches to letters.
- `\printbibliography[heading=bibintoc]` lists the bibliography in the ToC.
- Labels follow a consistent scheme: `ch:`, `sec:`, `fig:`, `tab:`, `eq:`.
