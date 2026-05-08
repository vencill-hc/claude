# MixRank Query Patterns Reference

Extended query patterns for the MixRank people database. See SKILL.md for core patterns (person search, experience, skills).

## Person Profiling

**Full profile for a person:**
```sql
SELECT p.*, lp.headline, lp.summary, lp.industry_name,
       lp.connection_count, lp.follower_count,
       pl.locality, pl.country_region, pl.formatted_address
FROM persons p
LEFT JOIN linkedin_profiles lp ON lp.person_id = p.person_id
LEFT JOIN person_locations pl ON pl.person_id = p.person_id
WHERE p.person_id = 12345;
```

**Career history for a person:**
```sql
SELECT e.company_name, e.title, e.is_current,
       e.start_date, e.end_date, e.seniority, e.job_function
FROM experience e
WHERE e.person_id = 12345
ORDER BY e.start_date DESC NULLS LAST;
```

## Experience & Career Analysis

**Title distribution at a company:**
```sql
SELECT e.title, count(*) AS cnt
FROM experience e
WHERE e.company_name ILIKE '%microsoft%' AND e.is_current = true
GROUP BY e.title
ORDER BY cnt DESC
LIMIT 20;
```

## Talent Flow & Career Paths

**Where do alumni of a company go:**
```sql
SELECT e2.company_name AS destination, count(DISTINCT e1.person_id) AS alumni_count
FROM experience e1
JOIN experience e2 ON e1.person_id = e2.person_id AND e1.id != e2.id
WHERE e1.company_name ILIKE '%amazon%' AND e1.is_current = false
  AND e2.is_current = true
GROUP BY e2.company_name
ORDER BY alumni_count DESC
LIMIT 20;
```

**Company-to-company talent flow:**
```sql
SELECT p.name_full, e1.title AS title_at_source, e1.end_date,
       e2.title AS title_at_dest, e2.start_date
FROM experience e1
JOIN experience e2 ON e1.person_id = e2.person_id AND e1.id != e2.id
JOIN persons p ON p.person_id = e1.person_id
WHERE e1.company_name ILIKE '%google%' AND e2.company_name ILIKE '%meta%'
ORDER BY e2.start_date DESC NULLS LAST
LIMIT 20;
```

**Career paths to a specific role (e.g., CTO):**
```sql
SELECT prev.title AS previous_title, prev.company_name AS previous_company,
       curr.title AS current_title, curr.company_name AS current_company,
       p.name_full
FROM experience curr
JOIN experience prev ON curr.person_id = prev.person_id AND curr.id != prev.id
JOIN persons p ON p.person_id = curr.person_id
WHERE curr.title ILIKE '%chief technology officer%' AND curr.is_current = true
  AND prev.start_date < curr.start_date
ORDER BY prev.end_date DESC NULLS LAST
LIMIT 20;
```

## Skills Analysis

**Top skills overall:**
```sql
SELECT skill, count(*) AS cnt
FROM skills
GROUP BY skill
ORDER BY cnt DESC
LIMIT 30;
```

**Skills for people at a company:**
```sql
SELECT s.skill, count(DISTINCT s.person_id) AS cnt
FROM skills s
JOIN experience e ON e.person_id = s.person_id
WHERE e.company_name ILIKE '%apple%' AND e.is_current = true
GROUP BY s.skill
ORDER BY cnt DESC
LIMIT 20;
```

**Skill co-occurrence (what skills appear together):**
```sql
SELECT s2.skill AS co_skill, count(*) AS co_count
FROM skills s1
JOIN skills s2 ON s1.person_id = s2.person_id AND s1.skill != s2.skill
WHERE s1.skill = 'Data Science'
GROUP BY s2.skill
ORDER BY co_count DESC
LIMIT 20;
```

## Education Analysis

**Alumni of a school:**
```sql
SELECT p.name_full, p.current_company_name, p.current_title,
       ed.degree, ed.field_of_study
FROM education ed
JOIN persons p ON p.person_id = ed.person_id
WHERE ed.school_name ILIKE '%stanford%'
LIMIT 20;
```

**Degree distribution:**
```sql
SELECT degree, count(*) AS cnt
FROM education
WHERE degree IS NOT NULL
GROUP BY degree
ORDER BY cnt DESC
LIMIT 20;
```

**Top employers for alumni of a school:**
```sql
SELECT e.company_name, count(DISTINCT e.person_id) AS alumni_count
FROM education ed
JOIN experience e ON e.person_id = ed.person_id AND e.is_current = true
WHERE ed.school_name ILIKE '%mit%'
GROUP BY e.company_name
ORDER BY alumni_count DESC
LIMIT 15;
```

## Geographic & Demographic Analysis

**People by country:**
```sql
SELECT country_iso, country_name, count(*) AS cnt
FROM persons
GROUP BY country_iso, country_name
ORDER BY cnt DESC
LIMIT 20;
```

**People by city (using person_locations):**
```sql
SELECT pl.locality, pl.country_iso, count(*) AS cnt
FROM person_locations pl
WHERE pl.locality IS NOT NULL AND pl.locality != ''
GROUP BY pl.locality, pl.country_iso
ORDER BY cnt DESC
LIMIT 20;
```

**Industry distribution:**
```sql
SELECT lp.industry_name, count(*) AS cnt
FROM linkedin_profiles lp
WHERE lp.industry_name IS NOT NULL
GROUP BY lp.industry_name
ORDER BY cnt DESC
LIMIT 20;
```

**Seniority distribution (using experience arrays):**
```sql
SELECT unnest(seniority) AS level, count(*) AS cnt
FROM experience
WHERE seniority IS NOT NULL
GROUP BY level
ORDER BY cnt DESC;
```

## Certification & Language Analysis

**Top certifications:**
```sql
SELECT title, count(*) AS cnt
FROM certifications
WHERE title IS NOT NULL
GROUP BY title
ORDER BY cnt DESC
LIMIT 20;
```

**Top certification issuers:**
```sql
SELECT company_name, count(*) AS cnt
FROM certifications
WHERE company_name IS NOT NULL
GROUP BY company_name
ORDER BY cnt DESC
LIMIT 20;
```

**Multilingual professionals:**
```sql
SELECT p.name_full, p.country_iso, count(l.name) AS lang_count,
       array_agg(l.name) AS languages
FROM languages l
JOIN persons p ON p.person_id = l.person_id
GROUP BY p.person_id, p.name_full, p.country_iso
HAVING count(l.name) >= 3
ORDER BY lang_count DESC
LIMIT 20;
```
