---
name: crunchbase-v2-analyzer
description: >
  Analyze Crunchbase Advanced Financials data (new CSV export API) in a local PostgreSQL database
  (crunchbase_v2). Single table: organizations (4.3M rows) with revenue_range, valuations, funding,
  employee bands, stock symbols, and more. Use for revenue coverage analysis, company profiling,
  and comparing against the legacy crunchbase database.
  Triggers: "crunchbase v2", "crunchbase new", "revenue range", "advanced financials",
  "crunchbase revenue", "new crunchbase data", "crunchbase_v2".
---

# Crunchbase V2 Analyzer (Advanced Financials)

You have access to a local PostgreSQL database (`crunchbase_v2`) containing 4,313,885 organization records from Crunchbase's newer CSV Export API (Advanced Financials package). This is **separate from** the legacy `crunchbase` database.

```bash
psql crunchbase_v2 -c "SQL HERE"
```

No authentication needed (localhost, current user).

## Tables

### `organizations` (materialized view — use this)

Clean, typed view of the raw data. **4,313,885 rows.**

| Column | Type | Description |
|--------|------|-------------|
| uuid | text | Crunchbase UUID (PK) |
| permalink | text | URL-safe identifier |
| name | text | Display name |
| legal_name | text | Legal entity name |
| short_description | text | One-line description |
| company_type | text | for_profit, non_profit, etc. |
| operating_status | text | active, closed, etc. |
| status | text | operating, was_acquired, closed, ipo |
| ipo_status | text | private, public, delisted |
| **revenue_range** | **text** | **Revenue band (see encoding below)** |
| num_employees_enum | text | Employee count band |
| funding_stage | text | seed, early_stage_venture, late_stage_venture, etc. |
| funding_total_usd | numeric | Total funding raised (USD) |
| equity_funding_total_usd | numeric | Equity funding (USD) |
| valuation_usd | numeric | Latest valuation (USD) |
| valuation_date | text | Date of latest valuation |
| founded_on | text | Founded date |
| last_funding_at | text | Last funding date |
| last_funding_type | text | Type of last funding round |
| listed_stock_symbol | text | Stock ticker (e.g., NASDAQ:AAPL) |
| stock_exchange_symbol | text | Exchange symbol |
| linkedin | text | LinkedIn URL |
| website_url | text | Company website |
| locations | text | Comma-separated locations (city, state, country) |
| location_groups | text | Region groups (Bay Area, West Coast, etc.) |
| categories | text | Comma-separated category names |
| category_groups | text | Comma-separated category group names |
| num_current_positions | int | Current employee positions tracked |
| num_funding_rounds | int | Total funding rounds |
| num_investments | int | Investments made (if investor) |
| num_acquisitions | int | Acquisitions made |
| rank | int | Crunchbase popularity rank (lower = more prominent) |
| rank_org | int | Organization-specific rank |
| updated_at | text | Last updated timestamp |
| created_at | text | Record creation timestamp |

### `organizations_raw` (staging — all 148 columns as TEXT)

Raw import of the full CSV. Use when you need columns not in the materialized view (e.g., founder names, investor names, diversity spotlights, image URLs).

## Revenue Range Encoding

| Code | Revenue Range | Count | % of All |
|------|--------------|-------|----------|
| `r_00000000` | Less than $1M | 398,154 | 9.2% |
| `r_00001000` | $1M – $10M | 1,669,186 | 38.7% |
| `r_00010000` | $10M – $50M | 312,170 | 7.2% |
| `r_00050000` | $50M – $100M | 51,833 | 1.2% |
| `r_00100000` | $100M – $500M | 53,657 | 1.2% |
| `r_00500000` | $500M – $1B | 14,331 | 0.3% |
| `r_01000000` | $1B – $10B | 12,025 | 0.3% |
| `r_10000000` | $10B+ | 4,045 | 0.1% |
| *(empty/null)* | No data | 1,798,484 | 41.7% |

**Human-readable helper:**
```sql
CASE revenue_range
    WHEN 'r_00000000' THEN '<$1M'
    WHEN 'r_00001000' THEN '$1M-$10M'
    WHEN 'r_00010000' THEN '$10M-$50M'
    WHEN 'r_00050000' THEN '$50M-$100M'
    WHEN 'r_00100000' THEN '$100M-$500M'
    WHEN 'r_00500000' THEN '$500M-$1B'
    WHEN 'r_01000000' THEN '$1B-$10B'
    WHEN 'r_10000000' THEN '$10B+'
    ELSE 'No data'
END AS revenue_label
```

## Employee Count Encoding

| Code | Range |
|------|-------|
| `c_00001_00010` | 1–10 |
| `c_00011_00050` | 11–50 |
| `c_00051_00100` | 51–100 |
| `c_00101_00250` | 101–250 |
| `c_00251_00500` | 251–500 |
| `c_00501_01000` | 501–1,000 |
| `c_01001_05000` | 1,001–5,000 |
| `c_05001_10000` | 5,001–10,000 |
| `c_10001_max` | 10,001+ |

## Indexes

- `idx_org_uuid` on uuid
- `idx_org_permalink` on permalink
- `idx_org_revenue` on revenue_range
- `idx_org_ipo` on ipo_status
- `idx_org_employees` on num_employees_enum
- `idx_org_name` on name

## Common Query Patterns

**Revenue coverage by segment:**
```sql
SELECT num_employees_enum, count(*) AS total,
    count(*) FILTER (WHERE revenue_range IS NOT NULL AND revenue_range != '') AS has_revenue,
    round(100.0 * count(*) FILTER (WHERE revenue_range IS NOT NULL AND revenue_range != '') / count(*), 2) AS pct
FROM organizations
GROUP BY num_employees_enum ORDER BY num_employees_enum;
```

**Find a company:**
```sql
SELECT name, permalink, revenue_range, num_employees_enum, ipo_status, listed_stock_symbol, funding_total_usd
FROM organizations WHERE name ILIKE '%company_name%' ORDER BY rank LIMIT 10;
```

**Large public companies with revenue:**
```sql
SELECT name, revenue_range, listed_stock_symbol, num_employees_enum, funding_total_usd
FROM organizations
WHERE listed_stock_symbol IS NOT NULL AND listed_stock_symbol != ''
    AND revenue_range IS NOT NULL AND revenue_range != ''
ORDER BY rank LIMIT 50;
```

**Cross-reference with legacy DB:**
```sql
-- Find companies in legacy DB that have revenue in v2
SELECT v2.name, v2.revenue_range, v2.num_employees_enum, v1.total_funding_usd AS legacy_funding
FROM crunchbase_v2.public.organizations v2
JOIN crunchbase.public.organizations v1 ON v2.uuid = v1.uuid
WHERE v2.revenue_range IS NOT NULL AND v2.revenue_range != ''
LIMIT 20;
```

## Relationship to Legacy Database

| Aspect | `crunchbase` (legacy) | `crunchbase_v2` (new) |
|--------|----------------------|----------------------|
| API | Bulk Export v4 | CSV Export (Advanced Financials) |
| Tables | 16 (orgs, people, jobs, funding, etc.) | 1 (organizations only, so far) |
| Rows | ~15.5M total | 4.3M organizations |
| Revenue field | **None** | **revenue_range** |
| Column naming | flat (e.g., `total_funding_usd`) | dotted in raw (e.g., `funding_total.value_usd`) |
| Join key | `uuid` | `uuid` (same UUIDs, cross-DB joins work) |

## Data Quality Notes

- **Duplicate entities**: Some companies have multiple records (e.g., Berkshire Hathaway at both `berkshire-hathaway` and `berkshire-hathaway-corp`). Use `rank` to find the canonical entry (lower rank = more prominent).
- **IPO status gaps**: Some clearly public companies (e.g., P&G) may show as `private`. Cross-reference with `listed_stock_symbol`.
- **Multi-value columns**: `categories`, `locations`, `category_groups` are comma-separated. Use `string_to_array()` + `unnest()` for grouping.
- **Revenue is crowdsourced**: Crunchbase's UX asks users to validate revenue ranges. Quality is good for large/public companies but less reliable for smaller/private ones.
- The `r_00000000` band appears to mean "less than $1M" and includes VC firms and pre-revenue startups.
