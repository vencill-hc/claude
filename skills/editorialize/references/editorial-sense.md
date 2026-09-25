# Editorial sense

Taste applied as a knife, in the middle of the pass order: after humanizing cleans the language, before the voice goes on. Her scoping of the pass:

> editorializing should lend structure, clarify ideas, and sharpen arguments for the audience, but shouldn't minimize or cut the wobblieness and latitude that voicing needs to be unique

This pass decides what the piece is, whether it deserves to exist, and what shape carries the argument. It does not sand wobble; wobble is the voice pass's raw material, and an editorial pass that pre-smooths it produces beige with good bones.

## The contract with the reader

Her articulation, on why a lead-in needs a paragraph behind it:

> The caps throw an idea at you and hook the reader into following the rest of the paragraph, which does the job of convincing the reader that this is worth their precious eyes to continue.

Every opening is a promise and everything after it is payoff or breach. Edit from the reader's side of the contract: the reader owes the piece nothing.

Which is why a piece never opens on metadata. A PR that leads with "Resolves SUP-124" has spent its first and most-read line on a ticket number, and a ticket number promises the reader nothing. Lead with the bug, the cost, or the shape of the fix; the substance is the hook. Ticket ids are citations, not headlines. Footer them.

## Form must match mass

> A dropcap into a single sentence is, like, meaningless.

Ornament needs prose to anchor it. No flourish on a stub: when the structure is grander than the content, cut the structure or grow the content. PRs stay plain (house rule); drama lives where long prose lives.

## The editor's questions

Ask of every draft, in order:

1. What is the one idea? If it can't be said in a sentence, the piece isn't ready to be edited, it's still being written.
2. Is it worth the reader's eyes at all? Sometimes the verdict is: this is a table. Or a commit message. Or nothing.
3. Does every paragraph advance the idea? Cut the ones that decorate it.
4. Where would a reader start skimming? Cut what they'd skim.
5. Does it end on the last fact? No bow.

## Kill the showing-off

The "earn the seat" test, applied at this pass to structure: sections that exist to look thorough, examples that exist to display effort, headers that organize nothing. Prose ornament is the voice pass's jurisdiction and polices itself with the one-metaphor budget; do not pre-cut it here. When editing text that is already voiced (a re-revision), the test extends to lines: any line that displays craft rather than carrying the idea gets cut, especially the good ones. A kept darling reads as vanity; a cut darling reads as confidence.

## Judge the whole

Clusters, not sentences, in editing as in tell-detection. A draft is judged as a shape, promise, payoff, exit, and a piece where every individual sentence survives can still fail as a shape. When it does, restructure before polishing; polish on a bad shape is wasted.

## Standalone test for audience-facing deliverables (added 2026-07-15)

Flagged on the seniority evaluation memo. Session-internal vocabulary leaked into a
document the audience reads cold: rubric decision ids ("D6"), matcher tier codenames
("token_set"), corpus tier slang ("silver pass"), taxonomy acronyms used without
introduction (ISCO, SFIA, ESCO). The reader contract: every term either arrives
defined or does not appear. Internal codenames get translated to what they mean, not
footnoted.

Worse than the jargon: provenance inflation. A drafted intuition-first query list was
presented as "representative recruiter searches", which claims customer evidence that
does not exist. Data whose provenance is a draft, an assumption, or the team's own
intuition is labeled as exactly that, in the sentence where it is used, or it reads as
a fabricated citation the moment anyone asks where it came from.

## PR bodies (added 2026-08-11, moved same day)

The rulings from her SUP-420 edit live in the pr-body skill, which owns the form:
skeleton, cut rules, provenance carve-out, footers. One note stays here because it
touches the standalone test above: the standalone test governs documents an audience
reads cold; PR-body numbers ride on the thread and tooling the reviewer can reach, and
carry no in-body methodology. The parenthetical attitude, though, is general prose law,
not PR law: if it's not important enough to be a main-text sentence, cut it. A short
"e.g." aside is fine; supporting examples that break the flow of the prose get bullets,
charts, or supporting figures, and a precision caveat that changes no decision
compresses to notation ("~10.26%").

## Function values are double-quoted (2026-08-20)

In taxonomy-facing prose, any referenced job function value reads in double quotes ("HR management", "Sales") so the value name separates from running text; keywords keep code style so the two vocabularies stay visually distinct. Flagged on the Function Labeling Answers doc.

## Semicolons and colons (2026-09-21)

Cross-posted from the typography skill's Type Composition extraction (Butterick, *Practical Typography*, "Semicolons and Colons"). Kept here because generated prose misuses both marks, and correct use is one of the things that stops a page reading as machine output.

- A semicolon joins two complete sentences in place of a conjunction. Both sides must stand alone.
- After a subordinate clause, the mark is a comma, not a semicolon.
- When a conjunction already joins the clauses, drop the semicolon. One connector per joint.
- Semicolons separate list items that themselves contain commas ("Tulsa, Oklahoma; Flint, Michigan"). This is the one list use that survives; ordered items still go in a numbered list (banned-tells.md, semicolon-stacked ordered lists).
- A colon introduces whatever completes the idea before it. The left side sets up, the right side pays off.
- Structural semicolons are one of her voice moves (exemplars.md, the semicolon hinge). These rules bound the move; they do not retire it.

For anything beyond this, the authority is Garner's *Modern English Usage*. Cite it rather than inventing a rule.

## Sharpen, don't strip (2026-09-25)

Flagged on the Compound Title Walk artifact, after ~20 copy edits on a page that had already been editorialized. Her scoping:

> Often the first draft of an artifact has much much much too much text, but the solution isn't to just remove text, it's to sharpen the ideas so only the relevant concepts are surfaced and highlighted, to make sure the reader is trained to view the visuals with the right lens

Deletion is the wrong tool because it leaves the surviving sentences unchanged, and the surviving sentences were usually describing the visual rather than teaching how to read it. The pass is: for each sentence, name the concept it exists to surface; if the figure or the layout already surfaces it, the sentence goes; if not, rewrite the sentence until it states the mechanism in the page's own vocabulary and nothing else. What remains is the lens. The concrete checks live in artifact-narrative-review § 5b; the reader contract above (every opening a promise) is the same law applied to a page where the figures are the payoff.
