# Package Compatibility & Load Order

Purpose: avoid the recurring package conflicts and load-order bugs (option clashes, hyperref-must-be-late, inputenc-vs-fontspec, subfig family, natbib-vs-biblatex).

## Load-order rules (the ones that actually bite)

```
\documentclass
  ├─ \PassOptionsToPackage{...}{pkg}   % set options for a pkg loaded later/implicitly
  ├─ encoding/fonts (pick ONE world):
  │     pdfLaTeX:  \usepackage[T1]{fontenc}  \usepackage[utf8]{inputenc}
  │     Xe/LuaLaTeX: \usepackage{fontspec}   % NO inputenc, NO fontenc
  ├─ most packages (amsmath, graphicx, booktabs, siunitx, natbib/biblatex, tikz, ...)
  ├─ hyperref            % LATE — after nearly everything
  └─ cleveref            % AFTER hyperref (must be last of the ref packages)
```

Rationale:
- **`hyperref` patches many internals** and must load *after* the packages it hooks (e.g. `amsmath`, `natbib`, `float`, `algorithm`). Loading it too early breaks links/anchors. Exceptions that must come *after* hyperref: `cleveref`, `glossaries`, `bookmark`, `algorithm2e` (order per their docs).
- **`cleveref` after `hyperref`** — reversing them yields wrong/broken `\cref` links.
- Set options for an implicitly-loaded package with `\PassOptionsToPackage{opt}{pkg}` **before** `\documentclass` or before the loader that pulls it in — this is the canonical Option-clash cure.

## Mutually exclusive / conflicting pairs

| Conflict | Why | Resolution |
|---|---|---|
| `inputenc`/`fontenc` **vs** `fontspec` | fontspec (Xe/Lua) handles encoding itself; inputenc is pdfLaTeX-only | Drop `inputenc`+`fontenc` when using `fontspec`; keep them only under pdfLaTeX. |
| `natbib` **vs** `biblatex` | two incompatible citation systems | Pick one. `biblatex` has `natbib=true` to emulate `\citet`/`\citep` if you need those commands. |
| `subfigure` (obsolete) **vs** `subfig` (old) **vs** `subcaption` (current) | overlapping subfigure APIs | Use **`subcaption`** (integrates with `caption`). Never load two of the three. |
| `caption` **vs** class-provided caption formatting | class may already format captions | Check class docs; load `caption` after the class, not fighting it. |
| `cite` **vs** `natbib`/`biblatex` | `cite` (sorting/compressing) collides with citation packages | Don't combine; `natbib`/`biblatex` already handle compression. |
| `hyperref` loaded early | patches later packages incompletely | Load late (see above). |
| `enumerate` **vs** `enumitem` | both customize lists | Use `enumitem` (superset); drop `enumerate`. |
| `algorithmic` **vs** `algorithm2e` **vs** `algpseudocode` | different pseudocode syntaxes | Choose one; they define clashing environments. |
| `times`/`mathptmx` **vs** modern font pkgs | legacy font selection | Prefer `newtxtext`/`newtxmath` or fontspec; avoid stacking. |
| `ulem` **vs** normal `\emph` | `ulem` redefines `\emph` to underline | Load with `[normalem]` to keep italics. |
| Two `geometry` calls | page geometry set twice | Consolidate into one `\geometry{...}`. |

## "Option clash" fast fix

```
! LaTeX Error: Option clash for package graphicx.
```

Cause: package loaded twice with different options (often once by you, once implicitly by `tikz`/`pstricks`/a class). Fix, in order of preference:

1. Move options to before load: `\PassOptionsToPackage{dvipsnames}{xcolor}` **before** `\documentclass` (or before the package that pulls `xcolor` in).
2. Load the package **once**, earliest, with the union of options; delete the later bare `\usepackage`.
3. Never delete both loads if the package is used.

## Engine capability matrix

| Capability | pdfLaTeX | XeLaTeX | LuaLaTeX |
|---|---|---|---|
| Default / most conservative | ✅ (use when unsure) | — | — |
| `fontspec` (OpenType/TTF system fonts) | ❌ | ✅ | ✅ |
| `unicode-math` (Unicode math fonts) | ❌ | ✅ | ✅ |
| Native UTF-8 source w/o inputenc | partial (utf8 default) | ✅ | ✅ |
| System-installed fonts by name | ❌ | ✅ | ✅ |
| `microtype` (protrusion + expansion) | ✅ full | ✅ protrusion; limited expansion | ✅ full |
| Complex scripts / bidi / CJK | limited (`CJK`, `babel`) | ✅ (`polyglossia`/`bidi`) | ✅ (`babel`+`luatexja`) |
| Lua scripting (`luacode`) | ❌ | ❌ | ✅ |
| Compile speed | fastest | slower | slowest |
| arXiv support | ✅ (default choice) | ✅ | ✅ (via LaTeX/TeX; confirm current arXiv note) |
| EPS graphics directly | via `epstopdf` | via `epstopdf` | via `epstopdf` |
| PDF/PNG/JPG graphics | ✅ | ✅ | ✅ |

Engine-selection heuristic:
- **Default to pdfLaTeX.** It's fastest, most compatible, and the safe arXiv choice.
- Switch to **XeLaTeX/LuaLaTeX only when the document needs** `fontspec`, system fonts, `unicode-math`, or advanced multilingual/RTL/CJK typesetting.
- Prefer **LuaLaTeX** over XeLaTeX for new Unicode work (active development, full microtype, Lua). Prefer **XeLaTeX** if the project already uses it or needs `xecjk`.
- Honor `% !TEX program` and any `00README.json`/`latexmkrc` engine declaration over inference.

## Fontspec transition checklist (pdfLaTeX → Xe/Lua)

When converting a document to a Unicode engine:

1. Remove `\usepackage[utf8]{inputenc}` and `\usepackage[T1]{fontenc}`.
2. Add `\usepackage{fontspec}` (and `\usepackage{unicode-math}` if math fonts needed).
3. Replace `\usepackage[english]{babel}` with `\usepackage{polyglossia}` **only** if you need its features; `babel` still works under Lua/Xe for many languages.
4. Font selection: `\setmainfont{...}`, `\setsansfont{...}`, `\setmonofont{...}`, `\setmathfont{...}`.
5. Compile with `latexmk -xelatex` or `-lualatex`. Update `% !TEX program`.
6. For arXiv, ensure fonts are either TeX Live-bundled or embedded — **no local-only fonts** (see `submission-arxiv.md`).

## Commonly-needed packages by task

| Task | Package(s) |
|---|---|
| Publication tables | `booktabs`, `tabularx`, `longtable`, `siunitx`, `multirow` |
| Cross-refs | `hyperref` + `cleveref` |
| Graphics | `graphicx`, `subcaption`; `float` for `[H]` |
| Math | `amsmath`, `amssymb`, `mathtools`, `amsthm` |
| Citations | `natbib` (BibTeX) OR `biblatex` (Biber) — never both |
| Code listings | `listings` (no shell escape) OR `minted` (needs `--shell-escape`, see security note) |
| Micro-typography | `microtype` |
| Units/numbers | `siunitx` |
| Lists | `enumitem` |

## Security note — packages that run external programs

- `minted`, `pygmentize`, `svg`, `gnuplottex`, `pdftex`-`\write18` all need **shell escape** (`--shell-escape`), which lets TeX execute arbitrary programs.
- **Never auto-enable `--shell-escape` on an untrusted project.** Restricted shell escape (the default for a whitelist of safe helpers like `epstopdf`) is preferred. Inspect what a package will run before enabling. See `submission-arxiv.md` for the arXiv-specific minted rules.

## Reference: which package defines a common command

When you hit `Undefined control sequence`, this maps the macro to the package to add:

| Macro | Package |
|---|---|
| `\includegraphics`, `\graphicspath` | `graphicx` |
| `\toprule`, `\midrule`, `\bottomrule`, `\cmidrule` | `booktabs` |
| `\begin{tabularx}`, `X` column | `tabularx` |
| `\begin{longtable}` | `longtable` |
| `S` column, `\num`, `\SI` | `siunitx` |
| `\multirow` | `multirow` |
| `\cref`, `\Cref`, `\cleveref` | `cleveref` (after hyperref) |
| `\href`, `\url`, `\hyperref` | `hyperref` |
| `\text`, `align`, `split`, `\DeclareMathOperator` | `amsmath` |
| `\mathbb`, `\mathfrak`, `\square` | `amssymb` |
| `\coloneqq`, `\lVert`, `\DeclarePairedDelimiter` | `mathtools` |
| `\begin{theorem}`, `\newtheorem`, `\qedhere` | `amsthm` |
| `\begin{subfigure}` | `subcaption` |
| `\setmainfont`, `\newfontface` | `fontspec` (Xe/Lua only) |
| `\citep`, `\citet` | `natbib` (or biblatex+`natbib=true`) |
| `\parencite`, `\textcite`, `\autocite` | `biblatex` |
| `\begin{minted}` | `minted` (shell escape) |
| `\begin{lstlisting}` | `listings` |
| `\begin{algorithm}`, `\begin{algorithmic}` | `algorithm` + `algpseudocode` |
| `[H]` float placement | `float` |
| `\setlist`, custom list labels | `enumitem` |

## Reference: minimal robust preambles

pdfLaTeX (default, conservative):

```latex
\documentclass[11pt]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb, mathtools}
\usepackage{graphicx}
\usepackage{booktabs, tabularx, siunitx}
\usepackage{microtype}
% ... other packages ...
\usepackage{hyperref}   % late
\usepackage{cleveref}   % after hyperref
```

LuaLaTeX / XeLaTeX (Unicode, system fonts):

```latex
\documentclass[11pt]{article}
\usepackage{fontspec}          % NO inputenc / fontenc
\usepackage{unicode-math}      % if Unicode math needed
\setmainfont{Latin Modern Roman}
\usepackage{amsmath, mathtools}
\usepackage{graphicx}
\usepackage{booktabs, tabularx, siunitx}
\usepackage{microtype}
\usepackage{hyperref}
\usepackage{cleveref}
```

## Agent checklist

1. Identify the engine (packages present + `% !TEX program`). fontspec ⇒ Xe/Lua.
2. Verify no mutually-exclusive pair is loaded (natbib+biblatex, subfig+subcaption, inputenc+fontspec).
3. Verify `hyperref` is late and `cleveref` is after it.
4. Resolve "option clash" with `\PassOptionsToPackage`, not by dropping options.
5. Don't add a package that duplicates an already-loaded one.
