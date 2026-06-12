# Auto-Updates & Deployment

## Built-in updater (`tauri-plugin-updater`)

- **Signature enforcement**: cryptographic signatures strictly required.
- **Key generation**: `tauri signer generate` creates ECDSA keys.
  - **Public key** → embed in `tauri.conf.json` statically.
  - **Private key** → CI env vars: `TAURI_PRIVATE_KEY` / `TAURI_KEY_PASSWORD`.
- **Server responses**:
  - `204 No Content` — no update available.
  - `200 OK` + JSON with `url`, `version`, `signature` — update available.
- **Windows exit hook**: Tauri force-quits before applying updates on Windows. Use `on_before_exit` to hook cleanup logic.

## Anti-patterns

### DevTools in production macOS builds

Enabling the `devtools` cargo feature in macOS release builds invokes private OS APIs → **guaranteed Apple App Store rejection**.

### Incorrect State type wrapping

Using `State<'_, AppState>` instead of `State<'_, Mutex<AppState>>` — compiler can't catch this mismatch → **runtime panic**.

### `Tauri-Custom-Header` in production

This HTTP header override is for development/testing only. Do not ship it.

### Vanilla dev server on untrusted networks

Lacks mutual authentication and encryption. Only use on trusted local networks.

## Source gaps

- **Mobile CI/CD**: `tauri-action` mobile support is in progress but not yet available. Manual config required.
- **Windows OV certificates**: the standard guide applies to OV certificates acquired before June 1, 2023. Post-2023 OV certs have different CA-mandated requirements not covered by the standard CLI integration.
