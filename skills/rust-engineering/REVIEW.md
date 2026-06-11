# Anti-Patterns & Code Review

## Anti-patterns

### Locks across await points

Do not hold `std::sync::Mutex` across `.await` — deadlocks or panics. If a lock must span `.await`, use `tokio::sync::Mutex`. Prefer restructuring to use message passing (channels).

### Stringly-typed interfaces

Never use raw `String` or `bool` to represent complex states or identifiers. Use enums and newtypes.

### N+1 query problems

Never emit sequential DB queries inside loops (especially SeaORM). Use `.find_with_related()` or batch queries.

### Ignoring graceful shutdown

Always intercept `SIGTERM`. Drain in-flight HTTP requests. Close database connections cleanly.

## Code review checklist

Run before finalizing any Rust output:

- [ ] Algebraic data types (enums/structs) make illegal states unrepresentable
- [ ] Ownership efficient (`&T` over `.clone()`, explicit lifetimes where useful)
- [ ] Error handling robust (`Result`, `?`) — no `.unwrap()` or panics in production paths
- [ ] CPU-bound tasks isolated from async event loop via `spawn_blocking`
- [ ] Concurrency safe — no standard locks held across `.await`
- [ ] Security tools satisfied (`cargo-audit`, `cargo-deny`, `clippy -- -D warnings`)
- [ ] Logs structured (JSON) and trace-correlated via `tracing` + OpenTelemetry
- [ ] Graceful shutdown and connection draining implemented

## Completion criteria

Generated/refactored code must: align with strict ownership rules, handle errors idiomatically without panicking, structure domains using type-driven design, separate async/CPU boundaries, and pass all lints + `cargo test`.
