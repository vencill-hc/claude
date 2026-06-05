# Worked example: paragraph

One paragraph through the three passes, in order: humanize, editorialize, voice. The draft is a design-doc opening in default LLM register, seeded with tells on purpose; it is the specimen, not the standard. For markdown-structured artifacts, see worked-example-pr.md.

## Stage 0, the beige draft

> In today's rapidly evolving data landscape, entity resolution serves as a crucial cornerstone of our data platform. It's not just about matching records—it's about building a comprehensive, robust foundation for downstream consumers. This document delves into the key challenges and explores potential solutions, highlighting the importance of a unified approach. Let's dive in.

55 words. Tells: undue-significance opener, copula avoidance ("serves as"), negative parallelism with an em dash, five AI-vocabulary words, a superficial -ing clause, signposting close.

## Stage 1, humanized

Strip the tells, preserve the meaning, rewrite rather than delete (banned-tells.md; humanizer.md for the full catalog).

> Entity resolution is the foundation of our data platform. A correct merge decision determines what every downstream consumer sees. This document describes where our merges go wrong and proposes fixes.

30 words. Clean, accurate, and anyone's. The floor, not the finish.

## Stage 2, editorialized

The editor's questions (editorial-sense.md). The one idea: wrong merges propagate, invisibly, everywhere. The first sentence is throat-clearing for an internal audience that already knows what entity resolution is. Lead with the cost.

> Every downstream consumer inherits a wrong merge, quietly, at scale. This doc names where our merges go wrong and what each fix costs.

23 words. Structure is set: hook first, payoff promised. Still anyone's prose; editorial shaped the argument and left the language plain on purpose.

## Stage 3, voiced

Apply her moves (exemplars.md): one minted phrase spent in-sentence, precision kept. The structure already made room at the front, so the ornament lands as thesis, and no later pass exists to sand it off.

> A bad merge is a lie with excellent distribution: every downstream consumer inherits it, quietly, at scale. This doc names where our merges go wrong and what each fix costs.

30 words, just over half the original draft, and the original was already short; real documents shed more.

## What to notice

- Each pass has a distinct job. Humanize fixed the language without adding anything. Editorial cut a sentence the audience didn't need and put the hook first, working on clean anonymous material with no ornament to mis-judge. Voice painted last, on sound structure.
- The order is the protection. Voice after editorial means the minted phrase survives; editorial after voice would have had to decide whether to keep it, and the knife always takes some paint.
- Stage 1 and stage 3 land near the same word count with entirely different value. Compression alone gets you clean and forgettable; the editorial and voice passes are the difference.
