# Plugin Playbook

High-leverage Obsidian community plugins and how to use them. Your vault's actual set is the source of truth — check `.obsidian/community-plugins.json` (read it; never stage it). This is a recommended toolkit, not a required one. Reach for a plugin before hand-rolling structure.

| Want | Plugin | How |
|---|---|---|
| Create notes from templates, auto-route to the right folder | **Templater** | `<% %>` scripting; use `tp.file.move()` so notes land in place. See [VAULT-SYSTEM.md](VAULT-SYSTEM.md). |
| SQL-style queries / tables over notes | **Dataview** | DQL blocks. See [QUERIES.md](QUERIES.md). |
| Embedded task lists + deadlines | **Tasks** | ` ```tasks ` query blocks. See [QUERIES.md](QUERIES.md). |
| "What existing notes relate to this?" | **Smart Connections** | Local-embedding "related notes" pane + vector search, no API key. Harvest hits into `same:` / link fields. Data in `.smart-env/` (gitignored). |
| Navigate a multi-note hierarchy | **Breadcrumbs** | Set `up:` / `down:` / `same:` in frontmatter to build a parent→siblings→children trail. |
| Turn a DOI/arXiv id into a literature note | **Citations / BibLib / Zotero bridge** | Auto-fills title/authors/year/venue/citekey into a reference note; cite with `[@citekey]`. |
| Find a paper's neighbours / citation map | **Reference Map** | Sidebar surfaces a paper's own citations for literature discovery. Cache in `.reference-map/` (gitignored). |
| Export a note/section to DOCX/PDF/ePub | **Pandoc** | "Export current document"; keep per-project Pandoc defaults in an `export/` folder. |
| Auto-format notes on save | **Linter** | Normalizes frontmatter order, blank lines, heading spacing. |
| Tab-navigated, auto-aligned tables | **Advanced Tables** | Editing aid only — output is plain Markdown. |
| Deep-link to a note/heading/block from outside | **Advanced URI** | `obsidian://advanced-uri?vault=<vault>&filepath=<path>&heading=<h>`. |
| Charts on a dashboard | **Charts** | ` ```chart ` blocks from YAML. |

## Diagrams (Mermaid)

Mermaid renders natively in fenced ` ```mermaid ` blocks. For any explanation of a process, architecture, workflow, or "how X works," include a diagram — text alone under-communicates flow.

Common types: `graph TD`/`graph LR` (flowcharts, pipelines, decision trees), `sequenceDiagram` (message passing, API calls), `classDiagram` (data models), `stateDiagram-v2` (lifecycles), `erDiagram` (entity relationships), `gantt` (timelines). Set a theme with `%%{init: {'theme': 'dark'}}%%` at the top. The **Mermaid ELK Renderer** plugin gives better auto-layout for dense graphs.

*Optional convention:* lock a `classDef` color palette vault-wide so diagrams stay visually consistent (e.g., one color per node role). Document the palette in your vault constitution and don't change it ad hoc.

## Driving Obsidian programmatically (REST API / MCP)

The **Local REST API** plugin exposes the vault over HTTP and backs most Obsidian MCP servers. Defaults: HTTPS on port **27124**, optional HTTP on **27123**. Authenticate direct REST calls with `Authorization: Bearer <your-api-key>` (the plugin generates the key; store it in an env var, never in a note).

```
GET  /vault/                                 list files
GET  /vault/<path>                           read a note
POST /commands/execute  { "commandId": "app:open-file", "args": { "path": "<path>" } }
POST /commands/execute  { "commandId": "dataview:dataview-force-refresh-views" }
```

Prefer an Obsidian MCP server (`mcp__obsidian__*` or however yours is registered) when its tools are exposed — it keeps the index and link graph consistent. Fall back to direct HTTPS REST, then to filesystem edits only for what MCP/REST can't cover (`.base`/`.canvas` byte-level work, bulk rename, git).

## Sync & version control

- **Official Obsidian Sync** or **Self-hosted LiveSync** — real-time cross-device replication (the live mirror). Run only one sync solution at a time.
- **Obsidian Git** — auto-commits history to the vault's branch (version control). Coexists with a live-sync mirror; the mirror is not a substitute for commits.

## Routing safety net

A note-mover plugin (e.g., **Advanced Note Mover**) can catch notes that escaped template routing into an inbox or the vault root. Treat it as a *safety net*, not the primary router — if it has to correct a note, fix the template or route that produced the stray note. Protect content folders from automatic moves; run in preview/manual mode first.
