# Arabic Content

Rules for producing Arabic and bilingual Arabic/English content that reads as native authorship rather than translated English — canonical name spellings, language-leak scanning, RTL verification, and Arabic-locale test gating.

## What it does

- Enforces **author, don't translate**: Arabic drafted directly for the target register, with the English version used only as a meaning reference, and English-mirroring syntax rejected
- Keeps **one canonical Arabic spelling** per brand, product, and personal name, recorded in project memory so it is confirmed once and never re-asked or drifted
- Scans **rendered output** for language leaks in both directions — Latin strings in the Arabic locale, stray Arabic in the English one — because leaks usually come from data, defaults, and fallbacks rather than translation files
- Treats mixed-language UI as a **bug, not a cosmetic issue**
- Verifies **RTL rendering**: layout direction, alignment, icon mirroring, number/date formatting, and explicit direction handling for mixed bidi strings
- Gates test campaigns on the **Arabic path as a first-class target** — never English-only with Arabic assumed equivalent
- Ships a verification checklist and a common-failure-modes list (word-for-word UI strings, unlocalized data leaking district/category names, name spelling drift, fixing locale files when the leak is in hardcoded defaults)

## When to use

Writing or reviewing Arabic UI strings, i18n locale files, marketing copy, store listings, or documentation; building or testing any AR/EN bilingual app or site; or when someone flags mixed-language UI, awkward translated register, or a misspelled name. Layer it on top of a general cross-locale test process (`test-ui` / `test-ux`) — this skill adds the Arabic-specific authorship, canonical-spelling, and leak rules.

## What's inside

- [SKILL.md](SKILL.md) — the five-step workflow (author don't translate, canonical spellings, leak scan, RTL check, Arabic test gate), verification checklist, common failure modes
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/arabic-content ~/.claude/skills/`
**Codex:** `cp -r skills/arabic-content $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\arabic-content "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse skills\arabic-content "$env:USERPROFILE\.codex\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
