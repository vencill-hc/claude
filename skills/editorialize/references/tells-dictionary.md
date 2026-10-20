# Tells dictionary

Single words and phrases that mark prose as Claude's, one entry per term, modeled on the Claudish dictionary (programasweights.com/claudish/dictionary). Augments banned-tells.md, which keeps the constructions and house rulings. scripts/tell-check.py flags the pattern of every active entry; `tell-check.py --self-test` checks that each pattern matches its Before line and misses its After line.

Entries are appended, never rewritten. To unban a term, set its status to inactive with the reason in parentheses; to ban it again, set it back to active. Inactive entries stay as the record of what was ruled acceptable, and they keep their patterns so the switch works both ways.

Fields, in order:
- the heading: the term as Claude writes it
- status: active or inactive, then added date and source, separated by middle dots
- also: variants the pattern catches (optional)
- pattern: a case-insensitive regex in backticks (optional; no pattern means judgment only)
- Means: the plain definition
- Misuse: how Claude uses it
- Instead: what to write
- Before / After: a repair pair (optional, but the self-test needs it)

## load-bearing
status: active · added: 2026-10-09 · source: claudish; also the consultant lexicon in banned-tells.md
also: load bearing, load-bearing assumption, load-bearing invariant
pattern: `\bload[- ]bearing\b`

Means: so important that everything else depends on it.
Misuse: a wall term applied to any code, rule, assumption, or argument Claude wants to sound essential. It asserts the importance and skips what depends on it.
Instead: say what breaks if it changes.

Before: "The checksum is the load-bearing invariant in this flow."
After: "This process only works if the checksum stays the same."

## the honest shape
status: active · added: 2026-10-09 · source: claudish
pattern: `\bhonest shape\b`

Means: the real situation, stated plainly.
Misuse: a candor frame before a blunt summary, usually when something only partly works. Flagging one sentence as honest implies the others weren't.
Instead: delete the frame and state the fact.

Before: "The honest shape is asymmetric: reads work; writes do not."
After: "Reads work, but writes don't."

## one honest caveat
status: active · added: 2026-10-09 · source: claudish
also: honest caveat
pattern: `\bhonest caveat\b`

Means: one limitation the reader should know about.
Misuse: the same candor frame, placed before an admission that something doesn't fully work.
Instead: state the limitation.

Before: "One honest caveat: rollback works only before cleanup."
After: "Rollback works only before cleanup."

## that's not nothing
status: active · added: 2026-10-09 · source: claudish
also: that is not nothing
pattern: `\bthat(?:'?s| is) not nothing\b`

Means: a small but real success.
Misuse: a consolation line after a partial result, softening the news that the problem isn't solved.
Instead: say what the result does and what remains.

Before: "The probe found one valid lead. That's not nothing."
After: "The check found one useful lead. The problem isn't solved yet."

## you're right to push back
status: active · added: 2026-10-09 · source: claudish
also: you are right to push back
pattern: `\bright to push back\b`

Means: the correction was right.
Misuse: a formal acknowledgment before Claude revises an answer it got wrong. It grades the objection instead of fixing the error.
Instead: the corrected fact, with "You're right" in front at most.

Before: "You're right to push back: the cache isn't authoritative."
After: "The cache isn't the official source."

## belt-and-suspenders
status: active · added: 2026-10-09 · source: claudish
also: belt and suspenders, belt-and-braces
pattern: `\bbelt[- ]and[- ](?:suspenders|braces)\b`

Means: a second safeguard in case the first one fails.
Misuse: the idiom stands in for a description of what the second check catches.
Instead: name what the extra check catches.

Before: "The second guard is a belt-and-suspenders check."
After: "The second guard catches anything the first one misses."

## durable path forward
status: active · added: 2026-10-09 · source: claudish
also: durable fix, durable solution
pattern: `\bdurable (?:path|fix|solution)\b`

Means: a solution meant to last.
Misuse: promises longevity without saying how long or what could break it.
Instead: say what it fixes for good and what it leaves open.

Before: "This gives us a durable path forward."
After: "This gives us a longer-term solution."

## substrate
status: active · added: 2026-10-09 · source: claudish
pattern: `\bsubstrate\b`

Means: whatever runs underneath a feature.
Misuse: a broad name for a database, log, service, or anything else behind the scenes, so the reader can't tell which.
Instead: name the component.

Before: "The event log is the durability substrate."
After: "The event log is what keeps the data from being lost."

## spine
status: active · added: 2026-10-09 · source: claudish
also: the spine of
pattern: `\bspine\b`

Means: the central structure that organizes the rest.
Misuse: an anatomy metaphor for whatever Claude considers central, often stacked with another ("the load-bearing spine").
Instead: say what it organizes or connects.

Before: "The queue is the spine of the deployment flow."
After: "The queue organizes the deployment process."

## seam
status: active · added: 2026-10-09 · source: claudish
also: seams
pattern: `\bseams?\b`

Means: where two parts of a program connect.
Misuse: a sewing metaphor for an interface or integration point.
Instead: name the two parts and where they meet.

Before: "Keep the parsing seam explicit."
After: "Make it clear where the parser connects to the rest of the program."

## cadence
status: active · added: 2026-10-09 · source: claudish
also: daily cadence, weekly cadence, regular cadence
pattern: `\b(?:daily|weekly|hourly|nightly|monthly|regular) cadence\b`

Means: how often something happens.
Misuse: "a daily cadence" where "every day" is shorter. Cadence as prose rhythm, the way this skill uses it, is fine and not matched.
Instead: every day, weekly, on a schedule.

Before: "Run the check on a daily cadence."
After: "Run the check every day."

## shape
status: active · added: 2026-10-09 · source: claudish
also: right shape, wrong shape, same shape, response shape, change shape, shape of the problem
pattern: `\b(?:right|wrong|same|response|change) shape\b|\bshape of the (?:problem|change|fix)\b`

Means: how something is organized or what form it takes.
Misuse: a catch-all for format, scope, structure, or kind. The shape of a distribution is statistics and is not matched.
Instead: format, structure, scope, or kind, whichever is meant.

Before: "The response has the right shape."
After: "The response is formatted correctly."

## thread / wire / plumb through
status: active · added: 2026-10-09 · source: claudish
also: threaded end-to-end, plumbed through, wired through
pattern: `\b(?:thread|plumb|wire)(?:s|d|ed|ing)? (?:end-to-end|through)\b`

Means: pass something through every part that needs it.
Misuse: plumbing and sewing metaphors for "every layer now receives X", without naming the layers.
Instead: say which parts now receive it.

Before: "The timeout is threaded end-to-end through every layer."
After: "Every part of the program now receives the timeout setting."

## hard X
status: active · added: 2026-10-09 · source: claudish
also: hard stop, hard gate, hard boundary, hard constraint
pattern: `\bhard (?:stop|gate|boundary|constraint)\b`

Means: a rule that cannot be ignored.
Misuse: "hard" as an intensifier on gate, stop, or boundary, instead of saying what happens when the rule trips.
Instead: state the rule as an instruction.

Before: "A signature mismatch is a hard stop."
After: "Stop if the signatures don't match."

## surfaced
status: active · added: 2026-10-09 · source: claudish
also: surfacing
pattern: `\bsurfac(?:ed|ing)\b`

Means: found or revealed.
Misuse: the all-purpose finding verb. A check surfaces a problem, or a problem just surfaces, and nobody is said to have found it. Surface as a noun (attack surface, API surface) is not matched.
Instead: found or showed, with who or what found it.

Before: "The probe surfaced a configuration mismatch."
After: "The check found that the settings don't match."

## cleanly
status: active · added: 2026-10-09 · source: claudish
pattern: `\bcleanly\b`

Means: without obvious errors.
Misuse: a loose reassurance on a migration, test, or change that names no check.
Instead: name the check that passed, or cut the word.

Before: "The migration landed cleanly."
After: "The migration finished without any obvious problems."

## coherent
status: active · added: 2026-10-09 · source: claudish
also: coherence
pattern: `\bcoheren(?:t|ce)\b`

Means: internally consistent.
Misuse: the same loose reassurance applied to files, plans, or systems, with no check named.
Instead: name the check, or cut the word.

Before: "Both snapshots are coherent and hash-verified."
After: "Both saved versions passed the file-integrity check."

## gated on
status: active · added: 2026-10-09 · source: claudish
also: X-gated, owner-gated, approval-gated, quality-gated
pattern: `\bgated on\b|\b\w+-gated\b`

Means: blocked until a requirement is met.
Misuse: compound gates (owner-gated, quality-gated) that hide who or what does the unblocking.
Instead: fine for engineers. For PM or client readers, "can't X until Y".

Before: "Deployment is gated on CI."
After: "We can't deploy until the automated checks pass."

## provenance
status: active · added: 2026-10-09 · source: claudish
also: lineage
pattern: `\bprovenance\b|\blineage\b`

Means: where a piece of data came from and how it changed on the way.
Misuse: a noun that turns "we don't know where this came from" into a property the data lacks.
Instead: fine for engineers. For PM or client readers, say where it came from or that nobody knows.

Before: "The cache entry lacks provenance."
After: "We don't know where this cached value came from."

## canonical
status: active · added: 2026-10-09 · source: claudish
also: source of truth, authoritative
pattern: `\bcanonical\b|\bsource of truth\b`

Means: the version everyone should treat as official.
Misuse: used where there is only one version, so nothing needed ranking.
Instead: fine where several copies exist. For PM or client readers, "official".

Before: "Read from the canonical manifest."
After: "Use the official manifest."

## landed
status: active · added: 2026-10-09 · source: claudish
also: has landed, have landed
pattern: `\b(?:has|have|had) landed\b`

Means: merged into the codebase.
Misuse: stretched to anything finished, including deploys and migrations that were never merges.
Instead: merged, deployed, or finished, whichever happened.

Before: "The fix has landed."
After: "The fix was merged."

## drift
status: active · added: 2026-10-09 · source: claudish
also: drifted, schema drift, configuration drift, behavioral drift
pattern: `\bdrift(?:s|ed|ing)?\b`

Means: two things that used to match no longer do.
Misuse: used without saying what the thing drifted from.
Instead: fine for engineers with the reference named. For PM or client readers, "no longer matches".

Before: "The generated file has drifted from the schema."
After: "The generated file no longer matches the expected format."

## blast radius
status: active · added: 2026-10-09 · source: claudish
pattern: `\bblast radius\b`

Means: what a failure or change could affect.
Misuse: applied to ordinary code changes, where nothing was counted.
Instead: the count of what is affected, when it was measured. For PM or client readers, "it will affect fewer things".

Before: "This keeps the migration's blast radius narrow."
After: "If the migration goes wrong, it will affect fewer things."

## fail closed
status: active · added: 2026-10-09 · source: claudish
also: fails closed
pattern: `\bfails? closed\b`

Means: block the action when a check fails or gives no answer.
Misuse: precise among engineers; Claudish only when the reader doesn't know the term.
Instead: for PM or client readers, "block the request".

Before: "If verification times out, fail closed."
After: "If the check times out, block the request."

## boundary
status: active · added: 2026-10-09 · source: claudish
also: ownership boundary, trust boundary, serialization boundary
pattern: `\b(?:ownership|trust|serialization) boundar(?:y|ies)\b`

Means: where one part's job ends and another's begins.
Misuse: "keeps the boundary clean" as a stand-in for saying which part does what.
Instead: say which part is responsible for what.

Before: "This keeps the ownership boundary clean."
After: "This keeps each part responsible for its own work."

## wedged
status: active · added: 2026-10-09 · source: claudish
also: wedge, wedges
pattern: `\bwedge[sd]?\b`

Means: stuck, or making something else stuck.
Misuse: precise among engineers; opaque to anyone else.
Instead: for PM or client readers, "stuck" or "stops processing".

Before: "A stalled worker can wedge the queue."
After: "A stuck worker can stop the queue from processing new jobs."

## contract
status: active · added: 2026-10-09 · source: claudish
also: preserve the contract, existing contract
pattern: `\b(?:preserves?|breaks?|keeps?) the (?:existing )?contract\b`

Means: a promise about how a piece of software behaves.
Misuse: "preserves the contract" where no formal contract exists.
Instead: "won't break existing code", or name the behavior callers rely on.

Before: "The fallback preserves the existing contract."
After: "The backup behavior won't break existing code."

## anchored
status: active · added: 2026-10-09 · source: claudish
also: anchor
pattern: `\banchored (?:to|on)\b`

Means: based on a fixed reference point.
Misuse: a metaphor where "compared against" says the same thing.
Instead: name the reference and the comparison.

Before: "The comparison is anchored to the signed release."
After: "Use the signed release as the version to compare against."

## byte-identical
status: active · added: 2026-10-09 · source: claudish
also: byte for byte, byte-for-byte identical
pattern: `\bbyte[- ](?:identical|for[- ]byte)\b`

Means: every byte of the two files matches.
Misuse: precise when a byte comparison actually ran; otherwise it overstates the check.
Instead: keep it when the bytes were compared. For PM or client readers, "exactly the same".

Before: "Both artifacts are byte-identical."
After: "The two files are exactly the same."

## freeze the binding
status: inactive (binding is a Data Universe term) · added: 2026-10-09 · source: claudish
also: frozen binding
pattern: `\bfreeze the \w+ binding\b|\bfrozen binding\b`

Means: keep a choice or connection from changing.
Misuse: jargon for "don't change which X it uses".
Instead: say what must stay fixed.

Before: "Freeze the compiler binding."
After: "Don't change which compiler the program uses."

## X-shaped
status: active · added: 2026-10-09 · source: claudish
also: credential-shaped, report-shaped
pattern: `\b\w+-shaped\b`

Means: looks or behaves like X, but may not be X.
Misuse: attached to every noun. Once is a coinage; on every noun it's a tell.
Instead: spend it where the resemblance is the point.

Before: "The string is credential-shaped."
After: "The string looks like a credential but may not be valid."

## what lands
status: active · added: 2026-10-20 · source: VV, on the HelloSky Linear ticket drafts (pr-body table header "Piece / What lands")
also: lands in, lands on, lands with, landing
pattern: `\bwhat lands\b|\blands? (\w+ )?(in|on|with|behind|as)\b|\blanding (shape|step)\b`

Means: arrives, is delivered, is merged, is written to a table.
Misuse: one coinage verb standing in for ship, merge, write, deliver, add and schedule, so a reader cannot tell which one happened. As a table header ("What lands") it names nothing: a scope table lists deliverables, a change table lists changes.
Instead: the plain verb for the event. Header a scope table "Deliverable" or "Change". Aviation and Beam senses stay ("the file is landed in the bucket" is pipeline vocabulary; use it for that only).

Before: "This ticket ports the crawler and lands it as the source of the ingestion job."
After: "This ticket ports the crawler and makes it the source of the ingestion job."
