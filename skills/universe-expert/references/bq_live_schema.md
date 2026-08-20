# BigQuery materialized schema — live facts vs the Pydantic models

Point-in-time snapshot, verified via INFORMATION_SCHEMA **2026-06-09/11** (DAT-47 work).
Source of truth is NOT this file: the Pydantic models live in this repo (`src/data_types/`),
the materialized tables are produced by `data-universe-rails` RisingWave migrations, and the
live answer is always one INFORMATION_SCHEMA query away (refresh queries at the bottom).
Column lists below will drift; the structural invariants age slowly. Verify before relying.

## The one thing to internalize

**Pydantic models ≠ materialized tables.** The BQ tables in `gdulabs-production.data_universe`
track the Entity models' shapes but differ in storage and in a few load-bearing details below.

## Structural invariants (slow-aging; bit DAT-47 repeatedly)

- **Nested/repeated fields are JSON columns**, not native ARRAY<STRUCT>. Access pattern:
  `UNNEST(JSON_QUERY_ARRAY(col)) AS e` then `JSON_VALUE(e, '$.field')` (scalar) /
  `JSON_QUERY(e, '$.field')` (subtree). Cast numbers: `SAFE_CAST(JSON_VALUE(...) AS INT64)`.
  Empty is `[]` (NOT NULL) — `IS NOT NULL` checks on JSON array columns match empty arrays;
  filter with `ARRAY_LENGTH(JSON_QUERY_ARRAY(col)) > 0`.
- **No `is_primary` on employments.** Current/primary employment =
  `people.primary_employment_id -> employments.employment_id`. It is set ONLY when the person
  has a current employment; expect large null rates on some cohorts (DAT-47: ~16% of matched
  had no primary). Current employment = `end_year IS NULL` (not -1).
- **`locations.country_code` is already ISO 3166-1 alpha-2**; `region_code` is the bare
  subdivision (NY, ON), populated mainly for US/CA. ISO 3166-2 = CONCAT(country, '-', region).
- **`people.websites` has never been written by any ingestion** (confirmed 2026-06-11 via 1%
  TABLESAMPLE, 7.6M people: 100% `[]`). Twitter/github URLs exist only in raw vendor feeds.
- **Layer tables carry per-layer `source` + the bound entity id**: `person_layers` has
  `person_id`, `source`, `discarded_at` → per-person source provenance is a 3-column query.
  `employment_layers` has NO person_id (only `employment_id` + `person_layer_id`).
- **GDU does not materialize per-FIELD source** (lost at bind). Entity-level signals only:
  layer sources (above) and `external_identifiers` types.
- **people ≈ 760M rows** (1% sample = 7.6M, 2026-06-11).

## data_universe tables (2026-06-11)

employment_layers, employments, investment_layers, investment_partner_layers,
investment_partners, investments, location_layers, locations, organization_layers,
organizations, people, person_layers

Key columns (verified 2026-06-09/11; refresh before trusting):
- **people**: person_id, primary_employment_id, given_name, family_name, full_name, avatar_url,
  headline, summary, location_id, created_at, updated_at (scalar); emails, phone_numbers,
  linkedin_slugs, highlights, embeddings, external_identifiers, websites, languages (JSON).
- **employments**: employment_id, organization_id, organization_name, person_id, job_title,
  job_description, start_year/month, end_year/month, job_function, seniority, job_location,
  is_fulltime, job_type (scalar); board_roles, board_committee_memberships (JSON).
- **locations**: location_id, raw_location, city, region, region_code, country, country_code,
  latitude, longitude.
- **organizations**: organization_id, parent_organization_id, year_founded, logo_url,
  employee_count (scalar); organization_names, domains, websites, locations, addresses,
  industries, funding_events, external_identifiers, highlights, trading_identifiers (JSON).
- **person_layers**: id, person_id, location_layer_id, primary_employment_id, given/family/
  full_name, avatar_url, headline, summary, source, source_unique_id, discarded_at (+ JSON:
  source_metadata, phone_numbers, emails, highlights, linkedin_slugs, embeddings,
  external_identifiers, websites, languages).
- **investments**: investment_id, investor_name, investor_organization_id,
  investee_organization_id, investee_name, investment_type, funding_event_date (DATE),
  raised_amount (INT64), raised_amount_currency_code, role.
- **investment_partners**: investment_partner_id, person_id, investment_id, person_name —
  person-keyed deal participation (firm partners AND direct angels).

## data_universe_mixrank (raw feed staging; 2026-06-11)

| table | clustered by | columns |
|---|---|---|
| linkedin_profile_records | profile_id | file_path, read_at (TIMESTAMP), job_name, profile_id (INT64), profile_row (STRING = raw JSON) |
| linkedin_profile_slug_records | slug | file_path, read_at, job_name, slug (STRING), profile_slug_row (STRING) |
| linkedin_company_records | linkedin_company_id | file_path, read_at, job_name, linkedin_company_id (INT64), company_row (STRING) |

Gotchas (cost ~$600 of avoided scans on DAT-47):
- `linkedin_profile_records` is ~99TB. The only person key is INSIDE `profile_row` — a naive
  join scans everything. Prune via the `profile_id` clustering: resolve candidate profile_ids
  first, filter `WHERE profile_id IN UNNEST(ids)` (script variables work; estimates do NOT
  show cluster pruning — check bytes billed, not the pre-run estimate).
- The slug table's top-level `slug` column is **NULL** for `profile_slugs/feed/` files — the
  clustered column is unusable there. The JSON inside carries `person_id`,
  `linkedin_profile_id`, `linkedin_user_id`, `slug_status`.
- **The reliable person bridge**: GDU `people.external_identifiers[type=mixrank_person_id]`
  == raw `person_id` (100% of profiles). `linkedin_member_id` (= user_id) == profile_id in
  only ~56% — never join member_id -> profile_id alone.
- Feed holds re-snapshots: dedupe with `QUALIFY ROW_NUMBER() OVER (PARTITION BY ... ORDER BY
  read_at DESC) = 1`.
- The raw profile blob carries fields GDU never ingests: education, skills, follower_count,
  connection_count, certifications, publications, patents, awards, courses, volunteering,
  profile-level company_name/title.

## BQ usage notes (generic but earned here)

- `HAVING COUNT(DISTINCT person_id) = 1` with `ANY_VALUE(person_id) AS person_id` in the
  SELECT → "aggregations of aggregations" (HAVING binds the alias). Qualify the column.
- `CREATE TEMP TABLE` needs a script/session; small scratch tables are simpler in the console.
- `USING (col)` breaks once any joined table re-introduces the column; prefer explicit `ON`
  in long join chains.

## Refresh queries (console; metadata, free)

```sql
SELECT table_name FROM `gdulabs-production.data_universe.INFORMATION_SCHEMA.TABLES` ORDER BY table_name;

SELECT table_name, column_name, data_type
FROM `gdulabs-production.data_universe.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = '<table>' ORDER BY ordinal_position;

SELECT table_name, column_name, data_type
FROM `gdulabs-production.data_universe_mixrank.INFORMATION_SCHEMA.COLUMNS`
ORDER BY table_name, ordinal_position;
```
