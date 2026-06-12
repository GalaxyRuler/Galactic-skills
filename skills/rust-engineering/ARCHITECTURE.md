# Architecture

## Project structure

- Split: `main.rs` (minimal entry point) + `lib.rs` (core domain logic) for maximum testability.
- Use Cargo Workspaces for large, multi-crate projects.

## Type-driven architecture

- **Newtype pattern**: `struct UserId(u64)` enforces domain boundaries, prevents primitive obsession.
- **Typestate pattern**: encode state-machine transitions into the type system. Invalid operations fail compilation.

## Backend & APIs

- `axum` or `actix-web` with `tokio` for HTTP services.
- Database connection pools (`PgPool`) injected via application state extractors.
- Graceful shutdown: intercept `SIGTERM`, drain in-flight requests, close DB connections.

## Databases

Three major paradigms — choose per project needs:

| Crate | Style | Key trait |
|-------|-------|-----------|
| **SQLx** | Async, compile-time validated raw SQL | Requires `DATABASE_URL` in CI |
| **SeaORM** | Async ActiveRecord abstractions | `.find_with_related()` for eager loading |
| **Diesel** | Mature type-safe DSL (sync; `diesel-async` available) | Strong compile-time query checking |

Avoid N+1: never emit sequential DB queries inside loops — batch or eager-load.

## WebAssembly (WASM)

- Offload CPU-bound work (crypto, image rendering) to Rust via `wasm-bindgen`; let JS manage DOM.
- Full Rust frontend: Leptos, Dioxus, or Yew.

## Desktop (Tauri v2)

- Strict separation: JS/TS frontend, Rust backend.
- Communicate via IPC Commands (`invoke()`) and Events.
- Never expose raw filesystem or process access to the frontend.
- Full Tauri guide: [tauri-engineering](../tauri-engineering/SKILL.md).

## Edge / Serverless (Cloudflare Workers)

- Target `wasm32-unknown-unknown`. Use `worker` crate for bindings.
- Keep binary size minimal — no `std::net`, no `tokio`. Use `worker::Fetch` for HTTP.
- `wrangler dev` for local testing, `wrangler deploy` for publish.
