# Fonts

Butterick sells fonts, and the book’s “Font Recommendations” chapter is partly a catalogue. This sheet keeps the judgments that transfer: which system fonts are tolerable, which free fonts are worth using, what replaces the defaults, and how licensing works. His own faces appear only where he names them as the replacement for a default.

## Principles

- Professional fonts are the most visible improvement available. A text family needs roman, italic, bold, bold italic and real small caps; expect $20–50 per style. License per user; sharing one license across an organization is the most common violation. (font-basics)
- Prefer OpenType `.otf`, except TrueType `.ttf` for Microsoft Office on Windows, which renders it better and is the only format Word will embed. (font-basics)
- A name is not a design. Baskerville, Garamond and Caslon are unprotected names reused across unrelated fonts. Trademarked names (Myriad) do identify one design. (font-basics)
- System fonts are not free fonts: preinstalled does not mean openly licensed. Most free fonts are not worth using; the good ones came from funded organizations. (free-fonts)
- Uniformity is numbing; good faces vary subtly between letters. Screen-optimized faces (Georgia, Verdana, Cambria, Calibri) look clunky at 600 dpi and stay off anything that may be printed. (cambria-alternatives, system-fonts)
- Two fonts per document at most, each with one job. See formatting.md.

## System font tiers

The A list is fine for print and screen; the B list for screen and drafts in limited doses; the C list is questionable; the F list is fatal to credibility. Some F-list faces are honest and merely inapt for professional work. (system-fonts)

| Tier | Fonts |
|---|---|
| A, tolerable | Athelas, Avenir, Bell MT, Book Antiqua, Californian FB, Calisto MT, Century Schoolbook, Charter, Franklin Gothic, Garamond, Gill Sans, Goudy Old Style, Helvetica and Helvetica Neue (bland, overused), Hoefler Text, Iowan Old Style, Optima, Palatino (harsh rendering of Zapf), Seravek, Sitka |
| B, limited doses | Agency FB, Big Caslon, ITC Bodoni 72, Calibri, Candara, Centaur, Constantia, Corbel, Futura, Geneva, Gloucester MT Extra Condensed, High Tower Text, Modern No. 20, Perpetua, Rockwell, Segoe UI, Tw Cen MT |
| C, questionable | Baskerville (brittle, quaint), Cambria and Georgia (screen only), Times New Roman, Courier, Consolas, Menlo, Andale Mono, Berlin Sans FB, Bernard MT, Castellar, Century Gothic, Cochin, Cooper Black, Didot, Elephant, Engravers MT, Eras, Felix Titling, Haettenschweiler, Impact, Lucida (all), Maiandra, Niagara, Onyx, Plantagenet Cherokee, Skia |
| F, never | Arial, Verdana, Tahoma, Trebuchet MS, Comic Sans, Papyrus, Bookman Old Style, Copperplate, Brush Script and the Office scripts, American Typewriter, Monaco, Century, and roughly sixty novelty faces (Algerian, Bauhaus 93, Chalkboard, Curlz, Jokerman, Marker Felt, Noteworthy, Zapfino and kin) |

Bodoni MT is B-listed but called skunked on the bad-fonts page; treat it as C. Bookman Old Style is the corduroy suit of fonts. Times New Roman connotes apathy: the absence of a choice. Arial cannot produce good typography. (bad-fonts, times-new-roman-alternatives, helvetica-and-arial-alternatives)

## Free fonts worth using

| Font | License | Role |
|---|---|---|
| Charter (Bitstream) | free, original X Consortium files; also a macOS system font | best free text serif; Matthew Carter, 1987, designed for 300 dpi. Keep the Bitstream notice on unmodified copies. |
| Source Serif | OFL | text serif; Cambria replacement |
| Source Code | OFL | monospace |
| Fira Mono | free | monospace; the one free font endorsed without reservation. Not Fira Code, whose ligatures are the practice the book rejects. |
| IBM Plex | OFL | full family, serif, sans, mono |
| Cooper Hewitt | OFL | sans |
| Charis | free | Charter derivative with a bigger character set and questionable modifications |

For Google Fonts in artifacts, the same names apply: Source Serif 4, Source Code Pro, Fira Mono, IBM Plex Serif / Sans / Mono, Charis SIL. Charter is not on Google Fonts; it ships with macOS and can be self-hosted.

## Alternatives to the defaults

| Default | Why leave it | Paid alternatives the book names |
|---|---|---|
| Helvetica, Arial | bland; Arial is a Helvetica clone | Neue Haas Grotesk, Atlas, Concourse, Hermes Maia |
| Times New Roman | the non-choice | Plantin (Times is a taller, brighter Plantin), Equity |
| Courier | spindly, lumpy | Triplicate, Pitch, Input, Fira Mono (free) |
| Palatino, Book Antiqua | system version misrepresents Zapf | Palatino Nova, Verdigris, Valkyrie, Iowan Old Style (system) |
| Baskerville | brittle, quaint | Baskerville 10, Ingeborg, Kingfisher |
| Century Schoolbook | loose and broad | Century Supra, Miller, Harriet, Ingeborg |
| Georgia | 1990s screen font | Miller, Harriet, Chronicle, Century Supra |
| Verdana | 1990s screen font | Alright Sans, Sweet Sans, Breuer, Hermes Maia, Concourse |
| Gill Sans | overexposed, though charming | Ideal Sans, Brandon Text, Verlag |
| Cambria | monotonous screen font | Guardian Egyptian, Elena, Skolar, Source Serif (free) |
| Calibri | soft rounded corners in print | Seravek (system), Guardian Sans, Fort, Concourse |
| Minion | the Adobe default, chosen by bundling | Lyon and the other serifs above |

## Monospace and code

Monospace only for code and aligned figures; never body text. If forced: not Courier. No programming ligatures in shared code; `!=` and `<=` must not be redrawn into symbols the text does not contain. Redesigned l/1 and 0/O for disambiguation are fine. Tabular figures do the alignment job in proportional fonts. (monospaced-fonts, ligatures-in-programming-fonts-hell-no)

## Licensing and identification

- US law does not copyright letterforms; only the font software can be registered (1976 statute, 1992 regulation). Scope is unsettled case law (Adobe v. Southern Software, 1997, settled). Treat licensing as an honor system and honor it. (the-copyright-status-of-fonts)
- Identify a book’s fonts from its colophon; a website’s from the `font-family` in its CSS. Judge by the distinctive letters (A E G M Q R S a e f g r s t and the ampersand), not punctuation. WhatFont, WhatTheFont and Identifont cover about 95% of real-world fonts; @Font_ID and @TypeID for the rest. (identifying-fonts)

## Where the pages disagree

- Seravek is listed as a system font (macOS) and sold as a Calibri alternative; both are true.
- Charter is called free and also ships as a macOS system font; both are true.
- Bodoni MT sits on the B list and is condemned as skunked; follow the condemnation.
