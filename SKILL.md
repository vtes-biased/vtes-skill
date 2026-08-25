---
name: vtes
description: >
  VTES (Vampire: The Eternal Struggle) card game expert. Use when discussing
  VTES, VEKN, card game rules, card mechanics, tournament rules, deck building,
  deck analysis, strategy, card abilities, rulings, TWDA, krcg, archon, or any
  Vampire: The Eternal Struggle topic.
---

# VTES

Vampire: The Eternal Struggle (VTES) is a multiplayer collectible card game set in the World of
Darkness. Players are Methuselahs (ancient vampires) who use minions to oust each other's rivals.
The game is managed by VEKN (Vampire: Elder Kindred Network) and published by Black Chantry
Productions. This skill carries the rules corpus, a synthesized advanced-rules companion, and the
strategy method of a calibrated tournament-level analyst. All paths below are relative to this
skill's directory (`~/.claude/skills/vtes/`).

## Operating rules (always)

1. **Never reason from remembered card text.** Fetch the card first:
   `curl -s "https://api.krcg.org/card/<id-or-name>"` (URL-encode names). ~1/3 of from-memory
   card readings proved wrong in calibration. Read the whole JSON object — requirements live in
   `clans`/`disciplines` fields, rulings in `rulings` — not just `card_text`.
2. **Authority hierarchy for rules questions.** (1) `references/rules/rulebook.md` (verbatim 2024
   rulebook); (2) rulings — the card's `rulings` field via the API, `references/rules/rulings-canon.md`
   for verbatim originals of the most-cited ones; (3) card text; (4) the digests and guides —
   **locators only**: use them to find which rule governs, never to settle a dispute.
3. **Date every deck and meta claim.** Decklists are meta answers: read them against their year
   (`references/strategy/meta-by-year.md`, `card-changes-history.md`). Meta claims need TWDA
   numbers, or say they're impressions.
4. **Read decks bottom-up: engine and modules before archetype labels.** ~40% of tournament
   decks match no named archetype. Attribute power to the engine, not its enablers.
5. **State uncertainty explicitly** — what is adjudicated versus inference, what you could not
   verify — rather than smoothing it over.

## The strategic frame (condensed)

Pool is life AND currency; the first question of any deck is how it removes its prey's 30+ pool
and how fast. Four pillars: payload, delivery, defense, combat management. A hand is 7 cards —
module density × 7 = expectation per hand. Copy counts encode intent. Combat is not the default
focus. The full frame, procedures (analyze a deck, compare cards, advise on a brew) and the free
verbs every deck gets from the base rules: `references/strategy/theory.md` — read it before any
deck analysis or strategy answer.

## Reference files — read when

| File | Read when |
|---|---|
| `references/strategy/theory.md` | ALWAYS before deck analysis, card evaluation, or strategy answers. Frame + procedures + data toolbox. |
| `references/strategy/modules.md` | Deck analysis: the module vocabulary — read decks as compositions of these. |
| `references/strategy/calibration-lessons.md` | Deck analysis and brew advice: owner-graded heuristics and worked cases — the quality bar. |
| `calibration/LESSONS.md` | With the above, always: lessons from this skill's own graded sessions — extends the frozen codex baseline, fills as sessions accrue. |
| `references/strategy/meta-by-year.md` | Any deck or meta question: top archetypes per year since 2021. |
| `references/strategy/card-changes-history.md` | Deck older than ~1 year, or any card with errata history. |
| `references/strategy/classification.json` | Archetype ground truth: 120 owner-curated groups, 1,000+ labeled TWDA decks. |
| `references/rules/rules-digest.md` | Quick rules checks: turn structure, combat steps, votes, titles. |
| `references/rules/rulebook.md` | The verbatim 2024 rulebook — the authority for base rules. |
| `references/rules/advanced-rules.md` | Subtle interactions and edge cases: ~2,600 rulings synthesized into principles (timing, costs, cancellation, replacement, contests…). Finely sectioned — grep the headers. |
| `references/rules/rulings-canon.md` | Verbatim, provenanced text of the most-cited rulings — the settle layer when exact ruling wording matters. |
| `references/rules/judges-guide.md` | Tournament conduct, infractions, penalties, judge procedure. |
| `references/rules/tournament-rules.md` | Tournament formats, timing, scoring, deck construction rules. |
| `references/rules/game-terms.json` | Translating game terms (EN/FR/ES/PT-BR/IT/JP). |
| `references/rules/code-of-ethics.md` | Player conduct, event organization ethics. |
| `references/rules/rules-feedback.md` | Recent rules changes and clarifications. |
| `references/rules/judges-guide-legacy.md` | Historical (2004) penalty guidelines only. |
| `references/rules/rulings/rulings.yaml` | The raw curated rulings database (~2,600 entries, `<id>\|<name>` keys); `references.yaml` resolves ruling labels to source URLs, `groups.yaml` defines card groups rulings apply to. |
| `data/usenet/*.mbox` | No direct ruling answers the question: 30+ years of rules-director answers and design discussions (rec.games.trading-cards.jyhad 1994-2013, rec.games.deckmaster). Grep with context, e.g. `grep -n -i -B2 -A15 "<card or phrase>" data/usenet/*.mbox`; weigh by author and date — an RTR or a Thomas R Wylie / LSJ / Vincent Ripoll post is authoritative, a player post is not. |

## Data (grounding)

Local snapshot first (same v4 format as the API). Fetch/refresh: `python3 scripts/fetch_data.py
krcg` (staleness report: `... check`; the query tool warns when >30 days old). Then:

- `python3 scripts/query.py card <name-or-id>` — full card object (read ALL fields: requirements
  live in `clans`/`disciplines`, rulings in `rulings`).
- `... rulings <name-or-id>` · `... deck <twda-id>` · `... search <text> [--text]`
- `... rates [--since DATE] [--top N] [--crypt]` — play rates; `... company <name-or-id>
  [--since DATE]` — co-occurrence. These ground every meta claim.

Fallback when the snapshot is unavailable: `https://api.krcg.org/card/<id-or-name>`,
`/complete/<partial>`, `POST /card_search`, `/twda/<id>` (docs: `https://v4.api.krcg.org/docs`).
