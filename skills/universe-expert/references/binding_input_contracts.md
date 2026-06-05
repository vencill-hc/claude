# Binding Input Contracts (`XxxLayerForBinding`)

Convention for any new or modified offline binding pipeline in `data-universe-pipelines`.

## The pattern

Binding pipelines are shuffle-heavy: Layers move through repeated Dataflow `GroupByKey` / `CoGroupByKey` / `MultiKeyLeftJoin` steps. The cost of every shuffle is proportional to the size of each Layer record. The source `XxxLayer` / `XxxLayerRead` models carry many fields the binder doesn't read (embeddings, highlights, funding events, addresses, descriptions, etc.) — these fat fields ride through every shuffle as dead weight.

The fix is a **narrowed Pydantic projection** holding only the columns the binder consumes, loaded from BQ/PG instead of the full Layer.

## Canonical example

```python
class OrganizationLayerForBinding(BaseModel):
    """
    Narrow projection of OrganizationLayer holding only the columns the binding pipeline
    consumes. Intentionally not derived from OrganizationLayer or OrganizationLayerRead so
    that unused columns are not pulled from BigQuery/Postgres and shuffled through Dataflow.
    """

    __test_mode_entity_id_column__: ClassVar[str] = "organization_id"

    id: UUID
    source: str
    source_unique_id: str
    organization_id: UUID | None = None
    organization_names: list[OrganizationLayerOrganizationName] | None = None
    domains: list[OrganizationLayerDomain] | None = None
    external_identifiers: list[OrganizationLayerExternalIdentifier] | None = None
    created_at: datetime
    discarded_at: datetime | None
```

## Rules

1. **`BaseModel`, not `XxxLayer` / `XxxLayerRead` inheritance.** Inheritance pulls every parent field through the shuffle even if the column is omitted from `SELECT`. A standalone model is the contract.
2. **Spell SELECT columns inline** in each BQ and Postgres query. Don't extract to a Python constant. Duplication across BQ + Postgres is intentional; Pydantic validation at parse time is the source of truth that columns match the projection. (User feedback memory `feedback_inline_sql_columns.md`.)
3. **Type all binder helpers on the narrowed type** — matching, scoring, bindable-fields extraction, DoFn process methods. Pyright then enforces the contract: any access to a dropped field fails lint.
4. **Keep the binder output type as `XxxLayer`** (or `XxxLayerRead`). The narrowed type is for *input*; downstream events still use the full Layer shape. `BindXxxIDsToGroup` constructs a fresh `XxxLayer(id=, ..._id=, source=, source_unique_id=)`.
5. **Extend the `L` TypeVar** in `src/transforms/binding_transforms.py` if the binder uses `BoundLayerGroup[L]` / `FoldLayersIntoGroups[L]`. Employments binder doesn't (uses its own infrastructure); organizations, people, and locations do.
6. **Skip narrowing when payoff is small.** Use judgment based on shuffle volume and field-fatness. Location was done for consistency but yields minimal savings.

## Implementation checklist

When narrowing a new binder (or adding a field that participates in binding):

1. **`src/data_types/<entity>_types.py`** — add or update `XxxLayerForBinding(BaseModel)` next to `XxxLayerRead`. Mirror the canonical example.
2. **`src/pipelines/bind/<entity>/bind_<entity>_sources.py`** — add `ReadAllXxxLayersForBinding(ReadQueryFromBQ)` with an inline-column SELECT. Update any Postgres SELECTs (one-off, streaming) to enumerate the same columns. Swap `model=XxxLayerRead` → `model=XxxLayerForBinding`.
4. **`src/pipelines/bind/<entity>/bind_<entity>_transforms.py`** — update all helper signatures from `XxxLayerRead` → `XxxLayerForBinding`. Keep `XxxLayer` for the output construction in `BindXxxIDsToGroup`. Update `PCollection[XxxLayerRead]` casts in `bind_<entity>_layers` to `PCollection[XxxLayerForBinding]`.
5. **`src/pipelines/bind/<entity>/bind_<entity>_pipeline.py`** — swap `ReadAllXxxLayers` for `ReadAllXxxLayersForBinding`. Update `PCollection[]` cast types. Drop now-unused `psycopg.sql.SQL` import if no longer needed.
6. **`src/transforms/binding_transforms.py`** — if `BoundLayerGroup`/`FoldLayersIntoGroups` is used, add the new type to the `L` TypeVar constraint list.
7. **Helpers like `utils/person_utils.py:normalized_full_name`** — broaden parameter unions to accept the new type if the binder calls them.
8. **Test fixtures** — swap `XxxLayerRead(...)` constructions to `XxxLayerForBinding(...)`. Drop constructor args for fields no longer in the projection (`updated_at`, etc.).
9. **Verify** — `make format`, `make lint` (pyright is load-bearing), `make tests`. **Do NOT run `make dump_schemas`** — CI regenerates schemas. Keeps logic commits clean and review-focused.

## Reference PRs

- gdulabs/data-universe-pipelines#414 — Employments (first; established the pattern)
- gdulabs/data-universe-pipelines#416 — Organizations
- gdulabs/data-universe-pipelines#417 — People (largest savings — `embeddings` dropped)
- gdulabs/data-universe-pipelines#418 — Locations (consistency; minimal savings)
- gdulabs/data-universe-pipelines#419 — Pattern documentation in `docs/concepts.md`
- gdulabs/data-universe-rails#787 — Rails-side doc note

## Known pre-existing footgun

`ReadAllXxxLayersForBinding.__init__` mutates a caller-provided `where_clauses` list via `.append`. If a caller reuses the list across multiple instantiations, the discarded-at clause stacks. All four binders have this pattern (inherited from #414's `ReadAllEmploymentLayersForBinding`). Fix is one line — `where_clauses = list(where_clauses or [])` — defer to a single follow-up PR that fixes all four. Don't flag on review of new binder narrowing work.
