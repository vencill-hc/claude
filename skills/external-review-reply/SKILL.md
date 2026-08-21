---
name: external-review-reply
description: Answer a PM/client review question set (Zain, Jacqueline, EZ rounds) about GDU taxonomies, workbooks, or counts. Use when a thread doc or shared doc carries numbered questions about labels, keywords, mappings, counts that don't reconcile, or workbook methodology. Triggers - "answer these questions", "working through this doc", "Zain's questions", "question set", "the counts don't reconcile", "rebuild the workbook".
---

# External Review Reply

Answering a numbered question set from a PM or client reviewer about GDU taxonomy
artifacts (workbooks, review sheets, keyword maps, count claims). Ran twice at full
cost before this skill existed: the function-labeling set (2026-08-20) and the
industry-labeling set (2026-08-21). Both sessions independently rediscovered the same
arc; this skill is that arc.

## The Core Insight

Most count and spec questions from reviewers are **artifact-drift questions dressed as
spec questions**. The reviewer is reading a circulated snapshot; the spec moved. Before
answering anything, build the vintage table: for every artifact in play (their sheet,
your workbook, the code, each consented run), establish its date and what revision it
reflects. Then answer every question from the current source of truth and say which
artifact is stale and whether it will be regenerated. State this framing once, up
front, in the reply: it explains half the list.

## Workflow

1. **Read the question set in its original doc** (Drive MCP), not the user's paraphrase.
   The doc often carries an already-answered sibling section whose format is the
   template for yours.
2. **Locate ground truth before answering anything** (map below). Check the workpod
   thread's plan.md/notes.md first: a prior session may have answered half of it.
3. **Build the vintage table** (artifact → date → spec revision).
4. **Reconcile every floating count by deriving it from a concrete set.** A number like
   "141" or "544" is never explained by hand-waving; write a throwaway script that
   produces each candidate set and its cardinality until the reviewer's number either
   derives exactly or is shown to be a reconstruction artifact bounded by two real sets.
   Both outcomes are shippable answers; a vibe is not.
5. **Verify every citation yourself.** Agents paraphrase even when told to quote
   (standing VV feedback). Every file:line, label string, and number in the reply comes
   from a script you ran or a line you read this session.
6. **Produce data asks as artifacts, not prose**: self-contained export scripts written
   into the workpod thread (auto-locate the repo, self-checking asserts, CSV outputs
   next to the script). Anything prod-shaped becomes a drafted .sql + runner staged for
   a consent gate (section below).
7. **Draft the reply via the editorialize skill** and stage it in the thread as
   `<reviewer>-reply-<date>.md`. House format (ruled on the function answers doc, v2-v5):
   interview format, questions bold+italic when staged as a Doc; answers factual and
   agentless, no I/you; plain meaning attached to every number; Title Case headings;
   run `tell-check.py`. Stage as a private unshared Google Doc only when asked; VV
   reviews before anything is shared or pasted. Never send to the reviewer directly.
8. **Save state**: plan.md gets dated decision entries (surgical appends only),
   state.md gets a progress entry (append-only, cap 10, archive overflow to notes.md),
   notes.md gets the verification facts so no future session re-derives them.
   Cross-reference sibling threads that flagged the question set.

## Ground-Truth Map (GDU)

| What | Where |
|---|---|
| Function taxonomy spec | `src/utils/job_function_taxonomy.py` (repo, check the live PR branch) |
| Function parser semantics | `src/utils/employment_utils.py` (word-boundary prefix match, sentinel subs) |
| Industry canonical labels | `DataUniverseIndustries` enum, `src/constants/industry_mappings.py` (149) |
| Industry dictionaries | same file: CB (800 keys), LinkedIn (540), CB-investor (22); 1,362 keys / 2,811 edges |
| Non-dictionary label paths | legacy CX verbatim passthrough (`legacy_cx_transforms.py`); Apollo/PDL/linkedin_code map to nothing |
| Per-label org volumes | org-industry-resolution thread, `du_isic_audit.py` VOLUMES (2026-07-28 run) |
| Per-edge removal cost | dat-55 thread, `blast_radius.py` + `blast_radius.csv` (person-grain since 2026-08-21) |
| Circulated sheets | Drive search by title; read via Drive MCP. v1 workbook = by company type, v2 = by Nova label |
| Prior rulings | workpod thread plan.md Decisions log + the merge log / design doc for the taxonomy |

"Nova" is the client-facing product name; GDU/EZ/Nova stay undefined in replies (client
knows). "MixRank vs Crunchbase" means LINKEDIN-typed vs CRUNCHBASE-typed claims.

## Number Discipline

- "People" means distinct person profiles (`COUNT(DISTINCT person_id)`), never
  employment rows. Emit both grains under honest names ("people", "work histories").
  A circulated workbook shipped 20-30% high by violating this once.
- Attach a plain meaning to every number in reviewer-facing prose; internal jargon
  only in a flagged technical appendix.
- When two artifacts disagree, the reply names which one is wrong and which gets fixed.

## Consented Prod Runs

- SDK clients only (`google.cloud.bigquery`), never gcloud/bq CLI.
- Runner script in the thread, modeled on `blast_radius.py`: dry-run is the default
  and prints the bytes estimate; `--execute` gates the real run; `maximum_bytes_billed`
  guard; results written as CSV next to the script.
- Consent is per invocation, at runtime, in her words. "This needs to be fixed" names a
  defect, not a run: stage the fix, dry-run, then ask one short question. Prior
  consents never carry forward.
- Before a rerun overwrites a circulated artifact, preserve the old file under a dated,
  reason-suffixed name (`blast_radius-2026-08-18-workhistories.csv`).

## Common Mistakes

| Mistake | Fix |
|---|---|
| Answering the reviewer's framing instead of checking the artifact they're reading | Fetch their sheet/doc; their question often describes a layout you replaced |
| Trusting a sub-agent's quoted line numbers | Re-read cited lines yourself before they go out as fact |
| Explaining a count discrepancy in prose | Derive each candidate set by script; cardinalities or it didn't happen |
| One combined "fix + judgment" deliverable | Mechanical exports ship now; judgment calls (taxonomy changes) get their own PR/round |
| Publishing anything on plan approval | Draft + stage only; VV reviews every outward artifact, every time |
