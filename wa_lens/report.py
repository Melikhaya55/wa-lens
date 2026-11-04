"""Minimal self-contained HTML report from an export directory."""
import json
from pathlib import Path

from .i18n import STR


def build(export_dir, out, lang="en"):
    s = json.loads((Path(export_dir) / "summary.json").read_text(encoding="utf-8"))
    t = STR.get(lang, STR["en"])
    rows = "".join(
        "<tr><td>%s</td><td>%d</td></tr>" % (k, v)
        for k, v in sorted(s.get("stores", {}).items())
    )
    html = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'><title>wa-lens</title>"
        "<style>body{font-family:sans-serif;background:#0a0908;color:#f3ead8;max-width:900px;"
        "margin:40px auto;padding:0 20px}td{padding:4px 12px;border-bottom:1px solid #333}"
        "h1{color:#e8c766}</style></head><body>"
        "<h1>%s</h1><p>%s</p><table>%s</table><p>%s</p></body></html>"
        % (
            t["report_title"],
            t["profile"] % s.get("profile", "?"),
            rows,
            t["own_data_notice"],
        )
    )
    Path(out).write_text(html, encoding="utf-8")
