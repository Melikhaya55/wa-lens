# Security & responsible-use policy

wa-lens is an **own-data-only** tool (data portability: POPIA, GDPR Art. 20, CCPA, PIPL).

- Use it only on browser profiles **you own and are logged into**.
- Do not use it to read anyone else's messages, device, or account. That is illegal in most jurisdictions (incl. South Africa's POPIA and RICA, EU GDPR, US CFAA/ECPA, China PIPL/CSL) and violates WhatsApp's ToS.
- The tool makes **no network calls** and sends nothing anywhere (stdlib sqlite/json/pathlib only — verify: `grep -rn "import urllib\|requests\|socket" wa_lens/` returns nothing).
- Never commit real exports (JSONL/media) to any repo — `.gitignore` blocks `*.jsonl`, `media/`, `exports/` so they cannot be pushed by accident. Tests use synthetic fixtures only.
- Your exports stay on your machine. WhatsApp Web stores message bodies end-to-end-encrypted (`$ciphertext`) at rest; wa-lens does not and cannot decrypt them — exports contain metadata, contacts, media and ciphertext blobs only. Keep exports local, encrypt them at rest if you move them, delete them when done.
- Report vulnerabilities privately (GitHub security advisory or DM @Melikhaya55). Do not open public issues containing real personal data.
