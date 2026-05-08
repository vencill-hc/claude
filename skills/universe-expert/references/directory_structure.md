# Directory Structure

Full layout of the `data-universe-pipelines` repo. Read when navigating files or deciding where new code belongs.

```
src/
├── clients/                    # External API clients (Apollo, Cohere, GCS, Logo.dev)
├── constants/                  # Enums, mappings, PubSub topics, pipeline names
│   ├── pipeline_names.py       # PipelineName enum (all registered pipelines)
│   ├── crunchbase_constants.py # CB-specific mappings
│   ├── pubsub_input_topics.py  # Streaming input subscriptions
│   └── pubsub_output_topics.py # Sink topic classes per pipeline
├── data_types/                 # Pydantic models (THE source of truth)
│   ├── layer.py                # LayerBaseModel, LayerSourceUniqueKeyMixin
│   ├── person_types.py         # PersonLayer → PersonLayerRead → Person
│   ├── organization_types.py   # OrganizationLayer → OrganizationLayerRead → Organization
│   ├── employment_types.py     # EmploymentLayer → EmploymentLayerRead → Employment
│   ├── location_types.py       # LocationLayer → LocationLayerRead → Location
│   ├── event_types.py          # EventType enum, Event base, all event classes
│   ├── source_types.py         # SourceName enum
│   ├── job_types.py            # JobSeniority, JobFunction enums
│   ├── embedding_types.py      # EmbeddingRecord
│   ├── message_types.py        # PubSub message models
│   ├── crunchbase/             # CB raw row types (CrunchbasePersonRow, etc.)
│   ├── mixrank/                # MR raw types
│   ├── legacy_layers/          # Legacy import types
│   ├── apollo_types.py         # Apollo enrichment types
│   └── fortune_500_types.py    # Fortune 500 types
├── pipelines/                  # All pipeline code, organized by stage
│   ├── options.py              # Pipeline option classes
│   ├── ingestion/              # Source → Layer transforms + events
│   │   ├── crunchbase/         # CB bulk export → Person/Org/Employment events
│   │   ├── mixrank/            # MR JSONL → Person/Org/Employment events
│   │   ├── fortune_500/        # F500 → Organization events
│   │   ├── legacy_cx/          # Legacy CX import
│   │   └── legacy_locations/   # Legacy location import
│   ├── enrichment/             # Apollo enrichment pipeline
│   │   └── apollo/             # Streaming enrichment + migration
│   ├── bind/                   # Entity binding (layer → entity resolution)
│   │   ├── person/             # Person binding
│   │   ├── organizations/      # Organization binding
│   │   ├── employments/        # Employment binding
│   │   └── location/           # Location binding
│   └── label/                  # Entity labeling (computed properties)
│       ├── people/             # Highlights, primary employment, avatars
│       ├── organizations/      # Industries, logos
│       └── employments/        # Job designations
├── sources/                    # BigQuery/Postgres read transforms
│   ├── bigquery_source.py      # Generic BQ reader
│   ├── entity_bq_source.py     # Entity-specific BQ reader
│   ├── layer_source.py         # ReadAllPersonLayers, ReadAllOrganizationLayers, etc.
│   ├── crunchbase_source.py    # FetchCrunchbaseBulkExport
│   ├── source_unique_ids.py    # ID generation per source
│   └── db_connections.py       # Postgres connection helpers
├── sinks/                      # Output transforms
│   ├── bq_sink.py              # WriteToBQ (BigQuery)
│   ├── pg_sink.py              # WriteToPG (Postgres)
│   └── pubsub_sink.py          # WriteEventsToPubsub
├── transforms/                 # Shared/reusable transforms
│   ├── delta_dataset_transforms.py   # DeltaDatasets (core diffing)
│   ├── event_generator_transforms.py # GenerateEvent, GenerateGroupedEvents
│   ├── binding_transforms.py         # BoundLayerGroup, FoldLayersIntoGroups
│   ├── join_transforms.py            # GroupedFullJoin, MultiKeyLeftJoin
│   ├── group_transforms.py           # Grouping utilities
│   ├── fork_transforms.py            # Fork PCollections
│   ├── postgres_transforms.py        # PostgresFetchingDoFn base class
│   ├── quick_batch_transform.py      # QuickBatch
│   ├── quick_dedupe_transform.py     # QuickDedupe
│   ├── quick_window_transform.py     # QuickWindow (streaming)
│   └── reading/                      # CSV/JSON file readers
└── utils/                      # Pure helper functions
    ├── bq_utils.py             # BQTable, schema inference
    ├── person_utils.py         # Name normalization
    ├── employment_utils.py     # Title parsing, date logic
    ├── linkedin_utils.py       # Slug extraction
    ├── string_cleaning_utils.py
    ├── uuid_utils.py           # uuid7() generation
    └── ...

test/                           # Mirrors src/ structure exactly
├── pipelines/ingestion/crunchbase/test_crunchbase_person_transforms.py
├── transforms/test_delta_dataset_transforms.py
└── ...

entrypoint.py                   # RUN_METHODS dict maps PipelineName → run function
Makefile                        # All dev commands
```

## Top-Level Summary

- `src/data_types/` — Pydantic models (source of truth for all entity shapes)
- `src/pipelines/` — Pipeline code grouped by stage: `ingestion/`, `enrichment/`, `bind/`, `label/`
- `src/sources/`, `src/sinks/`, `src/transforms/` — Reusable Beam I/O and transforms
- `src/clients/`, `src/constants/`, `src/utils/` — Supporting code
- `test/` — Mirrors `src/` exactly
- `entrypoint.py` — `RUN_METHODS` dict maps `PipelineName` enum to its `run()` function
