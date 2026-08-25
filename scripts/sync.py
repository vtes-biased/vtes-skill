#!/usr/bin/env python3
"""Sync-as-ingress against the upstream repos (wiki/design.md, decision 2). Stdlib + git.

Usage:
  python3 scripts/sync.py status [--offline]   # refresh upstream caches, report drift (exit 1 if any)
  python3 scripts/sync.py apply [name ...]     # no args: copy all changed mechanical files.
                                               # curated/watch entries must be named explicitly,
                                               # and only AFTER their change has been merged/assessed.

File modes (manifest below):
  copy    — verbatim-carried, no local delta: status diffs upstream vs the embarked file;
            apply overwrites the embarked file.
  curated — verbatim-carried WITH a sanctioned local delta (see SOURCES.md): status diffs
            upstream vs the committed snapshot (scripts/sync_snapshots/), so the sanctioned
            delta stays invisible; merge upstream changes into the embarked file BY HAND
            FIRST, then apply (refreshes the snapshot only).
  watch   — not embarked: upstream changes prompt revisiting synthesized files (the note says
            which); assess/update them first, then apply (refreshes the snapshot only).

After applying anything: update SOURCES.md with the new upstream commits printed by status.
"""

import argparse
import difflib
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "upstreams"
SNAPSHOTS = ROOT / "scripts" / "sync_snapshots"

UPSTREAMS = {
    "vtes-advanced-rules": {
        "url": "https://github.com/vtes-biased/vtes-advanced-rules.git",
        "submodules": True,
    },
    "codex-of-the-damned": {
        "url": "https://github.com/lionel-panhaleux/codex-of-the-damned.git",
        "submodules": False,
    },
}

# (upstream, src path in upstream, dst path in this repo or None, mode, note)
MANIFEST = [
    ("vtes-advanced-rules", "rulebook2024/content.md",
     "references/rules/rulebook.md", "copy", ""),
    ("vtes-advanced-rules", "docs/advanced-rules.md",
     "references/rules/advanced-rules.md", "copy", ""),
    ("vtes-advanced-rules", ".claude/references/rulemonger/canon.md",
     "references/rules/rulings-canon.md", "copy", ""),
    ("vtes-advanced-rules", "vtes-rulings/rulings/rulings.yaml",
     "references/rules/rulings/rulings.yaml", "copy", ""),
    ("vtes-advanced-rules", "vtes-rulings/rulings/groups.yaml",
     "references/rules/rulings/groups.yaml", "copy", ""),
    ("vtes-advanced-rules", "vtes-rulings/rulings/references.yaml",
     "references/rules/rulings/references.yaml", "copy", ""),
    ("codex-of-the-damned", ".claude/references/strategist/calibration.md",
     "references/strategy/calibration-lessons.md", "copy", ""),
    ("codex-of-the-damned", ".claude/references/strategist/meta-by-year.md",
     "references/strategy/meta-by-year.md", "copy", ""),
    ("codex-of-the-damned", ".claude/references/strategist/card-changes-history.md",
     "references/strategy/card-changes-history.md", "copy", ""),
    ("codex-of-the-damned", ".claude/skills/twda/data/classification.json",
     "references/strategy/classification.json", "copy", ""),
    ("codex-of-the-damned", ".claude/references/strategist/modules.md",
     "references/strategy/modules.md", "curated",
     "sanctioned local delta: canonized header (SOURCES.md). Merge the upstream change into "
     "the dst by hand, keeping the delta — then `apply modules.md` to refresh the snapshot."),
    ("codex-of-the-damned", ".claude/agents/strategist.md",
     None, "watch",
     "revisit references/strategy/theory.md (theory, golden rules, procedures) and "
     "SKILL.md's operating rules / strategic frame — then `apply strategist.md`."),
    ("vtes-advanced-rules", ".claude/agents/rulemonger.md",
     None, "watch",
     "revisit SKILL.md operating rule 2 (authority hierarchy) and the rules routing table — "
     "then `apply rulemonger.md`."),
]


def _git(*args: str, cwd: pathlib.Path | None = None) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
    ).stdout.strip()


def _refresh_caches(offline: bool) -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    for name, spec in UPSTREAMS.items():
        path = CACHE / name
        if offline:
            if not path.exists():
                sys.exit(f"--offline but no cache for {name}; run without --offline first")
            print(f"(offline: using cached {name})", file=sys.stderr)
            continue
        if not path.exists():
            print(f"cloning {spec['url']} ...", file=sys.stderr)
            cmd = ["clone", "--depth", "1", spec["url"], str(path)]
            if spec["submodules"]:
                cmd[1:1] = ["--recurse-submodules", "--shallow-submodules"]
            _git(*cmd)
        else:
            print(f"refreshing {name} ...", file=sys.stderr)
            _git("fetch", "--depth", "1", "origin", "HEAD", cwd=path)
            _git("reset", "--hard", "FETCH_HEAD", cwd=path)
            if spec["submodules"]:
                _git("submodule", "update", "--init", "--depth", "1", cwd=path)


def _entry_name(entry) -> str:
    _up, src, dst, _mode, _note = entry
    return pathlib.Path(dst if dst else src).name


def _baseline_path(entry) -> pathlib.Path:
    _up, src, dst, mode, _note = entry
    if mode == "copy":
        return ROOT / dst
    return SNAPSHOTS / _entry_name(entry)


def _upstream_path(entry) -> pathlib.Path:
    up, src, _dst, _mode, _note = entry
    return CACHE / up / src


def _changed_entries():
    changed = []
    for entry in MANIFEST:
        upstream = _upstream_path(entry)
        baseline = _baseline_path(entry)
        if not upstream.exists():
            sys.exit(f"upstream file vanished: {upstream} — adjudicate before syncing")
        if not baseline.exists() or upstream.read_bytes() != baseline.read_bytes():
            changed.append(entry)
    return changed


def cmd_status(args) -> int:
    _refresh_caches(args.offline)
    changed = _changed_entries()
    for entry in MANIFEST:
        up, src, dst, mode, note = entry
        name = _entry_name(entry)
        if entry not in changed:
            print(f"IN-SYNC          {mode:7} {name}")
            continue
        print(f"UPSTREAM-CHANGED {mode:7} {name}   [{up}/{src}]")
        if note:
            print(f"    -> {note}")
        baseline = _baseline_path(entry)
        old = baseline.read_text().splitlines() if baseline.exists() else []
        new = _upstream_path(entry).read_text(errors="replace").splitlines()
        for line in difflib.unified_diff(old, new, str(baseline.relative_to(ROOT)),
                                         f"{up}/{src}", lineterm="", n=2):
            print("    " + line)
    print("\nupstream heads (for SOURCES.md once applied):")
    for name, spec in UPSTREAMS.items():
        path = CACHE / name
        line = f"  {name} @ {_git('rev-parse', '--short', 'HEAD', cwd=path)}"
        if spec["submodules"]:
            line += "  (" + ", ".join(
                s.split()[1] + " @ " + s.split()[0].lstrip("+-U")[:7]
                for s in _git("submodule", "status", cwd=path).splitlines()
            ) + ")"
        print(line)
    return 1 if changed else 0


def cmd_apply(args) -> int:
    changed = _changed_entries()
    if args.names:
        targets = []
        for name in args.names:
            matches = [e for e in MANIFEST if _entry_name(e) == name]
            if not matches:
                sys.exit(f"no manifest entry named {name!r}")
            targets.extend(matches)
    else:
        targets = [e for e in changed if e[3] == "copy"]
        skipped = [e for e in changed if e[3] != "copy"]
        for entry in skipped:
            print(f"NOT applied ({entry[3]}, name it explicitly once handled): "
                  f"{_entry_name(entry)}", file=sys.stderr)
    for entry in targets:
        _up, _src, dst, mode, _note = entry
        upstream = _upstream_path(entry)
        if mode == "copy":
            shutil.copy(upstream, ROOT / dst)
            print(f"applied  {dst}")
        else:
            SNAPSHOTS.mkdir(parents=True, exist_ok=True)
            shutil.copy(upstream, SNAPSHOTS / _entry_name(entry))
            print(f"snapshot refreshed  {_entry_name(entry)} "
                  f"(the {'embarked file' if dst else 'synthesized files'} must already "
                  "carry your merge/assessment)")
    if targets:
        print("\nnow update SOURCES.md with the heads from `status`, and commit.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("status")
    p.add_argument("--offline", action="store_true")
    p.set_defaults(func=cmd_status)
    p = sub.add_parser("apply")
    p.add_argument("names", nargs="*")
    p.set_defaults(func=cmd_apply)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
