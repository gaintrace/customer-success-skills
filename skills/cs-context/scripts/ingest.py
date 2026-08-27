#!/usr/bin/env python3
"""
Ingest whatever the user actually gave you and normalise it.

Real customer success data does not arrive as a clean API payload. It arrives as a CSV
exported from Salesforce with three title rows above the header, an XLSX from finance with
merged cells and a currency column formatted as text, a JSON dump from a warehouse, a
tab-separated file someone saved as .csv, and a second file at a different grain that has to
be joined on a column whose name nobody wrote down.

This script handles that. It sniffs encoding and delimiter, finds the real header row,
maps columns onto the canonical schema with a synonym dictionary, normalises dates, money
and booleans, classifies what entity each file holds, resolves accounts across files, and
reports everything it could not do rather than guessing.

    python3 ingest.py data/*.csv                       # inspect and map
    python3 ingest.py data/*.csv --out normalised.json # write normalised entities
    python3 ingest.py accounts.xlsx --explain          # show every mapping decision
    python3 ingest.py export.csv --map "Cust ID=account_id,MRR=arr"   # override a mapping

Standard library only. No network. Never mutates the input files.

Design rule: this script does not silently coerce. Anything ambiguous is reported with its
confidence and left for a human or the agent to confirm. A wrong column mapping produces a
confidently wrong analysis, which is the failure mode the whole library exists to prevent.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import sys
import unicodedata
import zipfile
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree as ET

# ======================================================================================
# Canonical field vocabulary — see references/normalized-schema.md
# Synonyms are lowercase, punctuation-stripped. Order matters: first match wins, so put
# the specific before the generic ("arr" before "revenue").
# ======================================================================================

FIELD_SYNONYMS: dict[str, list[str]] = {
    "account_id": [
        "account id", "accountid", "acct id", "customer id", "customerid", "cust id",
        "company id", "org id", "organization id", "organisation id", "tenant id",
        "workspace id", "sfdc id", "salesforce id", "crm id", "external id", "client id",
    ],
    "name": [
        "account name", "customer name", "company name", "company", "organization",
        "organisation", "client name", "client", "account", "customer", "name",
    ],
    "arr": [
        "arr", "annual recurring revenue", "annualised recurring revenue",
        "annualized recurring revenue", "contract value", "acv", "annual contract value",
        "annual value", "yearly value", "total contract value", "tcv",
    ],
    "mrr": ["mrr", "monthly recurring revenue", "monthly revenue", "monthly value"],
    "segment": ["segment", "tier", "customer segment", "account segment", "band", "category"],
    "owner_csm": [
        "csm", "customer success manager", "success manager", "account manager", "owner",
        "account owner", "assigned csm", "csm name", "am", "am name", "rep",
    ],
    "status": ["status", "account status", "customer status", "state", "lifecycle stage", "stage"],
    "start_date": [
        "start date", "contract start", "contract start date", "subscription start",
        "customer since", "signup date", "sign up date", "created date", "created at",
        "first payment date", "go live date", "golive date", "onboarded date",
    ],
    "renewal_date": [
        "renewal date", "renewal", "contract end", "contract end date", "end date",
        "expiry date", "expiration date", "expires", "term end", "next renewal",
        "current term end", "subscription end date",
    ],
    "notice_period_days": [
        "notice period", "notice period days", "notice days", "cancellation notice",
        "termination notice", "notice", "opt out days", "opt out period",
    ],
    "auto_renew": [
        "auto renew", "autorenew", "auto renewal", "automatic renewal", "evergreen",
        "auto renew flag", "renews automatically",
    ],
    "seats_purchased": [
        "seats", "seats purchased", "licenses", "licences", "licensed seats",
        "contracted seats", "purchased seats", "quantity", "user limit", "seat count",
        "subscription quantity", "entitlement",
    ],
    "seats_provisioned": [
        "seats provisioned", "provisioned seats", "assigned seats", "assigned licenses",
        "assigned licences", "seats assigned", "users provisioned",
    ],
    "active_users": [
        "active users", "mau", "monthly active users", "wau", "weekly active users",
        "dau", "daily active users", "unique users", "distinct users", "logins",
        "active user count", "users active", "active seats",
    ],
    "plan": ["plan", "tier name", "product", "sku", "package", "edition", "subscription plan"],
    "term": ["term", "billing period", "billing frequency", "contract term", "term length"],
    "discount_pct": ["discount", "discount pct", "discount percent", "discount %", "discount rate"],
    "industry": ["industry", "vertical", "sector"],
    "employee_count": ["employees", "employee count", "headcount", "company size", "size"],
    "country": ["country", "region", "geo", "territory", "location"],
    "health_score": ["health score", "health", "healthscore", "score", "risk score", "churn score"],
    "nps": ["nps", "net promoter score", "nps score"],
    "csat": ["csat", "satisfaction", "satisfaction score", "customer satisfaction"],
    # contact
    "contact_id": ["contact id", "contactid", "user id", "userid", "person id"],
    "email": ["email", "email address", "e mail", "contact email", "user email", "primary email"],
    "title": ["title", "job title", "role title", "position"],
    "role": ["role", "contact role", "persona", "buyer role", "relationship"],
    "last_seen_product": ["last seen", "last login", "last active", "last activity", "last seen at"],
    # tickets
    "ticket_id": ["ticket id", "ticketid", "case id", "case number", "issue id", "conversation id"],
    "created_at": ["created", "created at", "created date", "opened", "opened at", "date created"],
    "resolved_at": ["resolved", "resolved at", "closed at", "closed date", "date closed"],
    "priority": ["priority", "severity", "urgency", "sev"],
    "ticket_type": ["type", "ticket type", "case type", "issue type", "category"],
    "satisfaction": ["satisfaction rating", "csat rating", "ticket satisfaction", "rating"],
    # invoices
    "invoice_id": ["invoice id", "invoice number", "invoice", "inv no"],
    "amount": ["amount", "total", "invoice amount", "value", "revenue", "price", "charge"],
    "due_at": ["due date", "due at", "payment due"],
    "paid_at": ["paid date", "paid at", "payment date", "date paid"],
    # interactions
    "interaction_type": ["activity type", "interaction type", "meeting type", "channel"],
    "timestamp": ["timestamp", "date", "datetime", "activity date", "occurred at", "when"],
    # opportunities
    "opportunity_id": ["opportunity id", "opp id", "deal id"],
    "close_date": ["close date", "expected close", "forecast close date"],
    "forecast_category": ["forecast category", "forecast", "commit category"],
}

# Which canonical fields imply which entity. Used to classify a file by what it contains.
ENTITY_SIGNATURES: dict[str, tuple[set[str], set[str]]] = {
    #                      strong indicators                        supporting
    "subscription": ({"renewal_date", "auto_renew", "notice_period_days", "term"},
                     {"arr", "mrr", "seats_purchased", "plan", "start_date", "discount_pct"}),
    "ticket":       ({"ticket_id", "priority", "resolved_at"},
                     {"created_at", "satisfaction", "ticket_type"}),
    "invoice":      ({"invoice_id", "due_at", "paid_at"}, {"amount", "status"}),
    "contact":      ({"email", "contact_id", "title"}, {"name", "role", "last_seen_product"}),
    "opportunity":  ({"opportunity_id", "close_date", "forecast_category"}, {"amount", "status"}),
    "interaction":  ({"interaction_type"}, {"timestamp", "email"}),
    "usage_daily":  ({"active_users"}, {"timestamp", "created_at"}),
    "account":      ({"account_id"}, {"name", "arr", "segment", "owner_csm", "industry"}),
}

NULLISH = {"", "-", "--", "n/a", "na", "none", "null", "nil", "#n/a", "#null!",
           "not available", "unknown", "tbd", "?", "."}

TRUEISH = {"true", "t", "yes", "y", "1", "on", "enabled", "active", "✓", "x", "checked"}
FALSEISH = {"false", "f", "no", "n", "0", "off", "disabled", "inactive", "✗", "unchecked"}

DATE_FORMATS = [
    "%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%m-%d-%Y",
    "%d.%m.%Y", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%SZ",
    "%d %b %Y", "%d %B %Y", "%b %d, %Y", "%B %d, %Y", "%b %d %Y", "%B %d %Y",
    "%d-%b-%Y", "%d-%b-%y", "%m/%d/%y", "%d/%m/%y", "%Y%m%d",
]

CURRENCY_CHARS = "$£€¥₹R$CHFkr zł₽₺A$C$NZ$S$HK$"


# ======================================================================================
# Reading — encoding, delimiter, header detection, XLSX
# ======================================================================================

def read_text(path: Path) -> tuple[str, str]:
    """Return (text, encoding). Tries the encodings that actually show up in CS exports."""
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "utf-16", "cp1252", "latin-1"):
        try:
            return raw.decode(enc), enc
        except (UnicodeDecodeError, UnicodeError):
            continue
    return raw.decode("latin-1", errors="replace"), "latin-1 (with replacements)"


def sniff_delimiter(sample: str) -> str:
    """csv.Sniffer is fragile on real exports; count candidates on the densest lines instead."""
    lines = [l for l in sample.splitlines()[:50] if l.strip()][:20]
    if not lines:
        return ","
    best, best_score = ",", -1.0
    for delim in [",", "\t", ";", "|"]:
        counts = [l.count(delim) for l in lines]
        if not counts or max(counts) == 0:
            continue
        mode = Counter(counts).most_common(1)[0]
        # Reward a high, consistent field count.
        score = mode[0] * (mode[1] / len(counts))
        if score > best_score:
            best, best_score = delim, score
    return best


def find_header_row(rows: list[list[str]]) -> int:
    """
    Exports routinely carry title rows, blank rows, filter descriptions and a report date
    above the real header. Score each of the first 20 rows on how header-like it is.
    """
    best_idx, best_score = 0, -1.0
    for i, row in enumerate(rows[:20]):
        cells = [c.strip() for c in row]
        filled = [c for c in cells if c]
        if len(filled) < 2:
            continue
        score = 0.0
        score += len(filled) / max(len(cells), 1) * 2          # mostly populated
        score += sum(1 for c in filled if not _looks_numeric(c)) / len(filled) * 2  # words not numbers
        score += sum(1 for c in filled if canonical_for(c)[0]) / len(filled) * 4    # recognisable names
        if len(set(filled)) == len(filled):
            score += 1                                          # unique headers
        if i + 1 < len(rows) and len(rows[i + 1]) == len(row):
            score += 1                                          # next row same width
        if score > best_score:
            best_idx, best_score = i, score
    return best_idx


def _looks_numeric(s: str) -> bool:
    return bool(re.fullmatch(r"[\s\d,.\-+()%$£€]+", s.strip())) and any(ch.isdigit() for ch in s)


def read_xlsx(path: Path) -> list[list[str]]:
    """
    Minimal XLSX reader — zipfile + ElementTree, no third-party dependency.
    Handles shared strings, inline strings, and the Excel serial date epoch.
    Reads the first worksheet only; --sheet selects another.
    """
    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    with zipfile.ZipFile(path) as z:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall(f"{ns}si"):
                shared.append("".join(t.text or "" for t in si.iter(f"{ns}t")))

        sheets = sorted(n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml$", n))
        if not sheets:
            raise ValueError("no worksheet found in workbook")
        root = ET.fromstring(z.read(sheets[0]))

        rows: list[list[str]] = []
        for row in root.iter(f"{ns}row"):
            cells: dict[int, str] = {}
            for c in row.findall(f"{ns}c"):
                ref = c.get("r", "")
                col = _col_index(re.match(r"[A-Z]+", ref).group(0)) if re.match(r"[A-Z]+", ref) else len(cells)
                t = c.get("t")
                v = c.find(f"{ns}v")
                if t == "s" and v is not None:
                    val = shared[int(v.text)] if v.text and int(v.text) < len(shared) else ""
                elif t == "inlineStr":
                    is_el = c.find(f"{ns}is")
                    val = "".join(x.text or "" for x in is_el.iter(f"{ns}t")) if is_el is not None else ""
                else:
                    val = v.text if v is not None and v.text is not None else ""
                cells[col] = val
            width = max(cells) + 1 if cells else 0
            rows.append([cells.get(i, "") for i in range(width)])
        return rows


def _col_index(letters: str) -> int:
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


# ======================================================================================
# Column mapping
# ======================================================================================

def normalise_header(h: str) -> str:
    h = unicodedata.normalize("NFKD", h)
    h = re.sub(r"\(.*?\)", " ", h)                    # drop "(USD)", "(days)"
    h = re.sub(r"[^\w\s]", " ", h)
    h = re.sub(r"_+", " ", h)
    h = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", h)        # camelCase → camel Case
    return re.sub(r"\s+", " ", h).strip().lower()


def canonical_for(header: str) -> tuple[str | None, float, str]:
    """Return (canonical_field, confidence 0-1, why)."""
    h = normalise_header(header)
    if not h:
        return None, 0.0, "empty header"

    for field, syns in FIELD_SYNONYMS.items():
        if h == field.replace("_", " ") or h in syns:
            return field, 1.0, f"exact match on '{h}'"

    # Substring, longest synonym first so "annual recurring revenue" beats "revenue".
    best: tuple[str | None, float, str] = (None, 0.0, "no match")
    for field, syns in FIELD_SYNONYMS.items():
        for syn in sorted(syns, key=len, reverse=True):
            if syn in h or h in syn:
                conf = len(syn) / max(len(h), len(syn))
                if conf > best[1]:
                    best = (field, round(min(conf, 0.85), 2), f"substring '{syn}' in '{h}'")
    if best[0]:
        return best

    # Token overlap as a last resort — deliberately capped low so it always gets reviewed.
    h_tokens = set(h.split())
    for field, syns in FIELD_SYNONYMS.items():
        for syn in syns:
            s_tokens = set(syn.split())
            if not s_tokens:
                continue
            overlap = len(h_tokens & s_tokens) / len(s_tokens)
            if overlap >= 0.6 and overlap * 0.6 > best[1]:
                best = (field, round(overlap * 0.6, 2), f"token overlap with '{syn}'")
    return best


# ======================================================================================
# Value normalisation
# ======================================================================================

def is_null(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v.strip().lower() in NULLISH)


def parse_money(v: Any) -> tuple[float | None, str | None]:
    """
    Handles $1,234.56 · 1.234,56 € · (500) for negative · 1.2k · 3.4M · text-formatted cells.
    Returns (value, currency_symbol_if_seen).
    """
    if is_null(v):
        return None, None
    if isinstance(v, (int, float)):
        return float(v), None
    s = str(v).strip()
    cur = next((c for c in "$£€¥₹" if c in s), None)
    neg = s.startswith("(") and s.endswith(")") or s.startswith("-")
    s = re.sub(r"[^\d.,kKmMbB-]", "", s)
    mult = 1.0
    if s and s[-1] in "kK":
        mult, s = 1e3, s[:-1]
    elif s and s[-1] in "mM":
        mult, s = 1e6, s[:-1]
    elif s and s[-1] in "bB":
        mult, s = 1e9, s[:-1]
    if not s or s in {"-", ".", ","}:
        return None, cur
    # Decide which separator is the decimal point.
    if "," in s and "." in s:
        s = s.replace(",", "") if s.rfind(".") > s.rfind(",") else s.replace(".", "").replace(",", ".")
    elif "," in s:
        parts = s.split(",")
        s = s.replace(",", ".") if len(parts[-1]) == 2 and len(parts) == 2 else s.replace(",", "")
    try:
        val = float(s) * mult
    except ValueError:
        return None, cur
    return (-abs(val) if neg else val), cur


def parse_date(v: Any, dayfirst_hint: bool | None = None) -> tuple[str | None, str | None]:
    """Return (ISO date, ambiguity_note). Ambiguity is reported, never silently resolved."""
    if is_null(v):
        return None, None
    if isinstance(v, (int, float)) or (isinstance(v, str) and re.fullmatch(r"\d{5}", str(v).strip())):
        # Excel serial date. 1899-12-30 epoch accounts for the 1900 leap-year bug.
        try:
            n = int(float(v))
            if 20000 < n < 60000:
                return (date(1899, 12, 30).toordinal() + n and
                        date.fromordinal(date(1899, 12, 30).toordinal() + n).isoformat()), None
        except (ValueError, OverflowError):
            pass
    s = str(v).strip()
    for fmt in DATE_FORMATS:
        try:
            d = datetime.strptime(s, fmt).date()
            note = None
            m = re.match(r"^(\d{1,2})[/\-.](\d{1,2})[/\-.]", s)
            if m and int(m.group(1)) <= 12 and int(m.group(2)) <= 12 and int(m.group(1)) != int(m.group(2)):
                note = (f"ambiguous D/M vs M/D in '{s}' — read as "
                        f"{'day-first' if fmt.startswith('%d') else 'month-first'}; confirm the source locale")
            return d.isoformat(), note
        except ValueError:
            continue
    return None, f"unparseable date '{s}'"


def parse_bool(v: Any) -> bool | None:
    if is_null(v):
        return None
    s = str(v).strip().lower()
    if s in TRUEISH:
        return True
    if s in FALSEISH:
        return False
    return None


def parse_int(v: Any) -> int | None:
    val, _ = parse_money(v)
    return int(round(val)) if val is not None else None


NUMERIC_FIELDS = {"arr", "mrr", "amount", "discount_pct", "health_score", "nps", "csat"}
INT_FIELDS = {"seats_purchased", "seats_provisioned", "active_users",
              "notice_period_days", "employee_count"}
DATE_FIELDS = {"start_date", "renewal_date", "created_at", "resolved_at", "due_at",
               "paid_at", "close_date", "timestamp", "last_seen_product"}
BOOL_FIELDS = {"auto_renew"}


def coerce(field: str, raw: Any) -> tuple[Any, str | None]:
    if is_null(raw):
        return None, None
    if field in DATE_FIELDS:
        return parse_date(raw)
    if field in BOOL_FIELDS:
        b = parse_bool(raw)
        return b, (None if b is not None else f"unrecognised boolean '{raw}'")
    if field in INT_FIELDS:
        n = parse_int(raw)
        return n, (None if n is not None else f"unrecognised integer '{raw}'")
    if field in NUMERIC_FIELDS:
        val, cur = parse_money(raw)
        note = None
        if val is None:
            note = f"unrecognised number '{raw}'"
        elif field == "discount_pct" and val > 1 and "%" in str(raw):
            val = val / 100.0
        return val, note
    return str(raw).strip(), None


# ======================================================================================
# File processing
# ======================================================================================

class Ingested:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.encoding = ""
        self.delimiter = ""
        self.header_row = 0
        self.headers: list[str] = []
        self.mapping: dict[str, tuple[str | None, float, str]] = {}
        self.entity = "unknown"
        self.entity_confidence = 0.0
        self.records: list[dict[str, Any]] = []
        self.issues: list[str] = []
        self.notes: Counter = Counter()
        self.row_count = 0
        self.skipped_rows = 0


def load_rows(path: Path, ing: Ingested) -> list[list[str]]:
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xlsm"}:
        ing.encoding = "xlsx"
        ing.delimiter = "n/a"
        return read_xlsx(path)
    if suffix == ".xls":
        raise ValueError("legacy .xls is not supported — re-save as .xlsx or .csv")

    text, enc = read_text(path)
    ing.encoding = enc

    if suffix in {".json", ".ndjson", ".jsonl"} or text.lstrip()[:1] in "[{":
        ing.delimiter = "json"
        return json_to_rows(text, ing)

    ing.delimiter = sniff_delimiter(text[:20000])
    return list(csv.reader(io.StringIO(text), delimiter=ing.delimiter))


def json_to_rows(text: str, ing: Ingested) -> list[list[str]]:
    """Flatten a JSON array / NDJSON / {data:[...]} envelope into header+rows."""
    objs: list[dict] = []
    stripped = text.strip()
    try:
        data = json.loads(stripped)
        if isinstance(data, list):
            objs = [o for o in data if isinstance(o, dict)]
        elif isinstance(data, dict):
            for key in ("data", "results", "records", "rows", "items", "accounts", "value"):
                if isinstance(data.get(key), list):
                    objs = [o for o in data[key] if isinstance(o, dict)]
                    break
            else:
                objs = [data]
    except json.JSONDecodeError:
        for line in stripped.splitlines():                     # NDJSON
            line = line.strip()
            if not line:
                continue
            try:
                o = json.loads(line)
                if isinstance(o, dict):
                    objs.append(o)
            except json.JSONDecodeError:
                ing.skipped_rows += 1
    if not objs:
        raise ValueError("no JSON objects found")

    flat = [_flatten(o) for o in objs]
    keys: list[str] = []
    for f in flat:
        for k in f:
            if k not in keys:
                keys.append(k)
    return [keys] + [[_stringify(f.get(k)) for k in keys] for f in flat]


def _flatten(o: dict, prefix: str = "", depth: int = 0) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in o.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict) and depth < 3:
            out.update(_flatten(v, f"{key}.", depth + 1))
        else:
            out[key] = v
    return out


def _stringify(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, (list, dict)):
        return json.dumps(v, separators=(",", ":"))
    return str(v)


def classify(fields: set[str]) -> tuple[str, float]:
    best, best_score = "unknown", 0.0
    for entity, (strong, supporting) in ENTITY_SIGNATURES.items():
        s = len(fields & strong) * 2 + len(fields & supporting)
        denom = len(strong) * 2 + len(supporting)
        score = s / denom if denom else 0
        if fields & strong and score > best_score:
            best, best_score = entity, round(score, 2)
    return best, best_score


def ingest_file(path: Path, overrides: dict[str, str]) -> Ingested:
    ing = Ingested(path)
    rows = load_rows(path, ing)
    rows = [r for r in rows if any(str(c).strip() for c in r)]
    if not rows:
        ing.issues.append("file is empty after removing blank rows")
        return ing

    ing.header_row = 0 if ing.delimiter == "json" else find_header_row(rows)
    if ing.header_row > 0:
        ing.notes[f"skipped {ing.header_row} preamble row(s) above the header"] += 1

    ing.headers = [str(h).strip() for h in rows[ing.header_row]]
    body = rows[ing.header_row + 1:]

    for h in ing.headers:
        if h in overrides:
            ing.mapping[h] = (overrides[h], 1.0, "manual override via --map")
        else:
            ing.mapping[h] = canonical_for(h)

    mapped = {m[0] for m in ing.mapping.values() if m[0]}
    ing.entity, ing.entity_confidence = classify(mapped)

    # Duplicate canonical targets are a real hazard: two columns both mapping to `arr`
    # means one of them is wrong, and picking silently is how the wrong number ships.
    targets = Counter(m[0] for m in ing.mapping.values() if m[0])
    for field, n in targets.items():
        if n > 1:
            cols = [h for h, m in ing.mapping.items() if m[0] == field]
            ing.issues.append(
                f"{n} columns map to `{field}` ({', '.join(cols)}) — "
                f"confirm which is authoritative with --map before trusting it"
            )

    width = len(ing.headers)
    for row in body:
        if len(row) != width:
            if len(row) < width:
                row = list(row) + [""] * (width - len(row))
            else:
                ing.skipped_rows += 1
                ing.notes["row wider than header — extra cells dropped"] += 1
                row = row[:width]
        rec: dict[str, Any] = {}
        raw: dict[str, Any] = {}
        for h, cell in zip(ing.headers, row):
            field = ing.mapping[h][0]
            raw[h] = cell
            if not field:
                continue
            val, note = coerce(field, cell)
            if note:
                # Group by the note's shape, not its literal value, so 400 unparseable
                # dates collapse to one line instead of 400.
                ing.notes[re.sub(r"'[^']*'", "'…'", note)] += 1
            if val is not None and (field not in rec or rec[field] in (None, "")):
                rec[field] = val
        if not rec:
            ing.skipped_rows += 1
            continue
        rec["_source_file"] = path.name
        rec["_raw"] = raw
        ing.records.append(rec)

    ing.row_count = len(ing.records)
    return ing


# ======================================================================================
# Cross-file identity resolution and quality
# ======================================================================================

def resolve_identity(files: list[Ingested]) -> dict[str, Any]:
    """Match records to accounts by id, then by normalised name. Report the join rate."""
    by_id: dict[str, str] = {}
    by_name: dict[str, str] = {}
    for f in files:
        if f.entity != "account":
            continue
        for r in f.records:
            aid = str(r.get("account_id") or r.get("name") or "").strip()
            if not aid:
                continue
            if r.get("account_id"):
                by_id[str(r["account_id"]).strip().lower()] = aid
            if r.get("name"):
                by_name[_norm_name(str(r["name"]))] = aid

    joined = unjoined = 0
    unmatched_examples: list[str] = []
    for f in files:
        if f.entity == "account":
            continue
        for r in f.records:
            key = str(r.get("account_id") or "").strip().lower()
            nkey = _norm_name(str(r.get("name") or ""))
            target = by_id.get(key) or by_name.get(nkey)
            if target:
                r["_resolved_account"] = target
                joined += 1
            else:
                unjoined += 1
                if len(unmatched_examples) < 5 and (key or nkey):
                    unmatched_examples.append(r.get("account_id") or r.get("name") or "?")

    total = joined + unjoined
    return {
        "account_records": sum(len(f.records) for f in files if f.entity == "account"),
        "child_records": total,
        "joined": joined,
        "unjoined": unjoined,
        "join_rate": round(joined / total, 3) if total else None,
        "unmatched_examples": unmatched_examples,
    }


def _norm_name(n: str) -> str:
    n = unicodedata.normalize("NFKD", n).lower()
    n = re.sub(r"\b(inc|llc|ltd|limited|corp|corporation|gmbh|plc|sa|bv|pty|co|company|group|holdings)\b", "", n)
    return re.sub(r"[^a-z0-9]", "", n)


def quality_report(files: list[Ingested], identity: dict[str, Any]) -> list[str]:
    """The checks from references/evidence-standard.md, run against what was actually loaded."""
    out: list[str] = []
    all_recs = [r for f in files for r in f.records]

    if identity["join_rate"] is not None:
        rate = identity["join_rate"]
        verdict = "PASS" if rate >= 0.9 else ("WARN" if rate >= 0.8 else "FAIL")
        out.append(f"[{verdict}] identity join rate {rate:.0%} "
                   f"({identity['joined']}/{identity['child_records']} child records resolved to an account)")
        if rate < 0.9 and identity["unmatched_examples"]:
            out.append(f"        unmatched examples: {', '.join(map(str, identity['unmatched_examples']))}")
        if rate < 0.8:
            out.append("        below 0.80 — usage-derived risk scores must be labelled Low confidence; "
                       "the missing records are not randomly distributed")

    # Duplicate accounts
    names = [_norm_name(str(r["name"])) for f in files if f.entity == "account"
             for r in f.records if r.get("name")]
    dupes = [n for n, c in Counter(names).items() if c > 1 and n]
    out.append(f"[{'PASS' if not dupes else 'WARN'}] duplicate account names: {len(dupes)}"
               + (f" — e.g. {', '.join(dupes[:3])}" if dupes else ""))

    # Currency consistency
    currencies = set()
    for f in files:
        for r in f.records:
            for h, cell in (r.get("_raw") or {}).items():
                if f.mapping.get(h, (None,))[0] in NUMERIC_FIELDS:
                    _, cur = parse_money(cell)
                    if cur:
                        currencies.add(cur)
    if len(currencies) > 1:
        out.append(f"[FAIL] mixed currency symbols {sorted(currencies)} — "
                   f"convert to one reporting currency and record the FX rate date")
    elif currencies:
        out.append(f"[PASS] single currency symbol {sorted(currencies)[0]}")

    # Contract completeness — the fields that govern every renewal decision
    subs = [r for f in files if f.entity in {"subscription", "account"} for r in f.records]
    if subs:
        for field, why in [
            ("renewal_date", "no renewal timeline can be built"),
            ("notice_period_days", "the opt-out deadline cannot be computed — "
                                   "renewals are lost on this field being absent"),
            ("auto_renew", "the strongest single commercial risk signal is unavailable"),
            ("arr", "nothing can be ranked or sized in dollars"),
        ]:
            present = sum(1 for r in subs if r.get(field) is not None)
            pct = present / len(subs)
            verdict = "PASS" if pct >= 0.95 else ("WARN" if pct >= 0.7 else "FAIL")
            out.append(f"[{verdict}] `{field}` present on {pct:.0%} of {len(subs)} records"
                       + ("" if pct >= 0.95 else f" — {why}"))

    # History depth
    dates = [r[f] for r in all_recs for f in ("start_date", "created_at", "timestamp")
             if isinstance(r.get(f), str)]
    if dates:
        span_days = (datetime.fromisoformat(max(dates)).date()
                     - datetime.fromisoformat(min(dates)).date()).days
        verdict = "PASS" if span_days >= 365 else ("WARN" if span_days >= 90 else "FAIL")
        out.append(f"[{verdict}] date span {span_days} days ({min(dates)} → {max(dates)})"
                   + ("" if span_days >= 365 else " — under 12 months limits cohort and trend claims"))

    # Unmapped columns carrying real data
    for f in files:
        unmapped = [h for h, m in f.mapping.items() if not m[0] and h.strip()]
        if unmapped:
            out.append(f"[WARN] {f.path.name}: {len(unmapped)} unmapped column(s) — "
                       f"{', '.join(unmapped[:6])}{' …' if len(unmapped) > 6 else ''}")
    return out


# ======================================================================================
# Output
# ======================================================================================

def render(files: list[Ingested], identity: dict[str, Any], explain: bool) -> str:
    o: list[str] = ["# Ingestion Report", ""]

    o.append("## Files")
    o.append("| File | Format | Encoding | Header row | Rows | Entity | Confidence |")
    o.append("|---|---|---|---|---|---|---|")
    for f in files:
        o.append(f"| {f.path.name} | {f.delimiter} | {f.encoding} | {f.header_row + 1} | "
                 f"{f.row_count} | {f.entity} | {f.entity_confidence:.0%} |")
    o.append("")

    o.append("## Column mapping")
    o.append("Anything below 0.80 confidence needs confirming before the numbers are used.")
    o.append("")
    for f in files:
        o.append(f"**{f.path.name}**")
        o.append("")
        o.append("| Source column | → canonical field | Confidence | Why |")
        o.append("|---|---|---|---|")
        for h, (field, conf, why) in f.mapping.items():
            if not h.strip():
                continue
            if field:
                flag = "" if conf >= 0.8 else " ⚠"
                o.append(f"| `{h}` | `{field}`{flag} | {conf:.0%} | {why} |")
            elif explain:
                o.append(f"| `{h}` | — | — | unmapped: {why} |")
        low = [h for h, (fl, c, _) in f.mapping.items() if fl and c < 0.8]
        if low:
            o.append("")
            o.append(f"⚠ **Confirm these before use:** {', '.join(f'`{h}`' for h in low)} — "
                     f"override with `--map \"{low[0]}=<field>\"`.")
        o.append("")

    o.append("## Data quality gate")
    o.append("")
    for line in quality_report(files, identity):
        o.append(f"- {line}")
    o.append("")

    notes = Counter()
    for f in files:
        notes.update(f.notes)
    if notes:
        o.append("## Parsing notes")
        o.append("")
        for note, n in notes.most_common(15):
            o.append(f"- {note} — {n} occurrence(s)")
        o.append("")

    issues = [(f.path.name, i) for f in files for i in f.issues]
    if issues:
        o.append("## Issues requiring a decision")
        o.append("")
        for name, i in issues:
            o.append(f"- **{name}**: {i}")
        o.append("")

    o.append("## What this does NOT tell you")
    o.append("")
    o.append("- Whether the export is complete. A CSV of 40 accounts from a 400-account book looks")
    o.append("  identical to a full export. Confirm the row count against the source system.")
    o.append("- Whether the numbers are current. Nothing here knows when the export was taken —")
    o.append("  ask, and record it as the as-of date on every downstream claim.")
    o.append("- Whether test, internal or sandbox accounts were excluded. Ask for the rule.")
    o.append("- What a column means when its name is ambiguous. `Status` and `Type` are mapped on")
    o.append("  name alone; confirm the value vocabulary before scoring on them.")
    return "\n".join(o)


def main() -> int:
    ap = argparse.ArgumentParser(description="Ingest and normalise arbitrary CS data files.")
    ap.add_argument("paths", nargs="+", help="CSV / TSV / XLSX / JSON / NDJSON files")
    ap.add_argument("--out", help="write normalised records to this JSON file")
    ap.add_argument("--explain", action="store_true", help="show unmapped columns too")
    ap.add_argument("--map", default="", help='overrides, e.g. "Cust ID=account_id,MRR=arr"')
    args = ap.parse_args()

    overrides: dict[str, str] = {}
    for pair in filter(None, (p.strip() for p in args.map.split(","))):
        if "=" not in pair:
            print(f"bad --map entry {pair!r}, expected 'Column=field'", file=sys.stderr)
            return 2
        col, field = pair.split("=", 1)
        if field.strip() not in FIELD_SYNONYMS:
            print(f"unknown canonical field {field!r}. Known: {', '.join(sorted(FIELD_SYNONYMS))}",
                  file=sys.stderr)
            return 2
        overrides[col.strip()] = field.strip()

    files: list[Ingested] = []
    for p in args.paths:
        path = Path(p)
        if not path.exists():
            print(f"[skip] {p} does not exist", file=sys.stderr)
            continue
        try:
            files.append(ingest_file(path, overrides))
        except Exception as e:                                  # noqa: BLE001 — report, never abort the batch
            ing = Ingested(path)
            ing.issues.append(f"could not read: {type(e).__name__}: {e}")
            files.append(ing)

    if not files:
        print("no readable files", file=sys.stderr)
        return 1

    identity = resolve_identity(files)
    print(render(files, identity, args.explain))

    if args.out:
        payload: dict[str, list[dict]] = defaultdict(list)
        for f in files:
            for r in f.records:
                r.pop("_raw", None)
                payload[f.entity].append(r)
        Path(args.out).write_text(json.dumps(payload, indent=2, default=str))
        print(f"\nWrote {sum(len(v) for v in payload.values())} records to {args.out}")

    hard_fail = any("[FAIL]" in l for l in quality_report(files, identity))
    return 1 if hard_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
