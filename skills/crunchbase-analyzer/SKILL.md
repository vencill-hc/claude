---
name: crunchbase-analyzer
description: >
  Analyze Crunchbase company, investor, funding, people, and acquisition data in a local
  PostgreSQL database (~15.5M rows, 16 tables). Use when asking questions about companies,
  investors, funding rounds, board members, IPOs, acquisitions, jobs, degrees, events, or funds.
  Triggers: "crunchbase", "company data", "investor data", "funding data", "board members",
  "who invested in", "how much funding", "IPO data", "acquisition data", "talent flow",
  "co-investors", "board overlap", "funding trends", "investor portfolio", "competitive landscape",
  "distribution analysis", "employee count", "category analysis", "education background",
  "career history", "fund size", "market map".
---

# Crunchbase Analyzer

You have access to a local PostgreSQL database (`crunchbase`) containing ~15.5M rows of Crunchbase data across 16 tables. Run queries directly via:

```bash
psql crunchbase -c "SQL HERE"
```

No authentication needed (localhost, current user).

## Tables at a Glance

| Table | Rows | Description |
|-------|------|-------------|
| organizations | 4,182,073 | Companies, investors, schools |
| jobs | 3,228,134 | Employment/role relationships |
| people | 2,099,280 | Individuals |
| people_descriptions | 1,503,913 | Bios (1:1 with people, same uuid) |
| investments | 1,274,720 | Investor participation in rounds |
| degrees | 1,108,126 | Educational background |
| funding_rounds | 762,747 | Funding events |
| event_appearances | 448,232 | Event participation |
| investors | 320,739 | Investor entities |
| investment_partners | 287,025 | Partner-level deal attribution |
| acquisitions | 197,127 | M&A events |
| ipos | 54,727 | IPO events |
| org_parents | 32,354 | Parent-child org relationships |
| events | 30,981 | Conferences/events |
| funds | 28,300 | Investment funds |
| category_groups | 804 | Category taxonomy |

For full column details, types, and enum values, see `references/schema.md`.

## Approach

When answering questions:
1. **Explain your approach** - describe what tables and joins you'll use and why
2. **Write the SQL** - run the query via psql
3. **Interpret results** - explain what the data means in context
4. **Suggest follow-ups** - offer related analyses the user might want

## Data Coverage

Our local DB contains 16 of Crunchbase's 47 available CSV collections. Loaded: organizations, people, people_descriptions, jobs, funding_rounds, investments, investors, investment_partners, acquisitions, ipos, funds, degrees, events, event_appearances, org_parents, category_groups. **Not loaded:** addresses, awards, categories, diversity_spotlights, growth_insights, key_employee_changes, layoffs, legal_proceedings, locations, ownerships, partnership_announcements, press_references, principals, products_insights, product_launches, r_and_d, organizations_similarity, and various prediction tables. If a question requires data from an unloaded collection, inform the user.

## Common Query Patterns

### Funding & Investment Analysis

**Total funding for a company:**
```sql
SELECT name, total_funding_usd, num_funding_rounds, last_funding_on
FROM organizations WHERE name ILIKE '%company_name%' AND primary_role = 'company';
```

**Funding rounds for a company:**
```sql
SELECT fr.investment_type, fr.announced_on, fr.raised_amount_usd,
       fr.post_money_valuation_usd, fr.investor_count
FROM funding_rounds fr
JOIN organizations o ON o.uuid = fr.org_uuid
WHERE o.name ILIKE '%company_name%'
ORDER BY fr.announced_on;
```

**Who invested in a company:**
```sql
SELECT i.investor_name, i.investor_type, i.is_lead_investor,
       fr.investment_type, fr.announced_on, fr.raised_amount_usd
FROM investments i
JOIN funding_rounds fr ON fr.uuid = i.funding_round_uuid
WHERE fr.org_uuid = (SELECT uuid FROM organizations WHERE name ILIKE '%company_name%' LIMIT 1)
ORDER BY fr.announced_on;
```

**Top investors by deal count:**
```sql
SELECT name, investment_count, investor_types, total_funding_usd
FROM investors
ORDER BY investment_count DESC NULLS LAST
LIMIT 20;
```

**Most funded companies:**
```sql
SELECT name, total_funding_usd, num_funding_rounds, status, country_code
FROM organizations
WHERE primary_role = 'company' AND total_funding_usd IS NOT NULL
ORDER BY total_funding_usd DESC
LIMIT 20;
```

### Company Profiling & Filtering

**Find companies by category:**
```sql
SELECT name, total_funding_usd, employee_count, status, country_code
FROM organizations
WHERE category_list ILIKE '%artificial intelligence%'
  AND primary_role = 'company'
ORDER BY total_funding_usd DESC NULLS LAST
LIMIT 20;
```

**Companies by location and size:**
```sql
SELECT name, total_funding_usd, employee_count, category_list
FROM organizations
WHERE country_code = 'USA' AND state_code = 'CA'
  AND employee_count IN ('101-250', '251-500')
  AND primary_role = 'company' AND status = 'operating'
ORDER BY total_funding_usd DESC NULLS LAST
LIMIT 20;
```

### Board & People Analysis

**Board members of a company:**
```sql
SELECT p.name, j.title, j.started_on, j.ended_on, j.is_current
FROM jobs j
JOIN people p ON p.uuid = j.person_uuid
WHERE j.org_uuid = (SELECT uuid FROM organizations WHERE name ILIKE '%company_name%' LIMIT 1)
  AND j.job_type = 'board_member'
ORDER BY j.started_on DESC NULLS LAST;
```

**Where a person has worked:**
```sql
SELECT j.org_name, j.title, j.job_type, j.started_on, j.ended_on, j.is_current
FROM jobs j
JOIN people p ON p.uuid = j.person_uuid
WHERE p.name ILIKE '%person_name%'
ORDER BY j.started_on DESC NULLS LAST;
```

**People with specific educational background:**
```sql
SELECT p.name, d.institution_name, d.degree_type, d.subject, d.completed_on
FROM degrees d
JOIN people p ON p.uuid = d.person_uuid
WHERE d.institution_name ILIKE '%stanford%'
  AND d.degree_type ILIKE '%mba%'
LIMIT 20;
```

### IPO & Acquisition Analysis

**Largest IPOs:**
```sql
SELECT org_name, went_public_on, stock_exchange_symbol, stock_symbol,
       money_raised_usd, valuation_price_usd, share_price_usd
FROM ipos
WHERE money_raised_usd IS NOT NULL
ORDER BY money_raised_usd DESC
LIMIT 20;
```

**Acquisitions by a company:**
```sql
SELECT acquiree_name, acquired_on, price_usd, acquisition_type
FROM acquisitions
WHERE acquirer_name ILIKE '%company_name%'
ORDER BY acquired_on DESC;
```

**Most acquisitive companies:**
```sql
SELECT acquirer_name, count(*) as acq_count,
       sum(price_usd) as total_spent_usd
FROM acquisitions
GROUP BY acquirer_name
ORDER BY acq_count DESC
LIMIT 20;
```

### Fund Analysis

**Funds raised by an investor:**
```sql
SELECT f.name, f.announced_on, f.raised_amount_usd
FROM funds f
JOIN investors inv ON inv.uuid = f.entity_uuid
WHERE inv.name ILIKE '%investor_name%'
ORDER BY f.announced_on DESC;
```

### Distribution & Market Analysis

**Funding distribution by stage:**
```sql
SELECT investment_type, count(*) as rounds,
       percentile_cont(0.5) WITHIN GROUP (ORDER BY raised_amount_usd) as median_usd,
       avg(raised_amount_usd) as avg_usd
FROM funding_rounds
WHERE raised_amount_usd IS NOT NULL AND raised_amount_usd > 0
GROUP BY investment_type ORDER BY rounds DESC;
```

**Category market map (top funded categories):**
```sql
SELECT unnest(string_to_array(category_list, ',')) AS category,
       count(*) as companies, sum(total_funding_usd) as total_funding
FROM organizations WHERE primary_role = 'company' AND category_list IS NOT NULL
GROUP BY category ORDER BY total_funding DESC NULLS LAST LIMIT 20;
```

**Employee size distribution for a category:**
```sql
SELECT employee_count, count(*) as cnt
FROM organizations
WHERE category_list ILIKE '%artificial intelligence%' AND primary_role = 'company'
GROUP BY employee_count ORDER BY cnt DESC;
```

### Network & Relationship Analysis

**Co-investors (who co-invests with a given investor):**
```sql
SELECT i2.investor_name, count(DISTINCT i1.funding_round_uuid) as co_investments
FROM investments i1
JOIN investments i2 ON i1.funding_round_uuid = i2.funding_round_uuid
  AND i1.investor_uuid != i2.investor_uuid
WHERE i1.investor_name ILIKE '%investor_name%'
GROUP BY i2.investor_name ORDER BY co_investments DESC LIMIT 20;
```

**Board overlap (companies sharing board members):**
```sql
SELECT j2.org_name, count(DISTINCT j1.person_uuid) as shared_members
FROM jobs j1
JOIN jobs j2 ON j1.person_uuid = j2.person_uuid AND j1.org_uuid != j2.org_uuid
WHERE j1.org_uuid = (SELECT uuid FROM organizations WHERE name ILIKE '%company%' LIMIT 1)
  AND j1.job_type = 'board_member' AND j2.job_type = 'board_member'
GROUP BY j2.org_name ORDER BY shared_members DESC LIMIT 20;
```

**Investor portfolio (all companies an investor backed):**
```sql
SELECT o.name, o.category_list, o.status, o.total_funding_usd,
       fr.investment_type, fr.announced_on
FROM investments i
JOIN funding_rounds fr ON fr.uuid = i.funding_round_uuid
JOIN organizations o ON o.uuid = fr.org_uuid
WHERE i.investor_name ILIKE '%investor_name%'
ORDER BY fr.announced_on DESC;
```

### Talent Flow & Career Analysis

**Talent flow between two companies:**
```sql
SELECT p.name, j1.title AS title_at_source, j1.ended_on,
       j2.title AS title_at_dest, j2.started_on
FROM jobs j1
JOIN jobs j2 ON j1.person_uuid = j2.person_uuid AND j1.org_uuid != j2.org_uuid
JOIN people p ON p.uuid = j1.person_uuid
WHERE j1.org_name ILIKE '%source_company%' AND j2.org_name ILIKE '%dest_company%'
ORDER BY j2.started_on DESC NULLS LAST;
```

**Where do alumni of a company go:**
```sql
SELECT j2.org_name, count(*) as alumni_count
FROM jobs j1
JOIN jobs j2 ON j1.person_uuid = j2.person_uuid AND j1.org_uuid != j2.org_uuid
WHERE j1.org_name ILIKE '%company_name%' AND j1.is_current = false AND j2.is_current = true
GROUP BY j2.org_name ORDER BY alumni_count DESC LIMIT 20;
```

### Trend Analysis

**Funding trends by year and stage:**
```sql
SELECT extract(year FROM announced_on) AS yr, investment_type,
       count(*) as rounds, sum(raised_amount_usd) as total_raised
FROM funding_rounds
WHERE announced_on IS NOT NULL AND raised_amount_usd IS NOT NULL
GROUP BY yr, investment_type ORDER BY yr DESC, total_raised DESC;
```

**IPO trends by year:**
```sql
SELECT extract(year FROM went_public_on) AS yr, count(*) as ipo_count,
       sum(money_raised_usd) as total_raised, avg(valuation_price_usd) as avg_valuation
FROM ipos WHERE went_public_on IS NOT NULL
GROUP BY yr ORDER BY yr DESC;
```

**Acquisition trends by year:**
```sql
SELECT extract(year FROM acquired_on) AS yr, count(*) as acq_count,
       sum(price_usd) as total_value, avg(price_usd) as avg_price
FROM acquisitions WHERE acquired_on IS NOT NULL
GROUP BY yr ORDER BY yr DESC;
```

## Join Cheat Sheet

```
organizations.uuid  <--  funding_rounds.org_uuid
organizations.uuid  <--  jobs.org_uuid
organizations.uuid  <--  ipos.org_uuid
organizations.uuid  <--  acquisitions.acquiree_uuid / acquirer_uuid
organizations.uuid  <--  org_parents.uuid (child) / parent_uuid (parent)
organizations.uuid  <--  funds.entity_uuid
organizations.uuid  <--  people.featured_job_organization_uuid
organizations.uuid  <--  degrees.institution_uuid (schools only)

people.uuid  <--  jobs.person_uuid
people.uuid  <--  people_descriptions.uuid (1:1, same PK)
people.uuid  <--  degrees.person_uuid
people.uuid  <--  investment_partners.partner_uuid

investors.uuid  <--  investments.investor_uuid
investors.uuid  <--  investment_partners.investor_uuid
investors.uuid  <--  funds.entity_uuid

funding_rounds.uuid  <--  investments.funding_round_uuid
funding_rounds.uuid  <--  investment_partners.funding_round_uuid

events.uuid  <--  event_appearances.event_uuid
```

## Performance Tips

- **Use `_usd` columns** for monetary comparisons (pre-converted, avoids currency issues)
- **Use indexed columns** in WHERE clauses: uuid PKs, org_uuid, person_uuid, investor_uuid, funding_round_uuid, country_code, status, primary_role, job_type
- **Use LIMIT** for exploratory queries on large tables (organizations, jobs, people)
- **Use ILIKE** for name matching (data is not consistently cased)
- **Filter by primary_role** when querying organizations to narrow scope (company vs investor vs school)
- **Use `string_to_array()` + `unnest()`** to split comma-separated fields for accurate GROUP BY analysis

## Data Quality Gotchas

- `employee_count` is a text range bucket ("1-10", "11-50", etc.), not a number
- `investor_types` in the investors table is comma-separated; use LIKE '%venture_capital%' to match
- `degree_type` is free-text and NOT normalized (BS, B.S., Bachelor of Science all exist). Use ILIKE patterns or group with CASE WHEN for aggregation
- `is_lead_investor` in investments is text ('true'/'false'), not boolean
- `category_list` and `category_groups_list` are comma-separated strings
- `roles` in organizations is comma-separated; an org can be both "company" and "investor"
- `lead_investor_uuids` in funding_rounds is comma-separated UUIDs, not a single FK
- Many monetary fields are NULL when undisclosed; filter `IS NOT NULL AND > 0` for accurate stats
- `founded_on`, `started_on`, `ended_on` dates can be partial (year-only shows as Jan 1)
- Organization names are not unique; always verify with uuid, domain, or additional filters
- `people_descriptions` is 1:1 with `people` sharing the same uuid PK, not a separate FK join
- The `rank` column on most tables is Crunchbase's internal popularity/importance score (lower = more prominent)
- `status` on organizations: 'operating', 'closed', 'acquired', 'ipo' — use to filter active companies
- `investment_type` values use underscores not spaces: 'series_a' not 'Series A'
