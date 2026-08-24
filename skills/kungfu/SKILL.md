---
name: kungfu
description: Perform a "look back and look forward" gap analysis on recent work. Identifies patterns that should become skills, analyzes remaining work, and automatically generates new skills for future sessions.
---

# Kung Fu: Retro → Skills → Backlog

Retrospective over recent work: find repeating patterns worth a skill, correct
skills that misfired, and queue tooling/process fixes. De-templated 2026-08-24
(the original carried Entity4/NetSuite boilerplate from a foreign project);
this is the process as actually practiced here. Outputs land in the claude
skills repo and the workpod `kungfu-backlog` thread — never in ad-hoc files or
new projects.

## Look back

- `git log` across every repo touched recently (pipelines, workpod, claude,
  dotfiles, …) plus the active workpod threads' Recent progress.
- The session itself: errors hit repeatedly, house rules violated under
  momentum, tools worked around instead of fixed, anything researched twice.

## Gap tests — 2+ occurrences or it isn't a pattern

| Signal | Response |
|---|---|
| Same multi-step workflow twice | Workflow skill |
| Same rule violated despite being written down | Harness guard (hook) — prose doesn't hold under momentum |
| Same error class twice | Fix the tool itself; a workaround skill is a smell |
| Same research twice | Reference file under the owning existing skill, not a new skill |
| Existing skill misfired or went stale | Update it in place; never create a near-duplicate |

## Look forward

Scan open work (workpod threads, PR stack, the kungfu-backlog itself) for
upcoming tasks the identified gaps would bite. That ranking — not novelty —
orders the recommendations.

## Outputs (all four, every run)

1. **Skills**: create/update under `~/Documents/git/claude/skills/<name>/`,
   symlink from `~/.claude/skills/`, add to the gdu profile if domain-scoped,
   commit. Before creating, read the neighboring skills a new one would
   border and rule out overlap (see the 2026-08-24 dedup pass in the
   kungfu-backlog decisions log for what happens otherwise).
2. **Rules-of-working corrections** → auto-memory (`feedback`/`project`
   types), cross-linked.
3. **Tooling/process recommendations** → APPEND as checklist items to the
   standing workpod thread `kungfu-backlog` (evidence, proposed fix, rough
   size). Never scaffold a new workpod project for a retro.
4. **Report**: patterns found, skills shipped/updated, items queued — one
   line of evidence each. Recommendations are queued, not executed; VV
   prioritizes the backlog.

## Boundaries

- Skipped-skill candidates get recorded in the backlog thread's notes.md with
  the reason, so future runs don't re-litigate them.
- Run at natural breakpoints (end of a review round, a merged PR, a shipped
  deliverable) — not mid-task.
