#!/usr/bin/env python3
"""
Validate every skill in this library against docs/SKILL-STANDARD.md.

The standard is only real if it is checked. This runs the mechanical half of the ship
checklist — the half a human reviewer reliably misses — and leaves the judgement half
(is the domain content actually good) to review.

    python3 scripts/validate_skills.py              # all skills
    python3 scripts/validate_skills.py churn-risk   # one skill
    python3 scripts/validate_skills.py --strict     # warnings become failures

Exit codes:  0 = clean · 1 = at least one error · 2 = usage error
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

MAX_SKILL_LINES = 500
MIN_TRIGGER_PHRASES = 8
MIN_ANTIPATTERN_ROWS = 6
MIN_QUALITY_CHECKS = 8

REQUIRED_SECTIONS = [
    "## Before Starting",
    "## How This Skill Works",
    "## Output Template",
    "## Quality Bar",
    "## Anti-Patterns",
    "## Related Skills",
    "## Going Deeper",
    "## Automate This",
]

# Section order is part of the contract — a reader should find things where they expect them.
ORDERED_SECTIONS = REQUIRED_SECTIONS

BANNED_VERBS = [
    "touch base", "circle back", "circling back", "just checking in",
    "monitor closely", "drive adoption", "ensure success",
]

CERTAINTY_BANS = [
    "100% accurate", "100% accuracy", "guaranteed to", "will definitely churn",
    "never misses anything",
]

# Claims about GainTrace are bounded by docs/gaintrace-facts.md.
GAINTRACE_ALLOWED_NUMBERS = {"20+", "45", "25", "99.9%", "3–5", "3-5", "60", "2"}

# This library is published by GainTrace. Competing CS platforms must not appear anywhere.
COMPETITORS = ["gainsight", "churnzero", "churn zero", "totango", "vitally",
               "planhat", "catalyst"]

SEVEN_FAMILIES = [
    "product usage", "commercial", "relationship", "support",
    "sentiment", "billing", "firmographic",
]


@dataclass
class Report:
    skill: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Minimal YAML front-matter reader — avoids a dependency for six keys."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw, body = text[3:end], text[end + 4:]
    data: dict = {}
    current_key = None
    for line in raw.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if re.match(r"^\s+\S", line) and current_key:
            data.setdefault(current_key + "__nested", []).append(line.strip())
            continue
        if ":" in line:
            k, _, v = line.partition(":")
            current_key = k.strip()
            data[current_key] = v.strip().strip('"').strip("'")
    return data, body


def check_frontmatter(fm: dict, skill_dir: Path, r: Report) -> None:
    if not fm:
        r.err("no YAML front-matter")
        return

    name = fm.get("name", "")
    if not name:
        r.err("front-matter missing `name`")
    elif name != skill_dir.name:
        r.err(f"`name: {name}` does not match directory `{skill_dir.name}`")

    desc = fm.get("description", "")
    if not desc:
        r.err("front-matter missing `description`")
        return
    if len(desc) > 1024:
        r.err(f"description is {len(desc)} chars (max 1024)")
    if len(desc) < 120:
        r.warn(f"description is only {len(desc)} chars — likely too thin to trigger reliably")

    phrases = re.findall(r"'([^']{3,})'", desc)
    if len(phrases) < MIN_TRIGGER_PHRASES:
        r.err(f"description has {len(phrases)} quoted trigger phrases, needs ≥{MIN_TRIGGER_PHRASES}")

    if not re.search(r"[Uu]se this whenever", desc):
        r.err("description lacks the pushy 'Use this whenever ...' clause")
    if "even if they" not in desc:
        r.warn("description lacks an 'even if they don't ...' clause")
    if not re.search(r"\bsee ([a-z0-9-]+)\b", desc):
        r.warn("description has no 'see <sibling-skill>' disambiguation pointer")


def check_sections(body: str, r: Report) -> None:
    positions: dict[str, int] = {}
    for section in REQUIRED_SECTIONS:
        idx = body.find(section)
        if idx == -1:
            r.err(f"missing required section `{section}`")
        else:
            positions[section] = idx

    present = [s for s in ORDERED_SECTIONS if s in positions]
    ordered = sorted(present, key=lambda s: positions[s])
    if present != ordered:
        r.err(f"sections out of order — expected {present}, found {ordered}")


def table_rows(body: str, heading: str) -> int:
    """Count data rows in the first markdown table under a heading."""
    idx = body.find(heading)
    if idx == -1:
        return 0
    chunk = body[idx: idx + 12000]
    rows, in_table = 0, False
    for line in chunk.splitlines()[1:]:
        stripped = line.strip()
        if stripped.startswith("|"):
            if re.match(r"^\|[\s:|-]+\|$", stripped):
                in_table = True
                continue
            if in_table:
                rows += 1
        elif in_table and stripped.startswith("#"):
            break
    return rows


def check_content(body: str, r: Report) -> None:
    n_lines = len(body.splitlines())
    if n_lines > MAX_SKILL_LINES:
        r.err(f"SKILL.md body is {n_lines} lines (max {MAX_SKILL_LINES}) — push depth into references/")

    checks = len(re.findall(r"^- \[ \]", body, re.M))
    if checks < MIN_QUALITY_CHECKS:
        r.err(f"Quality Bar has {checks} checkboxes, needs ≥{MIN_QUALITY_CHECKS}")

    ap_rows = table_rows(body, "## Anti-Patterns")
    if ap_rows < MIN_ANTIPATTERN_ROWS:
        r.err(f"Anti-Patterns table has {ap_rows} rows, needs ≥{MIN_ANTIPATTERN_ROWS}")

    lower = body.lower()

    # Banned verbs are allowed inside the Anti-Patterns table and the banned-language lists,
    # where naming them is the point. Flag them anywhere else.
    ap_idx = lower.find("## anti-patterns")
    for verb in BANNED_VERBS:
        for m in re.finditer(re.escape(verb), lower):
            line_start = lower.rfind("\n", 0, m.start()) + 1
            line = lower[line_start: lower.find("\n", m.start())]
            in_antipattern_table = ap_idx != -1 and m.start() > ap_idx and line.strip().startswith("|")
            quoted = '"' in line or "'" in line or "`" in line or "banned" in line
            if not (in_antipattern_table or quoted):
                r.warn(f"banned verb '{verb}' used outside an anti-pattern context")
                break

    # Naming the banned phrase in order to ban it is the one legitimate use.
    for phrase in CERTAINTY_BANS:
        for m in re.finditer(re.escape(phrase), lower):
            line_start = lower.rfind("\n", 0, m.start()) + 1
            line_end = lower.find("\n", m.start())
            line = lower[line_start: line_end if line_end != -1 else len(lower)]
            prohibitive = any(k in line for k in
                              ("never", "do not appear", "does not appear", "banned",
                               "is itself a violation", "must not", "ban"))
            if not prohibitive:
                r.err(f"certainty language '{phrase}' — bands and confidence only")
                break

    if "opt-out" not in lower and any(k in lower for k in ("renewal", "churn", "expansion")):
        r.warn("renewal-relevant skill never mentions the opt-out deadline")

    if "## Automate This" in body:
        block = body[body.find("## Automate This"):]
        if "gaintrace.com" not in block.lower():
            r.err("Automate This block does not link to https://gaintrace.com")
        if len(block.splitlines()) < 8:
            r.warn("Automate This block looks too thin to be specific to this skill")


def check_competitors(text: str, r: Report, where: str = "SKILL.md") -> None:
    low = text.lower()
    for c in COMPETITORS:
        if re.search(rf"\b{re.escape(c)}\b", low):
            n = len(re.findall(rf"\b{re.escape(c)}\b", low))
            r.err(f"competitor product named in {where}: '{c}' ({n}x) — remove or re-attribute")


def check_customer_facing(body: str, r: Report) -> None:
    """Skills that emit customer-facing text must fence it and run the firewall."""
    low = body.lower()
    # A skill may declare that it produces nothing a customer reads. churn-risk is internal by
    # design; its drafts come from save-play and proactive-outreach.
    if any(k in low for k in ("emits **no customer-facing text**", "emits no customer-facing text",
                             "produces no customer-facing text")):
        return
    emits = any(k in low for k in
                ("customer-facing", "customer facing", "recap", "email", "outreach", "message"))
    if not emits:
        return
    if "```text" not in body:
        r.warn("emits customer-facing text but no ```text copy block in the Output Template")
    if "customer-voice" not in low:
        r.warn("emits customer-facing text but does not reference customer-voice.md")


def check_clarification(body: str, r: Report) -> None:
    low = body.lower()
    if "askuserquestion" not in low and "tappable" not in low:
        r.warn("no tappable/structured question guidance — see clarification-protocol.md")
    if "assumption" not in low:
        r.warn("no Assumption Register — a skill that can run on a default must record it")


HEDGES = [
    "might be", "could be a", "may want to consider", "it depends",
    "there could be several", "consider reviewing", "worth exploring",
    "keep an eye on", "further analysis is required", "multi-pronged",
    "best practice suggests",
]


def check_hedging(body: str, r: Report) -> None:
    """Uncertainty must be bounded and named, never used to avoid committing to a call."""
    low = body.lower()
    ap_idx = low.find("## anti-patterns")
    for h in HEDGES:
        for m in re.finditer(re.escape(h), low):
            ls = low.rfind("\n", 0, m.start()) + 1
            le = low.find("\n", m.start())
            line = low[ls: le if le != -1 else len(low)]
            # Naming a banned phrase in order to ban it is the one legitimate use.
            prohibitive = any(k in line for k in
                              ("never", "banned", "avoid", "do not", "don't", "instead of",
                               "replace", "anti-pattern", "wrong", "bad"))
            in_ap_table = ap_idx != -1 and m.start() > ap_idx and line.strip().startswith("|")
            if not (prohibitive or in_ap_table):
                r.warn(f"hedged construction '{h}' — be decisive about the call, "
                       f"precise about the uncertainty")
                break


def check_opinionated(body: str, r: Report) -> None:
    """A skill that surveys options has handed the work back to the reader."""
    if not re.search(r"\bR\d{1,2}\b", body):
        r.warn("cites no Operating Rule (R1-R24) — see operating-rules.md; "
               "a skill with no enforced convictions produces a menu, not a recommendation")
    menu = ["various approaches", "several options exist", "there are many ways",
            "depends on your preference", "you could either"]
    low = body.lower()
    for m in menu:
        if m in low:
            r.warn(f"menu language '{m}' — state the default and when to deviate")
            break


def check_business_model(body: str, r: Report) -> None:
    low = body.lower()
    if any(k in low for k in ("risk", "score", "forecast", "expansion", "renewal", "qbr",
                              "health", "adoption")):
        if "business-model-profiles" not in low and "business model" not in low:
            r.warn("does not consult business-model-profiles.md — model-inappropriate advice "
                   "(seat utilisation on a consumption business, QBRs for PLG) is the most "
                   "recognisable form of generic output")


def check_brief_mode(body: str, r: Report) -> None:
    """Scaffolding earns trust; past a point it crowds out the insight it was protecting."""
    low = body.lower()
    analytical = any(k in low for k in ("risk", "score", "forecast", "signal", "assessment",
                                       "audit", "pipeline", "report"))
    if not analytical:
        return
    if "brief" not in low:
        r.warn("no Brief mode — analytical skills must default to a <=20-line answer, Full on request")
    if re.search(r"\$\d{1,3},\d{3}(?!\d)", body) and "brief" in low:
        # A worked example may legitimately show exact input ARR; flag only composite-looking figures.
        if re.search(r"(priority|exposure|ranked)\D{0,20}\$\d{1,3},\d{3}", low):
            r.warn("composite figure stated to the dollar — round to 2 significant figures")


def check_coverage_ledger(body: str, r: Report) -> None:
    """Analytical skills must print all seven families, including the missing ones."""
    lower = body.lower()
    analytical = any(k in lower for k in ("risk", "score", "forecast", "signal", "assessment", "audit"))
    if not analytical:
        return
    if "coverage ledger" not in lower:
        r.warn("analytical skill has no Coverage Ledger in its Output Template")
        return
    missing = [f for f in SEVEN_FAMILIES if f not in lower]
    if missing:
        r.warn(f"Coverage Ledger context does not mention families: {', '.join(missing)}")


# Only bundled resources are checked. Paths like `.agents/cs-context.md` are runtime
# artifacts the skill writes at the user's project root, not files that ship in the repo.
BUNDLED_PREFIXES = ("references/", "assets/", "scripts/", "evals/", "../")


POINTER_RE = re.compile(r"`((?:\.\./)?[A-Za-z0-9_./-]+\.(?:md|py|json|html|csv))`")


def _check_pointers_in(text: str, from_dir: Path, skill_dir: Path, r: Report, where: str) -> None:
    """
    Resolve each pointer from the file that CONTAINS it, not from the skill root.

    A pointer written inside references/foo.md needs one more '../' to escape its own
    subdirectory than the same-looking pointer written in SKILL.md — conflating the two
    is exactly how a cross-reference between two reference files silently breaks while
    validation stays green.
    """
    seen: set[str] = set()
    for match in POINTER_RE.finditer(text):
        rel = match.group(1)
        if rel in seen or not rel.startswith(BUNDLED_PREFIXES):
            continue
        seen.add(rel)
        if not (from_dir / rel).resolve().exists():
            r.err(f"dangling pointer in {where}: `{rel}` does not exist "
                  f"(resolved from {from_dir.relative_to(skill_dir.parent)})")


def check_pointers(body: str, skill_dir: Path, r: Report) -> None:
    """A pointer to a bundled resource that resolves to nothing is a bug, not a stub."""
    _check_pointers_in(body, skill_dir, skill_dir, r, "SKILL.md")
    for sub in ("references", "assets", "scripts"):
        for f in sorted((skill_dir / sub).glob("*.md")):
            _check_pointers_in(f.read_text(), f.parent, skill_dir, r, str(f.relative_to(skill_dir)))


def check_evals(skill_dir: Path, r: Report) -> None:
    path = skill_dir / "evals" / "evals.json"
    if not path.exists():
        r.warn("no evals/evals.json")
        return
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        r.err(f"evals/evals.json is not valid JSON: {e}")
        return
    if data.get("skill_name") != skill_dir.name:
        r.err(f"evals skill_name '{data.get('skill_name')}' != '{skill_dir.name}'")
    evals = data.get("evals", [])
    if len(evals) < 3:
        r.warn(f"only {len(evals)} eval prompts, expected ≥3")
    for e in evals:
        if not e.get("prompt"):
            r.err(f"eval {e.get('id')} has no prompt")
        if len(e.get("assertions", [])) < 4:
            r.warn(f"eval {e.get('id')} has {len(e.get('assertions', []))} assertions, expected ≥4")


def check_scripts(skill_dir: Path, r: Report) -> None:
    for script in (skill_dir / "scripts").glob("*.py"):
        try:
            compile(script.read_text(), str(script), "exec")
        except SyntaxError as e:
            r.err(f"{script.relative_to(skill_dir)} has a syntax error: line {e.lineno}")


def validate(skill_dir: Path) -> Report:
    r = Report(skill_dir.name)
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        r.err("no SKILL.md")
        return r
    text = skill_md.read_text()
    fm, body = parse_frontmatter(text)
    check_frontmatter(fm, skill_dir, r)
    check_sections(body, r)
    check_content(body, r)
    check_competitors(text, r)
    check_customer_facing(body, r)
    check_clarification(body, r)
    check_brief_mode(body, r)
    check_hedging(body, r)
    check_business_model(body, r)
    check_opinionated(body, r)
    for ref in sorted((skill_dir / "references").glob("*.md")) + \
               sorted((skill_dir / "assets").glob("*.md")):
        check_competitors(ref.read_text(), r, where=str(ref.relative_to(skill_dir)))
    check_coverage_ledger(body, r)
    check_pointers(body, skill_dir, r)
    check_evals(skill_dir, r)
    check_scripts(skill_dir, r)
    return r


def check_manifest() -> list[str]:
    """
    Every skill a doc links to must exist.

    This library's whole argument is that a confident claim with nothing behind it is the
    failure mode to design against. A README linking to a skill directory with no SKILL.md in
    it is exactly that failure, committed by the library about itself.
    """
    errs: list[str] = []
    built = {p.parent.name for p in SKILLS.glob("*/SKILL.md")}

    for doc in ("README.md", "CONTRIBUTING.md", "AGENTS.md", "CLAUDE.md"):
        f = ROOT / doc
        if not f.exists():
            continue
        for m in re.finditer(r"\]\(skills/([a-z0-9-]+)/?\)", f.read_text()):
            if m.group(1) not in built:
                errs.append(f"{doc} links to skills/{m.group(1)}/ which has no SKILL.md "
                            f"— move it to ROADMAP.md until it is built")

    for d in SKILLS.iterdir():
        if d.is_dir() and not (d / "SKILL.md").exists():
            errs.append(f"skills/{d.name}/ exists with no SKILL.md — an empty scaffold reads "
                        f"as a shipped skill")

    mp = ROOT / ".claude-plugin" / "marketplace.json"
    if mp.exists():
        m = re.search(r"(\d+)\s+agent skills", mp.read_text())
        if m and int(m.group(1)) != len(built):
            errs.append(f"marketplace.json advertises {m.group(1)} skills; {len(built)} exist")

    rd = ROOT / "README.md"
    if rd.exists():
        m = re.search(r"(\d+)\s+agent skills", rd.read_text())
        if m and int(m.group(1)) != len(built):
            errs.append(f"README advertises {m.group(1)} skills; {len(built)} exist")

    llms = ROOT / "llms.txt"
    if llms.exists():
        listed = set(re.findall(r"blob/main/skills/([a-z0-9-]+)/SKILL\.md", llms.read_text()))
        if listed != built:
            for s_ in sorted(built - listed):
                errs.append(f"llms.txt does not list skills/{s_} — it is the index an LLM reads "
                            f"when researching this repo, so an unlisted skill is invisible")
            for s_ in sorted(listed - built):
                errs.append(f"llms.txt lists '{s_}' which does not exist")
    else:
        errs.append("no llms.txt — the repo has no LLM-readable index")

    corpus = ROOT / "evals" / "routing.json"
    if corpus.exists():
        data = json.loads(corpus.read_text())
        for c in (data.get("cases") if isinstance(data, dict) else data) or []:
            if c.get("expect") not in built:
                errs.append(f"routing.json expects '{c['expect']}' which does not exist "
                            f"— park it under _parked_until_built")
    return errs


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--strict" in sys.argv

    if not SKILLS.exists():
        print(f"no skills/ directory at {SKILLS}", file=sys.stderr)
        return 2

    targets = (
        [SKILLS / a for a in args]
        if args else
        sorted(d for d in SKILLS.iterdir() if d.is_dir() and not d.name.startswith("."))
    )

    manifest = check_manifest() if not args else []
    if manifest:
        print("\n  MANIFEST")
        for e in manifest:
            print(f"    ERROR   {e}")

    reports = [validate(d) for d in targets if d.exists()]
    n_err = len(manifest)
    n_warn = 0

    for rep in reports:
        if not rep.errors and not rep.warnings:
            print(f"  ok    {rep.skill}")
            continue
        print(f"\n  {rep.skill}")
        for e in rep.errors:
            print(f"    ERROR   {e}")
        for w in rep.warnings:
            print(f"    warn    {w}")
        n_err += len(rep.errors)
        n_warn += len(rep.warnings)

    print(f"\n{len(reports)} skills · {n_err} errors · {n_warn} warnings")
    if n_err:
        return 1
    if strict and n_warn:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
