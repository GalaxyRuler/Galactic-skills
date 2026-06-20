# Canvas & Bases

Two native Obsidian file types for visual maps and dashboards. Both are edited as files — validate before saving.

## JSON Canvas (`.canvas`)

Use Canvas for visual maps, project graphs, research maps, or dependency diagrams. A `.canvas` file is JSON with top-level `nodes` and `edges` arrays (the open [JSON Canvas](https://jsoncanvas.org) spec).

**Rules:**
- Generate unique 16-character lowercase-hex IDs for every node and edge.
- Required node fields: `id`, `type`, `x`, `y`, `width`, `height`.
- Node types: `text`, `file`, `link`, `group`.
  - `text` needs `text`; `file` needs `file`; `link` needs `url`; `group` may have a `label`.
- Use real newline escapes (`\n`) inside JSON strings; do not double-escape to `\\n`.
- Space new nodes 50–100px apart; align coordinates to 10 or 20px increments.

**Validate before finishing:**
1. JSON parses.
2. IDs are unique across nodes *and* edges.
3. Every edge `fromNode` / `toNode` points at an existing node.
4. Node-type required field present (`text` / `file` / `url`, or group `label`).
5. Edge `fromSide`/`toSide` ∈ {`top`,`right`,`bottom`,`left`}; ends are `none` or `arrow`.

Minimal skeleton:

```json
{
  "nodes": [
    {"id":"a1b2c3d4e5f60718","type":"text","text":"Start","x":0,"y":0,"width":200,"height":60},
    {"id":"f1e2d3c4b5a60718","type":"file","file":"notes/next.md","x":0,"y":120,"width":260,"height":80}
  ],
  "edges": [
    {"id":"0011223344556677","fromNode":"a1b2c3d4e5f60718","fromSide":"bottom","toNode":"f1e2d3c4b5a60718","toSide":"top","toEnd":"arrow"}
  ]
}
```

## Bases (`.base`)

Use a `.base` for native Obsidian dashboards instead of Dataview blocks where a saved, filterable view is cleaner. Base files are YAML.

**Authoring checklist:**
1. Define global `filters` first; use nested `and`, `or`, `not` only when needed.
2. Add `formulas` only for computed values reused by views.
3. Add `properties` display names for user-facing columns.
4. Configure `views` (`table`, `cards`, `list`, `map`) with an explicit `order`.
5. Validate YAML and every formula reference before opening in Obsidian.

Skeleton:

```yaml
filters:
  and:
    - 'file.ext == "md"'
    - 'file.hasTag("project")'

formulas:
  days_since_update: 'if(updated, (today() - date(updated)).days, "")'

properties:
  formula.days_since_update:
    displayName: "Days Since Update"

views:
  - type: table
    name: "Projects"
    order:
      - file.name
      - status
      - summary
      - formula.days_since_update
```

**Pitfalls:**
- Quote strings containing YAML special characters: `:`, `{}`, `[]`, `#`, `|`, `<`, `>`, `=`, `%`, backticks.
- Wrap formulas containing double quotes in single quotes: `'if(done, "Yes", "No")'`.
- Date subtraction returns a Duration — access `.days`/`.hours` before `round()`.
- Guard optional properties: `if(due, (date(due) - today()).days, "")`.
- Every `formula.x` used in `order`, `properties`, or `summaries` must be defined under `formulas`.

**Embed a Base in a note:**

```markdown
![[projects.base]]
![[projects.base#Active Projects]]
```
