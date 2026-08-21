---
name: taxonomy-workbook-regen
description: Regenerate the job-function taxonomy review workbook from the current spec, run the full consistency battery, and stage it to Drive with supersede protocol. Use when the taxonomy spec changes, before recirculating to reviewers, or on "regenerate the workbook", "is the workbook consistent", "recirculate to EZ/Jacqueline". Not for spec edits themselves (use add-function-carveout).
---

# Taxonomy Workbook Regen

Regenerate `job-function-taxonomy.xlsx` from the live spec and prove every tab agrees with every other artifact before it circulates. Born from the 2026-08-21 session where three workbook generations were live at once (544/570/573 keys) and the Volumes tabs spoke a pre-rename vocabulary the Keywords tab had already left behind.

## Locations

- Generator: `~/Documents/git/workpod/projects/role-ontology-overhaul/threads/vvencill-job-function-taxonomy/build_function_workbook.py`
- It hardcodes `~/Documents/git/data-universe-pipelines` (module import + `docs/job_function_taxonomy.md` parse) — the spec branch (`vvencill/sup-420-taxonomy-swap` until merged) MUST be checked out in the main clone. Worktrees are invisible to it.
- `VOLUMES_DIR` near line 212 picks the volumes run. The volumes run must be measured **at the same spec commit** the Keywords/Functions tabs render, or the measurement tabs speak a stale vocabulary.

## Procedure

1. Check out the spec branch in the main clone (verify clean tree first).
2. If the spec changed since the last volumes run, re-measure first — no prod access needed:
   `.venv/bin/python scripts/job_function_volume/volume_accounting.py --input ~/Documents/git/workpod/assets/titles.ndjson.gz --out-dir <thread>/volumes-runN/`
   (multiprocessing; minutes, not hours; exits nonzero on balance-invariant violation). Keep prior runs; bump N.
3. Point `VOLUMES_DIR` at the new run.
4. `uv run --with openpyxl python3 build_function_workbook.py` — stdout must say `Volumes: loaded` and the keyword-row count must equal live + removed keys.
5. Run the battery (`scripts/` in this skill; update the pinned `TIP` commit in `diff_workbook_vs_spec.py` first):
   - `diff_workbook_vs_spec.py` — workbook keys vs spec keys 1:1. Expected noise: 5 band-marker strings on the spec side, the 16 removed keys as deliberate workbook rows.
   - `verify_workbook_part2.py` — exact invariants: 113 function values, 20 hatches, Volumes AND Migration each sum to the corpus total (1,423,915,893) with diff 0.
   - `verify_workbook_part3.py` — vocabulary currency: no pre-rename value names in Volumes/Migration, current carve-out keys present in Keywords. Update its key/name lists as the spec evolves.
6. Restore the main clone to `main`.

## Trust the Closing Invariant, Not String Grep

The accounting-closes-to-corpus check (diff 0) mathematically proves all state rows are present. A string-grep "state missing" failure against that is the grep pattern being wrong — this false-failed twice in one session (states are named `1_null_title`, `3_no_keyword_match`, not prose). Never "fix" the workbook to satisfy a grep heuristic.

One legitimate historical mention survives: the Functions-tab note "Renamed from HR operations…" — rationale text, not a value. Part-3 scopes its checks to Volumes/Migration for this reason.

## Drive Staging

See the `drive-deliverables` skill for connector constraints. Workbook specifics:
- The connector cannot upload the xlsx (classifier blocks large base64) — Vanessa drags it into Drive, sends the URL; then retitle it `Job Function Taxonomy YYYY-MM-DD` via `update_file`.
- Retitle every prior Drive copy with `(superseded YYYY-MM-DD)`. Never trash them — reviewer comments (e.g. Jacqueline's) live on old copies.
- If a copy must not circulate yet, retitle with a `(HOLD - <reason>)` marker.
- Spot-check the uploaded copy post-drag (read content, grep a carve-out key and a banned pre-rename name) — verify what circulates, not just the local file.

## After Regen

- Any doc that says "the regenerated export is coming" (answer docs, PR bodies) must be updated to link the sheet — stale forward references caused a v4/v5 churn once.
- The design doc's measured-outcome section (§12) drifts when volumes are re-measured; flag the deltas for Vanessa to rule on rather than editing figures silently.
- Log the regen (run number, spec commit, key counts) as a dated line in the thread's plan.md.
