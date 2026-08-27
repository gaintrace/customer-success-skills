#!/usr/bin/env python3
"""
Pre-send scan for any customer-facing negotiation draft.

    python3 pre_send_scan.py draft.txt
    ... | python3 pre_send_scan.py

Exit 0 = send-ready. Exit 1 = at least one FAIL. Every FAIL is rewritten, never softened.

Four rules, in the order they are most often broken:

  C13  Announce, do not ask.  The price paragraph carries no question mark and no request
       construction. A price framed as a request invites a counter before the conversation
       starts.
  C3   Say the number, then stop.  Justification precedes the number; the number is the last
       thing in its paragraph. A hedge after a price negotiates against yourself.
  R18  The firewall.  No internal assessment vocabulary reaches the customer.
  4C   The copy block.  No unfilled placeholder. A block containing [Name] is not send-ready.
"""

from __future__ import annotations

import re
import sys

# ── C13 · request and interrogative constructions banned in a price paragraph ────────────
REQUEST_CONSTRUCTIONS = [
    "would you be open to", "how do you feel about", "is there room", "would that work",
    "does that work for you", "would that be acceptable", "are you comfortable with",
    "we were hoping", "we would like to propose", "we'd like to propose", "if you are willing",
    "if you'd be willing", "would you consider", "could we", "can we get", "what do you think",
    "let me know if that", "hoping you might", "any chance",
]

# ── C3 · softeners banned after a price in the same paragraph ────────────────────────────
POST_NUMBER_SOFTENERS = [
    "of course", "that said", "however", "but ", "obviously", "we are flexible",
    "we're flexible", "happy to discuss", "happy to talk", "there is flexibility",
    "there's flexibility", "i know that", "hopefully", "just to say", "no pressure",
    "if that is a problem", "if that's a problem", "we can look at", "we can revisit",
    "open to discussing", "nothing is set in stone",
]

# ── R18 · the never-list. Internal assessment vocabulary. ────────────────────────────────
FIREWALL_TERMS = [
    "at-risk", "at risk", "churn", "health score", "risk band", "arr", "exposure",
    "forecast", "save play", "concession", "walk-away", "walk away", "rung",
    "approval band", "deal desk", "precedent", "coverage tier", "detractor", "atr",
]

PLACEHOLDER = re.compile(r"\[[A-Za-z][A-Za-z /_-]{1,30}\]")
MONEY = re.compile(r"[$£€]\s?\d[\d,.]*\s?(?:k|m|bn)?", re.I)
PCT = re.compile(r"\b\d+(?:\.\d+)?\s?%")
PRICE_WORDS = re.compile(
    r"\b(fee|fees|price|pricing|rate|uplift|increase|renewal term|term is|discount|"
    r"invoice|total|cost)\b", re.I)


def sentences(paragraph: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", paragraph.strip())
    return [p for p in parts if p.strip()]


def is_price_paragraph(p: str) -> bool:
    if MONEY.search(p):
        return True
    return bool(PCT.search(p) and PRICE_WORDS.search(p))


def scan(text: str) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()]

    for m in PLACEHOLDER.finditer(text):
        findings.append(("FAIL", f"4C · unfilled placeholder {m.group(0)} — fill it or drop "
                                 f"the sentence and raise UNKNOWN above the divider"))

    low_all = text.lower()
    for term in FIREWALL_TERMS:
        if re.search(rf"\b{re.escape(term)}\b", low_all):
            findings.append(("FAIL", f"R18 · firewall term '{term}' in customer text — rewrite, "
                                     f"do not soften"))

    for i, para in enumerate(paragraphs):
        if not is_price_paragraph(para):
            continue
        low = para.lower()

        # C13 — announce, do not ask.
        if "?" in para:
            findings.append(("FAIL", "C13 · the price paragraph contains a question mark. "
                                     "A price is announced with a rationale, not requested"))
        for c in REQUEST_CONSTRUCTIONS:
            if c in low:
                findings.append(("FAIL", f"C13 · request construction '{c}' in the price "
                                         f"paragraph — state the number as a decision"))

        # C3 — say the number, then stop.
        sents = sentences(para)
        priced = [n for n, s in enumerate(sents) if MONEY.search(s) or
                  (PCT.search(s) and PRICE_WORDS.search(s))]
        if priced and priced[-1] != len(sents) - 1:
            findings.append(("FAIL", "C3 · the number is not the final sentence of its "
                                     "paragraph. Justification precedes the number; nothing "
                                     "follows it"))
        if priced:
            last = sents[priced[-1]]
            hits = list(MONEY.finditer(last)) or list(PCT.finditer(last))
            tail = last[hits[-1].end():].strip() if hits else ""
            tail_clean = tail.strip(" .!?—-")
            if tail_clean:
                findings.append(("FAIL", f"C3 · text follows the number in the same sentence: "
                                         f"'{tail_clean[:60]}'. Move it in front of the number"))
            for s in POST_NUMBER_SOFTENERS:
                if s in low[low.find(last.lower()):]:
                    findings.append(("FAIL", f"C3 · softener '{s.strip()}' after the price — "
                                             f"the silence does the work"))

        # The paragraph after the price is the second place the number gets negotiated away.
        if i + 1 < len(paragraphs):
            nxt = paragraphs[i + 1].lower()
            for s in POST_NUMBER_SOFTENERS:
                if nxt.startswith(s):
                    findings.append(("WARN", f"C3 · the paragraph after the price opens with "
                                             f"'{s.strip()}' — start a new subject instead"))

    return findings


def main() -> int:
    text = (open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1
            else sys.stdin.read())
    findings = scan(text)
    if not findings:
        print("PASS — send-ready. C13, C3, R18 and the placeholder rule all clear.")
        return 0
    seen: set[str] = set()
    fails = 0
    for level, msg in findings:
        if msg in seen:
            continue
        seen.add(msg)
        print(f"{level}  {msg}")
        fails += level == "FAIL"
    print(f"\n{fails} FAIL · rewrite before sending.")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
