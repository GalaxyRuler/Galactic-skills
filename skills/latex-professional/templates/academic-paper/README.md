# Academic paper template (generic preprint)

A neutral preprint skeleton on the standard `article` class: title with
multiple authors/affiliations, abstract, keywords, numbered sections, an
equation, a figure, a table, and a BibLaTeX bibliography.

## This is NOT a venue template

When you submit to a specific venue, use that venue's **official** class:

| Venue family        | Official class (install separately) |
|---------------------|-------------------------------------|
| IEEE                | `IEEEtran`                          |
| ACM                 | `acmart`                            |
| Springer            | `sn-jnl` (Springer Nature)          |
| Elsevier            | `elsarticle`                        |
| APS (physics)       | `revtex4-2`                         |

This skeleton is only for drafting and for preprint servers (e.g. arXiv) where
a neutral layout is fine. **Do not vendor or ship this layout to a venue that
mandates its own class** --- move your content into the official class instead.

## Layout

```
academic-paper/
├── main.tex     # title/authors, abstract, keywords, sections, refs
├── refs.bib     # PLACEHOLDER bibliography (replace before real use)
├── latexmkrc    # build config: pdfLaTeX + Biber
└── figures/     # graphics referenced via \graphicspath{{figures/}}
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

- For a two-column layout, add `twocolumn` to the `\documentclass` options.
- `\keywords{...}` is a tiny local helper; official venue classes provide their
  own keyword mechanism, so drop it when you migrate.
- Labels follow a consistent scheme: `sec:`, `fig:`, `tab:`, `eq:`.
