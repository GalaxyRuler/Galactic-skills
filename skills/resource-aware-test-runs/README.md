# Resource-Aware Test Runs

Protects an interactive Windows desktop from CPU-hungry local test suites while preserving honest verification — narrow tests during red/green loops, worker caps on bursty runners, full suites at the boundary, and a clear statement of what was not verified.

## What it does

- Inspects the repo's existing scripts and runner **before** choosing flags, then prefers the normal test command with the smallest relevant target added
- Keeps **red loops narrow** — file, test-name, or package filters instead of a full-suite run while proving a failing test
- Caps bursty JS runs: for Vitest, sets **both** `--minWorkers` and `--maxWorkers` (`--maxWorkers` alone can conflict with a higher default minimum) plus a compact reporter for repeat loops
- **Saves full verification for the boundary**: runs the broader lint/type/test/build gate before claiming completion, and announces long or uncapped runs before starting them
- Handles **Cargo contention on Windows** — recognizes package-cache and artifact-directory lock waits, and uses a short lane-specific `CARGO_TARGET_DIR` for parallel worktrees or agent lanes
- Keeps the Cargo registry cache shared (waiting is cheap) while isolating artifact dirs (locks waste red/green time)
- Serializes Rust tests that touch process-global state or static atomics with `-- --test-threads=1` rather than mistaking interleaving for product behavior
- **Refuses to paper over performance symptoms**: measures the specific command before blaming background processes, and records command, exit code, wall time, and whether caps/reporters were used
- Explicitly does not weaken release gates, CI requirements, or an exact command the user asked for

## When to use

Running local test suites on an interactive Windows desktop — especially npm/Vitest/Playwright suites, TDD red loops, Rust/Cargo tests across multiple worktrees, or reports of lag, stutter, high CPU, or noisy full-suite output.

## What's inside

- [SKILL.md](SKILL.md) — six-step workflow (target/script identification, narrow red loop, worker caps, boundary verification, Cargo lock contention, measuring performance symptoms), verification checklist, common failure modes
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/resource-aware-test-runs ~/.claude/skills/`
**Codex:** `cp -r skills/resource-aware-test-runs $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\resource-aware-test-runs "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse skills\resource-aware-test-runs "$env:USERPROFILE\.codex\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
