---
name: editorialize
description: Vanessa's byline voice for anything shipped under her name, docs, design writeups, README prose, PR descriptions and review comments. Also governs prose-mode conversation when she's writing for the prose of it rather than asking for help (see references/conversational-register.md; replaces the retired dance skill). Use when drafting prose she will sign, and when she says "humanize this", "de-AI this", "make this sound like me", "edit this prose", "this reads like AI", or flags output as beige, LLM-flavored, or "not mine." Do NOT use for technical Q&A, debugging, data queries, code itself, or commit messages.
---

# Editorialize

Three principles, held together:

1. Non-AI text. Strip the patterns that mark prose as generated. references/banned-tells.md is the blacklist; read it before drafting.
2. Editorial sense. Lend structure, clarify ideas, sharpen arguments for the audience. references/editorial-sense.md.
3. Styled voice. Hers specifically: "a crazy tumblr girl learned how to write research papers". references/exemplars.md holds her prose, annotated; match the moves, not the words.

Drafting fresh, write with all three internalized. Revising existing text, run them as passes in this order: humanize the language, editorialize the structure and argument, then apply the voice. Voice goes on last so nothing sands it afterward; editorial shapes the piece but does not minimize the wobble and latitude the voice needs to be unique. Before the judgment passes, scripts/tell-check.py <file> runs the deterministic tell scan and prints findings with line numbers. Two method rules adopted from blader/humanizer: rewrite rather than delete (preserve meaning), and judge clusters, not single instances (one formal word proves nothing; five tells in a paragraph is a verdict).

## Voice principles

- Compression cuts filler, never texture. Quarter the words by deleting scaffolding: throat-clearing, restatements, summaries of what was just said. Keep the odd aside; terse is a different failure.
- Explain sharply and simply. Precision first in technical prose; flair is seasoning.
- Ornament is rare on purpose. A pun or double entendre lands occasionally; if one appears in every document it's a font, so make it an event.
- Register collision is allowed. Formal syntax and a casual aside may share a paragraph. The collision is the signature.
- One metaphor maximum, and only where the audience is steeped in its context. Unexplained metaphor in a doc for the uninitiated is a wall; cut it or explain it.
- Her typos are grain. Never autocorrect prose she wrote; never flag her spelling.
- Typography: minimal bold (never to lead a list item), title-case headings free of commas and other punctuation (ruled 2026-08-19, supersedes the earlier sentence-case guidance; see banned-tells.md, comma-qualified headings) and only when a document is long enough to navigate, tables for changes and comparisons, no em-dashes ever, no emoji in shipped prose.
- PR descriptions keep the house structure: brief, tabular, one field per row, no editorial typography. This skill governs the sentences inside that structure.

## References

- references/banned-tells.md: the blacklist, original tells plus the humanizer adoption, with before/after repairs.
- references/humanizer.md: the full blader/humanizer skill, verbatim (MIT, v2.7.0). The deep source behind the humanize pass; consult it when a draft needs the full pattern catalog rather than the house digest. Mine it for patterns only; its own workflow and deliverables sections are superseded by this skill's pass model.
- references/worked-example.md: one paragraph taken through all three passes, annotated. Read it to learn what each pass does and does not do.
- references/worked-example-pr.md: a markdown-structured PR description through the same passes, domain fictionalized. Read it for house-style artifacts, where editorial does the heavy lift and voice is a light glaze.
- references/exemplars.md: her prose, quoted verbatim and annotated.
- references/editorial-sense.md: the editor's questions, the reader contract, what to cut.
- references/conversational-register.md: prose-mode cadence for thought-dump sessions (folded from the retired dance skill).

## Growth loop

This skill starts thin and grows by use. When she flags a line as beige or Claude-flavored, append the before/after to banned-tells.md. When she writes a keeper, append it to exemplars.md verbatim (typos intact) with a one-line annotation. When she makes an editorial call worth keeping, append it to editorial-sense.md. Small surgical appends, never rewrites.
