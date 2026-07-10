# Tables & Figures

Purpose: produce publication-grade tables (booktabs, siunitx) and portable figures (relative paths, correct formats per engine) that survive submission.

## Tables: booktabs is the baseline

Rules for professional tables:
- **No vertical rules.** Ever. `booktabs` philosophy: whitespace separates columns, not lines.
- **Three horizontal rules only:** `\toprule` (top), `\midrule` (below header), `\bottomrule` (end). Use `\cmidrule(lr){2-3}` for a rule spanning a subset of columns.
- **No double rules.** No `\hline\hline`.
- Caption goes **above** tables (convention), **below** figures.

```latex
\begin{table}[t]
  \centering
  \caption{Model accuracy by dataset.}
  \label{tab:accuracy}
  \begin{tabular}{l S[table-format=2.1] S[table-format=2.1]}
    \toprule
    Model & {Dev (\%)} & {Test (\%)} \\
    \midrule
    Baseline      & 71.2 & 69.8 \\
    Ours          & 78.5 & 77.1 \\
    \bottomrule
  \end{tabular}
\end{table}
```

Note: `table` = the floating wrapper (caption, placement, numbering). `tabular` = the grid itself. `tabular` can appear without `table` (inline, non-floating); `table` without `tabular` is pointless.

## Column-type cheat sheet

| Need | Use | Notes |
|---|---|---|
| Fixed left/center/right | `l` / `c` / `r` | basic `tabular` columns |
| Wrap text to a fixed width | `p{3cm}` (top), `m{3cm}` (mid, `array` pkg), `b{3cm}` (bottom) | manual width |
| Auto-stretch text column to fill `\linewidth` | `tabularx` `X` column | needs total width arg |
| Numeric decimal alignment | `siunitx` `S` column | aligns on decimal point; put text headers in `{ }` |
| Span columns | `\multicolumn{2}{c}{Header}` | merges horizontally |
| Span rows | `\multirow{2}{*}{Label}` (`multirow` pkg) | merges vertically |

### tabularx (fit to a width, wrap text)

```latex
\begin{tabularx}{\linewidth}{l X X}
  \toprule
  Field & Description & Notes \\
  \midrule
  name  & The record's display name & wraps automatically \\
  \bottomrule
\end{tabularx}
```

`X` columns share the leftover width and wrap. Combine `l`/`r`/`c` fixed columns with `X` flexible ones.

### siunitx S-columns (numeric alignment)

```latex
\usepackage{siunitx}
\begin{tabular}{l S[table-format=3.2] S[table-format=1.3e1]}
  \toprule
  Run & {Time (s)} & {Loss} \\
  \midrule
  A & 12.40 & 3.1e-2 \\
  B &  9.05 & 2.7e-2 \\
  \bottomrule
\end{tabular}
```

- `table-format=3.2` = up to 3 integer + 2 decimal digits; aligns on the decimal point.
- Header text in an `S` column **must be braced** `{Time (s)}` so siunitx doesn't try to parse it as a number.
- Use `\num{}`/`\SI{}{}` in text for consistent number/unit formatting. Don't change any numeric values when reformatting.

### longtable (multi-page tables)

For tables that span pages (can't float):

```latex
\usepackage{longtable}
\begin{longtable}{l r}
  \caption{Long list.}\label{tab:long}\\
  \toprule Item & Value \\ \midrule
  \endfirsthead
  \toprule Item & Value \\ \midrule
  \endhead
  \midrule \multicolumn{2}{r}{\emph{continued}} \\
  \endfoot
  \bottomrule
  \endlastfoot
  ...rows...
\end{longtable}
```

- `longtable` is NOT wrapped in `table` (it manages its own float/caption).
- For a wide *and* long table, `xltabular` combines `longtable` + `tabularx`.
- Requires an extra compile pass for column widths to settle (latexmk handles it).

## Label conventions

Prefix labels by type so `\cref` can name them and humans can scan:

| Kind | Prefix | Example |
|---|---|---|
| Section | `sec:` | `\label{sec:method}` |
| Figure | `fig:` | `\label{fig:arch}` |
| Table | `tab:` | `\label{tab:results}` |
| Equation | `eq:` | `\label{eq:loss}` |
| Algorithm | `alg:` | `\label{alg:train}` |
| Appendix | `app:` | `\label{app:proofs}` |

Place `\label` **immediately after `\caption`** (not before) so the counter is correct. Reference with `\cref{fig:arch}` (cleveref auto-prints "Figure 3").

## Figures

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=0.8\linewidth]{figures/architecture}
  \caption{System architecture.}
  \label{fig:arch}
\end{figure}
```

Rules:
- **Relative paths only.** `figures/architecture`, never `C:/Users/.../architecture.pdf`. Absolute paths break on every other machine and on arXiv.
- **Omit the extension** and let the engine choose the best available (`.pdf` > `.png` > `.jpg` typically). Being explicit is fine too, but omission aids format-swapping.
- Use `\graphicspath{{figures/}{img/}}` (trailing slashes, each in its own braces) to set search dirs so you can write bare filenames.
- Size with `width=...\linewidth` / `\textwidth` — relative units, not fixed `cm`, so it adapts to the column.
- `\caption` goes **below** the image (figure convention).

### Supported graphics formats per engine

| Format | pdfLaTeX | XeLaTeX | LuaLaTeX | Note |
|---|---|---|---|---|
| PDF | ✅ | ✅ | ✅ | preferred for vector figures |
| PNG | ✅ | ✅ | ✅ | raster; good for screenshots |
| JPG/JPEG | ✅ | ✅ | ✅ | raster; photos |
| EPS | ❌ direct → `epstopdf` | ❌ direct → `epstopdf` | same | `epstopdf` (restricted shell escape) converts on the fly; or pre-convert |

- **pdfLaTeX/Xe/Lua cannot embed EPS directly** — `epstopdf` (auto-loaded by `graphicx` under `\usepackage{epstopdf}` or restricted shell escape) converts it. For arXiv EPS-only sources, use the classic `latex`+`dvips` route instead. See `submission-arxiv.md`.
- Don't mix EPS with PDF/raster in a way that forces two incompatible pipelines; standardize on PDF where possible.

### Subfigures (use subcaption)

```latex
\usepackage{subcaption}
\begin{figure}[t]
  \centering
  \begin{subfigure}[b]{0.48\linewidth}
    \includegraphics[width=\linewidth]{figures/a}
    \caption{Case A.}\label{fig:a}
  \end{subfigure}\hfill
  \begin{subfigure}[b]{0.48\linewidth}
    \includegraphics[width=\linewidth]{figures/b}
    \caption{Case B.}\label{fig:b}
  \end{subfigure}
  \caption{Two cases.}\label{fig:both}
\end{figure}
```

Reference sub-parts with `\cref{fig:a}` → "Figure 3a". **Use `subcaption`**, not obsolete `subfigure` or older `subfig` — never mix them (see `package-compatibility.md`).

### wrapfig caution

`\usepackage{wrapfig}` wraps text around a figure but is **fragile**: it misbehaves near page breaks, list environments, section headings, and other floats, often producing overlaps or bad spacing. Use sparingly; verify the rendered page. Prefer a normal float unless the layout truly requires wrapping.

## Placement specifiers

- `[t]` top, `[b]` bottom, `[h]` here-ish, `[p]` float page, `[!]` override LaTeX's aesthetics, `[H]` (needs `float` pkg) forces exactly here.
- Prefer `[t]` or `[tb]` for papers; avoid `[H]` unless a reviewer/venue demands exact placement — it disables float management and can cause overfull pages.

## Asset verification

Run `python scripts/check-latex-assets.py <main>.tex` to list every `\includegraphics`/`\input`/`\include` target and flag: missing files, absolute paths, case-mismatched names, and formats incompatible with the detected engine. Fix flagged paths **before** compiling or submitting — a missing figure is a hard error (`File not found`, see `compile-error-playbook.md`).

## Agent checklist

1. Tables use booktabs rules, no verticals; caption above.
2. Numeric columns aligned via `siunitx` `S`; values unchanged.
3. Figures use relative paths + `\linewidth` sizing; caption below.
4. Labels prefixed (`fig:`/`tab:`/...) and placed after `\caption`.
5. Graphics formats match the engine; EPS handled via epstopdf or the right pipeline.
6. `check-latex-assets.py` reports no missing/absolute-path assets.
