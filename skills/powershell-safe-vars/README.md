# PowerShell Safe Vars

A catalog of PowerShell footguns that break AI-agent tool calls and one-liners — automatic-variable collisions, quoting/heredoc traps, and null-handling bugs — each with the safe pattern to use instead.

## What it does

- Flags **automatic-variable collisions**: assigning to `$HOME`, `$Host`, `$PID`, `$Error`, `$Matches`, `$Profile`, `$PSScriptRoot`, etc. (PowerShell variable names are case-insensitive, so `$home` and `$HOME` are the same variable)
- Fixes **string-interpolation traps**: `"$var:suffix"` gets misparsed as a scope reference — brace it (`"${var}:suffix"`) or use `-f`
- Stops **Bash-habit mistakes**: heredocs (`<<'PY'`) don't exist in PowerShell — use a here-string piped to the command instead
- Guards **null-handling**: `Get-Content -Raw` can return `$null`, so `.Trim()`/`.Substring()` on it throws — coerce to `[string]` first
- Covers **native-command quoting**: single-quote regex/glob args containing `"`, `|`, `$`, `[`, `]`, `*`, or `?` so PowerShell's parser doesn't intercept them first
- Covers **`$PSScriptRoot` in parameter defaults**, **process exit-code timing**, **conditionals inside object literals**, and **piping directly off `foreach`/`if`** — each with the safe rewrite
- Ends with a verification checklist and a "common failure modes" table for fast self-review before running a script

## When to use

Writing or editing PowerShell commands or scripts — especially variable naming, shell quoting, heredocs, or path/string interpolation that might fail silently or throw a `ParserError`.

## What's inside

- [SKILL.md](SKILL.md) — the full pattern catalog: 12 numbered workflow rules, verification checklist, common failure modes

## Install

**Claude Code:** `cp -r skills/powershell-safe-vars ~/.claude/skills/`
**Codex:** `cp -r skills/powershell-safe-vars $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\powershell-safe-vars "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse skills\powershell-safe-vars "$env:USERPROFILE\.codex\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
