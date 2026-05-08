# MixRank Database Schema Reference

Database: `mixrank` (PostgreSQL, localhost, no auth required)
Source: 100K LinkedIn-enriched person profiles from MixRank JSONL export
Extensions: `unaccent`, `pg_trgm`

---

## Table: persons (100,000 rows)

Core person entity. One row per person. Hub table that all others join to via `person_id`.

| Column | Type | Notes |
|--------|------|-------|
| person_id | BIGINT | PK, MixRank person ID |
| account_id | BIGINT | MixRank account ID (often same as person_id) |
| name_full | TEXT | Full name (GIN trigram indexed) |
| name_first | TEXT | First name |
| name_middle | TEXT | Middle name (often NULL) |
| name_last | TEXT | Last name (B-tree indexed) |
| name_nick | TEXT | Nickname (rarely populated) |
| name_suffix | TEXT | Suffix (Jr., III, etc.) |
| name_title | TEXT | Name prefix (Dr., Prof., etc.) |
| country_iso | TEXT | ISO 2-letter country code (B-tree indexed) |
| country_name | TEXT | Full country name |
| current_company_id | BIGINT | MixRank company ID for current job |
| current_company_name | TEXT | Current employer name (B-tree indexed) |
| current_title | TEXT | Current job title |
| current_start_date | DATE | Current job start date |
| privacy_redact | BOOLEAN | Privacy redaction flag |
| created_at | TIMESTAMPTZ | Record creation timestamp |
| updated_at | TIMESTAMPTZ | Record last update timestamp |

**Indexes:** person_id (PK), country_iso, name_last, current_company_name, name_full (GIN trigram)

### Key Values: country_iso (top 15)

| Value | Approx % |
|-------|----------|
| US | ~22% |
| IN | ~12% |
| BR | ~7% |
| GB | ~4% |
| DE | ~3% |
| ID | ~3% |
| FR | ~3% |
| CA | ~2% |
| MX | ~2% |
| ES | ~2% |
| NG | ~2% |
| AU | ~2% |
| IT | ~2% |
| PH | ~1.5% |
| PK | ~1.5% |

---

## Table: person_locations (95,020 rows)

Geocoded location data. 1:1 with persons (separate table to keep persons lean).

| Column | Type | Notes |
|--------|------|-------|
| person_id | BIGINT | PK, FK to persons |
| latitude | DOUBLE PRECISION | Geocoded latitude |
| longitude | DOUBLE PRECISION | Geocoded longitude |
| location_string | TEXT | Raw location string (e.g., "Detmold, North Rhine-Westphalia, Germany") |
| locality | TEXT | City/town name |
| admin_district | TEXT | State/province code (e.g., "CA", "NW") |
| admin_district2 | TEXT | County/district (e.g., "Lippe") |
| country_region | TEXT | Country name |
| country_iso | TEXT | ISO 2-letter country code |
| postal_code | TEXT | Postal/ZIP code (often empty) |
| formatted_address | TEXT | Formatted address string |
| neighborhood | TEXT | Neighborhood (often empty) |
| address_line | TEXT | Street address (often empty) |

**Indexes:** person_id (PK)

---

## Table: linkedin_profiles (100,000 rows)

LinkedIn profile metadata. 1:1 with persons.

| Column | Type | Notes |
|--------|------|-------|
| person_id | BIGINT | PK, FK to persons |
| profile_id | BIGINT | LinkedIn profile ID (can be negative) |
| user_id | BIGINT | LinkedIn user ID |
| slug | TEXT | LinkedIn URL slug |
| url | TEXT | Full LinkedIn profile URL |
| name | TEXT | Name as shown on LinkedIn |
| first_name | TEXT | LinkedIn first name |
| last_name | TEXT | LinkedIn last name |
| headline | TEXT | User-written headline/tagline |
| summary | TEXT | Profile summary (can be long, may contain newlines) |
| industry_id | INTEGER | LinkedIn industry ID (B-tree indexed) |
| industry_name | TEXT | LinkedIn industry name |
| company_name | TEXT | Current company per LinkedIn |
| title | TEXT | Current title per LinkedIn |
| linkedin_company_id | BIGINT | LinkedIn company ID for current employer |
| country_iso | TEXT | Country per LinkedIn |
| country_name | TEXT | Country name per LinkedIn |
| locality | TEXT | Location string per LinkedIn |
| profile_pic | TEXT | Profile picture URL |
| cover_image | TEXT | Cover image URL |
| connection_count | INTEGER | Number of connections |
| recommender_count | INTEGER | Number of recommendations received |
| follower_count | INTEGER | Number of followers |
| jobs_count | INTEGER | Number of jobs listed |
| slug_status | TEXT | Slug status ("A" = active) |
| is_incomplete | BOOLEAN | Whether profile is incomplete |
| is_memorial | BOOLEAN | Memorial/deceased profile flag |
| dob | DATE | Date of birth (rarely populated) |
| activity_at | TIMESTAMPTZ | Last activity timestamp |
| last_seen | TIMESTAMPTZ | Last time profile was observed |
| created_at | TIMESTAMPTZ | LinkedIn record creation |
| updated_at | TIMESTAMPTZ | LinkedIn record last update |

**Indexes:** person_id (PK), industry_id

---

## Table: experience (171,638 rows)

Work history entries. Multiple rows per person.

| Column | Type | Notes |
|--------|------|-------|
| person_id | BIGINT | FK to persons |
| id | BIGINT | LinkedIn experience entry ID |
| company_id | BIGINT | MixRank company ID (merged from top-level experience) |
| linkedin_company_id | BIGINT | LinkedIn company ID (different ID space) |
| is_current | BOOLEAN | Whether this is the current position |
| company_name | TEXT | Company name (GIN trigram indexed, B-tree indexed) |
| title | TEXT | Job title (GIN trigram indexed, B-tree indexed) |
| summary | TEXT | Role description/summary |
| locality | TEXT | Job location |
| start_date | DATE | Start date (may be year-only as YYYY-01-01) |
| start_date_year | INTEGER | Start year |
| start_date_month | INTEGER | Start month (NULL = year-only) |
| end_date | DATE | End date (NULL = current) |
| end_date_year | INTEGER | End year |
| end_date_month | INTEGER | End month |
| seniority | TEXT[] | Seniority classifications (e.g., {"Senior","Director"}) |
| job_function | TEXT[] | Job function classifications (e.g., {"Engineering","Management"}) |
| employment_type | TEXT[] | Employment type (e.g., {"Full-time"}) |
| academic_qualification | TEXT[] | Academic qualification level |

**PK:** (person_id, id)
**Indexes:** person_id, company_name, linkedin_company_id, is_current, title, company_name (GIN trigram), title (GIN trigram)

### Key Values: seniority

| Value |
|-------|
| Entry level |
| Associate |
| Mid-Senior level |
| Senior |
| Director |
| Vice President (VP) |
| Executive |
| Chief X Officer (CxO) |
| Owner |
| Partner |
| Manager |
| Internship |
| Unpaid / Internship |
| Not Applicable |

### Key Values: job_function

| Value |
|-------|
| Accounting, Administrative, Advertising, Analyst, Art / Creative |
| Business Development, Consulting, Customer Service, Design, Education |
| Engineering, Finance, General Business, Health Care Provider, Human Resources |
| Information Technology, Legal, Management, Manufacturing, Marketing |
| Other, Product Management, Production, Project Management, Public Relations |
| Purchasing, Quality Assurance, Research, Sales, Strategy / Planning |
| Supply Chain, Training, Writing / Editing |

### Key Values: employment_type

| Value |
|-------|
| Full-time |
| Part-time |
| Contract |
| Internship |
| Volunteer |
| Other |

### Array Query Examples

```sql
-- Find all Senior-level engineers
SELECT person_id, company_name, title
FROM experience
WHERE 'Senior' = ANY(seniority) AND 'Engineering' = ANY(job_function);

-- Find experience matching ANY of multiple seniority levels
SELECT person_id, company_name, title
FROM experience
WHERE seniority && ARRAY['Director', 'Vice President (VP)', 'Chief X Officer (CxO)'];

-- Unnest arrays for aggregation
SELECT unnest(seniority) AS level, count(*) FROM experience
WHERE seniority IS NOT NULL GROUP BY level ORDER BY count DESC;
```

---

## Table: education (71,754 rows)

Educational background. Multiple rows per person.

| Column | Type | Notes |
|--------|------|-------|
| education_id | BIGSERIAL | PK (auto-generated) |
| person_id | BIGINT | FK to persons |
| school_id | BIGINT | LinkedIn school ID (often NULL) |
| school_name | TEXT | School/university name (B-tree + GIN trigram indexed) |
| school_logo_url | TEXT | School logo URL |
| degree | TEXT | Degree name (free-text, not normalized) |
| field_of_study_id | BIGINT | LinkedIn field of study ID |
| field_of_study | TEXT | Field of study name |
| grade | TEXT | Grade/GPA (rarely populated) |
| activities | TEXT | Activities (rarely populated) |
| notes | TEXT | Additional notes |
| start_date | DATE | Start date |
| start_date_year | INTEGER | Start year |
| start_date_month | INTEGER | Start month |
| end_date | DATE | End date |
| end_date_year | INTEGER | End year |
| end_date_month | INTEGER | End month |

**Indexes:** education_id (PK), person_id, school_name, degree, school_name (GIN trigram)

### Key Values: degree (top 15, free-text)

Common patterns: "Bachelor of Science - BS", "Master of Business Administration - MBA", "Bachelor's degree", "Master's degree", "Doctor of Philosophy - PhD", "Bachelor of Arts - BA", "Associate's degree", etc.

Note: Degree values are NOT normalized. Use ILIKE patterns: `degree ILIKE '%bachelor%'`, `degree ILIKE '%mba%'`, `degree ILIKE '%phd%' OR degree ILIKE '%doctor%'`

---

## Table: skills (152,683 rows)

Professional skills. Multiple rows per person. ~65% of persons have at least one skill.

| Column | Type | Notes |
|--------|------|-------|
| person_id | BIGINT | FK to persons (composite PK) |
| skill | TEXT | Skill name (composite PK, B-tree + GIN trigram indexed) |

**PK:** (person_id, skill)
**Indexes:** person_id, skill, skill (GIN trigram)

### Top Skills (typical)

Microsoft Office, Leadership, Management, Communication, Teamwork, Project Management, Microsoft Excel, Customer Service, Public Speaking, Marketing, Sales, Research, Social Media, Strategic Planning, Team Leadership, Data Analysis, Python, JavaScript, SQL, etc.

---

## Table: certifications (25,039 rows)

Professional certifications and licenses.

| Column | Type | Notes |
|--------|------|-------|
| certification_id | BIGSERIAL | PK (auto-generated) |
| person_id | BIGINT | FK to persons |
| title | TEXT | Certification name |
| credential_id | TEXT | Credential ID string |
| verify_url | TEXT | Verification URL |
| summary | TEXT | Certification description |
| linkedin_company_id | BIGINT | LinkedIn company ID of issuer |
| company_id | BIGINT | MixRank company ID of issuer |
| company_name | TEXT | Issuing organization name |
| date_year | INTEGER | Issue year |
| date_month | INTEGER | Issue month |
| expire_date_year | INTEGER | Expiration year |
| expire_date_month | INTEGER | Expiration month |

**Indexes:** certification_id (PK), person_id

---

## Table: languages (18,694 rows)

Language proficiencies. ~12% of persons have language entries.

| Column | Type | Notes |
|--------|------|-------|
| language_id_seq | BIGSERIAL | PK (auto-generated) |
| person_id | BIGINT | FK to persons |
| language_id | INTEGER | LinkedIn language ID |
| name | TEXT | Language name (in that language, e.g., "português", "Deutsch") |
| proficiency_id | INTEGER | Proficiency level ID |
| proficiency | TEXT | Proficiency description |

**Indexes:** language_id_seq (PK), person_id

### Key Values: proficiency

| Value |
|-------|
| Native or bilingual proficiency |
| Full professional proficiency |
| Professional working proficiency |
| Limited working proficiency |
| Elementary proficiency |

Note: Language `name` is often in the original language (e.g., "polski" not "Polish", "Deutsch" not "German"). Use ILIKE for matching.

---

## Table: lookup_seniority (14 rows)

Reference table for seniority classifications.

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | PK |
| seniority | TEXT | Seniority level name (UNIQUE) |

---

## Table: lookup_job_function (35 rows)

Reference table for job function classifications.

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | PK |
| job_function | TEXT | Job function name (UNIQUE) |

---

## Table: lookup_employment_type (7 rows)

Reference table for employment type classifications.

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | PK |
| employment_type | TEXT | Employment type name (UNIQUE) |

---

## Table: lookup_industry (147 rows)

Reference table for LinkedIn industry classifications.

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | PK |
| industry_name | TEXT | Industry name (UNIQUE) |

---

## Join Patterns

### Hub-and-Spoke Model

All tables connect through `persons.person_id`:

```
persons.person_id  <--  person_locations.person_id    (1:1, location details)
persons.person_id  <--  linkedin_profiles.person_id   (1:1, LinkedIn metadata)
persons.person_id  <--  experience.person_id           (1:many, work history)
persons.person_id  <--  education.person_id            (1:many, schools/degrees)
persons.person_id  <--  skills.person_id               (1:many, skill tags)
persons.person_id  <--  certifications.person_id       (1:many, certs/licenses)
persons.person_id  <--  languages.person_id            (1:many, language proficiencies)
```

### Common Multi-Table Joins

**Full person profile with current job and location:**
```
persons -> linkedin_profiles (on person_id, 1:1)
        -> person_locations (on person_id, 1:1)
        -> experience (on person_id, WHERE is_current = true)
```

**People at a company with their skills:**
```
experience (WHERE company_name ILIKE ..., is_current = true)
-> persons (on person_id)
-> skills (on person_id)
```

**School alumni at a specific company:**
```
education (WHERE school_name ILIKE ...)
-> experience (on person_id, WHERE company_name ILIKE ...)
-> persons (on person_id)
```

**Industry breakdown of people with a skill:**
```
skills (WHERE skill = ...)
-> linkedin_profiles (on person_id)
GROUP BY industry_name
```

### Lookup Table Joins (optional, for validation)

The classification arrays on `experience` contain text values. Lookup tables map IDs to names but are not needed for most queries since the text values are stored directly in the arrays:

```sql
-- You can query directly:
SELECT * FROM experience WHERE 'Senior' = ANY(seniority);

-- Or validate against lookup:
SELECT * FROM lookup_seniority ORDER BY id;
```
