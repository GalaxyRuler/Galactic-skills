# `latexmkrc` variants

Ready-to-copy `latexmk` configuration files. Each one is self-contained; pick
the one that matches your engine and bibliography backend and copy it into your
project.

## How to use

Copy the chosen file into your project root under one of these names:

- `latexmkrc` (no dot) --- picked up when you run `latexmk` from that directory.
- `.latexmkrc` (hidden) --- the traditional per-project name; also works.

```sh
cp latexmkrc-biber /path/to/project/latexmkrc
cd /path/to/project
latexmk main.tex
```

(`latexmk` also reads a global `~/.latexmkrc`; a project-local file overrides it
for that project.)

## Which one?

| File                 | Engine     | Bibliography backend        | Use when |
|----------------------|------------|-----------------------------|----------|
| `latexmkrc-pdflatex` | pdfLaTeX   | auto-detected               | Simple ASCII/Latin-1 docs; let latexmk decide biber vs bibtex. |
| `latexmkrc-xelatex`  | XeLaTeX    | auto-detected               | Unicode text and system fonts via `fontspec`. |
| `latexmkrc-lualatex` | LuaLaTeX   | auto-detected               | Unicode/system fonts; Lua scripting. |
| `latexmkrc-biber`    | pdfLaTeX   | **Biber** (forced)          | **Recommended default.** BibLaTeX with `backend=biber`. |
| `latexmkrc-bibtex`   | pdfLaTeX   | **BibTeX** (forced)         | Legacy/natbib or a venue that requires BibTeX. |

**Default recommendation: `latexmkrc-biber`.** All templates in this package use
BibLaTeX + Biber.

## Switching engine on a biber/bibtex config

The engine and the backend are independent. To use Biber with XeLaTeX, start
from `latexmkrc-biber` and change the engine line:

```perl
$pdf_mode = 5;   # xelatex   (4 = lualatex)
$xelatex  = 'xelatex -interaction=nonstopmode -halt-on-error -file-line-error %O %S';
```

## Notes

- `-halt-on-error -file-line-error` make failures stop early with clear
  `file:line` messages --- useful for both humans and automated agents.
- `run.xml` is produced by Biber only; it is harmless to list in `$clean_ext`
  for BibTeX configs but is omitted from `latexmkrc-bibtex` for tidiness.
- None of these enable `-shell-escape`; add it yourself only if a package
  (e.g. `minted`) genuinely needs it, and understand the security implications.
