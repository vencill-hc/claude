---
name: mixrank-analyzer
description: >
  Analyze MixRank LinkedIn-enriched people data in a local PostgreSQL database
  (100K professional profiles, 12 tables). Use when asking about people, careers,
  skills, education, companies, talent pools, workforce analysis, or professional
  profiles.
  Triggers: "mixrank", "people data", "linkedin data", "talent data", "career history",
  "job titles", "skills analysis", "who works at", "workforce analysis", "talent pool",
  "professional profiles", "geographic talent", "industry analysis", "seniority analysis",
  "school alumni", "skill distribution", "career path", "hiring patterns", "talent flow".
  Do NOT use for crunchbase data queries, company research, investor/funding analysis,
  IPO data, or acquisition data — use crunchbase-analyzer instead. Do NOT use for
  general company lookups without a people/talent angle.
---

# MixRank People Analyzer

You have access to a local PostgreSQL database (`mixrank`) containing ~100K LinkedIn-enriched professional profiles across 12 tables. Run queries directly via:

```bash
psql mixrank -c "SQL HERE"
```

No authentication needed (localhost, current user).

## Tables at a Glance

| Table | Rows | Description |
|-------|------|-------------|
| persons | 100,000 | Core entity: name, country, current job |
| person_locations | 95,020 | Geocoded lat/lng, city, state, country |
| linkedin_profiles | 100,000 | Profile metadata, headline, summary, industry |
| experience | 171,638 | Work history: company, title, dates, classifications |
| education | 71,754 | Schools, degrees, fields of study |
| skills | 152,683 | Skill names per person |
| certifications | 25,039 | Professional certifications with issuer |
| languages | 18,694 | Language proficiencies |
| lookup_seniority | 14 | Reference: seniority levels |
| lookup_job_function | 35 | Reference: job function categories |
| lookup_employment_type | 7 | Reference: employment types |
| lookup_industry | 147 | Reference: industry classifications |

For full column details, types, and key value distributions, see `references/schema.md`.

## Data Coverage

- **Geographic:** 96 countries. ~22% US, ~12% India, ~7% Brazil, ~4% UK, then Germany, Indonesia, France, etc.
- **Experience:** 171,638 entries across 100K persons (avg ~1.7 per person; many have 3-5)
- **Education:** 71,754 entries (~72% of persons have at least one)
- **Skills:** 152,683 entries (~65% of persons have skills listed)
- **Certifications:** 25,039 entries (~15% of persons)
- **Languages:** 18,694 entries (~12% of persons)
- **Industry:** Assigned on linkedin_profiles via industry_id/industry_name

## International Data

The dataset is heavily international with diacritics, non-Latin characters, and multilingual names. Use `unaccent()` and trigram search:

```sql
-- Find people named "Müller" regardless of diacritics
SELECT name_full FROM persons WHERE unaccent(name_full) ILIKE '%muller%' LIMIT 10;

-- Fuzzy name search (trigram similarity)
SELECT name_full, similarity(name_full, 'Joao Silva') AS sim
FROM persons
WHERE name_full % 'Joao Silva'
ORDER BY sim DESC LIMIT 10;
```

## Approach

When answering questions:
1. **Explain your approach** — describe what tables and joins you'll use and why
2. **Write the SQL** — run the query via psql
3. **Interpret results** — explain what the data means in context
4. **Suggest follow-ups** — offer related analyses the user might want

## Common Query Patterns

For the full catalog of 20+ query patterns (talent flow, skills, education, geographic, certifications, languages), see `references/query-patterns.md`.

### Person Search

**Find a person by name:**
```sql
SELECT p.person_id, p.name_full, p.country_iso, p.current_company_name, p.current_title
FROM persons p
WHERE p.name_full ILIKE '%john smith%'
LIMIT 10;
```

**Fuzzy name search (handles typos and diacritics):**
```sql
SELECT p.name_full, p.country_iso, p.current_company_name,
       similarity(unaccent(p.name_full), unaccent('Francois Dupont')) AS sim
FROM persons p
WHERE unaccent(p.name_full) % unaccent('Francois Dupont')
ORDER BY sim DESC LIMIT 10;
```

### Experience & Career

**People currently at a company:**
```sql
SELECT p.name_full, e.title, e.seniority, e.start_date
FROM experience e
JOIN persons p ON p.person_id = e.person_id
WHERE e.company_name ILIKE '%google%' AND e.is_current = true
ORDER BY e.start_date
LIMIT 20;
```

**Top employers by headcount:**
```sql
SELECT e.company_name, count(DISTINCT e.person_id) AS headcount
FROM experience e
WHERE e.is_current = true AND e.company_name IS NOT NULL
GROUP BY e.company_name
ORDER BY headcount DESC
LIMIT 20;
```

### Skills

**People with a specific skill combination:**
```sql
SELECT p.name_full, p.current_company_name, p.current_title
FROM persons p
WHERE p.person_id IN (
    SELECT person_id FROM skills WHERE skill = 'Python'
    INTERSECT
    SELECT person_id FROM skills WHERE skill = 'Machine Learning'
)
LIMIT 20;
```

## Join Cheat Sheet

`persons.person_id` is the hub connecting all tables:

```
persons.person_id  <--  person_locations.person_id    (1:1)
persons.person_id  <--  linkedin_profiles.person_id   (1:1)
persons.person_id  <--  experience.person_id           (1:many)
persons.person_id  <--  education.person_id            (1:many)
persons.person_id  <--  skills.person_id               (1:many)
persons.person_id  <--  certifications.person_id       (1:many)
persons.person_id  <--  languages.person_id            (1:many)
```

All joins use `person_id`. There are no cross-table joins beyond this hub pattern.

## Troubleshooting

If `psql mixrank` fails with "connection refused" or "database does not exist", check: `pg_isready -d mixrank`. The database runs on localhost with no auth — ensure PostgreSQL is running.

## Performance Tips

- **Use indexed columns** in WHERE: `persons.country_iso`, `persons.name_last`, `experience.company_name`, `experience.is_current`, `experience.title`, `education.school_name`, `skills.skill`
- **Trigram indexes** exist on: `persons.name_full`, `experience.company_name`, `experience.title`, `education.school_name`, `skills.skill` — these accelerate ILIKE and `%` (similarity) queries
- **Use `unaccent()`** when searching international names: `WHERE unaccent(name_full) ILIKE '%muller%'`
- **Use LIMIT** on exploratory queries — experience and skills tables are large
- **Array operators** for classification fields: `'Senior' = ANY(seniority)`, `seniority && ARRAY['Senior', 'Director']` (overlap)
- **Avoid** `SELECT *` on experience — join only the columns you need

## Data Quality Gotchas

- **Company names are not normalized:** "Google", "Google LLC", "Google Inc.", "Alphabet Inc." are separate strings. Use ILIKE with wildcards or aggregate with similarity functions.
- **Year-only dates:** Many start/end dates show as `YYYY-01-01` when only the year was provided. Check `start_date_year`/`start_date_month` columns for the original granularity (month=NULL means year-only).
- **Classification arrays:** `seniority`, `job_function`, `employment_type`, `academic_qualification` on experience are `TEXT[]`. Use `= ANY(col)` or `@>` operators, not `=`.
- **Skills sparsity:** ~35% of persons have no skills listed. Skill-based queries will systematically exclude these people.
- **Headline vs title:** `linkedin_profiles.headline` is the user-written tagline (e.g., "Passionate about AI"). `linkedin_profiles.title` and `experience.title` are actual job titles. Don't confuse them.
- **NULL semantics:** NULL in classification arrays means "not classified," not "none." Empty array `{}` would mean explicitly empty (rare).
- **Negative IDs:** Some `profile_id` and `linkedin_company_id` values are negative. This is normal MixRank encoding — treat them as opaque identifiers.
- **Duplicate experience entries:** Some persons have near-duplicate experience records (same company/title, slightly different dates). The ETL deduplicates on `(person_id, id)` but some semantic duplicates may remain.
- **Current job mismatch:** `persons.current_company_name` (from MixRank's `job` field) may differ from the latest `experience` entry with `is_current=true`. The experience table is more reliable for current role analysis.
- **Industry is person-level:** `industry_id`/`industry_name` on `linkedin_profiles` reflects the person's self-selected industry, not a company-level classification.
