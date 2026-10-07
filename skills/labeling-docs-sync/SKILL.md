---
name: labeling-docs-sync
description: Use after merging any labeling change in data-universe-pipelines - job function keywords, seniority parsing, industry mappings, person highlights, funding-stage bands, board-seat rules - or on "update the mappings sheet", "is the mappings doc current", "regenerate the field mappings", "publish the mapping workbook", "what changed in labeling since". Also before reviewers consume the mappings folder. Not for the taxonomy review workbook (taxonomy-workbook-regen) or spec edits (add-function-carveout).
---

# Labeling Docs Sync

Keep the reviewer-facing "GDU Field Derived Mappings" workbook truthful to the labeling code on `origin/main`. Consumers are **non-technical** — every tab leads with a plain-language intro, keyword tables use human-readable phrases (never regex or sentinel tokens), and jargon stays out. Versioning is additive: each sync drops a NEW dated file in the shared folder; old versions are never edited or trashed.

## Config

- **Drive folder**: `PENDING — Vanessa is setting up the shared folder; ask for the folder ID/URL and record it here.` Until then, create in My Drive root and tell her to move it.
- **File naming**: `GDU Field Derived Mappings YYYY-MM-DD` (date of the sync, not of the code change).
- Original circulating sheet (read-only reference, owned externally): Drive `1Rn5CFPnnQRteIn_WIfm3E7QZL-ocypaJ`.
- Sync log: `~/Documents/git/workpod/projects/pe-594-seniority-classification/threads/vvencill-pe-594-master-tracking/notes.md` under `## Sheet sync log`. **First-ever sync / no log entry**: do a full regeneration and start the log; don't hunt for a baseline that doesn't exist.

## What the workbook covers, and what code feeds each tab

| Tab | Source of truth (all in `~/Documents/git/data-universe-pipelines`) |
|---|---|
| Industry Mapping | `src/constants/industry_mappings.py` (Crunchbase 800, Investor 22, LinkedIn 540 keys) |
| Job Function Mapping | `src/utils/job_function_taxonomy.py` `SPEC_BANDS` (five bands, order = priority, `None` = blocker) and `REMOVED_KEYWORDS`; `employment_utils.JOB_FUNCTION_TITLE_COMPONENTS` is the flattened re-export the multi-tab generator still imports. Rationale and function descriptions: `docs/job_function_taxonomy.md`. |
| Seniority Mapping | `src/utils/seniority_utils.py` + `board_seat_utils.py` exclusions + `string_validator_utils.py` synonyms |
| Highlight Mapping | curated `assets/highlights.csv` (reviewed language), audited against `PersonLayerHighlight.GenericValue` (`src/data_types/person_types.py`); rule thresholds live in `src/pipelines/label/people/person_highlights_transforms.py` |
| Funding Mapping | `OrganizationLayerFundingEvent.get_organization_stage` (`src/data_types/organization_types.py`) |

## Standalone Nova mapping docs (DAT-63 / DAT-64)

Chris's "Nova - <X> Mapping" Drive folders (parent `10s6LwePwHefzYoYI8XaeEW82qzdwU8mk`) hold one "(Original)" sheet each from 2026-08-27 plus dated update subfolders. New versions are separate files next to the original, never edits.

- Function: `scripts/build_function_mapping_doc.py <out.xlsx>` with `GDU_REPO=<clean main checkout>`; run it from the main clone so `uv run` has the project deps (a bare worktree venv lacks `phonenumbers`). Tabs: keyword table by band, functions catalog, removed keywords, delta against `assets/function_mapping_original_2026-08-27.csv`. Target folder `1B_CGgdUKQK3MfgIdXtIyTkGXED46wbiF` (subfolder "September 2026 Updates" `1WD0tJD5Qbo3S4bMKi2Y6TEE1jOo6YDBi`). Original sheet `1EjP_mhnbypZ4kmdZKDTo4Zs63x9Uivxq5WXSW2bwoDQ`.
- Industry: `scripts/build_industry_mapping_doc.py <out.xlsx>`, same invocation. Tabs: edge table with market/capability kind, GDU industry catalog with feeder counts, consulting rule, three-way delta (original sheet vs code on 27 Aug vs now; `assets/industry_mapping_original_2026-08-27.csv` and `assets/industry_mapping_code_2026-08-27.csv`). Chris's original sheet held only 356 of the 1,026 LinkedIn edges the code had that day, so the delta marks those "Missing from original" rather than "Added". Folder `1K4L_h2y6S19l2nWeHMa1lOW7l1zxdsw4` (subfolder "September 2026 Updates" `1zL4iQeKl7Jrk_wEcWswoZJ7eoMiWo00L`), original sheet `14R6AaKwT3RvCbPZzS614IW1h7gUhu2dfayWCVkEdKnM`.
- A ~50KB xlsx is too large to pass through the Drive connector as base64 from this side; the xlsx lives in its workpod thread (never copy it elsewhere); Vanessa drags it into the folder from there, then retitle with `update_file` if needed.

## Procedure

1. **What changed**: `git -C <repo> fetch -q origin main`, then `git log --format='%h %ad %s' --date=short origin/main -- <files above>` and compare to the last hash in the sync log. Nothing new → say so, stop.
2. **Pending changes**: `gh pr list --repo gdulabs/data-universe-pipelines --state open`, then `gh pr view N --json files` for PRs touching the source files. A hit in a shared file (`job_types.py`, `employment_utils.py`) is only relevant if the diff touches the labeling constants/enums this workbook renders — check the diff hunks, not just the filename. Report pending PRs to Vanessa separately; never fold unmerged work into the workbook.
3. **Highlight-rule audit** (the one non-generated tab): if `person_highlights_transforms.py` or `PersonLayerHighlight` changed since the last sync, read the diff and update `assets/highlights.csv` prose to match (thresholds: 12+ mo backing tenure, 3+ startups = Serial, 120+ mo = Industry Veteran, 60+ mo = loyal, 2.0x valuation = growth — verify against code, don't trust this list). New enum values with no curated row render as visible NOT YET DOCUMENTED stubs — write the row with Vanessa rather than shipping the stub if time allows.
4. **Generate** on main: check out `main` in the pipelines clone (verify clean tree first; restore the prior branch after), then
   `uv run --with openpyxl python3 ~/.claude/skills/labeling-docs-sync/scripts/build_mappings_workbook.py <scratchpad>/gdu_field_derived_mappings.xlsx`
   Heed the drift WARNING (it diffs the source files against origin/main — a feature-branch checkout is fine only if it says identical). Check the printed invariants: industry rows > 2000, seniority rows = lexicon size, highlight enum coverage, undocumented list.
5. **Spot-read the output** as a consumer would: open one tab's rows and confirm no sentinel tokens (`_e_a_`, `cxo`) or regex leaked into the visible text.
6. **Publish**: upload the xlsx via the Drive connector `create_file` into the configured folder with the dated name. If the classifier blocks the upload (large base64 — a ~290KB xlsx has died this way; this workbook is ~100KB, usually fine), fall back per `drive-deliverables`: Vanessa drags the file in, then retitle via `update_file`.
7. **Log**: append to the sync log — date, main hash, tabs affected, pending PRs, Drive file ID.

## Traps

- `founder`/`owner` mapping to Uncategorized with kind EXEC_HEAD is intentional (PE-763); not a bug to normalize away.
- Two seniority orderings exist in code: `_LADDER` (resolution) and `PRIMARY_EMPLOYMENT_ORDINAL_SENIORITIES` (primary-employment pick). Only the ladder belongs in the workbook. The `JobSeniority` enum declaration order is neither — never render it as a rank.
- Seniority rule order: board disqualifier (rule 2) runs before board-seat exclusion (rule 6), so "Board Certified Surgeon" → Entry via `certified`, not Uncategorized.
- `is_fulltime` has no writer in the repo (derived at read time from `PART_TIME_JOB_TITLES`); it's a highlight ingredient, not a workbook tab.
- `DataUniverseIndustries` lives in `industry_mappings.py`, not `src/data_types/`.
- The generator imports the checkout directly — unmerged local branches change the output silently except for the drift warning. Trust the warning over your memory of what's merged.
- `SENIORITY_NOTES`/`TOKEN_DISPLAY` in the generator and `assets/highlights.csv` are the curated halves: reviewed plain-language phrasing lives there and follows `editorialize` register. When a code change makes a note stale, fix the note in the same sync.
