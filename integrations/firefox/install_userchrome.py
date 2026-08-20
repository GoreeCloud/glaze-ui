#!/usr/bin/env python3
"""Install, update, or remove the optional Glaze UI userChrome.css safely.

The target Firefox profile must be supplied explicitly. This tool never guesses or
selects a profile automatically.
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "userchrome" / "userChrome.css"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_profile(path: Path) -> Path:
    profile = path.expanduser().resolve()
    if not profile.is_dir():
        raise SystemExit(f"Firefox profile does not exist or is not a directory: {profile}")
    markers = ("prefs.js", "compatibility.ini", "times.json", "places.sqlite")
    if not any((profile / marker).exists() for marker in markers):
        raise SystemExit(
            "Target does not look like a Firefox profile. Expected at least one of: "
            + ", ".join(markers)
        )
    return profile


def backup_existing(target: Path) -> Path | None:
    if not target.exists():
        return None
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = target.with_name(f"userChrome.css.backup-{stamp}")
    shutil.copy2(target, backup)
    return backup


def install(profile: Path) -> None:
    chrome_dir = profile / "chrome"
    chrome_dir.mkdir(mode=0o700, exist_ok=True)
    target = chrome_dir / "userChrome.css"
    backup = backup_existing(target)
    shutil.copy2(SOURCE, target)
    target.chmod(0o600)
    print(f"Installed: {target}")
    print(f"SHA-256: {sha256(target)}")
    if backup:
        print(f"Backup: {backup}")
    print(
        "Firefox must also have toolkit.legacyUserProfileCustomizations.stylesheets=true. "
        "This tool intentionally does not modify Firefox preferences."
    )


def remove(profile: Path) -> None:
    target = profile / "chrome" / "userChrome.css"
    if not target.exists():
        print(f"Nothing to remove: {target}")
        return
    backup = backup_existing(target)
    target.unlink()
    print(f"Removed: {target}")
    if backup:
        print(f"Backup retained: {backup}")


def verify(profile: Path) -> None:
    target = profile / "chrome" / "userChrome.css"
    if not target.is_file():
        raise SystemExit(f"userChrome.css is not installed in: {profile}")
    source_digest = sha256(SOURCE)
    target_digest = sha256(target)
    print(f"Source SHA-256:    {source_digest}")
    print(f"Installed SHA-256: {target_digest}")
    if source_digest != target_digest:
        raise SystemExit("Installed userChrome.css differs from canonical source.")
    print("Installed userChrome.css matches canonical source.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True, type=Path, help="Exact Firefox profile directory")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--install", action="store_true")
    action.add_argument("--remove", action="store_true")
    action.add_argument("--verify", action="store_true")
    args = parser.parse_args()

    profile = require_profile(args.profile)
    if args.install:
        install(profile)
    elif args.remove:
        remove(profile)
    else:
        verify(profile)


if __name__ == "__main__":
    main()
