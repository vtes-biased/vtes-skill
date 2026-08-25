# Board

What must change, in priority order. The goal is zero; completion is deletion.
Context lives in `wiki/`, asks live here. Never the other way round.

1. **Data layer (phase 2).** First decide the data format version: `data/vtes.json` is V3
   format while the API is v4, and `data/v4/` and `data/v5/` directories exist — the snapshot
   must match the format the skill's API habits are grounded on. Then: fetch script for
   `static.krcg.org/data/` (vtes.json, twda.json →
   gitignored `data/`, with a fetched-at stamp) + a query CLI: card by name/id (full object),
   rulings for a card, TWDA deck by id, card-name search, play rates / co-occurrence since a
   date. Staleness warning past ~30 days, refetch on demand via `Last-Modified`. Then point
   `theory.md`'s data toolbox and `SKILL.md` at the local tooling.
2. **Sync script + install (phase 3).** `sync` script per `wiki/design.md` decision 2; update
   `SOURCES.md` hashes; a repo skill wrapping the sync-as-ingress workflow. Decide GitHub remote
   (org `vtes-biased`, name, visibility — owner call) and push.
3. **Calibration harness (phase 4).** `calibration/` corpus format (question, answer given,
   owner grade, correction), a fixed regression set, first graded sessions with the owner; a
   repo skill wrapping the calibration loop.

<!-- shipped since last upkeep: 1 -->
