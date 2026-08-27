# Cadence Design

> How many touches, how far apart, on which channels, who signs them, and — the part everyone
> skips — when to stop. Plus the honest way to measure whether any of it works.

**Contents**
1. [What a cadence is for](#1-what-a-cadence-is-for)
2. [The default trigger cadence](#2-the-default-trigger-cadence)
3. [The permission close](#3-the-permission-close)
4. [Suppression: caps, cooldowns and blackouts](#4-suppression-caps-cooldowns-and-blackouts)
5. [The escalation ladder](#5-the-escalation-ladder)
6. [Cadence patterns by trigger family](#6-cadence-patterns-by-trigger-family)
7. [Measuring outreach honestly](#7-measuring-outreach-honestly)
8. [Capacity: what a CSM can actually run](#8-capacity-what-a-csm-can-actually-run)
9. [Stopping permanently](#9-stopping-permanently)

Evidence tags: `[M]` measured · `[V]` vendor-reported · `[P]` practitioner rule · `[D]` derived
here from stated assumptions.

---

## 1. What a cadence is for

A cadence exists to survive the fact that a good message arrives on a bad day. The champion is in
a board prep, the admin is on leave, the CFO is closing the quarter. One touch tests your message
against one moment. Three touches test it against three.

What a cadence is **not** for: manufacturing urgency, wearing someone down, or covering for a
message that had nothing to say. If touch 1 had no reason to exist, touch 3 does not either — it
just costs more.

**The design constraint is the customer's attention budget, not your time.** For a high-touch CSM
carrying 15 accounts, capacity allows roughly 1.7 personalised touches per account per week (§8) —
far more than any account should receive. The binding constraint is the fatigue cap, not the
calendar.

Three properties make a cadence legitimate:

| Property | Test |
| --- | --- |
| **Each touch carries new information** | Could touch 2 have been sent before touch 1? If yes, it is a reminder, not a touch |
| **Channels vary** | Three emails is one channel tested three times, not three attempts |
| **There is a stated end** | If you cannot name the condition under which you stop, you have designed a subscription, not a play |

---

## 2. The default trigger cadence

**Three touches over 12 days, channels mixed, then stop.** `[P]` — a library convention; no
published dataset exists for optimal spacing of CS touches to existing customers, so treat these
day counts as a starting configuration and replace them with your own reply-timing distribution
once you have ≥30 sends per trigger.

| Touch | Day | Channel | Content | Length |
| --- | --- | --- | --- | --- |
| **1** | 0 | Email — or Slack if the ask is operational and a shared channel exists | The trigger, one data point, one ask, one exit | 50–100 words |
| **2** | +4 | **A different channel from touch 1** | New information: a second data point, an artifact, or a named person's answer. Never a reminder | 80–140 words |
| **3** | +12 | Email, in the original thread | The permission close (§3) | 40–60 words |

**Why +4 and +12 rather than +3 and +7.** A 4-day gap clears a normal week's inbox cycle without
landing in the same working day twice; a 12-day gap puts the close in a different week and a
different mental context from touch 2. Tighter spacing on a customer you already have reads as a
prospecting sequence — which is exactly what it will be pattern-matched to.

**Variations**

| Situation | Cadence |
| --- | --- |
| **Urgent operational** (U9 integration break, S2 SLA breach, B1 payment failure) | Phone or Slack immediately, email same day confirming, then follow the incident, not a cadence |
| **T1 declared intent** (S3 higher-tier request, upgrade-page visit) | Touch 1 within 24h, touch 2 at +2 days. Two touches only — if someone asked and you needed three attempts, the routing is broken |
| **Executive** (X4 leadership change, R2 sponsor change) | 2 touches, +7 days apart, both exec-signed. Executives do not respond to frequency |
| **Lifecycle / calendar** (C1 opt-out checkpoints) | One touch per checkpoint (T−120, T−90, T−60, T−30). Each is a separate trigger, not a cadence |
| **Tech-touch segment** | Automated: email → in-app → email, exit on the condition clearing. A four-touch variant (email → in-app → phone → follow-up email) run weekly is a common configuration `[P]`. The human cost sits in the build, not the send — budget it as a one-off, then measure the marginal cost per account |

**Stop conditions — any one ends the cadence immediately.** Print these in the artifact:

- Any reply, of any kind, including "not now"
- The trigger condition clears (utilisation drops, integration reconnects, invoice pays)
- A fatigue cap is hit (§4)
- A Sev-1 or escalation opens on the account
- The account enters the renewal endgame under a different owner
- The customer asks for less contact — permanently, and recorded on the `contact` record

---

## 3. The permission close

Touch 3 is not a follow-up. It is an offer to stop, and it works because it makes "no" cheap.

**Its four jobs, in order:**

1. Name the silence without accusation — silence is information, not rudeness
2. State what you will stop doing, specifically
3. Leave one path back that costs a single word
4. Keep the door open without a date

**Worked version — after two unanswered touches on a usage-drop trigger:**

> Subject: `the export job`
>
> Three weeks of no reply usually means this isn't near the top of the list — which is a completely
> fine answer, and more useful to me than a maybe.
>
> The export volume is still at about a fifth of where it was in July, so it's on my list either
> way. Reply "later" and I'll stop bringing it up until something changes on your side. Reply
> "wrong person" and I'll find the right one.
>
> Nothing needed otherwise.

**What makes it work**

| Element | In the example |
| --- | --- |
| Names the silence, no guilt | "usually means this isn't near the top of the list — which is a completely fine answer" |
| Says what stops | "I'll stop bringing it up until something changes" |
| One-word reply path | "later" / "wrong person" |
| Keeps the fact alive | "still at about a fifth of where it was in July" |
| No new ask | The last line removes the obligation entirely |

**Never**: "circling back", "bumping this", "in case this got buried", "third attempt", or a
guilt-shaped question ("did I do something wrong?"). And never send a permission close on an
account where **we** owe **them** something — there, the outstanding commitment is the message.

---

## 4. Suppression: caps, cooldowns and blackouts

The suppression layer is what separates a trigger programme from a spam programme. Every value
below is `[P]` — an operating convention drawn from published expansion-timing guidance and CS
platform practice, not a measured optimum. Tune them; do not remove them.

### 4.1 Fatigue caps

| Cap | Value | Counts what |
| --- | --- | --- |
| Account cap | ≤4 proactive outbound touches / rolling 30 days | Every `interaction` with `direction='outbound'` and a trigger ID, across all senders |
| Person cap | ≤2 proactive touches / rolling 14 days | Per `contact_id`, not per account |
| Distinct-cadence cap | ≤2 cadences running concurrently on one account | Two open loops is the most a champion can track |
| Sender cap | ≤1 exec-signed message / 60 days | Exec air cover devalues with use |

Caps count only **proactive** outbound. Replies, incident communications, contractual notices, and
anything the customer initiated are exempt and are not counted.

### 4.2 Cooldowns and blackouts

| Rule | Window | Blocks |
| --- | --- | --- |
| Post-Sev-1 cooldown | 14 days from resolution | Any commercial ask |
| Post-escalation cooldown | 30 days from escalation closure | Any commercial ask |
| Post-advocacy separation | 14 days | A second ask of any kind to the same person |
| Ask spacing | 90 days minimum between two distinct commercial asks to the same buyer | Commercial asks |
| Annual ask ceiling | ≤2 expansion asks per account per year, excluding customer-initiated | Commercial asks |
| Onboarding blackout | Contract start → verified time-to-first-value | Expansion and advocacy asks |
| Post-uplift blackout | 90 days after a price increase takes effect | Expansion asks |
| Renewal endgame | `opt_out_deadline − 30 days` → renewal date | **New** expansion asks. A new ask here turns the renewal into a bargaining chip |
| Post-renewal window | T+0 to T+60 after signature | Nothing — this is a legitimate expansion window, and the relationship reset removes the "you're only asking because of the renewal" objection |

### 4.3 The gates that override everything

| Gate | Rule |
| --- | --- |
| **Open-loop gate** | If we owe them an overdue commitment, that commitment is the only outreach that sends. Writing about anything else while a promise is outstanding is the fastest way to lose a champion |
| **Health gate** | No expansion or advocacy ask on an account at `churn-risk` band At Risk or worse. State the gate in the artifact and name what would lift it |
| **Escalation override** | C5 (auto-renew off) and R1 (champion departure) are never suppressed. They route to `save-play`, not to this queue |
| **C4 · acknowledgement source** | A customer-voiced Regulated trigger — detractor free-text, an escalation, a complaint, a promise of ours they chased — with no verbatim sentence of theirs on record is **held**, not written. Print `UNKNOWN — requires <ticket · survey verbatim · transcript>` and either retrieve the quote or phone them. Our paraphrase of their complaint, returned to them, is what turns an escalation into a churn (`email-craft.md` §11.1) |

### 4.4 Alert hygiene

An outreach queue is only as good as the alert set that feeds it. The test to apply to every rule
in whichever platform holds your alerts `[P]`: it must be **actionable**, **owned by a named
person**, and carry **meaningful business risk if ignored**. An alert set that fails any of the
three trains the CSM to dismiss on reflex, and the dismissal habit generalises to the alerts that
mattered.

Four hygiene rules that follow from it:

| Rule | Effect |
| --- | --- |
| Tier alerts into *act today* / *watch this week* / *information only* | Urgency stops being uniform, so it starts meaning something |
| Collapse per-user alerts into one account-level alert | Ten blocked-invite events are one trigger, not ten |
| Fire once, on the first time the condition is met | Otherwise the same trigger re-fires daily and trains dismissal |
| Retune quarterly and retire dead rules | Measure **action rate** (outreach sent ÷ triggers fired) per trigger ID; a rule whose action rate sits well below your book median is noise. Set the floor from your own measured baseline |

---

## 5. The escalation ladder

Move one rung at a time. Each rung is gated on the prior rung completing its full cadence, because
skipping rungs tells the customer that the person you skipped had no authority — which is a claim
about your own company you probably do not want to make.

| Rung | Sender | Recipient | Gate to earn this rung | Typical use |
| --- | --- | --- | --- | --- |
| **1** | CSM | Champion / admin | Default | Everything starts here |
| **2** | CSM, manager cc'd | Champion + their manager | Rung 1's full cadence completed with no reply, and the trigger is still true | Silence on a material trigger |
| **3** | VP CS signs | Exec sponsor | Rung 2 complete, and either ARR ≥ segment threshold or a decision-level trigger fired | R2 sponsor change, C5 auto-renew off, S2 repeat SLA breach |
| **4** | CCO / CEO signs | Their C-level | Rung 3 complete and the renewal or the relationship is materially at stake | Reserved. Once a year per account, at most |

**Rules**

- The recipient at each rung must be an **altitude match** for the sender. A CSM writing to a CFO
  skips two rungs in one move and is usually forwarded back down to the person they skipped.
- **A parallel exec-to-exec touch is not an escalation** — on R1 (champion departure) and R2
  (sponsor change), rung 1 and rung 3 fire simultaneously by design, because the account has lost
  its only path and the exec message is the replacement path, not the pressure.
- Never escalate on silence alone when the trigger has decayed. Escalate on the *fact*, and the
  fact must still be true.
- Say what you are doing internally: "escalating to rung 3 because the T−60 checkpoint passed with
  no renewal conversation held" is an auditable decision. "Looping in leadership" is not.

The sponsor-change play — two sequenced emails, VP of Customer Success first, then the assigned
CSM, both drafted for human review before sending — is a rung 3 + rung 1 pair, not an escalation
over time `[P]`. Rung 3 goes first here because the new sponsor has no relationship to spend and
the VP's title is the only thing carrying the introduction.

---

## 6. Cadence patterns by trigger family

| Family | Default touches | Spacing | Channel mix | End condition |
| --- | --- | --- | --- | --- |
| **Product usage & adoption** | 3 | 0 / +4 / +12 | Email → Slack or in-app → email | Trigger clears, or reply |
| **Commercial & contract** | 1 per checkpoint | T−120 / T−90 / T−60 / T−30 | Email, always in writing | Written confirmation of intent, or notice received |
| **Relationship & engagement** | 2–3 | 0 / +7 / +14 | Email → champion relay or phone → email | Any reply, or a new contact identified |
| **Support & reliability** | Incident-shaped, not cadence-shaped | Immediate, then per the incident | Phone or Slack → email confirming | Resolution acknowledged by them |
| **Sentiment & VoC** | 1–2 | 0 / +5 | Phone or email → email | Reply, or the loop is closed in writing |
| **Billing & payment** | Automated dunning, then 1 human touch | System schedule, human at failure 2 | Automated email → CSM email or phone | Payment clears |
| **Firmographic & external** | 1–2 | 0 / +7 | Email → exec email if warranted | Any reply. These do not justify a third touch |

### 6.1 Channel selection

Channel is a decision about latency and permission, not preference. `trigger-catalog.md` carries
the per-trigger default; override it with this table when the situation differs.

| Channel | Use when | Do not use when | Latency |
| --- | --- | --- | --- |
| **Email** | The message needs a record, a number, or a forwardable artifact | It is time-critical inside 4 hours | Hours–days |
| **Slack Connect** | A shared channel exists and the ask is small and operational | The message contains commercial terms, or the recipient is an exec | Minutes–hours |
| **In-app** | The recipient is mid-task and the ask is a product action | The ask needs a decision or a budget | Seconds |
| **Phone / video** | Something broke, someone left, or a number is about to change | Nothing has changed | Immediate |
| **Champion relay** | The right recipient will not take a cold approach from us | The champion is the problem | Days |
| **Exec-to-exec** | A decision-level event, and we are single-threaded | It is the first attempt on any channel | Days |

**Channel mixing rules**

- Never send touches 1 and 2 on the same channel. If the first channel was wrong, repeating it
  tests nothing.
- Slack Connect is for operational asks only. Commercial terms, notice dates and anything a
  procurement team may later read go in email, where there is a record.
- In-app is for asks that are product actions. It cannot carry a decision or a budget question.
- Phone is the right first channel for exactly four situations: something broke, someone left, a
  number is about to change, or a detractor responded.

---

## 7. Measuring outreach honestly

### 7.1 The metric set

| Metric | Formula | Segment by | What it tells you |
| --- | --- | --- | --- |
| **Reply rate** | replies ÷ sends | Trigger ID, altitude, segment | A trigger below the book median is a badly specified trigger, not a badly written email |
| **Meeting-booked rate** | meetings scheduled ÷ sends | Trigger ID | The only outreach metric that survives contact with a forecast |
| **Action rate** | outreach sent ÷ triggers fired | Trigger ID | A low action rate means the trigger set is producing noise. There is no published floor worth quoting — set yours from your own first quarter of data |
| **Trigger precision** | triggers the customer confirmed ÷ triggers fired | Trigger ID | The false-positive rate you are spending credibility on |
| **Time-to-first-touch** | first send − trigger fired | Trigger ID | A trigger's entire value is lead time. A 9-day median destroys a 14-day window |
| **Cadence completion** | cadences that reached their stop condition ÷ cadences started | CSM | Abandoned cadences are worse than none — you taught them to ignore you and then confirmed it |
| **Suppression rate** | suppressed ÷ triggers fired | Gate | A 0% suppression rate means the gates are not running |

Set your own baselines. Published reply-rate benchmarks are for **cold outbound to prospects**
(Lavender's February 2026 report: 231,818 emails from ~50k inboxes, technical buyers 5.2%, ops
leaders 5.4% on A-grade emails) `[V]`. Customer outreach is a different population and no
equivalent public dataset was found. Measure 4–8 weeks by trigger ID and use that.

### 7.2 The attribution problem, stated plainly

**You cannot attribute retention to outreach from observational data.** Accounts that receive
outreach are selected precisely because something was happening — and that same something predicts
the outcome. Comparing "accounts we contacted" to "accounts we didn't" measures the selection, not
the play. Every version of the claim "our outreach programme saved $2M of ARR" that is built this
way is wrong in a direction you cannot bound.

### 7.3 The holdout, which is the only honest answer

| Step | Design |
| --- | --- |
| **1. Pick one trigger** | Test a single trigger ID at a time. Testing "the programme" tests nothing |
| **2. Randomise at the account level** | Every account that fires the trigger is randomly assigned: 80–90% treatment, 10–20% holdout. Randomise on a stable hash of `account_id`, so an account cannot drift between arms |
| **3. Hold the arms for a full renewal cycle** | Reply rate reads in days; retention reads in quarters. A 30-day holdout answers a 30-day question |
| **4. Pre-register the outcome** | Name the metric — gross renewal rate, expansion ARR, or ticket volume — before you look. Post-hoc metric selection is how a null result becomes a win |
| **5. Report the arm sizes and the difference** | With n per arm. A 4-point difference on 22 accounts is noise |
| **6. Carve out the harmful cases** | Never hold out an operational trigger. Nobody's integration stays broken for a study. Holdouts apply to *discretionary* outreach only — U1, U2, U3, U6, U10, U11, X1, X5, X7, X8 |

**Until the holdout has run, report reply rate and meeting-booked rate as activity metrics, and
state in the same sentence that the retention link is untested.** That sentence costs you nothing
with a Chief Customer Officer and costs you everything when it is discovered missing.

---

## 8. Capacity: what a CSM can actually run

The arithmetic below is `[D]` — derived from stated assumptions, not measured. Replace the
assumptions with your team's own time study; the structure of the calculation is the point.

**Assumption:** 25% of a 40-hour week is available for proactive outreach = **600 minutes**. This
is a library default, not a benchmark. Confirm it before sizing any queue.

| Touch type | Minutes (research + write + log) |
| --- | --- |
| Trigger-sourced 1:1 email, personalised from data | 20 |
| Slack Connect message | 6 |
| Champion relay (asking for one introduction) | 12 |
| Phone attempt including voicemail and note | 15 |
| Exec-to-exec email drafted for a VP or CCO to send | 30 |
| In-app message, marginal cost once the campaign is built | 0.5 |
| One-to-many campaign build (one-time) | 180 |

**Weekly capacity at 600 minutes:** 30 personalised emails, or a realistic mix of **~26 touches**
(12 emails + 6 exec emails + 8 calls = 240 + 180 + 120 = 540 minutes, leaving 60 for logging).

Divide that capacity by the book size recorded in `cs-context` §3 to get what a single account can
actually receive. The account counts below are a **worked example, not a published benchmark** —
substitute your own, and the arithmetic carries `[D]`:

| Coverage model | Accounts (example) | Touches / account / week `[D]` | What this forces |
| --- | --- | --- | --- |
| High touch | 15 | ~1.7 | Capacity is not the constraint — the fatigue caps are. Spend the surplus on depth, not frequency |
| Mid touch | 45 | ~0.6 | Roughly one personalised touch per account per fortnight. Rank hard; T4–T6 triggers rarely earn a human |
| Low touch | 120 | ~0.2 | Only T1 and T2 triggers get a person. Everything else must be a campaign or it does not happen |
| Tech touch | 500 | ~0.05 | Human time is reserved for escalation triggers only. The trigger catalog must run as automation end-to-end |

**Sizing the trigger volume against it.** Do not guess the fire rate — measure it:

```
Weekly trigger volume = (triggers fired per account per month × accounts) ÷ 4.33
Coverage gap          = weekly trigger volume − weekly touch capacity
```

Worked example `[D]`: a mid-touch CSM with 45 accounts observing 1.8 triggers per account per
month → `(1.8 × 45) ÷ 4.33 = 18.7` triggers per week against ~26 touches of capacity. That book is
runnable. The same CSM at 120 accounts → 49.9 triggers per week against 26 touches: **half the
triggers will never be worked**, and the only honest responses are to raise the strength threshold,
route T3–T6 to campaigns, or change the coverage model. Pretending otherwise produces a queue that
silently drops the bottom half at random rather than by rank.

`../scripts/outreach_queue.py` computes both the ranked queue and this capacity fit deterministically.

---

## 9. Stopping permanently

Some accounts should be removed from proactive outreach entirely. Record the reason on the
`contact` or `account` record so the next CSM does not rediscover it the hard way.

| Condition | Action |
| --- | --- |
| The customer asked for less contact | Honour it exactly as stated, record the date, and route future triggers through the channel they named |
| Three consecutive cadences completed with zero replies from anyone at the account | Stop discretionary outreach. Switch to contractual and operational messages only, and escalate the multithreading problem to `stakeholder-map` |
| The account is in an active `save-play` | This skill's queue defers entirely — one owner, one plan, one voice |
| Notice has been served | Outreach becomes a wind-down and win-back conversation, owned elsewhere |
| The only known contact has left and no replacement is identified | The trigger is R1 and the play is exec-to-exec, not a cadence |

**Recording a stop is a finding, not an admission.** An account with three failed cadences and no
reply from any contact is telling you something more important than any usage metric: there is
nobody left who is willing to talk to you. That belongs in the risk assessment, not in next
Monday's queue.
