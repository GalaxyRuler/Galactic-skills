---
name: resource-aware-test-runs
description: Use when running local test suites on an interactive Windows desktop, especially npm/Vitest/Playwright suites, TDD red loops, or reports of lag, stutter, high CPU, or noisy full-suite output.
---

# Resource-Aware Test Runs

## Overview

Protect the user's interactive desktop while preserving honest verification. Focused tests come first; broad suites run when they are actually needed.

## When to use

Use this when:
- Running tests locally on the user's Windows desktop.
- A repo's full suite is CPU-heavy, parallel, noisy, or known to cause lag/stutter.
- Doing TDD red/green loops where a full suite would be premature.
- Running Rust/Cargo tests or builds on Windows where multiple worktrees, agents, or long builds can contend for package-cache or artifact locks.

Do not use this to weaken release gates, CI requirements, or explicit user commands. If the user asks for an exact command, run that command or explain the risk before changing it.

## Workflow

1. Identify the target and script
- Inspect the repo's existing scripts and test runner before choosing flags.
- Prefer the repo's normal test command with the smallest relevant target added.

2. Red loop: run the narrowest meaningful test
- Avoid full-suite runs while proving a new failing test or debugging one file.
- Use file, test-name, or package-level filters when available.

3. Cap bursty JS test runs when interactivity matters
- For Vitest through npm, prefer:

```powershell
npm test -- test/path/to/file.test.ts --minWorkers=1 --maxWorkers=2 --reporter=dot
```

- If running the whole Vitest suite with caps, set both `--minWorkers` and `--maxWorkers`; `--maxWorkers` alone can conflict with a higher default minimum.
- Use compact reporters for repeat loops, but rerun with normal output when diagnostics are needed.

4. Save full verification for the boundary
- Run the broader lint/type/test/build gate before claiming completion when the change warrants it.
- Announce long or uncapped full-suite runs before starting them if they are likely to affect desktop responsiveness.
- If a full run is deferred because of cost or user preference, state exactly what was and was not verified.

5. Handle Cargo contention on Windows deliberately
- If Cargo repeatedly prints `Blocking waiting for file lock on package cache` or `artifact directory`, check whether another build/test is active before starting another broad command.
- For parallel worktrees or agent lanes, prefer a short, lane-specific `CARGO_TARGET_DIR` such as `C:\t\<repo-or-task>` to reduce artifact-directory contention and long path pressure.
- Keep the Cargo registry/package cache shared unless there is a specific reason to isolate it; most contention is acceptable waiting, while artifact locks often waste red/green time.
- For Rust tests that touch process-global state or static atomics, use targeted tests first and add `-- --test-threads=1` when interleaving can invalidate the assertion.
- Record the exact env vars, target dir, command, exit code, and whether the failure was a test assertion, compile failure, timeout, or lock wait.

6. Do not paper over performance symptoms
- If the user reports lag during tests, measure the specific command before blaming background processes.
- Capture command, exit code, wall time, and whether worker caps or reporters were used.

## Verification checklist

- The first test command was focused to the changed behavior unless the user requested a full suite.
- Worker caps or compact output were used when the suite is known to be bursty and local interactivity matters.
- Cargo runs that risk lock contention use a scoped `CARGO_TARGET_DIR` or explicitly report why the default target dir was kept.
- Rust tests with shared process-global state are serialized or otherwise isolated when proving behavior.
- Full verification was run at the end, or the final response clearly says why it was not.
- No repo scripts, dependencies, or lockfiles were changed just to make local testing quieter unless explicitly requested.

## Common failure modes

- Running `npm test` for every red-phase check in a large Vitest repo.
- Using `--maxWorkers=2` without `--minWorkers=1` in Vitest and hitting a worker-minimum conflict.
- Hiding useful failure output behind a compact reporter; switch back to normal output for diagnosis.
- Treating resident `node` or `npx` processes as the cause without measuring the exact test command.
- Starting several broad Cargo builds in parallel on Windows and losing time to package-cache or artifact-directory locks.
- Re-running process-global Rust tests concurrently and mistaking interleaving for product behavior.
