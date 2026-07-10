# Table snippets

Copy-paste LaTeX blocks for common tables. Preambles list only the extra
packages each snippet needs beyond `graphicx`/`hyperref`/`cleveref`.

Rules of thumb:

- Use **`booktabs`** rules (`\toprule`, `\midrule`, `\bottomrule`) --- never
  vertical rules, rarely `\hline`.
- Wrap every table in a `table` float with a `\caption` **above** the tabular
  and a `\label` after the caption. Label scheme: `tab:`.
- Right-align numbers; left-align text.

---

## 1. Basic booktabs table

Preamble:

```latex
\usepackage{booktabs}
```

Body:

```latex
\begin{table}[htbp]
  \centering
  \caption{A basic table with booktabs rules.}
  \label{tab:basic}
  \begin{tabular}{lrr}
    \toprule
    Method   & Accuracy & Time (s) \\
    \midrule
    Baseline & 0.81     & 12.4     \\
    Ours     & 0.89     &  9.7     \\
    \bottomrule
  \end{tabular}
\end{table}
```

---

## 2. `tabularx` --- automatic column widths to a fixed total width

`X` columns share the leftover width so the table hits the target width exactly.

Preamble:

```latex
\usepackage{booktabs}
\usepackage{tabularx}
```

Body:

```latex
\begin{table}[htbp]
  \centering
  \caption{A full-width table; the description column wraps automatically.}
  \label{tab:tabularx}
  \begin{tabularx}{\linewidth}{l r X}
    \toprule
    Symbol & Value & Description \\
    \midrule
    $\alpha$ & 0.05 & Significance level used for all hypothesis tests. \\
    $\beta$  & 0.20 & Type-II error target for the power analysis. \\
    \bottomrule
  \end{tabularx}
\end{table}
```

Tip: for a right-aligned `X` column, define `\newcolumntype{R}{>{\raggedleft\arraybackslash}X}` (needs `array`).

---

## 3. `longtable` --- tables that break across pages

Do **not** wrap `longtable` in a `table` float; it is its own float-like
environment and manages page breaks itself.

Preamble:

```latex
\usepackage{booktabs}
\usepackage{longtable}
```

Body:

```latex
\begin{longtable}{lrr}
  \caption{A long table that continues across pages.}
  \label{tab:longtable} \\
  \toprule
  Item & Count & Share \\
  \midrule
  \endfirsthead

  \multicolumn{3}{c}{\tablename\ \thetable{} -- continued} \\
  \toprule
  Item & Count & Share \\
  \midrule
  \endhead

  \midrule
  \multicolumn{3}{r}{continued on next page} \\
  \endfoot

  \bottomrule
  \endlastfoot

  Alpha & 120 & 0.24 \\
  Beta  &  98 & 0.19 \\
  % ... many more rows ...
  Omega &  15 & 0.03 \\
\end{longtable}
```

---

## 4. `siunitx` S-column --- align numbers on the decimal point

The `S` column aligns on the decimal marker and handles units, uncertainties,
and significant figures. Protect header text with braces `{...}`.

Preamble:

```latex
\usepackage{booktabs}
\usepackage{siunitx}
```

Body:

```latex
\begin{table}[htbp]
  \centering
  \caption{Numbers aligned on the decimal point with siunitx.}
  \label{tab:siunitx}
  \begin{tabular}{l S[table-format=3.2] S[table-format=1.3]}
    \toprule
    {Method}  & {Score} & {p-value} \\
    \midrule
    Baseline  &  81.20  & 0.047 \\
    Ours      & 128.95  & 0.003 \\
    \bottomrule
  \end{tabular}
\end{table}
```

`table-format=3.2` reserves 3 integer + 2 decimal digits so columns line up.

---

## 5. `multirow` / `multicolumn` --- spanning cells

`\multicolumn` spans columns (built in); `\multirow` spans rows (needs the
`multirow` package). Use `\cmidrule(lr){...}` for rules under grouped headers.

Preamble:

```latex
\usepackage{booktabs}
\usepackage{multirow}
```

Body:

```latex
\begin{table}[htbp]
  \centering
  \caption{Spanning cells with multirow and multicolumn.}
  \label{tab:spanning}
  \begin{tabular}{llrr}
    \toprule
    \multirow{2}{*}{Model} & \multirow{2}{*}{Size}
      & \multicolumn{2}{c}{Accuracy} \\
    \cmidrule(lr){3-4}
      &        & Dev  & Test \\
    \midrule
    \multirow{2}{*}{Ours}
      & small  & 0.84 & 0.82 \\
      & large  & 0.90 & 0.88 \\
    \bottomrule
  \end{tabular}
\end{table}
```

---

## Reference in text

```latex
See \Cref{tab:basic} for the main results.   % cleveref -> "Table 1"
```
