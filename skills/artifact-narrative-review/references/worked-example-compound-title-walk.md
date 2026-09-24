# Worked Example: Compound Title Walk (2026-09-24)

An interactive explainer for SUP-626/627: how a job title becomes one job-function label on `main` (first match in dictionary order) versus the prototype resolver (collect every match, dedup, rank by band). About 30 published versions in one session, most driven by her corrections. The corrections are the lesson; each one below generalizes.

Sources lived in the thread's `title-walk/` folder: `trace_main.py` and `trace_feature.py` run the real parsers and emit JSON, `build_page.py` injects it into `page.tpl.html`.

## What she corrected, in order

1. **Start where the code is real.** The feature branch was WIP, so the first version drew only `main`. The prototype column started as prose and was rebuilt from real resolver traces as soon as she asked for "show don't tell". Never draw a mechanism from its description when it can be run.
2. **Shared stages render once.** Normalization is common to both; it became a single trunk card with a fork into the two method columns.
3. **Her sketch was the spec.** A notebook photo showed the dictionary as a vertical strip with keyword pills pointing into it. That became the core figure for both sides. A second sketch showed "footnote" meaning a panel outside the column, beside it, not a column inside the card.
4. **Real keys, not placeholders.** The `"key": "value"` filler beside the strip became real dictionary keys, then per-band samples in the margin note.
5. **Explain the bands.** The bands carried meaning nobody had written down (Band 1 is specificity guards placed first only because first match forces it; Band 5 records when keys were added). The margin note gave each band: key count, definition, examples, in that order.
6. **Color.** Graded blue-grey bands read as one thing; she asked for distinct hues, then rainbow order, then soft colored-pencil pastels. The prototype's bands took a second pastel set so no band reads as its counterpart.
7. **Mirror, don't invent.** Three ranking visuals were rejected (a tier ladder, a sort-key table with the deciding column shaded, an elimination list) before "shouldn't it just look like the chart on the main side?". The prototype strip is the same figure re-sorted into its bands; the table under it has main's shape.
8. **Substring grid for dedup.** Overlap removal became a character-cell grid after a reference image: literal letters only (`account` fills seven cells of "accountant"), shortest on top, long titles condensed with "…".
9. **Align what both sides share.** Main got a "rank" step marker where the prototype has one, and spacers keep rank and output circles level across columns.
10. **Encode what main never considers.** Red × where main's dashed lines meet unreached pills, red "never reached" in its table; the prototype's losing lines went solid grey so dashed means only one thing.
11. **Curate the examples.** Every non-ticket example was re-run through both parsers and kept only if it showed one concept, each with a "what this shows" caption. Two surprises changed the copy (HVAC Engineer is a ruled compound key, not a band effect) and the design (the pair-ruling showcase was the weakest ruling).
12. **The drawing exposed an ad hoc mechanism.** "Where does this come from? Feels adhoc" about the pair-ruling step led to measuring it (93% of its reach was adjacent compound-key territory) and folding all 15 pairs into co-occurrence compound keys, 78/78 rulings still reproduced.
13. **Inspectable populations.** Hover "click to see all keywords" on every band (strip and margin note), popup listing every key with its position, header tinted to the band, current title's keys highlighted and scrolled to, page scroll locked.
14. **Secondary view behind a button.** The band-to-band ribbon ("how the same keys regroup") lives in a popup opened from a "Compare keywords" button between the columns, not as another section.
15. **Clickable floor.** Proportional band heights with a 10% minimum for any clickable band; the true count stays in the label. Bars doubled in width for the same reason.
16. **Polish passes last.** Editorialize caught five "X, not Y" reframes, comma headings, and a leaked "this ticket's working notes" reference. Typography raised body to 16px, dropped Arial from the fallback, capped the caption measure at 40em, and set filename badges in real lowercase.

## Process lessons

- A narrative review after the first full version would have batched items 5, 11, 12 and the notebook leak instead of discovering them one turn at a time.
- The page was assembled by regex-splicing JS blocks into a template; two splices clobbered each other's code and one overwrote the wrong caption. See the kungfu backlog for the fix.
