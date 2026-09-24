# Worked example: DAT-68 no-voter explainer (2026-09-24, versions 1–9)

A one-page artifact backing a PR note: under the headcount vote, organizations whose records lack a headcount lose industries. Page: "Organizations the Vote Empties". Sibling it should have borrowed from on day one: the Industry Vote Switchboard (DAT-68, 2026-09-21).

## Iterations and what each taught

| Version | Change | Her call | Lesson |
|---|---|---|---|
| 1 | Record cards, two before/after chip panels, a counts table, a closing question | Ran artifact-narrative-review: lede never stated the finding; the decision hid in a footnote | Lede carries the number people will cite |
| 2 | Rule-comparison bars on one scale, per-record squares, prose cut | “Feels worse visually”; letters A/B dropped so nothing could refer back | A show-don't-tell rewrite can over-rotate; keep the anchors |
| 3 | Punnett square; cases A–C restored; bar diagram per case | Pointed at the switchboard’s ribbons instead | Reuse the house figure before inventing one |
| 3 (data) | Building the diagram exposed a false caption: case B’s cut industries came from a 10-person page **with** a headcount | — | Trace every example’s mechanism to its records before captioning |
| 4 | Switchboard ribbons ported; kept/cut ribbons green/red | Asked for the outcome colors on the ribbons | Color marks by the outcome the page argues |
| 5–6 | 5% floor on ending bars, then on source bars | Asked for each end separately | Apply the floor to both ends at once |
| 7 | Tossed records drawn by name, greyed, dashed weightless lines; dropped industries as dashed bars; choice section cut (the page backs a PR note, it is not a decision memo); totals re-cut by reason A/B/C | “in production, never voted” made no sense | Excluded inputs stay on the figure; no internal shorthand as labels |
| 8 | editorialize pass | — | Fragments without subjects, a hanging “the cut decides”, a “not X” reframe |
| 9 | typography pass | — | 12px chart-text floor, no mono outside numbers and ids, caps letterspacing 7–8% |

## Numbers behind the figures

Every example and count came from the prod export of the labeling source’s own inputs run through the real vote code locally (DAT-68 thread: `vote_gated_orgs.py`, `removal_reasons.py`), plus one named-records query for the three examples. No count on the page is inferred.
