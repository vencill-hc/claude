# CSS starter for documents and artifacts

Butterick’s numbers as a stylesheet. Paste it into an HTML artifact or Claude Doc, set the four tokens, and adjust by eye. This is a document starter, not a design-token system (visual-design-foundations owns those), and it slots inside the artifact-design page contract (title, theming, CDN allowlist, phone width). The book rejects modular heading scales, so none is here.

## The four tokens

```css
:root {
  --body-font: "Source Serif 4", Charter, Georgia, serif;   /* a text face; Georgia is the draft-only fallback */
  --body-size: 18px;                                        /* 15–25 px; specify web type in px */
  --body-leading: 1.35;                                     /* 120–145%, unitless so it inherits */
  --measure: 38em;                                          /* ≈ 45–90 characters at body size; never ch, which measures the zero */

  /* Colors as tokens so the artifact-design dark-mode contract can redefine them. */
  --ink: #222;          /* screen body text: dark gray, not black; print overrides to #000 */
  --ink-soft: #444;     /* captions, sources, subtitles, rules */
  --rule: #444;
  --gridline: #ccc;
  --link: #1a4a8a;
  --paper: #fff;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { --ink: #ddd; --ink-soft: #aaa; --rule: #888; --gridline: #444; --link: #8ab4f8; --paper: #111; }
}
:root[data-theme="dark"] { --ink: #ddd; --ink-soft: #aaa; --rule: #888; --gridline: #444; --link: #8ab4f8; --paper: #111; }
```

`ch` is rejected because it measures the width of the digit 0, not an average character. At 18 px body, 38em is about 72 characters of a text serif; check by counting a real line and adjust. Butterick prefers `vw`-scaled sizes so type and container scale together; a fixed px body with an em-based measure is the simpler starting point for an artifact and stays inside the band at phone width if the container also has side padding.

## Body and paragraphs

```css
body {
  font-family: var(--body-font);
  font-size: var(--body-size);
  line-height: var(--body-leading);
  color: var(--ink); background: var(--paper);   /* dark gray for screen; print overrides to black */
  font-kerning: normal;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
}
main { max-width: var(--measure); margin: 0 auto; padding: 0 16px; }

/* One paragraph cue. Pick one block and delete the other. */
p { margin: 0 0 0.6em; }                                /* space after: 4–10 pt ≈ 50–100% of body size */
/* p { margin: 0; text-indent: 1.5em; } p:first-of-type { text-indent: 0; }   /* indent: 1–4× body size */

blockquote { margin: 0.6em 2em; font-size: 0.95em; line-height: 1.3; }   /* 2–5 em indent, slightly smaller and tighter */
```

## Headings

```css
h1, h2, h3 {
  font-family: inherit;               /* same font; a second font is optional and must have one job */
  font-weight: 700;                   /* bold is optional; if used, size may drop half a point */
  text-align: left;                   /* never centered, never all caps, never underlined, never Title Case */
  hyphens: none;
  break-after: avoid;                 /* keep-with-next */
  margin: 1.6em 0 0.5em;              /* space carries the heading; less below than above */
}
h1 { font-size: 1.15em; }             /* half-point steps over body, not a 200% jump */
h2 { font-size: 1.08em; }
h3 { font-size: 1em; }
/* No h4+. Three levels at most, two preferred. */
```

## Emphasis, caps, small caps

```css
em { font-style: italic; }            /* on a sans body use bold instead; never bold and italic together */
strong { font-weight: 700; }
u, .underline { text-decoration: none; }   /* underlining is a typewriter habit */
.caps { text-transform: uppercase; letter-spacing: 0.08em; }            /* 5–12%; under one line only */
.small-caps { font-variant-caps: small-caps; letter-spacing: 0.06em; }  /* real smcp or nothing */
a { color: var(--link); text-decoration: underline; text-decoration-thickness: 0.5px; text-underline-offset: 0.15em; }   /* color for links and nothing else; Butterick tolerates dropping the underline, accessibility keeps a thin one */
```

## Lists, rules, tables

```css
ul, ol { padding-left: 1.4em; }       /* at most two indent levels */
hr { border: 0; border-top: 0.5pt solid var(--rule); margin: 1.2em 0; }   /* 0.5–1 pt, single, solid */

table { border-collapse: collapse; border: 0; }
th, td { border: 0; padding: 0.15em 0.6em; text-align: left; vertical-align: baseline; }
thead th { border-bottom: 0.5pt solid var(--rule); }       /* restore only the border legibility needs */
td.num, th.num { text-align: right; font-variant-numeric: tabular-nums lining-nums; }
```

## Figure block (data visualizations)

```css
figure { margin: 1.2em 0; }
figure .title { font-weight: 700; font-size: 1.05em; margin: 0 0 0.3em; text-align: left; }
figure .subtitle { color: var(--ink-soft); margin: 0 0 0.6em; font-size: 0.9em; }   /* one step below the title; Urban ratio ≈ 0.8 of title */
figure .axis, figure .tick, figure .legend {
  font-variant-numeric: tabular-nums lining-nums;                 /* digits align; lining beside caps */
  font-size: 0.8em;                                               /* ≈ 0.6 of the title (Urban ratio); never below 12 px (Datawrapper) */
  letter-spacing: 0.01em;
}
figure .label-caps { text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.75em; }
figure figcaption, figure .source { font-size: 0.8em; color: var(--ink-soft); hyphens: none; word-break: break-word; }  /* never hyphenate a URL */
figure .gridline { stroke: var(--gridline); stroke-width: 0.5; }   /* hairline, single, solid (SVG user units, ≈ half a point) */
figure text { fill: var(--ink); }                                       /* body color; series color belongs to marks, not labels */
```

## Print stylesheet

```css
@media print {
  :root { --ink: #000; --paper: #fff; }                       /* black without exception on paper */
  body { font-size: 11pt; line-height: 1.3; }                 /* 10–12 pt */
  main { max-width: none; margin: 0 1.75in; }                /* 1.5–2 in side margins at ~12 pt */
  h1, h2, h3 { break-after: avoid; }
  a { color: inherit; }
}
```

## Property crosswalk

| Book rule | CSS |
|---|---|
| point size 15–25 px web | `font-size` in px |
| line spacing 120–145% | unitless `line-height` |
| line length 45–90 chars | `max-width` in em on the container, plus `padding` |
| margins, not indents, set the measure | `margin`, `padding` on the container |
| first-line indent 1–4× | `text-indent` |
| paragraph space 4–10 pt | `margin-bottom` (after, not before) |
| letterspacing caps 5–12% | `letter-spacing: 0.05em–0.12em` |
| real small caps | `font-variant-caps: small-caps` (needs `smcp`) |
| kerning on | `font-kerning: normal`, `text-rendering: optimizeLegibility` |
| tabular lining figures | `font-variant-numeric: tabular-nums lining-nums` |
| oldstyle in lowercase text | `font-variant-numeric: oldstyle-nums proportional-nums` |
| ligatures only if f collides | `font-variant-ligatures: common-ligatures` or `none` |
| no hyphenation in headings and URLs | `hyphens: none` |
| keep heading with next | `break-after: avoid` |
| rules 0.5–1 pt solid | `border-top: 0.5pt solid` |
| tiered heading numbers | `counter-reset`, `counter-increment` |
| OpenType features | `font-feature-settings`, `font-variant-*`; desktop yes, mobile inconsistent |
| dark gray screen text, black print | `--ink` token, redefined for dark mode and set to `#000` under `@media print` |

## Fonts for artifacts

From the CDN allowlist, Google Fonts carries the free faces the book endorses: Source Serif 4, Source Code Pro, Fira Mono, IBM Plex Serif, IBM Plex Sans, IBM Plex Mono, Charis SIL. Load one text face and, if needed, one monospace. Georgia stays only as an unloaded fallback for the moment before the web font arrives.
