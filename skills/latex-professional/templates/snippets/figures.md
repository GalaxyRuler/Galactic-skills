# Figure snippets

Copy-paste LaTeX blocks for common figures. Preambles list only the extra
packages each snippet needs.

Rules of thumb:

- Wrap graphics in a `figure` float with `\centering`, a `\caption` **below**
  the graphic, and a `\label` after the caption. Label scheme: `fig:`.
- Set `\graphicspath{{figures/}}` once in the preamble and refer to files by
  their **relative** name (`example.pdf`, not `/home/user/.../example.pdf`).
- Prefer vector formats (`.pdf`, `.eps` via engine support) for plots and
  diagrams; use `.png`/`.jpg` for photographs.

---

## 0. One-time preamble setup

```latex
\usepackage{graphicx}
\graphicspath{{figures/}}   % all \includegraphics names resolve under figures/
```

With this, `\includegraphics{example}` finds `figures/example.pdf` (extension
optional; pdfLaTeX tries `.pdf`, `.png`, `.jpg`).

---

## 1. Single figure

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.6\linewidth]{example.pdf}
  \caption{A single centered figure.}
  \label{fig:single}
\end{figure}
```

Size with `width=` (relative to `\linewidth`), `height=`, or `scale=`. Prefer
`\linewidth` over `\textwidth` so it also works inside a column or `minipage`.

---

## 2. Side-by-side subfigures (`subcaption`)

Preamble:

```latex
\usepackage{graphicx}
\usepackage{caption}
\usepackage{subcaption}
```

Body:

```latex
\begin{figure}[htbp]
  \centering
  \begin{subfigure}[t]{0.48\linewidth}
    \centering
    \includegraphics[width=\linewidth]{example-a.pdf}
    \caption{First panel.}
    \label{fig:sub-a}
  \end{subfigure}
  \hfill
  \begin{subfigure}[t]{0.48\linewidth}
    \centering
    \includegraphics[width=\linewidth]{example-b.pdf}
    \caption{Second panel.}
    \label{fig:sub-b}
  \end{subfigure}
  \caption{Two subfigures; refer to panels as \subref{fig:sub-a}.}
  \label{fig:subfigs}
\end{figure}
```

Reference the whole figure with `\Cref{fig:subfigs}` and a panel with
`\Cref{fig:sub-a}` (cleveref) or `\subref{fig:sub-a}` (just the "(a)").

---

## 3. Full-width figure across both columns (`figure*`)

In a two-column document, `figure*` spans the full page width. It can only be
placed at the top of a page (`[t]`) or on a dedicated float page (`[p]`).

```latex
\begin{figure*}[t]
  \centering
  \includegraphics[width=\linewidth]{wide-example.pdf}
  \caption{A page-wide figure spanning both columns.}
  \label{fig:wide}
\end{figure*}
```

(In a one-column document `figure*` behaves like `figure`.)

---

## 4. Text-wrapped figure (`wrapfig`) --- USE WITH CAUTION

`wrapfig` flows text around a figure. It is **fragile**: it misbehaves next to
list environments, page breaks, and other floats, and can overlap text if the
paragraph is too short. Only reach for it when a normal float genuinely will not
do, and always eyeball the result.

Preamble:

```latex
\usepackage{graphicx}
\usepackage{wrapfig}
```

Body (place it just before the paragraph it should sit beside, not inside a
list, and not straddling a page break):

```latex
\begin{wrapfigure}{r}{0.4\linewidth}  % r = right side; l = left
  \centering
  \includegraphics[width=0.38\linewidth]{example.pdf}
  \caption{A wrapped figure.}
  \label{fig:wrap}
\end{wrapfigure}
Placeholder paragraph text that flows around the figure. Keep this paragraph
long enough to reach past the bottom of the image, otherwise the following text
may collide with it.
```

If layout breaks, switch back to a normal `figure` float --- that is almost
always the right call.

---

## 5. Robust relative paths (portability)

Do:

```latex
\graphicspath{{figures/}}          % trailing slash, relative, in the preamble
\includegraphics[width=0.6\linewidth]{plot}   % no extension, no leading path
```

Avoid:

```latex
\includegraphics{C:/Users/me/project/figures/plot.pdf}  % absolute -> not portable
\includegraphics{../../shared/plot.pdf}                 % brittle across machines
```

Multiple search directories are allowed:

```latex
\graphicspath{{figures/}{figures/generated/}}
```

Notes:

- Use forward slashes `/` in paths even on Windows --- LaTeX accepts them and
  they stay portable.
- Avoid spaces and non-ASCII characters in figure filenames.
- Keep every asset inside the project tree so the whole folder builds anywhere.

---

## Reference in text

```latex
As shown in \Cref{fig:single}, ...     % cleveref -> "Figure 1"
```
