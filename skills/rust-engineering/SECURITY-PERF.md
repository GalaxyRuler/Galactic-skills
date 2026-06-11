# Security & Performance

## Supply chain auditing

- `cargo-audit` — block builds on known CVEs.
- `cargo-deny` — ban non-compliant licenses, duplicate crates.

## Unsafe Rust constraints

- Isolate `unsafe` to minimal, heavily documented modules.
- Obey aliasing rules (Stacked/Tree Borrows): never hold `&mut T` concurrently with any other ref to same memory.
- Validate with `Miri`, AddressSanitizer (ASan), ThreadSanitizer (TSan) in CI.

## Application hardening

- Ban unbounded recursion/memory features (e.g., `serde_json::unbounded_depth`).
- Wipe sensitive buffers with `zeroize`.

## Async workload routing

- IO-bound → `tokio::spawn` (standard async tasks).
- CPU-bound (crypto, sorting) → `tokio::task::spawn_blocking` or Rayon thread pool.
- Never starve the Tokio executor.

## Benchmarking

- `Criterion` (`cargo bench`) in `benches/` directory.
- `black_box` to prevent compiler over-optimization in micro-benchmarks.

## Memory efficiency

- `with_capacity()` when sizes known.
- `write!()` over `format!()` in hot paths.
- `SmallVec` / `ArrayVec` for predominantly small lists.
- Avoid allocations in hot loops.

## CI/CD deployment

- Multi-stage Dockerfiles + `cargo-chef` to cache dependency build layer.
- Static MUSL builds for highly concurrent deployments: override allocator with `jemalloc`.

## Linting

- `cargo clippy -- -D warnings` — treat all warnings as errors.
- `rustfmt` for consistent formatting.
