# Article template (generic `article` class)

A minimal single-document article using standard LaTeX only. No venue or
publisher class is involved.

## Layout

```
article/
├── main.tex          # the document
├── refs.bib          # PLACEHOLDER bibliography (replace before real use)
├── latexmkrc         # build config: pdfLaTeX + Biber
├── figures/          # put example.pdf and other graphics here
└── sections/         # optional: split long docs into \input files here
```

## Build

- **Engine:** pdfLaTeX
- **Bibliography backend:** BibLaTeX + Biber

```sh
latexmk main.tex     # full build (LaTeX -> Biber -> LaTeX x2)
latexmk -c           # remove aux files (keeps the PDF)
latexmk -C           # remove aux files and the PDF
```

`latexmk` reads the bundled `latexmkrc`, so you do not need extra flags.

If you build by hand instead of with `latexmk`:

```sh
pdflatex main
biber main
pdflatex main
pdflatex main
```

## Notes

- Colours/links come from `hyperref`; smart references (`\Cref`) come from
  `cleveref`, which is loaded last on purpose.
- Graphics resolve through `\graphicspath{{figures/}}`; use relative names
  such as `\includegraphics{example.pdf}`.
- Labels follow a consistent scheme: `sec:`, `fig:`, `tab:`, `eq:`.
