---
name: rust-engineering
description: Production-grade Rust engineering guidelines — ownership, type-driven design, error handling, async/concurrency, testing, security, and performance. Use when writing new Rust applications, designing Rust architecture, refactoring Rust code, implementing async/concurrency, integrating databases (SQLx/SeaORM/Diesel), configuring Rust CI/CD pipelines, building with axum/actix-web/Tauri/WASM, or performing Rust code reviews. Also triggers on Cargo.toml, .rs files, or mentions of borrow checker, lifetimes, or traits.
---

# Rust Engineering

Strict operational guidelines for generating, refactoring, and reviewing production Rust code.

## Core principles

1. **Make illegal states unrepresentable** — ADTs (enums/structs) + Typestate eliminate invalid states at compile time
2. **Explicit over implicit** — `Result<T, E>` everywhere, no `.unwrap()` in production paths
3. **Pragmatism (KISS/YAGNI)** — simplest correct solution wins; no premature trait objects
4. **Zero-cost abstractions** — monomorphized generics + ownership = safety without GC overhead

## Agent workflow

1. **Analyze context** — determine domain (backend API, CLI, Tauri desktop, WASM frontend) → select patterns
2. **Enforce type design** — scaffold data model with Newtypes and Enums
3. **Implement** — strict ownership, borrowing, async concurrency rules
4. **Validate & secure** — error propagation, structured logging, no unbounded/unsafe vulnerabilities
5. **Review** — run code review checklist before finalizing. See [REVIEW.md](REVIEW.md)

## Ownership & borrowing

- Prefer `&T` over `.clone()`. Clone only when ownership transfer unavoidable.
- Tree-like ownership hierarchies; avoid circular graphs.
- `Cow<'a, T>` for conditional ownership when mutation is rare.
- `Rc<T>` single-threaded, `Arc<T>` multi-threaded shared ownership.
- `RefCell<T>` single-threaded / `Mutex<T>`+`RwLock<T>` multi-threaded interior mutability.

## Lifetimes & traits

- Rely on elision rules. Explicit annotations: short lowercase (`'a`, `'ctx`).
- Derive `Debug`, `Clone`, `PartialEq`, `Eq`, `Default` on public types.
- Prefer `impl Trait` / generics (static dispatch) over `Box<dyn Trait>` unless heterogeneous collections required.

## Error handling

- `Result<T, E>` + `?` operator for all fallible operations.
- `thiserror` for library error enums, `anyhow` for application context.
- `.unwrap()`/`.expect()` only for statically proven invariants (compiler blind spots).

## Async / concurrency

- IO-bound → `tokio::spawn`. CPU-bound → `tokio::task::spawn_blocking` or Rayon.
- **Never** hold `std::sync::Mutex` across `.await`. Use `tokio::sync::Mutex` or channels.

## Observability

- `tracing` crate for structured, span-based instrumentation. `#[instrument]` on async functions.
- `tracing-subscriber` with `fmt` layer (dev) and `json` layer (prod). Filter via `RUST_LOG` env var.
- Pair with `tracing-opentelemetry` for distributed trace export when needed.

## Project structure

- `main.rs` minimal entry point, `lib.rs` core domain logic. Cargo Workspaces for multi-crate.
- Newtype pattern (`struct UserId(u64)`) for domain boundaries.
- Typestate pattern for state-machine transitions enforced at compile time.

## Testing

- `#[test]` in `#[cfg(test)]` module for unit tests. `tests/` dir for integration tests.
- `cargo-nextest` for parallel execution. `mockall`/`wiremock` for mocking. `proptest` for property-based testing. `cargo-fuzz` for untrusted input.

## Architecture, security, performance

Domain-specific backends (axum, actix-web, Tauri, WASM), database paradigms (SQLx, SeaORM, Diesel), supply-chain auditing, unsafe constraints, deployment: [ARCHITECTURE.md](ARCHITECTURE.md), [SECURITY-PERF.md](SECURITY-PERF.md).

For Tauri desktop/mobile apps, see the [tauri-engineering](../tauri-engineering/SKILL.md) skill — it covers guest-host architecture, IPC commands, ACL security, and binary optimization.

## Anti-patterns & review checklist

Critical anti-patterns (locks across await, stringly-typed interfaces, N+1 queries, missing graceful shutdown) and the full review checklist: [REVIEW.md](REVIEW.md).
