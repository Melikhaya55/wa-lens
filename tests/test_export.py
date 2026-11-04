"""Tests use a synthetic fixture only — never real user data."""
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from wa_lens import exporter  # noqa: E402


def make_profile(root):
    idb = root / "storage/default/https+++web.whatsapp.com/idb"
    idb.mkdir(parents=True)
    db = idb / "1test.sqlite"
    con = sqlite3.connect(db)
    con.executescript(
        """
        CREATE TABLE object_store(id INTEGER PRIMARY KEY, auto_increment INTEGER NOT NULL DEFAULT 0, name TEXT NOT NULL, key_path TEXT);
        CREATE TABLE object_data(object_store_id INTEGER NOT NULL, key BLOB NOT NULL, index_data_values BLOB DEFAULT NULL, file_ids TEXT, data BLOB NOT NULL, PRIMARY KEY(object_store_id, key)) WITHOUT ROWID;
        INSERT INTO object_store VALUES (1,0,'message',NULL),(2,0,'contact',NULL);
        """
    )
    con.execute(
        "INSERT INTO object_data VALUES (1, ?, NULL, NULL, ?)",
        (b"chat1_msg1", b"\x00\x01hello world this is a test message body"),
    )
    con.execute(
        "INSERT INTO object_data VALUES (2, ?, NULL, NULL, ?)",
        (b"27123@s.whatsapp.net", b"Contact Name Test Person"),
    )
    con.commit()
    con.close()


class ExportTest(unittest.TestCase):
    def test_export_synthetic(self):
        with tempfile.TemporaryDirectory() as td:
            prof = Path(td) / "profile"
            make_profile(prof)
            out = Path(td) / "out"
            s = exporter.export(str(prof), str(out))  # profile root -> auto-locates idb
            self.assertEqual(s["stores"].get("message"), 1)
            self.assertEqual(s["stores"].get("contact"), 1)
            line = (out / "message.jsonl").read_text(encoding="utf-8").strip()
            self.assertIn("hello world", line)
            summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["idb_files_copied"], 1)

    def test_search(self):
        from wa_lens import search as sea

        with tempfile.TemporaryDirectory() as td:
            prof = Path(td) / "profile"
            make_profile(prof)
            out = Path(td) / "out"
            exporter.export(str(prof), str(out))
            n = sea.search(str(out), "test person", limit=10)
            self.assertGreaterEqual(n, 1)


if __name__ == "__main__":
    unittest.main()
