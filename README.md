# Galactic Skills

Public skills for [Claude Code](https://claude.ai/code) and [Codex](https://openai.com/codex) — privacy-scanned and generalized for anyone to install.

## What are skills?

Skills are instruction files that extend an AI coding agent with domain-specific workflows. Install a skill and the agent knows how to handle that task type automatically.

Every skill here ships in dual-runtime format: `SKILL.md` for Claude Code, `agents/openai.yaml` companion for Codex.

## Installing a skill

**Claude Code:**

```bash
# copy the skill folder into your skills directory
cp -r skills/<skill-name> ~/.claude/skills/
```

**Codex:**

```bash
cp -r skills/<skill-name> $CODEX_HOME/skills/
```

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\<skill-name> "$env:USERPROFILE\.claude\skills\"   # Claude Code
Copy-Item -Recurse skills\<skill-name> "$env:USERPROFILE\.codex\skills\"    # Codex
```

## Skills

| Skill | Description |
|-------|-------------|
| [repo-stewardship](skills/repo-stewardship) | Safely acquire, inspect, sync, validate, and prepare Git repositories for review or delivery — permission tiers, quality gates, changelog/SemVer discipline, PR readiness reports |

## How skills get here

Each skill passes a privacy scan and generalization pass before publishing. Process details: [docs/PUBLISHING.md](docs/PUBLISHING.md).

## Contributing

Adapt freely — replace any `<placeholder>` values with your own config. PRs welcome if they pass the [quality bar](docs/PUBLISHING.md#quality-bar).

## License

[MIT](LICENSE)
