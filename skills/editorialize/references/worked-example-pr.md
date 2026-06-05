# Worked example: PR description

A markdown-structured artifact through the three passes. The stage-0 draft is structurally faithful to a real shipped PR (headers, bullet patterns, provenance paragraph, footer) with the domain fictionalized; the markdown shapes and tells are the specimen, the pipeline names are invented.

The lesson differs from the paragraph example: real shipped output is often nearly clean at the language level, so humanize is close to a no-op, editorial does the heavy structural lift, and voice is a light final glaze. The passes do different amounts of work depending on the artifact; that variance is normal.

## Stage 0, the shipped draft

> ## Summary
>
> Adds two batch + one-off Beam binding pipelines that assign `subscription_id` / `seat_id` to ingested `SubscriptionLayer` / `SeatLayer` rows and emit `Update*LayerEvent`s: the binding step ACME-77 ingestion left as a TODO. Mirrors the existing `bind/*` packages and uses the shared clustering framework, so it's multi-source-ready without copying the legacy hand-rolled account machinery.
>
> Re-lands the binding work from #123 directly on `main`. The original PR merged into the stacked `acme-77-dedup` branch rather than `main`, so the two dedup commits are intentionally excluded here (they remain owned by #99).
>
> ## What's included
>
> - Projection models: `SubscriptionLayerForBinding`, `SeatLayerForBinding` (narrow `…ForBinding` projections); 4 types added to the `binding_transforms.L` TypeVar.
> - `bind_subscriptions`: reads `SubscriptionLayer`s joined to bound account `organization_id`s, clusters by `(account, plan, term)`, assigns `subscription_id`.
> - `bind_seats`: reads `SeatLayer`s joined to bound `person_id` + parent `subscription_id`, clusters by `(person, subscription)`, assigns `seat_id`. Runs after `bind_subscriptions`.
> - Registration: 2 new sink topics, 4 pipeline names + 2 configs (`has_one_off=True`), entrypoint wiring, 2 weekly Airflow DAGs ordered after the account/person binds and each other.
>
> ## Key design decisions
>
> - No layer-ref resolution in binding. Ingestion ships `(source, source_unique_id)` refs; the downstream processor resolves them into `*_layer_id` columns. Binding reads the populated, indexed columns and joins on them.
> - Shared clustering framework, not the legacy 650-line account copy.
>
> 🤖 Generated with Claude Code

## Stage 1, humanized

Run tell-check, then judge. Findings on this draft:

- The 🤖 footer trips the emoji rule. Judgment: it is a provenance marker, and the humanize pass exists to remove AI mannerisms from writing she directs and owns, never to disguise authorship she wants disclosed. Keeping or cutting it is the author's call, made explicitly, not hygiene applied by default.
- "Shared clustering framework, not the legacy 650-line account copy" matches the X-not-Y shape. Judgment: it is contrastive information, terse, and earns the construction. Kept. Single hits prove nothing; the blacklist has a judge.
- Otherwise clean. "Re-lands", "hand-rolled account machinery", and "the binding step ingestion left as a TODO" are human texture already; touch nothing.

Net change from this pass: zero edits, two recorded judgments. That is a valid outcome.

## Stage 2, editorialized

House style (post-#459): brief, tabular, one field per row, no narrative sections. Three headers on a one-screen body organize nothing. The Summary paragraph narrates what a table can carry. The provenance paragraph is worth one line, not two.

> Adds the binding step ACME-77 ingestion left as a TODO: batch + one-off pipelines that assign `subscription_id` / `seat_id` and emit update events. Re-lands #123 on `main`; the two dedup commits stay with #99.
>
> | Change | Where |
> |---|---|
> | `SubscriptionLayerForBinding`, `SeatLayerForBinding` projections; 4 types on `binding_transforms.L` | models |
> | `bind_subscriptions`: cluster by `(account, plan, term)`, assign `subscription_id` | `bind/subscriptions` |
> | `bind_seats`: cluster by `(person, subscription)`, assign `seat_id`, runs after `bind_subscriptions` | `bind/seats` |
> | 2 sink topics, 4 pipeline names, 2 configs (`has_one_off=True`), 2 weekly DAGs after the account/person binds | registration |
>
> Design note: no layer-ref resolution in binding. Ingestion ships `(source, source_unique_id)` refs, the downstream processor resolves them into `*_layer_id` columns, and binding joins on the indexed result. Shared clustering framework, not the legacy 650-line account copy.
>
> 🤖 Generated with Claude Code

Roughly half the length, zero headers, the table carries the inventory. The argument got sharper (the TODO callback now opens the piece); no sentence-level texture was touched.

## Stage 3, voiced

In a house-structured PR the voice lives in verb choice and the rare aside, never ornament; the structure is locked and the audience is reviewers. Two word-level moves:

> Design note: binding never re-derives refs. Ingestion ships `(source, source_unique_id)`, the downstream processor pays to resolve and index them, and binding joins on the columns someone already paid for. Shared clustering framework, not the legacy 650-line account copy.

"Pays for" carries the actual argument (the cost lives upstream on purpose) in her register. Everything else stands. A voice pass that changes two phrases in a PR is the pass working, not failing.

## What to notice

- Pass effort inverted versus the paragraph example: humanize 0 edits, editorial heavy, voice light. The artifact dictates the distribution.
- The footer survived two passes that flag it, because both deferred the same question to the author. Hygiene never overrides disclosure.
- Editorial enforced house structure without touching texture; the texture that existed at stage 0 ("Re-lands", "hand-rolled") is still present at stage 3.
