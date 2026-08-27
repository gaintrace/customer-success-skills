#!/usr/bin/env python3
"""
Audit how reliably each skill triggers, and whether skills collide.

A skill's `description` is the only thing loaded until it fires. With thirty skills in one
domain, two failures matter more than anything in the skill body:

  1. **Under-triggering** — the user asks for exactly this and nothing fires, because they
     phrased it the way a CSM talks rather than the way the skill is named.
  2. **Collision** — five skills all claim "which accounts are at risk", the wrong one wins,
     and the user concludes the library is unreliable.

This script measures both. It parses every description, finds duplicated trigger phrases across
skills, and routes a corpus of realistic prompts to see which skill would actually win.

    python3 scripts/check_triggers.py                  # full audit
    python3 scripts/check_triggers.py --collisions     # only phrase collisions
    python3 scripts/check_triggers.py --route "acme has gone quiet, should I worry"
    python3 scripts/check_triggers.py --corpus evals/routing.json

Exit 0 clean · 1 problems found · 2 usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

MIN_PHRASES = 8
MAX_DESC = 1024
# Phrases so generic that claiming them guarantees a collision in a CS library.
TOO_GENERIC = {
    "churn", "risk", "renewal", "customer", "account", "health", "expansion",
    "revenue", "retention", "report", "data", "meeting", "call", "email", "qbr",
}
STOP = {"the", "a", "an", "my", "our", "is", "are", "of", "to", "for", "in", "on",
        "and", "or", "with", "at", "it", "this", "that", "should", "i", "we", "do",
        "what", "how", "can", "me", "be", "have", "has", "was", "will", "just"}


def parse_description(md: Path) -> tuple[str, str]:
    text = md.read_text()
    if not text.startswith("---"):
        return "", ""
    end = text.find("\n---", 3)
    fm = text[3:end] if end != -1 else ""
    name = desc = ""
    for m in re.finditer(r"^(name|description):\s*(.*)$", fm, re.M):
        val = m.group(2).strip().strip('"').strip("'")
        if m.group(1) == "name":
            name = val
        else:
            desc = val
    return name, desc


# A quote mark adjacent to a letter is an apostrophe, not a delimiter — otherwise "don't"
# and "they've" shatter every description into fake trigger phrases.
PHRASE_RE = re.compile(r"(?<![A-Za-z])'([^']{3,120})'(?![A-Za-z])")


def phrases(desc: str) -> list[str]:
    """Trigger phrases are the properly-delimited single-quoted fragments."""
    out: list[str] = []
    for p in PHRASE_RE.findall(desc):
        p = p.strip().lower()
        # A one-word fragment shorter than 8 characters cannot discriminate between thirty
        # skills in one domain; treating it as a trigger is how 'what' ends up matching
        # every prompt in the corpus.
        if len(p) < 4 or (" " not in p and len(p) < 8):
            continue
        if p in STOP:
            continue
        out.append(p)
    return out


def tokens(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z']+", s.lower()) if w not in STOP and len(w) > 2}


def load_skills() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for d in sorted(p for p in SKILLS.iterdir() if p.is_dir() and (p / "SKILL.md").exists()):
        name, desc = parse_description(d / "SKILL.md")
        out[d.name] = {
            "declared_name": name,
            "desc": desc,
            "phrases": phrases(desc),
            "dir": d,
        }
    return out


# ======================================================================================
# Description hygiene
# ======================================================================================

def audit_descriptions(skills: dict[str, dict]) -> list[str]:
    problems: list[str] = []
    for slug, s in skills.items():
        d, ph = s["desc"], s["phrases"]
        if not d:
            problems.append(f"{slug}: no description")
            continue
        if s["declared_name"] != slug:
            problems.append(f"{slug}: name field is '{s['declared_name']}'")
        if len(d) > MAX_DESC:
            problems.append(f"{slug}: description {len(d)} chars (max {MAX_DESC})")
        if len(ph) < MIN_PHRASES:
            problems.append(f"{slug}: {len(ph)} trigger phrases (min {MIN_PHRASES})")
        if not re.search(r"[Uu]se this whenever", d):
            problems.append(f"{slug}: no 'Use this whenever ...' clause — models under-trigger skills")
        if "even if" not in d.lower():
            problems.append(f"{slug}: no 'even if they don't ...' clause")
        if not re.search(r"\bsee ([a-z0-9-]+)\b", d):
            problems.append(f"{slug}: no 'see <sibling>' disambiguation — collisions go unresolved")
        generic = [p for p in ph if p in TOO_GENERIC]
        if generic:
            problems.append(f"{slug}: bare generic trigger(s) {generic} — guarantees collision; "
                            f"qualify them ('churn risk for my book', not 'churn')")
        # A CSM types the way they talk. If no phrase is first-person or conversational,
        # the skill will only fire when the user already knows its name.
        conversational = [p for p in ph if re.search(r"\b(i|my|me|we|our|they|them)\b", p)]
        if len(conversational) < 2:
            problems.append(f"{slug}: fewer than 2 first-person triggers — real prompts sound "
                            f"like 'my renewals' or 'they've gone quiet', not command names")
    return problems


# ======================================================================================
# Collisions
# ======================================================================================

def find_collisions(skills: dict[str, dict]) -> tuple[dict, list]:
    exact: dict[str, list[str]] = defaultdict(list)
    for slug, s in skills.items():
        for p in s["phrases"]:
            exact[p].append(slug)
    hard = {p: owners for p, owners in exact.items() if len(owners) > 1}

    near: list[tuple[str, str, str, str, float]] = []
    items = [(slug, p, tokens(p)) for slug, s in skills.items() for p in s["phrases"]]
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a_slug, a_p, a_t = items[i]
            b_slug, b_p, b_t = items[j]
            if a_slug == b_slug or not a_t or not b_t:
                continue
            jac = len(a_t & b_t) / len(a_t | b_t)
            if jac >= 0.6 and a_p != b_p:
                near.append((a_slug, a_p, b_slug, b_p, round(jac, 2)))
    return hard, sorted(near, key=lambda x: -x[4])


# ======================================================================================
# Routing
# ======================================================================================

def route(prompt: str, skills: dict[str, dict]) -> list[tuple[str, float, list[str]]]:
    """
    Approximate what an agent does when choosing a skill: reward literal phrase matches
    heavily (longer = more specific = better), token overlap lightly.
    """
    p = prompt.lower()
    p_tok = tokens(prompt)
    scored: list[tuple[str, float, list[str]]] = []
    for slug, s in skills.items():
        score = 0.0
        hits: list[str] = []
        for ph in s["phrases"]:
            if ph in p:
                score += 3.0 + len(ph.split()) * 0.8
                hits.append(ph)
            else:
                pt = tokens(ph)
                if pt and len(pt & p_tok) / len(pt) >= 0.75:
                    score += 1.2
                    hits.append(f"~{ph}")
        d_tok = tokens(s["desc"])
        if p_tok:
            score += len(p_tok & d_tok) / len(p_tok) * 1.5
        if slug.replace("-", " ") in p:
            score += 4.0
        if score > 0:
            scored.append((slug, round(score, 2), hits[:4]))
    return sorted(scored, key=lambda x: -x[1])


def audit_routing(corpus: list[dict], skills: dict[str, dict]) -> tuple[list[str], int, int]:
    problems: list[str] = []
    correct = ambiguous = 0
    for case in corpus:
        prompt, want = case["prompt"], case["expect"]
        ranked = route(prompt, skills)
        if not ranked:
            problems.append(f"NO MATCH  {prompt!r}\n            expected {want} — nothing would fire")
            continue
        top, top_score, hits = ranked[0]
        runner = ranked[1] if len(ranked) > 1 else None
        if top != want:
            problems.append(
                f"MISROUTE  {prompt!r}\n            expected {want}, would fire {top} "
                f"({top_score}, via {hits})")
            continue
        correct += 1
        if runner and top_score - runner[1] < 1.5:
            ambiguous += 1
            problems.append(
                f"AMBIGUOUS {prompt!r}\n            {top} ({top_score}) barely beats "
                f"{runner[0]} ({runner[1]}) — add a disambiguating phrase to one of them")
    return problems, correct, ambiguous


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit skill triggering and collisions.")
    ap.add_argument("--collisions", action="store_true", help="only phrase collisions")
    ap.add_argument("--route", metavar="PROMPT", help="show which skill would fire")
    ap.add_argument("--corpus", default="evals/routing.json", help="routing test corpus")
    args = ap.parse_args()

    skills = load_skills()
    if not skills:
        print("no skills found", file=sys.stderr)
        return 2

    if args.route:
        ranked = route(args.route, skills)
        if not ranked:
            print(f"Nothing would fire for {args.route!r} — a coverage gap.")
            return 1
        print(f"\n{args.route!r}\n")
        for slug, sc, hits in ranked[:5]:
            print(f"  {sc:6.2f}  {slug:26s}  {', '.join(hits) or '—'}")
        if len(ranked) > 1 and ranked[0][1] - ranked[1][1] < 1.5:
            print(f"\n  ⚠ ambiguous — {ranked[0][0]} barely beats {ranked[1][0]}")
        return 0

    fail = False
    hard, near = find_collisions(skills)

    if hard:
        fail = True
        print("## Hard collisions — the same phrase claimed by more than one skill\n")
        for p, owners in sorted(hard.items()):
            print(f"  '{p}'\n      claimed by: {', '.join(owners)}")
        print()

    if near:
        print("## Near collisions — phrases likely to compete\n")
        for a, ap_, b, bp, j in near[:25]:
            print(f"  {j:.2f}  {a}: '{ap_}'\n        {b}: '{bp}'")
        if len(near) > 25:
            print(f"  … and {len(near) - 25} more")
        print()

    if args.collisions:
        return 1 if fail else 0

    problems = audit_descriptions(skills)
    if problems:
        fail = True
        print("## Description hygiene\n")
        for p in problems:
            print(f"  {p}")
        print()

    corpus_path = ROOT / args.corpus
    if corpus_path.exists():
        corpus = json.loads(corpus_path.read_text())
        cases = corpus["cases"] if isinstance(corpus, dict) else corpus
        rp, correct, ambiguous = audit_routing(cases, skills)
        print(f"## Routing — {correct}/{len(cases)} prompts reach the intended skill"
              f" ({ambiguous} of those only just)\n")
        for p in rp:
            print(f"  {p}")
        if rp:
            fail = True
        print()
    else:
        print(f"## Routing — no corpus at {args.corpus}; write one to test this\n")

    # Coverage: a skill nothing routes to will never fire in practice.
    if corpus_path.exists():
        expected = {c["expect"] for c in cases}
        never = sorted(set(skills) - expected)
        if never:
            print("## Untested skills — no routing case claims these\n")
            for s in never:
                print(f"  {s}")
            print()

    print(f"{len(skills)} skills · {'PROBLEMS FOUND' if fail else 'clean'}")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
