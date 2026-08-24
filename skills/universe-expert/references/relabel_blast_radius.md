
# Relabel Blast Radius

Exact affected-population counts for parser/taxonomy changes in
`data-universe-pipelines`, measured against `gdulabs-production`. Built and
validated 2026-08-19 (swap: 294.56M People / 682.85M employments; #540 delta:
65.79M / 90.91M). The harness lives in `scripts/job_function_volume/` on the
taxonomy-swap branch (until folded: workpod thread
`role-ontology-overhaul/threads/vvencill-job-function-taxonomy/people-affected-2026-08-19/harness.patch`).

## The method (why it's shaped this way)

The parser CANNOT run in SQL (Python `re` vs RE2 diverge on `\w`/`\b`;
`normalize_job_title` has no SQL equivalent — settled decision, don't
relitigate). So every exact count is a roundtrip:

1. classify distinct exported titles LOCALLY with the real parser (FastMatcher
   fast path, self-checked against the slow path; 238M rows ≈ 6 min on 14 cores)
2. load the deciding titles to a temp BQ table
3. join back to `employments` on the export's light normalization and count in BQ

The join key is `TRIM(REGEXP_REPLACE(LOWER(job_title), r'\s+', ' '))` — the
export's own grouping key, computable identically on both sides, and it can
never merge titles that classify differently (it's the first step of
`normalize_job_title`).

## Mode 1 — stored-vs-new (what a relabel run rewrites)

"Affected" = the stored value actually changes: `label_employments` deltas
new-vs-extant layers, so identical re-parses emit nothing.

```bash
# input: the titles export (workpod/assets/titles.ndjson.gz, or regenerate
# with export_titles.py — 94GB scan)
uv run python scripts/job_function_volume/estimate_affected_people.py \
    --exact ~/Documents/git/workpod/assets/titles.ndjson.gz
# cheap companions: --buckets (SQL-only bounds), --sample (1-in-1000 person
# hash), --person-layers (rows a relabel CREATES — usually tiny; creation
# requires a missing labeling PersonLayer, not a changed value)
```

## Mode 2 — rev-vs-rev (one PR's causal delta)

Never simulate an old parser from memory or from a frozen copy of uncertain
vintage — run each revision's REAL code from its own worktree:

```bash
git worktree add --detach /tmp/wt-before <base-rev>
git worktree add --detach /tmp/wt-after  <pr-head>
uv run python scripts/job_function_volume/classify_titles_at_rev.py \
    --src /tmp/wt-before/src --titles <export> --out before.ndjson.gz
# ... same for after, then:
uv run python scripts/job_function_volume/delta_affected_people.py \
    --before before.ndjson.gz --after after.ndjson.gz --table delta_<pr>_titles
```

Outputs are line-aligned; the compare skips identical lines on raw bytes and
only parses disagreements. The ROLLUP query returns per-flow employments +
distinct People + grand total in one scan. This measures parse-vs-parse;
stored-value staleness is deliberately out of scope for a PR delta.

## Non-negotiable discipline

- **Consent per invocation.** Every prod-touching run (even a re-run) gets VV's
  explicit yes at runtime. `--dry-run` first, report GB, then run. Background
  long runs and report on completion.
- **Temp datasets:** dated `tmp_<purpose>_mmddyyyy`, location mirrored from
  `data_universe`, `default_table_expiration_ms` = 7 days. Note the expiry in
  the workpod when saving results.
- **Cross-check before reporting.** At least one independent estimate must
  bracket the exact number (sample mode, SQL-only bounds, or
  employments-per-person ratio). The 2026-08-19 sample landed 0.07% off exact.
- **Save to workpod** (`role-ontology-overhaul/threads/vvencill-job-function-taxonomy/`):
  run logs + flow tables as a dated artifact dir, record in notes.md, progress
  entry in state.md.

## Gotchas that already burned a run

| Trap | Rule |
|---|---|
| `pl.source = 'universe_labeling'` matched ZERO rows (stored value is UPPERCASE) — a full 224GB query returned garbage that looked plausible | Join literals come from the code that writes them (`SourceName.UNIVERSE_LABELING.value`, `generate_labeling_person_unique_id`), never retyped; assert in tests |
| Rev-pinned runner imported `volume_accounting`, whose top-level imports pre-seeded `sys.modules` with the CURRENT branch's parser — the pinned import would silently resolve wrong | Runner imports nothing that touches `utils.*`; `_init` asserts each module's `__file__` is under the pinned src |
| `git diff > file` through the rtk hook writes token-compressed non-patches | `rtk proxy git diff`, then verify `git apply --check --reverse` |
| A result exactly equal to a total (e.g. missing-layer count == people_total) | Treat as a broken join until proven otherwise |
| "Classification takes ~1h" was folklore; benchmark said 9 min | Benchmark 2M rows and extrapolate before redesigning around a cost |
| Per-title classifications from prior accounting runs are NOT recoverable (outputs are aggregates) | Reclassifying is cheap (~6 min); don't archaeology the old run |

## Invariants the tools enforce (trust, but check the console)

- buckets: three buckets sum to people_total (nonzero exit on violation)
- delta compare: line counts must zip strict; title misalignment asserts
- classify runners: 50k-row fast-vs-slow self-check per revision before the run
