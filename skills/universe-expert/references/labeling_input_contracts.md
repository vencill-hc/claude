# Labeling Input Contracts (`XxxLayerForLabeling`)

Sibling pattern to `binding_input_contracts.md`. Read that file first — the BaseModel-not-inheritance, inline-SELECT, and pyright-as-contract rules carry over verbatim.

## The pattern

Labeling pipelines read the extant labeling Layer (rows where `source == SourceName.UNIVERSE_LABELING`) from BigQuery (batch) or Postgres (streaming/one-off) and feed it into `DeltaDatasets` alongside freshly-computed labeling Layers. The extant read is the shuffle-heavy side and benefits from a narrow projection. Each entity has one: `PersonLayerForLabeling`, `EmploymentLayerForLabeling`, `OrganizationLayerForLabeling`.

Savings are smaller than binding (one `CoGroupByKey` per labeling pipeline vs. many for binding) but real, with the largest payoff on `PersonLayer` (drops `embeddings`).

## Canonical example

```python
class EmploymentLayerForLabeling(BaseModel):
    """
    Narrow projection of EmploymentLayer holding only the columns the labeling pipeline
    reads or writes.

    Fields that the labeling pipeline writes (job_function, seniority, board_roles,
    board_committee_memberships, source_metadata) MUST be included so DeltaDatasets can
    detect no-change cases when comparing freshly-computed labeling layers against extant
    ones.
    """

    __test_mode_entity_id_column__: ClassVar[str] = "employment_id"

    id: UUID
    source: str
    source_unique_id: str
    source_metadata: dict[str, str] | None = None
    employment_id: UUID | None = None

    job_function: JobFunction | None = None
    seniority: JobSeniority | None = None
    board_roles: list[BoardRole] | None = None
    board_committee_memberships: list[BoardCommitteeMembership] | None = None
```

## The rule that differs from binding

**The projection must hold every field the labeler reads AND every field the labeler writes.**

`DeltaDatasets.compare_entities_for_upsert` compares freshly-computed labeling Layers against extant ones via `model_dump(exclude_unset=True)`, field by field. If a labeler-written field is dropped from the extant-side projection, every comparison sees "new has it, extant doesn't" and emits a spurious upsert on every batch run. The first-pass version of #421 kept only read-fields and the no-delta test in `test_label_persons` caught it.

For binding, only read-fields matter (the binder's output is constructed fresh as a full `XxxLayer`). For labeling, both matter.

## The discard-event splat

`DeltaDatasets` has two output streams:

- **`to_upsert`** — keyed entries from the *new* feed (the labeler's output). Carries the full `EmploymentLayer` constructed by `inject_labeling_employment_layers` and mutated by `LabelJobDesignations` / `LabelBoardSeat`. The narrow type is not involved on this path.
- **`to_discard`** — keyed entries present only in the *extant* feed (read from BQ/PG as the narrow projection). These are stale labeling rows the current run no longer produces; downstream needs a tombstone event.

Discard event payloads are typed as the full `XxxLayer`. The narrow projections aren't subclasses, so each discard `data_wrapper_fn` splats the narrow projection into a full Layer to preserve the payload shape:

```python
data_wrapper_fn=lambda el: EmploymentLayerEventData(
    employment_layer=EmploymentLayer(**el.model_dump())
)
```

This is **lossless**, not "lossy but tolerable." Every field dropped from `XxxLayerForLabeling` was already `None` on `SourceName.UNIVERSE_LABELING` rows, because those rows are written exclusively by this pipeline, which only ever populates labeler-written fields. `EmploymentLayer(**narrow.model_dump())` defaults the dropped fields to `None` — byte-identical to what the pre-PR full read would have produced.

This is the answer to the recurring review concern: *"isn't the splat dropping fields we set on `XxxLayerForLabeling`?"* No — the labelers write to `bundle.update_employment_layer` (full type, flows through `to_upsert`); the narrow projection appears only on the extant read side feeding `to_discard`.

## The load-bearing invariant

> `XxxLayerForLabeling` ⊇ every field ever written by any code path on `SourceName.UNIVERSE_LABELING` rows.

While this holds:
- No spurious upserts (write-fields covered → `DeltaDatasets` comparison sees equality).
- Lossless discard splat (dropped fields were `None` on these rows).

When it breaks (a labeler starts writing a new field that isn't in the narrow type):
- Every batch run emits a spurious upsert for every row.
- The discard splat silently drops the new field from tombstone payloads.

**Mitigation**: when a labeler adds a new write target, add the field to `XxxLayerForLabeling` in the same PR. The docstring on each `XxxLayerForLabeling` should call out the read-fields ∪ write-fields rule so future contributors don't re-derive it.

## Implementation checklist

When narrowing a new labeling pipeline (or adding a labeler-written field):

1. **`src/data_types/<entity>_types.py`** — add or update `XxxLayerForLabeling(BaseModel)`. Include both read-fields and write-fields. Include `__test_mode_entity_id_column__`.
2. **`src/pipelines/label/<entity>/<entity>_labeling_source*.py`** — add `ReadAllXxxLayersForLabeling(ReadQueryFromBQ)` with an inline-column BQ SELECT. Update streaming/one-off Postgres SELECTs to enumerate the same columns. Wire bundle types to the narrow projection.
3. **`src/pipelines/label/<entity>/<entity>_labeling_transforms.py`** — the discard `data_wrapper_fn` splats narrow → full: `lambda el: XxxLayerEventData(layer=XxxLayer(**el.model_dump()))`. The upsert path is unchanged (operates on full Layer from the labeler bundle).
4. **`src/pipelines/label/<entity>/<entity>_labeling_pipeline.py`** — swap `ReadAllXxxLayers` for `ReadAllXxxLayersForLabeling`. Update `PCollection[]` cast types.
5. **Test fixtures** — swap extant-side constructions to `XxxLayerForLabeling(...)`. The existing no-delta tests catch missing write-fields.
6. **Verify** — `make format`, `make lint`, `make tests`. Do NOT run `make dump_schemas` locally (per `feedback_no_local_schema_dump.md`).

## Reference PRs

- gdulabs/data-universe-pipelines#414/#416/#417/#418 — Binding narrowing (sibling pattern; read first if unfamiliar)
- gdulabs/data-universe-pipelines#419 — Binding pattern documentation in `docs/concepts.md`
- gdulabs/data-universe-pipelines#421 — Labeling narrowing for employments, organizations, people (this pattern's establishing PR)

## Out of scope

The **materialized-Entity helpers** used by labeling (`PersonWithLayerIds`, `EmploymentWithOrganization`, `OrganizationWithLayerIds`) are a separate optimization category — inheritance-expansion of materialized entities rather than Layer narrowing. Different shape, different risk profile. Not covered by this pattern.
