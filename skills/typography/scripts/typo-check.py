#!/usr/bin/env python3
"""Type-composition scan for the typography skill. Report only; never rewrites.

Flags typewriter habits that Butterick's Practical Typography (Type Composition
chapter) rules out: straight quotes, doubled spaces, hyphens faking dashes,
period ellipses, alphabetic symbol substitutes, stacked exclamation points,
hyphenated numeric ranges, the letter x as a times sign.

Prose only. Fenced code blocks, inline code, HTML tags and entities,
<script>/<style>/<pre>/<code> bodies, YAML front matter, markdown horizontal
rules and table separator rows are skipped: straight quotes and hyphens are
syntax there, not typography. To mention a wrong form on purpose, put it in
inline code.

This is a review aid, not a gate. Findings are a reader's to weigh: house
style may ban the em dash the DASH finding points toward, and a PR body may
want straight quotes around an identifier. Nothing here demands an em dash.

Usage:
    typo-check.py <file> [<file> ...]
    cat draft.md | typo-check.py -
Exit 1 when anything is flagged, 0 when clean.
"""
import re
import sys

# (code, message, compiled regex). Lexical only; judgment stays with the reader.
PATTERNS = [
    ("QUOTE", "straight double quote; “ ” (U+201C/U+201D) in prose",
     re.compile(r'(?<!\d)"')),
    ("APOS", "straight apostrophe or single quote; ’ (U+2019) or ‘ ’ in prose",
     re.compile(r"(?<!\d)'")),
    ("SPACE2", "consecutive word spaces; one space after every sentence",
     re.compile(r"(?<=\S) {2,}(?=\S)")),
    ("DASH", "hyphens standing in for a dash; – (U+2013), — (U+2014), or recast",
     re.compile(r"(?<=\S)\s*-{2,3}\s*(?=\S)|(?<=\w) - (?=\w)")),
    ("ELLIPSIS", "period ellipsis; … (U+2026)",
     re.compile(r"(?<!\.)\.{3}(?!\.)|(?<!\.)\. \. \.(?!\.)")),
    ("SYMBOL", "alphabetic symbol substitute; © ® ™",
     re.compile(r"\((?:c|C|r|R|tm|TM)\)")),
    ("BANG", "stacked exclamation points; one at most",
     re.compile(r"!{2,}|\?!|!\?")),
    ("RANGE", "hyphen in a numeric range; – (U+2013), or 'from X to Y'",
     re.compile(r"(?<![\w-])\d+(?:\.\d+)?-\d+(?:\.\d+)?(?![\w-])")),
    ("TIMES", "letter x as a multiplication sign; × (U+00D7)",
     re.compile(r"(?<=\d)\s?[xX]\s?(?=\d)")),
]

# Things that look like RANGE hits but are identifiers, not ranges.
RANGE_ALLOW = re.compile(
    r"^\d{4}-\d{2}(?:-\d{2})?$"        # ISO dates 2026-09-22, 2026-09
    r"|^\d{3}-\d{3,4}$"                 # phone fragments 555-1234
    r"|^\d{1,3}-\d{1,3}-\d{2,4}$"       # 1-800-…, 12-34-5678
)

FENCE = re.compile(r"^\s*(```|~~~)")
HRULE = re.compile(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$")
TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")
INLINE_CODE = re.compile(r"`[^`\n]*`")
HTML_BLOCK = re.compile(r"<(script|style|pre|code)\b.*?</\1\s*>", re.S | re.I)
HTML_TAG = re.compile(r"<[^>\n]+>")
HTML_ENTITY = re.compile(r"&[#\w]+;")
MASK = "\x00"   # NUL, not space: same length as the original, never matches \s or \w


def _blank(m):
    return re.sub(r"[^\n]", MASK, m.group(0))


def mask_html(text):
    """Mask tags, entities and code-bearing element bodies, preserving length and newlines."""
    text = HTML_BLOCK.sub(_blank, text)
    text = HTML_TAG.sub(_blank, text)
    text = HTML_ENTITY.sub(_blank, text)
    return text


def prose_lines(text, is_html):
    """Yield (index, masked_line) for lines that count as prose."""
    masked = mask_html(text) if is_html else text
    lines = masked.split("\n")
    i = 0
    if lines and lines[0].strip() == "---":            # YAML front matter
        try:
            i = lines.index("---", 1) + 1
        except ValueError:
            i = 0
    in_fence = False
    for n in range(i, len(lines)):
        line = lines[n]
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence or HRULE.match(line) or TABLE_SEP.match(line):
            continue
        yield n, INLINE_CODE.sub(lambda m: MASK * len(m.group(0)), line)


def scan(name, text):
    is_html = name.lower().endswith((".html", ".htm"))
    hits = []
    for n, line in prose_lines(text, is_html):
        for code, msg, rx in PATTERNS:
            for m in rx.finditer(line):
                if code == "RANGE" and RANGE_ALLOW.match(m.group(0)):
                    continue
                hits.append((name, n + 1, m.start() + 1, code, msg, m.group(0)))
    return hits


def main(argv):
    paths = argv[1:] or ["-"]
    total = 0
    for p in paths:
        text = sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()
        for name, ln, col, code, msg, frag in scan(p, text):
            total += 1
            print(f"{name}:{ln}:{col}: {code} {msg}  [{frag.strip()!r}]")
    if total:
        print(f"{total} finding(s)", file=sys.stderr)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
