# DSR Filtering (Data Subject Request scrubbing/suppression)

DSR = Data Subject Request. When a person submits a deletion/suppression request, ingestion
pipelines must stop creating or updating layers for them. This happens at the **tail of
ingestion, after layers are generated and before `DeltaDatasets`** — so a scrubbed person
never produces an upsert, and (critically) a scrubbed entity with no new layer doesn't look
like a net-deletion and fire a spurious discard.

Read this when adding DSR compliance to any ingestion pipeline, or when wiring a new source
that ingests person data.

Reference files:
- `src/transforms/dsr_transforms.py` — the three `FilterDsr…` PTransforms
- `src/sources/dsr_sources.py` — the digest fetchers
- `src/pipelines/ingestion/crunchbase/crunchbase_investment_transforms.py` — usage example

All matching is done on **HMAC-SHA256 digests** computed with the DSR HMAC secret
(`dsr_hmac_digest`, mirroring Rails' `DSR.hmac_digest`: lowercase + strip, then HMAC). The
secret comes from `DSR_HMAC_SECRET_OVERRIDE` or GCP Secret Manager (`dsr_hmac_secret`). Raw
PII is never compared in the pipeline.

## Two mechanisms

### 1. Scrubbed layers — `FilterDsrScrubbedLayers`

For people who **already have extant layers** that the DSR process has marked. An extant
layer is scrubbed when its `source_metadata` contains `dsr_scrubbed_at` (`is_dsr_scrubbed`).

- Takes a `(new_layers, extant_layers)` tuple, returns a `(compliant_new, compliant_extant)`
  tuple.
- Collects scrubbed extant `source_unique_id`s into a side input; drops any `new_layers`
  whose key matches; **also re-filters the extant side** so the scrubbed entity isn't seen
  by `DeltaDatasets` as a deletion. Both sides must flow into the delta.
- A custom `get_source_unique_id_fn` lets you scrub a layer because a *related* entity was
  scrubbed. For employments: call it once on the employment's own extants, then again on
  person extants with `get_source_unique_id_fn=lambda el: el.person_layer_id`.
- Counter: `dsr/scrubbed_new_layers_dropped`.

**Sentinel trick for "not applicable" rows.** When a related-entity extractor doesn't apply
to some layers (e.g. an org-investor IL has no related person), return a sentinel that can't
collide with a real id. #405 uses `_NON_PERSON_INVESTOR_SENTINEL = ""` — an empty string
never equals a real `generate_crunchbase_person_unique_id` output, so those layers pass
through untouched.

### 2. Suppressed layers — `FilterDsrSuppressedLinkedInSlugs` / `FilterDsrSuppressedEmails`

For people who submitted a DSR **before any extant layer exists** — `FilterDsrScrubbedLayers`
would miss them because there's nothing extant to match against. These pre-emptively filter
*new* layers against suppression tables:

- `FilterDsrSuppressedLinkedInSlugs` — digest of the LinkedIn slug vs
  `dsr.suppressed_linkedin_slugs`. Pass a `get_linkedin_slug_fn`; layers returning `None`
  pass through. Counter: `dsr/linkedin_slug_suppressed`.
- `FilterDsrSuppressedEmails` — `(email_digest, name_digest)` pair vs `dsr.suppressed_emails`.
  Pass `get_emails_fn` and `get_name_fn`; layers with no email or no name pass through.
  Counter: `dsr/email_suppressed`.

**Per-worker TTL cache.** Suppression sets are tiny (single digits) and change rarely, so
each worker fetches the set on its first element and caches it. Streaming pipelines refresh
every `_DSR_SUPPRESSION_TTL_SECONDS` (15 min), bounding staleness to ≤1 TTL per worker; batch
pipelines fetch once (point-in-time snapshot). This deliberately avoids a globally-consistent
`PeriodicImpulse` side input — see the docstring on `_CachedSuppressionFilter` for the
trade-off rationale.

## Where it slots in the pipeline

Always: **generate new layers → DSR filters → `DeltaDatasets` → events.** Example from the
investment IL transform:

```python
new_investment_layers = investments_enriched | "Generate…" >> beam.ParDo(...)

# Pass 1: own extants scrubbed.  Pass 2: related PersonLayer scrubbed (sentinel for non-person).
dsr_new, dsr_extant = (new_investment_layers, extant_investment_layers) \
    | "Filter DSR-scrubbed InvestmentLayers" >> FilterDsrScrubbedLayers()
dsr_new, _ = (dsr_new, extant_person_layers) \
    | "Filter InvestmentLayers with DSR-scrubbed Person" \
    >> FilterDsrScrubbedLayers(get_source_unique_id_fn=_investment_layer_person_investor_unique_id)

deltas = (dsr_new, dsr_extant) | "Delta…" >> DeltaDatasets(...)
```

Note both the DSR-compliant **new** and **extant** collections feed the delta — dropping the
re-filtered extant side would resurrect the spurious-discard bug the transform exists to
prevent. Organizations are not DSR-scrubbable, so org investee/investor layers are
intentionally left unfiltered.
