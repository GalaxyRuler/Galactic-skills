# Tauri Engineering

Production-grade guidelines for building, securing, and shipping Tauri v2 desktop and mobile applications.

## What it does

- Applies the guest-host architecture (TAO/WRY, OS-native Webview, no bundled Chromium, SPA/SSG not SSR)
- Designs IPC commands and state management correctly (Custom Protocol, owned types in async commands, `app.manage()`)
- Hardens security via the ACL capability/permission system
- Optimizes binary size and performance; configures auto-updates and CI/CD
- Defers Rust-side patterns to the [rust-engineering](../rust-engineering) skill

## When to use

Building Tauri desktop or mobile apps, configuring `tauri.conf.json`, writing Tauri commands/plugins, setting up permissions/capabilities, debugging Webview issues, optimizing binary size, configuring auto-updates, or reviewing Tauri code. Also triggers on `tauri.conf.json`, `tauri-plugin-*`, or mentions of WRY/TAO/Webview2/WebKitGTK.

## What's inside

- [SKILL.md](SKILL.md) — architecture, IPC & commands, state management, security/ACL, plugins
- [TESTING-PERF.md](TESTING-PERF.md) — testing strategy and performance / binary-size optimization
- [UPDATES-DEPLOY.md](UPDATES-DEPLOY.md) — auto-updates and CI/CD deployment
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/tauri-engineering ~/.claude/skills/`
**Codex:** `cp -r skills/tauri-engineering $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\tauri-engineering "$env:USERPROFILE\.claude\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
