# CLAUDE.md

This repo is the **source of truth for the `/vtes` agent skill** — a self-contained VTES
(Vampire: The Eternal Struggle) expert skill. It is installed by symlinking the repo into
`~/.claude/skills/vtes`, so editing here edits the live skill. The goal: make an agent as
competent at VTES as an expert player — judge-level on rules, calibrated-analyst-level on
strategy.

## What is what

- **`SKILL.md`** — the always-loaded router and operating frame. Keep it lean: golden rules,
  condensed frame, routing table, data endpoints. Anything longer belongs in `references/`.
- **`references/rules/`** and **`references/strategy/`** — the knowledge. Two kinds of file live
  here, and the distinction governs every edit:
  - **Verbatim-carried** (most files): copied from an upstream repo, mapped in `SOURCES.md`.
    **Never hand-edit these** — fix the upstream and resync, or you fork silently. The one
    sanctioned local delta is recorded per-file in `SOURCES.md`.
  - **Synthesized** (`references/strategy/theory.md`, `SKILL.md`): curated in this repo. Upstream
    changes don't merge into them mechanically — an upstream diff is a *prompt* to revisit the
    synthesis, a curation decision.
- **`SOURCES.md`** — the provenance map: every verbatim file → upstream path, commit, copied-at
  date, and the dedup/drop decisions. Update it on every sync.
- **`wiki/`** — standing knowledge: design decisions and rationale. Read `wiki/design.md` before
  changing the architecture.
- **`BOARD.md`** — what must change, in priority order. The goal is zero; completion is deletion.
- **`calibration/`** (once phase 4 lands) — the owner-graded corpus and regression set.

## Standing constraints

- **Harness-neutral knowledge.** Everything under `references/` is plain Markdown/JSON/scripts
  with no Claude-Code-isms, so the knowledge layer can be reused by other harnesses (a public
  bot, another agent). `SKILL.md` is the only Claude-Code-specific file.
- **Self-contained.** No file references into other repos. Network grounding (api.krcg.org,
  static.krcg.org) is first-class and encouraged; cross-repo file paths are forbidden.
- **Grounding discipline applies to maintenance too.** When editing knowledge files, verify
  claims against the rulebook/rulings/API — never from memory.
- **Bulk data is not committed.** Snapshots fetched from static.krcg.org live in `data/`
  (gitignored); scripts and freshness stamps are committed, the data is not.

## Maintenance loops

- **Sync** (scripted in phase 3, manual until then): fetch the upstream heads, diff the
  verbatim-carried files against what's embarked, update `SOURCES.md` hashes. A diff on a
  verbatim file → apply it; a diff that touches synthesized material → treat as ingress, decide.
  Upstreams: `vtes-biased/vtes-advanced-rules` (+ its `rulebook2024` submodule) and
  `lionel-panhaleux/codex-of-the-damned`, plus the pre-repo skill files (now owned here).
- **Calibration** (phase 4): graded Q&A sessions with the owner; feedback becomes corpus entries
  only after owner adjudication; a fixed regression set is re-run after skill revisions.
  Community feedback, when it arrives, is *candidate* entries — the owner remains the judge.

## Commits

Trunk-based: straight to `main`, fast-forward, no feature branches. Describe the change itself.
