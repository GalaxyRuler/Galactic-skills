# Book template (generic `book` class)

A book skeleton using the standard `book` class: parts, chapters, and the
`\frontmatter` / `\mainmatter` / `\backmatter` structure.

> If you want more built-in design control (custom chapter styles, margin
> notes, verbatim page layout), the `memoir` class is a drop-in alternative:
> change `\documentclass{book}` to `\documentclass{memoir}`. Everything in
> this skeleton also works under `memoir`.

## Layout

```
book/
├── main.tex          # front/main/back matter, parts, \input chapters
├── chapters/
│   └── chapter1.tex  # one chapter per file
├── refs.bib          # PLACEHOLDER bibliography (replace before real use)
├── latexmkrc         # build config: pdfLaTeX + Biber (+ index)
└── figures/          # create as needed; referenced via \graphicspath
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

## Optional index

An index is wired up but disabled. To enable it:

1. Uncomment `\usepackage{makeidx}` and `\makeindex` in `main.tex`.
2. Uncomment `\printindex` near the end of `main.tex`.
3. Mark terms with `\index{term}` in the text.

`latexmk` runs `makeindex` for you; a manual build needs `makeindex main.idx`
between the LaTeX passes.

## Notes

- `\frontmatter` uses roman page numbers and unnumbered chapters; `\mainmatter`
  switches to arabic numbers and numbered chapters; `\backmatter` unnumbers
  chapters again (for the bibliography and index).
- `openright` starts each chapter on a right-hand page (drop it for one-sided).
- Labels follow a consistent scheme: `part:`, `ch:`, `sec:`, `fig:`, `tab:`,
  `eq:`.
