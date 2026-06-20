# Obsidian Markdown Syntax

Obsidian-flavored Markdown for internal vault structure. Use this for links, structure, and formatting inside a vault.

## Links & embeds

```markdown
[[Note Name]]                  internal note link
[[Note Name|Display Text]]     internal link with alias
[[Note Name#Heading]]          heading link
[[Note Name#^block-id]]        block link
[[#Heading]]                   same-note heading link
![[Note Name]]                 embedded note (transclusion)
![[Note Name#Heading]]         embed a single section
![[image.png|300]]             embedded image with width
![[file.pdf#page=3]]           embed a PDF page
```

Prefer `[[wikilinks]]` for vault notes — Obsidian tracks renames and updates them. Use `[label](https://…)` only for external URLs.

**Bare-name vs path links.** If basenames are unique across the vault, write `[[phase-a-foundations]]`, not `[[plans/project/phase-a-foundations]]`. Bare-name links survive folder moves; path links break on every move. Keeping basenames unique is worth the discipline.

## Callouts

```markdown
> [!note]
> Plain callout.

> [!warning] Custom title
> Warning text with a custom title.

> [!faq]- Collapsed
> Body hidden until expanded (the trailing `-` collapses by default; `+` starts expanded).
```

Common types: `note`, `info`, `tip`, `warning`, `danger`, `todo`, `question`/`faq`, `example`, `quote`, `success`, `failure`, `bug`, `abstract`. Callouts nest by adding `>>`.

## Block & structure syntax

- **Block IDs** — append `^block-id` at the end of a paragraph to make it linkable. For list items or quotes, put the `^block-id` on its own line directly after.
- **Comments** — `%%inline hidden%%` or a multi-line `%% … %%` block. Not rendered, not exported.
- **Highlights** — `==highlighted text==`.
- **Footnotes** — `text[^1]` with `[^1]: definition` elsewhere in the note.
- **Tags** — `#tag` or `#nested/tag` inline. In frontmatter keep `tags` as a YAML list unless nearby notes use inline arrays — match the local convention.

## Math

- Inline: `$x = 1$`
- Block: `$$\hat{y} = X\beta + \epsilon$$`

## Tables

Standard GFM pipe tables render in Obsidian. The Advanced Tables community plugin adds Tab-navigation and auto-alignment, but the raw syntax is plain Markdown.

## Frontmatter (properties)

Every note should open with YAML frontmatter. Obsidian reads it as typed "properties."

```yaml
---
title: My Note
created: 2025-01-15
tags:
  - topic
status: draft
aliases: [alt name]
---
```

Match the field set and tag style already used by nearby notes of the same type — a divergent schema silently breaks Dataview/Bases queries that filter on those fields. See [VAULT-SYSTEM.md](VAULT-SYSTEM.md) for per-type frontmatter schemas and [QUERIES.md](QUERIES.md) for how queries consume these fields.

## Mermaid & diagrams

Diagrams live in fenced ` ```mermaid ` blocks and render natively. See [PLUGINS.md](PLUGINS.md) for diagram-type guidance and theming. For visual maps, use a `.canvas` file (see [CANVAS-AND-BASES.md](CANVAS-AND-BASES.md)).
