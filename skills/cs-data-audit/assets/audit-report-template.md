# CS Data Audit — report template

> Emitted by `cs-data-audit`. Copy this file whole and populate it. Populate every table or write
> `UNKNOWN — requires <source>` in it; **never delete a row** — a silently omitted domain is
> indistinguishable from an untested one.
>
> **Internal document.** It carries system access detail, per-account ARR variance and disclosed
> gaps. It is never forwarded to a customer, in whole or in part (`R18`).

---

# CS Data Audit — <Company> · <date> · scope: <decision set>
**Internal.** Contains system access detail and disclosed gaps. Not shareable with a customer.
*Run on defaults: <the ones taken, or "none — all four questions answered">. Data as of <date>.*

## Bottom Line
<3 sentences: overall grade, the decision currently being made wrong and its dollar value,
the single fix to fund first.>

| | |
|---|---|
| Overall data grade | X/100 — <Reliable / Usable with caveats / Directional only / Not usable> |
| ARR governed by degraded decisions | $X across N accounts |
| Families reliable / partial / missing | a / b / c of 7 |
| Max confidence any downstream skill may claim | High / Medium / Low / Insufficient |
| Predictive work possible today? | Yes / No — <the blocking condition> |
| Fund first | <gap> · <effort days> · <owner> · unlocks <what> |
| Audit confidence | <level> — <access method and what could not be tested> |

**What would change the grade:** <the single measurement that would move it, and who can run it.>

## 1. Decision Set Under Audit
| # | Decision | Cadence | Owner | ARR governed | Fields consumed | Currently reliable? |
|---|---|---|---|---|---|---|
## 2. Source Inventory
| # | System | Signal family | Connected | Access | Account key | Latency claimed | Staleness observed | History | % of ARR covered | Owner | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
<every family from cs-context §9, including absent ones>
## 3. Field Completeness, Validity & Freshness
| Entity.field | Dimension | Test applied | Pass criteria | Result | Value | ARR affected | Damage if wrong |
|---|---|---|---|---|---|---|---|

**Null-vs-zero test:** <dates on which all accounts wrote exact zeros, if any>
## 4. Identity Resolution
| Measure | Value | Pass criteria | Result |
|---|---|---|---|
| User join rate | | ≥90% | |
| Volume join rate | | ≥90% | |
| ARR join rate | | ≥90% | |
| Duplicate accounts (top ARR decile) | | 0 | |
| Internal/test exclusion rule documented | | Yes | |
### Breakage catalogue
| # | Case | Detected | Accounts | ARR affected | Error direction | Metric distorted | Measured damage | Fix | Effort (days) |
|---|---|---|---|---|---|---|---|---|---|
<all 7 cases, including those measured at zero>
## 5. Event Taxonomy
| Check | Value | Pass criteria | Result | Consequence if failed |
|---|---|---|---|---|
<all 10 checks>
**Core action:** <named event, or `UNKNOWN — requires product/CS agreement`> ·
**Fleet-vs-account decay test:** <result>
## 6. Churn Labels
| # | Check | Value | Pass criteria | Result | What its failure blocks |
|---|---|---|---|---|---|
<all 10 checks>

### Label sufficiency for modelling
| Ambition | Minimum required | You have | Verdict |
|---|---|---|---|
## 7. Contract Data — document test
| Field | Sampled (n) | Matches paper | Accuracy | 95% CI | Median days since last edit | Owner | Result |
|---|---|---|---|---|---|---|---|

**Opt-out deadline computability:** <N accounts / $X ARR with no computable `renewal_date − notice_period_days`> — these cannot enter Commit.

## 8. Metric Integrity
| Metric | Reported | Reproduced from raw | Variance | Tolerance | Result | Definition documented | Version |
|---|---|---|---|---|---|---|---|
### System disagreement (accounts varying >5%)
| Account | CRM ARR | Billing ARR | Warehouse ARR | CS platform ARR | Max variance | Ruled source of truth |
|---|---|---|---|---|---|---|
## 9. Coverage Scoring
| Signal family | Presence /20 | Acct coverage /20 | Completeness /20 | Freshness /20 | Fidelity /20 | Score /100 | Ledger status |
|---|---|---|---|---|---|---|---|
| Product usage & adoption | | | | | | | |
| Commercial & contract | | | | | | | |
| Relationship & engagement | | | | | | | |
| Support & reliability | | | | | | | |
| Sentiment & VoC | | | | | | | |
| Billing & payment | | | | | | | |
| Firmographic & external | | | | | | | |
### Downstream confidence caps
| Skill | Families required | Weakest family score | Max confidence | Blocked? | Unblocked by |
|---|---|---|---|---|---|
## 10. Remediation Plan
| Rank | Gap | Decisions degraded | B ($ARR) | D | U | C | E (days) | Priority | Action | Owner | Start | Done by | Expected effect | Success measure |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
### Sequence
| Wave | Weeks | Items | Gate to advance |
|---|---|---|---|
### Quick wins — start this month
| Fix | Effort | Owner | Unlocks |
|---|---|---|---|
### Deliberately not doing yet
| Fix | Cost | Why not yet | Revisit when |
|---|---|---|---|
## 11. Funding Case — for the CFO
| Tier | Cost (days / $) | What it buys | ARR it de-risks | What stays broken |
|---|---|---|---|---|
### For the CTO / Head of Data
| Item | Eng days | One-off or ongoing | Blocks what | Not eng work |
|---|---|---|---|---|

### Ingest Report — when any file was supplied
| File | Rows | Header row found at | Columns mapped ≥0.80 | Mappings confirmed below 0.80 | Join rate to accounts | As-of date |
|---|---|---|---|---|---|---|

Any mapping still unconfirmed below 0.80 is listed here and the fields it feeds are scored
`UNKNOWN`, not estimated.

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | <e.g. audited the eight default decisions> | <question unanswered / field absent> | <the specific figure, rank or verdict that changes> |

One row per assumption, each with a concrete consequence. "May affect results" is not a
consequence — if you cannot name what would change, you did not need the assumption.

### Coverage Ledger
| Signal family | Source checked | Status | Notes |
|---|---|---|---|
<all 7 families, always>

**Coverage: X / 7 families (Y%) → downstream confidence capped at <level>.**
Blind spots: <which families are weakest and what that specifically hides.>

### What this audit could not check
| Item | Why | What it would take |
|---|---|---|
