---
name: tauri-engineering
description: Use when building Tauri desktop or mobile apps, configuring tauri.conf.json, writing Tauri commands/plugins, setting up Tauri permissions/capabilities, debugging Webview issues, optimizing Tauri binary size, configuring Tauri auto-updates, or reviewing Tauri code — production-grade Tauri v2 engineering guidelines covering guest-host architecture, IPC commands, state management, ACL security, plugins, testing, performance optimization, auto-updates, and CI/CD. Also triggers on tauri.conf.json, tauri-plugin-*, or mentions of WRY/TAO/Webview2/WebKitGTK.
---

# Tauri Engineering

Strict operational guidelines for building, securing, and shipping Tauri v2 applications. For Rust-side patterns (ownership, error handling, async, testing), see [rust-engineering](../rust-engineering/SKILL.md).

## Architecture

- **Guest-host model**: multi-process — TAO for window management, WRY for rendering via OS-native Webview (not bundled Chromium).
- **No SSR**: configure frameworks for SPA or SSG mode. SvelteKit → `@sveltejs/adapter-static`.
- **Vite**: `strictPort: true`, mobile HMR via `TAURI_DEV_HOST`, build targets `chrome105` (Windows) / `safari13` (macOS/iOS).

## IPC & commands

- Custom Protocol (JSON-RPC styled) replaces JSON string injection in v2.
- Raw byte streaming via `tauri::ipc::Response` for large payloads — bypasses JSON serialization.
- Async commands can't accept `&str` or `State<'_, T>` — use owned types (`String`) or wrap in `Result`.
- Commands in `lib.rs` must not be `pub`; register with `tauri::generate_handler!`.

## State management

- Register with `app.manage()` during setup.
- Shared mutable state → `std::sync::Mutex` or `RwLock`.
- Async: use `std::sync::Mutex` unless guard held across `.await` → then `tokio::sync::Mutex`.

## Security

- **ACL**: define Permissions (commands + scopes) and Capabilities (map to windows/webviews). Identifiers: lowercase ASCII, max 116 chars.
- **Isolation Pattern**: required for high security — sandboxed `<iframe>`, AES-GCM encrypted IPC payloads.
- **CSP**: always enforce. Tauri calculates script hashes and appends nonces.
- **Filesystem**: `tauri-plugin-fs` enforces Base Directory containment. Block `../` traversal.
- **Shell**: pre-configure allowed processes, args, and paths in capabilities.

## Testing & performance

Testing checklist, binary optimization (`lto`, `codegen-units`, `strip`), cross-platform bundling (Linux/macOS/Windows), and CI/CD with `tauri-apps/tauri-action`: [TESTING-PERF.md](TESTING-PERF.md).

## Auto-updates & anti-patterns

Updater signature enforcement, key management, server response contracts, platform-specific deployment, and critical anti-patterns to avoid: [UPDATES-DEPLOY.md](UPDATES-DEPLOY.md).
