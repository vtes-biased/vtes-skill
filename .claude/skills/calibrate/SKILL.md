---
name: calibrate
description: >
  Run the owner-graded calibration loop for the vtes-skill repo: a graded session (owner asks,
  the skill answers, the owner grades, the exchange is recorded) or a regression re-run after a
  skill revision. Use for "calibration session", "grade the skill", "run the regression set".
---

# Calibrate the skill

The owner is the only grader (`wiki/design.md`, decision 3). The corpus format and the
regression-membership rule live in `calibration/README.md` — follow them exactly.

## Graded session (owner present)

1. Note the current commit (`git rev-parse --short HEAD`) — it goes in every entry produced
   this session. Take the owner's question; infer the mode (rules | analysis | advice) from it.
2. Answer with the full skill, exactly as a user-facing answer: invoke the vtes skill and follow
   its operating rules — grounding via the data layer, authority hierarchy, dated meta claims.
   No shortcuts and no extra hedging because it is a test; the corpus must grade the skill's
   real behavior.
3. Take the owner's grade and corrections. Record the entry in
   `calibration/corpus/YYYY-MM-DD-<slug>.md` **verbatim, before distilling anything** — raw
   record first, curation second.
4. Distill: if a correction generalizes, propose wording for `calibration/LESSONS.md` — or for
   `theory.md`/`SKILL.md` when the lesson is frame-level — and let the owner approve it before
   writing. Record in the entry's Generalization section where the lesson went (or that it is
   case-specific).
5. Ask the owner whether the entry joins the regression set (`regression: yes`); propose it by
   default when the correction was substantive.
6. One commit for the session (entries + lessons together). Push.

## Regression re-run (after a skill revision)

1. Collect every corpus entry with `regression: yes`.
2. For each, spawn a fresh subagent whose prompt contains ONLY the question and the instruction
   to answer using the vtes skill — never the recorded answer, grade, or correction. Fresh
   answers must not be contaminated by the expected result.
3. Diff each fresh answer against the entry's graded answer + correction. Sort: holds (the
   correction is respected), improved, drifted (the corrected mistake is back, or a new one).
4. Produce a drift report for the owner — never self-grade. Corpus entries and lessons stay
   untouched until the owner rules; fixes decided from the report are ordinary skill revisions
   (which then warrant their own re-run).

## Candidates (community feedback)

Feedback from non-owner sources enters as `status: candidate` entries in the same format,
clearly attributed. Candidates never drive a revision and never join the regression set until
the owner grades them (they then become `status: graded`).

Escalate instead of deciding alone when: a correction contradicts a carried knowledge file
(that is an upstream fix or a `/sync` question, not a lesson), or a lesson would rework
`SKILL.md`'s operating rules or a `wiki/design.md` decision.
