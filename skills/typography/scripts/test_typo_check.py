"""Self-check for typo-check.py. Run: python3 test_typo_check.py (plain asserts, no framework)."""
import importlib.util
import pathlib

spec = importlib.util.spec_from_file_location("tc", pathlib.Path(__file__).with_name("typo-check.py"))
tc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tc)


def codes(text, name="t.md"):
    return sorted({h[3] for h in tc.scan(name, text)})


# flagged
assert codes('He said "hi" to me.') == ["QUOTE"]
assert codes("it's fine") == ["APOS"]
assert codes("One.  Two.") == ["SPACE2"]
assert codes("word -- word") == ["DASH"]
assert codes("word---word") == ["DASH"]
assert codes("a thing - another thing") == ["DASH"]
assert codes("and so on...") == ["ELLIPSIS"]
assert codes("wait . . . what") == ["ELLIPSIS"]
assert codes("Copyright (c) 2026 Acme(TM)") == ["SYMBOL"]
assert codes("No way!!") == ["BANG"]
assert codes("pages 330-39 and 1880-1912") == ["RANGE"]
assert codes("8.5 x 11 paper") == ["TIMES"]

# not flagged
assert codes("She is 6' 10\" tall") == []                     # foot and inch marks
assert codes("filed 2026-09-22, call 555-1234") == []           # date, phone
assert codes("ticket PE-439 and DAT-68") == []                  # identifiers
assert codes("- a list item\n- another") == []                  # markdown bullets
assert codes("---\ntitle: x\n---\nbody") == []                  # front matter
assert codes("para\n\n---\n\npara") == []                       # horizontal rule
assert codes("use `it's` and `\"x\"` here") == []               # inline code
assert codes("```\nx = 'a' -- b\n```\nprose") == []             # fenced code
assert codes("Curly ‘quotes’ and “these” pass") == []
assert codes("An em dash — allowed by Butterick") == []         # never demanded, never flagged
assert codes("range 1880–1912 with en dash") == []
assert codes('<p class="x">it&rsquo;s fine</p><code>a -- b</code>', "t.html") == []
assert codes('<p>it\'s "quoted"</p>', "t.html") == ["APOS", "QUOTE"]

# line numbers survive skipping
hits = tc.scan("t.md", "clean\n```\ncode\n```\nbad -- here")
assert hits[0][1] == 5, hits

print("ok")

# markdown table separator rows are structure, not dashes
assert codes("| a | b |\n|---|---|\n| 1 | 2 |") == []
assert codes("|:---|---:|") == []
print("ok (table rows)")

