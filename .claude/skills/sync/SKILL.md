---
name: sync
description: >
  Run the upstream sync-as-ingress loop for the vtes-skill repo: check the upstream repos for
  changes to the carried knowledge files, adjudicate the diffs, apply, and record provenance.
  Use for "sync the skill", "check upstreams", or after the owner says an upstream repo changed.
---

# Sync the skill with its upstreams

The diff is an **ingress artifact**, not a notification: every upstream change is adjudicated
before it lands (wiki/design.md, decision 2). Never rubber-stamp.

1. Run `python3 scripts/sync.py status`. Exit 0 and all IN-SYNC → report "clean", done.
2. For each **copy** entry marked UPSTREAM-CHANGED: read the diff. Sanity-check it against the
   skill (does it contradict `SKILL.md`'s routing descriptions, `wiki/design.md` decisions, or
   other carried files?). If sound, `python3 scripts/sync.py apply` (no args applies all
   mechanical changes). If it contradicts something, stop and surface to the owner — do not
   apply half a sync silently.
3. For each **curated** entry (has a sanctioned local delta, see SOURCES.md): read the diff
   (it is against the snapshot, so the sanctioned delta does not appear). Merge the upstream
   change into the embarked file **by hand, first**, preserving the delta — **then**
   `apply <name>` to refresh the snapshot. Applying before merging silently drops the upstream
   change from tracking.
4. For each **watch** entry: the upstream file is not embarked; the note names the synthesized
   files to revisit. Read the diff, decide whether `theory.md` / `SKILL.md` need updating, make
   the updates (or record in the commit message why none were needed) — **then** `apply <name>`.
5. Update `SOURCES.md`: the upstream heads printed by `status`, dated today; any new sanctioned
   delta gets its own note. If a synced file's role changed (new sections worth routing to),
   update `SKILL.md`'s routing table.
6. One commit for the whole sync, describing what changed upstream and what was decided.
   Push.

Escalate instead of deciding alone when: an upstream change reverses a `wiki/design.md`
decision, a curated merge conflicts with the sanctioned delta itself, or a watch diff implies
reworking the synthesized layer substantially.
