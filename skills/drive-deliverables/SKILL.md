---
name: drive-deliverables
description: Stage reviewer-facing deliverables to Google Drive through the claude.ai connector - create docs from HTML, version by trash-and-replace, supersede-rename stale assets, work around the no-body-edit and upload-size limits. Use when a reply, report, or export must land in Google Drive/Docs/Sheets - "put this in a google doc", "update the sheet assets", "reply in this doc", "recirculate".
---

# Drive Deliverables

Mechanics for shipping deliverables through the claude.ai Google Drive connector without version churn. Voice/prose rules live in `editorialize`; this skill is the plumbing.

## Hard Connector Limits

1. **No body edits, ever.** `update_file` changes title/folder only. An existing Doc or Sheet's content cannot be touched — every content change means creating a NEW file (new ID, breaks circulated links). So: get ALL formatting and content rules BEFORE the first publish, and batch revisions.
2. **Creation-time formatting works.** `create_file` with `contentMimeType: text/html` converts to a real Google Doc: headings, bold/italic, `<code>`, tables, links, inline CSS. xlsx uploads convert to Sheets the same way.
3. **Large binary uploads are blocked.** The permission classifier denies big base64 payloads (a ~290KB xlsx died this way, in a subagent too). Vanessa drags the file into Drive and sends the URL; then retitle it via `update_file`.
4. **Reading big files:** `read_file_content` results over the token cap land in a tool-results file — `jq -r '.fileContent'` + grep it, don't re-read.

## Versioning Protocol

- Revise: edit the local HTML source (keep it in the workpod thread or scratchpad), `create_file` the new version with the SAME title, `trash_file` the old ID immediately. One live version, always.
- Stale-but-referenced assets (reviewer comments live on them): never trash — retitle with `(superseded YYYY-MM-DD)`.
- Not ready to circulate: retitle with `(HOLD - <reason>)`.
- New files land unshared in My Drive root — do NOT pass `parentId` of a shared folder, or reviewers see the draft before Vanessa does. She moves/pastes after review.
- Verify what circulates: after any upload or paste, read the Drive copy back and grep for the load-bearing content.

## Reviewer-Doc Content Rules (learned by churn)

- Interview format for Q&A replies: questions verbatim in `<b><i>`, answers plain; `<p>&nbsp;</p>` spacer between blocks.
- Answers are agentless — no I/you statements (see editorialize banned-tells "Dangling conversational pronouns").
- Taxonomy value names double-quoted; keywords in `<code>` (editorial-sense ruling 2026-08-20).
- Before publishing, sweep for stale forward references ("will be regenerated", "still owed") — if a promised artifact now exists, link it; tense must match reality everywhere in the doc, not just the paragraph you edited.
