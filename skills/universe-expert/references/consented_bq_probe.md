# Consented BQ probe — the house pattern for one-off prod measurements

Read this before writing any ad-hoc script that touches `gdulabs-production`.
Prod access is SDK-only (never gsutil/gcloud/bq CLI) and consent is per-run,
per invocation, no carry-forward. Three scripts built to this shape on DAT-55
(2026-08-18) are the worked examples:
`workpod/projects/dat-55/threads/vvencill-dat-55-industry-labeling-investigation/`
(blast_radius.py, crunchbase_coverage.py, wearables_top50.py).

## The shape

- One self-contained script per question, in the workpod thread (not the repo,
  not /tmp). Docstring states the method and the exact `Run:` lines.
- `google.cloud.bigquery` client, project pinned. Run with the pipelines repo
  venv (`~/Documents/git/data-universe-pipelines/.venv/bin/python`) — it has
  the SDK; bare `uv run` does not.
- Dry-run by default: print `total_bytes_processed` per query and exit.
  `--execute` required to run. `maximum_bytes_billed` hard cap on every
  executed job (200 GiB default).
- Small inputs ship as ONE JSON string query parameter (`@edges_json` style),
  parsed in SQL with `UNNEST(JSON_QUERY_ARRAY(@param))`. No temp tables, no
  string-interpolated SQL values.
- Enum values imported from the repo's Pydantic types (e.g.
  `SourceName.UNIVERSE_LABELING.value`), never retyped as literals.
- Explicit `ON` joins, never `USING`. JSON columns per bq_live_schema.md
  (`UNNEST(JSON_QUERY_ARRAY(col))` + `JSON_VALUE`).
- Outputs: CSV written next to the script + a printed summary where every
  number carries a plain reading.

## Consent protocol (the part that has been gotten wrong)

- A user message describing work ("let's query BQ for X") is NOT consent.
  Consent is an affirmative answer to an explicit "may I run <script> against
  prod" question, per run. Dry-runs also hit the prod API: ask before those
  too unless the user just said "run the dry-runs".
- Re-runs after verdict/input changes are new runs: ask again.
- Cheap reruns are a feature, not a loophole — design scripts so a re-consented
  rerun is one command (verdict-set flags, --totals-only style scoping).

## Query-shape notes earned on DAT-55

- Employments joins dominate cost (~45-95 GiB per shape); a COUNT(DISTINCT
  person_id) subquery re-scans employments — budget for it.
- Distinct-union questions ("how many total X affected") cannot be answered
  from per-item CSVs (double counting across items and within orgs); they need
  their own union query.
- Wall time is compute-bound on wide joins, not scan-bound; minutes are normal.
