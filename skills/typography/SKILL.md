---
name: typography
description: Typeset written output well, per Butterick's Practical Typography. Character rules (curly quotes, real dashes and ellipses, one space, real © ® ™, downward apostrophes) bind in every response, PR body, doc and artifact; body-text, heading, layout, table, font and chart-label rules bind wherever CSS or page layout is under control (HTML artifacts, Claude Docs, PDF/docx, slides, data visualizations). Use when producing or reviewing any document, artifact, deck, figure or table, or on "typography", "typeset", "fix the quotes", "fix the dashes", "make this look better", "this looks like a default template". House writing rules (editorialize, pr-body, the chat no-em-dash rule) outrank this skill where they collide. Do NOT use for code, SQL, commit messages, or spreadsheet layout; UI design tokens and type scales belong to visual-design-foundations.
---

# Typography

Condensed from Matthew Butterick, *Practical Typography* (https://practicaltypography.com/), a reader-supported book. Rules are paraphrased with his numbers kept; nothing here reproduces his text. If the book earns its keep, pay for it.

Precedence: house rules win. Chat replies to VV carry no em dashes (system rule) and her signed prose follows editorialize; this skill fills in everything those rules leave open and never overrides them.

## Body text first

Four decisions set the typographic quality of any document. Make them before touching anything else.

| Decision | Print | Screen |
|---|---|---|
| Point size | 10–12 pt | 15–25 px |
| Line spacing | 120–145% of point size | same, written as unitless `line-height` 1.2–1.45 |
| Line length | 45–90 characters incl. spaces (2–3 lowercase alphabets) | same, held with `max-width` |
| Font | a professional text face; never Times New Roman, Arial, or a novelty face | same; Google Fonts picks in references/fonts.md |

Then paragraphs: first-line indent of 1–4× the point size, *or* 4–10 pt of space between paragraphs, never both.

## Key rules

Characters (every medium, including markdown and chat):
- Curly quotes “ ” ‘ ’, never straight. Straight marks survive only as foot/inch marks after digits and inside code.
- Apostrophes point down: ’ (U+2019), including word-initial ones (’70s).
- One space after a sentence. Never two consecutive spaces or whitespace characters.
- Hyphen for compounds and phrasal adjectives, en dash – for ranges and paired names, em dash — for a sentence break. Never `--` or `---`.
- Ellipsis is one character … with spaces around it, never three periods.
- Real symbols: © ® ™ × − ÷, never `(c)` `(R)` `(TM)` or the letter x between numbers.
- Nonbreaking space after ¶ and §, between © and its year, inside “Fig. 3”, “Ms. Marvel”, 6′ 10″.
- One exclamation point per document longer than three pages. Never stacked.
- Ampersands only inside proper names.

Emphasis:
- Bold *or* italic, never both, and as little as possible. Never a whole paragraph in either.
- Never underline. Web links are the one tolerated case; this skill keeps a thin underline on links for accessibility even though the book allows dropping it, and formatting.md and css.md defer to this sentence. Never all caps beyond one line; letterspace caps and small caps 5–12%.
- Real small caps or none. Kerning always on.
- Headings: at most three levels, ideally two. Space above and below carries them; size rises in half-point steps, not by a multiple. Not centered, not underlined, not all caps. Headings and titles are Title Case, the house ruling of 2026-08-19 shared with editorialize and pr-body; Butterick prefers sentence case and is overruled on this one point.

Layout:
- Left-align. Center only a short title or a name on a card. Justify only with hyphenation on, and only in real layout software.
- Margins set the measure. 1.5–2 in side margins at 12 pt on letter paper; on the web, generous `margin`/`padding` and a capped container.
- Tables: all borders off first, then restore only what legibility needs. Rules 0.5–1 pt, single, solid. Tabular lining figures in number columns.
- Lists: automatic bullets or numbers, never typed; never asterisks as bullets. Bullets drop when every item fits one line on a slide.
- Rules come from the border tool, never from repeated hyphens or underscores.

Fonts:
- Two fonts per document at most, each with one consistent job, switched only at paragraph breaks.
- System fonts only when forced, and then only from the tolerated list. Never the credibility-fatal list (Arial, Verdana, Comic Sans, Papyrus, Trebuchet, Tahoma, Copperplate, Bookman Old Style, Brush Script).
- Screen-era faces (Georgia, Verdana, Calibri, Cambria) never in anything that may be printed.
- Monospace only for code and aligned figures; never for body text.

## Which reference binds where

| Medium | Load | What is under your control |
|---|---|---|
| Markdown, chat, PR bodies, email | composition.md | Characters only. |
| HTML artifacts, web pages | css.md first; composition for the text; formatting and layout only when reviewing or when a question comes up | Everything. css.md already carries the layout numbers. |
| Claude Docs | composition, formatting (emphasis, headings), layout (paragraphs, lists, tables) | Characters and structure only: no CSS, no fonts. Three heading levels at most, one paragraph cue, minimal table borders, one emphasis tool at a time. |
| PDF, docx, letters, papers, résumés | documents.md preset, then layout.md; composition for the text; formatting and fonts on demand | Everything plus page breaks, widows, embedding. |
| Slides | composition, formatting, documents.md (presentation preset) | Size held constant, black background in a dark room, no centering, text-first layout. |
| Code, code blocks, monospace | composition.md (code exceptions), fonts.md (monospace picks) | Straight quotes and backticks stay; no programming ligatures; tabular figures. |
| Data visualizations, dashboards, number tables | visuals.md, then css.md figure block | Title, labels, tick text, legend, caption, number columns. The book has no rule for subtitles, axis labels, annotations or legends; visuals.md fills those from Datawrapper, the Urban Institute, the UK Government Analysis Function and the ONS, each marked as not Butterick’s. |

## Workflow

1. Name the medium. It decides which rules can even be applied.
2. Make the four body-text decisions and write them down (CSS tokens, a docx style, a slide master).
3. Write. Headings by space, emphasis by one tool at a time, paragraphs by one cue.
4. For an HTML artifact, paste the css.md starter and adjust the four tokens. A Claude Doc takes no CSS: apply the structure rules to the text.
5. Look at the result in its real medium. Two candidates that disagree get rendered side by side; reasoning alone does not settle typography. `scripts/typo-check.py` is an optional second pair of eyes for the character rules; it reports with line numbers and never rewrites.

## Handoffs

- editorialize owns voice, structure, and usage (semicolons, colons, Garner). pr-body owns PR skeletons and points here for characters. This skill owns characters and layout beneath both.
- visual-design-foundations owns UI design tokens and type scales for product interfaces. css.md is a document starter, not a token system, and Butterick rejects modular heading scales outright.
- artifact-design owns the artifact page contract (title, theming, CDN allowlist, phone width). css.md slots inside it.
- Never fetch practicaltypography.com pages into a document; cite the book by name and link the page.

## References

- references/composition.md: characters, glyph table with code points and entities, white-space characters, hyphenation, math symbols, ligatures, accents.
- references/formatting.md: bold/italic/caps/small caps, point size, headings, letterspacing, kerning, color, figures, ordinals, URLs, OpenType, mixing fonts.
- references/layout.md: alignment, indents and paragraph space, line spacing and length, margins, hyphenation, block quotes, lists, tables, rules, widows, keep-with-next, columns, grids, styles, the nine maxims.
- references/fonts.md: system-font tiers, free fonts worth using, alternatives-to-X table, monospace picks, licensing and identification.
- references/documents.md: presets for research paper, letter, business card, résumé, slide deck, website, email, PDF export and font embedding, screen-only documents, printers and paper.
- references/visuals.md: chart typography by part, number tables, gridlines, color text, projected figures, plus a sourced extension (Datawrapper, Urban Institute, Government Analysis Function, ONS) for the parts the book never covers.
- references/css.md: the starter stylesheet with the four tokens, heading and paragraph rules, figure block, and the CSS-property crosswalk.
- scripts/typo-check.py: optional report-only scan for the character rules, with scripts/test_typo_check.py (plain asserts, `python3 test_typo_check.py`).
