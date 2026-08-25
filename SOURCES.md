# SOURCES

Provenance map for every verbatim-carried file. Updated on every sync (see `CLAUDE.md`).
Upstream commits recorded at copy time; "pre-repo skill" = the unversioned
`~/.claude/skills/vtes` directory this repo replaced (those files are now owned here — no
upstream to sync from).

Upstream states at the initial copy (2026-08-25):

- `vtes-advanced-rules` @ `5c93271` (submodules: `rulebook2024` @ `0644d3d`, `vtes-rulings` @ `888cd79`)
- `codex-of-the-damned` @ `708386d`

## Verbatim-carried files

| Local file | Upstream | Local delta |
|---|---|---|
| `references/rules/rulebook.md` | vtes-advanced-rules `rulebook2024/content.md` | none |
| `references/rules/advanced-rules.md` | vtes-advanced-rules `docs/advanced-rules.md` | none (Jekyll front matter kept) |
| `references/rules/rulings-canon.md` | vtes-advanced-rules `.claude/references/rulemonger/canon.md` | none (header speaks in the rulemonger's voice; treat as a provenanced cache — live sources win on disagreement) |
| `references/strategy/modules.md` | codex-of-the-damned `.claude/references/strategist/modules.md` | header canonized 2026-08-25 (DRAFT label removed, site links neutralized) — sanctioned by owner |
| `references/strategy/calibration-lessons.md` | codex-of-the-damned `.claude/references/strategist/calibration.md` | none |
| `references/strategy/meta-by-year.md` | codex-of-the-damned `.claude/references/strategist/meta-by-year.md` | none |
| `references/strategy/card-changes-history.md` | codex-of-the-damned `.claude/references/strategist/card-changes-history.md` | none |
| `references/strategy/classification.json` | codex-of-the-damned `.claude/skills/twda/data/classification.json` | none (snapshot; upstream evolves with each TWDA pass — resync deliberately) |
| `references/rules/rules-digest.md` | pre-repo skill `vtes-rules.md` (≡ codex `rules/vtes-rules-digest.md`, byte-identical) | owned here |
| `references/rules/judges-guide.md` | pre-repo skill `judges-guide-v2.md` (≡ codex `rules/judges-guide.md`) | owned here |
| `references/rules/judges-guide-legacy.md` | pre-repo skill `judges-guide.md` (2004 penalties guide) | owned here |
| `references/rules/tournament-rules.md` | pre-repo skill `tournament-rules.md` | owned here |
| `references/rules/code-of-ethics.md` | pre-repo skill `code-of-ethics.md` | owned here |
| `references/rules/rules-feedback.md` | pre-repo skill `rules-feedback.md` | owned here |
| `references/rules/game-terms.json` | pre-repo skill `game_terms.json` | owned here |

## Synthesized files (curated here, never synced)

| Local file | Sources |
|---|---|
| `SKILL.md` | pre-repo skill `SKILL.md` (frame), strategist + rulemonger golden rules (generalized) |
| `references/strategy/theory.md` | codex-of-the-damned `.claude/agents/strategist.md` — theory, golden rules, procedures, data toolbox; custodial machinery (site style, read-only rules, repo paths) dropped; procedures re-grounded on the public KRCG API |

## Dropped on dedup / scope (revisit deliberately)

- codex `rules/vtes-rules-full.md` — the 2024 rulebook reformatted; superseded by `rulebook.md`.
- vtes-advanced-rules `vtes-rulings/rulings/*.yaml` — raw rulings DB; covered by API `rulings`
  field + `advanced-rules.md` + `rulings-canon.md`.
- codex `.claude/skills/twda/references/archetype-page-style.md` — site house style, not knowledge.
- rulemonger/strategist agent definitions — custodial roles; their knowledge was extracted.
