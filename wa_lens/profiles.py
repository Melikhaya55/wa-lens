"""Cross-browser, cross-OS detection of WhatsApp Web storage directories."""
import os
import sys
from pathlib import Path

MAX_HITS = 300


def candidate_roots():
    home = Path.home()
    roots = []
    if sys.platform.startswith("linux"):
        roots += [
            home / ".mozilla/firefox",
            home / ".config/google-chrome",
            home / ".config/chromium",
            home / ".config/BraveSoftware/Brave-Browser",
            home / ".config/microsoft-edge",
            home / ".local/share/ice/firefox",   # ICE/SSB web-apps (e.g. WhatsApp)
            home / ".var/app",                    # flatpak apps (e.g. WhatSie)
            home / "snap",
        ]
    elif sys.platform == "darwin":
        app = home / "Library/Application Support"
        roots += [
            app / "Firefox/Profiles",
            app / "Google/Chrome",
            app / "Microsoft Edge",
            app / "BraveSoftware/Brave-Browser",
            app / "Chromium",
        ]
    elif sys.platform == "win32":
        appdata = os.environ.get("APPDATA", "")
        local = os.environ.get("LOCALAPPDATA", "")
        roots += [
            Path(appdata) / r"Mozilla\Firefox\Profiles",
            Path(local) / r"Google\Chrome\User Data",
            Path(local) / r"Microsoft\Edge\User Data",
            Path(local) / r"BraveSoftware\Brave-Browser\User Data",
            Path(local) / r"Chromium\User Data",
        ]
    return [r for r in roots if r.exists()]


def find_whatsapp_stores():
    """Return directories whose path mentions web.whatsapp.com and look like idb/storage dirs."""
    hits = []
    for root in candidate_roots():
        try:
            for p in root.rglob("*web.whatsapp.com*"):
                s = str(p)
                if p.is_dir() and ("idb" in s or "IndexedDB" in s or "storage" in s):
                    hits.append(p)
                    if len(hits) >= MAX_HITS:
                        return hits
        except (PermissionError, OSError):
            continue
    return hits
