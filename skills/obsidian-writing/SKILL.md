---
name: obsidian-writing
description: Use when writing, editing, or organizing content in an Obsidian vault — notes, frontmatter/properties, wikilinks, callouts, Dataview/Tasks queries, Bases (.base) dashboards, Canvas (.canvas) files, Templater automation, citation/literature workflows, or vault git commits. Also use when setting up an anti-drift vault system (one-note-one-home routing, self-routing templates, project boards) or driving Obsidian through its Local REST API or an Obsidian MCP server.
---

# Obsidian Writing

Methodology for working inside an Obsidian vault: native Markdown, queries, dashboards, automation, and an optional opinionated vault-management system that keeps a growing vault from drifting. Replace every `<placeholder>` with your own vault's values.

## Orient before writing (30 seconds)

1. **Read the vault's agent constitution** if present — a `CLAUDE.md`, `AGENTS.md`, or `GEMINI.md` at the vault root carries routing rules specific to that vault. Vault instructions win over this skill.
2. **Open the relevant hub/MOC or board** to load context for what you're about to write.
3. **Check an existing note of the same type** — match its frontmatter, folder, and naming before creating a new one.
4. **Never stage `.obsidian/`** (app state) in a commit.

## Tool choice — narrowest surface that proves the result

| Need | Prefer |
|---|---|
| Note CRUD, search, move, command-palette action | Obsidian MCP (`mcp__obsidian__*` or however your server is named) if exposed; else the Local REST API |
| Live Dataview refresh, open-note state, palette action | REST/MCP `POST /commands/execute` |
| `.base` / `.canvas`, byte-level edits, bulk rename, git ops | Filesystem edit; reload/open in Obsidian afterward |

Using MCP/REST keeps Obsidian's index, frontmatter parser, and link graph consistent. Don't guess live render state from file text when the user reports a UI/render problem — capture the exact error via REST/MCP or the `obsidian` CLI.

## Markdown essentials

`[[Note]]`, `[[Note|alias]]`, `[[Note#Heading]]`, `[[Note#^block]]`, `![[Note]]`, `![[img.png|300]]`. Prefer `[[wikilinks]]` (rename-safe) for internal links; use `[label](https://…)` only for external URLs. Callouts: `> [!note]`, `> [!warning] Title`, `> [!faq]-` (collapsed). Full syntax → [MARKDOWN-SYNTAX.md](MARKDOWN-SYNTAX.md).

## Reference files

- [MARKDOWN-SYNTAX.md](MARKDOWN-SYNTAX.md) — wikilinks, embeds, callouts, block IDs, comments, highlights, math, tags, frontmatter
- [QUERIES.md](QUERIES.md) — Dataview tables and Tasks query blocks, generalized patterns + live-refresh
- [CANVAS-AND-BASES.md](CANVAS-AND-BASES.md) — JSON Canvas authoring rules + `.base` YAML dashboards
- [PLUGINS.md](PLUGINS.md) — high-leverage plugin playbook (Templater, Dataview, Tasks, citations, Smart Connections, Breadcrumbs, Mermaid, Pandoc, sync/git, REST API/MCP)
- [VAULT-SYSTEM.md](VAULT-SYSTEM.md) — optional opinionated system: one-note-one-home routing, frontmatter schemas, self-routing templates, anti-drift checklist, project-board ritual, literature workflow

## Vault git commits

The vault is its own git repo. Stage only your changed notes — `git add <files>`, never `git commit -A`, never `.obsidian/`. Run `git status` first. Suggested message style: `docs(vault): <what changed>`. Commit to the vault's own branch (often `main` or `master`).

## Common mistakes

| Mistake | Fix |
|---|---|
| Staging `.obsidian/` app state | `git status` first; stage only your files |
| Creating a note without frontmatter | Every note gets frontmatter matching nearby notes of its type |
| Guessing live render state | Inspect via REST/MCP/CLI; don't assume from file text |
| Breaking a `.base` formula or `.canvas` edge | Validate YAML / parse JSON before saving — see CANVAS-AND-BASES.md |
| Hardcoding folder paths in links | Use bare-name `[[wikilinks]]` so moves don't break them |
