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

1. **Ingestion**: Reads raw source data, transforms to Layers, diffs against extant via DeltaDatasets, emits Upsert/Discard events to PubSub
2. **Binding**: Groups Layers into Entities by matching on bindable fields (names, slugs, domains, etc.)
3. **Labeling**: Computes derived properties (highlights, primary employment, industries, cached avatars/logos)

Each stage has both **batch** and **streaming** variants.

## Key Enums

`SourceName`, `PipelineName`, and `EventType` are the three enums you'll touch most. For full membership, see `references/data_types.md`.

## Development Commands

See CLAUDE.md quick reference for `make tests`, `make lint`, `make format`, `make dump_schemas`, `make console`, `make deps`, and DB commands (`make db_setup`, `make db_migrate`, `make db_console`).

## Domain Concepts (Brief)

- **Layer**: A single source's view of an entity. Multiple layers from different sources can describe the same real-world entity.
- **Binding**: The process of grouping layers that represent the same entity and assigning a shared entity ID.
- **Materialization**: Merging bound layers into a single entity record with all fields resolved.
- **Labeling**: Computing derived/enriched properties on materialized entities (highlights, primary employment, etc.).
- **DeltaDatasets**: The core diffing transform that compares new data against existing data and emits upsert/discard decisions.
- **Events**: The output of pipelines — typed PubSub messages that trigger downstream processing.

## Local `.claude/` Resources (Always Available in This Repo)

The repo ships authoritative guides in `.claude/`. Read these before writing code — do not rely on summaries here.

- **`.claude/architecture.md`** — Implementation patterns: Pydantic v2 gotchas, Beam pickling, DoFn lifecycle, CoGroupByKey, `beam.Reshuffle()`, PubSub sink semantics, adding new fields (with Alembic migrations), adding new entity types, CI/CD.
- **`.claude/conventions.md`** — Code style rules: `import typing as t`, `t.cast()` usage, naming (`TransformXxxToYyyEvents`, `GenerateXxx`), 120-char line length, conventional commits.
- **`.claude/tech_stack.md`** — Exact versions: Python 3.11, Apache Beam 2.71.0, Pydantic v2, ruff + pyright.
- **`.claude/agents/test-lint-runner.md`** — Haiku sub-agent for running `make format`, `make lint`, `make tests` with concise pass/fail summaries. Delegate to it instead of running these in the main thread.

## Reference Files

For detailed documentation, see:
- `references/directory_structure.md` — Full repo layout, every directory annotated
- `references/data_types.md` — Full Pydantic model hierarchy, nested types, field docs, enum membership
- `references/pipeline_patterns.md` — How to add pipelines, transforms, tests; DeltaDatasets pattern
- `references/infrastructure.md` — GCP setup, deployment, pipeline options, streaming patterns
