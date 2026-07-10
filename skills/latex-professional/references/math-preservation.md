# Math Preservation

Purpose: reformat equations for style/layout WITHOUT altering meaning. When an agent touches math, semantics are sacred — presentation is negotiable.

## The one rule

**Change how math LOOKS, never what math SAYS.** If a reformat could alter the value, scope, or claim of an expression, don't do it — flag it.

## Hard rules (never do these without an explicit request)

- Never rename a variable, function, operator, or index (`x`→`y`, `\alpha`→`a`, `\sum_i`→`\sum_j`).
- Never change a quantifier (`\forall`↔`\exists`), its order, or its scope.
- Never change a domain / set / bound (`[0,1]`→`(0,1)`, `\in \mathbb{R}`→`\in \mathbb{Z}`, `\sum_{i=1}^{n}`→`\sum_{i=0}^{n}`).
- Never flip an (in)equality or its direction (`=`, `\leq`, `<`, `\geq`, `>`, `\neq`, `\approx`, `\equiv`, `\propto`, `\sim`).
- Never change a sign, exponent, subscript, or coefficient.
- Never alter an assumption, hypothesis, or a theorem's conclusion.
- Never "simplify"/"correct" a formula you think is wrong — the author may mean it. **Flag, don't fix.**
- Never infer an ambiguous or truncated formula — ask.
- Never renumber or drop equation labels that are `\ref`/`\eqref`/`\cref`-ed elsewhere.
- Never change math punctuation that carries meaning (a trailing comma/period is typographic and stays; but `,` inside `f(x,y)` is structural).

What you MAY do freely: whitespace, indentation, wrapping long lines, choosing a better environment (per table below) **that renders identically**, adding `\,`/`\;` thin spaces, aligning at `&`, promoting inline `$...$` to display when the author asks, fixing `$$...$$` → `\[...\]` (see below).

## Environment selection table

| Need | Environment | Notes |
|---|---|---|
| One numbered display equation | `equation` | `\[...\]` for the **unnumbered** variant. Never `$$...$$` (see below). |
| Multi-line, aligned at relations (`=`, `\leq`) | `align` / `align*` | `&` marks the alignment column; `\\` ends a line. One number per line unless `\nonumber`. |
| Multi-line, centered, no alignment | `gather` / `gather*` | Each line centered, own number. |
| One equation broken over lines, ONE number | `split` (inside `equation`) | Aligns at `&`; the whole block gets a single number. |
| Case distinctions | `cases` (inside math) | `\begin{cases} a & x>0 \\ b & x\le 0 \end{cases}` |
| Matrices | `matrix`/`pmatrix`/`bmatrix`/`vmatrix`/`Vmatrix` | `()`, `[]`, single-bar det, double-bar norm respectively. Choose by the delimiter the author intended — **don't swap bracket type**. |
| Aligned system w/o numbers, in text | `aligned` (inside math) | like `align` but nests inside `equation`/inline. |
| Theorem-like | `theorem`/`lemma`/`proposition`/`corollary`/`definition`/`proof` | from `amsthm`; preserve the `\label`, statement, and QED. |

Deprecated / avoid: `eqnarray` (bad spacing — migrate to `align` **only if** you preserve every token and number). `$$...$$` (plain-TeX; breaks spacing/`\tag`) → use `\[...\]` (unnumbered) or `equation` (numbered).

## Label & numbering discipline

- Keep every existing `\label{eq:foo}`; downstream `\eqref{eq:foo}`/`\cref{eq:foo}` depends on it.
- When splitting one `equation` into `align`, decide numbering deliberately: if the original had one number and one label, use `split` (keeps one number) — don't silently create N numbers.
- Suppress a line's number with `\nonumber` or `\notag`, not by deleting `\label`.
- Never reorder numbered equations (shifts every auto-number and reference).

## Good vs bad reformats

### GOOD — pure layout change, identical rendering

```latex
% Before (cramped, plain-TeX delimiters):
$$f(x) = \sum_{i=1}^{n} a_i x^i + \int_0^1 g(t)\,dt$$

% After (proper AMS, numbered, unchanged math):
\begin{equation}
  f(x) = \sum_{i=1}^{n} a_i x^i + \int_0^1 g(t)\,dt
  \label{eq:f-def}
\end{equation}
```

### GOOD — break a long line with `split`, keep ONE number

```latex
\begin{equation}
\begin{split}
  L(\theta) &= \sum_{i=1}^{n} \big( y_i - f(x_i;\theta) \big)^2 \\
            &\quad + \lambda \lVert \theta \rVert_2^2 .
\end{split}
\label{eq:loss}
\end{equation}
```

### BAD — semantic drift disguised as cleanup

```latex
% Original:
\begin{equation}
  \forall \epsilon > 0,\ \exists \delta > 0:\ |x-a| < \delta \Rightarrow |f(x)-f(a)| < \epsilon
\end{equation}

% WRONG "reformat" (changed quantifier order, flipped strict/non-strict,
%   renamed the bound, dropped a condition):
\begin{equation}
  \exists \delta > 0,\ \forall \epsilon \ge 0:\ |x-a| \le d \Rightarrow |f(x)-f(a)| < \epsilon
\end{equation}
```

Every one of `\forall`↔`\exists` swap, `>`→`\ge`, `\delta`→`d`, `<`→`\le` is a forbidden edit. This changes the definition of continuity into something false.

### BAD — "fixing" a formula the author may mean

```latex
% Author wrote (maybe intentional, e.g. a deliberate approximation):
E = mc

% Do NOT silently "correct" to E = mc^2. FLAG it:
%   "eq:energy line 88 reads `E = mc` — missing exponent? confirm intended form."
```

## Ambiguity → ask, never guess

Flag (don't auto-resolve) when:
- OCR/paste garble: `l` vs `1`, `O` vs `0`, missing braces around a subscript (`x_10` vs `x_{10}`).
- A dangling operator or unmatched delimiter (`\left(` with no `\right)`).
- A macro used but not defined in the preamble (could be a custom operator with specific meaning — check `\newcommand`/`\DeclareMathOperator` first).
- Units attached to numbers — preserve exactly; prefer `siunitx` (`\SI{9.8}{m/s^2}`) only if the author already uses it, and never change the numeric value or unit.

## Custom macros & operators

- Before editing, grep the preamble for `\newcommand`, `\renewcommand`, `\DeclareMathOperator`, `\DeclarePairedDelimiter`. A symbol like `\R` or `\argmin` may be author-defined with exact meaning.
- Preserve custom-macro calls verbatim; don't expand them inline (loses intent and breaks consistency).
- `\DeclareMathOperator{\argmin}{arg\,min}` → keep using `\argmin`, don't hand-write `\text{arg min}`.

## Cross-reference hygiene

- Use `\eqref{}` (adds parentheses) or `cleveref`'s `\cref{}` — but only match the document's existing convention; don't mix.
- If you renumber/relabel (only on explicit request), update *every* reference site, then rebuild twice so numbers resolve.

## Agent checklist before saving math edits

1. Diff is whitespace/environment/label-neutral in meaning — no token added, removed, or changed.
2. Every `\label` that existed still exists and is unique.
3. Delimiters balanced (`\left`/`\right`, braces, `$`/`\[`).
4. Rendered output verified (compile) — the equation number count and cross-refs resolve.
5. Any uncertainty was flagged to the user, not silently resolved.
