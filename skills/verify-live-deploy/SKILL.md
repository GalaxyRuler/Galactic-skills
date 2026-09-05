---
name: verify-live-deploy
description: Use when merging or deploying a change that ships to a live target — websites, Workers, VPS services, or installed desktop apps — releasing, claiming a change is live, or when the user asks "is it deployed?" or reports the live site unchanged. This verifies the production/deployed artifact, not local behavior of a change.
---

# Verify Live Deploy

## Overview

Merged, deployed, and live are three different states. A merge with no deploy leaves production on old code; a deploy with no liveness check leaves stale caches and old installs undetected. Never report "done" for a shipped change until the user-facing artifact is verified running the new code, or the report explicitly says which state was reached.

## When to use

Use this when:
- Completing a change that ships via a deploy step (VPS, Cloudflare Worker/Pages, static host, container).
- Cutting a release of a desktop app the user runs locally.
- The user asks whether something is live, or says the site looks unchanged after a "done" claim.

## Workflow

1. Report the three states explicitly
- After any merge, state: merged (yes/no), deployed (yes/no/not attempted), live-verified (yes/no).
- Never let "merged" imply "deployed". If the project auto-deploys on merge, verify the pipeline actually ran and succeeded — do not assume.

2. Deploy if authorized
- If the deploy path is known and authorized, run it rather than handing it back to the user.
- If not authorized, say exactly what command or pipeline still needs to run.

3. Verify liveness against the real artifact
- Check the production URL, not localhost or a preview.
- Prefer proof that defeats caching: build hash or version string in the served payload, a version/health endpoint, a cache-busting query, or a rendered check of the specific changed element.
- For CDN-fronted sites, account for cache TTL; a hard refresh on your side does not prove the user's cache is clear.

4. Desktop releases: verify the installed copy
- A release is not done when the artifact is published. If the user runs an installed copy, confirm the installed version was updated (install it if authorized, or state that the local install is still on the old version).

5. Close honestly
- "Done" only after live verification. Otherwise: "merged and deployed; live check pending because X" — never a bare success claim.

## Verification checklist

- Final report names all three states: merged / deployed / live-verified.
- Liveness evidence is specific: version string, hash, endpoint response, or rendered element — not "deploy command exited 0".
- Production URL (or installed binary version) was checked, not a local or preview build.
- Any skipped verification is stated with the reason.

## Common failure modes

- Claiming done after merge while production still serves the old build.
- Treating a successful push or CI run as proof of deployment.
- Verifying on localhost/preview and reporting the production site as updated.
- Publishing a desktop release while the user's installed copy stays stale.
- Declaring a cached page updated because the deploy log looked clean.
