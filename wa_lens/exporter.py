"""Export WhatsApp Web IndexedDB sqlite files to JSONL + media. Zero-dependency, stdlib only."""
import hashlib
import json
import re
import shutil
import sqlite3
import tempfile
from pathlib import Path

PRINTABLE = re.compile(r"[\x20-\x7e\u00c0-\u024f\u1e00-\u1eff]{6,}")

# Stores worth exporting (auto-discovered per idb; this is the allowlist of interesting ones).
INTERESTING = (
    "contact", "chat", "message", "message-history", "message-info", "reactions",
    "poll-votes", "label", "label-association", "label_sublist", "pinned-messages",
    "call-log", "profile-pic-thumb", "group-metadata", "participant", "favorite",
    "user-prefs", "business-profile", "newsletter-metadata", "sync-keys",
)


def printable(blob):
    if not isinstance(blob, (bytes, bytearray)):
        return ""
    b = bytes(blob)
    s = b.decode("utf-8", errors="ignore")
    s16 = b.decode("utf-16-le", errors="ignore")
    t = s if len(PRINTABLE.findall(s)) >= len(PRINTABLE.findall(s16)) else s16
    return " | ".join(PRINTABLE.findall(t))[:4000]


def copy_idb(src_dir, tmpdir):
    src = Path(src_dir)
    dst = Path(tmpdir)
    dst.mkdir(parents=True, exist_ok=True)
    n = 0
    for f in sorted(src.glob("*.sqlite*")):
        shutil.copy2(f, dst / f.name)
        n += 1
    return n


def export_store(con, sid, out_path, media_dir, max_rows):
    cur = con.execute(
        "select key, data from object_data where object_store_id=?", (sid,)
    )
    count = 0
    with open(out_path, "w", encoding="utf-8") as fh:
        while count < max_rows:
            row = cur.fetchone()
            if row is None:
                break
            count += 1
            key, blob = row
            text = printable(blob)
            rec = {
                "key": key.hex() if isinstance(key, (bytes, bytearray)) else str(key),
                "size": len(blob) if isinstance(blob, (bytes, bytearray)) else 0,
                "ciphertext": "$ciphertext" in text,
                "text": text[:1000],
            }
            if (
                isinstance(blob, (bytes, bytearray))
                and len(blob) > 32768
                and "$ciphertext" not in text
                and len(text) < len(blob) // 4
            ):
                h = hashlib.sha256(blob).hexdigest()[:16]
                (media_dir / h).write_bytes(blob)
                rec["media_file"] = h
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return count


def locate_idb(profile_dir):
    """Accept the idb dir, a web.whatsapp.com storage dir, or a browser profile root; return the idb dir."""
    p = Path(profile_dir)
    if p.is_dir() and "web.whatsapp.com" in p.name and list(p.glob("*.sqlite*")):
        return p
    if p.is_dir() and p.name == "idb" and list(p.glob("*.sqlite*")):
        return p
    for cand in p.rglob("*web.whatsapp.com*"):
        if not cand.is_dir():
            continue
        if list(cand.glob("*.sqlite*")):
            return cand
        idb = cand / "idb"
        if idb.is_dir() and list(idb.glob("*.sqlite*")):
            return idb
    return p


def export(profile_dir, out_dir, max_rows=200000):
    """Copy idb files from profile_dir, then export interesting stores to out_dir. Returns summary dict."""
    profile_dir = locate_idb(profile_dir)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    media = out / "media"
    media.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        nfiles = copy_idb(profile_dir, tmp)
        summary = {"profile": str(profile_dir), "idb_files_copied": nfiles, "stores": {}}
        for f in sorted(Path(tmp).glob("*.sqlite")):
            try:
                con = sqlite3.connect(str(f))  # plain path: uri mode breaks on '%' in filenames
            except sqlite3.Error:
                continue
            try:
                smap = {r[0]: r[1] for r in con.execute("select id,name from object_store")}
            except sqlite3.Error:
                smap = {}
            for sid, name in smap.items():
                if name not in INTERESTING:
                    continue
                p = out / (name.replace("/", "_") + ".jsonl")
                cnt = export_store(con, sid, p, media, max_rows)
                summary["stores"][name] = cnt
            con.close()
    (out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    return summary
