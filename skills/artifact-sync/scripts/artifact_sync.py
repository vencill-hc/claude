"""Helpers for moving a Claude artifact between a workpod thread directory and a Claude account.

Stdlib only. Every subcommand reads or writes files under one artifact directory
(`<thread>/artifact/<name>/`) so the Artifact / ArtifactData tool calls stay small.

  collections <page.html>            print the db collection names the page code reads or writes
  normalize <artifact-dir>           turn `ArtifactData ... out_dir=<dir>/seed` exports into plain document bodies
  writes <artifact-dir> [--chunk 50] print the `writes` JSON arrays (one per line) for `ArtifactData batch`
  manifest <artifact-dir> --page P [--url U] [--account A] [--capabilities JSON] [--files F ...]
                                     write or update manifest.json (urls are kept per account)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

COLLECTION_RE = re.compile(r"""\.collection\(\s*["'`]([^"'`$]+)["'`]\s*\)|\bdb\.doc\(\s*["'`]([^"'`$]+)["'`]""")


def cmd_collections(args: argparse.Namespace) -> None:
    text = Path(args.page).read_text()
    found: set[str] = set()
    for m in COLLECTION_RE.finditer(text):
        if m.group(1):
            found.add(m.group(1))
        elif m.group(2):
            parts = m.group(2).split("/")
            if len(parts) % 2 == 0:  # doc path: collection is everything but the last segment
                found.add("/".join(parts[:-1]))
    for c in sorted(found):
        print(c)


def cmd_normalize(args: argparse.Namespace) -> None:
    seed = Path(args.dir) / "seed"
    n = 0
    for p in sorted(seed.rglob("*.json")):
        d = json.loads(p.read_text())
        body = d.get("data") if isinstance(d, dict) and "data" in d and "version" in d else d
        if not isinstance(body, dict):
            sys.exit(f"{p}: document body is not an object")
        p.write_text(json.dumps(body, indent=1, ensure_ascii=False, sort_keys=True) + "\n")
        n += 1
    print(f"normalized {n} documents under {seed}")


def cmd_writes(args: argparse.Namespace) -> None:
    root = Path(args.dir)
    seed = root / "seed"
    entries = []
    for p in sorted(seed.rglob("*.json")):
        rel = p.relative_to(seed)
        collection = "/".join(rel.parts[:-1])
        entries.append({"op": "set", "collection": collection, "doc_id": p.stem, "file_path": str(p)})
    if not entries:
        sys.exit(f"no documents under {seed}")
    for i in range(0, len(entries), args.chunk):
        print(json.dumps(entries[i : i + args.chunk]))
    print(f"{len(entries)} documents in {-(-len(entries) // args.chunk)} batch call(s)", file=sys.stderr)


def cmd_manifest(args: argparse.Namespace) -> None:
    root = Path(args.dir)
    path = root / "manifest.json"
    m = json.loads(path.read_text()) if path.exists() else {"urls": {}}
    m["page"] = args.page
    if args.capabilities is not None:
        m["capabilities"] = json.loads(args.capabilities)
    if args.files is not None:
        m["files"] = args.files
    if args.icon:
        m["icon"] = args.icon
    seed = root / "seed"
    m["collections"] = sorted({"/".join(p.relative_to(seed).parts[:-1]) for p in seed.rglob("*.json")}) if seed.exists() else []
    if args.url:
        m.setdefault("urls", {})[args.account or "unknown"] = args.url
    m["updated_at"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    path.write_text(json.dumps(m, indent=1, sort_keys=True) + "\n")
    print(json.dumps(m, indent=1, sort_keys=True))


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("collections"); c.add_argument("page"); c.set_defaults(fn=cmd_collections)
    n = sub.add_parser("normalize"); n.add_argument("dir"); n.set_defaults(fn=cmd_normalize)
    w = sub.add_parser("writes"); w.add_argument("dir"); w.add_argument("--chunk", type=int, default=50); w.set_defaults(fn=cmd_writes)
    m = sub.add_parser("manifest"); m.add_argument("dir"); m.add_argument("--page", required=True)
    m.add_argument("--url"); m.add_argument("--account"); m.add_argument("--capabilities"); m.add_argument("--icon")
    m.add_argument("--files", nargs="*"); m.set_defaults(fn=cmd_manifest)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
