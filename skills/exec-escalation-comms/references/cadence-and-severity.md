# Cadence and Severity — the clock, the notice period, the send date

> Read this **when setting severity, choosing an update cadence, or picking the date a planned
> change is announced.** Severity decides how fast the first note goes and how often the next one
> follows; the notice table decides whether an announcement is legitimate or a change the
> customer had no way to decline. Both are arithmetic, and `../scripts/update_clock.py` does the
> arithmetic — this file is what the numbers mean and where they came from.
>
> Evidence labels: `[M]` measured · `[V]` vendor · `[P]` practitioner · `[A]` academic ·
> `[L]` legal or regulatory primary text.

**Contents** — [1. Severity](#1-severity-from-their-ability-to-work) ·
[2. The clock](#2-the-clock) · [3. Who sends, and who signs](#3-who-sends-and-who-signs) ·
[4. Notice periods for planned changes](#4-notice-periods-for-planned-changes) ·
[5. Timing — day, hour, blackout](#5-timing--day-hour-blackout) ·
[6. What the business model changes](#6-what-the-business-model-changes) ·
[7. Many accounts, one change](#7-many-accounts-one-change) ·
[8. Running the clock](#8-running-the-clock)

---

## 1. Severity, from their ability to work

**Severity comes from the customer's ability to work.** Never from our engineering effort, never
from how embarrassing it is, and never from how loudly they are complaining — a quiet account
with a stopped workflow is S1 and a furious account with a cosmetic bug is not.

| Sev | The customer's position | Typical shape |
| --- | --- | --- |
| **S1** | A core workflow is unavailable with **no workaround**, data is exposed or lost, or **their own customers** are affected | Nightly batch fails three runs running; checkout down; PII exposed; their SLA to their client breached |
| **S2** | A core workflow is degraded, or a workaround exists that **costs them hours** | Reports run but take 40 minutes; a manual re-key restores the data; one region affected |
| **S3** | A non-core function is affected and the workaround is **cheap** | An export format broken with a supported alternative; an admin screen unavailable |
| **S4** | **Nothing is broken.** Something is changing that will cost them | Price rise, EOL, tier change, coverage change, a CSM handover |

### The reclassification triggers

Severity is re-evaluated on every update, and it moves **up** on any of these without discussion:

| Trigger | New floor | Why |
| --- | --- | --- |
| Their customers or end users are affected | **S1** | Their reputational exposure is now larger than their operational one |
| A regulator, auditor or external reporting deadline sits downstream | **S1** | The firmographic-and-external family, and the one most often skipped in the Step 1 sweep |
| **This is a repeat** of a failure they have already been told was fixed | **+1 level** | A repeat changes the note more than the failure does — the subject is now our credibility |
| Personal data may have been exposed | **S1**, and legal and security own the wording | `[L, Regulation (EU) 2016/679, Arts. 33–34]` — 72-hour supervisory-authority clock, phased reporting allowed |
| A named executive on their side has been drawn in | **+1 level** | Not because they matter more, but because the audience for every subsequent note has changed |
| The workaround stops working, or nobody has verified it works | **+1 level** | An unverified workaround is not a workaround |

Severity moves **down** only after resolution, and the downgrade is stated in the note. Silently
downgrading is how a cadence gets dropped without anyone deciding to drop it.

### What severity is not

| Not a severity input | Why |
| --- | --- |
| ARR, tier, logo value | It changes who *sends* (§3) and the sequencing (§7). It never changes how fast the truth travels |
| Our internal priority label | `P1` is our queue. The customer's workflow is the subject |
| How angry the contact is | Anger is a relationship signal, not an impact measurement. Regulate down (`C27`) and set severity from the workflow |
| Whether we have a fix | A cause-unknown S1 is still an S1, and it is the note most often skipped |

---

## 2. The clock

| Sev | First note within | Update floor | Stops when |
| --- | --- | --- | --- |
| **S1** | **60 min** of confirmed customer impact | **Hourly** | Resolved, then closure within 1 business day |
| **S2** | **4 business hours** | **Twice daily** | Resolved, then closure within 1 business day |
| **S3** | **Same business day** | **Daily** | Resolved, then closure in the next scheduled contact |
| **S4** | Per the notice table (§4) | As stated in the first note | The effective date passes |

These are **floors, not ceilings.** Sending more often is always allowed; sending less often
breaks the commitment made in the first note, which is a second failure with your signature on
it.

**Where the S1 floor comes from.** Public status-page practice converges on a 30-minute baseline
for a live, customer-impacting incident, with an explicit instruction never to go silent:
Atlassian's guidance is to update "every 30 minutes (or whatever cadence is appropriate)" and to
communicate early and often `[P, Atlassian Statuspage incident-communication guidance, accessed
2026-08]`; incident.io specifies every 30 minutes for a SEV1 and 20–30 minutes in the early
stages, with "we're still investigating, no new information, next update in 30 minutes" as a
legitimate update `[P, incident.io incident-communication best practices, accessed 2026-08]`.
**This skill sets the named-account floor at 60 minutes rather than 30**, deliberately: a
personally-written note to a named executive at 30-minute intervals degrades into a status-page
paste, and the status page is already doing that job. Where the account is under 30-minute
contractual reporting, follow the contract.

### The no-news update is the whole discipline

**Send the update even when there is nothing new.** Silence for two cadence cycles reads as loss
of control, and the customer fills the gap by escalating to someone who knows less than you do.
The pre-written column in the cadence plan is what makes this happen:

| Update # | Due (their tz) | Sender | What it says if nothing has changed |
| --- | --- | --- | --- |
| 3 | 14:00 BST | Jo Whitfield | "No change since 13:00. Still on the migration path; replica lag ruled out. Nothing needed from you. Next update 15:00." |
| 4 | 15:00 BST | Jo Whitfield | "No change since 14:00. Sam's team is testing the rollback in staging. Next update 16:00." |

Fill that last column **before** the first note goes out. A column filled in advance is a column
that gets sent at 15:00 on a Friday.

### Overdue

`../scripts/update_clock.py` computes the next due time from `severity`, `customer_impact_confirmed_at`
and `updates_sent_at`, and **exits 1** when one is overdue. An overdue update is handled by
sending it late with the lateness named — "This is 20 minutes later than I said; that is on me" —
never by quietly resetting the clock.

---

## 3. Who sends, and who signs

The clock is set by severity. **The sender is set by severity *and* account weight**, because who
signs the note is the only legitimate place account value enters this skill.

| Sev | Sender | Countersigned / on the thread | Call first? (`C26`) |
| --- | --- | --- | --- |
| **S1** | VP+ or the incident lead | CSM on the thread, named, with a direct line | **Yes, always**, before the written note |
| **S2** | CSM | Their manager, cc'd | Yes for a top-decile account; otherwise the note leads and the call follows the same day |
| **S3** | CSM | — | No |
| **S4 · price, EOL, tier** | The executive who owns the decision | CSM on the thread | Yes for named accounts; the call goes a **day** before the list send, never the same hour |
| **S4 · departing CSM** (`R3` mirrored) | **The departing person**, before their last working day, with the successor named | The successor, cc'd | Yes |

**Never** send an S1 first note from a shared alias. A no-reply address on a note about a stopped
workflow tells the reader exactly how much of a conversation this is going to be.

---

## 4. Notice periods for planned changes

An S4 announcement has two independent tests, and **both** must pass:

1. **The policy period** — the notice length the change type deserves.
2. **`R1` · the opt-out calendar** — the announcement lands **before**
   `renewal_date − notice_period_days`, **computed per account.** A change announced after a
   customer's own notice window has closed is a change they had no way to decline, and it is the
   single most common way a legitimate price rise becomes a churn.

| Change | Default notice | Grounding |
| --- | --- | --- |
| **Price increase** | **90 days** before the effective date, and before every affected account's opt-out deadline | Contract benchmarks: **87%** of standardised cloud service agreements auto-renew, **84%** of those carry a **30-day** customer non-renewal notice, and **21%** include an automatic renewal uplift, most commonly **5–8%** `[V, Common Paper, 2026 SaaS Contract Benchmark Report, >1,000 cloud service agreements]`. 90 days clears the common 30- and 60-day windows with margin |
| **Product or feature end-of-life** | **365 days** | The de-facto standard among major platform vendors: Google Cloud commits to at least 12 months for GA services, IBM publishes a 12-month deprecation period, Square deprecates APIs at least 12 months before retirement, and Salesforce gives at least one year's notice before an API version's support ends `[V, published vendor deprecation policies — Google Cloud, IBM, Square, Salesforce developer documentation, accessed 2026-08]` |
| **API version deprecation** | **180 days** minimum, **365** where the customer has built against it | Same corpus; 6–12 months is the published range, and 12 months is where widely-used endpoints sit `[V]` |
| **Support tier or coverage change** | **90 days** | Practitioner convention; it changes an entitlement the customer budgeted for `[P]` |
| **Feature moving to a higher tier** | **90 days**, and never inside an active term | Treat as a price increase, because that is what it is |
| **Named CSM change** | **10 business days**, from the departing person | `R3` mirrored: when the departure is ours, the note goes out **before** the last working day with the successor named |
| **Planned maintenance with downtime** | **14 days**, plus a 24-hour reminder | Practitioner convention `[P]` |
| **Security or data incident** | Immediate; legal and security own the wording | Controller notifies the supervisory authority without undue delay and, where feasible, within **72 hours** of becoming aware; phased reporting is permitted; notifying affected individuals is a separate, high-risk-triggered duty `[L, Regulation (EU) 2016/679, Arts. 33–34]` |

### The opt-out arithmetic

```
opt_out_date = renewal_date − notice_period_days
margin       = opt_out_date − announce_date
```

| Margin | Verdict | Action |
| --- | --- | --- |
| `< 0` | **Breach.** Announced after their window closed | Do not send on that date. Move the effective date, not the notice. For that account the change starts at the *following* term |
| `0–13 days` | **Tight** | Call before the email, and expect the call to be about the timing rather than the change |
| `≥ 14 days` | OK | Proceed with the tiering in §7 |

`notice_period_days` comes from the signed contract, not from a policy default. Where it is
missing, the row reads `UNKNOWN — requires notice_period_days from the signed contract` and the
account is held back from the send. `../scripts/update_clock.py` prints one row per account and exits 1 on
any breach or unknown.

### SLA credits are not this skill's business

Where downtime crosses a contractual threshold, a credit may be **owed**. The widely-copied
shape is AWS's: **10% / 25% / 100%** of the monthly bill for the affected region, tiered by
availability band, with claims opened **within 60 days** of the affected billing period
`[V, Amazon Compute Service Level Agreement, accessed 2026-08]`. **Read your own SLA; do not
assume this one.** State that the entitlement exists and
who will contact them about it; **do not compute, offer or negotiate it inside the escalation
note** (`R11`). A concession attached to an apology becomes the expected response to every future
incident.

---

## 5. Timing — day, hour, blackout

`C26`: **bad news by voice, early in the week, early in the day.** Email removes tone and hands
the reader unlimited time to escalate before you can answer.

| Slot | Verdict | Reason |
| --- | --- | --- |
| Tue–Thu, 09:00–11:00 their time | **Best** | They can reach their own people the same day |
| Monday before 09:00 | Acceptable | Lands in the week-opening triage, which is where they want it |
| Any day 16:00+ | Poor | Forwarded at 16:55, discussed without you all evening, a position by morning |
| **Friday after 14:00** | **Refused for S4** | Compounds over a weekend with nobody available. If it must go, the sender is on the phone first and reachable all weekend, and the note says so |
| Their close week, quarter end, or a known launch | Move it, or say why it could not move | This is a `cs-context` fact; asking for it mid-incident is how you get closed |

**S1 and S2 have no timing window.** A live incident is sent when it is confirmed, at 03:00 on a
Sunday if that is when it is confirmed. The timing rules govern S4 — the news that has a
choosable date — and the closure and review notes.

**The call-first gate.** For genuinely bad news to a reachable account, the written note is the
**follow-up to a call**, never the first notification. Where the call could not be placed, the
note still goes — and the reason is stated above the divider, not hidden: *"Sent without a call:
Dana is unreachable until Thursday and the 14:00 update was due at 14:00."*

---

## 6. What the business model changes

Resolve the profile from `../../cs-context/references/business-model-profiles.md` first. A
consumption business apologising for seat downtime, or a self-serve business writing an
exec-to-exec note to an account with no executive, is the recognisable shape of generic output.

| Model | What "bad news" is | Impact stated in | Cadence and channel | The trap |
| --- | --- | --- | --- | --- |
| **Per-seat** | Downtime, a broken workflow, a seat-price rise | Users blocked × hours × their loaded rate | Per §2; email to the admin and the buyer | Quoting seat counts as the impact when the outage blocked one workflow used by 12 of 400 seats |
| **Consumption / usage-based** | Failed jobs, throttling, **billing for consumption we caused** — a retry storm we triggered is a bill they did not choose | Jobs, records, GB processed, **and the credited units** | Per §2, plus a billing line: what we are zeroing and when it shows on the invoice | Apologising for "downtime" when the customer's actual loss is a re-run they paid for twice. Compute the consumption impact before the note (`R11` still bars a discretionary credit — a *correction* of consumption we caused is not a concession) |
| **Flat tier** | Feature unavailability, tier repackaging | The specific capability and the workflow it blocked | Per §2 | Reaching for utilisation language that does not exist in this model |
| **Per-transaction / outcome** | Failed or mis-priced transactions, settlement delay | Transactions, value, settlement hours | S1 by default — their revenue is the unit | Treating it as a systems outage when it is a revenue event, which changes who must be told first (their finance lead, not their IT lead) |
| **Product-led / self-serve** | Outage, data loss, price change, plan repackaging | Accounts, workspaces, actions blocked | **In-product plus status page plus email to workspace admins.** There is frequently no exec, no sponsor and no QBR — inventing one produces absurd output | Writing an exec-to-exec note to a $99/month workspace. Above a value threshold, promote to the named-account path |
| **Enterprise sales-led** | All of the above, plus anything their procurement will re-read at renewal | Their units, with the arithmetic shown | Per §2, with the exec ladder in §3 | Under-escalating because the CSM has a good relationship with one contact |
| **Regulated vertical** (health, financial, public sector) | Anything touching audit trails, retention, reporting deadlines, or personal data | Their compliance obligation, named | Legal and security own the wording; this skill drafts the relationship note beside it | Sending the relationship note *before* the regulated notification, which puts a second, inconsistent account of the same event on the record |
| **Self-hosted / on-prem** | A defect in a version they run, an EOL of that version | Which of *their* deployed versions, and the upgrade path | Longer notice — they need a change window | Announcing on a SaaS timeline to a customer whose change board meets monthly |
| **Partner / channel-led** | Everything above, twice | Both the partner's units and the end customer's | The partner is told first and given the note to forward, **plus** a version they can send in their own name | Going direct to the end customer and destroying the partner's position, or hiding behind the partner and never reaching the affected user |

**Contract shape changes the notice arithmetic, not the note.** Monthly evergreen has no notice
period, so every day is the opt-out deadline and `R1`'s margin computation is meaningless —
announce a price change with a full billing cycle plus 30 days, and expect the answer within
days rather than at a renewal.

---

## 7. Many accounts, one change

For a planned change hitting many accounts, sequencing is the whole design. Three tiers, and the
gap between them is deliberate:

| Tier | Who | How | When |
| --- | --- | --- | --- |
| **1** | Top-decile ARR, every account with a live escalation, every reference customer, every account inside 14 days of its opt-out margin | Call from the named exec, then an individually-written note | **Day 0** |
| **2** | Named-CSM accounts | Individually-addressed note from their CSM, personalised at least in the impact line | **Day 1** |
| **3** | Everyone else | One list send, lowest-common-denominator wording | **Day 2** |

**Never run tier 1 and tier 3 in the same hour.** A top account learning about a price rise from
a bulk email, minutes before their CSM calls, learns two things at once — the change, and that
they are on a list.

**Assume the tier-3 wording reaches a competitor's account executive within the day.** Write it
so that is survivable: no internal reasoning, no apology for a commercial decision, no
implication that the change is negotiable for some customers and not others.

Every tier-1 and tier-2 account gets its own `R1` margin computed. **Accounts whose margin is
negative are removed from this announcement entirely** and take the change at their next term —
that is a per-account decision, printed in the internal brief with the arithmetic beside it.

---

## 8. Running the clock

Run from the skill directory:

```bash
python3 scripts/update_clock.py scripts/sample_incident.json
python3 scripts/update_clock.py incident.json --now 2026-08-28T13:30:00Z
```

| Input key | Supplies |
| --- | --- |
| `incident.severity` · `customer_impact_confirmed_at` · `updates_sent_at` | First-note deadline, next due time, overdue flag, the next five commitment times |
| `impact.units_affected` · `manual_minutes_per_unit` · `people_involved` · `loaded_hourly_rate` | The hours and cost arithmetic, with the working printed and the composite rounded |
| `planned_change.announce_on` · `effective_on` · `required_notice_days` | Notice given vs required |
| `accounts[].renewal_date` · `notice_period_days` | The per-account opt-out margin and the breach verdict |

Exit codes: **0** clean · **1** a breach, an overdue update, or a missing `notice_period_days` ·
**2** bad input. **Treat exit 1 as a stop, not a warning** — it means either a customer is owed a
note right now, or an announcement is about to go to someone who cannot decline it.

None of the script's output is customer-facing until it has been rewritten in their units and
passed the leak scan in `../../cs-context/references/customer-voice.md`.
