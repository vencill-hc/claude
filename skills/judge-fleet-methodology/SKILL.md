---
name: judge-fleet-methodology
description: 'Methodology checklist for designing or reviewing LLM-judge agent fleets — grounding studies, label/dictionary review passes, vendor data-quality comparisons, any run where agents judge data and the resulting numbers feed a decision, deliverable, or slide. Use BEFORE writing the fleet prompt or study plan, and when asked to review such a plan for rigor ("is this defensible", "what would a reviewer say"). Triggers: "grounding fleet", "review fleet", "LLM as judge", "agent verdicts", "precision study", "vendor comparison", "double review", "judge rubric".'
---

# Judge-Fleet Methodology

Checklist for studies where LLM agents judge data quality. Derived from the DAT-55
industry-labeling fleets (Sonnet review, Opus double-review, vendor-comparison
grounding design, 2026-08). Work through every section before the fleet runs;
findings that surface only after the run usually invalidate the numbers.

## 1. Pre-register before running

Write these into the plan before any agent runs, so results can't be interpreted
post-hoc:

- **Decision threshold**: what result triggers what action, numerically
  (e.g. "recommend precedence only if unique-label precision differs by ≥15 points
  with non-overlapping 95% CIs"). "Mostly noise" is not a threshold.
- **Metric grain**: micro (pool all labels; heavy items dominate) vs macro
  (per-item average). Pick one and say why.
- **Partial verdicts**: how `partial`/`uncertain` counts in the numerator
  (half-credit vs excluded changes headline numbers materially).
- **Exclusion criteria**: written before anyone eyeballs the frame. Log every
  excluded row with its reason so the sample is reproducible.

## 2. Keep ground truth independent

- If judges research via web search, blacklist the sources under evaluation and
  their mirrors (e.g. judging LinkedIn/Crunchbase labels → ban linkedin.com,
  crunchbase.com, zoominfo, pitchbook aggregator pages). Search results are
  saturated with exactly these sites; contamination is circular and biased toward
  whichever vendor ranks better.
- Record the URLs each judgment actually used in the output JSONL so contamination
  is auditable afterward.

## 3. Blind the judge

- Present items as a shuffled, unattributed pool — the judge must not know which
  source/vendor supplied which label. Re-attach attribution in the metrics script.
- One agent may research AND judge, but it must not see anything that invites
  brand-halo or anchoring (source names, prior verdicts, DU's current label).

## 4. Validate the judge

- A human calibration eyeball of wave 1 is calibration, not validation. Also do at
  least one of:
  - **Gold subset**: human hand-labels ~15 items independently; report agreement
    between fleet and gold.
  - **Second-model double review**: rerun the full set with a different model;
    report agreement % and queue disagreements for human ruling first
    (DAT-55: Sonnet vs Opus agreed 89.8%; the 252 disagreements were the
    human-review queue).
- If the rubric changes after a calibration wave, re-run that wave under the final
  rubric — never mix judgments made under two rubrics.

## 5. Sample honestly

- Name the frame's conditioning and what it makes unobservable (e.g. requiring
  both vendors present → "both miss the company" is invisible; the study answers
  precision-where-both-speak, not which vendor is better).
- Head-of-distribution samples (top-N by size) measure where data is cleanest —
  an upper bound. Scope every claim ("among large X firms") and watch the
  qualifier survive into slides.
- Check the selection variable's provenance: sorting by a field derived from a
  judged source selects via a contestant's variable.
- When compared sources have different label semantics (many broad tags vs one
  primary label), per-label precision differs by construction. Report label
  counts per source per item alongside precision.

## 6. Report

- Every headline number carries its n and a binomial CI. Tiny subsets
  (unique-to-one-vendor labels are often 10–30 items) are usually underpowered —
  say so rather than letting a 20-point gap masquerade as signal.
- Never headline a mechanical agreement number (string overlap) without the
  semantic figure beside it.
- Note temporal mismatch when judging scraped claims against today's web; have
  the judge flag "recently pivoted" items.

## 7. Cost design

Waves with a human checkpoint after wave 1; compact structured output only;
cheapest adequate model. (Per the metered-fleets rule — the org has hit spend
limits mid-fleet before.)

## Companion skill

Once the design passes this checklist, `review-fleet` carries the operational
mechanics: batch prep, wave sizing, mechanical verification, merge, and the
confidence-routed human queue.
