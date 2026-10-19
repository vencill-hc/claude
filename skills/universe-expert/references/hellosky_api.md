# HelloSky Enterprise API — working notes

Dated snapshot, 2026-10-19. The docs are the reference for anything not here: https://api.hellosky.ai/enterprise/docs
(machine-readable: https://api.hellosky.ai/enterprise/openapi.json). Do not answer shape questions from the UI-export
psql table or the vendor workbooks; those are stand-ins (memory: hellosky-api-docs-are-gold).

## Access

- Base URL `https://api.hellosky.ai/enterprise` (not `/v1`; the spec's `servers` entry is `/enterprise`).
- Auth header `X-API-Key`. Only VV holds the key; scripts read `HELLOSKY_API_KEY` from the environment and she runs
  them. Never ask for the key.
- Every response carries `credits_consumed` and `credits_remaining`. As of 2026-10-19 the key reports 0 and 0 on every
  call: unmetered. `GET /credits` is free and shows the balance. Rate limit 100 req/s.

## What is live and what is not

- Live: `GET /companies/{id}`, `POST /companies/batch` (≤100 ids, same `include` values as the single GET, returns
  `companies`, `not_found`, `redirects`), `POST /companies/search`, `/companies/{id}/subsidiaries`, `/acquisitions`,
  `POST /companies/leadership-team` and `/board-members` (≤5 companies per call), people and investors endpoints,
  companies-lists, `GET /filters/sectors`, `GET /credits`, `GET /usage`.
- Answers 501 ("Not yet available in this release"): `POST /exports`, `GET /exports/{id}`, `GET /changes`, webhooks.
  The ingestion plan (workpod `hellosky-ingestion/vvencill-hellosky-ingestion-pipeline`) is built on exports; until
  they ship, sampling and any interim landing go through `POST /companies/batch`. There is no endpoint that lists every
  licensed company id (vendor question 13).

## Company object

`include=company` returns the enriched profile; the nine block values (`financials`, `market`, `ownership`,
`structure`, `transactions`, `compensation`, `governance`, `details`, `documents`) or `all_company_data` each add a key
of the same name. Blocks carry `availability` and `last_updated`.

Profile keys and shapes, from the 180-company sample:
- `names`: list of plain strings, 1 to 5, no primary flag.
- `social_urls`: objects `{type, url}`; types linkedin, crunchbase, twitter, facebook, wikipedia. LinkedIn is a
  `/company/` page.
- `website_domains`: bare domains, one per company.
- `headquarter_locations`: objects `{address, city, state, postal_code, country}` with ISO-2 country; one per company.
- `sectors`: flat list of strings, up to 20, includes business-model tags (B2B, B2C, B2G, Services,
  Product/Manufacturing). `primary_sector` is a separate scalar, a member of `sectors` in all but one case, and not
  position 0 (first in 17 of 174). `customer_sectors`: the sectors a company sells into. `primary_customer_segment`:
  Enterprise / Mid-Market / Small-Medium or null.
- `headcounts`: yearly series `{date, headcount}` that reads like a LinkedIn member count (Deutsche Telekom 14,260).
  `resolved_headcount` `{headcount, resolved_at}` is the grounded figure, filled for 31/180. No block carries a
  headcount; `financials.periods` is revenue/EBIT/assets only.
- `revenues` `{date, amount_usd, is_predicted}`; `resolved_revenue` `{amount_usd, year, resolved_at, confidence}`.
- `status`: Public / Private / Acquired / Closed / null. `asset_class`: Pre-Funding, Public, Acquired, PE-Primary,
  PE-Backed, VC-Backed, null. Neither is the workbook's ownership type.
- `founded_on` date string; `last_updated` timestamp; `logo_urls`, `stock_tickers`, `market_cap`, `deals`, `events`
  (cxo changes with person ids), `active_investors`.

Empty for every sample company as of 2026-10-19, though documented and filled in the docs' ABB example (vendor
question 14): `investor_id`, `market.identifiers` (cik/lei/isin/figi), `financials.not_applicable_fields`.
`primary_sector` was in the same state until HelloSky fixed it the same day; refetch before assuming a field is dead.

## Local artifacts (workpod `hellosky-ingestion/threads/vvencill-hellosky-company-export-exploration`)

- `fetch_companies_batch.py`: stdlib pull by id list through `/companies/batch`, resumable, default include
  `company` + `all_company_data`; writes `companies.jsonl` and `batches.jsonl` under `data/hellosky_api_<date>[_suffix]/`.
  A rerun into an existing directory skips every id already present, so refetches need a new `--out-dir`.
- `hellosky_api_load.py`: loads a pull into local psql `reference_data.hellosky_api_companies` (scalar columns plus
  the whole object in `doc` jsonb; drop + reload). Query blocks with jsonb paths.
- `filled_paths.jq`: per-path count of companies with the path filled; `data/.../filled_paths.tsv` is the result.
- `data/hellosky_enterprise_openapi_2026-10-19.json`: dated spec copy; `profile_examples.txt`, `profile_fill.txt`,
  `keys_docs_example_vs_4879.txt`, `compare_to_workbook.txt` beside the pulls.
- Sample ids: `data/sampleverse_2026-10-14_org_ids.txt` (the 180 SampleVerse companies). ABB is 37739, Deutsche
  Telekom 4879.

Vendor questions and their reasons live in the pipeline thread's notes.md; placeholders P1 to P12 there name what each
answer unblocks.
