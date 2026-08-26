# Calibration

The owner-graded corpus and the regression set — the falsifiability layer of the skill
(`wiki/design.md`, decision 3). This directory is plain data, usable by any harness; the loop
that fills it is the `/calibrate` repo skill (`.claude/skills/calibrate/`).

## Corpus entries — `corpus/YYYY-MM-DD-<slug>.md`

One file per graded exchange:

```markdown
---
date: 2026-08-25
mode: rules | analysis | advice
skill-commit: <short hash of this repo when the answer was produced>
model: <optional — only when the answer was produced by a non-default model (e.g. opus)>
status: graded | candidate
regression: yes | no
---

## Question

Verbatim, as asked.

## Answer given

Verbatim, as the skill produced it.

## Owner grade

The verdict in the owner's words.

## Correction

What the right answer was, and why. Omit the section when the grade is clean.

## Generalization

Where the lesson was folded: a `LESSONS.md` entry, a `theory.md`/`SKILL.md` edit (curation
decision), or "case-specific — none".
```

- `skill-commit` ties the answer to a skill revision — regression drift is meaningless without
  it.
- `status: graded` requires owner adjudication. Community feedback (once the public bot exists)
  enters as `status: candidate` in this same format and never drives a revision until the owner
  grades it.
- `regression: yes` marks membership in the fixed regression set. Default candidate: any graded
  entry with a substantive correction; the owner confirms membership.

## `LESSONS.md`

The distilled operating heuristics from this repo's graded sessions — synthesized here. It
*extends* the carried codex baseline (`references/strategy/calibration-lessons.md`), which is
frozen upstream knowledge: new lessons land in `LESSONS.md`, never in the carried file.

## Regression re-runs

After a skill revision (`SKILL.md`, `theory.md`, `LESSONS.md`, or a knowledge sync), every
`regression: yes` question is re-asked fresh — the answering context sees only the question,
never the recorded grade — and the fresh answers are diffed against the graded record into a
drift report. The owner adjudicates drift; nothing self-grades.
