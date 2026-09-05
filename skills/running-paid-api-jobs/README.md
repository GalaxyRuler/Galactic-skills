# Running Paid API Jobs

Treats a paid model/API run as a budget-bound operation rather than a normal retry — preserve the user's authorization exactly, preflight without spending, run once under capture, and report realized cost and artifacts without leaking secrets.

## What it does

- **Locks the authorization**: exact command, cost cap, run count, cwd, branch, and expected artifact paths, taken from the user and not silently altered
- Forbids raising the cap, increasing N, broadening conditions, or launching a second paid attempt without fresh approval
- **Preflights without spend**: verifies cwd/branch/SHA/dirty state, confirms credentials exist without printing them, prepares unique log paths so failed attempts are not overwritten
- Requires **checkpoint/resume support for runs over ~1 hour**, with the exact `--resume` invocation documented before spend starts — or explicit acknowledgment of the all-or-nothing risk
- Proposes **chunked or offloaded execution** for long jobs instead of tying up an interactive desktop, without restructuring an exactly-specified command on its own
- **Runs once under capture**: timer, stdout, stderr, exit code, output directory; a call that reaches the provider counts as spent even if it fails later
- **Post-run audit**: realized cost vs cap, cache hit/miss metrics, branch/SHA, exact command, start/end times, artifact paths
- **Secret-scans generated logs and artifacts** before surfacing their paths; never prints tokens, keys, private URLs, or credential-bearing env vars
- Final report states whether the authorized run count was respected and exactly what was not rerun or not verified

## When to use

The user authorizes a paid API, model, benchmark, eval, pilot, or one-off command with a hard cost cap, max-cost flag, strict budget, or explicit one-run limit. Not for free local tests, CI, dry runs, or mock/offline evals — unless they gate a later paid run.

## What's inside

- [SKILL.md](SKILL.md) — five-step workflow (lock authorization, preflight without spend, run once under capture, post-run audit, final report), verification checklist, common failure modes
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/running-paid-api-jobs ~/.claude/skills/`
**Codex:** `cp -r skills/running-paid-api-jobs $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\running-paid-api-jobs "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse skills\running-paid-api-jobs "$env:USERPROFILE\.codex\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
