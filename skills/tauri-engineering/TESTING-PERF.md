# Testing & Performance

## Testing checklist

- [ ] **E2E**: WebDriver protocols (WebdriverIO/Selenium) with `tauri-driver`
- [ ] **Headless CI**: wrap Linux runs in `xvfb-run` for virtual display
- [ ] **Frontend unit tests**: `@tauri-apps/api/mocks` (`mockIPC`, `mockWindows`) — test without Rust backend
- [ ] **Debug builds**: `tauri build --debug` leaves devtools enabled in compiled bundle
- [ ] **WebView Inspector**: Ctrl+Shift+I / Cmd+Option+I

## Binary size optimization

`Cargo.toml` release profile:

```toml
[profile.release]
codegen-units = 1
lto = true
opt-level = "s"
panic = "abort"
strip = true
```

Asset optimization: avoid custom fonts when possible; use `webp`, `webm`, SVG.

## Cross-platform bundling

### Linux

- Target `webkit2gtk-4.1` baseline (Ubuntu 22.04+).
- ARM cross-compilation (`aarch64`): install matching `gcc` linkers, set `PKG_CONFIG_SYSROOT_DIR`.

### macOS

- `.app` + `.dmg` formats.
- Code signing: Developer ID Application certificate (`.p12` base64 for CI) + Apple Notary Service.

### Windows

- NSIS (`.exe`) or WiX (`.msi`).
- `installMode: "passive"` for silent progress-bar-only updates.

## CI/CD

Use `tauri-apps/tauri-action` on GitHub Actions — automates Node/Rust setup, system deps, compilation, signing, and GitHub Release generation.

**Mobile gap**: `tauri-action` does not yet support mobile builds (.apk/.ipa). Mobile requires separate manual config or custom actions bridging `tauri ios build` / `tauri android build`.
