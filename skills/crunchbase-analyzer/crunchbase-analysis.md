# Board Membership Data Analysis: Crunchbase to Employment Schema

**Date:** 2026-02-09
**Branch:** `feat/board-membership-schema`
**Phase 1 Status:** Complete
**Data Source:** Local Crunchbase PostgreSQL database (13 analytical queries, 3.2M jobs records)

---

## 1. Source Data Landscape

### Total Records by `job_type`

| job_type | count | % of total |
|----------|------:|----------:|
| `executive` | 2,212,757 | 68.5% |
| `employee` | 664,365 | 20.6% |
| `board_member` | 248,397 | 7.7% |
| `advisor` | 92,982 | 2.9% |
| `board_observer` | 9,633 | 0.3% |
| **Board subtotal** | **350,012** | **10.8%** |

The `job_type` field is a clean, structured enum in Crunchbase with exactly 5 values. Three of these (`board_member`, `advisor`, `board_observer`) map directly to the `EmploymentType` enum values.

### Crunchbase `jobs` Table Schema

| column_name | data_type | is_nullable |
|-------------|-----------|-------------|
| uuid | text | NO |
| name | text | YES |
| type | text | YES |
| permalink | text | YES |
| cb_url | text | YES |
| rank | integer | YES |
| created_at | timestamp | YES |
| updated_at | timestamp | YES |
| person_uuid | text | YES |
| person_name | text | YES |
| org_uuid | text | YES |
| org_name | text | YES |
| started_on | date | YES |
| ended_on | date | YES |
| is_current | boolean | YES |
| title | text | YES |
| job_type | text | YES |

### Current vs. Past Board Seats (`board_member` only)

| is_current | count | % |
|------------|------:|--:|
| `true` | 199,369 | 80.2% |
| `false` | 49,028 | 19.8% |

**Insight:** 4:1 current-to-past ratio. Crunchbase significantly over-represents *current* board members. Past seats are underreported. The system should treat `is_current=true` with no `ended_on` date as "presumed current, not confirmed ended."

---

## 2. Board Role Classification from Titles

### Top 50 Board/Advisor Titles

| title | count |
|-------|------:|
| Board Member | 66,376 |
| Advisor | 37,165 |
| Member of the Board of Directors | 22,523 |
| Board of Directors | 18,379 |
| Director | 10,453 |
| Chairman | 7,894 |
| Board Observer | 6,784 |
| Board of Director | 6,464 |
| Investor | 5,513 |
| Advisory Board Member | 5,256 |
| Chairman of the Board | 5,000 |
| Chairman of the Board of Directors | 3,952 |
| Mentor | 3,621 |
| Board Director | 3,278 |
| CEO | 3,058 |
| Advisory Board | 2,843 |
| Board Advisor | 2,546 |
| Senior Advisor | 2,450 |
| Strategic Advisor | 2,397 |
| Member of Board of Directors | 2,282 |
| Board member | 2,204 |
| Member of the Advisory Board | 2,129 |
| Member | 2,002 |
| Member Board Of Directors | 1,895 |
| Board Of Director | 1,761 |
| Board Of Directors | 1,687 |
| Founder | 1,486 |
| Managing Director | 1,324 |
| Co-Founder | 1,246 |
| Member of the Board of Trustees | 1,196 |
| Member Board of Directors | 1,171 |
| Member of the Board | 1,101 |
| Board of Advisors | 1,051 |
| Non-Executive Director | 1,026 |
| Executive Director | 972 |
| CTO | 911 |
| Board of Trustees | 907 |
| Board | 777 |
| Chairman Of The Board | 772 |
| Partner | 743 |
| Member Of The Board Of Advisors | 705 |
| President | 699 |
| Board Chairman | 696 |
| Member of the Board of Advisors | 692 |
| Outside Director | 685 |
| Independent Director | 656 |
| Technical Advisor | 641 |
| Member, Board of Directors | 629 |
| Boards of Directors | 624 |
| Non Executive Director | 550 |

### Board Role Category Distribution

| Board Role Category | job_count | unique_people | % of board jobs |
|---------------------|----------:|--------------:|----------------:|
| Exec/Founder (insider) | 100,364 | 66,994 | 38.9% |
| General Board Member | 96,636 | 62,927 | 37.4% |
| Chairman/Chair | 27,622 | 21,921 | 10.7% |
| Observer | 8,483 | 4,196 | 3.3% |
| Advisory Board | 7,459 | 6,599 | 2.9% |
| Investor (by title) | 7,424 | 3,868 | 2.9% |
| Explicitly Independent | 6,196 | 5,070 | 2.4% |
| Trustee | 3,785 | 3,358 | 1.5% |
| Lead Director | 61 | 59 | 0.0% |

### BoardRole Enum Validation

The existing `BoardRole` enum is **validated by the data**. All 6 values have corresponding Crunchbase records:

- **CHAIRMAN** (10.7%): 27,622 jobs. Clear signal from title patterns (`Chairman`, `Chairwoman`, `Chairperson`, `Vice Chair`).
- **DIRECTOR** (37.4%): 96,636 "general" board member titles. This is the catch-all.
- **OBSERVER** (3.3%): 8,483 jobs. Maps cleanly from `job_type = 'board_observer'` + title patterns.
- **ADVISOR** (2.9%): 7,459 jobs within board-type records. Maps from `job_type = 'advisor'`.
- **LEAD_DIRECTOR** (0.02%): Only 61 in Crunchbase, but critical for SEC/governance data. Validates keeping it as a future-proof enum value.
- **VICE_CHAIRMAN**: Subset of the Chairman/Chair bucket. Will appear explicitly when title parsing is implemented.

**Recommendation:** The existing `BoardRole` enum needs no changes. The VICE_CHAIRMAN value is worth keeping for SEC data even though Crunchbase volumes are low.

**New insight:** 38.9% are "insider" board seats where the person holds an exec title (CEO, Founder, etc.) on the board role itself. This directly feeds `is_independent` inference:

```
Title contains CEO/Founder/CxO on a board_member job -> is_independent = false (inferred)
Title contains "Independent" or "Non-Executive"      -> is_independent = true (explicit)
All others                                            -> is_independent = null (unknown)
```

---

## 3. Independence Classification

### Cross-Referencing Board Members' Other Jobs

| Independence Category | People Count | Implication |
|----------------------|-------------:|-------------|
| Other (general board only) | 102,458 | Unknown -- need SEC data |
| C-Suite/Executive | 78,519 | Likely insider |
| Investor/VC | 55,379 | Likely non-independent (financial interest) |
| Founder/Owner | 46,965 | Likely insider |
| Advisory | 14,975 | Context-dependent |
| Explicitly Independent | 5,454 | Confirmed independent |

### Investor Cross-Reference

**14,402 people** sit on a board AND are investment partners at the same company (39,403 board-investor-same-company relationships via the `investment_partners` table).

### Data-Driven Independence Heuristic

```
Priority 1: Title explicitly says "Independent" / "Non-Executive" -> is_independent = true
Priority 2: Person is investor in same company (investment_partners) -> is_independent = false
Priority 3: Person holds exec role at same company (jobs table)      -> is_independent = false
Priority 4: Title on board job contains CEO/Founder/CxO              -> is_independent = false
Default:    -> is_independent = null (unknown, await SEC data)
```

**Key finding:** The design doc states `is_independent` is "Not available in Crunchbase," but the data shows it can be **inferred for ~45% of board seats** using title-based heuristics and the investment_partners cross-reference.

---

## 4. Tenure Analysis

### Date Coverage

| Metric | Value |
|--------|------:|
| Total board jobs | 258,030 |
| Has start date | 144,504 (56.0%) |
| Has end date | 31,000 (12.0%) |
| Marked is_current=true | 206,301 |
| Marked is_current=false | 51,729 |
| Earliest start | 1000-01-01 (data quality issue) |
| Latest start | 2026-01-08 |

### Tenure Distribution (valid start dates only)

| Tenure Bucket | Count | % |
|---------------|------:|--:|
| < 1 year | 7,623 | 5.5% |
| 1-3 years | 16,848 | 12.0% |
| 3-5 years | 22,458 | 16.1% |
| **5-10 years** | **51,092** | **36.5%** |
| 10-20 years | 35,450 | 25.4% |
| 20+ years | 6,363 | 4.6% |

**Median tenure is 5-10 years**, consistent with industry norms. The existing `start_year`/`start_month`/`end_year`/`end_month` fields on `EmploymentLayer` already capture this. The Crunchbase `started_on` / `ended_on` date fields map directly.

**Recommendation:** Tenure calculations should use `started_on` -> `start_year`/`start_month` and `is_current` -> `end_year = -1` (existing convention for "known current"). For the "Seasoned Board Director 10+ years" highlight (LABL-02), the 25.4% in the 10-20 year bucket + 4.6% in 20+ gives ~42,000 qualifying people.

---

## 5. Concurrent Board Seats

### Distribution of Current Board Seats Per Person

| Seats | People | % |
|-------|-------:|--:|
| 1 seat | 102,525 | 78.3% |
| 2 seats | 14,377 | 11.0% |
| 3 seats | 5,529 | 4.2% |
| 4-5 seats | 4,488 | 3.4% |
| 6-10 seats | 3,079 | 2.4% |
| 11+ seats | 921 | 0.7% |

### Top Board Collectors (Current Seats)

| First Name | Last Name | Board Seats |
|------------|-----------|------------:|
| Bandel | Carano | 58 |
| Jim | Robinson | 56 |
| Robert | Nelsen | 56 |
| Promod | Haque | 54 |
| Nisa | Leung | 53 |
| William | Hu | 49 |
| Navin | Chaddha | 47 |
| Will | Griffith | 44 |
| Matt | Murphy | 42 |
| Glenn | Solomon | 42 |
| Jeff | Horing | 42 |
| Annie | Lamont | 42 |
| Venky | Ganesan | 41 |
| Oleg | Tscheltzoff | 41 |
| Lip-Bu | Tan | 41 |
| Stuart | Ellman | 40 |
| Mike | Goguen | 40 |
| Peter | Fenton | 39 |
| Peter | Wagner | 39 |
| Brad | Feld | 38 |
| Steven | Krausz | 38 |
| Scott | Sandell | 38 |
| Jeff | Bussgang | 38 |
| Mike | Volpi | 38 |
| Hans | Tung | 37 |

These are predominantly VCs sitting on many portfolio company boards.

**Recommended highlight thresholds for LABL-03:**

- `has_board_experience`: seat_count >= 1 (all 130,919 current board members)
- `serial_board_member`: seat_count >= 3 (14,017 people)
- `prolific_board_member`: seat_count >= 6 (4,000 people)

---

## 6. Executive and Board Overlap

| Metric | Value |
|--------|------:|
| Total board members (unique people) | 145,619 |
| Total executives (unique people) | 1,584,096 |
| Total advisors (unique people) | 66,048 |
| **Board members who are also executives** | **93,221 (64%)** |
| Board members who are also advisors | 17,653 (12%) |
| Executives who are also advisors | 45,440 |

**64% of board members also hold executive titles.** This validates:

- **BIND-01/BIND-02:** The binding discriminator using `employment_type` is critical -- without it, 93K people would have board and exec roles merged into a single Employment entity.
- The "Executives with board seats" search is served by: `WHERE employment_type = 'BOARD_MEMBER' AND person_id IN (SELECT person_id FROM employment WHERE employment_type = 'JOB' AND seniority IN ('C_SUITE','VP'))`.
- The "has board experience" filter is: `EXISTS (SELECT 1 FROM employment WHERE person_id = p.id AND employment_type IN ('BOARD_MEMBER','OBSERVER'))`.

---

## 7. Board Relationships (Shared Seats)

### Pairs of People Currently Sharing 2+ Board Seats

| Shared Boards | Pair Count |
|--------------:|-----------:|
| 15 | 1 |
| 12 | 1 |
| 11 | 1 |
| 9 | 1 |
| 8 | 3 |
| 7 | 6 |
| 6 | 11 |
| 5 | 23 |
| 4 | 87 |
| 3 | 276 |
| 2 | 3,452 |
| **Total** | **3,861 pairs** (avg 2.2 shared boards) |

**Recommendation:** Board relationships are a graph problem. For v1, the most practical approach is to **not model relationships as schema fields** but instead compute them at query time or as a derived view. Two Employment records with `employment_type = BOARD_MEMBER` at the same `organization_id` creates an implicit relationship.

Example query for "related board seats":

```sql
-- Find people who share boards with a given person
SELECT DISTINCT e2.person_id, COUNT(DISTINCT e1.organization_id) as shared_boards
FROM employment e1
JOIN employment e2 ON e1.organization_id = e2.organization_id
WHERE e1.person_id = @target_person
  AND e2.person_id != @target_person
  AND e1.employment_type = 'BOARD_MEMBER'
  AND e2.employment_type = 'BOARD_MEMBER'
GROUP BY e2.person_id
ORDER BY shared_boards DESC
```

---

## 8. Committee Data

Committee mentions are **sparse in Crunchbase** (~1,500 total records):

| Title | Count |
|-------|------:|
| Investment Committee Member | 161 |
| Investment Committee | 138 |
| Executive Committee Member | 101 |
| Committee Member | 100 |
| Steering Committee Member | 87 |
| Executive Committee | 87 |
| Advisory Committee Member | 68 |
| Member of the Executive Committee | 61 |
| Advisory Committee | 44 |
| Selection Committee | 44 |
| Chairman of the Audit Committee | 42 |
| Steering Committee | 40 |
| Board Member and Audit Committee Chair | 37 |
| Member of the Investment Committee | 35 |
| Member of the Board of Directors & Chairman of the Audit Committee | 30 |
| Member, Advisory Committee | 29 |
| Screening Committee | 23 |
| Audit & Supervisory Committee Member | 22 |
| Management Committee Member | 22 |
| Chairman of the Executive Committee | 21 |

**Recommendation:** The `committee_memberships: list[str]` field is correctly designed for future SEC data. For Crunchbase Phase 2, optional title parsing (e.g., "Board Member and Audit Committee Chair" -> `["Audit"]`) is possible but low priority given the volume. Save committee extraction for SEC DEF 14A data (v2).

---

## 9. Schema Validation Summary

The Phase 1 schema on `feat/board-membership-schema` is **well-validated by the data**:

| Field | Schema | Data Validation | Coverage |
|-------|--------|-----------------|----------|
| `employment_type` | `EmploymentType` enum (4 values) | Crunchbase `job_type` maps 1:1 to 3 board values | 100% of board jobs |
| `board_role` | `BoardRole` enum (6 values) | Title-based classification covers 63% explicitly | 63% classifiable |
| `is_independent` | `bool \| None` | Title + investor cross-ref covers ~45% | 45% inferable |
| `committee_memberships` | `list[str]` | ~1,500 records in Crunchbase; awaits SEC | <1% (correct to defer) |

### Suggested Addition: `TRUSTEE` BoardRole Value

3,785 jobs (1.5% of board roles) have "Trustee" titles. These are distinct from Directors in governance structure (typically nonprofits, universities, hospitals). Currently they would fall into `DIRECTOR`, losing the distinction.

### Future Consideration: `IndependenceSource` Enum (v2)

When inferring independence from multiple sources, tracking the *source* of the determination becomes valuable:

```python
class IndependenceSource(str, Enum):
    TITLE_EXPLICIT = "TITLE_EXPLICIT"         # Title says "Independent"
    TITLE_INSIDER = "TITLE_INSIDER"           # Title says CEO/Founder on board job
    INVESTOR_CROSSREF = "INVESTOR_CROSSREF"   # investment_partners table match
    SEC_FILING = "SEC_FILING"                 # DEF 14A proxy statement
```

This is a v2 concern and does not affect Phase 2 work.

---

## 10. Search Question Coverage

| Search Question | Schema Fields Used | Query Approach |
|----------------|-------------------|----------------|
| Executives with board seats (past & present) | `employment_type`, `end_year` | Filter `employment_type IN (BOARD_MEMBER, OBSERVER)` + join on person having exec employment |
| "Has board experience" filter | `employment_type` | `EXISTS` subquery on employment where `employment_type = BOARD_MEMBER` |
| Speed up board/exec shortlists | `employment_type`, `board_role` | Direct enum filter, no title parsing at query time |
| Membership | `employment_type` | `BOARD_MEMBER`, `OBSERVER`, `ADVISOR` enum values |
| Member (who) | `person_id` + `organization_id` | Standard employment join |
| Role | `board_role` | `CHAIRMAN`, `DIRECTOR`, etc. enum filter |
| Independence | `is_independent` | Boolean filter (with null = unknown) |
| Committees | `committee_memberships` | `ARRAY_CONTAINS` on repeated field (BQ) |
| Tenure dates | `start_year`/`start_month`/`end_year`/`end_month` | Existing fields, no schema change needed |
| Board relationships | Derived from shared `organization_id` | Join query on employment table (no new field needed) |

---

## Appendix: Crunchbase Tables Available

| Table | Relevance |
|-------|-----------|
| `jobs` | Primary source -- board member records with titles, dates, job_type |
| `people` | Person identity, demographics, featured job |
| `organizations` | Company data for board-company relationships |
| `investments` | Investor-company relationships (for independence cross-ref) |
| `investment_partners` | Individual partner-level investment data (key for independence) |
| `funding_rounds` | Links investments to companies |
| `investors` | Investor entity profiles |
| `acquisitions` | M&A data (board turnover context) |
| `ipos` | IPO events (governance transition trigger) |
| `org_parents` | Corporate hierarchy |
| `degrees` | Education (not directly relevant) |
| `events` | Industry events |
| `event_appearances` | Conference appearances |
| `funds` | Fund-level data |
| `category_groups` | Industry taxonomy |
| `people_descriptions` | Biographical text |
