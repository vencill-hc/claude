# Pipeline Patterns Reference

## Adding a New Ingestion Pipeline

### Step-by-step

1. **Define source types** in `src/data_types/{source}/` — Pydantic models for raw source rows
2. **Add SourceName** enum value in `src/data_types/source_types.py`
3. **Add source unique ID generators** in `src/sources/source_unique_ids.py`
4. **Create source reader** in `src/sources/` — a `beam.PTransform` that reads raw data
5. **Create transform file** in `src/pipelines/ingestion/{source}/{source}_transforms.py`:
   - A `beam.DoFn` that converts raw rows to Layer objects
   - A `beam.PTransform` that orchestrates: read raw → transform → DeltaDatasets → GenerateEvents
6. **Create pipeline file** in `src/pipelines/ingestion/{source}/{source}_pipeline.py`:
   - `run_{source}_ingestion_pipeline(pipeline_options)` function
   - Reads source data + extant layers, passes through transforms, writes events to PubSub
7. **Create PubSub sink topics** in `src/constants/pubsub_output_topics.py`
8. **Register in entrypoint**:
   - Add `PipelineName` enum value in `src/constants/pipeline_names.py`
   - Import and add to `RUN_METHODS` dict in `src/entrypoint.py`
9. **Add Makefile target** for local testing
10. **Write tests** mirroring `src/` path in `test/`

### Example: Crunchbase Pipeline Structure

```
src/pipelines/ingestion/crunchbase/
├── crunchbase_pipeline.py                  # run_crunchbase_ingestion_pipeline()
├── crunchbase_person_transforms.py         # GeneratePersonLayerFromCrunchbaseInput (DoFn)
│                                           # TransformCrunchbasePeopleToPersonEvents (PTransform)
├── crunchbase_employment_transforms.py     # GenerateEmploymentLayerFromCrunchbaseInput (DoFn)
│                                           # TransformCrunchbaseJobToEmploymentEvents (PTransform)
└── crunchbase_organization_transforms.py   # GenerateOrganizationLayerFromCrunchbaseInput (DoFn)
                                            # TransformCrunchbaseOrganizationsToOrganizationEvents (PTransform)
```

## DeltaDatasets Pattern (Core Diffing Transform)

Location: `src/transforms/delta_dataset_transforms.py`

DeltaDatasets is a `beam.PTransform` that takes `(new_entities, extant_entities)` and outputs `DeltaDatasetsOutput` with `.to_upsert` and `.to_discard` PCollections.

### Usage

```python
delta = (new_entities, extant_entities) | "Delta" >> DeltaDatasets(
    get_key_fn=lambda x: x.unique_key,           # Required: match key
    get_group_key_fn=lambda x: x.source,          # Optional: group before matching
    dedupe_fn=lambda dupes: dupes[0],              # Optional: pick winner from duplicates
    upsert_if_fn=compare_entities_for_upsert,      # Optional: custom diff logic
    discard_from_empty_groups=True,                 # Discard extant if no new? (default True)
    crossover_id_field="person_id",                 # Optional: copy ID from extant to new
    check_source_integrity=True,                    # Verify single source per collection
    filter_already_discarded=True,                  # Skip already-discarded extant
)
upserted = delta.to_upsert
discarded = delta.to_discard
```

### How It Works

1. Groups new and extant by `get_group_key_fn` (or `get_key_fn`)
2. Within each group, matches entities by `get_key_fn`
3. For matched pairs: runs `upsert_if_fn` to check if changed → emits to_upsert if different
4. New without match → to_upsert
5. Extant without match → to_discard (if `discard_from_empty_groups=True`)
6. Already-discarded extant entities are skipped

### compare_entities_for_upsert

Default comparison: `model_dump(exclude_unset=True)` on both, then dict comparison allowing partial dicts (new entity may not have all fields). Returns True if any field differs.

## Event Generation Pattern

Location: `src/transforms/event_generator_transforms.py`

### GenerateEvent (DoFn)

```python
upsert_events = layers | "Generate" >> beam.ParDo(
    GenerateEvent(
        event_publisher=PipelineName.CRUNCHBASE_INGESTION,
        event_type=UpsertPersonLayerEvent,
        data_wrapper_fn=lambda pl: PersonLayerEventDataWithRelations(person_layer=pl),
    )
)
```

### GenerateGroupedEvents (PTransform)

Groups events by a key function before generating — used when PubSub ordering matters:

```python
events = layers | GenerateGroupedEvents(
    event_publisher=PipelineName.CRUNCHBASE_INGESTION,
    event_type=UpsertEmploymentLayerEvent,
    group_key_fn=employment_event_by_person_grouping_key_fn,
    data_wrapper_fn=lambda el: EmploymentLayerEventDataWithRelations(employment_layer=el),
)
```

## Source Unique ID Pattern

Location: `src/sources/source_unique_ids.py`

Every source has generator functions producing consistent unique IDs:

```python
# Format: "{source_type}:{identifier}"
generate_crunchbase_person_unique_id(uuid)     → "crunchbase_person_id:{uuid}"
generate_mixrank_linkedin_profile_unique_id(id) → "mixrank_linkedin_profile_id:{id}"
generate_apollo_person_unique_id(id)            → "apollo_person_id:{id}"
generate_labeling_person_unique_id(person_id)   → "person_labeling:{person_id}"
```

## Adding a New Transform

### DoFn Pattern (element-level processing)

```python
class GeneratePersonLayerFromSource(beam.DoFn):
    def process(self, element: SourceRow) -> t.Iterable[PersonLayer]:
        yield PersonLayer(
            source=SourceName.MY_SOURCE,
            source_unique_id=generate_my_source_unique_id(element.id),
            given_name=element.first_name,
            # ... map fields
        )
```

### PTransform Pattern (composed pipeline stages)

```python
class TransformSourceToPersonEvents(beam.PTransform):
    def expand(self, pcolls: tuple[PCollection, PCollection]) -> tuple[PCollection, PCollection]:
        raw_data, extant_layers = pcolls

        new_layers = raw_data | "Transform" >> beam.ParDo(GeneratePersonLayerFromSource())

        delta = (new_layers, extant_layers) | "Delta" >> DeltaDatasets(
            get_key_fn=lambda x: x.unique_key
        )

        upsert_events = delta.to_upsert | "Upsert Events" >> beam.ParDo(
            GenerateEvent(
                event_publisher=PipelineName.MY_INGESTION,
                event_type=UpsertPersonLayerEvent,
                data_wrapper_fn=lambda pl: PersonLayerEventDataWithRelations(person_layer=pl),
            )
        )
        discard_events = delta.to_discard | "Discard Events" >> beam.ParDo(
            GenerateEvent(
                event_publisher=PipelineName.MY_INGESTION,
                event_type=DiscardPersonLayerEvent,
                data_wrapper_fn=lambda pl: PersonLayerEventData(person_layer=pl),
            )
        )
        return upsert_events, discard_events
```

## Adding a New Data Type

1. Create the Pydantic model in `src/data_types/`
2. If it's a nested type used in a Layer, add it to the appropriate Layer class
3. If source-specific, put in `src/data_types/{source}/`
4. Run `make dump_schemas` to regenerate JSON schemas
5. Run `make lint` to verify type correctness

## Testing Patterns

### Test Structure

Tests use pytest with Apache Beam's `TestPipeline`:

```python
import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to

def test_my_transform():
    input_data = [MyModel(field="value")]
    expected = [ExpectedModel(field="transformed")]

    with TestPipeline("FnApiRunner") as pipeline:
        pcoll = pipeline | beam.Create(input_data)
        result = pcoll | MyTransform()
        assert_that(result, equal_to(expected))
```

### Key Testing Imports

```python
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to
```

### Testing DeltaDatasets

```python
with TestPipeline("FnApiRunner") as pipeline:
    new = pipeline | "New" >> beam.Create(new_entities)
    extant = pipeline | "Extant" >> beam.Create(extant_entities)
    delta = (new, extant) | DeltaDatasets(get_key_fn=lambda x: x.id)
    assert_that(delta.to_upsert, equal_to([...]), label="upserts")
    assert_that(delta.to_discard, equal_to([...]), label="discards")
```

### Testing DoFns Directly

```python
def test_my_dofn():
    dofn = MyDoFn()
    input_element = SourceRow(...)
    results = list(dofn.process(input_element))
    assert len(results) == 1
    assert results[0].field == "expected"
```

### Running Tests

```bash
make tests                              # All tests, parallel
make tests test/path/to/test_file.py    # Specific file, verbose
```

## Binding Pipeline Pattern

Location: `src/transforms/binding_transforms.py`

Binding resolves which Layers represent the same real-world entity:

1. **Group layers** by bindable fields (e.g., LinkedIn slugs, domains, names)
2. **Create `BoundLayerGroup`** clusters of matched layers
3. **Assign entity IDs** — new UUID for new groups, existing for matched
4. **Emit update events** with the bound entity IDs

Key classes:
- `BoundLayerGroup[L]`: A group of layers bound to one entity
- `LayerGroupIndex[L]`: Index structure for fast binding lookups
- `GenerateBoundLayerGroups(DoFn)`: Creates groups from layers
- `FoldLayersIntoGroups(PTransform)`: Multi-pass binding with existing groups

## PubSub Sink Pattern

```python
from sinks.pubsub_sink import WriteEventsToPubsub

_ = events | "Write events" >> WriteEventsToPubsub(
    pipeline_options=pipeline_options,
    topic=MyPipelineSinkTopics.UPSERT_PL_EVENTS,
    event_grouping_key_fn=person_event_grouping_key_fn,  # Optional
)
```

## BigQuery Sink Pattern

```python
from sinks.bq_sink import WriteToBQ

_ = records | "Write to BQ" >> WriteToBQ(
    table=BQTable(...),
    pipeline_options=pipeline_options,
)
```

Note: WriteToBQ automatically skips writes in `read_only` or `test_mode`.

## QuickDedupe / Latest.PerKey Determinism Gotcha

`QuickDedupe(key_lambda, window_size=None)` with no `dedupe_fn` falls through to
`beam.combiners.Latest.PerKey()` (`src/transforms/quick_dedupe_transform.py:48-51`).
"Latest" compares element *event timestamps* — but in a batch pipeline whose source
never assigns them (file/BQ reads without `TimestampedValue`), every element carries
`MIN_TIMESTAMP`, and `LatestCombineFn` resolves ties by arrival order (bundle/worker
scheduling). Three consequences:

1. **Tie-break is nondeterministic across runs.** If two same-key elements differ in
   any field, the survivor can flip per run. When the dedupe key is a synthesized
   natural key that *excludes* content fields (e.g. a `source_unique_id` hash), the
   downstream upsert comparator sees a "change" on every flip → perpetual event churn.
2. **ParDo outputs inherit the input element's timestamp**, so duplicates emitted from
   one input row always tie — streaming timestamps wouldn't help those.
3. `window_size=None` puts the combine in the global window, which only fires in
   batch; it's a batch-only signature (streaming callers must window first).

**Rule:** whenever the dedupe key doesn't cover the full element content, pass an
explicit deterministic `dedupe_fn` (e.g. max over a canonical serialization). Only
skip it when key == full content, where any winner is identical.

Empirical demo (elements print `Timestamp(-9223372036854.775)`; tied-timestamp winner
follows feed order): run a `beam.Create | FlatMap(fn, ts=beam.DoFn.TimestampParam)`
pipeline and call `LatestCombineFn().add_input` with equal timestamps in both orders.
