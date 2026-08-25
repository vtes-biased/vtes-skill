# Theory of the game and analysis procedures

The frame every VTES deck analysis and strategy answer hangs on, plus step-by-step procedures.
Synthesized from the codex-of-the-damned strategist (see `SOURCES.md`); curated here, not synced.
Companion files, same directory: `modules.md` (the deck-reading vocabulary),
`calibration-lessons.md` (owner-graded heuristics — the quality bar), `meta-by-year.md`,
`card-changes-history.md`, `classification.json` (archetype ground truth).

# Golden rules

1. **Never reason from remembered card text.** Before any claim about a card, fetch it
   (`curl -s "https://api.krcg.org/card/<id-or-name>"`, URL-encode names). Analysis built on a
   misremembered card is worthless — in calibration, ~1/3 of from-memory readings were wrong.
   Read the **whole card object**, not just `card_text`: recruit requirements live in the
   `clans` / `disciplines` fields (Tunnel Runner → `clans:['Akunanse']`).
2. **Date the deck, then read it against its year.** A decklist is a meta answer, not a timeless
   artifact. Check `card-changes-history.md` (did the card do the same thing then?) and
   `meta-by-year.md` (what were the top threats then?). Never judge an old list by today's meta
   without saying so.
3. **Meta claims need TWDA numbers.** "Widely played", "the dominant archetype", "a staple" —
   only with data behind it (see Data toolbox). Otherwise say it's an impression.
4. **Attribute power to the engine, not its pieces.** Madness Network grants off-turn actions;
   Metro Underground merely unlocks. The card that grants the effect is the engine; enablers are
   support (necessary, but pieces).
5. **Combat is not the default focus.** Payload, delivery, defense and economy come first; give
   combat a deep reading only when the deck is actually a combat deck (and then analyze the
   module's *internal synergy*, not its card list).
6. **A&B economy is table stakes, not a finding.** Every competitive deck acts and still defends.
   Flag the exceptions (all-forward builds, bloat-as-sole-defense) — not the norm.
7. **"Better" is per-role, not absolute.** Card comparisons are answered for a deck's role and
   meta: Minion Tap beats Villein on cap-11 crypts (no 5-blood cap), Villein wins on midcaps.
   State the context or don't answer.
8. **Name the mechanics before the archetype.** ~40% of TWDA decks match no known archetype, and
   novel or emerging lists are common. Read the deck bottom-up as engine + modules first; use a
   named archetype only as one-line orientation, and drop it the instant the engine diverges.
   Forcing a familiar label onto a divergent deck is a top failure mode.

# Theory of the game

- **Economy.** Pool is life AND currency (minions, cards); each Methuselah starts at 30. Ousting
  the prey = 1 VP + 6 pool. The first question of any deck: *how does it remove its prey's 30+
  pool, and how fast?* The second: *what does it do the turn it can't?*
- **Four pillars** (also the priority order when cutting single copies): **payload** (bleed,
  votes, or damage permanents), **delivery** (stealth, block denial, swarm width, vote lock),
  **defense** (bloat is generic, bounce is the anti-bleed backbone, blocks, Delaying Tactics),
  **combat management** (posture: disabling / grinding / resisting).
- **Card flow.** Hand is 7; a module's expectation per hand = density × 7. Density classes:
  spam >25%, strong 14-25%, standard 7-14%, tactical <7%. Deck size ≈ peak rotation × 12 turns.
  Situational strong modules jam — look for the release valves (Dreams, Barrens, dual-mode
  cards). Recursion beats rotation.
- **Base mechanics — the free verbs.** The rules give every deck a card-free strategic layer;
  card slots only make sense relative to it. The Edge is an economy (1 pool per unlock phase,
  a vote, a resource some cards spend); torpor is a cost, not an endgame (leave/rescue + hunt
  is a resilience plan — thick blood regeneration IS combat defense); every ready minion is a
  bleed for 1 (width is a clock with zero cards in hand); hunting prices blood in actions;
  a successful block always leads to combat (a small blocker is never "damage-free"); Become
  Anarch and the other base actions are always in the pool of enablers — a "nothing in the deck
  fires this trigger" conclusion is incomplete until the base actions are checked. Full
  treatment: `calibration-lessons.md` § Base mechanics.
- **Archetype categories and their matchup logic.** Bleed: highest prey damage, weak in combat,
  bounce or bloat behind. Vote: high damage + bloat once locked, weak combat and bleed defense,
  damage-distribution freedom = table control (the real reason to play politics). Wall:
  exceptional defense, weak offense, wins long games, protects fragile payload permanents.
  Toolbox: versatile, must play its hand. Rush: table control, not a win plan — needs
  Fame/Dragonbound-class converters to matter on pool. Combo: absolute advantage, fragile,
  draws table hate.
- **Table dynamics.** Cross-table players are natural allies (and vote targets are free there).
  The predator-prey continuum: pressure ripples; with an odd table it comes back around. Lunge
  timing is the key skill: a failed lunge invites the table onto you. Bounce converts the
  predator's power into prey damage. Layered on all of it: deals, standing management, lay low.
- **Copy counts encode intent.** 5× Info Highway + 7× Minion Tap = 3-4 big vampires planned.
  2× of a unique = must land early. Zero wakes = deliberate all-forward. 1× utility beside a
  fetch engine = searchable answer, not filler. Weight focus by frequency, not cleverness: a
  one-off with no fetch is an opportunity (lunge tool, situational answer), never a core
  component; a 1× crypt card is not a designated role without a fetch (you open without it
  ~2/3 of games — only the 3-4× star is); doubled *permanents* are near-certain to be drawn
  and mark deliberate structure.

# Procedure: analyze a deck

1. **Fetch the list.** TWDA id: `curl -s "https://api.krcg.org/twda/<id>"` (JSON with crypt,
   library, date, event, player) — or read the provided list. Note date, event size, format.
2. **Fetch every card you'll lean on** from the KRCG API — all crypt cards (group, capacity,
   disciplines, title, ability) and every library card whose exact text matters to the analysis.
3. **Crypt first.** Grouping legality, capacity curve, discipline spread (inferior vs superior),
   titles (votes AND the titled reaction cards they unlock), abilities. Ask: what does this crypt
   *cohere around*? Copy counts: star (3-4×), core (2×), support (1×).
4. **Decompose the library into modules** (vocabulary: `modules.md`). For each: density and
   expectation, and its pillar. Identify the engine (golden rule 4) and the turn loop: what does
   a mid-game turn look like, action by action, reactions included?
5. **Map the four pillars.** Payload size and reach (bounce-proof? Archon limit?), delivery
   mechanism, defense (wakes? bounce count? bloat rate vs expected bleed pressure?), combat
   posture. Note the deliberate absences — they are choices (all-forward, bloat-as-defense).
6. **Meta-date it.** Year's top threats (`meta-by-year.md`), errata boundaries
   (`card-changes-history.md`). Which inclusions are meta calls? Would the list need adapting
   today, and how?
7. **Compare to relatives.** Archetype labels: `classification.json` (owner-curated ground
   truth — 120 groups, 1,000+ labeled decks since 2021-07, variants linked to mains). Is this
   list standard for its archetype, or a deliberate deviation? Deviations are where the player's
   read lives. If no archetype fits (≈40% of decks; they sit in the `noise` list), say so and
   read the deck on its own mechanics rather than forcing the nearest label (golden rule 8).
8. **Verdict.** Strengths, posture-aware weaknesses (a weakness must name the matchup and the
   mechanism), and what the pilot must do well to win (lunge timing, deal-making, jam
   management).

Depth bar (from owner grading): module-internal synergy, meta-dating, copy-count intent,
posture-aware weaknesses. "Accurate but shallow" fails: naming the modules is the start, the
analysis is *why these cards, in these numbers, in that year*.

# Procedure: compare cards / evaluate a card

1. Fetch both texts. 2. Define the role and deck context (or enumerate 2-3 realistic contexts).
3. Play rates and company: TWDA frequency and co-occurrence — which archetypes carry it
   (`classification.json` + deck scans; see Data toolbox). 4. Answer per context, with the
   numbers, and say which context dominates in practice.

# Procedure: advise on a brew / work-in-progress deck

Advice makes mechanics load-bearing where analysis only grades them, so the grounding rules bite
hardest here. Run the analysis procedure first (steps 2-5, 8 on the draft), then:

- **Check the player's premise before overruling their plan.** When an inclusion looks redundant
  or dead, first verify the card objects and rules that would make it so — the player may have
  seen a constraint you missed (a recruit requirement, a trigger gate, a single point of failure).
- **Enumerate what actually fires every engine** — trigger gates read literally, base actions
  included — before declaring an engine live or dead.
- Recommendations name the cut AND the add, sized in copies, with the pillar each serves.

# Data toolbox

Paths relative to the skill root. The local snapshot (v4 format, same shapes as the API) is the
primary source; refresh with `python3 scripts/fetch_data.py krcg` when the query tool warns.

- **Cards** (full object: `card_text`, `types`, `clans`, `disciplines`, `capacity`, `group`,
  `title`, `rulings`): `python3 scripts/query.py card <name-or-id>`; rulings only:
  `... rulings <name-or-id>`; name/text search: `... search <text> [--text]`.
- **TWDA decks**: `python3 scripts/query.py deck <twda-id>` (~4,500 winning decks since 1994).
- **Play rates / co-occurrence** (behind every meta claim): `python3 scripts/query.py rates
  --since <date> [--top N] [--crypt]` and `... company <name-or-id> --since <date>`.
- **API fallback** (no snapshot at hand): `https://api.krcg.org/card/<id-or-name>`,
  `/complete/<partial>`, POST `/card_search`, `/twda/<id>` — docs `https://v4.api.krcg.org/docs`.
- **Archetype ground truth**: `classification.json` (this directory). Labels are the owner's;
  the `noise` list is the ~40% matching no archetype.
- **Historical rules discussions**: `data/usenet/*.mbox` — see the routing table in `SKILL.md`.
