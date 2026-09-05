---
name: arabic-content
description: Use when writing, reviewing, or testing Arabic or bilingual Arabic/English content — UI strings, i18n locales, RTL layouts, store listings, posts, or docs — or when the user reports English leaking into the Arabic version or literal-sounding translations.
---

# Arabic Content

## Overview

Arabic output must read as content authored in Arabic, not as a translation of English. Bilingual apps must not leak one language into the other's rendered UI. Names and brand terms have one canonical Arabic spelling per project and must not drift.

## When to use

Use this when:
- Writing or reviewing Arabic UI strings, locale files, marketing copy, store listings, or documentation.
- Building or testing any AR/EN bilingual app or site.
- The user flags mixed-language UI, awkward translated register, or a misspelled name.

For the general cross-locale test process use test-ui/test-ux; this skill adds the Arabic-specific authorship, canonical-spelling, and leak rules and should be applied alongside them.

## Workflow

1. Author, never translate literally
- Draft Arabic content directly in Arabic for the intended register and audience; use the English version only as a meaning reference.
- Reject phrasing that mirrors English syntax or idiom word-for-word. Read the result as standalone Arabic and ask whether a native author would write it that way.
- Pick domain terms deliberately (e.g. the natural Arabic term for the concept, not the dictionary gloss).

2. Keep canonical spellings
- Brand names, product names, and personal names get one canonical Arabic spelling per project.
- Before writing such a name, check the project's glossary/memory; if absent, confirm the spelling once with the user and record it in project memory so it is never re-asked.

3. Scan for language leaks
- Rendered Arabic locale must contain no unintended Latin/English strings (labels, dropdown options, data-driven names, dates, placeholders) — and the English locale no stray Arabic.
- Scan rendered output, not just locale files: leaks usually come from data, defaults, and fallbacks, not translation files.
- Treat mixed-language UI as a bug, not a cosmetic issue.

4. Check RTL rendering
- Verify layout direction, alignment, icon mirroring, and number/date formatting in the Arabic locale.
- Mixed bidi strings (Arabic text with Latin identifiers or numbers) need explicit direction handling.

5. Gate tests on the Arabic path
- Any UI/E2E test campaign for a bilingual project must run the Arabic locale as a first-class target, including the leak scan above — not English-only with Arabic "assumed equivalent".

## Verification checklist

- Arabic copy reads as native authorship; no literal-translation register.
- All names/brand terms match the project's canonical spellings.
- Rendered AR locale scanned for Latin leaks (including data-driven lists); EN locale scanned for the reverse.
- RTL layout and bidi formatting verified on the changed screens.
- Test plans explicitly include the Arabic locale.

## Common failure modes

- Translating English UI strings word-for-word and shipping stilted Arabic.
- English district/category/product names leaking into the Arabic UI from unlocalized data sources.
- Spelling the user's name or product name differently across sessions.
- Testing only the English locale and declaring the bilingual app verified.
- Fixing locale files while the leak comes from hardcoded defaults or API data.
