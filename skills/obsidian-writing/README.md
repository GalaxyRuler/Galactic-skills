# Obsidian Writing

A methodology for writing, editing, and organizing content in an [Obsidian](https://obsidian.md) vault — native Markdown, live queries, dashboards, automation, and an optional opinionated vault-management system that keeps a growing vault from drifting.

## What it does

- Teaches Obsidian-flavored Markdown: rename-safe `[[wikilinks]]`, embeds, callouts, block IDs, math, and frontmatter properties
- Covers live dashboards: Dataview tables, Tasks query blocks, and native Bases (`.base`) views
- Covers JSON Canvas (`.canvas`) authoring with a validation checklist
- Gives a high-leverage plugin playbook (Templater, Dataview/Tasks, Smart Connections, Breadcrumbs, citation tooling, Pandoc, sync/git) and how to drive Obsidian via its Local REST API or an MCP server
- Ships an optional anti-drift vault system: one-note-one-home routing, per-type frontmatter schemas, self-routing Templater templates, a drift checklist, and a project-board update ritual

## When to use

Writing or editing notes; setting frontmatter/properties; building Dataview/Tasks/Bases dashboards; authoring Canvas files; writing Templater automation; running a citation/literature workflow; committing vault changes to git; or standing up a structured, drift-resistant vault.

## What's inside

- [SKILL.md](SKILL.md) — router: orientation, tool choice, Markdown essentials, git commits, common mistakes
- [MARKDOWN-SYNTAX.md](MARKDOWN-SYNTAX.md) — links, embeds, callouts, block IDs, comments, highlights, math, frontmatter
- [QUERIES.md](QUERIES.md) — Dataview tables, Tasks query blocks, live refresh, and when to use each
- [CANVAS-AND-BASES.md](CANVAS-AND-BASES.md) — JSON Canvas authoring rules + `.base` YAML dashboards
- [PLUGINS.md](PLUGINS.md) — plugin playbook + REST API/MCP + sync/version-control guidance
- [VAULT-SYSTEM.md](VAULT-SYSTEM.md) — optional opinionated system: routing, frontmatter schemas, self-routing templates, drift checklist, board ritual, literature workflow
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/obsidian-writing ~/.claude/skills/`
**Codex:** `cp -r skills/obsidian-writing $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\obsidian-writing "$env:USERPROFILE\.claude\skills\"
```

Replace every `<placeholder>` (vault path, project/tag names, API key) with your own values. The vault system in `VAULT-SYSTEM.md` is opinionated and optional — adopt the parts that fit your vault.

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
