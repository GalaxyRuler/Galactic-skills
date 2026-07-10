# Beamer template (minimal deck)

A minimal presentation using Beamer's **built-in** `Madrid` theme, so there are
no extra theme dependencies to install. (`metropolis` and similar are nice but
require separate packages/fonts; this deck deliberately avoids them.)

## Layout

```
beamer/
├── main.tex     # title frame, bullets, figure, table, references
├── refs.bib     # PLACEHOLDER bibliography (replace before real use)
└── figures/     # create as needed; example.pdf is referenced by main.tex
```

There is no `latexmkrc` here; the default `latexmk` behaviour builds a Beamer
deck correctly. Copy one of the variants from `../latexmkrc/` if you want a
pinned config.

## Build

- **Engine:** pdfLaTeX
- **Bibliography backend:** BibLaTeX + Biber

```sh
latexmk -pdf main.tex     # full build (LaTeX -> Biber -> LaTeX x2)
latexmk -c                # remove aux files (keeps the PDF)
```

By hand:

```sh
pdflatex main
biber main
pdflatex main
pdflatex main
```

## Notes

- `aspectratio=169` gives 16:9 slides; drop it for the classic 4:3.
- The references frame uses `[allowframebreaks]` so a long bibliography spills
  onto extra slides automatically.
- To try a different built-in look, change `\usetheme{Madrid}` to another
  bundled theme such as `default`, `Warsaw`, `Berlin`, or `Copenhagen` --- all
  ship with Beamer, no extra packages needed.
- Add the `figures/` directory yourself and drop `example.pdf` in it before
  building the figure frame.
