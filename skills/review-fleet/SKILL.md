---
name: review-fleet
description: Batch-judge 200+ items against a rubric with an agent fleet (mapping edges, label assignments, taxonomy rows, classification queues). Triggers - "review every mapping", "classify all N rows", "have agents judge this list", "second-pass review". NOT for code review (pr-code-review) or single-item judgments.
---

# Review fleet

Operational mechanics only. If the fleet's numbers will feed a decision,
deliverable, or slide, work through `judge-fleet-methodology` FIRST (thresholds,
contamination, blinding, sampling) — this skill assumes the study design is
already sound.

Batch-judge a large item list with agent waves. Proven on DAT-55 (2026-08-18):
2,471 mapping edges x 2 independent passes (Sonnet, then Opus), 100% coverage,
zero malformed outputs, human queue cut from 2,471 rows to ~530 contested ones.

## The shape

1. **Prep** (`prep_batches.py` pattern): split items into ~20 contiguous batch
   files of ~50 units each, JSONL, one line per unit. Keep natural groups
   together (an entry and all its siblings) — group context changes verdicts.
   Order batches by impact so partial completion is still useful. Assert totals.
2. **Waves**: 5 agents per wave, one batch each; verify between waves. Agents
   read their own input file and write their own output file (keeps orchestrator
   context flat); final reply is a count only.
3. **Verify** (`verify_reviews.py` pattern): mechanical, per batch — every input
   unit covered exactly once, enum fields valid, required fields nonempty.
   Re-dispatch failures; a machine-sleep kill mid-wave is recovered by checking
   for partial output files and relaunching the clean set.
4. **Merge**: join outputs back to the source list with context columns, sort
   the human queue by (confidence asc, impact desc), add empty human-verdict
   columns. The human rules on clusters, not rows: surface the 2-3 axes the
   disagreements group on.

## The prompt skeleton

- CONTEXT: what the system does with a verdict (the DAT-55 lesson: agents must
  know labels are applied conjunctively, not as coverage lists).
- VERDICT RULE with a type specimen (one worked valid + one worked invalid).
- AN OPERATIONAL TEST phrased as a question ("if every X got Y, would a
  complaint be justified for a meaningful share?").
- FULL VOCABULARY: give the complete target catalogue, not its size. Scope of
  a label is bounded by its siblings; agents without the list guess scope
  (round 1 missed this; round 2 fixed it).
- CONFIDENCE 1-5 with an anti-inflation clause: "a human reviews lowest-first,
  honest low confidence routes hard calls correctly."
- POPULATION RISK flag: verdicts rest on nominal meaning; when the verdict
  would flip if the real population is looser than the name, flag it instead
  of guessing (the Wearables lesson: vendor tags get applied to watchmakers).
- OUTPUT: strict JSONL schema, copy key strings EXACTLY, cover every unit in
  order, rationale <=20 words.
- "Do not ask permission before reading or writing files."

## Independent second pass (when stakes justify ~2x cost)

Blind re-judgment, not critique: second model reads the same inputs, never the
first pass's verdicts ("a first review exists but you must not seek it out"),
separate output dir, same rubric verbatim plus only the additions that fix
known round-1 limitations. Agreement is then evidence: agreed-invalid is the
defensible core; disagreements float to the human's top. DAT-55: 89.8%
agreement, and the diff caught a real dictionary bug (crunchbase "Windows"
mapped as building windows).

## Cost design (do this BEFORE launching; see meter-agent-fleets memory)

Per-batch: ~8k in / 4k out. Sonnet full pass over ~2,500 units ~= 250k tokens;
Opus ~5x. Waves cap concurrent spend and give checkpoints. Compact output
(short rationale, no prose) is the main lever.

## Known limits

- Agents judge nominal meaning; polysemous item names need an empirical
  spot-check (top-N-by-size pull) before final verdicts.
- Batches partition by impact order, not by difficulty; confidence sorting
  happens at merge, not at batching.
- Reference scripts live in the DAT-55 thread:
  `~/Documents/git/workpod/projects/dat-55/threads/vvencill-dat-55-industry-labeling-investigation/`
  (prep_batches.py, verify_reviews.py, diff_reviews.py, merge_reviews.py).
