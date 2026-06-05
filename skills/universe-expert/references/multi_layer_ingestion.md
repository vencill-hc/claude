# Multi-Layer Ingestion (one source → two related layers)

When a single source produces **two related layer types** in one ingestion pipeline, you hit
a cluster of problems that a single-layer pipeline never sees: parent-child invariants,
records the source models inconsistently, and "does the referenced thing exist" checks.

The canonical example is Crunchbase investment ingestion (PR #405), which emits both
`InvestmentLayer` (IL) and `InvestmentPartnerLayer` (IPL — one person per investment) from
the same run. Read this when adding any ingestion that emits a parent layer and a child
layer that references it.

Reference files:
- `src/data_types/investment_types.py` — `InvestmentLayer` / `InvestmentPartnerLayer`
- `src/pipelines/ingestion/crunchbase/crunchbase_investment_transforms.py` — the two
  `Transform…To…LayerEvents` PTransforms and their helper DoFns

## Pattern 1 — Parent-child layer invariant

A child layer must never be emitted without its parent. Enforce this **by design**, even
when today's data has zero orphans.

- The child's FK to the parent (`InvestmentPartnerLayer.investment_layer_id`) stays `None`
  at ingestion. It is resolved later, during **binding** (separate `bind_investments`
  ticket) — ingestion never sets cross-entity bound IDs.
- Gate the child stream on the existence of a matching parent. In #405,
  `_RequireMatchingInvestmentLayer` CoGroupByKeys IPLs against the freshly-built IL stream on
  `(investor_uuid, funding_round_uuid)`; IPLs with no matching IL are dropped and counted
  (`DEBUG_orphan_partner_dropped`). The gate also stamps the parent's
  `crunchbase_investment_uuid` into the child's `source_metadata` so the downstream event
  builder can construct the parent reference.
- This is why the IL transform **returns its `new_investment_layers` PCollection** even
  though it also emits events — the IPL transform consumes it as the existence gate input.
  Note it returns the *unfiltered* IL collection so the orphan-drop counter isn't polluted
  by DSR drops (see [[dsr_filtering]]).

`InvestmentPartnerLayerRead` makes the invariant explicit by re-declaring
`investment_layer_id: UUID` (non-optional) — the read model from the DB always has it, even
though the ingestion-time write model allows `None`.

## Pattern 2 — Synthesize layers for schema parity

When a source models some entities differently from others, **synthesize** the missing
records so downstream consumers get one uniform shape and a single query path.

Crunchbase models firm deal partners as `investment_partners` rows, but angel/individual
investors appear only as `investor_type="person"` on an `investments` row — never as a
partner row. To keep one person-investment query path,
`GenerateInvestmentPartnerLayerFromDirectInvestor` synthesizes an IPL for those direct
investors.

Rules that make synthesis safe:
- **Carry a synthetic `source_unique_id`** so real-vs-synthetic is detectable downstream.
  Use a dedicated generator with a distinguishing prefix
  (`generate_crunchbase_direct_investor_unique_id` → `crunchbase_direct_investor_id:…`).
- **Keep real foreign keys real.** The synthetic id goes only where a real partner id would
  live (`crunchbase_investment_partner_uuid`); fields that downstream code parses as a
  `UUID` (e.g. `crunchbase_partner_uuid`, used to build the `PersonLayer` reference) must
  still hold a real UUID — for a direct investor, the investor *is* the person, so mirror
  `investor_uuid` there. Storing the synthetic id in a slot that gets `UUID(...)`-parsed
  will raise.

## Pattern 3 — Validate "does it exist" with data + a diagnostic counter, not a blocking join

Before adding a defensive `CoGroupByKey` existence check on a foreign key, **query the source
dump** to confirm orphans actually occur. In #405, the dump had 1,274,720 investments and
**0** without a matching funding round — so a blocking existence check buys nothing that
PubSub's nack-retry (30-day TTL) doesn't already handle for genuinely-missing references.

The pattern that replaced the blocking check:
- Use a plain `InnerJoin` that **silently drops** unmatched rows (you've proven there are
  none).
- Run a **parallel diagnostic** `CoGroupByKey` whose DoFn emits *no output*, only a counter
  (`_CountInvestmentsWithoutFundingRound` → `DEBUG_investment_without_funding_round`). It
  costs a shuffle but tells you immediately if the upstream data drifts and the
  "zero orphans" assumption breaks.

## Pattern 4 — Cheap dedup + counter when two sources are "disjoint"

When two row streams feed the same layer and the source model says they're disjoint, keep an
inexpensive dedup anyway and attach a counter so production reports drift.

`_DedupPartnerRowsByPersonRound` CoGroupByKeys the real and synthesized partner rows on
`(funding_round_uuid, partner_uuid)`, **prefers the real row** on collision, and increments
`DEBUG_real_and_direct_partner_overlap` when overlap is seen. It emits tagged outputs so each
kind routes to its own layer-construction DoFn. The reviewer's note on #405: *"I like the
counter!"* — cheap defensive checks earn their keep when they come with observability.

## Pattern 5 — `crunchbase_updated_at` idempotency footgun (repo-wide)

Crunchbase layer builders stamp `crunchbase_updated_at` (the export timestamp) into
`source_metadata` (see lines ~98, ~149, ~193 of `crunchbase_investment_transforms.py`).
Because `DeltaDatasets` compares `source_metadata`, a timestamp that changes every export
makes **unchanged layers re-upsert on every daily run**.

This is a **known, repo-wide** Crunchbase pattern, not specific to investments. When you
touch it: do not "fix" it for one pipeline in isolation — it must be changed consistently
across all Crunchbase ingestions in one cross-pipeline PR, or the delta behavior diverges
between layer types. On #405 the reviewer accepted leaving it as-is precisely because the
other Crunchbase ingestions do the same thing.

## Quick reference

| Concern | Mechanism | Observability counter |
|---|---|---|
| Child needs parent | CoGroupByKey gate, FK left `None` until binding | `DEBUG_orphan_partner_dropped` |
| Inconsistent source modeling | Synthesize child + synthetic `source_unique_id` | — |
| "Does the FK target exist?" | InnerJoin (drop) + parallel diagnostic CoGroupByKey | `DEBUG_investment_without_funding_round` |
| Two "disjoint" sources | Dedup, prefer real, tagged outputs | `DEBUG_real_and_direct_partner_overlap` |
| Idempotency | Watch export timestamps in `source_metadata`; fix repo-wide | — |
