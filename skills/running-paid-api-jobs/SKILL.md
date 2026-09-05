---
name: running-paid-api-jobs
description: Use when the user authorizes a paid API, model, benchmark, eval, pilot, or one-off command with a hard cost cap, max-cost flag, strict budget, or explicit one-run limit.
---

# Running Paid API Jobs

## Overview

Paid runs are budget-bound operations, not normal retries. Preserve the user's authorization exactly, prove the run context, capture artifacts, and report spend without exposing secrets.

## When to Use

Use this for paid model/API commands, evals, benchmarks, pilots, or scripts where the user gives a cost cap, budget, max-cost flag, or "single approved run" language.

Do not use this for free local tests, CI, dry runs, or mock/offline evals unless they gate a later paid run.

## Workflow

1. Lock the authorization
- Identify the exact command, cost cap, run count, cwd, branch, and expected artifact paths.
- If the user supplied an exact command, run that command or the closest shell-equivalent; do not silently change paid parameters.
- Never raise the cap, increase N, broaden conditions, or run another paid attempt without fresh authorization.

2. Preflight without spend
- Verify cwd, branch, SHA, dirty state, and required local dependencies.
- Check that required credentials exist without printing their values.
- Prepare unique output/log paths. Preserve failed-attempt logs instead of overwriting them.
- For runs expected to take more than ~1 hour: require checkpoint/resume support before starting. Confirm the harness writes progress checkpoints and document the exact `--resume` (or equivalent) invocation in advance — local desktops lose power and restart mid-run. If checkpointing is unavailable, stop and get explicit user acknowledgment of the all-or-nothing risk before spending.
- Propose chunked execution (resumable segments) to the user as part of the authorization for long jobs; never silently restructure an exactly-specified command into segments. Suggest offloading multi-hour runs to a remote or always-on node instead of the interactive desktop when one is available.

3. Run once under capture
- Start a timer and capture stdout, stderr, exit code, and output directory.
- If the run fails before provider/API construction and no spend occurred, report that clearly before deciding whether any local equivalent is allowed.
- If the paid call starts, treat the run as spent even if it fails later.

4. Post-run audit
- Record realized cost, cache-hit/cache-miss metrics when available, branch/SHA, exact command, start/end times, and artifact paths.
- Scan generated logs/artifacts for secret-like values before reporting paths.
- Do not print tokens, API keys, private URLs, or credential-bearing environment variables.

5. Final report
- State whether the authorized run count was respected.
- Include cost used versus cap, cache behavior, secret-scan result, exit status, and artifacts.
- Say exactly what was not rerun or not verified.

## Verification Checklist

- Exact user cap and run count were preserved.
- Branch/SHA/cwd were verified before execution.
- Command, exit code, wall time, cost, cache metrics, and artifact paths were captured.
- Generated artifacts were scanned for secret-like strings before being surfaced.
- No credential values were printed.
- No second paid run was launched without explicit approval.
- Multi-hour runs had checkpoint/resume verified and the resume command documented before spend started.

## Common Failure Modes

- Retrying a paid command because the result was inconclusive.
- "Fixing" the command by changing N, condition, model, or cap.
- Treating a failed paid call as free just because the process exited nonzero.
- Overwriting first-attempt logs during a fallback.
- Reporting success without cost, cache, secret-scan, and artifact evidence.
- Starting a multi-hour paid run with no checkpointing, so a power cut or restart wastes the entire spend.
- Restarting an interrupted run from zero when a documented resume path existed.
