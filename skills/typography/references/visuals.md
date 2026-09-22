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

## What the book does not cover

Subtitle styling, axis-label placement, annotation placement and density, direct labeling versus a legend, and the ratio of tick-label size to body size. The book never names any chart part. When these matter, extend from a named source (candidates to evaluate first: Dona Wong, *The Wall Street Journal Guide to Information Graphics*; Datawrapper’s typography posts) and mark the extension as not Butterick’s.

## Where the pages disagree

color says printed body text is black, no exceptions; presentations starts projected text at 50% gray; color allows dark gray on screen. All three hold, by medium: paper, projector, screen.
