"""Regex search across an export directory's JSONL files."""
import re
from pathlib import Path


def search(export_dir, pattern, limit=200):
    rx = re.compile(pattern, re.I)
    n = 0
    for f in sorted(Path(export_dir).glob("*.jsonl")):
        with open(f, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if rx.search(line):
                    n += 1
                    print(f.name + ": " + line.strip()[:500])
                    if n >= limit:
                        return n
    return n
