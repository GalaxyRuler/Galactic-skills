# LaTeX Compile-Error Playbook

Purpose: map a log symptom to its likely root cause and the safest minimal fix, so an agent repairs the *first* real error instead of chasing cascades.

## Golden rules

- **Find the FIRST meaningful error, not the last.** LaTeX keeps going after an error; later messages are usually cascade noise. Fix the earliest `!` line, recompile, re-read.
- **One fix per compile.** Change the single most-likely cause, rebuild, re-read the log. Do not batch speculative edits.
- **Never rewrite globally to silence an error.** A local, targeted patch is almost always correct. Global search/replace masks the cause and creates new ones.
- **Prefer `latexmk`** — it re-runs LaTeX/bib/index/rerun until stable, so "Rerun to get cross-references right" resolves itself. Read the `.log`, not just terminal output.
- **Use the helper first:** `python scripts/parse-latex-log.py <main>.log` prints the `first_fatal_candidate` (kind + log line) and a finding count. Add `--json` for structured triage. Anchor your diagnosis on that line.

## Triage flow

```
1. Run: python scripts/parse-latex-log.py main.log
2. Jump to first_fatal_candidate line in main.log.
3. Read 3 lines above + the "l.NNN" line it points to → that source line is the cause.
4. Match the "! ..." string to the table below.
5. Apply the minimal fix. Recompile. Re-parse. Repeat until clean.
```

The `l.NNN` marker in the log is the **source line where TeX choked** (often the token right before the break). The `<recently read>` / `<argument>` fragments show the exact token.

## Symptom → cause → fix table

### `! Undefined control sequence`

- **Log looks like:** `! Undefined control sequence.` then `l.42 \includegrpahics`
- **Causes:** typo in a macro name; a package that defines the command isn't loaded; command defined later / in wrong scope; using a XeLaTeX/LuaLaTeX-only macro under pdfLaTeX.
- **Confirm:** the `l.NNN` line shows the offending `\command`. Grep for its correct spelling; check whether the providing package is in the preamble.
- **Minimal fix:** correct the spelling, OR add the missing `\usepackage{...}` (e.g. `\includegraphics`→`graphicx`, `\SI`/`\num`→`siunitx`, `\cref`→`cleveref`, `\toprule`→`booktabs`, `\text`→`amsmath`).
- **Do NOT:** define a fake stub macro to suppress it; that hides a missing package and produces wrong output.

### `! LaTeX Error: File \`xxx.sty' not found` / `File not found`

- **Log looks like:** `! LaTeX Error: File \`tikz.sty' not found.` or `! LaTeX Error: File \`fig1.pdf' not found.`
- **Causes:** package not installed in this TeX distribution; graphics/input file path wrong or case-mismatched (Linux/arXiv are case-sensitive); missing file extension the engine can't guess.
- **Confirm:** for `.sty`/`.cls`, run `kpsewhich xxx.sty` (empty = not installed). For assets, `ls` the path relative to the main file.
- **Minimal fix:** install via `tlmgr install <pkg>`; or fix the relative path / filename case; or add the extension. For a missing class, check spelling of `\documentclass{...}`.
- **Do NOT:** hard-code an absolute path (breaks on arXiv/other machines) or comment out the `\usepackage` if the package is actually used.

### `! LaTeX Error: Option clash for package xxx`

- **Log looks like:** `! LaTeX Error: Option clash for package graphicx.` with `The package ... has already been loaded with options: [...]`
- **Causes:** same package loaded twice with different options — often once explicitly and once implicitly by another package (e.g. `graphicx` pulled in by `tikz`; `xcolor` by `pstricks`).
- **Confirm:** search the preamble for two `\usepackage[...]{xxx}` lines, or a `\documentclass` option that a package re-requests.
- **Minimal fix:** load the package **once**, earliest, with the union of needed options; or move the option to `\PassOptionsToPackage{opt}{xxx}` **before** `\documentclass`. Remove the duplicate `\usepackage`.
- **Do NOT:** delete both loads. Consolidate; don't drop a needed option.

### `! Missing } inserted` / `! Extra }, or forgotten \endgroup`

- **Log looks like:** `! Missing } inserted.` or `! Extra }, or forgotten \endgroup.`
- **Causes:** unbalanced braces; a `{` opened in one macro argument and never closed; `\begin{env}` without `\end{env}`; a `$`/`\]` math delimiter mismatch throwing off brace parsing.
- **Confirm:** the `l.NNN` is where TeX *noticed* the imbalance, not always where it started. Check the enclosing environment/macro from that line upward for the unmatched brace.
- **Minimal fix:** add or remove the single offending brace at the true site. Verify with an editor's brace-match.
- **Do NOT:** sprinkle extra `}` until it compiles — that shifts the imbalance and corrupts structure.

### `! Paragraph ended before \xxx was complete` / `Runaway argument?`

- **Log looks like:** `Runaway argument?` followed by echoed text, then `! Paragraph ended before \foo was complete.`
- **Causes:** a blank line (paragraph break) inside the argument of a command that doesn't allow `\par` (many fragile/non-`\long` macros, or a `{`/`}` that was never closed so the argument "runs away").
- **Confirm:** the echoed runaway text shows how far TeX scanned. The missing `}` is usually just before the first blank line in that block.
- **Minimal fix:** close the unbalanced brace, or remove the blank line inside the argument, or make the macro `\long` if it legitimately spans paragraphs.
- **Do NOT:** delete the whole block; you'll lose content.

### `! Emergency stop` / `==> Fatal error occurred`

- **Log looks like:** `! Emergency stop.` then `*** (job aborted, no legal \end found)` or `(cannot \read from terminal in nonstop mode)`.
- **Causes:** a preceding error left TeX unable to continue (e.g. `\begin{document}` never found, missing `\end{document}`, a `\input` file that doesn't exist, or TeX prompting for input in batch mode).
- **Confirm:** scroll **up** — Emergency stop is a *consequence*. The real error is the earlier `!` line. If none, a structural file is missing/truncated.
- **Minimal fix:** repair the earlier error; ensure `\end{document}` exists; ensure every `\input`/`\include` target exists.
- **Do NOT:** treat Emergency stop itself as the bug. It never is.

### `! Package inputenc Error: Unicode character X not set up` / `LaTeX Error: Unicode character`

- **Log looks like:** `! Package inputenc Error: Unicode character ... (U+2014) not set up for use with LaTeX.`
- **Causes:** a real Unicode char (em-dash, curly quote, non-ASCII letter, math symbol) in the source under **pdfLaTeX** without a mapping; frequently an **engine mismatch** — the source expects XeLaTeX/LuaLaTeX.
- **Confirm:** the char code (U+xxxx) is in the message; find it on the `l.NNN` line. Decide: is this a document meant for a Unicode engine?
- **Minimal fix (pdfLaTeX):** add `\usepackage[utf8]{inputenc}` (default since 2018, so if already present the char needs a package: `textcomp`, `amssymb`, or a `\DeclareUnicodeCharacter`), or replace the literal with its LaTeX command. **Better fix if the doc is Unicode-heavy:** switch the engine to XeLaTeX/LuaLaTeX (+`fontspec`) — see `package-compatibility.md`.
- **Do NOT:** strip non-ASCII characters blindly (mangles names, math, other languages).

### `LaTeX Warning: Citation \`key' on page N undefined` / `Reference \`x' undefined`

- **Log looks like:** `LaTeX Warning: Citation \`smith2020' on page 3 undefined on input line 55.` or `LaTeX Warning: There were undefined references.`
- **Causes:** bibliography step hasn't run yet (needs another pass); wrong/missing citation key; `.bbl`/`.aux` stale; label typo for `\ref`.
- **Confirm:** does `.bbl` exist and contain the key? Did `bibtex`/`biber` actually run (check its own log)? Is the key spelled the same in `.bib` and `\cite`?
- **Minimal fix:** run the full sequence (`latexmk` does this automatically); fix key/label typos; ensure the `.bib` entry exists. See `bibliography-backends.md`.
- **Do NOT:** invent a bib entry to satisfy a citation — **flag the missing key** to the user instead.

### `I couldn't open database file xxx.bib` (BibTeX)

- **Log looks like:** (in `.blg`, BibTeX's log) `I couldn't open database file references.bib` / `---line N of file main.aux`.
- **Causes:** `\bibliography{references}` names a file that isn't in the search path; wrong name/extension (`\bibliography` takes the name **without** `.bib`); file in a subdir not on `BIBINPUTS`.
- **Confirm:** `ls` for the `.bib`; check the exact name in `\bibliography{...}`; open the `.blg` file (not the `.log`).
- **Minimal fix:** correct the filename in `\bibliography{...}` (no `.bib` extension), or put the `.bib` beside the main file / add its dir. For BibLaTeX use `\addbibresource{references.bib}` (**with** extension).
- **Do NOT:** create an empty `.bib` to silence it if the real file exists under a different name.

### `! Package biblatex Error: ...`

- **Log looks like:** `! Package biblatex Error: Incompatible package 'natbib'.` or `Package biblatex Warning: Please (re)run Biber on the file`.
- **Causes:** mixing `natbib`/`bibtex` with `biblatex`; ran `bibtex` when backend is `biber`; stale `.bbl` from the wrong backend; missing `\addbibresource`.
- **Confirm:** check for `\usepackage{biblatex}` **and** `\bibliography`/`\bibliographystyle` (illegal mix). Check whether `biber main` ran vs `bibtex main`.
- **Minimal fix:** pick one system. With `biblatex`: use `\addbibresource{...}` + `\printbibliography`, run **biber** (delete the old `.bbl` first). Never feed a BibTeX-produced `.bbl` to a Biber project or vice-versa. See `bibliography-backends.md`.
- **Do NOT:** run `bibtex` and `biber` on the same job, or leave a mismatched `.bbl` in place.

### `Overfull \hbox (…pt too wide)` / `Underfull \hbox (badness …)`

- **These are WARNINGS, not errors.** The PDF still builds. Do not "fix" them under time pressure or in a submission rush; they rarely block anything.
- **Log looks like:** `Overfull \hbox (15.3pt too wide) in paragraph at lines 88--90`.
- **Causes:** unbreakable long word/URL/inline-math/`\verb`; a `tabular`/image wider than `\textwidth`; disabled hyphenation.
- **Confirm:** go to the cited line range; look for a long token, wide table, or oversized graphic.
- **Minimal fix (only if it visibly overruns the margin):** `\usepackage{microtype}`; wrap URLs with `url`/`\sloppy`; resize the table/figure; add discretionary hyphens. Threshold-tune with `\hfuzz=2pt` only cosmetically.
- **Do NOT:** treat these as build failures or block a submission on them.

## Engine mismatch (meta-symptom)

Symptoms that all point at "wrong engine, not wrong source":

| Symptom | Meaning | Fix |
|---|---|---|
| `Unicode character ... not set up` en masse | source is Unicode-native | compile with XeLaTeX or LuaLaTeX |
| `! Undefined control sequence \setmainfont` | `fontspec` under pdfLaTeX | switch to Xe/Lua, or drop `fontspec` |
| `! Package fontspec Error: The fontspec package requires either XeTeX or LuaTeX` | same | switch engine |
| `inputenc`/`fontenc` errors under Xe/Lua | inputenc loaded with a Unicode engine | remove `inputenc`/`fontenc`, use `fontspec` |

Respect `% !TEX program = ...` magic comments and any `latexmkrc`/`00README.json` compiler declaration — they tell you the intended engine. See `main-file-discovery.md`.

## What proves it's fixed

- `parse-latex-log.py` reports **no** `first_fatal_candidate`.
- The PDF regenerates and page/label count is sane.
- No new earlier `!` line appeared (a fix can surface a previously-masked error — re-parse every time).
