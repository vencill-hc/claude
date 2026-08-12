---
name: universe-expert
description: Codebase map and development guide for the data-universe-pipelines repo. Use when working on pipelines, layers, beam transforms, bindings, ingestion, labeling, data universe entities (person, organization, employment, location), or specific pipeline sources. Trigger phrases - "add a pipeline", "new entity type", "beam transform", "DeltaDataset", "binding pipeline", "ingestion pipeline", "add a field", "new source", "pipeline options", "PubSub sink", "Dataflow pipeline". Do NOT use for crunchbase data queries or company research - use crunchbase-analyzer instead. Do NOT use for mixrank people queries or workforce analysis - use mixrank-analyzer instead.
---

# Data Universe Pipelines — Codebase Map

## What This Is

The `data-universe-pipelines` repo contains Apache Beam pipelines that ingest, transform, bind, and label entity data (People, Organizations, Employments, Locations) from multiple third-party sources into a unified data model called the "Data Universe." Pipelines run on Google Cloud Dataflow and emit events via PubSub.

## Top-Level Layout

- `src/data_types/` — Pydantic models (source of truth for all entity shapes)
- `src/pipelines/` — Pipeline code grouped by stage: `ingestion/`, `enrichment/`, `bind/`, `label/`
- `src/sources/`, `src/sinks/`, `src/transforms/` — Reusable Beam I/O and transforms
- `src/clients/`, `src/constants/`, `src/utils/` — Supporting code
- `test/` — Mirrors `src/` exactly
- `entrypoint.py` — `RUN_METHODS` dict maps `PipelineName` enum to its `run()` function

For the full directory tree, see `references/directory_structure.md`.

## Entity Model Hierarchy

Each entity type follows the pattern: **Layer → LayerRead → Entity**

| Entity       | Layer class          | Read class              | Entity class     | Key nested types |
|-------------|---------------------|------------------------|-----------------|-----------------|
| Person       | `PersonLayer`        | `PersonLayerRead`       | `Person`         | LinkedinSlug, Email, PhoneNumber, Highlight, Website, Language, ExternalIdentifier |
| Organization | `OrganizationLayer`  | `OrganizationLayerRead` | `Organization`   | OrganizationName, Domain, Website, Location, Address, Industry, FundingEvent, TradingIdentifier, ExternalIdentifier, Highlight, EmployeeCount |
| Employment   | `EmploymentLayer`    | `EmploymentLayerRead`   | `Employment`     | BoardSeat (with BoardRole enum), JobFunction, JobSeniority |
| Location     | `LocationLayer`      | `LocationLayerRead`     | `Location`       | (flat — city, region, country, lat/lng) |

- `LayerBaseModel` provides: `id`, `source`, `source_unique_id`, `source_metadata`
- `LayerSourceUniqueKeyMixin` provides: `unique_key` property = `"{source}:{source_unique_id}"`
- `LayerRead` classes add: `created_at`, `updated_at`, `discarded_at`
- Entity classes are the materialized output of the binding process

## Pipeline Lifecycle Stages

```
Ingestion → Binding → Labeling
   ↓            ↓          ↓
(Layers)    (Entities)  (Computed properties)
```

1. **Ingestion**: Reads raw source data, transforms to Layers, filters DSR-scrubbed/suppressed layers, diffs against extant via DeltaDatasets, emits Upsert/Discard events to PubSub. A single source can emit multiple **related** layers in one run (e.g. a parent `InvestmentLayer` and a child `InvestmentPartnerLayer`) — see `references/multi_layer_ingestion.md`.
2. **Binding**: Groups Layers into Entities by matching on bindable fields (names, slugs, domains, etc.)
3. **Labeling**: Computes derived properties (highlights, primary employment, industries, cached avatars/logos)

Each stage has both **batch** and **streaming** variants.

## Key Enums

`SourceName`, `PipelineName`, and `EventType` are the three enums you'll touch most. For full membership, see `references/data_types.md`.

## Development Commands

See CLAUDE.md quick reference for `make tests`, `make lint`, `make format`, `make dump_schemas`, `make console`, `make deps`, and DB commands (`make db_setup`, `make db_migrate`, `make db_console`).

Delegate `make format` / `make lint` / `make tests` runs to a Sonnet sub-agent per `references/test_lint_runner_agent.md` instead of running them in the main thread; the sub-agent returns a concise pass/fail summary with only anomalies.

## Domain Concepts (Brief)

- **Layer**: A single source's view of an entity. Multiple layers from different sources can describe the same real-world entity.
- **Binding**: The process of grouping layers that represent the same entity and assigning a shared entity ID.
- **Materialization**: Merging bound layers into a single entity record with all fields resolved.
- **Labeling**: Computing derived/enriched properties on materialized entities (highlights, primary employment, etc.).
- **DeltaDatasets**: The core diffing transform that compares new data against existing data and emits upsert/discard decisions.
- **Events**: The output of pipelines — typed PubSub messages that trigger downstream processing.

## Misc Notes

- **Job-title synonyms live in two unconnected places, running opposite directions.** Pipelines side: `JOB_TITLE_NORMALIZATION_SYNONYMS` (`src/utils/string_validator_utils.py:47`, 16 entries, directional long→short "chief financial officer" → "cfo") feeds `normalize_job_title`; actual CFO≡long-form equivalence is implicit per-parser (seniority `_NORMALIZE_SUBS` regexes collapse both to a `cxo` token in `src/utils/seniority_utils.py:83-108`; job function enumerates both spellings as keys in `src/utils/employment_utils.py:14`). Rails side (`data-universe-rails`): bidirectional OpenSearch `synonym_graph` equivalence groups at query time only (`packs/search/app/services/search/analysis/job_title_synonyms.rb`, wired as `search_analyzer` in `packs/search/app/public/search/person.rb` and `employment_job_title.rb`). Both repos store titles verbatim at ingestion/write; normalization happens only at label/bind time (pipelines) or query time (rails). The two lists share no file or generated artifact — they can drift silently (rails list already lacks CISO/CHRO/CPO and the VP/SVP pair; typeahead subfields get no synonym expansion; its `updateable: true` flag is inert — no `_reload_search_analyzers` caller, so edits need a full index rebuild).

## Reference Files

For detailed documentation, see:
- `references/directory_structure.md` — Full repo layout, every directory annotated
- `references/data_types.md` — Full Pydantic model hierarchy, nested types, field docs, enum membership
- `references/pipeline_patterns.md` — How to add pipelines, transforms, tests; DeltaDatasets pattern
- `references/infrastructure.md` — GCP setup, deployment, pipeline options, streaming patterns
- `references/binding_input_contracts.md` — `XxxLayerForBinding` pattern. **Read this** when touching any `src/pipelines/bind/` code or adding fields to an Entity Layer that should participate in binding.
- `references/labeling_input_contracts.md` — `XxxLayerForLabeling` pattern (sibling of binding contracts). **Read this** when touching any `src/pipelines/label/` code or adding a labeler-written field. Covers the read+write field invariant and the lossless discard-event splat.
- `references/multi_layer_ingestion.md` — Ingesting two **related** layers from one source. **Read this** when a pipeline emits a parent + child layer (e.g. `InvestmentLayer` + `InvestmentPartnerLayer`). Covers parent-child invariants, synthesizing layers for schema parity, validate-with-data existence checks, and the `crunchbase_updated_at` idempotency footgun.
- `references/dsr_filtering.md` — DSR (Data Subject Request) scrubbing/suppression. **Read this** when adding DSR compliance to an ingestion pipeline or ingesting person data. Covers `FilterDsrScrubbedLayers` (extant-marked) vs `FilterDsrSuppressed*` (pre-emptive), HMAC digests, and where filtering slots in (after layer generation, before `DeltaDatasets`).
- `references/test_lint_runner_agent.md` — sub-agent spec for running format/lint/tests. **Read this** before running any make-based verification; delegate to a Sonnet sub-agent instead of running in the main thread.
- `references/bq_live_schema.md` — how the materialized BigQuery tables differ from the Pydantic models (JSON columns, no is_primary, layer-table provenance, raw MixRank staging tables + scan-cost gotchas). **Read this** before writing SQL against `data_universe` or `data_universe_mixrank`. Dated snapshot with refresh queries embedded; verify column lists before relying on them.
