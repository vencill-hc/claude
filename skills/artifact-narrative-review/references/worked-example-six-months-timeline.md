# Worked Example: Six Months of GDU Labels (2026-09-29)

A consumer-facing retrospective of every labeling change from March to September: a centre-spine timeline, one card per change, each with one figure, a Before/Today toggle driven by scroll, and an optional companion panel on the opposite side of the spine. About 25 published versions in one session. The figures are the lesson; each correction below generalizes.

Sources: the PR bodies (read firsthand, not from agent summaries), the pre-PR mapping tables, and real parser output run at two revisions through temporary git worktrees. `measurement-tools/job_function_volume/classify_titles_at_rev.py` already does rev-pinned title classification with a self-check; use it instead of a hand-rolled labeler.

## What she corrected, figure by figure

1. **Her sketch was the layout.** A notebook photo of a spine with alternating cards, fade-in and fade-out on scroll, became the page. The companion-panel idea ("pop up a new frame on the opposite side of the timeline") came from her too and fixed every "too much for one card" problem after it.
2. **Show why, with real records.** A value-to-value mapping (Engineering → Software engineering) "looks like deck chair shuffling". Every split now carries its most-held real titles; the new-industries card shows real companies sitting in the old buckets.
3. **A split of one list into another is one fan at a time.** A Sankey of the ten biggest moves "is not doing us any good"; a 40-slice sunburst was "too hard to read"; twelve stacked split bars were "a lot going on". What held: her sketch's single bar fanning out to its new values, one old value at a time, picked by chip and auto-rotating on a timer, with the titles in a synced detail carousel beside it. A sunburst did work where there were eight slices and a two-level question (stays CxO or moves down, then where to).
4. **Removals show the whole population.** Seven fading edges "don't show the breadth". What held: one square per removed rule (62, 272, 66 added with a +), shaded by reach, reasons on hover; a carousel beside it samples one rule every 3 s and outlines its square.
5. **A pie or square-waffle for "where did N go" confused her.** One bar splitting apart, with an example title per segment, read; the breakdown later moved into a sunburst in a panel that slides out when the card turns to Today.
6. **The overlap strip is for overlap only.** Porting the Compound Title Walk's character strip was right for "pr" swallowing "principal" and "general counsel" swallowing "counselor"; using it on titles where one key simply matched was "totally inappropriate". Rows without overlap render as plain titles with the deciding key underlined. Match the house figure's CSS exactly (square collapsed cells, teal win), and namespace its classes: a board matrix `.cell` rule leaked rounded corners into it.
7. **A two-axis ontology is a matrix, colored by the second axis.** Board roles as a bipartite graph "doesn't show the relationship that changed"; a seat × how-held matrix with real parser output did, once each engagement column got its own color for contrast. Before/Today animated each title from its old flat bin to its cell (FLIP).
8. **Why a new label was needed is a Venn.** Three overlapping old buckets with each group sitting where its vendor tags put it (device makers in the triple overlap, vets beside hospitals, robots beside Samsung), then each group moving into its own new circle. Category names inside the circles got covered by the chips; they moved outside the circles.
9. **Color encodes the argument, not identity.** Unique per-branch colors with gradients on the fan were reverted within one turn; the moved / kept-its-name / no-function coding stayed.
10. **Carousels are feature frames.** A titled panel with prose was "useless"; the keeper was a bare frame, change up front (category, big arrow, label), centered against the card it serves, cross-highlighting the matching mark in that card.
11. **Before/Today on every figure, from real output.** Including the punctuation panel, where running the pre-PR code showed the title examples had not changed at all; the real change was in company-name cleanup, and the examples were swapped.
12. **Scroll-driven state needs smoothing.** A flip at the midpoint jittered: add hysteresis (to Today at 70% of the viewport, back only below 85%), lock each figure's height to the taller state, crossfade re-rendered figures, and let a click pin the reader's choice. Start the flip earlier than feels natural.
13. **Cut the scaffolding.** The review pass later removed the "What's Still Open" section, the timeline heading and its how-to paragraph, the per-toggle scroll hint, and two of six splash tiles; the lede was trimmed to its first sentence.

## Build hygiene that bit

- One figure throwing (a missing embedded JSON block) blanked every figure after it; draw each figure inside its own try/catch.
- `--c: var(--c)` is a cycle and renders nothing; set the color on the element instead.
- Headless Chrome with `--virtual-time-budget` does not advance CSS transitions, so a state switch screenshots as the old state; disable transitions in the preview copy. The scroll-fade also dims off-screen cards in a tall screenshot; override it in the preview too.
- Exact-count string replacement scripts (fail unless the match count is 1) caught every stale anchor; a substring of an indented line matching its more-indented twin was the one miss.
