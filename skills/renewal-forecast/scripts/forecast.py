#!/usr/bin/env python3
"""
forecast.py — deterministic renewal-forecast arithmetic for the `renewal-forecast` skill.

Standard library only. No network. Reads one JSON file, prints an auditable report.

    python3 forecast.py --sample > input.json     # emit a documented sample input
    python3 forecast.py input.json                # human-readable report
    python3 forecast.py input.json --json         # machine-readable output

WHAT IT COMPUTES
  1. ATR base, opt-out deadlines, and paper/notice exceptions
  2. Category roll-up (count, ATR, called value, base-rate weighting)
  3. Three views: unweighted ATR / category roll-up / base-rate anchor, and their gaps
  4. Downside / Base / Upside scenarios from explicitly named rate assumptions
  5. The full ARR bridge, opening -> closing, with a reconciliation check row
  6. GRR and NRR, both the cohort (period) method and the ATR (renewal-event) method,
     plus the dollar reconciliation between them
  7. Category movement vs a prior snapshot, as a transition matrix and a row list
  8. Concentration: top-N share, HHI, industry, segment, owner, single-threaded ARR,
     and the zero-out loss simulation for the largest account
  9. The computable half of the sandbag / happy-ears scan

WHAT IT DOES NOT DO
  It does not invent probabilities. Every rate used is supplied in the input under
  `base_rates` and `scenario_rates`; the built-in sample values are UNCALIBRATED
  PLACEHOLDERS and are labelled as such in the output. Replace them with the rates your
  own closed renewals actually realised (>= 4 quarters, >= 30 events per category bin)
  before quoting any weighted number to anyone.

CATEGORIES  closed_won | commit | most_likely | best_case | at_risk | omitted | closed_lost
"""

import argparse
import json
import sys
from datetime import date, datetime, timedelta

CATEGORIES = ["closed_won", "commit", "most_likely", "best_case", "at_risk", "omitted", "closed_lost"]
BASE_CASE_CATEGORIES = ["closed_won", "commit", "most_likely"]
UPSIDE_CATEGORIES = ["best_case"]

MONEY = lambda x: "${:,.0f}".format(x)          # noqa: E731
PCT = lambda x: "—" if x is None else "{:.1f}%".format(x * 100)  # noqa: E731


# ----------------------------------------------------------------------------- helpers
def _d(s):
    if not s:
        return None
    return datetime.strptime(s, "%Y-%m-%d").date()


def _f(row, key, default=0.0):
    v = row.get(key, default)
    return float(v) if v is not None else float(default)


def fail(msg):
    print("INPUT ERROR: " + msg, file=sys.stderr)
    sys.exit(2)


# ------------------------------------------------------------------------------ loading
def load(path):
    with open(path) as fh:
        data = json.load(fh)
    for key in ("period", "renewals"):
        if key not in data:
            fail("missing top-level key '%s'" % key)
    data.setdefault("mid_term", {})
    data.setdefault("prior_snapshot", [])
    data.setdefault("base_rates", {})
    data.setdefault("scenario_rates", {})
    data.setdefault("as_of", date.today().isoformat())
    for r in data["renewals"]:
        for key in ("account_id", "name", "atr", "category"):
            if key not in r:
                fail("renewal %s missing '%s'" % (r.get("account_id", "?"), key))
        if r["category"] not in CATEGORIES:
            fail("renewal %s has unknown category '%s'" % (r["account_id"], r["category"]))
        r.setdefault("called_arr", None)      # None means "not called yet" -> treated as UNKNOWN
        r.setdefault("expansion_arr", 0.0)
        r.setdefault("cross_sell_arr", 0.0)
        r.setdefault("expansion_committed_arr", 0.0)
        r.setdefault("expansion_proposed_arr", 0.0)
        r.setdefault("loss_type", "logo")
        r.setdefault("value_delta_reason", None)
        r.setdefault("churn_reason", None)
        r.setdefault("order_form_issued", None)
        r.setdefault("eb_contact_days", None)
        r.setdefault("distinct_contacts_90d", None)
    return data


def enrich(data):
    """Compute opt-out deadline and days-to-opt-out per renewal."""
    as_of = _d(data["as_of"])
    for r in data["renewals"]:
        rd = _d(r.get("renewal_date"))
        npd = r.get("notice_period_days")
        if rd and npd is not None:
            ood = rd - timedelta(days=int(npd))
            r["opt_out_deadline"] = ood.isoformat()
            r["days_to_opt_out"] = (ood - as_of).days
        else:
            r["opt_out_deadline"] = None      # UNKNOWN - requires the executed contract
            r["days_to_opt_out"] = None
        atr = _f(r, "atr")
        called = r["called_arr"]
        r["called_effective"] = atr if called is None else min(float(called), atr)
        r["value_delta"] = r["called_effective"] - atr
    return data


# ------------------------------------------------------------------------------- rollup
def category_rollup(data):
    rates = data["base_rates"]
    out = {}
    for cat in CATEGORIES:
        rows = [r for r in data["renewals"] if r["category"] == cat]
        atr = sum(_f(r, "atr") for r in rows)
        called = sum(r["called_effective"] for r in rows)
        rate = rates.get(cat)
        out[cat] = {
            "count": len(rows),
            "atr": atr,
            "called": called,
            "expansion": sum(_f(r, "expansion_arr") + _f(r, "cross_sell_arr") for r in rows),
            "base_rate": rate,
            "weighted": (atr * rate) if rate is not None else None,
        }
    total_atr = sum(v["atr"] for v in out.values())
    base_case = sum(out[c]["called"] for c in BASE_CASE_CATEGORIES)
    upside_band = base_case + sum(out[c]["called"] for c in UPSIDE_CATEGORIES)
    anchor_parts = [v["weighted"] for v in out.values() if v["weighted"] is not None]
    return {
        "by_category": out,
        "total_atr": total_atr,
        "total_called": sum(v["called"] for v in out.values()),
        "total_expansion": sum(v["expansion"] for v in out.values()),
        "base_case": base_case,
        "upside_band": upside_band,
        "at_risk_atr": out["at_risk"]["atr"],
        "at_risk_called": out["at_risk"]["called"],
        "base_rate_anchor": sum(anchor_parts) if anchor_parts else None,
        "base_rate_coverage": len(anchor_parts),
    }


# ---------------------------------------------------------------------------- scenarios
DEFAULT_SCENARIO_RATES = {
    # UNCALIBRATED PLACEHOLDERS. Replace with your own realised rates before use.
    "commit_hit_rate": 0.97,
    "most_likely_rate": 0.85,
    "most_likely_downside_rate": 0.70,
    "best_case_conversion": 0.40,
    "at_risk_save_rate": 0.50,
    "at_risk_upside_save_rate": 0.80,
}


def scenarios(data, roll):
    rates = dict(DEFAULT_SCENARIO_RATES)
    rates.update(data.get("scenario_rates") or {})
    supplied = set((data.get("scenario_rates") or {}).keys())
    bc = roll["by_category"]
    exp_called = roll["total_expansion"]
    exp_committed = sum(_f(r, "expansion_committed_arr") for r in data["renewals"])
    exp_proposed = sum(_f(r, "expansion_proposed_arr") for r in data["renewals"])

    down = (bc["closed_won"]["called"]
            + bc["commit"]["called"] * rates["commit_hit_rate"]
            + bc["most_likely"]["called"] * rates["most_likely_downside_rate"]
            + exp_committed)
    base = (bc["closed_won"]["called"]
            + bc["commit"]["called"] * rates["commit_hit_rate"]
            + bc["most_likely"]["called"] * rates["most_likely_rate"]
            + bc["at_risk"]["called"] * rates["at_risk_save_rate"]
            + exp_called)
    up = (bc["closed_won"]["called"]
          + bc["commit"]["called"]
          + bc["most_likely"]["called"]
          + bc["best_case"]["called"] * rates["best_case_conversion"]
          + bc["at_risk"]["called"] * rates["at_risk_upside_save_rate"]
          + exp_called + exp_proposed)
    return {
        "rates": rates,
        "rates_supplied": sorted(supplied),
        "rates_defaulted": sorted(set(rates) - supplied),
        "downside": down,
        "base": base,
        "upside": up,
        "expansion_called": exp_called,
        "expansion_committed": exp_committed,
        "expansion_proposed": exp_proposed,
    }


# ------------------------------------------------------------------------------- bridge
def bridge(data, roll):
    """Classify every renewal into a bridge line, then add mid-term movements."""
    ren_expansion = ren_cross = ren_decrease = ren_prod_churn = ren_logo_churn = 0.0
    for r in data["renewals"]:
        if r["category"] == "omitted":
            continue
        atr, called = _f(r, "atr"), r["called_effective"]
        ren_expansion += _f(r, "expansion_arr")
        ren_cross += _f(r, "cross_sell_arr")
        if called <= 0:
            if r["loss_type"] == "product":
                ren_prod_churn += atr
            else:
                ren_logo_churn += atr
        elif called < atr:
            delta = atr - called
            if r["value_delta_reason"] == "product_removal":
                ren_prod_churn += delta
            else:
                ren_decrease += delta

    mt = data["mid_term"]
    lines = [
        ("Opening ARR", _f(data["period"], "opening_arr"), "="),
        ("New customer ARR", _f(mt, "new_customer_arr"), "+"),
        ("New product ARR (cross-sell)", ren_cross + _f(mt, "cross_sell_arr"), "+"),
        ("Increased product ARR (upsell)", ren_expansion + _f(mt, "expansion_arr"), "+"),
        ("Contracted ramp ARR", _f(mt, "contracted_ramp_arr"), "+"),
        ("Reactivation ARR", _f(mt, "reactivation_arr"), "+"),
        ("Product decrease ARR", -(ren_decrease + _f(mt, "contraction_arr")), "-"),
        ("Churned product ARR", -(ren_prod_churn + _f(mt, "product_churn_arr")), "-"),
        ("Churned customer ARR", -(ren_logo_churn + _f(mt, "churn_arr")), "-"),
        ("FX movement", _f(mt, "fx_arr"), "+/-"),
    ]
    closing = sum(v for _, v, _ in lines)
    lines.append(("Closing ARR", closing, "="))
    return {
        "lines": lines,
        "closing_arr": closing,
        "renewal_event": {
            "expansion": ren_expansion, "cross_sell": ren_cross, "product_decrease": ren_decrease,
            "product_churn": ren_prod_churn, "logo_churn": ren_logo_churn,
        },
    }


# ---------------------------------------------------------------------------- retention
def retention(data, roll, br):
    opening = _f(data["period"], "opening_arr")
    mt = data["mid_term"]
    re_ = br["renewal_event"]

    contraction = re_["product_decrease"] + _f(mt, "contraction_arr")
    churn = re_["product_churn"] + re_["logo_churn"] + _f(mt, "product_churn_arr") + _f(mt, "churn_arr")
    expansion = re_["expansion"] + _f(mt, "expansion_arr")
    cross = re_["cross_sell"] + _f(mt, "cross_sell_arr")
    ramp = _f(mt, "contracted_ramp_arr")

    cohort = {}
    if opening > 0:
        cohort["grr"] = (opening - contraction - churn) / opening
        cohort["nrr"] = (opening + expansion + cross + ramp - contraction - churn) / opening
        cohort["nrr_ex_ramp"] = (opening + expansion + cross - contraction - churn) / opening
    else:
        cohort = {"grr": None, "nrr": None, "nrr_ex_ramp": None}

    atr_total = roll["total_atr"] - roll["by_category"]["omitted"]["atr"]
    retained = sum(r["called_effective"] for r in data["renewals"] if r["category"] != "omitted")
    uplift = re_["expansion"] + re_["cross_sell"]
    atr_method = {
        "atr": atr_total,
        "gross_renewal_rate": (retained / atr_total) if atr_total else None,
        "net_renewal_rate": ((retained + uplift) / atr_total) if atr_total else None,
    }

    logos = [r for r in data["renewals"] if r["category"] != "omitted"]
    lost_logos = [r for r in logos if r["called_effective"] <= 0 and r["loss_type"] == "logo"]
    logo_retention = (len(logos) - len(lost_logos)) / len(logos) if logos else None

    renewal_event_loss = re_["product_decrease"] + re_["product_churn"] + re_["logo_churn"]
    mid_term_loss = (_f(mt, "contraction_arr") + _f(mt, "product_churn_arr") + _f(mt, "churn_arr"))
    return {
        "cohort": cohort,
        "atr_method": atr_method,
        "logo_retention": logo_retention,
        "logos_at_renewal": len(logos),
        "logos_lost": len(lost_logos),
        "contraction": contraction, "churn": churn,
        "expansion": expansion, "cross_sell": cross, "ramp": ramp,
        "renewal_event_loss": renewal_event_loss,
        "mid_term_loss": mid_term_loss,
    }


# ----------------------------------------------------------------------------- movement
def movement(data):
    prior = {p["account_id"]: p for p in data.get("prior_snapshot", [])}
    if not prior:
        return None
    rows, matrix = [], {}
    for r in data["renewals"]:
        p = prior.get(r["account_id"])
        if not p:
            rows.append({"account": r["name"], "from": "(new to snapshot)", "to": r["category"],
                         "called_delta": r["called_effective"], "atr": _f(r, "atr")})
            continue
        pcalled = p.get("called_arr")
        pcalled = _f(r, "atr") if pcalled is None else float(pcalled)
        delta = r["called_effective"] - pcalled
        if p.get("category") != r["category"] or abs(delta) > 0.5:
            rows.append({"account": r["name"], "from": p.get("category"), "to": r["category"],
                         "called_delta": delta, "atr": _f(r, "atr")})
        key = "%s -> %s" % (p.get("category"), r["category"])
        matrix[key] = matrix.get(key, 0.0) + _f(r, "atr")
    prior_called = sum((_f(p, "called_arr") if p.get("called_arr") is not None else 0.0)
                       for p in data["prior_snapshot"])
    now_called = sum(r["called_effective"] for r in data["renewals"]
                     if r["account_id"] in prior)
    rows.sort(key=lambda x: x["called_delta"])
    return {"rows": rows, "matrix": matrix,
            "prior_called": prior_called, "now_called": now_called,
            "net_change": now_called - prior_called}


# ------------------------------------------------------------------------ concentration
def _share_table(data, field):
    totals = {}
    for r in data["renewals"]:
        if r["category"] == "omitted":
            continue
        totals[r.get(field) or "UNKNOWN"] = totals.get(r.get(field) or "UNKNOWN", 0.0) + _f(r, "atr")
    return sorted(totals.items(), key=lambda kv: -kv[1])


def concentration(data, roll, ret):
    rows = [r for r in data["renewals"] if r["category"] != "omitted"]
    total = sum(_f(r, "atr") for r in rows) or 1.0
    ranked = sorted(rows, key=lambda r: -_f(r, "atr"))
    shares = [_f(r, "atr") / total for r in ranked]
    hhi = sum((s * 100) ** 2 for s in shares)
    single_threaded = sum(_f(r, "atr") for r in rows
                          if r.get("distinct_contacts_90d") is not None
                          and r["distinct_contacts_90d"] <= 1)

    top = ranked[0] if ranked else None
    sim = None
    if top:
        opening = _f(data["period"], "opening_arr")
        lost = top["called_effective"]
        sim = {
            "account": top["name"],
            "atr": _f(top, "atr"),
            "base_case_delta": -lost,
            "grr_after": ((opening - ret["contraction"] - ret["churn"] - lost) / opening)
            if opening > 0 else None,
        }
    return {
        "total_atr": total,
        "top1": shares[0] if shares else None,
        "top5": sum(shares[:5]),
        "top10": sum(shares[:10]),
        "hhi": hhi,
        "by_industry": _share_table(data, "industry"),
        "by_segment": _share_table(data, "segment"),
        "by_owner": _share_table(data, "owner"),
        "single_threaded_atr": single_threaded,
        "single_threaded_share": single_threaded / total,
        "ranked": [(r["name"], _f(r, "atr"), _f(r, "atr") / total) for r in ranked],
        "zero_out": sim,
        "breaches": {
            "top1_over_10pct": bool(shares and shares[0] > 0.10),
            "top5_over_40pct": sum(shares[:5]) > 0.40,
            "hhi_over_1500": hhi > 1500,
            "industry_over_25pct": bool(_share_table(data, "industry")
                                        and _share_table(data, "industry")[0][1] / total > 0.25),
        },
    }


# ---------------------------------------------------------------------------- bias scan
def bias_scan(data, roll):
    rows = [r for r in data["renewals"] if r["category"] != "omitted"]
    at_atr = sum(_f(r, "atr") for r in rows)
    exact = [r for r in rows if abs(r["value_delta"]) < 0.5]
    no_reason = [r for r in rows if r["called_effective"] > 0 and r["value_delta"] < -0.5
                 and not r["value_delta_reason"]]
    churn_no_code = [r for r in rows if r["called_effective"] <= 0 and not r.get("churn_reason")]
    commit_no_paper = [r for r in rows if r["category"] == "commit"
                       and r.get("days_to_opt_out") is not None and r["days_to_opt_out"] <= 45
                       and r.get("order_form_issued") is False]
    commit_no_eb = [r for r in rows if r["category"] == "commit"
                    and (r.get("eb_contact_days") is None or r["eb_contact_days"] > 30)]
    past_deadline = [r for r in rows if r.get("days_to_opt_out") is not None
                     and r["days_to_opt_out"] < 0
                     and r["category"] in ("commit", "most_likely", "best_case")
                     and r.get("order_form_issued") is not True]
    null_notice = [r for r in rows if r["opt_out_deadline"] is None]
    return {
        "atr_in_scope": at_atr,
        "called_equals_atr_share": (sum(_f(r, "atr") for r in exact) / at_atr) if at_atr else None,
        "value_cut_without_reason": ["%s (%s)" % (r["name"], MONEY(r["value_delta"])) for r in no_reason],
        "full_churn_without_cause_code": [r["name"] for r in churn_no_code],
        "commit_inside_t45_no_order_form": [r["name"] for r in commit_no_paper],
        "commit_without_eb_contact_30d": [r["name"] for r in commit_no_eb],
        "held_above_at_risk_past_opt_out": [r["name"] for r in past_deadline],
        "null_notice_period": [r["name"] for r in null_notice],
    }


# ------------------------------------------------------------------------------ reports
def line(ch="-", n=92):
    return ch * n


def report(data, res):
    p = data["period"]
    roll, sc, br, ret, mv, con, bias = (res["rollup"], res["scenarios"], res["bridge"],
                                        res["retention"], res["movement"], res["concentration"],
                                        res["bias"])
    o = []
    A = o.append
    A(line("="))
    A("RENEWAL FORECAST — %s  (%s → %s)   snapshot %s" %
      (p.get("label", "period"), p.get("start", "?"), p.get("end", "?"), data["as_of"]))
    A(line("="))
    A("ATR                        %s across %d renewals" % (MONEY(roll["total_atr"]), len(data["renewals"])))
    A("Called renewal ARR         %s" % MONEY(roll["total_called"]))
    A("Base case (Closed+Commit+Most Likely)  %s" % MONEY(roll["base_case"]))
    A("Upside band (+ Best Case)              %s" % MONEY(roll["upside_band"]))
    A("At Risk exposure           %s ATR, called %s" % (MONEY(roll["at_risk_atr"]), MONEY(roll["at_risk_called"])))
    A("Expansion at renewal       %s called / %s proposed" % (MONEY(sc["expansion_called"]), MONEY(sc["expansion_proposed"])))
    A("")
    A("1. CATEGORY ROLL-UP");  A(line())
    A("%-14s %5s %14s %14s %10s %14s" % ("category", "n", "ATR", "called", "base rate", "weighted"))
    for cat in CATEGORIES:
        v = roll["by_category"][cat]
        if v["count"] == 0:
            continue
        A("%-14s %5d %14s %14s %10s %14s" % (cat, v["count"], MONEY(v["atr"]), MONEY(v["called"]),
          PCT(v["base_rate"]), MONEY(v["weighted"]) if v["weighted"] is not None else "—"))
    A("")
    A("2. THREE VIEWS");  A(line())
    A("%-24s %16s   %s" % ("unweighted ATR", MONEY(roll["total_atr"]), "motion capacity, not revenue"))
    A("%-24s %16s   %s" % ("category roll-up (base)", MONEY(roll["base_case"]), "the number you defend"))
    anchor = roll["base_rate_anchor"]
    A("%-24s %16s   %s" % ("base-rate anchor", MONEY(anchor) if anchor is not None else "UNKNOWN — requires base rates",
                           "the floor the human call must beat"))
    if anchor is not None:
        gap = roll["base_case"] - anchor
        A("    gap (base case − anchor): %s  %s" % (MONEY(gap),
          "human call is ABOVE the anchor — name the accounts" if gap > 0 else
          "human call is BELOW the anchor — check for sandbagging"))
    A("")
    A("3. SCENARIOS");  A(line())
    A("%-10s %16s   %s" % ("downside", MONEY(sc["downside"]), "Commit at hit rate, ML at downside rate, Best/At-Risk at 0"))
    A("%-10s %16s   %s" % ("base", MONEY(sc["base"]), "Commit at hit rate, ML at observed rate, At Risk at save rate"))
    A("%-10s %16s   %s" % ("upside", MONEY(sc["upside"]), "Commit/ML at 100%, Best Case converted, saves above base"))
    A("    rates supplied by input : %s" % (", ".join(sc["rates_supplied"]) or "none"))
    A("    rates DEFAULTED (uncalibrated placeholders — replace before quoting): %s"
      % (", ".join(sc["rates_defaulted"]) or "none"))
    A("")
    A("4. ARR BRIDGE");  A(line())
    for name, val, sign in br["lines"]:
        A("%-32s %5s %16s" % (name, sign, MONEY(abs(val)) if sign == "-" else MONEY(val)))
    A("")
    A("5. RETENTION");  A(line())
    c = ret["cohort"]
    A("cohort method   GRR %s   NRR %s   (NRR ex contracted ramp %s)"
      % (PCT(c["grr"]), PCT(c["nrr"]), PCT(c["nrr_ex_ramp"])))
    A("ATR method      gross renewal rate %s   net renewal rate %s   (ATR %s)"
      % (PCT(ret["atr_method"]["gross_renewal_rate"]), PCT(ret["atr_method"]["net_renewal_rate"]),
         MONEY(ret["atr_method"]["atr"])))
    A("logo retention  %s  (%d of %d logos reaching a renewal decision lost)"
      % (PCT(ret["logo_retention"]) if ret["logo_retention"] is not None else "UNKNOWN — no renewals in scope",
         ret["logos_lost"], ret["logos_at_renewal"]))
    A("reconciliation  renewal-event loss %s + mid-term loss %s = total period loss %s"
      % (MONEY(ret["renewal_event_loss"]), MONEY(ret["mid_term_loss"]),
         MONEY(ret["renewal_event_loss"] + ret["mid_term_loss"])))
    A("")
    if mv:
        A("6. MOVEMENT VS PRIOR SNAPSHOT");  A(line())
        A("net change in called ARR: %s" % MONEY(mv["net_change"]))
        for r in mv["rows"]:
            A("  %-26s %-13s -> %-13s  called Δ %14s" % (r["account"][:26], r["from"], r["to"], MONEY(r["called_delta"])))
        A("")
    A("7. CONCENTRATION");  A(line())
    if not con["ranked"]:
        A("No forecastable renewals in scope — concentration UNKNOWN.")
    else:
        A("top 1 %s   top 5 %s   top 10 %s   HHI %s"
          % (PCT(con["top1"]), PCT(con["top5"]), PCT(con["top10"]), "{:,.0f}".format(con["hhi"])))
        top_ind = con["by_industry"][0] if con["by_industry"] else ("UNKNOWN", 0.0)
        A("largest industry: %s %s" % (top_ind[0], PCT(top_ind[1] / con["total_atr"])))
        A("single-threaded ATR: %s (%s)" % (MONEY(con["single_threaded_atr"]), PCT(con["single_threaded_share"])))
    brc = con["breaches"]
    A("conventions breached: " + (", ".join(k for k, v in brc.items() if v) or "none"))
    if con["zero_out"]:
        z = con["zero_out"]
        A("zero-out simulation: if %s renews at zero, base case falls by %s and cohort GRR falls to %s"
          % (z["account"], MONEY(-z["base_case_delta"]), PCT(z["grr_after"])))
    A("")
    A("8. BIAS SCAN (computable checks only)");  A(line())
    A("share of ATR where called value exactly equals ATR: %s" % PCT(bias["called_equals_atr_share"]))
    for label, key in [("value cut with no delta reason", "value_cut_without_reason"),
                       ("full churn with no cause code", "full_churn_without_cause_code"),
                       ("Commit inside T-45 with no order form", "commit_inside_t45_no_order_form"),
                       ("Commit without EB contact <=30d", "commit_without_eb_contact_30d"),
                       ("held above At Risk past opt-out deadline", "held_above_at_risk_past_opt_out"),
                       ("null notice period (cannot enter Commit)", "null_notice_period")]:
        vals = bias[key]
        A("  %-42s %s" % (label, (", ".join(str(v) for v in vals) if vals else "none")))
    A("")
    A(line("="))
    A("All rates above are inputs, not measurements. Confidence is capped by the Coverage Ledger,")
    A("not by this script. No probability here is calibrated unless your input rates were backtested.")
    return "\n".join(o)


def compute(data):
    enrich(data)
    roll = category_rollup(data)
    br = bridge(data, roll)
    ret = retention(data, roll, br)
    return {
        "rollup": roll,
        "scenarios": scenarios(data, roll),
        "bridge": br,
        "retention": ret,
        "movement": movement(data),
        "concentration": concentration(data, roll, ret),
        "bias": bias_scan(data, roll),
    }


# ------------------------------------------------------------------------------- sample
SAMPLE = {
    "as_of": "2026-11-03",
    "period": {"label": "FY26 Q4", "start": "2026-11-01", "end": "2027-01-31", "opening_arr": 42800000},
    "base_rates": {"closed_won": 1.00, "commit": 0.97, "most_likely": 0.85,
                   "best_case": 0.35, "at_risk": 0.30, "omitted": 0.0},
    "scenario_rates": {},
    "mid_term": {"new_customer_arr": 610000, "expansion_arr": 180000, "cross_sell_arr": 95000,
                 "contraction_arr": 60000, "churn_arr": 140000, "product_churn_arr": 0,
                 "reactivation_arr": 35000, "contracted_ramp_arr": 120000, "fx_arr": -45000},
    "renewals": [
        {"account_id": "A-1001", "name": "Northwind Logistics", "segment": "Enterprise", "industry": "Logistics",
         "owner": "S. Okafor", "atr": 840000, "called_arr": 840000, "category": "commit",
         "expansion_arr": 42000, "value_delta_reason": None, "renewal_date": "2026-12-31",
         "notice_period_days": 90, "order_form_issued": True, "eb_contact_days": 12, "distinct_contacts_90d": 6},
        {"account_id": "A-1002", "name": "Halcyon Health", "segment": "Enterprise", "industry": "Healthcare",
         "owner": "S. Okafor", "atr": 620000, "called_arr": 560000, "category": "most_likely",
         "value_delta_reason": "seat_reduction", "renewal_date": "2027-01-15",
         "notice_period_days": 60, "order_form_issued": False, "eb_contact_days": 40, "distinct_contacts_90d": 4},
        {"account_id": "A-1003", "name": "Pemberton Financial", "segment": "Enterprise", "industry": "Financial Services",
         "owner": "R. Nakamura", "atr": 540000, "called_arr": 0, "category": "at_risk", "loss_type": "logo",
         "churn_reason": "vendor_consolidation", "renewal_date": "2027-01-31",
         "notice_period_days": 90, "order_form_issued": False, "eb_contact_days": 120, "distinct_contacts_90d": 1},
        {"account_id": "A-1004", "name": "Kestrel Analytics", "segment": "Mid-Market", "industry": "Software",
         "owner": "R. Nakamura", "atr": 180000, "called_arr": 180000, "category": "commit",
         "cross_sell_arr": 30000, "renewal_date": "2026-12-15", "notice_period_days": 30,
         "order_form_issued": True, "eb_contact_days": 8, "distinct_contacts_90d": 5},
        {"account_id": "A-1005", "name": "Foxglove Retail", "segment": "Mid-Market", "industry": "Retail",
         "owner": "T. Abara", "atr": 145000, "called_arr": 145000, "category": "best_case",
         "expansion_arr": 20000, "expansion_proposed_arr": 35000, "renewal_date": "2027-01-20",
         "notice_period_days": 30, "order_form_issued": False, "eb_contact_days": 55, "distinct_contacts_90d": 3},
        {"account_id": "A-1006", "name": "Arden Manufacturing", "segment": "Mid-Market", "industry": "Manufacturing",
         "owner": "T. Abara", "atr": 132000, "called_arr": 132000, "category": "most_likely",
         "renewal_date": "2026-12-20", "notice_period_days": 60, "order_form_issued": False,
         "eb_contact_days": 25, "distinct_contacts_90d": 2},
        {"account_id": "A-1007", "name": "Belvoir Media", "segment": "SMB", "industry": "Media",
         "owner": "T. Abara", "atr": 48000, "called_arr": 24000, "category": "at_risk",
         "value_delta_reason": "product_removal", "renewal_date": "2026-12-05",
         "notice_period_days": 30, "order_form_issued": False, "eb_contact_days": 70, "distinct_contacts_90d": 1},
        {"account_id": "A-1008", "name": "Corvid Labs", "segment": "SMB", "industry": "Software",
         "owner": "T. Abara", "atr": 36000, "called_arr": 36000, "category": "closed_won",
         "renewal_date": "2026-11-10", "notice_period_days": 30, "order_form_issued": True,
         "eb_contact_days": 5, "distinct_contacts_90d": 3},
        {"account_id": "A-1009", "name": "Dunmore Freight", "segment": "Mid-Market", "industry": "Logistics",
         "owner": "S. Okafor", "atr": 96000, "called_arr": 96000, "category": "most_likely",
         "renewal_date": "2027-01-10", "notice_period_days": 60, "order_form_issued": False,
         "eb_contact_days": 30, "distinct_contacts_90d": 4},
        {"account_id": "A-1010", "name": "Eastvale Energy", "segment": "Enterprise", "industry": "Energy",
         "owner": "R. Nakamura", "atr": 410000, "called_arr": 390000, "category": "commit",
         "value_delta_reason": "discount_concession", "renewal_date": "2026-12-31",
         "notice_period_days": 60, "order_form_issued": True, "eb_contact_days": 18, "distinct_contacts_90d": 5}
    ],
    "prior_snapshot": [
        {"account_id": "A-1001", "category": "most_likely", "called_arr": 840000},
        {"account_id": "A-1002", "category": "most_likely", "called_arr": 620000},
        {"account_id": "A-1003", "category": "most_likely", "called_arr": 540000},
        {"account_id": "A-1004", "category": "commit", "called_arr": 180000},
        {"account_id": "A-1005", "category": "best_case", "called_arr": 145000},
        {"account_id": "A-1006", "category": "most_likely", "called_arr": 132000},
        {"account_id": "A-1007", "category": "most_likely", "called_arr": 48000},
        {"account_id": "A-1008", "category": "commit", "called_arr": 36000},
        {"account_id": "A-1009", "category": "most_likely", "called_arr": 96000},
        {"account_id": "A-1010", "category": "commit", "called_arr": 410000}
    ],
}


def main():
    ap = argparse.ArgumentParser(description="Renewal forecast roll-up, ARR bridge, retention, concentration.")
    ap.add_argument("input", nargs="?", help="path to the JSON input file")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    ap.add_argument("--sample", action="store_true", help="print a documented sample input and exit")
    args = ap.parse_args()

    if args.sample:
        print(json.dumps(SAMPLE, indent=2))
        return
    if not args.input:
        ap.error("an input file is required (or use --sample)")

    data = load(args.input)
    res = compute(data)
    if args.json:
        print(json.dumps(res, indent=2, default=str))
    else:
        print(report(data, res))


if __name__ == "__main__":
    main()
