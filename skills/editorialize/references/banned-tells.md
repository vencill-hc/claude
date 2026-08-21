# Banned tells

Constructions that mark prose as LLM output. Each disqualifies a draft. Before/after pairs show the repair. Grows by appending; never rewrite existing entries.

## The corrective reframe

All forms: "not X but Y", "X is not Y, it's actually Z", "that's not X, that's Y". The tic of a model that wants every sentence to be a small revelation.

Before: "That's not a bug, it's actually a signal that the contract was never enforced."
After: "The contract was never enforced; the bug is the first evidence."

## The bow-tie ending

A final sentence that wraps the piece in a moral, restates the theme, or lands a callback. End on the last fact. If the closing sentence could be deleted with no information lost, delete it.

## Rule-of-three

Triads everywhere: three adjectives, three examples, three parallel clauses. Vary the count; one example often beats three. Includes the staccato fragment triad: "X. Not Y. Just Z."

## Consultant lexicon

load-bearing, leverage (as a verb), robust, delve, deep dive, "the key insight", "at its core", fundamentally, landscape, journey, "rich" anything, crucial, comprehensive, seamless. Use plain verbs and name the actual thing.

## Throat-clearing

"It's worth noting that", "Importantly,", "Here's the thing:", "The reality is", "Let's unpack this." Delete the opener; start with the fact.

Before: "It's worth noting that the join runs before the filter."
After: "The join runs before the filter."

## Hedge-stacking

"arguably", "potentially", "to some extent", chained. One hedge maximum, prefer zero: commit or omit.

## Em-dashes

Never. Colons, periods, parentheses, commas.

## Bold and heading spam

Bold never leads a list item. Bold is for rare critical callouts, roughly one per document. Headings exist for navigation; a document readable in one screen needs none.

## Length inflation

Restating the request, summarizing what was just said, paragraph captions on self-evident tables. Compression removes filler; terseness removes texture. Remove filler.

## Warm validating closes

"Hope this helps!", "You've got this", "Happy to dig deeper." End when the content ends.

## Motif callbacks

Reusing an earlier phrase to seem attentive. Once is voice; twice is a bit; three times is a tell.

---

# Humanizer adoption

Appended June 2026 from blader/humanizer, which builds on Wikipedia's "Signs of AI writing". Method rules that came with it: rewrite rather than delete (preserve meaning), and judge clusters, not single instances.

## Negative parallelism

"not just X, but Y", "it's not about X, it's about Y". Sibling of the corrective reframe above. State the thing directly.

## Copula avoidance

"serves as", "functions as", "acts as", "stands as a testament to", where "is" is meant. Use "is".

## High-frequency AI vocabulary

pivotal, tapestry, vibrant, testament, underscore, boast, foster, showcase, realm, multifaceted, ever-evolving. Extends the consultant lexicon above.

## Undue significance

"This reflects a broader trend", "in today's fast-paced world", "plays a vital role in shaping". If the broader trend matters, show evidence; otherwise cut.

## Superficial -ing analysis

Trailing clauses that fake depth: "highlighting the importance of", "underscoring the need for", "demonstrating the value of". Cut the clause; if the point matters it gets its own sentence.

## Weasel attributions

"experts say", "many believe", "widely regarded as", "some argue". Name who, or own the claim.

## False ranges

"from X to Y" spans that measure nothing ("from data pipelines to machine learning"). List the actual things or cut.

## Signposting

"Let's dive in", "Without further ado", "Buckle up". Extends throat-clearing above.

## Title Case headings and emoji decoration

Sentence case headings. No emoji in shipped prose.

## Chatbot correspondence

"I hope this helps", "feel free to", "as of my last update", knowledge-cutoff disclaimers. These never ship.

## Parenthetical example-stacking

Load-bearing examples or definitions crammed into running prose as serial parentheticals. One parenthetical aside is a voice move (a coinage minted in passing); a stack of them carrying the actual content is a list wearing a trenchcoat. When two or more items each need an example, break them into bullets, one item per line, example after the dash.

Before: "alpha-2 and alpha-3 are the ISO codes ("CA" / "CAN" for Canada); an exonym is one language's name for a place in another ("Turkey" for Türkiye, "Munich" for München); diacritic stripping normalizes accents ("Canadá" → "canada")."

After:
- alpha-2 / alpha-3 — the ISO 3166-1 country codes. "CA" and "CAN" for Canada.
- exonym — one language's name for a place in another. "Turkey" for Türkiye, "Munich" for München.
- diacritic stripping — accents normalized to bare ASCII before lookup, so "Canadá" becomes "canada".

## Evasive passive

Passive voice that hides an actor who matters ("mistakes were made", "it was decided"). Name the actor when naming it adds information.

Not banned: methodological passive, the paper-abstract register where the actor genuinely doesn't matter and convention foregrounds the method or result ("the filings are disclosed to the SEC", "more research is needed", "the set is forced unique on (exch, symbol)"). This is a feature of the abstract end of the register dial, not a tell. The test: does naming the actor add information? If no, passive is correct and often better. See the methodological-exposition passage in exemplars.md.

## Semicolon-stacked ordered lists

Sequential or ranked items (steps, gates, preconditions, anything introduced as "in order") packed into one sentence and joined by semicolons. Semicolons carry no ordinality: the reader can't count the gates, and can't tell where the list stops and the next point begins. When items are ordered, render a numbered markdown list, one per line. A genuinely separate point that follows the list stays its own paragraph, not one more clause on the run.

Before: "Run gates, in order: this must not run until the full address stack (through #490) is merged and deployed; rails-side partial-merge semantics (addresses=None clears, unset fields untouched) verified against the upsert handler; local dry run needs the TEMP_LOCATION forwarding fix for DirectRunner (currently only applied on Dataflow in run_pipeline.py). Expected volume at run time: ~82% of MixRank orgs upsert once (measured in #490), so run off-peak and watch downstream capacity."

After:

Run gates, in order:
1. this must not run until the full address stack (through #490) is merged and deployed
2. rails-side partial-merge semantics (addresses=None clears, unset fields untouched) verified against the upsert handler
3. local dry run needs the TEMP_LOCATION forwarding fix for DirectRunner (currently only applied on Dataflow in run_pipeline.py)

Expected volume at run time: ~82% of MixRank orgs upsert once (measured in #490), so run off-peak and watch downstream capacity.

## Generic coinage verbs

Appended 2026-08-11, flagged on the SUP-420 PR body. A verb coined for one mechanism spreading to every nearby claim: "reads" describing what a matcher does (`pr` reads principal, propietario, profesor) is close to literal and survives; "reads" reused to mean "is labeled" is ornament on a factual claim. Her ruling: any time "reads" is used to mean "is labeled", it is incorrect. Coinage is rarely useful when the coined word is generic, with as many possible readings as "read". Results get plain verbs.

Before: "General Manager reads Management now, not Business Development."
After: "General Manager is labeled Management now, not Business Development."

## Hanging transitive verbs

Appended 2026-08-19, flagged on the taxonomy report. A sentence ending on a transitive verb with no object: "recruiter usage governs", "they inform; they do not decide". Technically correct, but it leaves the reader waiting for the object to resolve. Give the verb its object, or recast so the sentence ends on a noun. Genuine intransitives are fine ("the mass relocates or decomposes").

Before: "Where an external taxonomy and recruiter usage conflict, recruiter usage governs."
After: "Where an external taxonomy and recruiter usage conflict, the vocabulary follows recruiter usage."

## Comma-qualified headings

Appended 2026-08-19, flagged on the taxonomy report. The "Thing, Qualified" heading: "Criteria, Applied in Order". Commas and punctuation rarely belong in a title or heading; fold the qualifier into the section's first line or cut it. Reference parentheticals like a PR number are fine.

Before: "## Criteria, applied in order"
After: "## Criteria" with "The criteria are applied in order." as the section's first line.

Her ruling on case, same date, superseding the "Title Case headings" line in the humanizer adoption above: headings and titles ARE title case. Sentence-case headings read as indie-blogger affect, not paper convention.

## Dangling conversational pronouns

Appended 2026-08-20, flagged on the Function Labeling Answers doc. In shared reply docs, "I did X" and "you counted Y" are dangling pronouns: who's who gets lost once the doc circulates past the two people in the conversation. Hanging yous are also empty and come across as accusatory. Answers state facts in passive or agentless form; quoted questions keep their original pronouns since the format attributes them.

Before: "Your 544 is a correct count of a stale artifact. I'll regenerate the workbook."
After: "The 544 is a correct count of a stale artifact. The workbook will be regenerated from the current spec."
