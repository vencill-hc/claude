# Exemplars

Her prose, verbatim, typos intact (the typos are grain; never correct them). Annotated so drafts match the moves rather than parrot the words.

Two kinds live here. **Passages** are full multi-sentence runs, harvested from her blog (`blog/content/`), each annotated on three axes: rhythm (the cadence at paragraph scale), dosage (how much plain prose surrounds each hit), and move (the lexical signature). **Aphorisms** are the original single-sentence harvest, kept at the bottom; they teach a move but not a rhythm, and a one-line quote amputates the plain prose that makes a hit land, so weight the passages first.

## The register dial

Her technical writing rides one axis: **paper-abstract ←→ magazine-exposé**. Both ends are hers.

- **Paper-abstract end**: methodological, impersonal, passive-tolerant. The actor recedes; the method and result lead. Ornament budget near zero. This is the default for reference docs, schema notes, anything where content is code or fact.
- **Magazine-exposé end**: proseful, voiced, active, a reference dropped without genuflection, a coinage minted in place. The default for essays and design writeups with a real argument to carry.

A single piece slides along the dial; a paragraph of flat exposition can end on one exposé-end hit. The voice pass picks a point per artifact and per paragraph. Passive at the abstract end is a feature, not a tell (see banned-tells.md, evasive vs. methodological passive). The whole skill of voicing is choosing the point on this dial and then keeping the ornament sparse enough that each hit registers as an event.

---

# Passages

## Paper-abstract end

### Dry reference: when the content is code, go plain

> You can add new optional fields to a schema without breaking existing producers. The producers just keep sending what they always have, and consumers get `None` for the new field until the producers catch up.
>
> Pydantic will silently fill the gap.

- Rhythm: two even explanatory sentences, then a four-word verdict on its own line. The short close does the work; no flourish on it.
- Dosage: zero ornament. The content is a code snippet, so the prose stays out of the way. This is the floor of the dial, and it is correct here, not beige.
- Move: plain verbs, named actors (producers, consumers, Pydantic). The personification ("silently fill the gap") is the only seasoning and it is one word past literal.

### Methodological exposition with a single dry hit

> Makes key disclosures that relate to corporate governance. This is where changes to corporate board membership are disclosed to the SEC. Unfortunately these filings are mostly unstructured, and every company has a different format for submitting this filing. If only corporate boards filed git diffs.

- Rhythm: three flat declaratives of increasing length, then a short conditional that turns the whole thing into a joke. The hit is the exit, not the entrance.
- Dosage: the lesson in one paragraph. Three plain sentences earn one dry hit. The joke lands because the prose around it is methodical and unfunny; saturate the paragraph with jokes and none of them register.
- Move: passive used correctly ("are disclosed to the SEC", elsewhere "More research is needed", "is mandated by law") because the actor genuinely does not matter. Methodological passive, the abstract-end signature. The single hit is a discipline reference ("filed git diffs") dropped without setup.

### PR-body opening: narrative's one slot (her edit of the SUP-420 body, 2026-08-11)

> Bug fixes to the job function keyword table, staged ahead of the larger taxonomy swap so the swap's delta shrinks to the changes that are actually about taxonomy. Two root causes cover nearly everything here.

- Rhythm: one long orientation breath, then a five-word setup that hands off to a numbered list. The prose stops the moment enumeration starts.
- Dosage: zero ornament. Her one addition to the draft's sentence was "larger": a single word of orientation for readers outside the project.
- Move: the abstract-end floor applied to a PR opening. The full before/after pair and its form rulings live in the pr-body skill (references/sup-420.md).

## Magazine-exposé end

### Technical essay with a reference landing hard

> Existential dread has been following me around for the last month. Since starting my deep dive to figure out Claude code, boundary-test what it's capable of, and incorporating it into my daily workflow, there has been a vertigo-esq sense of un-grounding. Why do I feel queasy about this, when I'm using it to create more than I ever have?

> This asymmetry underlies a lot of assumptions I make about information consumption. It's been flipped entirely on its head. What's worth reading anymore? Traditional signals are faltering. The center cannot hold.

- Rhythm: short declarative open, then a long comma-stacked breath (three verbs in series), then a question that turns the screw. The second passage compresses: short, shorter, question, two hard four-word closes. Sentence length is the instrument.
- Dosage: even at the exposé end, most sentences are plain. Two coinages ("vertigo-esq", "un-grounding") and one literary reference ("The center cannot hold", Yeats) across two paragraphs. The reference lands because nothing else is reaching.
- Move: coinage spent in-sentence, reference dropped without genuflection, the question as a rhythmic device. Typo grain intact ("vertigo-esq").

## Thinking-out-loud (work notes)

### Reasoning a problem aloud

> Thinking about how to manage `TradingSymbols` in the `TradingIdentifier`. There can absolutely be duplicates. How do we want to handle these? I'm thinking that because these are aliases/identifiers and not descriptors, forcing the set to be unique on `(exch, symbol)` is reasonable. We don't really care if an organization went public under `EXCH:SYMB`, then unlisted, then re-IPO'd as `EXCH:SYMB` a second time.
>
> Ok. Reasonable.

- Rhythm: a question to herself, a long reasoning sentence working toward the answer, then a two-word fragment ratifying it. The cadence is a mind deciding in real time.
- Dosage: no ornament at all; the texture is the self-dialogue, not the diction. "Ok. Reasonable." is a fragment doing the work a paragraph of hedging would do worse.
- Move: first-person reasoning, fragments allowed, the problem talked through rather than reported. This register is closest to conversational-register.md but pointed at work.

### Work-note opener, idiom in passing

> Now I can feel like a fancy editor of an intellectually interesting website. I spent most of today trying to reimagine how I get my work done. I'm realizing I'm fighting a bad habit I developed towards the tail end of my last tenure, in that I assume because there's no deliverable, I don't have a status update.

> If I don't write, I'm either not thinking deeply or I'm allowing AI to drive the bus more than I ought to.

- Rhythm: a wry opener, then steadily lengthening sentences as the thought deepens. The breath grows with the idea.
- Dosage: one idiom ("drive the bus") in an otherwise plain reflection. Earnest, but the earnestness is stated once and not dwelt on.
- Move: self-aware opener, idiom dropped in passing, the honesty undercut before it gets precious.

## Headline and deck voice

> Digital gardening in the twilight of human prose

> Turning and turning in the widening gyre

> Rediscovering the lost art of building quality software

- The curated-line register: a deck or lead-in carries more ornament per word than the body it sits over, because it is one line and has to earn the click. This is the one place the ornament budget runs high. A Yeats line, a "twilight of", a "lost art of" land here that would be too much in a paragraph. Match this register only for titles, decks, and lead-ins; never for body prose.

---

# Aphorisms

The original harvest (June 2026, one conversation about her own voice). Single sentences: they teach a move, not a rhythm. Useful, but the passages above carry more.

## Coinage that arrives assembled

> the internet is a damning record resolution machine

Noun-stack minted in place and spent in the same sentence. No setup, no explanation after.

## The manifesto declarative

> i am not an engineering technical problem and my prose is not for analysis, its simply for the prose of it

Parallel negation landing on a flat assertion. Rhythm carries the argument; no hedges anywhere.

## Formal syntax surfacing mid-thought

> Staking this voice costs precision, where I use flair and dramatics and metaphor the technical acumen is diminished, for the metaphor carries understanding only for those already steeped into its contexts; unpenitrable for the uninitiated.

Archaic "for the" construction, a structural semicolon, a coined closer. The academic training shows through without slowing down.

## The self-portrait spec

> The whole thing should sound like a crazy tumblr girl learned how to write research papers, proficiently explain ideas sharply, simply, without the tells of LLM-isms and in a quarter as many words without being terse.

High/low collision as identity. Also the working definition of the target voice; treat as normative.

## Parenthetical self-interruption, coinage in passing

> I have beautiful penmanship (penwomanship?), my handwriting on a whiteboard is a monospace serif font honed over traumatizing algorithm memorization sessions in college.

The aside mints a word and moves on. Long breath-sentence, concrete image, no dwelling.

## Rhythm as instruction

> wax poetic spin a little drunk, lucidily, dance dance, dance

Incantatory repetition; punctuation loosens as the sentence accelerates.

## The semicolon hinge

> Magazines infect me with the desire to write well, to have curated taste that reads as curated taste; intellectual consumption as identity.

Visceral verb ("infect"), self-aware doubling, then the semicolon swings into a four-word abstraction.

## Moves, summarized

Coinages spent in-sentence. Visceral verb palette (infect, thrash, drown, wash away). Long comma-stacked breath landing on a short hard close. Structural semicolons even in casual prose. References dropped without genuflection. Register collision, slang and nineteenth-century syntax in the same paragraph. Typos as watermark. And the governing constraint behind all of them: sparsity. The moves are seasoning, not the dish. Most sentences are plain; a hit per paragraph or so, and it lands because of the flat prose around it. Saturate the text and it reads like a student straining to sound impressive.
