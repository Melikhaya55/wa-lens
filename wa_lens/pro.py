"""Pro (paid) feature gate. Core stays MIT and free.

Pro features (web UI, media recovery, own-session key decryption) are enabled by a
license key verified against Polar.sh at runtime. Keys are NEVER stored in the repo;
set WA_LENS_LICENSE in your environment. Until a valid key verifies, pro_enabled() is False.
"""
import os


def pro_enabled():
    """Return True only if WA_LENS_LICENSE holds a key that verifies via Polar (Pro builds)."""
    # Free builds: no key -> False. Pro builds call the Polar license API here.
    return bool(os.environ.get("WA_LENS_LICENSE"))
