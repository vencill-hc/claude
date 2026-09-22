# Type composition

Character-level rules. They bind in every medium, including markdown, chat, PR bodies and email, because they are properties of the text itself, not of a layout. Source: Butterick, *Practical Typography*, “Type Composition” chapter (slugs in the right column resolve at https://practicaltypography.com/<slug>.html). Optional review aid: `scripts/typo-check.py` reports straight quotes, doubled hyphens and the other habits below with line numbers, and never rewrites.

## Glyph table

| Glyph | Name | Code point | HTML | Mac | Windows | Use |
|---|---|---|---|---|---|---|
| “ ” | double quotes | U+201C U+201D | `&ldquo;` `&rdquo;` | ⌥[ ⌥⇧[ | Alt 0147 0148 | every quotation in prose |
| ‘ ’ | single quotes | U+2018 U+2019 | `&lsquo;` `&rsquo;` | ⌥] ⌥⇧] | Alt 0145 0146 | nested quotes; ’ is also the apostrophe |
| – | en dash | U+2013 | `&ndash;` | ⌥- | Alt 0150 | ranges (1880–1912, pp. 330–39), paired names (Sarbanes–Oxley), casual minus |
| — | em dash | U+2014 | `&mdash;` | ⌥⇧- | Alt 0151 | sentence break; set closed, no spaces, unless the font crushes it |
| … | ellipsis | U+2026 | `&hellip;` | ⌥; | Alt 0133 | omission; one word space each side |
| © | copyright | U+00A9 | `&copy;` | ⌥g | Alt 0169 | in line with text, not raised; nonbreaking space before the year |
| ® | registered | U+00AE | `&reg;` | ⌥r | Alt 0174 | superscript, tight to the name |
| ™ | trademark | U+2122 | `&trade;` | ⌥2 | Alt 0153 | superscript, tight to the name |
| § ¶ | section, pilcrow | U+00A7 U+00B6 | `&sect;` `&para;` | ⌥6 ⌥7 | Alt 0167 0182 | citations only; nonbreaking space after; doubled for plurals (§§ 3–4) |
| × − ÷ | times, minus, divide | U+00D7 U+2212 U+00F7 | `&times;` `&minus;` `&divide;` | | | never x, hyphen, or slash; dimensions read 8.5″ × 11″ |
| ′ ″ | prime, double prime | U+2032 U+2033 | `&prime;` `&Prime;` | | | feet, inches, arcminutes; straight quotes substitute when the font lacks them |
| ­ | soft hyphen | U+00AD | `&shy;` | | | optional break point in a long word |
| (invisible) | nonbreaking space | U+00A0 | `&nbsp;` | ⌥space | Ctrl⇧space (Word) | glue between things that must not separate |
| (invisible) | thin space | U+2009 | `&thinsp;` | | | between initials when a word space looks wide |

## Quotes and apostrophes

- Curly quotes everywhere in prose. Straight `'` and `"` are typewriter marks with two legitimate homes: inside code (they are syntax) and as foot/inch marks after a digit (6' 10"). (straight-and-curly-quotes, foot-and-inch-marks)
- Apostrophes always point down: ’. Smart-quote software guesses wrong at the start of a word (‘70s should be ’70s, ‘n’ should be ’n’). To force it, type two straight singles and delete the first. (apostrophes)
- Fix quotes before apostrophes when cleaning pasted text; the other order goes wrong. Serve HTML as UTF-8 so the glyphs render. (straight-and-curly-quotes)
- Emphasis is bold or italic, never quotation marks. (straight-and-curly-quotes)
- Foot and inch marks stay straight even inside curly quotes, and bind to their number with a nonbreaking space. (foot-and-inch-marks)
- The Hawaiian ʻokina is a letter that points up, so it is set as ‘, not ’. (apostrophes)
- Tolerated: straight quotes in email and thumb-typed messages. Never curl quotes or backticks inside code. (straight-and-curly-quotes)

## Spaces and breaks

- One space after a sentence and after every other punctuation mark. The two-space habit is a monospace relic; no research supports it. Two spaces are tolerable only in monospaced text, or when your employer insists. (one-space-between-sentences)
- The word space does one thing: separate two words. Never stack it to align or indent. HTML collapses runs of whitespace to one space anyway, except `&nbsp;`. (word-spaces, white-space-characters)
- Six white-space characters, one job each: word space, nonbreaking space, tab, hard line break, carriage return, hard page break. Pick the one whose behavior survives editing. (white-space-characters)
- Nonbreaking space binds: § and ¶ to their number, © to its year, “Fig. 23”, “Ex. A”, “Ms. Marvel”, “Sgt. Rock”, 6′ 10″, and an ellipsis to the word beside it. Never chain nonbreaking spaces to open a gap. (nonbreaking-spaces)
- Hard line break (Shift+Return, `<br>`) starts a new line inside the same paragraph: address lines, a numbered heading that breaks badly, a signature block. Never a carriage return inside a list item, which renumbers the list. (hard-line-breaks)
- Carriage return means new paragraph. Vertical space comes from the paragraph’s space-after setting, never from extra returns. Strip doubled returns with find-and-replace, repeating until none remain. Tolerated in email, which has nothing better. (carriage-returns)
- Move text to a new page with one hard page break, or better, a page-break-before in the heading style. Never a run of returns. HTML has no page break; the CSS properties affect print only. (hard-page-breaks)
- Tabs: only for a horizontal gap mid-line, with tab stops set first (default stops every 0.5 in exist only so something happens). First-line indents come from the paragraph setting. Grids come from a table. Columns of figures align on a decimal tab. Never tab repeatedly across a line. HTML has no tabs; use a table, flexbox, or grid. (tabs-and-tab-stops)
- Thin space (U+2009, about half a word space) between initials when the full space looks wide. Layout software offers finer spaces (third, quarter, sixth, hair, figure, punctuation). (word-spaces)

## Hyphens and dashes

- Hyphen: compound words (topsy-turvy), phrasal adjectives before a noun (listener-supported radio, five-dollar bills), compound surnames (Sarbanes-Oxley the person). Prefixed words set solid (nonprofit). No hyphen after an -ly adverb (closely held company) or inside a foreign phrase used as an adjective (habeas corpus appeal). (hyphens-and-dashes)
- En dash: ranges (1880–1912, Exhibits A–E), paired words in connection or contrast (conservative–liberal split, Arizona–Nevada reciprocity, Sarbanes–Oxley Act as two authors). A range that opens with “from” takes “to”, not a dash. Also serves as a casual minus. (hyphens-and-dashes)
- Em dash: a sentence break where a comma is too weak and a colon too strong. Set closed against the words; open it with spaces only when a screen font crushes it. Never fake either dash with `--` or `---`. (hyphens-and-dashes)
- House rule: em dashes are banned in chat replies and in VV’s signed prose (editorialize). Recast with a period, comma, colon, or parentheses. The book’s permission does not apply there.
- Em and en are units (full and half body height), not letter widths. Bringhurst’s spaced en dash as a sentence break is Canadian practice, not American. (hyphens-and-dashes)
- Optional (soft) hyphen U+00AD marks where a word the dictionary does not know may break: jargon, odd names, trade names. Place as many as the word has break points; they stay invisible unless needed and do nothing when automatic hyphenation is off. Prefer them to `hyphens: auto`, whose browser support is spotty. (optional-hyphens)

## Symbols

- © ® ™ are real characters, never `(c)`, `(R)`, `(TM)`. ® and ™ superscript and tight to the name; © stays in line. Write “Copyright” or ©, not both. Turn off autocorrect’s parenthesized-letter substitution, which turns `Section 12(c)` into `Section 12©`. (trademark-and-copyright-symbols)
- Ellipsis is the single character …, spaced on both sides, nonbreaking on the side with text. Never three periods, bare or spaced. Fiction may use it for interrupted dialogue; elsewhere the em dash. If house style demands periods, join them with nonbreaking spaces. (ellipses)
- Math: × for multiplication and dimensions, − for subtraction, ÷ for division. The letter x and the hyphen are not math. Light arithmetic may use keyboard + = and an en dash for minus. (math-symbols)
- § and ¶ cite numbered sections and paragraphs, followed by a nonbreaking space, doubled for plurals. Spell the word out when the reference opens a sentence. Never scatter pilcrows through body text. (paragraph-and-section-marks)
- Ampersand is a contraction of *et*: use it the way you would use a contraction, so the more formal the document, the fewer. Inside a proper name it is always correct. (ampersands)
- Question marks: recast a flat topic sentence as a question when it reads pithier. Exclamation points: one per document over three pages, never stacked, never the interrobang outside comics. (question-marks-and-exclamation-points)
- Emoticons and emoji: out of anything formal. Never lean on an emoji’s exact rendering to carry nuance; every platform draws its own. A dry-humor winker for strangers is the one tolerated case. (emoticons-and-emoji)

## Parentheses, brackets, braces

- Parentheses hold citations and asides. Brackets mark your changes inside quoted material. Braces are for code and math. (parentheses-brackets-and-braces)
- Brackets and parentheses stay roman when their contents are italic or bold, unless the slanted letter physically collides with the upright mark, in which case italicize the mark and check by eye. (parentheses-brackets-and-braces)

## Semicolons and colons

Cross-posted to editorialize, which owns usage. Kept here because they push prose away from the generic. Garner’s *Modern English Usage* is the authority beyond these five. (semicolons-and-colons)

- A semicolon joins two complete sentences in place of a conjunction. After a subordinate clause the mark is a comma. When a conjunction already joins the clauses, drop the semicolon.
- Semicolons separate list items that themselves contain commas (Tulsa, Oklahoma; Flint, Michigan).
- A colon introduces whatever completes the idea before it.

## Accented characters

- Names keep their accents, every time: Dürer, Truffaut, Plácido Domingo. An unaccented name is misspelled. Names are set roman, never italic. (accented-characters)
- Loanwords English has absorbed drop the accent (naive, melee, coupe); ones still read as foreign keep it (cause célèbre, piña colada). A dictionary decides. For American readers write ss for ß, which reads as B or beta. (accented-characters)
- Typing: Mac dead keys `⌥e` `⌥i` `⌥u` `⌥n` and ⌥ plus the grave-accent key, then the letter (á is `⌥e` then `a`); direct keys `⌥a` å, `⌥o` ø, `⌥c` ç, `⌥'` æ, `⌥q` œ, `⌥s` ß. Windows Alt 0192–0252. HTML entities `&aacute;` through `&Uuml;`. (common-accented-characters)

## Ligatures

- Turn ligatures on only when the lowercase f actually collides with its neighbor in the chosen font, and check bold and italic separately. Otherwise off; they make body text look quaint. Never the decorative Th ligature. (ligatures)
- Enable through the font setting (Word Font › Advanced › Ligatures; CSS `font-variant-ligatures` or `text-rendering: optimizeLegibility`), never by pasting ligature glyphs, which break search, spell check and hyphenation. (ligatures)
- Never ligatures in programming fonts: `!=` `<=` `>=` `===` collide with real Unicode symbols and the substitution is context-blind. Redesigned glyphs for l/1 and 0/O disambiguation are fine. (ligatures-in-programming-fonts-hell-no)

## Signature lines

Print only. Repeat the underscore character; never underlined spaces (a select-all un-underline erases the line; a double-space find-and-replace halves it) or a drawn rule you plan to paste elsewhere. Keep the block on one page with keep-lines-together. In HTML use `&nbsp;` runs, since spaces collapse. (signature-lines)

## The typewriter habits

Twenty-two habits the typewriter taught, all wrong now: underlining, monospaced body text, all caps for emphasis, 12 pt as a default, one-inch margins as a default, single or double as the only line spacings, centering everything, ignoring kerning and letterspacing, two spaces after a period, straight quotes, hyphens as dashes, rules made from repeated characters. Robin Williams, *The Mac is Not a Typewriter*, made the same list first. (typewriter-habits)

## Where the pages disagree

- typewriter-habits lists “ignoring ligatures” as a habit; the ligatures page says leave them off unless the f collides. The dedicated page wins.
- typewriter-habits says tables, never tabs; the tabs page allows tabs for genuinely simple print jobs. Tabs ok in simple print, never in HTML.
- straight-and-curly-quotes bans straight quotes; foot-and-inch-marks and the code carve-out require them. Straight quotes only after digits and inside code.
