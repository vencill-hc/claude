# First run: `src/utils/seniority_utils.py`, 2026-09-29

Where the file started, where it ended, and which rulings came out of the walk between them.
Three commits on `vvencill/dat-72-73-sup-525-seniority-keywords`: 296679c, 29033f6, 74f5a12.

## Starting point (634 lines)

- Four `# === Section ===` banners (Constants, Helpers, Head position, Public API) carrying the
  structure; the compiled substitution list sat 170 lines from its source table; the segment join
  enum was filed under constants.
- Five definitions with no docstring: the lexicon row type, the segment's C-level index property,
  two small segment helpers, the parser class.
- Docstrings that were wrong: the module docstring listed the override rules out of order; the
  kind enum described board heads twice; the token enum claimed none of its members occur in
  natural titles (`pm`, `am` do); the service-tail inventory named a token `_svcs_` that does not
  exist (`svcs`); the substitution header blamed ordering on a leading-staff pattern with no
  ordering dependency.
- Twenty regex substitutions in an `OrderedDict[str, str]` with no readings; replacements mixed
  tokens, the bare string `""`, the literal `"practice lead"`, and an f-string re-inserting a
  consumed space.
- Loop variables `e`, `tok`, `i`, `m`, `n` alongside `entry`, `token`, `start`, `width`.
- The exec-only check allowed a `"&"` token that can never reach a segment.
- `_Segment.cxo_index` typed `int | None` and used in arithmetic at five sites: seven pyright
  errors nobody had run pyright to see.

## Ending point (627 lines)

- Order: five vocabulary types, every constant table, two dataclasses, fourteen functions, the
  parser class. No banners.
- Every definition documented; the wrong ones corrected.
- The substitution table is `list[_Sub]` with `reads`, `pattern`, `token: _Token` in aligned
  columns under `# fmt: off`; the two ordering constraints stated once in the header; no row
  comments; two new tokens (`EMPTY`, `PRACTICE_LEAD`); the staff prefix is a lookahead.
- `has_cxo` (bool) for the search, `cxo_index` (int) for the rules; pyright 0 errors.
- 153 tests unchanged across every commit.

## The presentation walk on the substitution table

| Step | Form | Her verdict |
|---|---|---|
| 1 | A comment above every regex row | "as equally unhelpful as having none" |
| 2 | One comment per group of rows | Grouping fights declaration order |
| 3 | `_Sub(reads, pattern, token)` rows, aligned, with a few row comments left | "why do we still have the # comments" |
| 4 | Same, no row comments, terse readings ("CxO family", "Staff prefix") | Readings still carried `…` |
| 5 | One argument per line via magic trailing commas | "I hate the expanded version" |
| 6 | Flat single-line rows, ruff spacing | Wanted the columns back |
| 7 | Aligned columns under `fmt: off`, plain readings, HRBP spelled out | Accepted |
| 8 | Same alignment applied to the 102-row lexicon | Reverted: columns are for regex tables only |

## Rulings that came out of it

- Row comments earn their place only for a decision the code can't show; ordering goes in the
  header once; ticket rationale lives with the tests.
- Every replacement in a substitution table is a typed token.
- A style pass ends with pyright, not just ruff and tests.
- Fixes to an unpushed commit are squashed into it; the rebase will conflict where later commits
  rewrote the file, and the resolution is "take the replayed commit's file, re-apply the fix".
