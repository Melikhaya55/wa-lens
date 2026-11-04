# wa-lens

**See inside your own WhatsApp Web data.** Export contacts, chats, message metadata, media and store inventories from **your own** browser profile into clean JSONL + an HTML report. Searchable, scriptable, zero-dependency, MIT.

> Own-data-only. This tool is for data you already have on your own machine (data portability: POPIA s14, GDPR Art. 20, CCPA, PIPL). Reading anyone else's account or device without authorization is illegal. See SECURITY.md.

## The gap this fills
Existing "WhatsApp reader/tracker" tools are closed-source, sketchy, and often spyware. There is no clean, open-source, MIT-licensed tool that simply exports **your own** WhatsApp Web browser storage in a documented, auditable way. wa-lens is that tool: readable code, no network calls, no telemetry, works fully offline.

## What it exports
- `summary.json` — profile path, idb files found, per-store row counts
- `<store>.jsonl` — one JSON record per row for known stores: `contact`, `chat`, `message`, `message-history`, `reactions`, `poll-votes`, `label`, `pinned-messages`, `group-metadata`, `participant`, `profile-pic-thumb`, … (store list auto-discovered from each idb `object_store` table; see docs/SCHEMA.md)
- `media/` — large binary blobs (photos/videos/docs/voice notes), named by sha256, referenced from the JSONL records
- `report.html` — human-readable report (i18n: en, xho, af, zh, es, fr, pt, ar)

## What it cannot do (truth first)
Message **bodies** are stored end-to-end encrypted at rest (records contain `$ciphertext`). Without the session keys from the logged-in browser session, plaintext bodies are not recoverable from the idb files alone. wa-lens exports all metadata, contacts, chat lists, media, filenames, timestamps, and any plaintext fields that WhatsApp Web itself stores. That is exactly what a data-portability export should contain.

## Install
```
pip install .          # or just run from source: python3 -m wa_lens
```
Requires Python ≥ 3.9. **No third-party dependencies.**

## Usage
```
wa-lens profiles                          # auto-detect WhatsApp Web storage on this machine
wa-lens export --profile <path> --out ./my-export
wa-lens search --export-dir ./my-export "regex"
wa-lens report --export-dir ./my-export --out report.html --lang en
```

## Works everywhere (RSA · USA · UK · EU · China · worldwide)
Profile auto-detection covers:
- **Linux**: Firefox (`~/.mozilla/firefox`), Chrome/Chromium/Brave/Edge (`~/.config/...`), ICE/SSB web-apps (`~/.local/share/ice/firefox/<App>`), flatpak apps (`~/.var/app/.../QtWebEngine/IndexedDB`, e.g. WhatSie), snap (`~/snap`)
- **macOS**: `~/Library/Application Support/{Firefox/Profiles, Google/Chrome, Microsoft Edge, BraveSoftware/Brave-Browser, Chromium}`
- **Windows**: `%APPDATA%\Mozilla\Firefox\Profiles`, `%LOCALAPPDATA%\{Google\Chrome, Microsoft\Edge, BraveSoftware}\...`

Report UI languages: English, isiXhosa, Afrikaans, 中文, Español, Français, Português, العربية. (Non-English strings are community drafts — PRs from native speakers welcome.)

## Verified against
Live WhatsApp Web browser profiles (Firefox/ICE web-app on Linux, WhatsApp Web 2026-10/11). The IndexedDB store schema was documented independently from real profiles — see **docs/SCHEMA.md** (SHA-256 digests of the inspected databases included).

## Roadmap
- [ ] Chromium-family idb (leveldb) reader — currently Firefox/QtWebEngine sqlite idb
- [ ] Decrypt bodies using keys extracted from the live session (own session only) — Pro
- [ ] Web UI for browsing exports — Pro
- [ ] Media recovery (deleted media carving) — Pro
- [ ] More stores: calls, newsletters, business profiles
- [ ] More languages

## Money (open core, MIT stays)
Core is free forever under MIT. Sustainable development is funded on top:
- **GitHub Sponsors** (see `.github/FUNDING.yml`) — [EXAMPLE — NOT CURRENT INCOME]
- **Polar.sh** — "wa-lens Pro" license keys (web UI, media recovery, session-key decryption for your own account) — license check via Polar API, keys never in the repo
- **Gumroad** — export-template packs + support bundles
- **Algora** — bounties on OSS issues
All figures are examples, not current income. Starting cost: [FREE — CONFIRMED ZERO COST].

## Contributing
PRs welcome: new browser/OS paths, store parsers, translations (native speakers only), tests. CI runs on Linux/macOS/Windows × Python 3.9–3.13.

## License
MIT — see LICENSE. © 2026 Melikhaya Cosbee Zaze.
