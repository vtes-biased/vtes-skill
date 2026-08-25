# vtes-skill

A self-contained agent skill making an AI assistant expert at **VTES**
(Vampire: The Eternal Struggle): judge-level on rules, calibrated-analyst-level on deck
analysis and strategy.

It merges three sources: the VEKN rules corpus (verbatim 2024 rulebook, tournament rules,
judges' guide), the [vtes-advanced-rules](https://github.com/vtes-biased/vtes-advanced-rules)
synthesis (~2,600 rulings distilled into principles), and the strategy method built for
[codex-of-the-damned.org](https://codex-of-the-damned.org) (theory of the game, module
vocabulary, owner-calibrated analysis procedures). Live card and TWDA data comes from
[KRCG](https://api.krcg.org) — the skill never reasons from remembered card text.

## Layout

- `SKILL.md` — the entry point (Claude Code skill format): operating rules + routing table.
- `references/rules/` — rulebook, advanced rules, rulings database & canon, judges' &
  tournament guides.
- `references/strategy/` — theory & procedures, modules catalog, calibration lessons, meta
  history, archetype classification.
- `scripts/` — fetch and query the bulk data (cards, rulings, TWDA from
  [static.krcg.org](https://static.krcg.org), plus the historical usenet rules-discussion
  archives hosted as this repo's `usenet-archives` release) into `data/` (gitignored).
- `SOURCES.md` — provenance of every carried file. `wiki/` — design decisions. `BOARD.md` —
  pending work.

## Install (Claude Code)

```sh
ln -s "$(pwd)" ~/.claude/skills/vtes
python3 scripts/fetch_data.py all   # cards + TWDA snapshot, usenet archives (~750MB extracted)
```

The knowledge layer (`references/`) is plain Markdown/JSON, deliberately harness-neutral —
reusable from any agent framework.

Licensed under [MIT](LICENSE); VTES game content (rulebook, card text and images) is used under
the [Dark Pack](https://www.worldofdarkness.com/dark-pack) agreement and remains the property of
Paradox Interactive AB.
