---
name: pr-body
description: "Use when drafting or revising a pull request description: 'write the PR body', 'draft the PR description', a finished branch needs its PR opened, or a body already live on GitHub needs editing. Not for review comments, commit messages, or general prose (editorialize governs those)."
---

# PR body

The body carries the review: what changed, why, and what moved. Reviewers read it once, next to the diff; everything else lives in the commits, CI, and the workpod thread. This skill owns the form. The sentences inside it still go through editorialize (tell scan, then a light voice glaze), and the register is the abstract end of that skill's dial: voice lives in verb choice and at most one dry aside.

A body she has already touched on GitHub is edited surgically from the live text (`gh pr view --json body`), never regenerated.

## The skeleton, in order

1. Opening paragraph: what this PR is and why now (what it's staged ahead of, what it unblocks). This is narrative's only slot in the body. One word of orientation for readers outside the project beats a sentence of it.
2. Root causes, numbered, when there is more than one. Example sets stack as bullets under their cause, never serial parentheticals.
3. The change table: the inventory, one field per row. When the delta is measured, an impact column (rows moved, latency, cost) on every row.
4. The total, with its decomposition as bullets.
5. Movements worth calling out by name: consequences a reviewer would want flagged, each carrying a fact the table does not (the largest single flip, a precedence the table already claimed).
6. Footer: ticket ids (`SUP-420/SUP-539`), then provenance lines. Ticket ids are citations, never the headline.

Sections that don't apply to a given PR are skipped, not padded; a feature PR may have no root causes and no measured delta, and its skeleton collapses to opening, table, footer.

Numbers appear once. Summing or decomposing the table is not repetition; re-narrating the same figures in different phrasing is, and a re-presentation that is vaguely or subtly different from the first makes the body harder to read, not more persuasive.

## What gets cut

The test for process content: does it scope what the reviewer reviews, or assure them the work was done diligently? Scoping stays ("re-lands #123 on main; the dedup commits stay with #99"). Assurance goes: measurement methodology, commit hygiene, test discipline, "nothing here touches the schemas". Methodology earns a place only when it is itself the code under review.

Also cut:

- Hedging. Genuine uncertainty about code performance is called out directly, or fixed before the review phase. A precision caveat that changes no decision compresses to notation: "~10.26%", not a parenthetical sentence about double-counting.
- Parentheticals not important enough to be a main-text sentence. A short "e.g." aside is fine; examples that break the flow of the prose become bullets, charts, or supporting figures.
- Interpretation paragraphs that re-narrate the table. If a paragraph adds no fact the table lacks, it goes.
- Generic coinage verbs on results. "Reads" meaning "is labeled" is always wrong; results get plain verbs. Coinage close to literal survives ("`pr` reads principal, propietario, profesor", describing a matcher).

## Provenance

In-body numbers ride on the thread and the measurement tooling the reviewer can reach; they do not need a methodology sentence. This is the PR carve-out from editorialize's standalone test, which governs documents an audience reads cold. The line that cannot be crossed: a number in the table is a measurement. If it is a guess or a draft, it does not go in the table.

## Footer conventions

The 🤖 generated-with line and the 🦋 revised-by line are provenance markers, exempt from the no-emoji rule; hygiene never overrides disclosure. Keeping the 🤖 line is the author's call, made explicitly.

## References

- references/sup-420.md: the calibration pair. A real draft, her edit of it, and the rulings extracted from the diff. When a judgment here feels ambiguous, this file is the tiebreak.
- references/worked-example.md: a fictionalized body through the editorialize passes; shows the pass-effort distribution typical of house-structured artifacts (humanize near zero, editorial heavy, voice two phrases).
