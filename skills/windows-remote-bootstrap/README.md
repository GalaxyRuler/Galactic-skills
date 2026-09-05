# Windows Remote Bootstrap

Remote Windows work fails at handoff boundaries — wrong directory, stale payload, nested quotes stripped by an intermediate shell, missing PATH entries, orphaned child processes, or silent success with no proof. This makes every step absolute-path, failure-loud, and independently verifiable.

## What it does

- Stages payloads in a fixed run root and proves freshness by filename, size, timestamp, and SHA-256 before running anything
- Invokes transferred scripts by absolute `-File` path — and explains when to use `& script.ps1 -Credential $cred` instead, because a native process boundary stringifies a `[pscredential]` into a false auth failure
- Covers SSH-to-Windows quoting: the remote shell may be `cmd.exe` and strip nested quotes; command lines hit "too long" before the script logic runs; `$()` gets eaten by the local shell
- Lists Windows PowerShell 5.1 portability traps: `$ErrorActionPreference`, `@($value)` for empty arrays, `ConvertTo-Json` on rich objects, missing `ProcessStartInfo.ArgumentList`, `.cmd` launch via `cmd.exe /d /c call`, `Get-Content -Raw` returning `$null`, unsigned P/Invoke constants
- Separates SSH reach from the foreground desktop — with an interactive-token scheduled-task lane (`schtasks /IT`) and hard assertions that the desktop is real: nonzero `GetForegroundWindow()`, foreground PID not `LogonUI`/`LockApp`, non-blank screenshot
- Refuses to disable UAC as a workaround, and keeps Windows passwords off the controller machine, out of prompts, repos, task specs, and logs
- Gives a VM app-acceptance pattern: fresh VM-local workspace, loopback-only binding on a task-owned port, stale-listener cleanup, wrapper PID vs actual listener PID, Playwright browser fallback order, reversible edit-and-revert verification
- Ends with a verification checklist and a common-pitfalls list (running from `System32`, reusing a stale payload, reporting "started" before verifying remote state)

## When to use

Preparing, transferring, running, or troubleshooting Windows bootstrap or acceptance scripts over SSH, WinRM, Taildrop, scheduled tasks, or VM consoles. Also when a remote Windows run fails on stale files, quoting, PATH, ports, process cleanup, or missing evidence — or when a GUI-dependent test needs a real interactive desktop rather than an SSH session.

## What's inside

- [SKILL.md](SKILL.md) — standard workflow, SSH-to-Windows rules, PowerShell portability traps, interactive-desktop lane, VM app acceptance pattern, verification checklist, common pitfalls
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/windows-remote-bootstrap ~/.claude/skills/`
**Codex:** `cp -r skills/windows-remote-bootstrap $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\windows-remote-bootstrap "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse skills\windows-remote-bootstrap "$env:USERPROFILE\.codex\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
