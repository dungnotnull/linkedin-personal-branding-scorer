#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_skill.py - static validator for Skill #150
(Personal Branding Scorer on LinkedIn).

Runs offline, with zero network and zero model I/O. It checks:

  1. Repo layout: required files/directories exist.
  2. Markdown frontmatter: `name` and `description` present on every skill file.
  3. main.md required sections present.
  4. Each sub-*.md exposes Role, Purpose, Inputs, Process, Output, Quality Gate.
  5. Scoring dimensions table in main.md has weights summing to 1.00 and the
     five canonical dimensions.
  6. SECOND-KNOWLEDGE-BRAIN.md: every `<!--hash:...-->` token is unique and well
     formed (16 lowercase hex chars).

Exit code 0 = pass, 1 = fail. Prints a summary.

Usage:
    python tests/validate_skill.py
    python tests/validate_skill.py --root /path/to/skill
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from typing import List, Tuple

REQUIRED_FILES = [
    "CLAUDE.md",
    "PROJECT-detail.md",
    "PROJECT-DEVELOPMENT-PHASE-TRACKING.md",
    "SECOND-KNOWLEDGE-BRAIN.md",
    "skills/main.md",
    "skills/sub-intake.md",
    "skills/sub-framework-selector.md",
    "skills/sub-scoring-engine.md",
    "skills/sub-improvement-roadmap.md",
    "tests/test-scenarios.md",
    "tools/knowledge_updater.py",
    "tools/README.md",
    "requirements.txt",
]

MAIN_REQUIRED_SECTIONS = [
    "## Role & Persona",
    "## Workflow (Harness Flow)",
    "## Sub-skills Available",
    "## Tools",
    "## Output Format",
    "## Quality Gates",
]

SUB_REQUIRED_SECTIONS = [
    "## Role",
    "## Purpose",
    "## Inputs",
    "## Process",
    "## Output",
    "## Quality Gate",
]

CANONICAL_DIMENSIONS = [
    "Profile completeness & keyword SEO",
    "Content strategy & cadence",
    "Engagement & network quality",
    "Authority & credibility signals",
    "Voice consistency & differentiation",
]
EXPECTED_WEIGHTS = [25, 25, 20, 20, 10]

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
NAME_RE = re.compile(r"^name:\s*(.+?)\s*$", re.MULTILINE)
DESC_RE = re.compile(r"^description:\s*(.+?)\s*$", re.MULTILINE)
HASH_RE = re.compile(r"<!--hash:([0-9a-f]{16})-->")
WEIGHT_RE = re.compile(r"\|\s*([^|]+?)\s*\|\s*(\d+)%\s*\|")


def read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def check_layout(root: str) -> List[str]:
    errs: List[str] = []
    for rel in REQUIRED_FILES:
        if not os.path.isfile(os.path.join(root, rel.replace("/", os.sep))):
            errs.append(f"missing file: {rel}")
    return errs


def check_frontmatter(path: str, rel: str) -> List[str]:
    errs: List[str] = []
    if not os.path.isfile(path):
        return errs
    text = read(path)
    m = FRONTMATTER_RE.match(text)
    if not m:
        errs.append(f"{rel}: missing YAML frontmatter")
        return errs
    fm = m.group(1)
    if not NAME_RE.search(fm):
        errs.append(f"{rel}: frontmatter missing 'name'")
    if not DESC_RE.search(fm):
        errs.append(f"{rel}: frontmatter missing 'description'")
    return errs


def has_section(text: str, section: str) -> bool:
    return section in text


def check_main(root: str) -> List[str]:
    errs: List[str] = []
    path = os.path.join(root, "skills", "main.md")
    if not os.path.isfile(path):
        return ["skills/main.md: missing"]
    text = read(path)
    errs += check_frontmatter(path, "skills/main.md")
    for sec in MAIN_REQUIRED_SECTIONS:
        if not has_section(text, sec):
            errs.append(f"skills/main.md: missing section {sec!r}")
    return errs


def check_subs(root: str) -> List[str]:
    errs: List[str] = []
    subs = ["sub-intake.md", "sub-framework-selector.md", "sub-scoring-engine.md", "sub-improvement-roadmap.md"]
    for name in subs:
        path = os.path.join(root, "skills", name)
        rel = f"skills/{name}"
        if not os.path.isfile(path):
            errs.append(f"{rel}: missing")
            continue
        text = read(path)
        errs += check_frontmatter(path, rel)
        for sec in SUB_REQUIRED_SECTIONS:
            if not has_section(text, sec):
                errs.append(f"{rel}: missing section {sec!r}")
    return errs


def check_weights(root: str) -> List[str]:
    errs: List[str] = []
    path = os.path.join(root, "skills", "main.md")
    if not os.path.isfile(path):
        return errs
    text = read(path)
    # Find the "Scoring Dimensions" table block.
    dims_found = {d: None for d in CANONICAL_DIMENSIONS}
    for line in text.splitlines():
        m = WEIGHT_RE.search(line)
        if not m:
            continue
        name, w = m.group(1).strip(), int(m.group(2))
        for canon in CANONICAL_DIMENSIONS:
            if canon.lower() in name.lower():
                dims_found[canon] = w
    missing = [d for d, w in dims_found.items() if w is None]
    if missing:
        errs.append(f"skills/main.md: dimensions missing weights: {missing}")
        return errs
    total = sum(dims_found.values())
    if total != 100:
        errs.append(f"skills/main.md: weights sum to {total}% (expected 100)")
    if dims_found != dict(zip(CANONICAL_DIMENSIONS, EXPECTED_WEIGHTS)):
        errs.append(f"skills/main.md: weights mismatch got {dims_found} expected {dict(zip(CANONICAL_DIMENSIONS, EXPECTED_WEIGHTS))}")
    return errs


def check_brain_hashes(root: str) -> List[str]:
    errs: List[str] = []
    path = os.path.join(root, "SECOND-KNOWLEDGE-BRAIN.md")
    if not os.path.isfile(path):
        return ["SECOND-KNOWLEDGE-BRAIN.md: missing"]
    text = read(path)
    tokens = HASH_RE.findall(text)
    if not tokens:
        errs.append("SECOND-KNOWLEDGE-BRAIN.md: no hash tokens found")
    seen = set()
    for t in tokens:
        if t in seen:
            errs.append(f"SECOND-KNOWLEDGE-BRAIN.md: duplicate hash token {t}")
        seen.add(t)
    return errs


def run(root: str) -> Tuple[int, List[str], List[str]]:
    errors: List[str] = []
    checks: List[str] = []

    e = check_layout(root)
    checks.append(f"layout: {'OK' if not e else 'FAIL'}")
    errors += e

    e = check_frontmatter(os.path.join(root, "skills", "main.md"), "skills/main.md")
    checks.append(f"main frontmatter: {'OK' if not e else 'FAIL'}")
    errors += e

    e = check_main(root)
    checks.append(f"main sections: {'OK' if not e else 'FAIL'}")
    errors += e

    e = check_subs(root)
    checks.append(f"sub-skills: {'OK' if not e else 'FAIL'}")
    errors += e

    e = check_weights(root)
    checks.append(f"scoring weights: {'OK' if not e else 'FAIL'}")
    errors += e

    e = check_brain_hashes(root)
    checks.append(f"brain hashes: {'OK' if not e else 'FAIL'}")
    errors += e

    return (0 if not errors else 1), checks, errors


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Static validator for Skill #150.")
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    args = ap.parse_args(argv)
    code, checks, errors = run(args.root)
    print(f"validate_skill.py - root: {args.root}")
    for c in checks:
        print(f"  {c}")
    if errors:
        print("\nFAIL - {} issue(s):".format(len(errors)))
        for err in errors:
            print(f"  - {err}")
    else:
        print("\nPASS - all static checks succeeded.")
    return code


if __name__ == "__main__":
    sys.exit(main())
