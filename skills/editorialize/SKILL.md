---
name: editorialize
description: Vanessa's byline voice for anything shipped under her name, docs, design writeups, README prose, and review comments (PR bodies have their own skill, pr-body, which layers on this one). Also governs prose-mode conversation when she's writing for the prose of it rather than asking for help (see references/conversational-register.md; replaces the retired dance skill). Use when drafting prose she will sign, and when she says "humanize this", "de-AI this", "make this sound like me", "edit this prose", "this reads like AI", or flags output as beige, LLM-flavored, or "not mine." Do NOT use for technical Q&A, debugging, data queries, code itself, or commit messages.
---

# Editorialize

Three principles, held together:

1. Non-AI text. Strip the patterns that mark prose as generated. references/banned-tells.md is the blacklist; read it before drafting.
2. Editorial sense. Lend structure, clarify ideas, sharpen arguments for the audience. references/editorial-sense.md.
3. Styled voice. Hers specifically: "a crazy tumblr girl learned how to write research papers". references/exemplars.md holds her prose, annotated; match the moves, not the words.

Drafting fresh, write with all three internalized. Revising existing text, run them as passes in this order: humanize the language, editorialize the structure and argument, then apply the voice. Voice goes on last so nothing sands it afterward; editorial shapes the piece but does not minimize the wobble and latitude the voice needs to be unique. Before the judgment passes, scripts/tell-check.py <file> runs the deterministic tell scan and prints findings with line numbers. Two method rules adopted from blader/humanizer: rewrite rather than delete (preserve meaning), and judge clusters, not single instances (one formal word proves nothing; five tells in a paragraph is a verdict).

The voice pass has two halves, and the second is the one usually skipped. First the lexical half: her diction and moves (the words). Then the rhythmic half: match the cadence of the register's exemplar passage, not just its vocabulary. Vocabulary without rhythm is the common failure, right words, wrong breath. Pick the point on the register dial first (below), then match that passage's sentence-length sequence and the shape of its close. Read the draft for cadence: where does the breath land, does it end on a short hard sentence or trail into one. References/exemplars.md annotates passages for exactly this.

## The register dial

Her technical writing rides one axis: paper-abstract on one end, magazine-exposé on the other. Both are hers. The abstract end is methodological, impersonal, passive-tolerant, ornament near zero, the default for reference docs and schema notes and anything where the content is code or fact. The exposé end is proseful, voiced, active, a reference or coinage carrying an argument, the default for essays and design writeups. Pick the point per artifact before voicing, and let it slide within a piece: a paragraph of flat exposition can end on one exposé-end hit. Passive at the abstract end is correct, not a tell (banned-tells.md splits evasive from methodological passive). References/exemplars.md sorts the specimens along this dial.

## Voice principles

- Sparsity governs everything below. The moves are seasoning, not the dish. Most sentences are plain; a hit per paragraph or so, and it lands because of the flat prose around it. Saturate the text with coinage, metaphor, register collision, and long breath-sentences all at once and it reads like a student straining to sound impressive. The ornament budget covers every move, not just metaphor.
- Compression cuts filler, never texture. Quarter the words by deleting scaffolding: throat-clearing, restatements, summaries of what was just said. Keep the odd aside; terse is a different failure.
- Explain sharply and simply. Precision first in technical prose; flair is seasoning. At the abstract end of the dial, precision is the whole job and flair stays in the drawer.
- Ornament is rare on purpose. A pun or double entendre lands occasionally; if one appears in every document it's a font, so make it an event.
- Rhythm is a move, not a byproduct. The long comma-stacked breath landing on a short hard close, the sentence-length sequence, the fragment that ratifies a paragraph: these are deliberate and they are matched from the exemplar passages, not improvised.
- Register collision is allowed. Formal syntax and a casual aside may share a paragraph. The collision is the signature.
- One metaphor maximum, and only where the audience is steeped in its context. Unexplained metaphor in a doc for the uninitiated is a wall; cut it or explain it.
- Her typos are grain. Never autocorrect prose she wrote; never flag her spelling.
- Typography: minimal bold (never to lead a list item), title-case headings free of commas and other punctuation (ruled 2026-08-19, supersedes the earlier sentence-case guidance; see banned-tells.md, comma-qualified headings) and only when a document is long enough to navigate, tables for changes and comparisons, numbered lists for ordered or sequential items and bullets for unordered sets (never semicolon-stacked into one sentence), no em-dashes ever, no emoji in shipped prose.
- PR bodies have their own skill (pr-body), which owns the structure and the cut rules; this skill still governs the sentences inside it, at the abstract end of the dial.

## References

- references/banned-tells.md: the blacklist, original tells plus the humanizer adoption, with before/after repairs.
- references/humanizer.md: the full blader/humanizer skill, verbatim (MIT, v2.7.0). The deep source behind the humanize pass; consult it when a draft needs the full pattern catalog rather than the house digest. Mine it for patterns only; its own workflow and deliverables sections are superseded by this skill's pass model.
- references/worked-example.md: one paragraph taken through all three passes, annotated. Read it to learn what each pass does and does not do. (The PR worked example moved to the pr-body skill.)
- references/exemplars.md: her prose, quoted verbatim and annotated.
- references/editorial-sense.md: the editor's questions, the reader contract, what to cut.
- references/conversational-register.md: prose-mode cadence for thought-dump sessions (folded from the retired dance skill).

## Growth loop

This skill starts thin and grows by use. When she flags a line as beige or Claude-flavored, append the before/after to banned-tells.md. When she writes a keeper, append it to exemplars.md verbatim (typos intact): prefer a full passage tagged by register and annotated on rhythm, dosage, and move over a bare one-liner, since the passages are what teach cadence and restraint. Her blog (`blog/content/`) is the standing corpus to harvest from. When she makes an editorial call worth keeping, append it to editorial-sense.md. Small surgical appends, never rewrites.
