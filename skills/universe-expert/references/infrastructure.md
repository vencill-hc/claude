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
