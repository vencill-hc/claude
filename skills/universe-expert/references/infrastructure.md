# Infrastructure Reference

## GCP Project Structure

| Environment | Project | BQ Project |
|------------|---------|-----------|
| Production | `gdulabs-production` | `gdulabs-production` |
| Staging | `gdulabs-staging` | `gdulabs-staging` |

### Key GCP Services

- **Dataflow**: Runs Apache Beam pipelines (batch + streaming)
- **PubSub**: Event bus between pipeline stages
- **BigQuery**: Data warehouse for entity reads and analytics
- **Cloud Storage (GCS)**: Temp artifacts, ingestion files, image caches
- **Cloud Composer (Airflow)**: Pipeline orchestration/scheduling
- **CloudBuild**: CI/CD, Flex Template builds
- **Postgres**: Operational data store for layers/entities

### GCS Buckets (Production)

- `gs://gdulabs-data-universe-prod-pipelines-processing-artifacts/temp` — Dataflow temp
- `gdulabs-data-universe-prod-images-cache` — Avatar + logo cache
- `gdulabs-data-universe-prod-ingestion-mixrank` — MixRank data files

## Environment Configuration

### production.env

```
PROJECT=gdulabs-production
GCP_BQ_PROJECT=gdulabs-production
TEMP_LOCATION=gs://gdulabs-data-universe-prod-pipelines-processing-artifacts/temp
GCS_AVATAR_CACHE_BUCKET=gdulabs-data-universe-prod-images-cache
GCS_LOGO_CACHE_BUCKET=gdulabs-data-universe-prod-images-cache
```

### staging.env

```
PROJECT=gdulabs-staging
GCP_BQ_PROJECT=gdulabs-staging
TEMP_LOCATION=gs://gdulabs-data-universe-staging-pipelines-processing-artifacts/temp
GCS_AVATAR_CACHE_BUCKET=gdulabs-data-universe-staging-images-cache
GCS_LOGO_CACHE_BUCKET=gdulabs-data-universe-staging-images-cache
```

### Switching Environments

```bash
TARGET_ENV=staging make run_crunchbase_ingestion   # Use staging
TARGET_ENV=production make run_crunchbase_ingestion # Use production (default)
```

## Pipeline Options

### DataUniversePipelineOptions (`pipelines/options.py`)

All pipelines use these base options:

| Option | Type | Description |
|--------|------|-------------|
| `--gcp_bq_project` | str | GCP project for BigQuery reads |
| `--read_only` | bool | Dry run — no events emitted |
| `--test_mode` | bool | Limits source data for fast testing |

### BindingPipelineOptions

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--stale_binding_mode` | StaleBindingModeOptions | `unbind` | `keep` or `unbind` stale bindings |

### MixrankPipelineOptions

| Option | Type | Description |
|--------|------|-------------|
| `--payload` | str (JSON) | GCS file references `[{"bucket":"...","name":"..."}]` |

### PersonLabelingPipelineOptions

| Option | Type | Description |
|--------|------|-------------|
| `--gcs_avatar_cache_bucket` | str | GCS bucket for avatar caching |
| `--cache_top_avatar_only` | bool | Only cache highest-priority avatar |

## Streaming vs Batch Pipelines

### Batch Pipelines

- Read all data from BigQuery/GCS at pipeline start
- Process entire dataset
- Write results to PubSub/BQ
- Run to completion and exit
- Used for: ingestion, initial binding, bulk labeling

### Streaming Pipelines

- Subscribe to PubSub input topics
- Process events as they arrive
- Use windowing for grouping (`QuickWindow`)
- Run indefinitely
- Used for: real-time binding updates, incremental labeling, Apollo enrichment
- Identified by `_STREAMING` suffix in `PipelineName`

### Streaming Pipeline Marker

```python
# In entrypoint.py
STREAMING_PIPELINES = {
    PipelineName.APOLLO_STREAMING,
    PipelineName.BIND_EMPLOYMENTS_STREAMING,
    PipelineName.BIND_ORGANIZATIONS_STREAMING,
    PipelineName.BIND_PEOPLE_STREAMING,
    PipelineName.LABEL_EMPLOYMENTS_STREAMING,
    PipelineName.LABEL_ORGANIZATIONS_STREAMING,
    PipelineName.LABEL_PEOPLE_STREAMING,
}
```

These automatically get `StandardOptions.streaming = True`.

## Entrypoint Registration

Location: `src/entrypoint.py`

```python
from constants.pipeline_names import PipelineName

RUN_METHODS = {
    PipelineName.CRUNCHBASE_INGESTION: run_crunchbase_ingestion_pipeline,
    PipelineName.MIXRANK_INGESTION: run_mixrank_ingestion_pipeline,
    # ... all pipelines registered here
}
```

### Adding a New Pipeline

1. Add to `PipelineName` enum in `src/constants/pipeline_names.py`
2. Import `run_` function in `src/entrypoint.py`
3. Add to `RUN_METHODS` dict
4. If streaming, add to `STREAMING_PIPELINES` set

## Deployment Flow

### Flex Templates (Dataflow)

1. CloudBuild builds Docker image with pipeline code
2. Image pushed to Container Registry
3. Flex Template spec created referencing the image
4. Composer DAG or manual trigger launches from template

### Running Locally

```bash
# All local runs use DirectRunner with --test_mode
make run_crunchbase_ingestion    # Batch, DirectRunner
make run_bind_people             # Batch binding
make run_label_people            # Batch labeling

# Streaming uses multi_threading mode locally
make run_apollo_enrichment_pipeline_streaming
```

### Pipeline Arguments Pattern

```bash
python -m src.entrypoint \
    --pipeline_name=CRUNCHBASE_INGESTION \
    --job_name=crunchbase-ingestion-{user}-{timestamp} \
    --runner=DirectRunner \    # or DataflowRunner for cloud
    --test_mode \
    --setup_file=./setup.py \
    --temp_location=${TEMP_LOCATION} \
    --project=${PROJECT} \
    --gcp_bq_project=${GCP_BQ_PROJECT} \
    --region=us-central1
```

## Database (Postgres)

### Local Setup

```bash
make db_setup     # Drop + create du_pipelines DB, run migrations
make db_migrate   # Run Alembic migrations only
make db_console   # psql into du_pipelines
```

### Alembic Migrations

Location: `src/db/alembic/`

```bash
# Create new migration
. .venv/bin/activate; PYTHONPATH=./src alembic revision --autogenerate -m "description"
# Apply migrations
make db_migrate
```

### Table Definitions

Location: `src/db/tables/` — SQLAlchemy table definitions used by Alembic

## Python Environment

- Python 3.11
- Package manager: `uv` (fast pip replacement)
- Virtual environment: `.venv/`
- Linting: `ruff`
- Type checking: `pyright`
- Testing: `pytest` with `pytest-xdist` for parallelism
- Pre-commit hooks installed via `pre-commit`

### Dependency Files

- `requirements_dev.txt` — Development dependencies
- `requirements_test.txt` — Test dependencies
- `setup.py` — Package setup (used by Dataflow for worker dependencies)

## Adding a New Layer Type: Cross-Repo Checklist

**Critical:** A new layer type is a two-repo change. The pipeline reads BQ tables (`gdulabs-production:data_universe.<layer>`) that **this repo does not create**. They're materialized by a CDC pipeline owned by the sibling repo `data-universe-rails` (at `~/Documents/git/data-universe-rails/`):

```
Rails Postgres (source of truth, write store)
        │  (Postgres CDC)
        ▼
RisingWave  data_universe.<layer>
        │  (JDBC BigQuery sink)
        ▼
BigQuery  gdulabs-production:data_universe.<layer>   ← this repo reads here
```

If the rails-side migrations haven't merged + deployed, the BQ table doesn't exist and any pipeline run (even `MODE=test` on DirectRunner) fails with `Table … was not found in location US`.

### pipelines repo side (this repo)

1. New Pydantic models in `src/data_types/` extending `LayerBaseModel` + `LayerSourceUniqueKeyMixin` (also a `*LayerRead` variant for BQ reads).
2. New `ReadAllXxxLayers` / `ReadAllXxxLayerReads` source in `src/sources/layer_source.py` — points at `data_universe.<layer>`.
3. New entries in the appropriate enum in `src/constants/pubsub_output_topics.py` (e.g. `CrunchbaseIngestionSinkTopics.UPSERT_XL_EVENTS` / `DISCARD_XL_EVENTS`). Note the file header: topics added here **must also be provisioned externally** — see "PubSub topic provisioning" below.
4. New event types under `src/data_types/events/` and routing in `event_layer_from_type` if applicable.
5. Pipeline wiring in `src/pipelines/ingestion/<source>/<source>_pipeline.py` — sinks the new events to the new topics.
6. Transforms + tests under `src/transforms/` and `test/`.
7. JSON schemas regenerate via CI (`make dump_schemas` runs in CI; don't commit them locally — see auto-memory `feedback_no_local_schema_dump.md`).

### rails repo side (`data-universe-rails`) — must merge + deploy *first*

The reference precedent to mirror is **employment_layers**:

1. **Postgres migration** creating the layer table — `db/migrate/<ts>_create_<layer>s.rb`. Mirrors `db/migrate/20250617134347_create_employment_layers.rb`. Include:
   - `t.jsonb :event, null: false`
   - `t.enum :source` (uses the `source` Postgres enum)
   - `t.string :source_unique_id, null: false` + composite unique index on `[source, source_unique_id]`
   - Layer-specific columns + foreign keys to other `*_layers` tables as needed
   - Calls to `create_trigger :merge_<layer>s_event_bodies, on: :<layer>s, version: 1` and `create_trigger :z_generate_<layer>s_columns, on: :<layer>s, version: 1`
2. **Trigger SQL files** under `db/triggers/`: `merge_<layer>s_event_bodies_v01.sql` and `z_generate_<layer>s_columns_v01.sql`. Mirror the employment versions.
3. **RisingWave source migration** — `packs/risingwave/db/migrate/<ts>_create_data_universe_<layer>s.rb`. Mirrors `20250702171722_create_data_universe_employment_layers.rb`. Creates the CDC-fed `data_universe.<layer>s` table in RisingWave.
4. **RisingWave intermediate migration** — `packs/risingwave/db/migrate/<ts>_create_intermediate_<layer>s.rb`. Mirrors `20250708012819_create_intermediate_employment_layers.rb`. (Whether you need an intermediate depends on the layer's role in binding/labeling.)
5. **RisingWave BQ sink migration** — adds the new layer to the existing `create_bigquery_layer_sinks` (initial creation in `20250805205709_create_bigquery_layer_sinks.rb`). This is the step that creates the `gdulabs-production:data_universe.<layer>s` BQ table. Without this migration deployed, the pipeline cannot read.
6. Models, factories, Avo admin resources, policies, and tests — discoverable via `grep -rln employment_layer packs/` to find every place the precedent touches.

### PubSub topic provisioning

The header of `src/constants/pubsub_output_topics.py` says: *"Any new topics added here should be added to Terraform as well, so that they are created in the GCP project."*

**TODO**: no Terraform was found in either `data-universe-pipelines` or `data-universe-rails`. The actual provisioning location is unknown — likely a separate infra repo not cloned locally. Before shipping new topics, ask the team or `git log` an existing topic name (e.g. `data-universe-crunchbase-ingestion-upsert-employment-layer-events`) across known infra repos.

### Order of operations

1. Rails PR opens; reviewed; merged to `main`.
2. Rails deploys to prod (migrations run, including the BQ sink migration).
3. Verify `gdulabs-production:data_universe.<new_layer>` exists in BQ.
4. PubSub topics provisioned (whatever path that is — see TODO above).
5. Pipelines PR's dry-run (`make run_pipeline PIPELINE=<...>` — defaults to `MODE=test` + DirectRunner + `--test_mode` flag that short-circuits pubsub publishes) now succeeds.
6. Pipelines PR merges; scheduled DAG runs the real production ingestion.

### Cross-repo discovery commands

```bash
# Find the rails-side counterpart for a layer type
cd ~/Documents/git/data-universe-rails
ls db/migrate/ | grep -i <layer>
grep -rln "<layer>_layer" packs/risingwave/

# Find related rails PRs (open or merged)
gh -R gdulabs/data-universe-rails pr list --search "<keyword>" --state all
```
