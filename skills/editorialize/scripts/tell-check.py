#!/usr/bin/env python3
"""Deterministic tell scan for the editorialize skill.

Flags banned constructions from references/banned-tells.md, and the active
terms of references/tells-dictionary.md, with line numbers.
A first pass only: single hits prove nothing, clusters convict. The judgment
passes (voice, editorial) still happen after this.

Usage:
    tell-check.py <file> [<file> ...]
    cat draft.md | tell-check.py -
    tell-check.py --self-test    # dictionary patterns vs their Before/After lines
"""
import re
import sys
from pathlib import Path

# (name, compiled regex). Lexical patterns only; judgment stays with the reader.
PATTERNS = [
    ("em/en dash", re.compile(r"[—–]")),
    ("negative parallelism", re.compile(
        r"\bnot just\b|\bisn't just\b|\bnot only\b.{0,40}\bbut\b|"
        r"\bit'?s not about\b.{0,60}\bit'?s about\b", re.I)),
    ("corrective reframe", re.compile(
        r"\bthat'?s not (?:a |an |the )?\w+(?: \w+)?[,;]? (?:that'?s|it'?s)\b|"
        r"\b(?:is not|isn'?t) (?:a |an |the )?\w+(?: \w+)?[,;]? it'?s (?:actually )?\b", re.I)),
    ("copula avoidance", re.compile(
        r"\bserves? as\b|\bfunctions? as\b|\bacts? as\b|\bstands? as a testament\b", re.I)),
    ("AI vocabulary", re.compile(
        r"\b(?:delve[sd]?|delving|pivotal|tapestry|vibrant|testament|"
        r"underscor(?:e[sd]?|ing)|boasts?|foster(?:s|ing)?|showcas(?:e[sd]?|ing)|"
        r"realm|multifaceted|ever-evolving|crucial|comprehensive|seamless(?:ly)?|"
        r"robust|leverag(?:e[sd]?|ing))\b", re.I)),
    ("throat-clearing", re.compile(
        r"\bit'?s worth noting\b|^\s*importantly,|\bhere'?s the thing\b|"
        r"\bthe reality is\b|\blet'?s unpack\b|\blet'?s dive\b|"
        r"\bwithout further ado\b|\bbuckle up\b", re.I | re.M)),
    ("hedge-stacking", re.compile(
        r"\b(?:arguably|potentially|possibly|perhaps|somewhat|to some extent)\b"
        r"(?:\W+\w+){0,4}\W+"
        r"\b(?:arguably|potentially|possibly|perhaps|somewhat|to some extent)\b", re.I)),
    ("undue significance", re.compile(
        r"\bin today'?s\b|\bbroader trend\b|\bfast-paced world\b|"
        r"\bplays? a vital role\b|\brapidly evolving\b|\bever-changing\b", re.I)),
    ("superficial -ing analysis", re.compile(
        r",\s*(?:highlighting|underscoring|demonstrating|showcasing|emphasizing|"
        r"reflecting|signaling)\s+(?:the|its|their|a|an|how)\b", re.I)),
    ("weasel attribution", re.compile(
        r"\bexperts? (?:say|agree|believe)\b|\bmany believe\b|"
        r"\bwidely regarded\b|\bsome argue\b|\bit is believed\b", re.I)),
    ("false range", re.compile(
        r"\bfrom \w+(?: \w+)? to \w+(?: \w+)?,? (?:and beyond|the possibilities)\b", re.I)),
    ("chatbot correspondence", re.compile(
        r"\bi hope this helps\b|\bfeel free to\b|\bas of my last update\b|"
        r"\bhappy to (?:help|dig deeper|assist)\b|\byou'?ve got this\b", re.I)),
    ("warm close / bow-tie opener", re.compile(
        r"\bin conclusion\b|\bat the end of the day\b|\bultimately,\b", re.I)),
    ("emoji", re.compile(
        "[\U0001F300-\U0001FAFF\U00002728\U00002705\U0000274C\U0001F900-\U0001F9FF]")),
]


DICTIONARY = Path(__file__).resolve().parent.parent / "references" / "tells-dictionary.md"
FIELD = re.compile(r"^(status|pattern|Before|After): (.+)$", re.M)


def load_dictionary(path=DICTIONARY):
    """Entries of the tells dictionary as dicts: term, status, pattern, Before, After."""
    entries = []
    for chunk in re.split(r"^## ", path.read_text(encoding="utf-8"), flags=re.M)[1:]:
        entry = {"term": chunk.split("\n", 1)[0].strip()}
        entry.update(FIELD.findall(chunk))
        entry["status"] = entry.get("status", "").split(" ")[0]
        if entry["status"] not in ("active", "inactive"):
            sys.exit(f"tells-dictionary: {entry['term']!r} needs status: active or inactive")
        if "pattern" in entry:
            try:
                entry["pattern"] = re.compile(entry["pattern"].strip("`"), re.I)
            except re.error as e:
                sys.exit(f"tells-dictionary: bad pattern for {entry['term']!r}: {e}")
        entries.append(entry)
    return entries


def self_test(entries):
    """Every pattern must match its entry's Before line and miss its After line."""
    bad = [e["term"] for e in entries if "pattern" in e and "Before" in e and (
        not e["pattern"].search(e["Before"]) or e["pattern"].search(e.get("After", "")))]
    for term in bad:
        print(f"tells-dictionary: pattern for {term!r} misses its Before or hits its After")
    print(f"{len(entries)} entries, {len(bad)} failing.")
    return 1 if bad else 0


ENTRIES = load_dictionary()
PATTERNS += [(e["term"], e["pattern"]) for e in ENTRIES if e["status"] == "active" and "pattern" in e]


# Provenance footers (the 🤖 generated-with and 🦋 revised-by lines) are disclosure,
# not prose; exempt from the emoji rule. See the pr-body skill, footer conventions.
PROVENANCE_FOOTER = re.compile(r"^\s*>?\s*[\U0001F916\U0001F98B]")


def scan(name, text):
    findings = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if PROVENANCE_FOOTER.match(line):
            continue
        line = line.replace("’", "'")  # typeset drafts use curly apostrophes
        for pname, rx in PATTERNS:
            for m in rx.finditer(line):
                snippet = m.group(0)[:60]
                findings.append((lineno, pname, snippet))
    return findings


def main(argv):
    if len(argv) < 2:
        print(__doc__.strip())
        return 2
    if argv[1:] == ["--self-test"]:
        return self_test(ENTRIES)
    total = 0
    by_pattern = {}
    for path in argv[1:]:
        if path == "-":
            name, text = "<stdin>", sys.stdin.read()
        else:
            name = path
            try:
                with open(path, encoding="utf-8") as f:
                    text = f.read()
            except OSError as e:
                print(f"{path}: {e}", file=sys.stderr)
                return 2
        findings = scan(name, text)
        for lineno, pname, snippet in findings:
            print(f"{name}:{lineno}: [{pname}] {snippet!r}")
            by_pattern[pname] = by_pattern.get(pname, 0) + 1
        total += len(findings)
    if total:
        print(f"\n{total} finding(s):")
        for pname, count in sorted(by_pattern.items(), key=lambda kv: -kv[1]):
            print(f"  {count:3d}  {pname}")
        print("\nSingle hits prove nothing; clusters convict. Judge the whole.")
        return 1
    print("No tells found. The judgment passes still apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
