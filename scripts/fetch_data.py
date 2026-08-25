#!/usr/bin/env python3
"""Fetch the skill's bulk data into data/ (gitignored). Stdlib only.

Usage:
  python3 scripts/fetch_data.py krcg            # cards + TWDA (static.krcg.org, v4 format)
  python3 scripts/fetch_data.py usenet          # usenet mbox archives (GitHub release assets)
  python3 scripts/fetch_data.py usenet --from-local DIR   # copy zips from a local directory
  python3 scripts/fetch_data.py all
  python3 scripts/fetch_data.py check           # staleness report, no download
"""

import argparse
import datetime
import json
import pathlib
import shutil
import sys
import urllib.request
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
KRCG_DIR = ROOT / "data" / "krcg"
USENET_DIR = ROOT / "data" / "usenet"
STAMP = KRCG_DIR / "stamp.json"

# v4 format: matches api.krcg.org card/deck object shapes (see wiki/design.md).
KRCG_BASE = "https://static.krcg.org/data/v4/"
KRCG_FILES = ["vtes.json", "twda.json"]

# Durable home of the usenet archives: release assets on this skill's own repo
# (the mboxes have no reliable canonical source online; see SOURCES.md).
USENET_RELEASE = "https://github.com/vtes-biased/vtes-skill/releases/download/usenet-archives/"
USENET_ZIPS = ["rec.games.deckmaster.mbox.zip", "rec.games.trading-cards.jyhad.mbox.zip"]

STALE_DAYS = 30


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def _load_stamp() -> dict:
    if STAMP.exists():
        return json.loads(STAMP.read_text())
    return {}


def fetch_krcg() -> None:
    KRCG_DIR.mkdir(parents=True, exist_ok=True)
    stamp = _load_stamp()
    for name in KRCG_FILES:
        url = KRCG_BASE + name
        print(f"fetching {url} ...", file=sys.stderr)
        with urllib.request.urlopen(url) as resp:
            (KRCG_DIR / name).write_bytes(resp.read())
            stamp[name] = {
                "fetched_at": _now(),
                "last_modified": resp.headers.get("Last-Modified", ""),
            }
    STAMP.write_text(json.dumps(stamp, indent=2))
    print(f"done: {', '.join(KRCG_FILES)} -> {KRCG_DIR}", file=sys.stderr)


def fetch_usenet(from_local: str | None) -> None:
    USENET_DIR.mkdir(parents=True, exist_ok=True)
    for name in USENET_ZIPS:
        mbox = USENET_DIR / name.removesuffix(".zip")
        if mbox.exists():
            print(f"already present: {mbox.name}", file=sys.stderr)
            continue
        zip_path = USENET_DIR / name
        if from_local:
            src = pathlib.Path(from_local).expanduser() / name
            print(f"copying {src} ...", file=sys.stderr)
            shutil.copy(src, zip_path)
        else:
            url = USENET_RELEASE + name
            print(f"downloading {url} (large) ...", file=sys.stderr)
            with urllib.request.urlopen(url) as resp, open(zip_path, "wb") as out:
                shutil.copyfileobj(resp, out)
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(USENET_DIR)
        zip_path.unlink()
        print(f"extracted {mbox.name}", file=sys.stderr)


def check() -> int:
    stale = False
    stamp = _load_stamp()
    for name in KRCG_FILES:
        path = KRCG_DIR / name
        if not path.exists():
            print(f"MISSING  {name} — run: python3 scripts/fetch_data.py krcg")
            stale = True
            continue
        fetched = stamp.get(name, {}).get("fetched_at")
        age = None
        if fetched:
            age = (
                datetime.datetime.now(datetime.timezone.utc)
                - datetime.datetime.fromisoformat(fetched)
            ).days
        try:
            req = urllib.request.Request(KRCG_BASE + name, method="HEAD")
            with urllib.request.urlopen(req, timeout=10) as resp:
                upstream = resp.headers.get("Last-Modified", "")
        except OSError:
            upstream = "(offline)"
        local = stamp.get(name, {}).get("last_modified", "?")
        status = "OK" if upstream in (local, "(offline)") else "BEHIND"
        if age is not None and age > STALE_DAYS:
            status = f"STALE ({age}d old)"
        if status != "OK":
            stale = True
        print(f"{status:14} {name}  local={local}  upstream={upstream}")
    for name in USENET_ZIPS:
        mbox = USENET_DIR / name.removesuffix(".zip")
        print(f"{'OK' if mbox.exists() else 'MISSING':14} {mbox.name} (static archive)")
    return 1 if stale else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("what", choices=["krcg", "usenet", "all", "check"])
    parser.add_argument("--from-local", help="local dir holding the usenet mbox zips")
    args = parser.parse_args()
    if args.what == "check":
        return check()
    if args.what in ("krcg", "all"):
        fetch_krcg()
    if args.what in ("usenet", "all"):
        fetch_usenet(args.from_local)
    return 0


if __name__ == "__main__":
    sys.exit(main())
