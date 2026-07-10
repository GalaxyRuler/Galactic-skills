# Equation snippets

Copy-paste LaTeX blocks for common math. All of these need `amsmath`; matrices
also use `amsmath` (no extra package). Theorem scaffolding uses `amsthm`.

Preamble (covers everything below):

```latex
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsthm}   % only for the theorem/proof scaffold
```

Rules of thumb:

- One display equation → `equation`. Never use `$$ ... $$` (plain-TeX; breaks
  spacing).
- Multi-line aligned math → `align`. Unnumbered variants end in `*`.
- Label scheme: `eq:`. Reference with `\Cref{eq:...}` (cleveref) or `\eqref`.

---

## 1. Single numbered equation

```latex
\begin{equation}
  \label{eq:single}
  E = mc^{2}.
\end{equation}
```

Unnumbered: use `equation*` or `\[ ... \]`.

---

## 2. `align` --- multiple equations aligned on `&`

```latex
\begin{align}
  a &= b + c,        \label{eq:align-a} \\
  x &= y + z + w.    \label{eq:align-b}
\end{align}
```

Suppress the number on one line with `\nonumber` (or `\notag`):

```latex
\begin{align}
  f(x) &= (x+1)^2 \nonumber \\
       &= x^2 + 2x + 1. \label{eq:expand}
\end{align}
```

---

## 3. `split` --- one number for a broken single equation

`split` must sit **inside** `equation`; the whole thing gets one number.

```latex
\begin{equation}
  \label{eq:split}
  \begin{split}
    (a+b)^2 &= a^2 + 2ab + b^2 \\
            &= a^2 + b^2 + 2ab.
  \end{split}
\end{equation}
```

---

## 4. `gather` --- several centered equations, each numbered, no alignment

```latex
\begin{gather}
  a^2 + b^2 = c^2, \label{eq:gather-1} \\
  e^{i\pi} + 1 = 0. \label{eq:gather-2}
\end{gather}
```

---

## 5. `cases` --- piecewise definitions

```latex
\begin{equation}
  \label{eq:cases}
  \operatorname{sgn}(x) =
  \begin{cases}
    -1 & \text{if } x < 0, \\
     0 & \text{if } x = 0, \\
     1 & \text{if } x > 0.
  \end{cases}
\end{equation}
```

---

## 6. Matrices --- `pmatrix`, `bmatrix`, `vmatrix`

```latex
\begin{equation}
  \label{eq:matrices}
  A =
  \begin{pmatrix}       % round brackets ( )
    a & b \\
    c & d
  \end{pmatrix},
  \qquad
  B =
  \begin{bmatrix}       % square brackets [ ]
    1 & 0 \\
    0 & 1
  \end{bmatrix},
  \qquad
  \det A =
  \begin{vmatrix}       % vertical bars | |  (a determinant)
    a & b \\
    c & d
  \end{vmatrix}.
\end{equation}
```

Also available: `matrix` (no delimiters), `Bmatrix` `{ }`, `Vmatrix` `‖ ‖`.
For inline-sized matrices use the `smallmatrix` environment.

---

## 7. Theorem / proof scaffold (`amsthm`)

Put the theorem-style declarations in the **preamble**:

```latex
\usepackage{amsthm}
\theoremstyle{plain}      % bold header, italic body
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\theoremstyle{definition} % bold header, upright body
\newtheorem{definition}{Definition}
\theoremstyle{remark}
\newtheorem*{remark}{Remark}   % starred = unnumbered
```

Use them in the body:

```latex
\begin{definition}[Placeholder]
  \label{def:placeholder}
  A placeholder definition.
\end{definition}

\begin{theorem}[Placeholder]
  \label{thm:placeholder}
  A placeholder statement.
\end{theorem}

\begin{proof}
  Placeholder argument. \qedhere
\end{proof}
```

Reference with `\Cref{thm:placeholder}` → "Theorem 1".

---

## Common inline constructs

```latex
% Fractions, sub/superscripts
$\frac{a}{b}$, $x_i^2$, $\sqrt[3]{x}$

% Sum / integral with limits
$\sum_{i=1}^{n} i$, $\int_0^1 f(x)\,\mathrm{d}x$

% Well-spaced operators and text in math
$f\colon X \to Y$, $\quad \text{for all } x \in X$

% Bold vectors / blackboard sets (amssymb)
$\mathbf{v}$, $\mathbb{R}^n$
```
