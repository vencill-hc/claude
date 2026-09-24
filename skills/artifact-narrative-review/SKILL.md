---
name: artifact-narrative-review
description: Critical review of a data-narrative artifact against three axes, narrative cohesion, data-visualization craft, and voice/style. Answers "does this artifact tell a cohesive story a cold reader can act on". Use when the user says "review this artifact", "does this artifact tell a cohesive narrative", "is the story clear", "narrative review", "check the artifact reads well", "is this discoverable", "audit this artifact for clarity", or shares an artifact link asking for feedback on the story or visuals rather than the code. Do NOT use for building the artifact (that is artifact-design + dataviz), do NOT use for a bare correctness check of the underlying numbers, do NOT use for prose the user is signing outside an artifact (editorialize governs those).
---

# Artifact Narrative Review

Reviewing a data-narrative artifact for whether a cold reader can (1) understand the problem, (2) read the data and visuals unaided, and (3) leave with a defensible grasp of the decision-making space. Meticulous, honest, verdict-first.

## What this skill produces

A structured written review, in this order:

1. **Verdict** (2-3 sentences, honest). The single call: is the artifact carrying the argument the source material makes, or under-arguing.
2. **Narrative gaps**: what is in the source material (reply draft, plan, notes, ticket, underlying data) but not in the artifact, ordered by how much each gap changes a reader's grasp.
3. **Narrative shape**: read-order, callout placement, subtitle work.
4. **Data viz**: legibility, encoding overload, palette collisions, scale choices, discoverability.
5. **Voice and style**: per editorialize and pr-body.
6. **Legibility and polish**: hover, tooltip, legend, chip discoverability.
7. **What works**: keep-doing list, brief.
8. **Concrete edits, ranked**: actionable, cheapest-highest-impact first.

## The passes

Run them in this order. Each pass is a separate read; do not shortcut by combining.

### 0. Load context

Load in parallel (a single tool-use message with multiple calls):

- Read the artifact via the Artifact tool (`action: "read"`) AND Read the saved local file end to end. The head returned by `read` is not enough; the local path is in the read result. These two calls can run in one message.
- In the same message: Read the source material the artifact should convey. If the artifact is backed by a workpod thread, that is `plan.md`, `notes.md`, and any `*-reply-draft-*.md`. Also read the ticket text and the underlying CSVs or run outputs the charts were built from. Spot-check one figure from the artifact against source data. For every worked example, trace its caption's mechanism to the example's own records: the DAT-68 explainer stated that case B's cut industries came from records with no headcount, and the records showed a 10-person page with a headcount carrying them.
- Invoke `editorialize` and `pr-body` skills; invoke `dataviz` if the artifact has any chart, graph, plot, dashboard, or visualization. Skills invoked in parallel with the reads.

If the artifact is not backed by a workpod thread, ask the user for the source material before running the passes. Guessing what the artifact should say produces a bland review.

### 1. Verdict pass

Write the honest bottom line first, before any list. If the artifact under-argues, say so; if it over-argues past the data, say so. If it lands, say that too. This paragraph anchors every finding below.

The verdict answers: does a reviewer who has never seen the ticket close the tab with the same conviction the source material builds?

### 2. Narrative gaps

Cross-check the artifact against the source material. Common gaps:

- **The verdict, up front.** The source's opening sentence often names the call ("V1 empties the list, V3 does well on real companies"). The artifact's lede often does not, and reads as service copy ("Compare the variants, see where labels went"). The lede is the biggest single lever on cohesion.
- **The punchline table or number.** The single figure a reader cites in the meeting. Often present in the reply as its second table and buried behind a filter chip in the artifact.
- **Design counterfactuals.** "What if we ranked X ahead of Y" changes that the source raises for the team to decide. Not-in-artifact means the decision surface is invisible to the reader.
- **Named examples that anchor abstract findings.** Reply names EY, Deloitte, BCG, VA on ties; artifact shows one demo. The concrete names carry more than the number.
- **Cross-cutting findings.** Small counts that surface real-world patterns (mapping-dictionary gaps, single-source anomalies). Skipping them is usually fine, but check before cutting.
- **The decision surface, as a place.** If the artifact tells the reader what the numbers say but not what the team should discuss next, the reader has to build that themselves. A "For next week" or "Discussion" section often earns its place.

For each gap, name the source (reply draft line, notes item, ticket paragraph) so the author can trace and decide.

Two more gap checks, from the Compound Title Walk (2026-09-24):

- **Every example earns one concept.** A picker of example records is a lesson plan, not a sample. Each example should show exactly one mechanism, carry a one-line "what this shows" caption, and be run through the real system before the caption is written. Two of ten candidates contradicted the page's own copy: HVAC Engineer was claimed as a band effect but landed by a ruled compound key, and the pair-ruling showcase was the weakest ruling in the table. Duplicates of another example's concept get cut.
- **A step that won't draw cleanly is a design finding.** When a pipeline step can only be shown as a note ("a human ruled on this exact pair"), ask where it comes from before polishing it. The walk's pair-ruling step turned out to be a per-pair override table, and drawing it led to folding it into co-occurrence compound keys. Surface this to the author as a design question, not a layout fix.

### 3. Narrative shape

- **Tab or section order.** Does the read-order match the argument-order? A teaching tab ("How each rule picks") sitting before the reader has seen the fallout is a common miss. Overview, data views, teaching, drill-in is the usual arc; discussion or "for next week" at the far right.
- **Callout placement.** A callout doing the argumentative work is often below the table it should introduce. Move above.
- **Subtitle work.** A subtitle that describes the chart ("companies by number of labels") is not doing the same job as one that lands the finding ("53% rode a tiny record, 5% both vendors declared and still dropped, the cheapest proxy for probably-correct-and-gone"). Prefer the finding-landing subtitle.
- **Show, don't tell.** If the finding or the decision lives in a caption or note under a visual, the visual is decoration. Test: cover every paragraph and caption; can the reader still see the finding and the choice? The DAT-68 no-voter explainer (2026-09-24, v1) failed it: the two-voter rule's "575 change, none emptied" sat in a footnote under the table, and each case's point sat in a caption. A first fix (a shared-scale bar per rule option, per-record squares) looked worse to her; the one that held was the switchboard's ribbon diagram with the excluded records drawn on it, captions cut to what the figure cannot show.
- **Header level and grouping.** h2 for panels, h3 for cards inside. Group related panels visually; don't stack five equal-weight panels in one column when three would collapse.

### 4. Data viz pass

Load the `dataviz` skill before this pass whenever the artifact carries a chart, meter, dashboard element, or SVG visualization. That skill owns the palette formula, mark specs, and interaction rules; this pass calls out where they are violated. Ask, per chart:

- **What is it encoding?** One chart, one job. If a chart is encoding magnitude AND category composition AND a boolean subset AND per-variant identity all at once, break it up. The DAT-70 removals chart originally encoded four things at once (bar length as total, segment color as record shape, hatch pattern as corroboration, row color chip as variant) and reused the SAME 4-color palette for two different dimensions. Split concepts across separate visuals.
- **Palette collision.** If two dimensions (variant, shape, cohort, region) use the same categorical palette, readers cannot tell what a color means without a legend for every element. Kill one palette or move one dimension to text or position.
- **Crunched axes.** Small multiples with narrow bins produce collision at bin labels like "6–10" and "11–20". Options: bump `minmax` on the grid so fewer per row, rotate x-labels 35 degrees, increase viewBox, bump SVG font-size.
- **Shared vs per-chart scale.** Shared scale is the right call when a magnitude difference is the story (V1 collapse). Wrong when it flattens the sub-distributions the reader needs to compare. Add a toggle if both matter.
- **Redundant encoding.** Bar length and numeric label on the right, both showing the same magnitude, is fine; one reads at a glance, the other reads precise. Not redundant is length plus color plus hatch plus chip for the same data point; that is overload.
- **Discoverability of interaction.** If a chart segment or table row is clickable, the affordance must be visible. A tooltip that says "click to drill" or a hover cursor change beats silent interactivity.
- **Anchor labels.** Micro-axis labels ("companies", "labels per company") beat a subtitle sentence that describes them.
- **Small multiples first, dashboards second.** Comparing shapes across a categorical dimension (variants, cohorts, regions) reads faster as small multiples on a shared scale than as one grouped-bar chart.

Comparison artifacts (two systems, before and after, main and branch) add their own checks. Seed: the Compound Title Walk, 2026-09-24; its iterations are in references/worked-example-compound-title-walk.md.

- **Same grammar on both sides.** Each side of a comparison uses the same figure type, the same table shape and the same step names, so the eye reads only the difference. A ladder, a sort-key table and an elimination list were each rejected for the prototype's ranking before it reused main's strip figure re-sorted into the prototype's bands. Shared stages render once as a trunk, and the two methods branch off it.
- **Aligned markers.** Steps both sides share (rank, output) sit level across the columns; pad the shorter side rather than let the eye hunt.
- **One meaning per encoding, page-wide.** If dashed means "never considered" on one side, the other side's losers are solid grey. Red × plus red "never reached" in the table marks what a first-match system skips; the collect-all side has no ×, and its caption says so.
- **Two category systems, two palettes.** Main's bands and the prototype's bands sit on one page, so each set gets its own palette, and neither reuses the semantic win/lose colors. Rainbow order and soft colored-pencil pastels were her call for the band strip.
- **Proportional with a floor.** Segment heights follow counts, but anything clickable gets at least 10% of the bar; the true count stays in the label. The same holds for flow diagrams (DAT-68 no-voter explainer, 2026-09-24): no node on either end drops below 5% of the plot height, the rest share what is left on one scale, each ribbon ends at its record's share of the floored node so the node still fills, and the legend says the smallest bars are drawn larger than scale. She asked for the floor on the ending bars first and the sources second; apply it to both ends at once.
- **Labels away from connectors.** Put band labels on the side of the bar the arrows don't cross; figure headers go top-left, not centered over the mark.
- **Containment reads as a substring grid.** For longest-match or overlap logic, one row of letter cells per candidate, only the literal's letters filled, shortest candidate on top and longest on the bottom, long titles condensed with "…" cells.
- **Let the reader inspect the population.** Any band, bucket or segment a figure summarizes should open a popup listing every member with its position: hover text says "Click to see all …", the popup header takes the segment's color, the current selection's members are highlighted and scrolled to, and page scroll locks while it is open.
- **Secondary views behind a button.** A cross-system view (the band-to-band ribbon) belongs in a popup opened from a button placed between the columns, not as another inline section competing with the walk.
- **Margin notes sit outside the figure's card**, level with the figure they explain. "Footnote" in her sketches means a separate panel beside the column, not a column inside the card.

Explainer figures that walk a rule through examples add these. Seed: the DAT-68 no-voter explainer, 2026-09-24; its iterations are in references/worked-example-dat68-no-voter-explainer.md.

- **Reuse the house figure before drawing a new one.** Check the thread's and the project's earlier artifacts for a figure that already draws this mechanism. The explainer went through a card flow, per-record squares and a bar diagram before she pointed at the switchboard's records-to-industries ribbons, which already had the visual language and explained the concept. The Compound Title Walk hit the same thing with main's strip figure. Port the sibling's tokens and renderer, then reduce it.
- **Excluded inputs stay on the figure.** A record the rule ignores (no headcount, no weight) is drawn by name, greyed, with dashed weightless lines to what it declares; an outcome that only it causes is drawn too (a dashed "dropped" bar), not listed as text under the column. A text list headed with internal shorthand ("in production, never voted") read as nonsense to her.
- **Color the marks by the outcome the page argues.** When the point is kept versus cut, the ribbons take the kept and cut colors, not the source colors the sibling figure used.
- **Name the cases.** Examples get letters (A, B, C) in their headings so the summary chart, the Punnett square and the totals can point back at them. Dropping the letters in a rewrite broke every later cross-reference.
- **A rule over two yes/no conditions is a 2×2 grid.** "Which records vote" (headcount × mapped industry) read at a glance as a Punnett square; three cards in a row did not.

### 5. Voice and style pass

Follow `editorialize` and `pr-body` as loaded. Common tells inside artifacts:

- **Verb-first fragment leads** ("What each variant does to..."). Banned. Openings need explicit subjects.
- **Service-copy imperatives** ("Compare the variants, see where labels went, and open any company"). Not the author's register. Replace with the verdict.
- **Comma-in-title headings** ("Five Rules Side by Side"). August 2026 ruling: Title Case, no punctuation. "The Five Rules" or "Rule Comparison" or "The Five Rules on This Cohort".
- **Em-dashes anywhere in rendered text.** Voice rule is never. Legend separators ("Tiny record — carried by...") count; swap to colon. Watch for them in callouts, subtitles, and even legend text.
- **Chart-title syntax on section headers** ("How Many Labels a Company Ends With", "Where the Removed Labels Came From"). The author's style is terser and more nouny: "Labels per Company", "What Rode the Removed Labels", "Where the Cuts Land".
- **Number repetition between prose and table.** A concept card that says "863 of 1,500 companies" while the table already shows that row is the classic pr-body violation.
- **Beige positive descriptors** in subtitles ("provides valuable insights into...", "helps you explore"). Cut.
- **"Side by Side", "at a glance", "one-stop", "dashboard-style"** in a title or lede. All chart-vendor language.
- **Private-notebook references.** Source notes like "from this ticket’s working notes" point a shared artifact at the workpod. Name the method, not the notebook (see the workpod-never-cited-outward memory).
- **Two vocabularies for one concept.** If both systems group keys into bands, both say "band"; keep the value names (Band 3, ROLE) as the distinguishing layer.

### 6. Legibility and polish

- Hover tips consistent. A tooltip that names one thing should not silently rename it on hover.
- Legend entries match the terminology used in the chart, the sub, and the callouts. If the header says "Both vendors agreed" and the tooltip says "vendor-corroborated", pick one.
- Filter chips and cohort toggles need discoverable states. The current selection reads at a glance.
- Named entities carry themselves. A chip labeled "known limit" should tooltip its meaning, not require reading a callout in another panel.
- Text scales at phone width without horizontal scroll.
- Dark mode: colors validated per the design system; contrasts hold.

## Sources of gap

When looking for narrative gaps, expect the source material to live in one of:

- The **workpod thread** for the artifact: `~/Documents/git/workpod/projects/{project}/threads/{thread}/`. Read `plan.md` (approach, decisions log), `notes.md` (readings, findings, tool outputs), the reply draft `*-reply-draft-*.md` if one exists.
- The **ticket text** as it was quoted into the plan or reply.
- The **run output**: CSV, JSON, or txt summary the artifact was built from. Spot-check one number.
- **Prior sibling artifacts.** A DAT-70 artifact is often the second in a family (DAT-68 came first); the earlier artifact's shape informs what this one omits or repeats.

## Output shape

Deliver as a chat response. Structure:

```
## Verdict
[2-3 sentences, honest]

## What the source carries that the artifact does not
[bullet each with source citation]

## Narrative shape
[read-order, callouts, subtitles]

## Data viz
[chart-by-chart or theme-by-theme]

## Voice pass (editorialize + pr-body)
[tells found, banned patterns triggered]

## Small legibility items
[hover, legends, filters, chips]

## What works and should stay
[keep list, brief]

## Concrete edits, ranked
[cheapest-highest-impact first]
```

Do not publish the review as its own artifact unless asked; the review is chat.

## When to run it

Run it once after the first complete version, not only at the end. In the Compound Title Walk the narrative problems (examples that didn't illustrate, a leaked notebook reference, a step that exposed an ad hoc mechanism) surfaced one at a time over ~20 revisions; one early pass would have batched them.

## When NOT to use

- **Building or editing the artifact.** That is artifact-design + dataviz + the skill for the domain. This skill only reviews.
- **Correctness check on the underlying numbers.** Use the domain skill (crunchbase-analyzer, mixrank-analyzer, universe-expert, or the specific measurement harness).
- **A design-first pass before the artifact exists.** Use superpowers:brainstorming.
- **Prose the user is signing outside an artifact** (a Slack post, an email, a PR body). Use editorialize or pr-body directly.
- **Code review inside the artifact source.** Use pr-code-review (correctness) or ponytail-review (over-engineering).

## Growth loop

Append to this skill when a review turns up a pattern worth encoding:

- New voice tell: append to editorialize's `banned-tells.md` (not here).
- New data-viz anti-pattern with a fix that generalizes: append a bullet under **Data viz pass**.
- New narrative-gap category that recurs across artifacts: append a bullet under **Narrative gaps**.
- Worked example (a whole review that made the artifact meaningfully better): save as `references/worked-example-{artifact-name}.md` and cite it in the intro.

Small surgical appends, never rewrites. The DAT-70 layer-weighting explorer review (2026-09-18 to 2026-09-21, versions 1 through 8) is the seed worked example; save it under `references/` when the next artifact review earns comparison.
