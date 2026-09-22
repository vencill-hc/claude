# Text formatting

Styling rules: how words look once the characters are right. They bind wherever bold, italic, size, caps or color are under control: HTML artifacts, Claude Docs, PDF and docx, slides, figures. In markdown only bold, italic, and heading level exist, so only those rows apply. Source: Butterick, *Practical Typography*, “Text Formatting” chapter.

## Emphasis ladder

- Bold or italic, never both on the same text, and as little as possible. Emphasis everywhere is emphasis nowhere. Never a whole paragraph in bold. Never underline bold. (bold-or-italic)
- Serif body text: italic for gentle emphasis, bold for heavy. Sans-serif body text: skip italic (it rarely registers) and use bold. (bold-or-italic)
- A third level, when needed, is all caps or small caps, letterspaced. (bold-or-italic)
- Weights past bold (black, ultra) belong to display sizes, not body text. Semibold is fine. (bold-or-italic)
- Punctuation beside emphasized text stays unemphasized, including brackets and parentheses, unless a roman mark collides with an italic letter. (bold-or-italic)
- Unfamiliar foreign words italic (bête noire, Weltanschauung); naturalized ones roman (croissant, résumé). Familiarity decides, not origin. Spell it “sans serif”. (bold-or-italic)

## Underlining

Never in print. It is the typewriter’s only emphasis, drawn as a rule across the descenders. Bold, italic, caps, small caps or a size change replace it. On the web the book says links no longer need underlines either, since color signals clickability and major publications have dropped it; this skill keeps a thin underline on links for accessibility (SKILL.md, emphasis rules). Track-changes underlining is revision marking, not emphasis, and stays. (underlining)

## All caps and small caps

- All caps sparingly: headings under one line, running headers and footers, captions, labels, letterhead, business cards. Never a paragraph, never long text in bold caps. Caps make every word a rectangle. (all-caps)
- Letterspace caps and small caps 5–12% (CSS `letter-spacing: 0.05em–0.12em`; Word 0.6–1.4 pt per 12 pt). Kerning on. Never so far that another letter would fit in the gap. Lowercase is not letterspaced, except below 9 pt, and headline-size lowercase may need tightening. The band is judgment, not a wall. (letterspacing)
- Apply caps as formatting (`text-transform: uppercase`; Word Ctrl⇧A; Mac ⌘⇧A), not Caps Lock, so they can be toggled off. Use the font’s cap-height figures and punctuation alternates if it has them. (all-caps)
- Small caps: only real ones, from a font that has them (OpenType `smcp`; a separate file in older families). The word-processor checkbox shrinks capitals and produces marks that are too tall and too light. Times New Roman and most system fonts have none. In CSS `font-variant: small-caps` now reaches the real glyphs when present. Whether a small-cap word opens with a full capital is a preference. (small-caps)

## Point size

- Print body 10–12 pt; screen body 15–25 px, specified in px. Tune in half-point steps (10, 10.5, 11.5); a half point shows at text sizes. (point-size)
- Emphasis by size climbs a half point, not from 11 to 14. Business cards run 6–8 pt, where caps and lowercase are equally legible. (point-size)
- Smaller type takes tighter line spacing and a shorter measure; the three move together. Equal point sizes look different across fonts, so match by line breaks, not by the number. (point-size, em-sizing)

## Headings

- Three levels at most, two if possible. Deeper hierarchies stop being navigable. (headings)
- Space above and below carries a heading, with less below than above so it binds to its text. Then, if needed, bold. Size rises slightly: 12 pt body, 12.5 or 13 pt heading, not 14 or 15. A bold heading may even drop half a point below body size. (headings, space-above-and-below)
- Not all caps, not Title Case, not underlined, not centered. Not derived from a modular scale; size headings by eye. (headings)
- No hyphenation in headings; keep-lines-together and keep-with-next on. Indent at most two levels regardless of heading depth. (headings)
- Numbered hierarchies use tiered decimals (1, 1.1, 1.1.1). Never roman numerals, romanettes, or letters, which blur past F and confuse i with 9. Let the tool generate them (`<ol>`, CSS counters). (hierarchical-headings)

## Kerning

Always on. Fonts ship hundreds to thousands of designed pairs. Word: Font › Advanced › “Kerning for fonts 8 points and above”, set in the style. Pages: on and cannot be disabled. CSS: `font-kerning: normal` (default) or `text-rendering: optimizeLegibility`. Manual pair kerning is for professionals. (kerning)

## Color

- Printed body text is black. No exceptions. Color at text size costs legibility and buys nothing. (color)
- Emphasis is bold, not color. Letterforms cover too little area to carry hue. (color)
- On screen, consider dark gray for body text, since screens project light. Not if the PDF will be printed; gray prints gritty. (color)
- On a web page, color the links and nothing else. Colored type on a colored background almost always reads worse. (color)
- Thin or small type takes a more intense color than heavy or large. Build a palette from shades of one color, not several contrasting hues. Light colors adjust in small steps, dark colors in larger ones. (color)
- Print: knockout (white on dark) burns about 20× the toner and prints muddy. Spot color for one- or two-color jobs; process color for photographs, never for small type or stationery, where halftone dots show. A red nudged toward orange is the printer’s classic second color. (color)
- Slides: background pure black in a dark room, text starting at 50% gray and brightened only until legible; in a lit room, light gray background with dark text. See documents.md. (presentations)

## Figures

Four figure styles, two axes: lining or oldstyle × proportional or tabular.

| Context | Style | CSS |
|---|---|---|
| running lowercase text | oldstyle proportional | `font-variant-numeric: oldstyle-nums proportional-nums` |
| alongside capitals | lining | `lining-nums` |
| columns of numbers | tabular lining | `tabular-nums lining-nums` |
| unsure | the font’s defaults | none; defaults are never wrong |

Never oldstyle beside capitals. Excel supports no OpenType features, so pick a font whose defaults are already tabular; Numbers does support them. (alternate-figures)

## Ordinals

Turn off automatic superscripting (Word: AutoCorrect › AutoFormat As You Type › Ordinals). Shrunken ordinals are illegible. A professional font’s purpose-drawn superior figures are the one acceptable superscript. HTML needs an explicit `<sup>` and should not bother. (ordinals)

## Web and email addresses

Never hyphenate an address; the reader takes the hyphen as part of it. Break long ones with a hard line break at a natural point. In print, give a shortened URL beside the full one when the full one is unreadable, and the full one alone when the reference must outlive the shortener. Turn off blue-underline autoformatting in documents headed for paper; keep it in a PDF whose links work. (web-and-email-addresses)

## Email

A typography-free zone: fonts do not travel with the message and clients render metrics unpredictably. If formatting at all, common system fonts and no spacing tricks. Contact details in live text, never a scanned image. (emails)

## Goofy and monospaced fonts

- Novelty, script, handwriting, stencil and circus faces stay out of professional documents. Distinctive is the goal; goofy is a jackhammer in a library. Billboards and signs are the exception. (goofy-fonts)
- Body text is proportional, never monospaced. Monospace is for code, where compressed syntax needs alignment, and for tabular figures. If forced to monospace, not Courier. (monospaced-fonts)

## OpenType features

A feature needs both the font and the application. Check the foundry’s specimen for what the font carries. Word (2010+ Windows, 2011+ Mac) exposes ligatures, figures and stylistic sets; Excel and PowerPoint expose none; InDesign, Illustrator and QuarkXPress expose everything. Desktop browsers support features via `font-feature-settings` and the `font-variant-*` properties; mobile browsers are inconsistent. (opentype-features)

## Mixing fonts

Optional. Size, bold, italic and small caps can carry a document with one font. If mixing: two fonts, each with one consistent job, switched only at paragraph breaks. A third is rare, four or more almost never. Pair for low contrast; two faces by the same designer often work (Atlas and Lyon; Alright Sans and Harriet). Serif plus sans is not required. A slide deck counts as one document. (mixing-fonts)

## Metrics vs optical spacing

InDesign only. Choose metrics; it uses the designer’s widths and kerning pairs. Optical spacing discards what the font’s designer built. Exceptions: badly spaced fonts (most free ones) and a text face pressed into headline duty, judged by eye either way. (metrics-vs-optical-spacing)

## Where the pages disagree

- all-caps allows caps for a heading under one line; headings forbids all-caps headings. Read together: a one-line label, footer or table caption may be caps; a document heading should not be.
- point-size mentions the web habit of headings at about 200% of body; headings says raise size minimally. The habit is what the book rejects; the rule is the minimal rise.
