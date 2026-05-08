# Crunchbase Database Schema Reference

Database: `crunchbase` (PostgreSQL, localhost, no auth required)
Total: ~15.5M rows across 16 tables (of 47 available Crunchbase CSV collections)

Per the [Crunchbase Data Dictionary](https://data.crunchbase.com/docs/data-dictionary), each entity has a defined set of fields (Entity Name + Field Name). Our local DB contains the core collections. Collections NOT loaded include: addresses, awards, categories, closure_predictions, diversity_spotlights, funding_predictions, growth_insights, growth_predictions, investor_insights, investor_matches, ipo_predictions, key_employee_changes, layoffs, layoff_predictions, legal_proceedings, locations, organizations_similarity, ownerships, partnership_announcements, press_references, principals, products_insights, product_launches, r_and_d, remain_private_predictions, and acquisition_predictions.

---

## Table: organizations (4,182,073 rows)

Core company/school/investor entity table.

| Column | Type | Notes |
|--------|------|-------|
| uuid | text | PK |
| name | text | |
| type | text | |
| permalink | text | |
| cb_url | text | Crunchbase URL |
| rank | integer | |
| created_at | timestamp | |
| updated_at | timestamp | |
| legal_name | text | |
| roles | text | Comma-separated: "company", "investor", "school" |
| domain | text | Website domain |
| homepage_url | text | |
| country_code | text | ISO 2-letter (indexed) |
| state_code | text | |
| region | text | |
| city | text | |
| address | text | |
| postal_code | text | |
| status | text | (indexed) |
| short_description | text | |
| category_list | text | Comma-separated categories |
| category_groups_list | text | Comma-separated category groups |
| num_funding_rounds | integer | |
| total_funding_usd | numeric | Pre-converted to USD |
| total_funding | numeric | Original currency |
| total_funding_currency_code | text | |
| founded_on | date | |
| last_funding_on | date | |
| closed_on | date | |
| employee_count | text | Range bucket string |
| email | text | |
| phone | text | |
| facebook_url | text | |
| linkedin_url | text | |
| twitter_url | text | |
| logo_url | text | |
| alias1 | text | |
| alias2 | text | |
| alias3 | text | |
| primary_role | text | (indexed) |
| num_exits | integer | |

**Indexes:** uuid (PK), country_code, primary_role, status

### Key Values: status
| Value | Count |
|-------|-------|
| operating | 3,751,463 |
| closed | 252,251 |
| acquired | 134,113 |
| ipo | 44,238 |

### Key Values: primary_role
| Value | Count |
|-------|-------|
| company | 4,040,884 |
| investor | 110,200 |
| school | 30,989 |

### Key Values: employee_count
| Value | Count |
|-------|-------|
| 1-10 | 1,214,559 |
| 11-50 | 1,515,202 |
| 51-100 | 350,142 |
| 101-250 | 244,260 |
| 251-500 | 107,293 |
| 501-1000 | 73,384 |
| 1001-5000 | 65,316 |
| 5001-10000 | 14,435 |
| 10000+ | 18,033 |
| unknown | 579,449 |

---

## Table: people (2,099,280 rows)

Individual people (founders, executives, board members, etc.)

| Column | Type | Notes |
|--------|------|-------|
| uuid | text | PK |
| name | text | |
| type | text | |
| permalink | text | |
| cb_url | text | |
| rank | integer | |
| created_at | timestamp | |
| updated_at | timestamp | |
| first_name | text | |
| last_name | text | |
| gender | text | Primarily: male, female, not_provided |
| country_code | text | (indexed) |
| state_code | text | |
| region | text | |
| city | text | |
| featured_job_organization_uuid | text | (indexed) Links to organizations.uuid |
| featured_job_organization_name | text | |
| featured_job_title | text | |
| facebook_url | text | |
| linkedin_url | text | |
| twitter_url | text | |
| logo_url | text | |

**Indexes:** uuid (PK), country_code, featured_job_organization_uuid

---

## Table: people_descriptions (1,503,913 rows)

Extended bios/descriptions for people.

| Column | Type | Notes |
|--------|------|-------|
| uuid | text | PK, same as people.uuid |
| name | text | |
| type | text | |
| permalink | text | |
| cb_url | text | |
| rank | integer | |
| created_at | timestamp | |
| updated_at | timestamp | |
| description | text | Full bio text |

**Indexes:** uuid (PK)

---

## Table: jobs (3,228,134 rows)

Employment/role relationships between people and organizations.

| Column | Type | Notes |
|--------|------|-------|
| uuid | text | PK |
| name | text | |
| type | text | |
| permalink | text | |
| cb_url | text | |
| rank | integer | |
| created_at | timestamp | |
| updated_at | timestamp | |
| person_uuid | text | (indexed) Links to people.uuid |
| person_name | text | |
| org_uuid | text | (indexed) Links to organizations.uuid |
| org_name | text | |
| started_on | date | |
| ended_on | date | |
| is_current | boolean | |
| title | text | Job title |
| job_type | text | (indexed) |

**Indexes:** uuid (PK), person_uuid, org_uuid, job_type

### Key Values: job_type
| Value | Count |
|-------|-------|
| executive | 2,212,757 |
| employee | 664,365 |
| board_member | 248,397 |
| advisor | 92,982 |
| board_observer | 9,633 |

---

## Table: funding_rounds (762,747 rows)

Individual funding rounds for organizations.

| Column | Type | Notes |
|--------|------|-------|
| uuid | text | PK |
| name | text | |
| type | text | |
| permalink | text | |
| cb_url | text | |
| rank | integer | |
| created_at | timestamp | |
| updated_at | timestamp | |
| country_code | text | |
| state_code | text | |
| region | text | |
| city | text | |
| investment_type | text | |
| announced_on | date | |
| raised_amount_usd | numeric | Pre-converted to USD |
| raised_amount | numeric | Original currency |
| raised_amount_currency_code | text | |
| post_money_valuation_usd | numeric | Pre-converted to USD |
| post_money_valuation | numeric | |
| post_money_valuation_currency_code | text | |
| investor_count | integer | |
| org_uuid | text | (indexed) Links to organizations.uuid |
| org_name | text | |
| lead_investor_uuids | text | Comma-separated UUIDs |

**Indexes:** uuid (PK), org_uuid

### Key Values: investment_type (top 15)
| Value | Count |
|-------|-------|
| seed | 191,884 |
| series_unknown | 96,231 |
| grant | 79,929 |
| pre_seed | 71,657 |
| series_a | 71,179 |
| series_b | 33,426 |
| debt_financing | 33,134 |
| angel | 29,888 |
| post_ipo_equity | 26,220 |
| non_equity_assistance | 26,181 |
| private_equity | 23,970 |
| series_c | 14,755 |
| convertible_note | 11,733 |
| post_ipo_debt | 11,568 |
| equity_crowdfunding | 8,959 |

Full list: corporate_round, undisclosed, series_d, secondary_market, series_e, product_crowdfunding, initial_coin_offering, post_ipo_secondary, series_f, series_g, series_h, series_i, series_j

---

## Table: investments (1,274,720 rows)

Individual investor participation in funding rounds.

| Column | Type | Notes |
|--------|------|-------|
| uuid | text | |
| name | text | |
| type | text | |
| permalink | text | |
| cb_url | text | |
| rank | integer | |
| created_at | timestamp | |
| updated_at | timestamp | |
| funding_round_uuid | text | (indexed) Links to funding_rounds.uuid |
| funding_round_name | text | |
| investor_uuid | text | (indexed) Links to investors.uuid |
| investor_name | text | |
| investor_type | text | "organization" or "person" |
| is_lead_investor | text | Text field, not boolean |

**Indexes:** funding_round_uuid, investor_uuid

---

## Table: investors (320,739 rows)

Investor entities (VCs, angels, PE firms, etc.)

| Column | Type | Notes |
|--------|------|-------|
| uuid | text | PK |
| name | text | |
| type | text | |
| permalink | text | |
| cb_url | text | |
| rank | integer | |
| created_at | timestamp | |
| updated_at | timestamp | |
| roles | text | Comma-separated |
| domain | text | |
| country_code | text | (indexed) |
| state_code | text | |
| region | text | |
| city | text | |
| investor_types | text | Comma-separated |
| investment_count | integer | |
| total_funding_usd | numeric | Pre-converted to USD |
| total_funding | numeric | |
| total_funding_currency_code | text | |
| founded_on | date | |
| closed_on | date | |
| facebook_url | text | |
| linkedin_url | text | |
| twitter_url | text | |
| logo_url | text | |

**Indexes:** uuid (PK), country_code

### Key Values: investor_types (top single values)
| Value | Count |
|-------|-------|
| (empty) | 136,450 |
| angel | 56,722 |
| investment_partner | 51,251 |
| venture_capital | 27,901 |
| private_equity_firm | 12,611 |
| accelerator | 3,074 |
| investment_bank | 1,996 |
| angel_group | 1,977 |
| family_investment_office | 1,694 |
| corporate_venture_capital | 1,634 |
| incubator | 1,331 |
| micro_vc | 1,284 |
| government_office | 1,196 |
| hedge_fund | 723 |
| venture_debt | 520 |

Note: investor_types is comma-separated, so common combos include: `angel,investment_partner` (8,970), `private_equity_firm,venture_capital` (2,666), `micro_vc,venture_capital` (1,103)

---

## Table: investment_partners (287,025 rows)

Links individual partners (people) to funding rounds via their investor firm.

| Column | Type | Notes |
|--------|------|-------|
| uuid | text | |
| name | text | |
| type | text | |
| permalink | text | |
| cb_url | text | |
| rank | integer | |
| created_at | timestamp | |
| updated_at | timestamp | |
| funding_round_uuid | text | (indexed) Links to funding_rounds.uuid |
| funding_round_name | text | |
| investor_uuid | text | (indexed) Links to investors.uuid |
| investor_name | text | |
| partner_uuid | text | (indexed) Links to people.uuid |
| partner_name | text | |

**Indexes:** funding_round_uuid, investor_uuid, partner_uuid

---

## Table: acquisitions (197,127 rows)

Acquisition events between organizations.

| Column | Type | Notes |
|--------|------|-------|
| uuid | text | PK |
| name | text | |
| type | text | Always "acquisition" |
| permalink | text | |
| cb_url | text | |
| rank | integer | |
| created_at | timestamp | |
| updated_at | timestamp | |
| acquiree_uuid | text | (indexed) Links to organizations.uuid |
| acquiree_name | text | |
| acquiree_cb_url | text | |
| acquiree_country_code | text | |
| acquiree_state_code | text | |
| acquiree_region | text | |
| acquiree_city | text | |
| acquirer_uuid | text | (indexed) Links to organizations.uuid |
| acquirer_name | text | |
| acquirer_cb_url | text | |
| acquirer_country_code | text | |
| acquirer_state_code | text | |
| acquirer_region | text | |
| acquirer_city | text | |
| acquisition_type | text | |
| acquired_on | date | |
| price_usd | numeric | Pre-converted to USD |
| price | numeric | Original currency |
| price_currency_code | text | |

**Indexes:** uuid (PK), acquiree_uuid, acquirer_uuid

### Key Values: acquisition_type
| Value | Count |
|-------|-------|
| acquisition | 170,957 |
| lbo | 12,172 |
| merge | 6,489 |
| management_buyout | 2,062 |
| acquihire | 597 |

---

## Table: ipos (54,727 rows)

IPO events for organizations.

| Column | Type | Notes |
|--------|------|-------|
| uuid | text | PK |
| name | text | |
| type | text | |
| permalink | text | |
| cb_url | text | |
| rank | integer | |
| created_at | timestamp | |
| updated_at | timestamp | |
| org_uuid | text | (indexed) Links to organizations.uuid |
| org_name | text | |
| org_cb_url | text | |
| country_code | text | |
| state_code | text | |
| region | text | |
| city | text | |
| stock_exchange_symbol | text | e.g. nasdaq, nyse, tyo, bom, lse |
| stock_symbol | text | Ticker |
| went_public_on | date | |
| share_price_usd | numeric | Pre-converted to USD |
| share_price | numeric | |
| share_price_currency_code | text | |
| valuation_price_usd | numeric | Pre-converted to USD |
| valuation_price | numeric | |
| valuation_price_currency_code | text | |
| money_raised_usd | numeric | Pre-converted to USD |
| money_raised | numeric | |
| money_raised_currency_code | text | |

**Indexes:** uuid (PK), org_uuid

### Key Values: stock_exchange_symbol (top 10)
| Value | Count |
|-------|-------|
| nasdaq | 6,723 |
| tyo | 3,682 |
| bom | 3,473 |
| nyse | 3,236 |
| neeq | 2,655 |
| szse | 2,569 |
| hkg | 2,305 |
| cve | 2,143 |
| lse | 1,998 |
| sse | 1,971 |

---

## Table: funds (28,300 rows)

Investment funds raised by investor entities.

| Column | Type | Notes |
|--------|------|-------|
| uuid | text | PK |
| name | text | Fund name |
| type | text | |
| permalink | text | |
| cb_url | text | |
| rank | integer | |
| created_at | timestamp | |
| updated_at | timestamp | |
| entity_uuid | text | (indexed) Links to investors.uuid or organizations.uuid |
| entity_name | text | |
| entity_type | text | |
| announced_on | date | |
| raised_amount_usd | numeric | Pre-converted to USD |
| raised_amount | numeric | |
| raised_amount_currency_code | text | |

**Indexes:** uuid (PK), entity_uuid

---

## Table: degrees (1,108,126 rows)

Educational degrees for people.

| Column | Type | Notes |
|--------|------|-------|
| uuid | text | PK |
| name | text | |
| type | text | |
| permalink | text | |
| cb_url | text | |
| rank | integer | |
| created_at | timestamp | |
| updated_at | timestamp | |
| person_uuid | text | (indexed) Links to people.uuid |
| person_name | text | |
| institution_uuid | text | (indexed) Links to organizations.uuid (where primary_role='school') |
| institution_name | text | |
| degree_type | text | Free-text, not normalized |
| subject | text | |
| started_on | date | |
| completed_on | date | |
| is_completed | boolean | |

**Indexes:** uuid (PK), person_uuid, institution_uuid

### Key Values: degree_type (top 15)
| Value | Count |
|-------|-------|
| MBA | 85,198 |
| (empty) | 81,573 |
| BS | 67,269 |
| Degree | 65,409 |
| BA | 59,196 |
| unknown | 29,527 |
| MS | 24,311 |
| Bachelor's degree | 22,071 |
| B.S. | 20,241 |
| PhD | 17,495 |
| Bachelor of Science | 15,814 |
| B.A. | 14,692 |
| Bachelor's Degree | 13,078 |
| Master's degree | 11,897 |
| BBA | 11,500 |

Note: degree_type is free-text and NOT normalized. "BS", "B.S.", "Bachelor of Science", "Bachelor's degree", "Bachelor's Degree" all mean roughly the same thing. Use ILIKE patterns for matching.

---

## Table: events (30,981 rows)

Conferences, summits, and other events.

| Column | Type | Notes |
|--------|------|-------|
| uuid | text | PK |
| name | text | |
| type | text | |
| permalink | text | |
| cb_url | text | |
| rank | integer | |
| created_at | timestamp | |
| updated_at | timestamp | |
| short_description | text | |
| started_on | date | |
| ended_on | date | |
| event_url | text | |
| registration_url | text | |
| venue_name | text | |
| description | text | |
| country_code | text | |
| state_code | text | |
| region | text | |
| city | text | |
| logo_url | text | |
| event_roles | text | |

**Indexes:** uuid (PK)

---

## Table: event_appearances (448,232 rows)

Links people/organizations to events.

| Column | Type | Notes |
|--------|------|-------|
| uuid | text | PK |
| name | text | |
| type | text | |
| permalink | text | |
| cb_url | text | |
| rank | integer | |
| created_at | timestamp | |
| updated_at | timestamp | |
| event_uuid | text | (indexed) Links to events.uuid |
| event_name | text | |
| participant_uuid | text | (indexed) Links to people.uuid or organizations.uuid |
| participant_name | text | |
| participant_type | text | "person" or "organization" |
| appearance_type | text | e.g. "speaker", "sponsor", "exhibitor" |
| short_description | text | |

**Indexes:** uuid (PK), event_uuid, participant_uuid

---

## Table: category_groups (804 rows)

Category group definitions.

| Column | Type | Notes |
|--------|------|-------|
| uuid | text | PK |
| name | text | Group name |
| type | text | |
| permalink | text | |
| cb_url | text | |
| rank | integer | |
| created_at | timestamp | |
| updated_at | timestamp | |
| category_groups_list | text | |

**Indexes:** uuid (PK)

---

## Table: org_parents (32,354 rows)

Parent-child relationships between organizations.

| Column | Type | Notes |
|--------|------|-------|
| uuid | text | The child org UUID, links to organizations.uuid |
| name | text | |
| type | text | |
| permalink | text | |
| cb_url | text | |
| rank | integer | |
| created_at | timestamp | |
| updated_at | timestamp | |
| parent_uuid | text | (indexed) Links to organizations.uuid |
| parent_name | text | |

**Indexes:** parent_uuid

---

## Join Patterns

### Core Relationships

```
organizations.uuid  <--  funding_rounds.org_uuid
organizations.uuid  <--  jobs.org_uuid
organizations.uuid  <--  ipos.org_uuid
organizations.uuid  <--  acquisitions.acquiree_uuid
organizations.uuid  <--  acquisitions.acquirer_uuid
organizations.uuid  <--  org_parents.uuid (child)
organizations.uuid  <--  org_parents.parent_uuid (parent)
organizations.uuid  <--  funds.entity_uuid
organizations.uuid  <--  people.featured_job_organization_uuid

people.uuid  <--  jobs.person_uuid
people.uuid  <--  people_descriptions.uuid (1:1, same PK)
people.uuid  <--  degrees.person_uuid
people.uuid  <--  investment_partners.partner_uuid
people.uuid  <--  event_appearances.participant_uuid (when participant_type='person')

investors.uuid  <--  investments.investor_uuid
investors.uuid  <--  investment_partners.investor_uuid
investors.uuid  <--  funds.entity_uuid

funding_rounds.uuid  <--  investments.funding_round_uuid
funding_rounds.uuid  <--  investment_partners.funding_round_uuid

events.uuid  <--  event_appearances.event_uuid

organizations.uuid  <--  degrees.institution_uuid (schools)
```

### Common Multi-Table Joins

**Who invested in a company's funding round:**
```
organizations -> funding_rounds (on org_uuid)
             -> investments (on funding_round_uuid)
             -> investors (on investor_uuid)
```

**Board members of a company:**
```
organizations -> jobs (on org_uuid, WHERE job_type = 'board_member')
             -> people (on person_uuid)
```

**People at a company with their degrees:**
```
organizations -> jobs (on org_uuid)
             -> people (on person_uuid)
             -> degrees (on person_uuid)
```

**Which partner led a deal:**
```
funding_rounds -> investment_partners (on funding_round_uuid)
              -> people (partner_uuid = people.uuid)
              -> investors (on investor_uuid)
```

**Company acquisition history:**
```
organizations -> acquisitions (acquirer_uuid = organizations.uuid)
             -> organizations AS target (acquiree_uuid = target.uuid)
```
