# Document presets

Butterick’s “Sample Documents” chapter reworks one specimen of each type. These are the moves, plus the appendix pages on PDFs, embedding, screens, printers and designers. Chart and table typography lives in visuals.md; this file points there rather than repeating it.

## Research paper

The typewriter layout (1 in margins, 12 pt, double spacing, Times New Roman) optimizes nothing. Widen margins toward a 65-character measure, drop below 12 pt, tighten leading below double, use a real text face, one space between sentences, hyphenation on if justified, shorter first-line indents, no underlined headings. Control length by word count, not by padding margins. Obey a required layout when an authority insists. For shared drafts use common system fonts so collaborators’ machines do not reflow it; send a PDF when appearance must hold. (research-papers)

## Letter and letterhead

Foreground is the letter, background is the address block; the block must never upstage the text. Body text occupies more of the page than the stationery. Wide margins, short measure, one paragraph cue, no centered text, letter starting at the top of the page, a simple two-column arrangement. Name and address in a pale, quiet color (start near grayish blue). No screen fonts on paper. Letterpress first, offset second; internet printers only under about 500 pieces and only in process color, which stationery normally should not be. Off-white or ivory wove stock from a paper store. Laser-printed letterhead is fine when typography and paper get equal care. Do not mail what email or a PDF can carry. (letterhead)

## Business card

Strip everything nonessential. Small type is fine here (6–8 pt). Build outward from the text; never fling items to the four corners. No goofy or weak display faces; name at a reasonable size, consistent with the rest; caps and small caps letterspaced. Substantial stock, professionally printed, understated color, no stunt cards. (business-cards)

## Résumé

Spell it résumé (or resumé); bare “resume” is another word. Zero typos (about 90% of résumés have one, and one is enough to end a candidacy). Front-load page one; students stay on one page; two pages go on separate sheets. Larger margins, shorter lines, a real body font instead of Calibri, headings and gray boxes de-emphasized so employers, schools and dates surface, gentle bullets, good letterhead stock rather than novelty paper, delivered as a proper PDF. Several editors, each owing three changes. For design roles the résumé is the portfolio piece. (resumes)

## Slide deck

- Judge under the audience’s lighting: darken your room. Background pure black, not dark gray or a gradient. Text starts at 50% gray and brightens only until legible; thinner faces need more brightness. Thin sans serif. In a room that cannot be darkened, light gray background and dark gray text, not black on white. (presentations)
- Pick one base size that fits 12–15 lines and hold it on every slide; turn autofit off; cut text to fit the size, never the reverse. Loosen leading. Left-align; never center. Headlines modest and left. Lay out from the text outward, keep the layout narrower than the full screen on wide formats, repeat the same layout throughout. Pale color, sparingly. Drop bullets when every item fits one line. (presentations)
- A deck is one document for the two-font limit. Excel and PowerPoint expose no OpenType features, so pick fonts whose defaults already do what you need. (mixing-fonts, opentype-features)

## Website

Body text larger than the 1990s default, headings smaller, fonts beyond the Arial/Georgia/Verdana handful, navigation off the page edges, no layouts built from solid color blocks, no template cargo cults (full-bleed video, the 960 grid, hamburger menus). Hold 45–90 characters at every viewport width by scaling `font-size` and `max-width` together in `vw`, not by pixel-threshold media queries and not with `ch`. Phones are read closer, so the same size reads larger. Borrow from five centuries of print rather than from web templates. (websites, responsive-web-design)

## Email

Typography-free zone: system fonts or no formatting, no font-specific spacing, no alignment with spaces, contact details as live text. (emails)

## PDF export and font embedding

- Export straight to PDF (Office: File › Save As › PDF; Mac “Best for printing”; or the system Print › PDF route). Never print and scan; scans are large, slow and unsearchable, and bitmaps stay bitmaps. Combine PDFs in Acrobat rather than nesting documents in Word. (how-to-make-a-pdf)
- Word embeds only TrueType (`.ttf`), never OpenType PostScript (`.otf`), and reliably only the regular style, synthesizing italic and bold so line and page breaks shift. Check the font’s kind (Font Book ⌘I) and its embedding permission (`fsType` must read Editable or Installable). Windows: File › Options › Save › Embed fonts in this file, with both narrowing sub-options unchecked. Mac: Word › Preferences › Save › Font Embedding. (how-to-embed-fonts-in-a-word-document)

## Screen-only documents

Screen and print are no longer separate problems; resolution and color depth decide rendering, and phones (~326 dpi) and desktops (~185 dpi) now out-resolve the eye at reading distance (about 143 dpi needed at 24 in, 286 at 12 in). Use your print fonts on screen and retire the screen-optimized ones. A document read only on screen takes tighter margins and a larger size than letter paper; anything that might be printed keeps the print layout. Georgia and Calibri survive only for drafts exchanged with others, because everyone has them. (screen-reading-considerations)

## Printers and paper

Laser for text (inkjet for photographs). True PostScript over emulation. Ignore review-site verdicts and advertised dpi; judge from black text samples at several sizes. Monochrome beats color at the same price if color is not needed; price the toner first. Duplex plus opaque paper. Smoothest stock available, labeled laser, wove not laid; weigh smoothness, opacity and brightness. Print directly rather than photocopy when quality matters. (printers-and-paper)

## Working with a designer

Choose carefully, then stop micromanaging. Shortlist from portfolios (on the designer’s own domain) and referrals; ask for comparable samples and a written proposal with deliverables, budget and a prorated kill fee. No discounts, spec work or payment in exposure. Location is irrelevant. Review every deliverable in its real medium: print the letterhead, ask for HTML rather than a mockup. Keep the approval group small. (how-to-work-with-a-designer)

## Where the pages disagree

screen-reading-considerations retires Georgia and Calibri; research-papers and emails prescribe system fonts for shared drafts and mail. Both hold: the shared-draft and email cases are stated exceptions, not conflicts. websites says leave system fonts; emails requires them; web fonts can be served, mail fonts cannot.
