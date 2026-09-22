# Page layout

Rules for the page or container. Full control in print and HTML; partial on slides; none in markdown beyond list structure. Source: Butterick, *Practical Typography*, “Page Layout” chapter plus the two spine pages, “Typography in Ten Minutes” and “Summary of Key Rules”.

## Body text first

Four decisions, made before anything else, because body text is most of the document: font, point size, line spacing, line length. Print body text is traditionally serif; on screen serif or sans both render well now. (body-text, typography-in-ten-minutes)

| Setting | Value | Notes |
|---|---|---|
| Point size | 10–12 pt print, 15–25 px web | 12 pt is a typewriter default, not a choice |
| Line spacing | 120–145% of point size | Word “Single” is ~117%, “1.5 lines” ~175%, “Double” ~233%; all outside the band. Use “Exactly” with a measurement, or “Multiple” 1.03–1.24. Pages “Lines” adds ~17%, so 1.03–1.29. CSS unitless `line-height: 1.2–1.45`. Fonts that look small at a size take less. |
| Line length | 45–90 characters incl. spaces, or 2–3 lowercase alphabets | Measured in characters, never inches, because point size changes characters per inch. Set with margins, not paragraph indents. Plan the base measure so indented levels still land in range; use fewer, smaller indents. |
| Margins | 1.5–2 in sides at 12 pt on letter paper | One-inch margins leave a 6.5 in line, too long. Margins grow as size shrinks. Character count governs, not the inch figure. |

## Alignment

- Left-align in word processors and browsers. Justify only in professional layout software, only with hyphenation on, and put the extra space between words, never letters. Justified versus left is otherwise personal preference; books justify, magazines mix. (justified-text)
- Center only short phrases: a title, a name on a card or letterhead, a major section heading such as a table of contents. Never a block of body text; both edges go ragged and nothing aligns. Break centered lines by hand. (centered-text)

## Paragraphs

- Mark a paragraph one way: a first-line indent of 1–4× the point size (12–48 pt at 12 pt; toward the low end when the text block is under 3 in wide), *or* 4–10 pt of space after (50–100% of body size), never both. (first-line-indents, space-between-paragraphs)
- Space goes after the paragraph, not before, because word processors take the larger of before and after rather than adding them. Block quotations are the exception that may need space before. Larger type needs more space. (space-between-paragraphs)
- Indents come from the paragraph setting (`text-indent`), never spaces or tabs. The opening paragraph may go unindented. No hanging indents unless a bullet sits in them. Skip the word-processor drop cap. (first-line-indents)
- Never extra returns for space. (space-between-paragraphs)

## Margins

- The four margins need not match. Trim top and bottom to fit more text while the measure holds. Bottom about 0.25 in deeper than top, or the block appears to sag. If the block sits off-center, left and right differ by at least an inch; a small asymmetry reads as a mistake. (page-margins)
- Ratios (golden ratio 1.618:1, which 2.23 in margins all round produce on letter paper) are a starting point; judge with your eyes. (page-margins)
- Web: generous `margin` and `padding` so text never touches the container edge, and a capped container. (page-margins)

## Hyphenation

Always on with justified text. Consider off with left-aligned text, where it adds little, except when the measure is short. Off in headings. Control it in styles (Word Paragraph › Line and Page Breaks › Don’t hyphenate; CSS `hyphens`, spotty). Fix single bad breaks with nonbreaking and soft hyphens. (hyphenation)

## Block quotations

Slightly smaller type, slightly tighter leading, indented 0.5–1 in in print (2–5 em on the web), optionally both sides. Drop the quotation marks; the indent already says quoted. Never for emphasis. Edit and integrate quoted material instead of dumping it; readers skip long blocks. Extensive verbatim quotation for accuracy is the exception. (block-quotations)

## Lists

- Automatic bullets and numbers, never typed. `<ul>` for unordered, `<ol>` for ordered. Turn automatic list *detection* off; it guesses wrong about half the time. (bulleted-and-numbered-lists)
- Bullets just big enough to see, hollow preferred; the bullet may be a different font or smaller size than the item. Never asterisks, which sit too high and too small. Dingbats only as simple geometric shapes, checked for cultural or religious meaning. (bulleted-and-numbered-lists)

## Tables

- Any grid or side-by-side text is a table (or CSS grid); whitespace cannot hold a grid. (tables)
- Turn every border off first (table, row and cell carry separate settings), then restore only what legibility needs. Cell padding opens dense tables: start at 0.03 in, step by 0.01 in; top and bottom may exceed sides. (tables)
- Rules and borders sparingly, and try space above and below first. Borders 0.5–1 pt, single, solid; the half-point rule is the classic. A freestanding rule may run heavier or patterned. A rule above a heading separates sections; below it, it splits the heading from its text. Never a rule built from repeated characters. (rules-and-borders)

## Page control (print)

- Widow and orphan control on only when the breaks actually look bad; the gaps it leaves at page bottoms are often worse. Widows and orphans are controlled together. Fix a stray one by editing. On the web only a lone short word ending a paragraph matters. (widow-and-orphan-control)
- Headings carry keep-lines-together and keep-with-next. Never keep-lines-together on body text by default; it is blunter than widow control and moves whole paragraphs. A signature block is hard line breaks plus keep-lines-together. Multi-element groups pair keep-with-next with keep-lines-together. (keep-lines-together, keep-with-next-paragraph)
- Chapters open a page through page-break-before in the top heading style, not a manual break. Word processors drop space-above at a page top; work around it. (page-break-before)

## Space above and below

A heading is signaled first by space, like a dramatic pause, and less below than above so it binds to its text. When paragraphs already carry space, heading space scales up to outrank it. On screen, do not push a heading below the fold. (space-above-and-below)

## Columns and grids

- Letter paper takes two or three columns, never four. Align rows across columns; paragraph spacing is zero or a whole multiple of line spacing so baselines match. Columns fail on the web, which has no bottom edge, except for a link list that fits one screen. (columns)
- A grid in moderation, coarse and simple, neither rigid nor symmetric; leave it when an element plainly looks right off it. Web: start from a 1rem or 1vw grid. Print: a pica grid (1 pica = 12 pt), coarsened. No baseline grid on books or websites; only in wide multi-column work like newspapers. (grids)

## Styles

Format through paragraph and character styles, never element by element. Name styles for function (“Block Quotation”), not appearance (“Caslon Bold 11.5”). Modify built-ins before creating new ones. Character styles hold font, size, letterspacing, bold, italic, caps, small caps; paragraph styles hold line spacing, indents, rules. CSS inline versus block elements is the analog. (paragraph-and-character-styles)

## The nine maxims

1. Decide the body text first.
2. Split the page into foreground and background and keep the background quiet, using position, size, font and sometimes color.
3. Adjust in the smallest increment you can still see.
4. When unsure, make both versions and look at them.
5. Make things that are the same look the same, and things that look different actually be different.
6. Relate every new element to the ones already on the page.
7. Keep it simple: resist extra colors, fonts and decoration.
8. Imitate typography you admire.
9. Work outward from the text and let the white space fall where it will. (maxims-of-page-layout)

