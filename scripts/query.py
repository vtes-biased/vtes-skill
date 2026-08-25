#!/usr/bin/env python3
"""Query the local KRCG snapshot (fetch it first: scripts/fetch_data.py krcg). Stdlib only.

Usage:
  python3 scripts/query.py card <name-or-id>            # full card object (read ALL fields)
  python3 scripts/query.py rulings <name-or-id>         # just the card's rulings
  python3 scripts/query.py deck <twda-id>               # a TWDA deck
  python3 scripts/query.py search <text> [--text]       # name search; --text also searches card text
  python3 scripts/query.py rates [--since DATE] [--top N] [--crypt]   # play rates (decks containing card)
  python3 scripts/query.py company <name-or-id> [--since DATE] [--top N]  # co-occurring cards
"""

import argparse
import datetime
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
KRCG_DIR = ROOT / "data" / "krcg"
STALE_DAYS = 30


def _warn_staleness() -> None:
    stamp_path = KRCG_DIR / "stamp.json"
    if not stamp_path.exists():
        return
    stamp = json.loads(stamp_path.read_text())
    for name, info in stamp.items():
        fetched = info.get("fetched_at")
        if not fetched:
            continue
        age = (
            datetime.datetime.now(datetime.timezone.utc)
            - datetime.datetime.fromisoformat(fetched)
        ).days
        if age > STALE_DAYS:
            print(
                f"WARNING: {name} snapshot is {age} days old — "
                "run: python3 scripts/fetch_data.py krcg",
                file=sys.stderr,
            )


def _load(name: str):
    path = KRCG_DIR / name
    if not path.exists():
        sys.exit(f"missing {path} — run: python3 scripts/fetch_data.py krcg")
    _warn_staleness()
    return json.loads(path.read_text())


def _find_card(cards: list, key: str) -> dict:
    if key.isdigit():
        matches = [c for c in cards if c["id"] == int(key)]
    else:
        folded = key.casefold()
        names = lambda c: {
            str(c.get(k, "")).casefold() for k in ("name", "_name", "printed_name")
        }
        matches = [c for c in cards if folded in names(c)]
        if not matches:
            matches = [c for c in cards if any(folded in n for n in names(c))]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        sys.exit(f"no card matches {key!r}")
    sys.exit(
        f"{key!r} is ambiguous: " + ", ".join(f"{c['name']} ({c['id']})" for c in matches[:10])
    )


def _deck_cards(deck: dict):
    """Yield (card_id, card_name, count, section) flattening any nesting."""
    for section in ("crypt", "library"):
        stack = list(deck.get(section, {}).get("cards", []))
        while stack:
            entry = stack.pop()
            if "cards" in entry:  # a type-grouping node
                stack.extend(entry["cards"])
            else:
                yield entry["id"], entry.get("name", ""), entry.get("count", 1), section


def cmd_card(args) -> None:
    print(json.dumps(_find_card(_load("vtes.json"), args.key), indent=2, ensure_ascii=False))


def cmd_rulings(args) -> None:
    card = _find_card(_load("vtes.json"), args.key)
    print(json.dumps(
        {"name": card["name"], "id": card["id"], "rulings": card.get("rulings", [])},
        indent=2, ensure_ascii=False,
    ))


def cmd_deck(args) -> None:
    decks = _load("twda.json")
    matches = [d for d in decks if d.get("id") == args.key]
    if not matches:
        sys.exit(f"no TWDA deck with id {args.key!r}")
    print(json.dumps(matches[0], indent=2, ensure_ascii=False))


def cmd_search(args) -> None:
    folded = args.text_query.casefold()
    for card in _load("vtes.json"):
        in_name = folded in card["name"].casefold() or folded in card["_name"].casefold()
        if in_name or (args.text and folded in card.get("card_text", "").casefold()):
            print(f"{card['id']}  {card['name']}  [{'/'.join(card['types'])}]")


def _decks_since(since: str | None):
    decks = _load("twda.json")
    if since:
        decks = [d for d in decks if d.get("date", "") >= since]
    return decks


def cmd_rates(args) -> None:
    decks = _decks_since(args.since)
    counts: dict[tuple, int] = {}
    for deck in decks:
        for cid, name, _n, section in set(_deck_cards(deck)):
            if args.crypt != (section == "crypt"):
                continue
            counts[(cid, name)] = counts.get((cid, name), 0) + 1
    print(f"# decks containing the card, out of {len(decks)} decks"
          + (f" since {args.since}" if args.since else ""))
    top = sorted(counts.items(), key=lambda kv: -kv[1])[: args.top]
    for (cid, name), n in top:
        print(f"{n:5}  {n / len(decks):5.1%}  {name} ({cid})")


def cmd_company(args) -> None:
    card = _find_card(_load("vtes.json"), args.key)
    decks = [
        d for d in _decks_since(args.since)
        if any(cid == card["id"] for cid, *_ in _deck_cards(d))
    ]
    counts: dict[tuple, int] = {}
    for deck in decks:
        for cid, name, _n, _s in set(_deck_cards(deck)):
            if cid != card["id"]:
                counts[(cid, name)] = counts.get((cid, name), 0) + 1
    print(f"# {len(decks)} decks contain {card['name']}"
          + (f" since {args.since}" if args.since else "") + "; their most common cards:")
    for (cid, name), n in sorted(counts.items(), key=lambda kv: -kv[1])[: args.top]:
        print(f"{n:5}  {n / max(len(decks), 1):5.1%}  {name} ({cid})")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("card"); p.add_argument("key"); p.set_defaults(func=cmd_card)
    p = sub.add_parser("rulings"); p.add_argument("key"); p.set_defaults(func=cmd_rulings)
    p = sub.add_parser("deck"); p.add_argument("key"); p.set_defaults(func=cmd_deck)
    p = sub.add_parser("search")
    p.add_argument("text_query"); p.add_argument("--text", action="store_true")
    p.set_defaults(func=cmd_search)
    p = sub.add_parser("rates")
    p.add_argument("--since"); p.add_argument("--top", type=int, default=25)
    p.add_argument("--crypt", action="store_true")
    p.set_defaults(func=cmd_rates)
    p = sub.add_parser("company")
    p.add_argument("key"); p.add_argument("--since"); p.add_argument("--top", type=int, default=25)
    p.set_defaults(func=cmd_company)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
