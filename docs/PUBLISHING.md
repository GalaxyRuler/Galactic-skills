# How skills get published here

Every skill in this repo goes through a publish pipeline before landing on `main`.

## Pipeline

1. **Privacy scan** — every file in the skill folder is scanned for:
   - Personal emails and usernames
   - Hardcoded absolute paths (`C:\Users\<name>\...`, home directories)
   - API keys, tokens, secrets (`ghp_*`, `sk-*`, bearer tokens, long alphanumeric strings)
   - Internal project names or private repo references
   - Machine-specific config (hostnames, IPs, UUIDs)

2. **Generalization** — personal references are replaced with `<placeholder>` values. Technical content, logic, and structure are preserved unchanged.

3. **Dual-runtime packaging** — each skill ships with:
   - `SKILL.md` — Claude Code format (YAML frontmatter with `name` + `description`)
   - `agents/openai.yaml` — Codex companion manifest
   - `README.md` — human-facing landing page (what it does, when to use, what's inside, install)

4. **Docs update** — the top-level README skill table gets a row, and any other index or catalog that enumerates skills is kept in sync.

5. **Commit + push** — one commit per skill: `publish: add <skill-name>`.

## Skill folder layout

```
skills/<skill-name>/
├── README.md          # human-facing landing page (required)
├── SKILL.md           # main instructions (required, ~100 lines)
├── agents/
│   └── openai.yaml    # Codex manifest (required)
├── REFERENCE.md       # optional deep-dive docs
└── scripts/           # optional utility scripts
```

## Quality bar

- `description:` frontmatter states what the skill does and when to trigger it ("Use when...")
- SKILL.md stays under ~100 lines; detail goes in reference files, one level deep. A skill with two distinct operating modes may reach ~120 — but only after every lookup table and per-item detail already lives in `references/`. Length is never the reason to keep a table in SKILL.md
- Every skill folder has a `README.md` (what it does, when to use, what's inside, install) — kept in sync when modules change
- No time-sensitive info
- Concrete examples included
