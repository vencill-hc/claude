---
name: add-function-carveout
description: Add a keyword carve-out to the job-function taxonomy spec in data-universe-pipelines - measure the title-shape split, write Band-1 keys in post-normalization space, tests, docs ruling row, volume rerun. Use on "carve out X to Y", "should X route to a different function", "bring X back", or any spec-keyword judgment (SUP-571-style tickets, EZ review rulings). Not for adding whole function values (enum change, cross-repo).
---

# Add a Function Carve-Out

A carve-out routes a specific phrase to a different function than the general term it rides on (`investment banking` → M&A out of `investment`; `chief merchandising` → Sales out of `merchandis`). It is a keyword-only change: no enum edit, no cross-repo work.

## 1. Measure Before Ruling

The full title corpus is in local psql `gdu_titles` (`titles(job_title, job_function, n)` — 238M distinct / 1.42B people; recreate from `~/Documents/git/workpod/assets/titles.ndjson.gz` if dropped). Bucket the population by title shape:

```sql
SELECT CASE WHEN t ~ '<leadership pattern>' THEN 'leadership' ... END AS bucket,
       sum(n) FROM (SELECT lower(job_title) t, n FROM titles WHERE job_title ILIKE '%<stem>%') s
GROUP BY 1;
```

The ruling question is absolute population + phrase separability, not share: 56.6K merchandising leaders were 2.4% of their stem and still earned the carve-out. A new function *leaf* has a much higher bar (the collapse gate); a carve-out to an existing function only needs clean phrases. Vanessa rules; present the table and the options.

## 2. Keys Live in Post-Normalization Space

`normalize_job_title` (src/utils/string_validator_utils.py) runs BEFORE matching and rewrites via `JOB_TITLE_NORMALIZATION_SYNONYMS`:
- `vice president` → `vp` (fires first, so `senior vice president X` becomes `senior vp X` — a `vp X` key catches it free)
- `director` → `dir` (keys are `merchandising dir`, `dir of merchandising`, never "director")
- `chief executive officer` → `ceo`, `product manager` → `pm`, etc. — read the table before writing any key
- punctuation strips, `and` → `&`, `of` is KEPT (need both `vp X` and `vp of X` forms)
- raw `svp`/`evp` abbreviations do NOT normalize to vp — decide explicitly whether their volume earns keys (merchandising ruling: ~340 people, skipped, noted in a spec comment)

Match semantics: `\b{key}\w*\b` word-boundary prefix, first-match-wins over ordered bands. Carve-outs go in **Band 1** so they outrank the general term. Exact-token needs (`partner`, `pm`) go through `_perform_subs` sentinels instead — different mechanism.

## 3. The Five Touch Points

All in `data-universe-pipelines` on the spec branch, one commit:

1. `src/utils/job_function_taxonomy.py` — keys in BAND_1_CARVEOUTS with a one-to-three-line comment (rationale + date, no examples — those go in the PR).
2. `test/utils/test_job_function_taxonomy.py::test_counts` — bump `len(SPEC)`, append a dated history comment line in the existing style.
3. `test/utils/test_job_function_taxonomy.py::test_ordering_carveouts` — `SPEC_INDEX["<carve-out>"] < SPEC_INDEX["<general term>"]`.
4. `test/utils/test_employment_utils.py` — one `test_<name>_carve_out` with raw-title assertions both ways: every leadership shape → new function, the mass shapes → old function. Include synonym-rewritten forms ("Vice President, X", "Senior Vice President of X").
5. `docs/job_function_taxonomy.md` — one row in the `## Keyword rulings` table (band | `key` | function | rationale). Drift tests check the keyword is real; one family-head row is enough.

Run: `make tests TESTS="test/utils/test_job_function_taxonomy.py test/utils/test_employment_utils.py test/scripts/test_job_function_volume.py"`.

## 4. Aftermath

- Re-run volume accounting and regenerate the workbook (see `taxonomy-workbook-regen`) — a carve-out makes every existing measurement stale.
- Attribution will come in below the psql measurement (first-match-wins: titles carrying an earlier-matching token never reach the new keys). Expected, not a bug — say so when reporting.
- Do not push without Vanessa's review. Vocabulary judgment gets its own commit/PR shape, separate from mechanical fixes.
