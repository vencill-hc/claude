# Data Types Reference

## Base Classes (`data_types/layer.py`)

```python
class LayerBaseModel(BaseModel):
    id: UUID | None = None
    source: str                          # SourceName enum value
    source_unique_id: str                # Unique within source
    source_metadata: dict[str, str] | None = None

class LayerSourceUniqueKeyMixin(BaseModel):
    source: str
    source_unique_id: str
    @property
    def unique_key(self) -> str:         # "{source}:{source_unique_id}"
```

## SourceName Enum (`data_types/source_types.py`)

```python
class SourceName(str, Enum):
    # Data Universe internal
    UNIVERSE_APP = "UNIVERSE_APP"
    UNIVERSE_ADMIN = "UNIVERSE_ADMIN"
    UNIVERSE_CX = "UNIVERSE_CX"
    UNIVERSE_LABELING = "UNIVERSE_LABELING"
    # Third party
    CRUNCHBASE = "CRUNCHBASE"
    LINKEDIN = "LINKEDIN"
    MIXRANK = "MIXRANK"
    NYLAS = "NYLAS"
    PEOPLE_DATA_LABS = "PEOPLE_DATA_LABS"
    FORTUNE_500_SCRAPER = "FORTUNE_500_SCRAPER"
    APOLLO = "APOLLO"
    # Legacy
    LEGACY_ATLAS = "LEGACY_ATLAS"
    LEGACY_DATA_PLATFORM = "LEGACY_DATA_PLATFORM"
    LEGACY_ENRICHMENT = "LEGACY_ENRICHMENT"
```

## Person Types (`data_types/person_types.py`)

### Nested Types

| Type | Key Fields | Notes |
|------|-----------|-------|
| `PersonLayerLinkedinSlug` | `value`, `status` (SlugStatus enum), `is_primary` | Status: ALIVE, DEAD, UNKNOWN, INVALID, UNTRUSTED |
| `PersonLayerEmail` | `value`, `type` (EmailType), `is_primary`, `suppressed` | Types: personal, work, other |
| `PersonLayerPhoneNumber` | `value`, `type` (PhoneType), `is_primary` | Types: personal, work, other |
| `PersonLayerWebsite` | `value`, `type` (WebsiteType) | Types: homepage, twitter, facebook, github |
| `PersonLayerLanguage` | `language_name`, `language_iso`, `proficiency_type` | ISO 639-1 codes |
| `PersonLayerHighlight` | `value`, `generic_value`, `category`, `employment_ids` | See highlight categories below |
| `PersonLayerExternalIdentifier` | `value`, `type` | Types: linkedin_member_id, linkedin_member_urn, mixrank_person_id |

### Highlight Categories

- `COMPANY_IDENTITY`: FAANG, Fortune 500 Background
- `COMPANY_BACKING`: VC-backed Experience, PE-backed Experience, PE-backed CxO Experience
- `COMPANY_STAGE`: Early-Stage / Mid-Stage Startup Experience
- `DEEP_INDUSTRY_EXPERIENCE`: [Industry] Veteran
- `EMPLOYMENT_HISTORY_FEATURE`: Company Loyalty, Employee Through Growth, Serial Startup Employee
- `JOB_FEATURE`: CxO During Acquisition/IPO, Employed During Acquisition/IPO
- `COMPANY_AWARDS`: Fortune 500

### Model Hierarchy

```
PersonLayer(LayerBaseModel)
├── person_id, location_layer_id, primary_employment_id
├── given_name, family_name, full_name, avatar_url, headline, summary
├── linkedin_slugs: list[PersonLayerLinkedinSlug]
├── emails: list[PersonLayerEmail]
├── phone_numbers: list[PersonLayerPhoneNumber]
├── websites: list[PersonLayerWebsite]
├── languages: list[PersonLayerLanguage]
├── highlights: list[PersonLayerHighlight]
├── embeddings: list[EmbeddingRecord]
└── external_identifiers: list[PersonLayerExternalIdentifier]

PersonLayerRead(PersonLayer, LayerSourceUniqueKeyMixin)
├── id: UUID (required)
├── created_at, updated_at, discarded_at

PersonLayerWithEntityIds(PersonLayerRead)
├── location_id: UUID | None

Person(BaseModel)
├── person_id: UUID
├── All Person fields materialized (no layer metadata)

PersonWithLayerIds(Person)
├── person_layer_ids: list[UUID]
```

## Organization Types (`data_types/organization_types.py`)

### Nested Types

| Type | Key Fields | Notes |
|------|-----------|-------|
| `OrganizationLayerOrganizationName` | `value`, `is_primary` | At most one primary |
| `OrganizationLayerDomain` | `value`, `is_primary` | At most one primary |
| `OrganizationLayerWebsite` | `value`, `type`, `is_primary` | Types: homepage, twitter, facebook, crunchbase |
| `OrganizationLayerLocation` | `country_code`, `region`, `city`, `latitude`, `longitude` | |
| `OrganizationLayerAddress` | `premise`, `thoroughfare`, `postal_code`, `locality`, `administrative_area`, `country_code`, `raw_address` | xNAL standard |
| `OrganizationLayerIndustry` | `value`, `type` (IndustryType) | Types: data_universe, crunchbase, linkedin, pdl, apollo, etc. |
| `OrganizationLayerFundingEvent` | `investment_type`, `organization_stage`, `funding_event_date`, `raised_amount_usd`, `valuation_usd`, `acquirer_organization_name` | 25+ investment types |
| `OrganizationLayerTradingIdentifier` | `regulator_name`, `regulatory_id`, `went_public_on`, `delisted_on`, `trading_symbols` | SEC CIK, stock tickers |
| `TradingSymbol` | `exchange`, `symbol`, `share_class`, `is_primary` | e.g., NASDAQ:GOOGL |
| `OrganizationLayerExternalIdentifier` | `value`, `type` | Types: linkedin_id, linkedin_slug, apollo_id, crunchbase_uuid, mixrank_id |
| `OrganizationLayerHighlight` | `value`, `category`, `generic_value` | Categories: awards, top_tech |
| `OrganizationLayerEmployeeCount` | `count`, `lower_bound`, `upper_bound` | Must have count or both bounds |

### FundingEvent Investment Types (partial)

ANGEL, PRE_SEED, SEED, SERIES_A through SERIES_J, CONVERTIBLE_NOTE, DEBT_FINANCING, PRIVATE_EQUITY, IPO, POST_IPO_*, CORPORATE_ROUND, GRANT, ACQUISITION, UNKNOWN

### Organization Stage Derivation

- Early-Stage: Angel, Pre-Seed, Seed, Series A
- Mid-Stage: Series B, Series C
- Late-Stage: Series D through J
- Public: IPO, Post-IPO variants

### Model Hierarchy

```
OrganizationLayer(LayerBaseModel)
├── organization_id, parent_organization_layer_id
├── year_founded, employee_count, logo_url
├── organization_names, domains, websites, locations, addresses
├── industries, funding_events, trading_identifiers
├── external_identifiers, highlights
├── Validators: at most one primary name/domain/website, employee_count validation

OrganizationLayerRead(OrganizationLayer, LayerSourceUniqueKeyMixin)
├── created_at, updated_at, discarded_at

Organization(BaseModel)
├── organization_id, parent_organization_id
├── All Org fields materialized
```

## Employment Types (`data_types/employment_types.py`)

### BoardSeat Model

```python
class BoardSeat(BaseModel):
    class BoardRole(str, Enum):
        EXECUTIVE, FOUNDER, MEMBER, CHAIR, OBSERVER,
        ADVISOR, INVESTOR, INDEPENDENT, TRUSTEE, DIRECTOR
    roles: list[BoardRole] | None
    is_independent: bool | None
    committee_memberships: list[str] | None
```

### Model Hierarchy

```
EmploymentLayer(LayerBaseModel)
├── employment_id, person_layer_id, organization_layer_id
├── organization_name, job_title, job_description
├── start_year, start_month, end_year, end_month  # end=-1 means current
├── job_function: JobFunction, seniority: JobSeniority
├── job_location, is_fulltime
├── board_seat: BoardSeat

EmploymentLayerRead(EmploymentLayer, LayerSourceUniqueKeyMixin)
├── person_layer_id: UUID (required)
├── created_at, updated_at, discarded_at

Employment(BaseModel)
├── employment_id, person_id, organization_id
├── All employment fields + is_primary
```

### Job Enums (`data_types/job_types.py`)

**JobSeniority**: Uncategorized, Entry, Senior, Manager, Director, VP, CxO, Advisor/Board Member

**JobFunction**: ~35 values including Engineering, Sales, Marketing, Finance, Legal, HR, Operations, Product Management, Design, Data/Analytics, etc.

## Location Types (`data_types/location_types.py`)

```
LocationLayer(LayerBaseModel)
├── location_id
├── raw_location, city, region, region_code
├── country, country_code
├── latitude, longitude  # Decimal(10,6)

LocationLayerRead → Location (same pattern)
```

## Event Types (`data_types/event_types.py`)

### EventType Enum

For each entity: `UPSERT_{ENTITY}_LAYER`, `UPDATE_{ENTITY}_LAYER`, `DISCARD_{ENTITY}_LAYER`

### Event Model

```python
class Event(BaseModel):
    event_type: EventType
    event_id: UUID          # uuid7
    event_at: int           # microsecond timestamp
    event_publisher: str    # PipelineName value
    data: BaseModel         # Typed per event class
```

### Event Data Models

| Event Data Class | Fields | Used By |
|-----------------|--------|---------|
| `PersonLayerEventData` | `person_layer` | Discard events |
| `PersonLayerEventDataWithRelations` | + `location_layer`, `undiscard` | Upsert/Update events |
| `OrganizationLayerEventData` | `organization_layer` | Discard events |
| `OrganizationLayerEventDataWithRelations` | + `parent_organization_layer`, `undiscard` | Upsert/Update events |
| `EmploymentLayerEventData` | `employment_layer` | Discard events |
| `EmploymentLayerEventDataWithRelations` | + `person_layer`, `organization_layer`, `undiscard` | Upsert/Update events |
| `LocationLayerEventData` | `location_layer`, `undiscard` | All location events |

### Event Grouping Key Functions

Each entity type has a grouping key function used for PubSub ordering:
- Person: groups on `person_id` (or `source_unique_id` if unbound)
- Organization: groups on `organization_id` (or `source_unique_id`)
- Employment: `employment_event_default_grouping_key_fn` or `employment_event_by_person_grouping_key_fn`
- Location: groups on `location_id` (or `source_unique_id`)

## Source-Specific Types

### Crunchbase (`data_types/crunchbase/`)

- `CrunchbasePersonRow`: uuid, name, first_name, last_name, gender, location, featured_job, social URLs
- `CrunchbaseOrganizationRow`: uuid, name, domain, status, categories, funding, location, employee_count
- `CrunchbaseJobRow`: uuid, person_uuid, org_uuid, title, job_type (executive/employee/board_member/advisor/board_observer), dates
- `CrunchbaseAcquisitionRow`: acquirer/acquiree UUIDs, price, date
- `CrunchbaseFundingRoundRow`: org_uuid, investment_type, raised_amount, valuation, investors
- `CrunchbaseIPORow`: org_uuid, stock_exchange, symbol, valuation, went_public_on
- `CrunchbaseOrgParentRow`: uuid (child) → parent_uuid
- `CrunchbaseInvestorRow`: investor org/person data

### Mixrank (`data_types/mixrank/`)

- `MixrankLinkedinProfile`: Profile data with slugs, experiences, education
- `MixrankLinkedinCompany`: Company data from LinkedIn

## JSON Schema Generation

Run `make dump_schemas` to generate JSON schemas from all Pydantic models into `schemas/`.
