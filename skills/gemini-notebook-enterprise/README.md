# Gemini Notebook Enterprise

Automate Google Gemini Notebook Enterprise (NotebookLM Enterprise) through its documented
Discovery Engine Notebook API — inventory, sources, ingestion health, and agent integration —
while keeping notebook Q&A an explicitly negotiated capability instead of a guessed endpoint.

## What it does

- Separates the three layers people conflate: the **consumer** NotebookLM product (no supported
  API), **Gemini Notebook Enterprise** on Google Cloud (the only automatable surface), and the
  **agent** that calls it (Codex, Claude Code, a cron job) — which is an execution plane, never an
  alternative Notebook provider
- Maps the published **method surface**: notebooks create/get/listRecentlyViewed/batchDelete/share,
  sources batchCreate/get/batchDelete/uploadFile — with the accepted OAuth scopes and the IAM
  permission each one actually checks
- Covers the **generation surface**, which is where most "that's not automatable" answers go wrong:
  `notebooks.audioOverviews.create` takes `sourceIds` plus an `episodeFocus` instruction, so
  running the notebook's own model over a chosen subset of sources **is** documented — as a
  generated artifact, not as answer text with citations
- Names the **query asymmetry** honestly: no public Q&A transport is published, so the skill ships
  a **capability contract** that reports `unsupported_public_api` rather than inventing a URL, and
  forbids silently substituting a different RAG engine and calling the answer "NotebookLM"
- Treats source creation as an **asynchronous state machine** (`PENDING` → `COMPLETE` / `ERROR`),
  preserving Google's structured `failureReason` families (paywall, blocked domain, Drive download
  restriction, source too long, transcription failure) instead of collapsing them to "failed"
- Ships an **inventory model** that separates Google's identity fields from your governance fields,
  so "use only the approved sources" resolves to exact resource names rather than fuzzy titles
- Gives an **auth model that works**: user OAuth / ADC over API keys and exported service-account
  keys, narrow Discovery Engine scopes over `cloud-platform`, and Drive authorization added only
  when a workflow actually imports Drive documents
- Lays out **agent integration tiers** — local script, STDIO MCP, remote OAuth MCP broker — plus
  why hosted agent environments need the broker (setup secrets are gone by the agent phase) and how
  to split read / elevated / destructive / capability-gated tool scopes

## When to use

Enumerating notebooks or reconciling an inventory, adding or removing sources, sharing notebooks,
diagnosing a stuck `PENDING` source or a 401/403/429, designing how an agent reaches the Notebook
API, or answering "can we automate NotebookLM Q&A?"

Also triggers **defensively**: when someone proposes driving the consumer NotebookLM UI with
cookies or private frontend RPCs, the skill refuses that path and explains the supported one.

## What's inside

- [SKILL.md](SKILL.md) — the three-layer boundary, terminology, ten hard rules, capability
  contract, workflow, ingestion state machine, and the auth model in one paragraph
- [references/API-SURFACE.md](references/API-SURFACE.md) — endpoint and resource-name shapes,
  method → scope → IAM map, the query asymmetry, documented limits, representative JSON, source
  status/failure model, inventory schema, refresh algorithm
- [references/CODEX-INTEGRATION.md](references/CODEX-INTEGRATION.md) — the two independent auth
  layers, execution-mode table, why cloud agents need a broker, broker tool/scope tiers, skill
  packaging, capability-negotiation sequence, target architecture
- [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) — nine-step setup sequence,
  symptom → cause → action matrix, and the security baseline (credential handling, audit-log
  content warning, untrusted source contents, read/write separation)
- [scripts/notebook_client.py](scripts/notebook_client.py) — minimal REST client: pagination,
  retry policy that deliberately does **not** replay non-idempotent creates, capability-gated
  `query_notebook`, an `inventory` CLI, and an offline `--selftest`
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/gemini-notebook-enterprise ~/.claude/skills/`
**Codex:** `cp -r skills/gemini-notebook-enterprise $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\gemini-notebook-enterprise "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse skills\gemini-notebook-enterprise "$env:USERPROFILE\.codex\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.

## Script usage

```bash
python -m pip install google-auth requests
```

```bash
gcloud auth application-default login
```

```bash
python skills/gemini-notebook-enterprise/scripts/notebook_client.py inventory --project-number YOUR_PROJECT_NUMBER
```

```bash
python skills/gemini-notebook-enterprise/scripts/notebook_client.py --selftest
```

## A note on freshness

The Notebook API is a `v1alpha` preview surface. `references/API-SURFACE.md` is a **snapshot**, and
its rows carry **[verified]** / **[unverified]** tags recording what was confirmed against Google's
published how-to pages versus what came from reference pages that could not be machine-read. The
skill's standing instruction is to re-check the live docs before quoting method availability,
scopes, or limits — and never to quote consumer-tier NotebookLM limits for an Enterprise notebook.
