# Rust Engineering

Production-grade guidelines for generating, refactoring, and reviewing Rust — ownership, type-driven design, error handling, async/concurrency, testing, security, and performance.

## What it does

- Enforces "make illegal states unrepresentable" via ADTs, newtypes, and typestate
- Drives strict ownership/borrowing, `Result<T, E>` + `?` error handling, no `.unwrap()` in production paths
- Guides async/concurrency (tokio, never holding `std::sync::Mutex` across `.await`)
- Selects patterns by domain: backend API, CLI, Tauri desktop, WASM frontend
- Runs a code-review checklist against critical anti-patterns before finalizing

## When to use

Writing new Rust applications, designing architecture, refactoring, implementing async/concurrency, integrating databases (SQLx/SeaORM/Diesel), configuring CI/CD, building with axum/actix-web/Tauri/WASM, or reviewing Rust code. Also triggers on `Cargo.toml`, `.rs` files, or mentions of borrow checker, lifetimes, or traits.

## What's inside

- [SKILL.md](SKILL.md) — core principles, agent workflow, ownership/borrowing, lifetimes/traits, error handling, async, observability, project structure, testing
- [ARCHITECTURE.md](ARCHITECTURE.md) — domain backends (axum, actix-web, Tauri, WASM), database paradigms (SQLx, SeaORM, Diesel), deployment
- [REVIEW.md](REVIEW.md) — critical anti-patterns and the full code-review checklist
- [SECURITY-PERF.md](SECURITY-PERF.md) — supply-chain auditing, unsafe constraints, performance
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/rust-engineering ~/.claude/skills/`
**Codex:** `cp -r skills/rust-engineering $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\rust-engineering "$env:USERPROFILE\.claude\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
