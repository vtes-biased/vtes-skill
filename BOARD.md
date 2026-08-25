# Board

What must change, in priority order. The goal is zero; completion is deletion.
Context lives in `wiki/`, asks live here. Never the other way round.

1. **Sync script (phase 3).** `sync` script per `wiki/design.md` decision 2 (upstream heads →
   copy mapped verbatim files → update `SOURCES.md` hashes → print diff as ingress artifact);
   a repo skill wrapping the sync-as-ingress workflow.
2. **Calibration harness (phase 4).** `calibration/` corpus format (question, answer given,
   owner grade, correction), a fixed regression set, first graded sessions with the owner; a
   repo skill wrapping the calibration loop.
3. **Community-source enrichment (exploration).** Evaluate the blogs listed by the
   codex-of-the-damned index page as an additional knowledge tier (see `wiki/design.md`
   decision 6): which are worth embarking, in what form, labeled how. Scope before building.

<!-- shipped since last upkeep: 2 -->
