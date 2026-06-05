#!/usr/bin/env python3
"""Deterministic tell scan for the editorialize skill.

Flags banned constructions from references/banned-tells.md with line numbers.
A first pass only: single hits prove nothing, clusters convict. The judgment
passes (voice, editorial) still happen after this.

Usage:
    tell-check.py <file> [<file> ...]
    cat draft.md | tell-check.py -
"""
import re
import sys

# (name, compiled regex). Lexical patterns only; judgment stays with the reader.
PATTERNS = [
    ("em/en dash", re.compile(r"[—–]")),
    ("negative parallelism", re.compile(
        r"\bnot just\b|\bisn't just\b|\bnot only\b.{0,40}\bbut\b|"
        r"\bit'?s not about\b.{0,60}\bit'?s about\b", re.I)),
    ("corrective reframe", re.compile(
        r"\bthat'?s not (?:a |an |the )?\w+[,;]? (?:that'?s|it'?s)\b|"
        r"\bis not (?:a |an |the )?\w+[,;]? it'?s (?:actually )?\b", re.I)),
    ("copula avoidance", re.compile(
        r"\bserves? as\b|\bfunctions? as\b|\bacts? as\b|\bstands? as a testament\b", re.I)),
    ("AI vocabulary", re.compile(
        r"\b(?:delve[sd]?|delving|pivotal|tapestry|vibrant|testament|"
        r"underscor(?:e[sd]?|ing)|boasts?|foster(?:s|ing)?|showcas(?:e[sd]?|ing)|"
        r"realm|multifaceted|ever-evolving|crucial|comprehensive|seamless(?:ly)?|"
        r"robust|load-bearing|leverag(?:e[sd]?|ing))\b", re.I)),
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


def scan(name, text):
    findings = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for pname, rx in PATTERNS:
            for m in rx.finditer(line):
                snippet = m.group(0)[:60]
                findings.append((lineno, pname, snippet))
    return findings


def main(argv):
    if len(argv) < 2:
        print(__doc__.strip())
        return 2
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
