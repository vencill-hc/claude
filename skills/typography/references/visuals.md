# Chart and table typography

Butterick never discusses charts. This sheet maps the rules he does state onto the parts of a data visualization, and says plainly where the book is silent. Every rule cited is the book’s; the mapping onto a chart part is ours, and a part the rules do not reach is marked as such rather than given an invented rule. For a data-visualization artifact, load this file and then the figure block in css.md. documents.md and layout.md point here rather than restating table rules.

## Body first, then the figure

The four body-text decisions govern the figure’s text too. Screen body 15–25 px, unitless line-height 1.2–1.45, measure 45–90 characters for any caption or note, one or two fonts for the whole artifact with the figure sharing them. Tick labels and source lines may go smaller, but the smallest size the book endorses anywhere is 6–8 pt (business cards), where caps and lowercase read equally well, and below 9 pt lowercase wants a little letterspacing. (point-size, letterspacing)

## By chart part

### Title
- Space above and below carries it, not size. Rise in half-point steps over body, not a 200% jump. Left-aligned; center only a short title and break its lines by hand. Not all caps unless under one line, not underlined, not Title Case. (headings, point-size, centered-text, all-caps)
- A rule, if any, sits above the title to close the previous section, never beneath it. (rules-and-borders)
- Nested titles number as 1, 1.1, 1.1.1; never roman numerals or letters. (hierarchical-headings)

### Subtitle
No rule in the book. Our inference from the heading ladder: one level below the title, distinguished by space and at most a half-point of size, never a third font.

### Axis labels
No rule in the book beyond the general ones: lowercase at designed spacing, caps letterspaced 5–12%, lining figures beside caps.

### Tick labels
- Numbers in columns or along an axis take tabular lining figures so digit positions match (`font-variant-numeric: tabular-nums lining-nums`). Beside capitals, lining; never oldstyle beside caps. Defaults are never wrong when unsure. (alternate-figures, grids-of-numbers)
- Lowercase below 9 pt takes a touch of letterspacing; large headline-size text takes none or a little tightening. (letterspacing)

### Annotations
No rule in the book on placement or count. Emphasis rules still apply: bold or italic, not both; color is not emphasis at text size; never all caps beyond one line.

### Legend
- Our inference from the slide rule that bullets drop when every item fits one line: a legend needs no bullet or dash before each entry; the swatch does the work. (presentations)
- Colored text is the web’s idiom for clickable; our inference is that a legend label reads in body color beside its swatch, not in the series color. (color)

### Caption and source line
- Small caps or caps for a short label, letterspaced 5–12%, kerned. Headers, footers, captions and labels are where all caps belong. Six to eight points is acceptable for this kind of small print. (all-caps, small-caps, point-size)
- A source line is a URL problem: never hyphenate an address; break it by hand at a natural point. (web-and-email-addresses)

### Number tables
- Align digits of the same place value; tabular lining figures; right-align money so cents stack; align measurements on the decimal; leading zero on values below one; thousands separators on every figure in a column even the short ones ($6,736 under $16,736). Never pad with trailing zeros to force alignment; 98.000 asserts precision 98 does not have. (grids-of-numbers)
- Nominal numbers (zip codes, invoice and phone numbers) are labels: zips left-aligned, invoice and phone numbers right-aligned, and no arithmetic on them. Compare only commensurable units. (grids-of-numbers)
- A column header may take formatting inconsistent with its column, set last, to look right. (grids-of-numbers)
- Excel exposes no OpenType features; pick a font whose default figures are already tabular. Numbers does expose them. (alternate-figures)

### Gridlines and rules
- All borders off first; restore only what legibility needs. Aligned text already implies the grid. Cell padding is the first lever for a dense table: start 0.03 in, step 0.01 in; top and bottom may exceed sides. (tables)
- Rules 0.5–1 pt, single, solid; the half-point rule is the default. Never dotted, dashed or doubled borders. Try space before a line. Never a line made of repeated characters. On the web, CSS grid over table markup for layout. (rules-and-borders, tables)

### Colored text and backgrounds
- Color is not emphasis at text size; bold is. Colored type on a colored background almost always reads worse. Build the palette from shades of one hue rather than contrasting hues; adjust light colors in small steps and dark colors in larger ones. Thin or small type carries a more intense color than heavy or large. (color)
- Screen body text may be dark gray rather than black; printed body text is black without exception, so a figure destined for a printed PDF keeps black text. Laser-printed knockout (white on dark) burns about 20× the toner. (color)
- Do not build the layout from big blocks of flat color; that is decoration standing in for structure. (websites)

### Projected figures (slides)
Black background in a dark room, text from 50% gray upward, thin sans, pale accent colors, one size across the deck, layout narrower than the screen, no centering, loosened leading. In a lit room, light gray background and dark text. (presentations)

## Screen resolution

Modern displays out-resolve the eye at reading distance (about 143 dpi needed at 24 in; phones ~326, desktops ~185), so a weak font is exposed rather than hidden, and the print font is the right screen font. Screen-only figures may take tighter margins and larger type; anything that may be printed keeps print geometry. (screen-reading-considerations, the-infinite-pixel-screen)

## Beyond Butterick: the parts the book skips

Subtitle styling, axis labels, annotation placement, legends versus direct labels, and the size ratio between chart text and body text are not in the book. The rules below come from four named sources, each checked 2026-09-22, and are marked as theirs, not Butterick’s. Where they disagree with him, the disagreement is stated, and his rule wins for prose while theirs wins inside the figure.

Sources:
- Lisa Charlotte Muth, Datawrapper, “What to consider when using text in data visualizations” (https://www.datawrapper.de/blog/text-in-data-visualizations) and “Which fonts to use for your charts and tables” (https://www.datawrapper.de/blog/fonts-for-data-visualization).
- Urban Institute, Data Visualization Style Guide (https://urbaninstitute.github.io/graphics-styleguide/).
- UK Government Analysis Function, “Accessible charts: a checklist of the basics” (https://analysisfunction.civilservice.gov.uk/policy-store/charts-a-checklist/).
- Office for National Statistics, Service Manual, “Chart elements” (https://service-manual.ons.gov.uk/data-visualisation/build-specifications/chart-elements).

### Hierarchy and size ratios

- Two levels of text hierarchy, clearly different; the biggest, boldest, highest-contrast text carries the one thing the reader must take away, and everything secondary is small, thin and gray. (Muth)
- Nothing on a chart below 12 px; Datawrapper’s default body is 14 px. (Muth)
- Urban’s web sizes, as a ratio ladder you can scale from any body size: title 20 px black weight, subtitle 16 px italic, legend 14 px, axis titles, axis labels and data labels 12 px, source and notes 11 px. In print: title 12 pt, subtitle 10 pt, legend 9.5 pt, axis and data labels 8.5 pt, source and notes 8 pt. So labels sit at roughly 0.6 of the title and 0.85 of the legend, and sources a shade under the labels. (Urban Institute)
- Bold only for the title and for a few emphasized words inside an annotation; body, labels and legend in regular or medium. Thin weights only at large sizes in high contrast. (Muth)

### Subtitle

- One step below the title in size and weight (Urban: 16 px italic under a 20 px title). It carries the precise version of the claim the title makes colloquially: units, population, period. (Muth, Urban Institute)
- Sentence case. Urban sets titles in Title Case and figure numbers in all caps; Butterick and Muth both reject Title Case, and this skill follows them. (Muth, Urban Institute; conflict noted)

### Axis labels and tick labels

- Horizontal, never rotated. If they do not fit, shorten them, thin them, or move them somewhere else inside the chart. (Muth, Government Analysis Function)
- Repeat the unit in the axis label, tooltips and annotations, not only in the description. Abbreviate large numbers as 20k, 20m, 20b rather than a multiplier note. Cut false precision: 27%, not 22.42%. (Muth)
- Right-align y-axis values so digits line up; continuous data centered on tick marks, categories between them. Thousands separated by commas. (Government Analysis Function)
- Lining, tabular figures, as Butterick also requires. (Muth)
- Uppercase category or axis labels are tolerated when spaced out, made a little smaller, and a little bolder; letterspacing from 0.08em. (Muth; consistent with Butterick’s 5–12%)

### Direct labels over legends

- Label series directly on the chart, on the line or at its end, and omit the legend when you can. A legend makes the reader match colors, which fails WCAG success criterion 1.4.1 Use of Colour when color is the only cue; the Government Analysis Function marks this Essential for bar and line charts. (Government Analysis Function, Urban Institute, Muth)
- When a legend is unavoidable, place it above the chart, aligned left, entries running horizontally and wrapping; order and orient it the same way as the data. (ONS, Government Analysis Function)
- Line labels in black or dark gray. Colored label text only when its contrast against the background passes. (Government Analysis Function)

### Annotations

- Annotations explain design choices, point at outliers, and supply context. Put each one as close to the element it explains as possible. (Muth)
- Left-align anything longer than a few words; centered and right-aligned blocks read worse. (Muth; matches Butterick on centered text)
- When text crosses a mark, give it a thin outline in the background color rather than a box. (Muth)
- Reference lines 2 px dashed in a mid gray; annotation arrows 1 px, curved, open head, dark gray; highlighted ranges in the lightest gray. (ONS)

### Gridlines

- At most ten light gray gridlines, behind everything else. Zero line a little heavier than the rest (ONS: 1.5 px versus 1 px). (Government Analysis Function, ONS)
- With direct data labels, drop the y-axis labels and gridlines entirely. (Urban Institute)

### Font family

- Sans serif for chart text: it skims faster and reads better for dyslexic readers. Normal width, never condensed or extended. Muth names Roboto, Lato, Open Sans, Source Sans Pro and Noto Sans as free options; Urban uses Lato. This is the one place this skill departs from Butterick’s serif-or-sans neutrality: the figure takes a sans even when the document body is a serif, which also satisfies his two-fonts-one-job rule. (Muth, Government Analysis Function, Urban Institute)
- Check the font has the glyphs the data needs: currency signs, minus, multiplication, the language’s accents. (Muth)

### Titles and accessibility

- Every chart gets a title that says what, where and when, and ideally a headline that states the finding. The title lives in the page text with proper heading markup, not baked into the image, and every chart carries a text alternative that opens with the chart type. (Government Analysis Function)

## Where the pages disagree

color says printed body text is black, no exceptions; presentations starts projected text at 50% gray; color allows dark gray on screen. All three hold, by medium: paper, projector, screen.

Across sources: Urban sets chart titles in Title Case; Butterick and Muth reject it; this skill uses sentence case. Butterick is neutral between serif and sans on screen; the three chart sources all say sans for figures; this skill sets figure text in a sans. Butterick tolerates a legend’s bullets going; the chart sources go further and drop the legend itself when labels can sit on the data.
