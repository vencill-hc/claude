#!/usr/bin/env python3
"""Scan a skills root for overlapping skills and extraction candidates.

Walks every immediate subdirectory containing a SKILL.md, computes pairwise
similarity across description, body domain terms, and workflow signature, then
emits clusters and collision pairs as JSON. Intended to be invoked by the
skill-profiler Corpus Overlap mode.
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from score_trigger_description import STOPWORDS, DOMAIN_TERMS, tokenise  # noqa: E402

DESCRIPTION_COLLISION_THRESHOLD = 0.22
BODY_OVERLAP_THRESHOLD = 0.22
WORKFLOW_OVERLAP_THRESHOLD = 0.50
DOMAIN_TERM_SET = {t.lower() for t in DOMAIN_TERMS}

# Generic verbs/nouns that appear across many skills and add no signal value.
SIGNAL_NOISE = {
    "read", "write", "edit", "agent", "agents", "after", "back", "across",
    "analyze", "analyse", "analysis", "answering", "author", "check",
    "anti-patterns", "approach", "based", "before", "being", "between",
    "build", "case", "code", "command", "complete", "consider", "content",
    "context", "create", "current", "design", "detail", "different", "done",
    "each", "either", "every", "example", "examples", "execute", "explain",
    "feature", "field", "file", "files", "find", "first", "follow", "format",
    "function", "given", "good", "help", "here", "high", "include", "into",
    "issue", "know", "list", "make", "many", "method", "might", "model",
    "must", "name", "need", "new", "next", "note", "now", "only", "open",
    "option", "output", "over", "pass", "path", "pattern", "phase", "plan",
    "point", "process", "project", "provide", "question", "reason", "result",
    "return", "review", "run", "running", "same", "save", "section", "see",
    "show", "single", "specific", "start", "state", "step", "still", "stop",
    "store", "summary", "system", "take", "task", "test", "text", "them",
    "thing", "think", "through", "time", "tool", "tools", "track", "trigger",
    "type", "under", "until", "update", "use", "used", "user", "using",
    "value", "view", "wait", "want", "way", "well", "what", "when", "where",
    "which", "while", "whole", "whose", "with", "without", "work", "working",
}

WORKFLOW_PATTERNS = [
    re.compile(r"`([a-z][a-z0-9_]+\.py)`"),
    re.compile(r"subagent_type[\"']?\s*[:=]\s*[\"']([a-z][a-z0-9_-]+)[\"']", re.IGNORECASE),
    re.compile(r"\b(Read|Write|Edit|Bash|Grep|Glob|WebFetch|WebSearch|Task|Agent)\b"),
    re.compile(r"\b(playwright|psql|postgres|sqlite|docker|kubernetes|terraform|pytest|jest|vitest|rspec|minitest|rails|django|fastapi|beam|dataflow|pubsub|bigquery)\b", re.IGNORECASE),
]


def parse_frontmatter(content):
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    raw = parts[1]
    body = parts[2]
    fm = {}
    for key in ("name", "description"):
        match = re.search(rf"^{key}:\s*(.+?)(?:\n\S|\Z)", raw, re.MULTILINE | re.DOTALL)
        if match:
            value = match.group(1).strip()
            if value.startswith(">") or value.startswith("|"):
                value = value[1:].strip()
            fm[key] = re.sub(r"\s+", " ", value)
    return fm, body


def body_terms(body):
    """Return token set restricted to domain terms + tokens of length >= 4."""
    raw = tokenise(body)
    return {t for t in raw if t in DOMAIN_TERM_SET or len(t) >= 4}


def workflow_signature(body):
    sig = set()
    for pattern in WORKFLOW_PATTERNS:
        for match in pattern.finditer(body):
            token = match.group(1) if match.groups() else match.group(0)
            sig.add(token.lower())
    return sig


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def load_skills(root):
    skills = []
    root = Path(root).expanduser()
    for entry in sorted(root.iterdir()):
        if not entry.is_dir() or entry.is_symlink():
            continue
        skill_md = entry / "SKILL.md"
        if not skill_md.exists():
            continue
        try:
            content = skill_md.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        fm, body = parse_frontmatter(content)
        skills.append({
            "name": fm.get("name", entry.name),
            "dir": entry.name,
            "description": fm.get("description", ""),
            "desc_tokens": tokenise(fm.get("description", "")),
            "body_tokens": body_terms(body),
            "workflow": workflow_signature(body),
        })
    return skills


def compute_pairs(skills):
    pairs = []
    for i, a in enumerate(skills):
        for b in skills[i + 1:]:
            desc = jaccard(a["desc_tokens"], b["desc_tokens"])
            body = jaccard(a["body_tokens"], b["body_tokens"])
            workflow = jaccard(a["workflow"], b["workflow"])
            shared_body = sorted(a["body_tokens"] & b["body_tokens"])
            shared_desc = sorted(a["desc_tokens"] & b["desc_tokens"])
            shared_workflow = sorted(a["workflow"] & b["workflow"])
            pairs.append({
                "a": a["dir"],
                "b": b["dir"],
                "description_overlap": round(desc, 3),
                "body_overlap": round(body, 3),
                "workflow_overlap": round(workflow, 3),
                "shared_description_terms": shared_desc,
                "shared_body_terms": shared_body,
                "shared_workflow_terms": shared_workflow,
            })
    return pairs


def compute_distinctiveness(skills):
    """Inverse document frequency: terms in few skills are more distinctive."""
    total = len(skills)
    df = Counter()
    for s in skills:
        for term in s["body_tokens"]:
            df[term] += 1
    return {term: total / count for term, count in df.items()}


def union_find_clusters(skills, pairs, distinctiveness):
    parent = {s["dir"]: s["dir"] for s in skills}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    edges = []
    for p in pairs:
        # Body overlap is the primary clustering signal. Workflow alone causes
        # transitive chaining via incidental shared tools, so require body to
        # also clear at least half the threshold when only workflow is strong.
        body_strong = p["body_overlap"] >= BODY_OVERLAP_THRESHOLD
        workflow_with_body = (
            p["workflow_overlap"] >= WORKFLOW_OVERLAP_THRESHOLD
            and p["body_overlap"] >= BODY_OVERLAP_THRESHOLD * 0.7
        )
        if body_strong or workflow_with_body:
            union(p["a"], p["b"])
            edges.append(p)

    groups = {}
    for s in skills:
        root = find(s["dir"])
        groups.setdefault(root, []).append(s["dir"])

    clusters = []
    for members in groups.values():
        if len(members) < 2:
            continue
        cluster_edges = [
            e for e in edges if e["a"] in members and e["b"] in members
        ]
        shared_terms = Counter()
        for e in cluster_edges:
            for t in e["shared_body_terms"]:
                if t in SIGNAL_NOISE:
                    continue
                weight = distinctiveness.get(t, 1.0)
                if t in DOMAIN_TERM_SET:
                    weight *= 1.5
                shared_terms[t] += weight
            for t in e["shared_workflow_terms"]:
                if t in SIGNAL_NOISE:
                    continue
                shared_terms[t] += 3 * distinctiveness.get(t, 1.0)
        top_terms = [t for t, _ in shared_terms.most_common(8)]
        signal = top_terms[0] if top_terms else "shared-pattern"
        avg_body = round(
            sum(e["body_overlap"] for e in cluster_edges) / len(cluster_edges), 3
        ) if cluster_edges else 0.0
        avg_workflow = round(
            sum(e["workflow_overlap"] for e in cluster_edges) / len(cluster_edges), 3
        ) if cluster_edges else 0.0
        clusters.append({
            "skills": sorted(members),
            "shared_signal": signal,
            "evidence": {
                "avg_body_overlap": avg_body,
                "avg_workflow_overlap": avg_workflow,
                "top_shared_terms": top_terms,
            },
            "extraction_candidate": f"references/{signal}-pattern.md",
        })

    clusters.sort(
        key=lambda c: c["evidence"]["avg_body_overlap"] + c["evidence"]["avg_workflow_overlap"],
        reverse=True,
    )
    return clusters


def find_collisions(pairs):
    collisions = []
    for p in pairs:
        if p["description_overlap"] >= DESCRIPTION_COLLISION_THRESHOLD:
            collisions.append({
                "a": p["a"],
                "b": p["b"],
                "description_overlap": p["description_overlap"],
                "shared_keywords": p["shared_description_terms"],
            })
    collisions.sort(key=lambda c: c["description_overlap"], reverse=True)
    return collisions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "skills_root",
        nargs="?",
        default=os.path.expanduser("~/.claude/skills"),
        help="Path to the skills root directory (default: ~/.claude/skills)",
    )
    parser.add_argument(
        "--include-pairs",
        action="store_true",
        help="Include the full pairwise matrix in the output (verbose)",
    )
    args = parser.parse_args()

    skills = load_skills(args.skills_root)
    if not skills:
        print(json.dumps({
            "error": f"No SKILL.md files found under {args.skills_root}",
            "skills_scanned": 0,
        }))
        sys.exit(1)

    pairs = compute_pairs(skills)
    distinctiveness = compute_distinctiveness(skills)
    clusters = union_find_clusters(skills, pairs, distinctiveness)
    collisions = find_collisions(pairs)

    output = {
        "skills_root": str(Path(args.skills_root).expanduser()),
        "skills_scanned": len(skills),
        "skill_names": [s["dir"] for s in skills],
        "thresholds": {
            "description_collision": DESCRIPTION_COLLISION_THRESHOLD,
            "body_overlap": BODY_OVERLAP_THRESHOLD,
            "workflow_overlap": WORKFLOW_OVERLAP_THRESHOLD,
        },
        "clusters": clusters,
        "collisions": collisions,
    }

    if args.include_pairs:
        output["pairs"] = pairs

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
