# Reviewer taste

What the data-universe-pipelines reviewer keeps asking for, quoted from the
PRs where he asked. Each ask became a rule. A draft that violates one will get
the same comment again, so read this before writing comments, docstrings,
tests, or the PR body, not only at review time.

## 1. Comments carry the nuance of the term, never its provenance

The most repeated ask, four PRs running.

> "There are a bunch of mentions to EZ in this file that I don't love. EZ
> provided us input, but IMO they should not actually make their way into our
> code like this." (#587, `job_function_taxonomy.py`)

> "Comments about the distinction between things like `credit` and
> `commercial credit` are valuable, but not that EZ is a driver of them (nor
> the date in question for the resolution)." (#588, `job_function_taxonomy.py`)

> "Let's axe the dates here and instead just explain the distinction." (#608,
> `job_function_taxonomy.py:620`)

> "Let's try to avoid denoting review dates, which on their own aren't
> material. What is important to have as a docstring / code comment is the
> nuance that isn't clear from the lists themselves." (#608,
> `job_function_taxonomy.py:1045`)

Rule: a comment says what the distinction is. Who decided it, when, in which
session, on whose ruling, all belong in the commit message or the PR body.
Customer names never appear in code: "these are decisions we're agreeing to,
that affect all customers of the DU" (#587). The `publish-gate` hook refuses a
push whose added comments carry a date, a person, the customer, or the words
ruling / ruled / HITL / workpod.

## 2. Test comments are minimal; parentheticals go

> "I'd kill the comments here altogether." (#588, `test_job_types.py:110`)

> "Here too, I would remove the parenthetical." (#588, `test_job_types.py:95`)

> "Last one, let's strip the comments of their EZ ruling details and leave just
> the nuance of the term itself." (#588, `test_job_function_taxonomy.py`)

Rule: a test's name and its assertion are the documentation. A comment on a
test row earns its place only when the expected value would surprise a reader
without it, and then it is one clause, no parenthetical.

## 3. Scaffolding does not ship

> "I'm not sure this file + the related headcount vote fixture file are really
> necessary to be committed / maintained over time. As long as we have tests
> for the actual functionality difference, I'm not seeing it as necessary that
> we hard-coded this one-time export." (#602, `test_organization_utils_vote_parity.py`)

> "Hmm... I'm not sure I follow the need for this test. How is it different
> from our more explicit unit tests?" (#608, `test_job_function_golden.py`)

Rule: anything whose purpose was "help me while I build" (a golden snapshot, a
parity fixture, a one-time export, a measurement harness) stays in the workpod
thread or the measurement-tools repo. What ships is a test of the functional
difference, written as an explicit unit test. Before publishing, ask of every
new test file: would this exist if the change had been written in one sitting?

## 4. Code reads for humans, no coinage

> "This function looks like gibberish to me. I'm sure it works, given the test
> coverage, but is there any way to improve readability / comprehension for us
> human readers?" (#615, `seniority_utils.py:477`)

> "I'm not a fan of the terminology used here ("hatch"), nor do I like the
> repetition / presentation of "General X role"." (#569, `job_function_taxonomy.py:986`)

Rule: a dense function gets decomposed into named steps before it ships, and
the names are plain English behaviour, not house coinage. If a reviewer would
need the workpod to decode a word, the word does not go in.

## 5. A surprise in the diff gets a sentence in the body

> "What exactly does this do?" (#608, `employment_utils.py:592`, on an
> `lru_cache` decorator in a labeling PR)

Rule: any commit that is not the PR's headline (a perf change in a labeling
PR, a refactor beside a fix) gets one sentence in the body saying why it is in
this PR at all, and the code line it lands on gets a comment that says what it
does in place, not three lines above on a constant.

## 6. Our taxonomy, not the customer's

> "This is *our* mapping + ontology, not EZ's." (#588, `job_types.py`)

> "The Job Function Taxonomy document seems like the furthest into our repo /
> code that they should get." (#587)

Rule: customer input shapes the decision; the decision is ours. The docs
ruling table is the one place provenance lives, and even there the customer is
named as a source, not as the authority.
