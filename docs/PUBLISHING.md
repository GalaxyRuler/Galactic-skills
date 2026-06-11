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

4. **Catalog update** — the README skill table gets a row.

5. **Commit + push** — one commit per skill: `publish: add <skill-name>`.

## Skill folder layout

```
skills/<skill-name>/
├── SKILL.md           # main instructions (required, <100 lines)
├── agents/
│   └── openai.yaml    # Codex manifest (required)
├── REFERENCE.md       # optional deep-dive docs
└── scripts/           # optional utility scripts
```

## Quality bar

- `description:` frontmatter states what the skill does and when to trigger it ("Use when...")
- SKILL.md stays under ~100 lines; detail goes in reference files, one level deep
- No time-sensitive info
- Concrete examples included
