"""CLI entry point. Zero-dependency."""
import argparse
import json

from . import exporter, profiles as prof, report as rep, search as sea
from .i18n import LANGS, STR


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="wa-lens",
        description="Export and search YOUR OWN WhatsApp Web browser data. Own-data-only. MIT.",
    )
    ap.add_argument("--lang", default="en", choices=sorted(LANGS), help="UI language for report/search output")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("profiles", help="detect local browser profiles with WhatsApp Web storage")

    pe = sub.add_parser("export", help="export a profile's WhatsApp Web idb to a directory")
    pe.add_argument("--profile", required=True, help="idb dir, e.g. .../storage/default/https+++web.whatsapp.com/idb")
    pe.add_argument("--out", required=True, help="output directory")
    pe.add_argument("--max-rows", type=int, default=200000, help="cap rows per store")

    ps = sub.add_parser("search", help="regex search across an export")
    ps.add_argument("--export-dir", required=True)
    ps.add_argument("pattern")

    pr = sub.add_parser("report", help="build a self-contained HTML report from an export")
    pr.add_argument("--export-dir", required=True)
    pr.add_argument("--out", default="report.html")

    args = ap.parse_args(argv)
    t = STR.get(args.lang, STR["en"])

    if args.cmd == "profiles":
        hits = prof.find_whatsapp_stores()
        for h in hits:
            print(h)
        print(t["profiles_found"] % len(hits))
        return 0
    if args.cmd == "export":
        s = exporter.export(args.profile, args.out, args.max_rows)
        print(json.dumps(s, indent=2, ensure_ascii=False)[:6000])
        return 0
    if args.cmd == "search":
        n = sea.search(args.export_dir, args.pattern)
        print(t["matches"] % n)
        return 0
    if args.cmd == "report":
        rep.build(args.export_dir, args.out, args.lang)
        print(args.out)
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
