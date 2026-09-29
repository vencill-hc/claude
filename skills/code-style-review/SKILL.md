---
name: code-style-review
description: Full-pass readability review of one source file - organization, docstrings, naming, comments, regex and table presentation - gated by ruff + pyright + tests and shipped as phase-scoped commits. Use on "style review", "full pass revision", "is this file well organized", "review the docstrings", "clean up this module", or after a refactor lands and before the PR goes back to reviewers. Not for bugs (code-review), over-engineering (ponytail-review), or PR-wide review (pr-code-review).
---

# Code Style Review

A readability pass over one file, in one sitting, driven by the checklist below. Behavior never
changes; the tests are the proof. First run: `seniority_utils.py`, 2026-09-29, see
`references/seniority-utils-2026-09-29.md` for the starting point and where it ended.

## Baseline first

Run the file's tests (`make tests TESTS=...`), `ruff check`, and `pyright <file>` before touching
anything. Record the counts; the report quotes them.

## The checklist (her questions, in her order)

1. **Organization.** Types the constants need, then constants, then classes, then functions, then
   the public entry point last. No `# === Section ===` banners; the order carries the structure.
   Python forces the enums and row types above the tables that reference them at import time.
2. **Docstrings.** Every function, class and property has one. Correct before complete: read each
   against the code and fix the wrong ones first (rule order, a member described twice, a claim
   about what tokens occur naturally).
3. **Names.** Verbs for functions, questions for booleans, no adjectives. Shared names match the
   sibling modules (`_COMPILED_NORMALIZE_SUBS` as in `board_seat_utils`). Loop variables are
   consistent across the file (`entry`, `token`, `start`, `width`; never `e`, `tok`, `i`, `m`).
4. **Comments.** A comment that restates the code goes. What stays: an ordering constraint, said
   once in the header; a decision the code cannot show. Ticket rationale (DAT-72, the ruling date)
   lives in the tests that pin the titles, not in the table.
5. **Regex.** Every pattern compiled once at module load. Every table of regex presented as typed
   rows (next section). A single regex keeps the what-then-inventory comment.
6. **Dead branches** found while reading are removed and named in the report (the `"&"` allowance
   in the exec-only check could never fire because `&` is always a separator).

## Regex tables are typed rows in aligned columns

The ladder she walked and where it stopped: per-row comments (restate the regex) → group comments
(fight declaration order) → **typed row, three aligned columns**.

```python
class _Sub(t.NamedTuple):
    """A token substitution rule: the phrase, its regex, and its _Token substitution."""

    reads: str
    pattern: str
    token: _Token


# fmt: off
_NORMALIZE_SUBS: list[_Sub] = [
    _Sub("Chief Anything Officer",  r"chief\s[\w\s&]*\sofficer",                    _Token.CXO),
    _Sub("Chief of Staff and tail", r"chief of staff.*",                            _Token.COFS),
    _Sub("CxO family",              r"\b(?:ceo|cfo|coo|cto|cso|cmo|cdo|cpo|cio|ciso)\b", _Token.CXO),
    _Sub("Staff prefix",            r"^staff(?=\s)",                                _Token.STAFF_PFX),
    _Sub("HR Business Partner",     r"\bhrbp\b",                                    _Token.BIZ_PARTNER),
]
# fmt: on
```

- **Readings** are plain words: no ellipses, acronyms spelled out, the usual phrase rather than
  the regex's full reach (the header says the regex also takes neighbours). Short enough that
  every row stays under 120 columns; `ruff check` E501 still applies inside `fmt: off`.
- **Every replacement is a typed token**, including the empty string (`_Token.EMPTY`) and a
  rewrite to plain words (`_Token.PRACTICE_LEAD`). A pattern that consumed whitespace only to
  re-insert it (`^staff\s+` → `f"{tok} "`) becomes a lookahead (`^staff(?=\s)`).
- **No comments inside the list.** Ordering constraints go in the header once.
- **Columns are for regex tables only.** A lexicon of plain tuples stays ruff-formatted; she
  reverted that alignment the same day.
- **Rejected forms, don't re-offer:** one argument per line, flat unaligned rows, `…` in readings,
  abbreviations in readings, a comment per row.

## Gate

`ruff format`, `ruff check`, `pyright <file>`, tests. pyright is not optional: the first run
skipped it and seven Optional-operand errors rode through two commits until she read line 551.

## Commits

One commit per phase, each green on its own: extract functions, docstrings and organization,
file reorder. A fix to a commit that is still unpushed is squashed into it (`git commit --fixup
<sha>`, then `GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash --autostash <sha>~1`). Later
commits that rewrote the file will conflict on replay: take the replayed commit's own file
(`git checkout --theirs`), re-apply the fix, verify, continue. Confirm the final tree matches the
pre-squash tip (`git diff <old-tip> HEAD`). Unrelated working-tree edits stay unstaged and out of
every commit.

## Report

Before and after in the checklist's order, one line each. What was removed and why. The
verification counts. Then the commit list and what remains unstaged.
