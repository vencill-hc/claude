"""Dump the live seniority parser as flat tables for diffing against the GDU mapping sheet.

Run from the pipelines repo: `.venv/bin/python <this file> [--commit]`
Prints keyword → level → kind, the normalization substitutions, board-seat exclusions,
and the title synonym table. Output is markdown so it can be pasted or diffed directly.
"""

import subprocess
import sys
from pathlib import Path

REPO = Path.home() / "Documents/git/data-universe-pipelines"
sys.path.insert(0, str(REPO / "src"))

from utils import board_seat_utils as b  # noqa: E402
from utils import seniority_utils as s  # noqa: E402
from utils.string_validator_utils import JOB_TITLE_NORMALIZATION_SYNONYMS  # noqa: E402

rev = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
branch = subprocess.run(["git", "-C", str(REPO), "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
print(f"# Seniority spec @ {branch} {rev}\n")
FILES = ["src/utils/seniority_utils.py", "src/utils/board_seat_utils.py", "src/utils/string_validator_utils.py"]
subprocess.run(["git", "-C", str(REPO), "fetch", "-q", "origin", "main"])
drift = subprocess.run(["git", "-C", str(REPO), "diff", "--stat", "HEAD", "origin/main", "--", *FILES], capture_output=True, text=True).stdout
print(f"\n> {'WARNING: checkout differs from origin/main for parser files:\n' + drift if drift else 'Parser files identical to origin/main.'}\n")

print("## Ladder (multi-match resolution, high wins)\n")
print(" > ".join(k.value for k, _ in sorted(s._LADDER.items(), key=lambda kv: -kv[1])))

print("\n## Lexicon\n\n| keyword | level | kind |\n|---|---|---|")
for e in s._LEXICON:
    print(f"| {' '.join(e.tokens)} | {e.seniority.value} | {e.kind.value} |")

print("\n## Normalization substitutions (regex → token, in order)\n\n| regex | token |\n|---|---|")
for pat, tok in s._NORMALIZE_SUBS.items():
    print(f"| `{pat}` | `{tok or '(removed)'}` |")

print("\n## Demotion tokens (VP/CxO → Senior)\n")
print(", ".join(sorted(s._DOWNWEIGHT_TOKENS)))
print("\n## Board disqualifiers (board + this → Entry)\n")
print(", ".join(sorted(s._BOARD_DISQUALIFIER_TOKENS) + [" ".join(x) for x in s._BOARD_DISQUALIFIER_BIGRAMS]))
print("\n## Board-seat exclusions (discard board keyword, recompute)\n")
for p in b._EXCLUDED_BOARD_PATTERNS:
    print(f"- `{p.pattern}`")
print("\nEXCLUDE token regex(es):")
for pat, tok in b._NORMALIZE_SUBS.items():
    if tok == b._Token.EXCLUDE:
        print(f"- `{pat}`")

print("\n## Title synonyms (applied before tokenizing)\n\n| written | treated as |\n|---|---|")
for k, v in JOB_TITLE_NORMALIZATION_SYNONYMS.items():
    print(f"| {k} | {v} |")
