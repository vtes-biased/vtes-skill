# Design

The architecture of the skill and the decisions behind it. Settled 2026-08-25 between the owner
and Claude; revisit only with the owner.

## What this skill merges

Three sources, three altitudes:

- The **pre-repo `/vtes` skill** (unversioned, `~/.claude/skills/vtes`): a library — glossary +
  raw reference dumps (rulebook digest, tournament rules, judges' guides). Knew where facts
  live, had no method.
- **`vtes-advanced-rules`**: the rules depth — `advanced-rules.md` (~2,600 rulings synthesized
  into principles, adversarially verified by the rulemonger agent) and `canon.md` (provenanced
  verbatim rulings cache).
- **`codex-of-the-damned`**: the strategy method — the strategist agent's theory of the game,
  procedures, `modules.md` vocabulary, and the owner-graded `calibration.md` corpus.

The merge principle: **method and knowledge in, custodial machinery out**. The source agents are
repo custodians (FINDINGS-ONLY modes, memory protocols, site style rules, read-only
constraints); none of that entered the skill.

## Settled decisions

1. **Self-contained ≠ offline.** No cross-repo file references, ever. But the single most
   load-bearing calibration lesson is "never reason from remembered card text" and that
   grounding is the KRCG API / static.krcg.org data — network grounding is first-class.
   Phase 2 adds a local snapshot of `static.krcg.org/data/` (vtes.json with rulings, twda.json)
   plus query tooling, because grepping 13MB of JSON is worse than the API: the query CLI is
   the real design. Staleness is the new hazard — the tooling must stamp snapshot age, warn
   past ~30 days, refetch on demand (`Last-Modified` HEAD check).
2. **Sync script over git submodules.** Submodules would vendor an entire Flask site to reach
   four files. Instead: a script that reads the upstreams (local checkouts or shallow clones),
   copies the mapped files, records commit hashes in `SOURCES.md`, and prints the diff against
   what's embarked. **The diff is the ingress artifact.** Verbatim-carried files update nearly
   mechanically; diffs touching synthesized material are curation decisions.
3. **Calibration is owner-first, community-later.** Expert-level is unfalsifiable without a
   graded corpus (the codex strategist proved owner-graded runs drive quality). Phase 4 starts
   the corpus with the owner; a fixed regression set re-runs after each revision. The eventual
   public bot (ChatGPT app / Discord / claude.ai) is why `references/` stays harness-neutral —
   and community feedback only ever produces *candidate* entries; the owner adjudicates.
4. **`modules.md` is canonized** (owner, 2026-08-25). The DRAFT header is gone; per-entry ⚠
   flags remain as honest uncertainty markers from the mining pass.

## Dedup decisions (phase 1)

Recorded in `SOURCES.md` with the drops. The shape: one file per role.

- Verbatim 2024 rulebook: `rulebook2024/content.md` → `rules/rulebook.md`. Codex's
  `vtes-rules-full.md` was the same content reformatted — dropped.
- Condensed digest: the pre-repo skill's `vtes-rules.md` and codex's `vtes-rules-digest.md`
  were byte-identical → one copy, `rules/rules-digest.md`.
- Judges' guide: the pre-repo skill's `judges-guide-v2.md` and codex's `judges-guide.md` were
  the same document → `rules/judges-guide.md`; the 2004 guide kept as `judges-guide-legacy.md`.
- `rulings.yaml` (the raw 2,600-ruling database) was **not** embarked: per-card rulings arrive
  via the API/vtes.json, principles via `advanced-rules.md`, verbatim originals via
  `rulings-canon.md`. Revisit if a gap shows.
- `archetype-page-style.md` dropped: codex site style, not knowledge.

## Rules-answer authority hierarchy

(1) verbatim rulebook → (2) rulings (API `rulings` field; `rulings-canon.md` for verbatim
originals) → (3) card text → (4) digests and guides as locators only. Generalized from the
rulemonger; encoded in `SKILL.md` operating rules.

## Phases

1. ✅ Repo skeleton, dedup, synthesized SKILL.md + theory.md, harness (2026-08-25).
2. Data layer: snapshot fetch + query CLI. 3. Sync script + install. 4. Calibration harness.
Live lines: `BOARD.md`.
