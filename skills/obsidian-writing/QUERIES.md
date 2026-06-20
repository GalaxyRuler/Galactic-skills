# Dataview & Tasks Queries

Two query systems power live dashboards in a vault. Both depend on consistent frontmatter — see [VAULT-SYSTEM.md](VAULT-SYSTEM.md) for schemas.

## Dataview

SQL-style queries over note frontmatter and inline fields. Requires the **Dataview** community plugin.

```dataview
TABLE status, summary, updated
FROM #project
SORT updated DESC
```

```dataview
TABLE WITHOUT ID ("Phase " + phase) AS "Phase", status, updated, file.link AS "Plan note"
FROM #my-project-phase
SORT phase ASC
```

```dataview
LIST
FROM "papers/my-project"
WHERE type = "section"
SORT order ASC
```

**Backlink / cross-link table** — what links to the current note:

```dataview
TABLE status, summary, updated
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT updated DESC
```

Common sources: `#tag`, `"folder/path"`, `[[Note]]`, or combinations with `AND`/`OR`. Common fields: `file.link`, `file.name`, `file.mtime`, `file.tags`, plus any frontmatter key.

**Inline DataviewJS** (`dataviewjs` fenced block) is available for logic Dataview Query Language can't express — use sparingly; prefer DQL for readability.

## Tasks

Portable Markdown task queries. Requires the **Tasks** community plugin. Use ` ```tasks ` blocks for embedded reports:

````
```tasks
not done
due before 2025-02-01
sort by due
```
````

Task emojis the plugin recognizes: `📅` due · `🛫` start · `⏳` scheduled · `⏫`/`🔼`/`🔽` priority · `🔁` recurrence · `✅` completion date.

```markdown
- [ ] Draft section #project/my-project 📅 2025-02-01 ⏫
- [x] Ship release #project/my-project ✅ 2025-01-20
```

## Live refresh (REST/MCP)

Rendered Dataview output (not raw Markdown) refreshes via the Local REST API / an Obsidian MCP server:

```
POST /commands/execute   { "commandId": "dataview:dataview-force-refresh-views" }
```

After editing a note that feeds a dashboard, force a refresh so the live view reflects the change.

## Choosing between them and Bases

- **Tasks plugin** — owns embedded task *query blocks* and deadline reports.
- **Dataview** — owns flexible note/field queries and tables.
- **Bases** (`.base`, see [CANVAS-AND-BASES.md](CANVAS-AND-BASES.md)) — native Obsidian dashboards; prefer a `.base` over piling more Dataview blocks where a saved, filterable view is cleaner.

If a task plugin handles status cycling in your vault, let it own status — don't fight it with a second system.
