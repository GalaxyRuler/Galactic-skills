# Verify Live Deploy

Merged, deployed, and live are three different states. This stops "done" from being reported while production still serves the old build, a CDN still caches the old page, or the user's installed copy is still on the old version.

## What it does

- Forces every ship report to name all three states explicitly: merged (yes/no), deployed (yes/no/not attempted), live-verified (yes/no)
- Blocks the "auto-deploys on merge" assumption — the pipeline must be verified to have run and succeeded, not assumed
- Runs the deploy when the path is known and authorized, instead of handing it back; names the exact command or pipeline when it is not
- Requires liveness evidence against the production URL, never localhost or a preview build
- Demands cache-defeating proof: build hash, version string in the served payload, version/health endpoint, cache-busting query, or a rendered check of the specific changed element
- Accounts for CDN cache TTL — a hard refresh on your side is not proof the user's cache is clear
- Treats a desktop release as unfinished until the installed copy is confirmed updated, not merely published
- Closes honestly: "merged and deployed; live check pending because X" rather than a bare success claim
- Lists the common failure modes, including treating a green CI run or a clean deploy log as proof of liveness

## When to use

Completing a change that ships via a deploy step (VPS, Cloudflare Worker/Pages, static host, container), cutting a release of a desktop app the user runs locally, or when the user asks whether something is live and reports the site looking unchanged after a "done" claim.

## What's inside

- [SKILL.md](SKILL.md) — the three states, deploy-if-authorized rule, liveness verification against the real artifact, desktop-release check, verification checklist, common failure modes
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/verify-live-deploy ~/.claude/skills/`
**Codex:** `cp -r skills/verify-live-deploy $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\verify-live-deploy "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse skills\verify-live-deploy "$env:USERPROFILE\.codex\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
