# Save Play — <Account> · <Severity> · opened <date> · DRI <name>

**INTERNAL.** Contains risk, exposure and commercial language that must never reach the customer,
in any wording (`R18`). Do not forward. Do not screen-share.

<Defaults line, only when a Before-Starting question went unanswered: "Run on the recommended
defaults: nothing pre-approved commercially, VP CS available this week. Say the word and I will
re-run.">

## Bottom Line

<Three sentences: the cause, the one move that matters this week with its owner and date, and the
date by which this is decided either way.>

| | |
|---|---|
| ARR at stake · renewal · **opt-out deadline** | $<X> (<full loss / downsell of $Y>) · <date> · **<date>, <N> days of runway** |
| Primary cause · play · owner | <RCn — name> · locus <…> · origin <…> · **confidence <level>** · contributing <RCn> · <play> · <name> by <date> |
| Savability · exit criteria · stop-loss line | <band> `[P]`, a planning convention not a rate · <specific, observable, dated> · <the condition and its test date> |
| Exec engaged | <name, role, first action, date — or "not yet; requested by <date>"> |
| **Delivery of the bad news** (`C26`) | <what is being delivered> · <named caller> by phone <Mon–Wed date, HH:MM recipient-local> · written follow-up <within 2h / same day> · **Call placed: <date HH:MM · connected / voicemail+SMS / no answer / refused>** *or* **not yet — the written block is withheld** |
| **Register** (`C27`) | regulated / plain — regulated whenever severity is Critical, notice is served, an escalation is live, or the last inbound message is negative |
| Rules deviated from | <rule number · circumstance · what will be watched — or "none"> |

## 1. The diagnosis

**Cause: <RCn — name>.** <One paragraph: what happened, in what order, with dates.>

| Test applied | Evidence | Tier | Result |
|---|---|---|---|
| <identifying test for this cause> | <value + provenance tag> | Observed / Inferred | Positive |
| <differential test vs nearest neighbour> | <value + provenance tag> | Observed / Inferred | Negative |

**Ruled out**

| Cause | Rejected because |
|---|---|
| <RCn> | <the specific evidence that rejected it> |

**What would change the diagnosis:** <2–3 observable events.>

## 2. Timeline and commitment debt

| Date | Event | Source | Who knew | What we did / still owe | Status |
|---|---|---|---|---|---|

<Earliest detectable signal → today, including our own misses. Anything we promised and have not
delivered goes at the top: an unmet commitment of ours is the likeliest reason a save call fails.>

## 3. The play

**Objective:** <named person> will have <specific observable commitment> by <date>.

| # | Action | Owner | By | Expected effect | Success measure |
|---|---|---|---|---|---|

| | |
|---|---|
| **Can commit** | <dated, owned, internally agreed> |
| **Cannot commit** | <said plainly, with the nearest alternative> (`R19`) |
| **Customer must do** | <named person> — <action> — <date> |

| Working signals (≤14 days) | Failing signals (≤14 days) |
|---|---|

## 4. Exec engagement

| Which exec and why | The one ask | Decision needed by | What the call must achieve |
|---|---|---|---|

## 5. Delivering it (`C26`, `C27`)

| Block | Class | Register | Caller | Slot (recipient-local) | Call placed · outcome | Written follow-up |
|---|---|---|---|---|---|---|
| <e.g. the decline> | bad | regulated | <name, role> | <Mon–Wed, 08:00–11:30> | <date HH:MM · outcome> | <within 2h / same day> |

<A row per customer-facing block this play emits. A `bad` row with an empty **Call placed** cell is
an invalid plan: the written block is withheld, the voicemail line and scheduling note in
`../references/difficult-register.md` go out instead, and the withholding is stated here. Friday,
any slot after 15:00 local, and the day before a customer holiday are refused — a deviation is
recorded in **Rules deviated from** with its compensating control.>

## 6. Commercial position

| Tier available | The give | The required get | Approver | Used? |
|---|---|---|---|---|

**Floor:** <the structure below which we do not go, and why.>
**Not tradeable without VP approval:** notice window · auto-renew clause · uplift clause · audit
and true-up rights.

## 7. Checkpoints and stop-loss

| Checkpoint | Date | Test | Go | No-go |
|---|---|---|---|---|
| CP1 — is the play landing? | <open + 14d> | <working signals> | | |
| CP2 — go/no-go | <opt-out − 21d> | <criteria reachable in the time left?> | | |

**Economics** — from `../scripts/save_economics.py`, arithmetic shown:

| | |
|---|---|
| Retained gross profit if saved · play + concession cost | $<X> over <horizon> · $<X> (<hours by role>) + $<X> |
| **Break-even save probability `P*`** | **<X>%** — <above/below> the savability band · ceiling <X>% discount |
| **Call** | **Continue / Restructure / Exit** — <the reason in one line> |

## 8. Exit plan

<Required whenever a stop-loss trigger is live or notice has been served. See
`../references/graceful-exit.md`.>

| # | Step | Owner | By | Done |
|---|---|---|---|---|

**Win-back triggers:** <observable events, each with an owner and the date it is next checked.>

### Assumptions

| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | | | |

<One row per assumption, each with a concrete consequence. "May affect the plan" is not a
consequence — if you cannot name what would change, you did not need the assumption.>

### Coverage Ledger — the evidence base for the diagnosis

| Signal family | Source checked | Status | Notes |
|---|---|---|---|
| Product usage & adoption | | ✅/⚠️/❌ | |
| Commercial & contract | | | |
| Relationship & engagement | | | |
| Support & reliability | | | |
| Sentiment & VoC | | | |
| Billing & payment | | | |
| Firmographic & external | | | |

**Coverage: <X> / 7 (<Y>%) → diagnosis confidence capped at <level>** (`R23`).
Blind spots: <which families are missing and which causes they would most likely have revealed — a
missing sentiment family hides RC1 and RC11; a missing firmographic family hides RC9 and RC7.>
Under 40% coverage no cause is named and the play is the diagnostic conversation.
