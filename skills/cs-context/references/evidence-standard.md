# The Evidence Standard

> Read this before writing any customer success artifact. It is the difference between an
> analysis a Chief Customer Officer acts on and one they quietly stop reading.

**Contents**
1. [Why this exists](#1-why-this-exists)
2. [Provenance tags](#2-provenance-tags)
3. [The three evidence tiers](#3-the-three-evidence-tiers)
4. [Confidence levels and their entry criteria](#4-confidence-levels-and-their-entry-criteria)
5. [The Coverage Ledger](#5-the-coverage-ledger)
6. [Stating probability without false precision](#6-stating-probability-without-false-precision)
7. [Recency, staleness and decay](#7-recency-staleness-and-decay)
8. [Contradiction handling](#8-contradiction-handling)
9. [Internal vs customer-facing language](#9-internal-vs-customer-facing-language)
10. [The pre-return audit](#10-the-pre-return-audit)

---

## 1. Why this exists

A CS artifact gets forwarded. The risk brief you write lands in a QBR deck; the ARR-at-risk
number lands in a board slide; the "champion has left" inference lands in an email to the
customer. Once a number leaves your hands it loses its caveats — so the caveats have to be
structural, attached to the number itself, not appended as a paragraph at the bottom.

Three failures cause almost all of the damage:

| Failure | What it looks like | Consequence |
| --- | --- | --- |
| **Fabrication** | Filling an unknown with a plausible industry number | A CSM quotes it to a customer and is corrected |
| **Silent omission** | Dropping a section because there was no data for it | The reader assumes it was checked and clear |
| **False precision** | "87% churn probability" from a rules-based score | The score gets treated as a measurement; when it misses, the whole model is discarded |

Everything below is a defence against one of those three.

---

## 2. Provenance tags

Every factual claim carries its source inline.

```
[<system> · <object/field/metric> · <as-of date or window>]
```

**Good**

```
Weekly active users fell 62% over six weeks, 41 → 16
  [Amplitude · unique_users_7d · 2026-07-13 → 2026-08-24]

Auto-renew was switched off on 2026-08-02
  [Salesforce · Contract.AutoRenew__c · changed 2026-08-02 by m.torres@acme.com]

Two P1 tickets breached SLA in July and remain open
  [Zendesk · tickets #48211, #48390 · priority=urgent, status=open · as-of 2026-08-26]
```

**Bad**

```
Usage is down significantly.                      ← no number, no source, no window
Their NPS is around 30.                           ← "around" is a fabrication tell
Engagement has dropped since Q1.                  ← which metric, which Q1, which source
The champion seems disengaged.                    ← inference presented as observation
```

**Rules**

- A date range beats a single date for anything measured over time.
- Name the *record* (ticket ID, opportunity ID, contact email) when there are few enough to name.
- If a number is computed from two sources, tag both and show the arithmetic.
- If a source's last sync is older than its expected latency, append the staleness:
  `[Salesforce · Opportunity.CloseDate · last sync 2026-08-11, 15d stale]`.

---

## 3. The three evidence tiers

Every statement in an artifact is exactly one of these. Blurring them is the most common
way a CS analysis becomes untrustworthy.

### Observed

Read directly from a source. State the value and the tag.

> Licence utilisation is 43% — 86 of 200 provisioned seats logged in during the last 30 days
> [Amplitude · distinct_users_30d · through 2026-08-24] [Salesforce · Asset.Quantity=200].

### Inferred

Derived, modelled, correlated, or reasoned. State the conclusion, the inputs, **and the
inference rule** — so a reader can disagree with the rule rather than the conclusion.

> **Champion departure (inferred).** Email to j.chen@acme.com hard-bounced on 2026-08-11
> [Gmail · delivery status], their Slack Connect account deactivated on 2026-08-12
> [Slack · member_left], and they were the sole named contact on 7 of the last 9 threads
> [Gmail · thread participants, 180d]. **Rule applied:** bounce + directory removal + sole
> primary contact ⇒ departure, not absence. **What would falsify this:** an out-of-office
> auto-reply, or a forwarding address in the bounce body.

Inference rules must be *stated*, not implied. "Usage is down so they're going to churn" is
not an inference, it is an assertion wearing a costume.

### Unknown

Not available. Write it as a first-class finding.

```
UNKNOWN — requires <specific source and field>
```

> Executive sponsor sentiment: **UNKNOWN — requires an NPS/CSAT source or call transcripts;
> no VoC system is connected.** This is one of the two families most likely to explain a
> false-green account.

**Never** replace an Unknown with:
- an industry benchmark ("typically around 105%")
- a hedged guess ("probably fine")
- silence (dropping the row)
- the previous period's value carried forward without saying so

---

## 4. Confidence levels and their entry criteria

Confidence is not a vibe. It has entry criteria, and the criteria are printed alongside it.

| Level | Entry criteria | What you may do with it |
| --- | --- | --- |
| **High** | ≥3 independent signal families agree · all contributing sources <7 days stale · ≥90 days of account history · coverage ≥80% | State the call directly. Recommend an irreversible action (exec escalation, forecast category change). |
| **Medium** | 2 families agree, or 3 agree with one source >30 days stale · coverage 60–80% | State the call with the caveat named. Recommend a reversible action (outreach, a check-in, an internal flag). |
| **Low** | 1 family only · <90 days history · coverage 40–60% | State it as a hypothesis with the test that would confirm it. Recommend investigation, not intervention. |
| **Insufficient** | Coverage <40% on the families that matter for this question | **Do not produce a score.** Name what is missing and what it would take to answer. |

"Independent" matters: login count and session count are the same family. Login decline plus
a support escalation plus auto-renew being switched off are three.

**The confidence cap rule.** Confidence can never exceed what the Coverage Ledger permits,
no matter how strong the available signals look. A 95%-confident read of 40% of the picture
is a 40% read.

---

## 5. The Coverage Ledger

The mechanism that turns "nothing was missed" from a claim into something a reader can check.

Every analytical artifact ends with it. Signal families are fixed per skill — you do not get
to choose which ones to print based on what data happened to exist.

```markdown
### Coverage Ledger
| Signal family | Source checked | Status | Notes |
|---|---|---|---|
| Product usage & adoption | Amplitude (through 2026-08-24) | ✅ Complete | 18 months history |
| Commercial & contract | Salesforce (through 2026-08-26) | ✅ Complete | — |
| Support & reliability | Zendesk (through 2026-08-26) | ✅ Complete | Jira not connected — no bug-load view |
| Relationship & engagement | Gmail, Calendly | ⚠️ Partial | Calendar for 1 of 3 account team members |
| Sentiment & VoC | — | ❌ Missing | No NPS/CSAT/survey source connected |
| Billing & payment | Stripe (through 2026-08-27) | ✅ Complete | — |
| Firmographic & external | — | ❌ Missing | No news/funding/headcount source |

**Coverage: 4.5 / 7 families (64%) → confidence capped at Medium.**
The missing families are sentiment and firmographic. Both are common causes of a
false-green read, so treat this assessment as a **floor** on risk, not a ceiling.
```

**Scoring convention:** `✅ Complete` = 1.0, `⚠️ Partial` = 0.5, `❌ Missing` = 0.
Coverage = sum ÷ number of families. Always print the fraction and the percentage.

**The blind-spot sentence is mandatory.** Naming which families are missing is not enough —
say what those specific gaps typically hide, so the reader knows which direction the error runs.

---

## 6. Stating probability without false precision

A rules-based score is not a calibrated probability, and presenting it as one is a
fabrication. Use bands, and say what the band means.

| Band | Say it as | Never say |
| --- | --- | --- |
| Very likely to renew | "Very likely to renew — no risk signals across 7 families" | "97% renewal probability" |
| Likely | "Likely to renew, with one watch item" | "84%" |
| Uncertain | "Genuinely uncertain — signals conflict (see §Contradictions)" | "50/50" |
| At risk | "At risk — 3 of 7 families negative, ARR $148k exposed" | "31% probability" |
| Very likely to churn | "Very likely to churn absent intervention" | "6%" |

If — and only if — the score has been **backtested against actual renewal outcomes**, you may
state a calibrated probability, and you must state the calibration alongside it:

> Renewal probability **0.34** (model v3, calibrated on 412 renewals FY25–FY26;
> Brier score 0.14; accounts scored in this band renewed 31% of the time).

Absent that backtest, bands only.

**The certainty ban.** Never claim 100% accuracy, never claim a prediction is guaranteed, and
never write "will churn". Write "very likely to churn absent intervention" and name the
intervention.

---

## 7. Recency, staleness and decay

| Source type | Expected latency | Treat as stale beyond |
| --- | --- | --- |
| Product usage / events | < 24 h | 3 days |
| Billing / payments | < 24 h | 7 days |
| Support tickets | < 1 h | 2 days |
| CRM fields | < 1 h | 7 days |
| Email / calendar | < 1 h | 3 days |
| Survey / NPS | event-driven | 90 days (a 6-month-old NPS is a historical fact, not a current signal) |
| Call transcripts | < 24 h | 45 days |
| Firmographic / news | weekly | 30 days |

Weight recent evidence more heavily and say that you are doing so. A support escalation from
last week and one from ten months ago are not the same signal; if your method treats them
the same, the method is wrong.

When a source is stale, the correct move is to **say so and cap confidence** — not to
extrapolate forward.

---

## 8. Contradiction handling

Real accounts produce conflicting signals constantly. Suppressing the conflict to give a
clean answer destroys the artifact's value. Surface it.

```markdown
### Contradictions
| Signal A | Signal B | Reading |
|---|---|---|
| Usage +34% QoQ [Amplitude · events_30d] | Auto-renew switched off 2026-08-02 [Salesforce] | Usage growth is concentrated in one team (14 of 19 active users are in Engineering, 0 in the Finance org that bought it). Product-level health masks buyer-level risk. Trust the commercial signal. |
| NPS 9 from the champion, 2026-05 | Champion departed 2026-08-11 (inferred) | The score belonged to a person, not the account. Discard it as a current signal. |
```

When signals conflict, the tiebreak order for **renewal risk** is:

1. **Commercial actions** (auto-renew off, notice served, procurement engaged, seat reduction) — these are decisions, not indicators.
2. **Economic-buyer relationship** (sponsor departed, sponsor disengaged, no multithreading).
3. **Usage by the buying team** — not aggregate usage.
4. Aggregate usage.
5. Sentiment scores.

State which rule you applied.

---

## 9. Internal vs customer-facing language

Every artifact declares which it is, at the top. The translation is not cosmetic.

| Internal | Customer-facing |
| --- | --- |
| "At risk — 62% likely to churn" | *Never appears in customer-facing material.* |
| "Champion has left; we are single-threaded" | "We'd like to make sure the right people on your side are looped in — could you point us to who's picking up Jamie's work?" |
| "Low adoption in Finance" | "Finance hasn't come onto the platform yet — worth a session to get them started?" |
| "ARR at risk: $148k" | *Never.* |
| "Save play activated" | *Never.* |

**Hard rule:** never emit a customer-facing draft in the same block as internal risk
language without an explicit `--- CUSTOMER-FACING BELOW THIS LINE ---` separator and a
restated warning. Leaked internal risk language has ended renewals.

---

## 10. The pre-return audit

Before returning any artifact, walk this. It takes thirty seconds and catches almost everything.

- [ ] Every number has a provenance tag with a date or window
- [ ] Every inference states its rule and what would falsify it
- [ ] Every gap says `UNKNOWN — requires X` — no benchmarks substituted, no rows dropped
- [ ] Confidence level stated, with the criteria that earned it
- [ ] Confidence does not exceed the Coverage Ledger cap
- [ ] Coverage Ledger present, all families printed including missing ones, blind-spot sentence written
- [ ] No probability stated to two significant figures without a backtest
- [ ] The words "100% accurate", "guaranteed", "will churn", "definitely" do not appear
- [ ] Contradictions surfaced rather than smoothed
- [ ] Customer-facing content separated and free of internal risk language
- [ ] Every recommendation has an owner, a date, and an expected effect
- [ ] Arithmetic shown for any derived figure
