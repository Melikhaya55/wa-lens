# WhatsApp Web IndexedDB schema (observed 2026-11-04/05)

Documented independently from live browser profiles (offline copies of the profile's IndexedDB). No third-party tooling claims — just what the files contain.

## Container format (Firefox-family IndexedDB)
Each site gets `storage/default/https+++<site>/idb/*.sqlite` (+`-wal`/`-shm`). Tables:
- `database(name TEXT PK, origin, version, ...)` WITHOUT ROWID
- `object_store(id INTEGER PK, auto_increment, name TEXT, key_path TEXT)`
- `object_store_index(...)`, `index_data(...)`, `unique_index_data(...)` WITHOUT ROWID
- `object_data(object_store_id, key BLOB, index_data_values, file_ids TEXT, data BLOB)` WITHOUT ROWID, PK (object_store_id, key)
- `file(id, refcount)` + refcount triggers

## Observed WhatsApp object stores (80+ sampled)
`chat`, `contact`, `message`, `message-history`, `message-info`, `reactions`, `poll-votes`, `label`, `label-association`, `label_sublist`, `pinned-messages`, `group-metadata`, `participant`, `profile-pic-thumb`, `sync-keys`, `encrypted-mutations`, `pending-mutations`, `device-list`, `blocklist`, `optoutlist`, `favorite`, `favorite-stickers`, `recent-stickers`, `quick-reply`, `user-prefs`, `business-profile`, `newsletter-metadata`, `newsletter-polls-votes`, `newsletter-reactions`, `event-responses`, `comments`, `history-sync-notification`, `active-message-ranges`, `collection-version`, `agent`, `cart`, `poll-votes`, `ctwa-suggestion`, and more.

## Inspected database digests (SHA-256)
- 7,553,024 bytes: `446dc1d02ae5de8b6dc7847a3827a1e1926b703fdc89642d39e98891de966441`
- 117,809,152 bytes: `175dad5816306718d762d5d3ce6e3b214436eda6d88e6f967941aff1a8dea183`

## Key findings
- `message` rows carry `$ciphertext` bodies: message bodies are end-to-end encrypted at rest. Plaintext present: chat ids, `*.s.whatsapp.net` ids, media `filename`/`mimetype`/sizes, timestamps, types, fromMe flags.
- `contact` rows hold display/push names keyed by phone id (e.g. `27XXXXXXXXX@s.whatsapp.net`).
- Media blobs live in `object_data.data` (with `file_ids` refs) and in the browser HTTP cache.
- Chromium-family clients (e.g. flatpak WhatSie) store the same site as leveldb at `.../QtWebEngine/IndexedDB/https_web.whatsapp.com_0.indexeddb.leveldb` — wa-lens v0.1 reads the sqlite variant; leveldb reader is on the roadmap.
