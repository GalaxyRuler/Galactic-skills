---
name: powershell-safe-vars
description: Use when writing or editing PowerShell commands or scripts, especially when variable names, shell quoting, heredocs, or path/string interpolation may fail, or when writing command blocks for the user to run manually on Windows.
---

# PowerShell: Safe Variables, Quoting, and One-Liners

## When to use

Use this when writing or editing PowerShell (`pwsh`) commands/scripts inside Codex tool calls, especially for automations and one-liner scripts.

## Problems this prevents

PowerShell has **automatic variables** (some are read-only / constant), and variable names are **case-insensitive**. Accidentally assigning to one of these (e.g. `$HOME`, `$Host`) can cause a script to fail with errors like “Cannot overwrite variable … because it is read-only or constant.”

PowerShell also parses quoting, pipes, redirection, and command substitution differently than Bash. Copying Bash snippets directly can produce `ParserError`, `Missing file specification after redirection operator`, `The term 'from' is not recognized`, or `An empty pipe element is not allowed`.

## Workflow

1) Pick “safe” variable names
- Prefer descriptive names like `$userHome`, `$codexHome`, `$installRoot`, `$sessionDir`.
- Avoid short/common names that collide with automatic variables, including:
  - `$HOME` (often constant) → use `$userHome`
  - `$Host` (automatic variable) → use `$hostInfo` / `$hostProc`
  - `$PID`, `$PSVersionTable`, `$Error`, `$Matches`, `$Profile`, `$PSScriptRoot`, `$PSCommandPath`
- Remember: `$home` and `$HOME` are the *same* variable.

2) If you must reuse a risky name, change it immediately
- Rename the local variable to a safe name and update all references.

3) Keep “tool-call scripts” failure-loud
- Start scripts with: `$ErrorActionPreference='Stop'`
- Set timeouts explicitly in the tool call (e.g. `timeout_ms`) for long operations.

4) Avoid string-interpolation parsing traps
- If a variable is immediately followed by `:`, PowerShell can treat it like a scoped variable reference and throw: “Variable reference is not valid. ':' was not followed by a valid variable name character.”
- Fix by using one of:
  - `"${var}:suffix"` (brace the variable)
  - `("{0}:{1}" -f $var, $suffix)` (format operator)

5) Treat optional env vars as optional
- Some environments won’t set expected variables like `$env:CODEX_HOME`.
- Prefer defensive fallbacks, e.g.:
  - `$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }`

6) Guard method calls on optional strings and process state
- `Get-Content -Raw` can return `$null` for an empty file or missing optional output path, so calling `.Trim()`, `.Substring()`, `.Length`, or regex methods directly can fail with "You cannot call a method on a null-valued expression."
- Coerce optional text to `[string]` before string methods:

```powershell
$stdoutText = if (Test-Path -LiteralPath $outPath) { [string](Get-Content -Raw -LiteralPath $outPath) } else { '' }
$stderrText = if (Test-Path -LiteralPath $errPath) { [string](Get-Content -Raw -LiteralPath $errPath) } else { '' }
$cleanStdout = $stdoutText.Trim()
```

- Do not read `$process.ExitCode` until the process has exited; prefer direct invocation plus `$LASTEXITCODE` when no timeout is needed, or wait with `WaitForExit()` and precompute `$exitCode` before building result objects.
- Compute possibly-null fields before `[ordered]@{}` or `[pscustomobject]@{}` literals so failures are isolated and easier to diagnose.
- Do not pass live PowerShell objects such as `[pscredential]` through a nested native `powershell.exe -File ...` call. Invoke the script in the current session with `& .\script.ps1 -Credential $cred`; otherwise the object is stringified and downstream authentication may fail even when the password is correct.

7) Avoid `$PSScriptRoot` in parameter default expressions
- In Windows PowerShell and some invocation styles, `$PSScriptRoot` can be empty while parameter default values are being evaluated, causing `Join-Path $PSScriptRoot ...` to fail.
- Prefer computing defaults after `param()` runs, e.g.:
  - `if (!$ConfigPath) { $ConfigPath = Join-Path $PSScriptRoot 'runner-config.json' }`
  - Or pass `-ConfigPath` explicitly from the caller.

8) Do not paste Bash heredocs into PowerShell
- Bad in PowerShell: `python - <<'PY'`
- Use a PowerShell here-string piped to the command:

```powershell
@'
print("hello")
'@ | python -
```
- Here-string headers and terminators must each be alone on their own line. Do not write `@'{"json":true}` on one line.

9) Quote native-command regexes and globs PowerShell-first
- Prefer single quotes for regex/search arguments that contain `"`, `|`, `$`, `--`, `[`, `]`, `*`, `?`, or backslashes.
- Also single-quote native glob flags such as `rg -g '*.ts'`; otherwise PowerShell can parse `[` as indexing or `*` as multiplication before the native command receives it.
- Backslash does not escape a double quote in PowerShell. Use single quotes, or escape PowerShell double quotes with a backtick.
- If a native command argument keeps being parsed by PowerShell, reduce the expression, single-quote it, or pass the pattern from a variable.
- For `rg`, remember the default regex engine does not support look-around or backreferences. Use `--pcre2` only when those constructs are required; otherwise simplify the pattern, split it into multiple searches, or use `-F` for literal terms.

10) Compute conditionals before interpolation
- Do not use Bash-style `$((...))` in strings for command substitution or conditionals.
- Prefer a separate variable:

```powershell
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
"CodexHome=$codexHome"
```

11) Compute conditionals before object literals
- PowerShell `if` is a statement, not an expression. Do not put `if (...) { ... }` directly inside `[pscustomobject]@{}` values.
- Prefer precomputed variables:

```powershell
$childCount = if (Test-Path -LiteralPath $repoRaw) { (Get-ChildItem -LiteralPath $repoRaw).Count } else { 0 }
[pscustomobject]@{ Path = $repoRaw; ChildCount = $childCount }
```

12) Pipe control-flow output safely
- Do not pipe directly after a closing brace from `foreach`, `if`, or similar control-flow statements in one-liners.
- Capture rows first, then pipe the variable:

```powershell
$rows = foreach ($item in $items) { [pscustomobject]@{ Name = $item.Name } }
$rows | Format-Table -AutoSize
```

13) Commands handed to the user must be complete copy-paste units
- Any command block the user will run manually must work from a fresh terminal: include the `cd` to the correct working directory, required env vars, and the command — in one block, every time.
- Never give a bare snippet that assumes the current directory or session env (e.g. `uv run python -m scripts.X` fails with `ModuleNotFoundError` outside the repo root; scripts printing Unicode need `$env:PYTHONIOENCODING = "utf-8"` first).

```powershell
cd C:\path\to\repo
$env:PYTHONIOENCODING = "utf-8"
uv run python -m scripts.run_thing --flag
```

14) Windows shell gotchas when writing commands for the user
- `&&` and `||` work only in PowerShell 7+; Windows PowerShell 5.1 rejects them. Use `;` or separate lines unless pwsh 7 is confirmed — but note `;` does not short-circuit: gate with `if ($?) { ... }` or check `$LASTEXITCODE` when the second command must not run after a failure.
- `%VAR%` does not expand in PowerShell — use `$env:VAR`.
- Inline env-var prefixes (`NODE_ENV=production cmd`) are Bash-only — set `$env:NODE_ENV = 'production'` on its own line first.
- Machine-scope `[Environment]::SetEnvironmentVariable(..., 'Machine')` and registry writes under HKLM need an elevated shell — say so, or use `'User'` scope.
- Use `git <cmd> -h` for quick help; `git help <cmd>` tries to open a browser/man page on Windows.

15) Avoid empty or accidental parameters when forwarding arguments
- When a wrapper script forwards arrays to another command, remove empty strings and validate the final argv before invoking the child process.
- PowerShell can interpret an empty or malformed forwarded parameter as an ambiguous parameter name, e.g. `Parameter name '' is ambiguous`.
- Prefer explicit arrays and filter them:

```powershell
$cargoArgs = @($cargoArgs | Where-Object { -not [string]::IsNullOrWhiteSpace([string]$_) })
& $cargoExe @cargoArgs
```

## Verification checklist

- Script runs without `WriteError` / “Cannot overwrite variable …”.
- No assignments to automatic variables (scan for `=$` patterns on `$HOME`, `$Host`, etc.).
- Variables used for paths are built from `$env:USERPROFILE` / `$env:LOCALAPPDATA` as needed, with safe defaults when env vars are missing.
- No Bash heredoc/redirection syntax like `<<'PY'` remains in PowerShell commands.
- Optional file, command, or process output is coerced to `[string]` before string methods like `.Trim()`.
- External-process exit code fields are precomputed before object literals.
- Here-string headers and terminators are on their own lines.
- Regex/search/glob args containing pipes, embedded quotes, character classes, or wildcards are single-quoted, variable-backed, or PowerShell-escaped.
- `rg` patterns that use look-around or backreferences are either run with `--pcre2` or rewritten for the default engine.
- Forwarded argument arrays are checked for empty strings before being splatted into child commands.
- Complex conditionals are computed before interpolation or object literals.
- `foreach`/`if` statement output is assigned to a variable before piping.
- Command blocks written for the user include `cd` + env vars + command as one copy-paste unit.
- No `%VAR%` or inline `VAR=x cmd` prefixes in any PowerShell command; no `&&`/`||` unless pwsh 7+ is confirmed.

## Common failure modes

- Using `$home = ...` or `$host = ...` in a script (case-insensitive collision).
- Copy/pasting variable names from other shells (Bash `$HOME`) without adjusting for PowerShell semantics.
- Building strings like `"$path:$line"` without bracing (use `"${path}:$line"` or `-f`).
- Using `Join-Path $PSScriptRoot ...` inside a parameter default value (move it into the function/script body).
- Running `python - <<'PY'` or similar Bash heredocs in PowerShell; use a here-string piped to the command.
- Putting JSON or code on the same line as a here-string header (`@'` or `@"`).
- Calling `.Trim()`, `.Length`, `.Substring()`, or similar methods on optional `Get-Content -Raw` output without coercing it to `[string]` first.
- Reading `$process.ExitCode` before a launched process has exited, or embedding that read directly inside a result-object literal.
- Writing regex arguments with `\"` inside PowerShell double-quoted strings; use single quotes or backtick-escaped quotes.
- Running commands like `rg -n "foo[0-9]" . -g "*.ts"` and letting PowerShell parse `[` or `*`; use `rg -n 'foo[0-9]' . -g '*.ts'`.
- Writing `rg` patterns with look-ahead/look-behind and forgetting `--pcre2`.
- Passing empty strings through wrapper argument arrays and triggering ambiguous parameter errors.
- Embedding Bash-style `$((if ...))` in strings; compute the value first.
- Embedding `if (...) { ... }` directly inside a `[pscustomobject]@{}` value; compute the value first.
- Piping directly from `foreach (...) { ... } | Format-Table`; assign the rows first.
- Handing the user a module-relative command without the `cd` to the repo root, causing `ModuleNotFoundError` or path failures.
- Using `&&` in a command the user pastes into Windows PowerShell 5.1.
- Setting machine-scope env vars or HKLM keys from a non-elevated shell and getting access-denied errors.
