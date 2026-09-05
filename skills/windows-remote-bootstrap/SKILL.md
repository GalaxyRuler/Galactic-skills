---
name: windows-remote-bootstrap
description: Use when preparing, transferring, running, or troubleshooting Windows bootstrap or acceptance scripts over SSH, WinRM, Taildrop, scheduled tasks, or VM consoles — remote Windows machines, Windows VMs, copied PowerShell payloads, agent VM lanes, or failures involving stale files, quoting, PATH, ports, process cleanup, or missing evidence.
---

# Windows Remote Bootstrap

## Purpose

Remote Windows work fails most often at handoff boundaries: wrong directory, stale payload, hidden prompt, nested quote stripping, missing PATH entries, orphaned child processes, blocked elevation, or silent success without proof. Make every step absolute-path, failure-loud, and independently verifiable.

## Standard Workflow

1. Confirm the intended target before staging. If your environment documents its canonical VM and physical-runner targets, lane gates, and fail-closed states (a runner-registry skill, an `AGENTS.md` block, or a runner manifest), read that first and treat it as authoritative.
2. Stage payloads in a fixed directory such as `C:\AgentInstallers\<task>\<stamp>` or `C:\CodexRunner\bootstrap`.
3. Transfer, then prove freshness with filename, size, timestamp, and preferably SHA-256.
4. Invoke transferred `.ps1` files with an absolute `-File` path:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File C:\path\payload.ps1
   ```
   If the script parameter is a live PowerShell object such as `[pscredential]`, invoke the script in the current PowerShell session with `& C:\path\payload.ps1 -Credential $cred` instead of launching a nested `powershell.exe -File`; native process boundaries stringify objects and can cause false authentication failures.
5. Put complex remote logic in the payload, not in an inline SSH `-Command` string.
6. Print a final status line and write JSON/log artifacts under a known run root.
7. Make reruns idempotent, or explicitly remove only a verified task-owned workspace.

## SSH To Windows

- Assume the remote SSH shell may be `cmd.exe` or another shell that strips nested quotes before PowerShell sees them.
- Prefer `scp payload.ps1` plus `powershell -File C:\absolute\payload.ps1`.
- Stage large or complex payloads as files. Windows SSH command lines can fail with `The command line is too long` long before the script logic runs.
- If inline execution is unavoidable, run a tiny quoting probe first that prints received arguments exactly.
- Avoid PowerShell `$()` syntax in remote one-liners unless it is protected from local-shell expansion.
- For long runs, write timestamped step logs before and after external commands so hangs identify the boundary.

## Windows PowerShell Portability

- Start scripts with `$ErrorActionPreference = "Stop"` and set `$PSNativeCommandUseErrorActionPreference = $false` when native stderr is diagnostic, not fatal.
- Preserve empty arrays with `@($value)` when "none" is valid.
- Normalize rich objects into ordered hashtables before `ConvertTo-Json`.
- Prefer full paths or `Get-Command` checks for tools such as `git`, `node`, `npm.cmd`, `icacls.exe`, and `schtasks.exe`.
- Do not rely on `ProcessStartInfo.ArgumentList`; Windows PowerShell 5.1 lacks it.
- For `.cmd` and `.bat`, launch through `cmd.exe /d /c call "<script.cmd>" ...` or a similarly tested command string.
- Coerce optional file contents to strings before calling string methods. For example, `Get-Content -Raw` can yield `$null`; do not call `.Trim()` or `.Substring()` until you have normalized `$null` to `""`.
- When using P/Invoke from PowerShell, be explicit about unsigned integer constants. For example, `SetThreadExecutionState` keep-awake flags should be passed as a known `[uint32]` value instead of relying on signed `0x80000000` arithmetic.

## Interactive Desktop From SSH

SSH reaches the machine, not the logged-on foreground desktop. Use an interactive desktop lane when a test depends on foreground windows, toasts, screenshots, keyboard, mouse, or secure-desktop state.

Pattern:

1. Prove ordinary SSH readiness first.
2. Stage the GUI payload as a `.ps1` file under a task-owned run root such as `C:\AgentArtifacts\<task>\<stamp>`.
3. Create an interactive-token scheduled task for the logged-on user with `/IT`; run it; wait for a machine-readable JSON result file.
4. Assert the interactive desktop is usable before product QA:
   - `GetForegroundWindow()` returns a nonzero handle.
   - foreground PID is nonzero and not `LogonUI` or `LockApp`.
   - screenshot capture succeeds and produces a non-empty, non-blank image.
5. Copy evidence back with `scp` and validate the copied files.

Do not treat a successful SSH command as proof that the foreground desktop is usable. A locked or secure desktop can produce `GetForegroundWindow = 0`, blank or failed screenshots, and false infrastructure blocks.

Do not disable UAC to solve this. A legitimate admin-owned or user-owned scheduled task is acceptable; bypassing UAC is not. SSH cannot unlock the Windows secure desktop. If the target is logged out or locked, require a human unlock once, then use no-sleep/keep-awake settings only within the operator-approved QA mode.

Exception for a dedicated physical runner (`<your-runner-host>`) with a permanent interactive desktop: its lane, gates, and any auto-logon policy belong to that host's own runner registry — read it there rather than reinventing the policy per task. Never ask for, echo, store, or transmit the Windows password through the controller machine, prompts, repos, task specs, or logs.

## VM App Acceptance Pattern

For VM-based app acceptance, especially launch-and-restart acceptance tests:

- Resolve the canonical VM target, readiness gate, and fail-closed states from your runner registry first; proceed only when that gate reports `Ready`.
- Expand source into a fresh VM-local workspace under `C:\AgentWork\...`; do not run from synced host paths.
- Bind app servers to `127.0.0.1` only and choose a task-owned port.
- Clear stale listeners before first start and before restart.
- Capture both wrapper PID and actual listener PID. Stopping `cmd.exe`, `npm`, or `bun` may leave the child Node/Vite process alive.
- Stop process trees plus any process listening on the task port; verify the port closes after cleanup.
- Use browser fallback in this order when Playwright bundled browsers are missing: bundled Chromium, Edge channel, Chrome channel.
- For reversible visible edits, write UTF-8 without BOM, capture `git diff`, restart through the lifecycle command, assert the new value in a browser, then revert with Git and verify the marker is gone.
- Store evidence in the run root: setup JSON, app stdout/stderr, browser JSON, screenshots, Git diff, summary JSON, and command records.

## Verification Checklist

- Remote script path, run root, account, hostname, and PowerShell version are recorded.
- Target directory listing or hash proves the expected payload ran.
- The script prints final `PASS` or `FAIL` and writes machine-readable JSON.
- Required tools are resolved explicitly.
- App ports are closed after cleanup.
- Evidence paths in any matrix resolve from the declared run root.
- No secrets, auth tokens, credentials, private keys, or host profile data are printed or copied.

## Common Pitfalls

- Running from `C:\Windows\System32` and assuming `.\script.ps1` points to the transferred file.
- Reusing an old staged payload after a local patch.
- Reporting "sent" or "started" before verifying remote state.
- Treating an empty array as missing configuration after PowerShell collapses it to `$null`.
- Letting `ConvertTo-Json` serialize rich PowerShell objects instead of a small plain object graph.
- Assuming the wrapper PID is the app server PID.
- Marking VM acceptance pass without objective run-root evidence.
