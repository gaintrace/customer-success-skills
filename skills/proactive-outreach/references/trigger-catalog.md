# The Trigger Catalog

> 43 outreach triggers across the seven fixed signal families. Every one specifies the data
> condition that fires it, the channel, the sender, the timing window, the message frame, and the
> anti-pattern that ruins it. Walk this file in full on a book sweep. Do not sample it.

**Contents**
1. [The trigger contract](#1-the-trigger-contract)
2. [Strength tiers and decay](#2-strength-tiers-and-decay)
3. [Family 1 — Product usage & adoption (U1–U11)](#3-family-1--product-usage--adoption)
4. [Family 2 — Commercial & contract (C1–C6)](#4-family-2--commercial--contract)
5. [Family 3 — Relationship & engagement (R1–R5)](#5-family-3--relationship--engagement)
6. [Family 4 — Support & reliability (S1–S5)](#6-family-4--support--reliability)
7. [Family 5 — Sentiment & VoC (V1–V4)](#7-family-5--sentiment--voc)
8. [Family 6 — Billing & payment (B1–B4)](#8-family-6--billing--payment)
9. [Family 7 — Firmographic & external (X1–X8)](#9-family-7--firmographic--external)
10. [Suppression gate matrix](#10-suppression-gate-matrix)
11. [Instrumentation minimum](#11-instrumentation-minimum)
12. [Source register](#12-source-register)

Evidence tags used below: `[M]` measured benchmark with a named source and year · `[V]`
vendor-reported · `[P]` practitioner operating rule, not a measured statistic · `[D]` derived here
from stated assumptions. Never present a `[P]` or `[D]` number to a customer as an industry
benchmark.

---

## 1. The trigger contract

A trigger is only usable if all six fields are populated. Anything short of six is a hunch.

| Field | Definition |
| --- | --- |
| **ID + family** | The catalog ID and which of the seven fixed families detects it |
| **Condition** | Source system · normalised field · threshold. No threshold, no trigger |
| **Evidence** | The observed values with provenance tags, per `../../cs-context/references/evidence-standard.md` §2 |
| **Fired on** | The date the condition became true — not the date you noticed |
| **Strength** | T1–T6 (§2) |
| **Decay** | The date after which the trigger is no longer a legitimate reason to write |

Field names come from `../../cs-context/references/normalized-schema.md`. Do not invent parallel
vocabulary — a trigger written against `logins` when the schema says `usage_daily.core_actions` is
a trigger nobody else can reproduce.

Two columns appear in every response table and are worth defining once:

- **Window** — how long the trigger stays true *and* useful. Send inside it or suppress. Writing
  "I noticed last month that…" tells the customer exactly how long they waited for you.
- **Frame** — the sentence shape the message takes. It is not a template; it is the logic of the
  claim. The worked versions are in `message-library.md`.

---

## 2. Strength tiers and decay

Strength is about how much the customer has already told you, not how alarming the signal feels.

| Tier | Definition | Weight | Examples | Default decay |
| --- | --- | --- | --- | --- |
| **T1** | Declared intent — they asked, in words | 1.00 | Ticket asking for a gated capability, upgrade-page visit by a named admin, "can we add seats" in a transcript | 7 days |
| **T2** | Constraint hit — a commercial or technical boundary blocked them | 0.85 | Seat cap denial, entitlement limit, 429 rate limit, SLA breach, integration break | 14 days |
| **T3** | Behaviour change — a step change in what they do | 0.65 | Usage drop or spike ≥40%, silence ≥45 days, power user emerged, activation missed | 21 days |
| **T4** | Relationship or external event | 0.50 | Champion departed, exec sponsor changed, funding round, layoffs | 30 days |
| **T5** | Lifecycle or calendar | 0.35 | Opt-out deadline approaching, discount expiry, contract anniversary, day-N milestone | 45 days |
| **T6** | Informational | 0.15 | Product release, peer success story, regulation change | 60 days |

`[P]` — these tiers extend the T1–T6 signal-strength convention used in the expansion-signal
literature; the weights are an operating convention, not a measured conversion curve. Replace them
with your own observed reply and meeting rates by trigger ID as soon as you have ≥30 sends per
trigger (see `cadence-design.md` §6).

**Decay is not a nicety.** A trigger past its decay date has two honest dispositions: expire it,
or send a message that names the gap explicitly ("this has been sitting on my list for three
weeks and that's on me"). Sending the original frame late reads as a template that finally
dequeued.

---

## 3. Family 1 — Product usage & adoption

Source: product analytics (Amplitude / Mixpanel / PostHog / Pendo / Segment) → `usage_daily`,
`usage_event`. Cross-referenced with `subscription` for entitlement.

### Detection

| ID | Trigger | Condition — source · field · threshold | Strength | Decay |
| --- | --- | --- | --- | --- |
| **U1** | Usage drop | `usage_daily.core_actions` 30d mean ÷ prior 30d mean ≤ 0.60, and prior 30d mean > 0. **Compute per team as well as in aggregate** | T3 | 21d |
| **U2** | Usage spike | `usage_daily.core_actions` 30d ÷ prior 30d ≥ 1.40, or `usage_daily.active_users` +≥30% | T3 | 21d |
| **U3** | High-value feature never adopted | Feature entitled in `subscription.plan` and `usage_event.event_name` count = 0 over 90d, where the feature correlates with retention in your own cohort data | T5 | 45d |
| **U4** | New admin or user provisioned | `contact.first_seen_product` within 7d and `contact.role IN (admin, power_user)`; or `usage_event.event_name = 'user_invited'` | T3 | 14d |
| **U5** | Power user emerged | A contact in the top decile of `usage_event` volume for the account who was not in it 60d ago, and is not `contact.role = champion` | T3 | 21d |
| **U6** | Success milestone reached | `usage_event.event_name = 'milestone_completed'`, or a success-plan milestone marked achieved | T3 | **14d — the momentum window** |
| **U7** | Activation not reached by day N | `first_activation_event_date` IS NULL and `today − subscription.start_date ≥ N`, where N is the time-to-value target in `cs-context` §5 | T3 | 21d |
| **U8** | Entitlement limit approaching | `usage_consumed ÷ usage_entitlement ≥ 0.85`, or `distinct_users_30d ÷ seats_purchased ≥ 0.90`. Projected breach date computed from trailing-3-month growth | T2 | 14d |
| **U9** | Integration broken / disconnected | `usage_daily.integrations_active` decreased, or `integration_disconnected` / sustained auth-failure events | T2 | **48h** |
| **U10** | Seat provisioning gap (shelfware) | `seats_purchased − distinct_users_30d ≥ 25%` of `seats_purchased`, sustained 60d | T3 | 45d |
| **U11** | Relevant product release ships | Our release maps to a feature request they filed (`ticket.type='feature_request'`) or a capability they lack (U3) | T6 | 60d |

**Utilisation bands for U8 and U10** — `[P]`, the defaults most CS platforms ship with: <50% is a
downgrade risk and expansion is prohibited; 50–70% under-adopted; 70–85% healthy steady state;
≥85% expansion watchlist; ≥90% opportunity. Whichever platform holds your scorecard, check what
threshold its upsell playbook actually fires at before you inherit it — a band tuned for
consumption pricing fires far too late on seat-based contracts.

### Response

| ID | Channel | Sender → Recipient | Window | Frame | Anti-pattern |
| --- | --- | --- | --- | --- | --- |
| **U1** | Email; phone if the drop is in the buying team | CSM → the team lead whose team dropped | 7d | Name the specific workflow that stopped and ask whether it moved, broke, or ended | "Your usage is down" with no team, no metric, no window. It is also often *our* release that broke it — check before implying it is them |
| **U2** | Email | CSM → the admin driving it | 14d | Ask what changed, then ask whether the growth has headroom. Curiosity first, capacity second | Treating a spike as an instant upsell. A spike is often a one-off migration or a backfill |
| **U3** | In-app first, email second | Product-led / CSM → admin | 45d | Tie the unused feature to an outcome they already named, not to the feature's own merits | A feature tour. They did not adopt it because nobody showed them a reason, not because they didn't know it existed |
| **U4** | Slack if a shared channel exists, else email | CSM → the new person, cc the inviter | 14d | Welcome + the one thing that gets them productive this week + a named human | An onboarding drip that ignores that they joined an account already 14 months in |
| **U5** | Email | CSM → the power user, cc the champion | 21d | Name what they built or shipped, ask what they are trying to do next | Asking them for a reference on first contact. They do not know you yet |
| **U6** | Email; phone for a large milestone | CSM → champion, cc exec sponsor | **14d** | Their number, their baseline, their delta — then the next milestone and what it needs | Congratulating them on *our* metric ("you hit 10,000 events!"). Nobody's OKR is our event count |
| **U7** | Phone, then email | CSM → the admin who owns setup | 21d | Name the specific blocking step and offer to remove it, with a date | A "how's onboarding going?" email. They are stuck; asking is not helping |
| **U8** | Email to admin; separate note to the economic buyer | CSM → admin; CSM or AM → buyer | 14d | Blocked people and blocked work in their units, then the runway date, then two options including do-nothing | "You're at 94% of your licences." Meter-reading. State the denials, not the ratio |
| **U9** | Slack, else phone. Email only if neither exists | CSM or Support → the technical owner | **48h** | We found it before you reported it, here is what stopped, here is the fix and the ETA | Waiting for them to notice. A broken integration is a silent value killer and they will attribute the loss to you either way |
| **U10** | Email to the buyer, not the admin | CSM or AM → economic buyer | 45d | Offer to *right-size* before they discover it at renewal. Credibility now beats revenue later | Hiding it and hoping the renewal closes first. Their procurement runs the same report |
| **U11** | Email; in-app for volume segments | CSM → the person who asked | 60d | "You asked for this on [date]. It shipped. Here is the two-minute path to turn it on" | A release-notes blast. If they did not ask for it, this is a newsletter |

---

## 4. Family 2 — Commercial & contract

Source: CRM (Salesforce / HubSpot) → `subscription`, `opportunity`.

### Detection

| ID | Trigger | Condition — source · field · threshold | Strength | Decay |
| --- | --- | --- | --- | --- |
| **C1** | Opt-out deadline approaching | `subscription.opt_out_deadline − today ∈ {120, 90, 60, 30}`. Computed as `renewal_date − notice_period_days` | T5 | 14d per checkpoint |
| **C2** | Discount expiring | `subscription.discount_expires − today ≤ 120` and `discount_pct > 0` | T5 | 45d |
| **C3** | Contract anniversary | `today = subscription.start_date + 12n months` | T5 | 30d |
| **C4** | Seat reduction | `subscription.seats_purchased` decreased at any amendment | T2 | 14d |
| **C5** | Auto-renew switched off | `subscription.auto_renew` false and `auto_renew_changed_at` within 30d | T1 | **48h** |
| **C6** | Procurement or legal enters the thread | A contact with `role IN (procurement, blocker)` appears in `interaction.customer_participants` for the first time in 180d | T2 | 7d |

**Notice-period reality** `[V]`, contract-market guidance 2026: 30 / 60 / 90 days are the near
universal set, **30 days is the most common in standardised SaaS agreements**, and 60–90 days is
the market standard for negotiated enterprise agreements. If `notice_period_days` is unknown, the
trigger is `UNKNOWN — requires the executed contract`, and C1 cannot fire.

### Response

| ID | Channel | Sender → Recipient | Window | Frame | Anti-pattern |
| --- | --- | --- | --- | --- | --- |
| **C1** | Email, in writing, always | CSM at T−120/T−90; AM at T−60/T−30 | 14d | A courtesy notice naming the deadline date in plain words, plus the two things to settle before it | Letting the window pass quietly so the contract auto-renews. It is a bargaining chip, and the fastest way to destroy a reference account and the renewal two years out |
| **C2** | Email | AM → economic buyer | 45d | Raise it before they find it. Name the current rate, the standard rate, and what you propose | Discovering the discount cliff in the negotiation. Their finance team already has the number |
| **C3** | Email | CSM → champion, cc exec sponsor | 30d | A year of their numbers vs their baseline, then the year ahead. No ask | A "happy anniversary" note. Sentiment with no substance is worse than silence |
| **C4** | Phone, same day | CSM → the person who requested it | 14d | Ask what changed on their side. A reduction is partial churn that already happened | Processing the amendment as an admin task. Somebody made a decision and nobody asked why |
| **C5** | Phone, then exec-to-exec email | VP CS → exec sponsor, same day | **48h** | Not an outreach message — this is a `save-play` escalation. Confirm the decision, ask for the meeting | Emailing the CSM's usual contact. A flag flip is a decision taken above them |
| **C6** | Email | AM → the champion, asking who owns the process | 7d | Map the paper process by name and date before negotiating anything | Negotiating with procurement without the champion's map. You will concede against a process you never saw |

---

## 5. Family 3 — Relationship & engagement

Source: Gmail / Outlook / Slack / Calendly / CRM → `interaction`, `contact`.

### Detection

| ID | Trigger | Condition — source · field · threshold | Strength | Decay |
| --- | --- | --- | --- | --- |
| **R1** | Champion departure | `contact.email_status = 'hard_bounce'`, or Slack Connect `member_left`, or a LinkedIn/CRM title change, on a contact with `role IN (champion, economic_buyer)` | T4 | **48h** |
| **R2** | Exec sponsor change | A new contact with an exec title appears on the account, or the prior sponsor's `departed_at` is set | T4 | 7d |
| **R3** | Silence | `today − max(interaction.timestamp) ≥ 45` (Enterprise) / `≥ 60` (Mid-market) `[P]` | T3 | 30d |
| **R4** | Single-threaded | `COUNT(DISTINCT customer_participants)` across `interaction` in 90d ≤ 1 | T3 | 45d |
| **R5** | Relationship cooling | Meeting declined or postponed twice consecutively, or 30d mean `interaction.response_latency_hours` ≥ 2× the prior 90d mean | T3 | 21d |

**On R1/R2 magnitude.** No neutral published dataset puts a figure on how much churn traces to
leadership transitions, so do not carry one into a business case — count it yourself from your own
`churn-postmortem` records, which is the only number your CFO can audit anyway. What *is* measured:
Pew Research Center (2022) puts annual job-change rates at roughly 20% of workers `[M]`. Applied to
one named champion per account that implies roughly one champion in five turns over each year
(inferred — Pew measures workers, not champions, and it is a floor because it counts moves, not
internal role changes). On a 40-account book, expect R1 or R2 to fire around eight times a year and
expect to detect most of them from a bounce rather than from being told.

### Response

| ID | Channel | Sender → Recipient | Window | Frame | Anti-pattern |
| --- | --- | --- | --- | --- | --- |
| **R1** | Email to the next-most-senior known contact; exec-to-exec in parallel if ARR warrants | CSM → remaining contact; VP CS → their exec | **48h** | Acknowledge the change without speculating, state what is in flight and who is covering, ask who inherits it | Emailing the departed person's address again. It bounced; sending twice is a data-quality confession |
| **R2** | Exec-to-exec email, then a CSM email | VP CS → new exec; CSM → their chief of staff or the champion | 7d | Offer the 20-minute version of what their predecessor bought and what it has returned. Their problem is inheritance, not us | A welcome email that assumes they know what we are. They do not, and their default is to review the line item |
| **R3** | Email; different channel on touch 2 | CSM → champion | 30d | Do not apologise for the silence. Lead with the one thing that changed in their data while you were both quiet | "Just checking in." This is the exact trigger that produces the library's most-banned sentence |
| **R4** | Champion relay | CSM → champion, asking for one introduction | 45d | Name the specific role you are missing and why it protects *them*, not us | Cold-emailing four people on the account at once. That is a prospecting motion inside a paying customer |
| **R5** | Phone | CSM → champion | 21d | Ask directly whether the cadence still earns its place, and offer to change it | Increasing the cadence. If the reply latency doubled, more email is the wrong answer |

---

## 6. Family 4 — Support & reliability

Source: Zendesk / Intercom / Jira / PagerDuty → `ticket`.

### Detection

| ID | Trigger | Condition — source · field · threshold | Strength | Decay |
| --- | --- | --- | --- | --- |
| **S1** | Escalation resolved | `ticket.type='escalation'` moved to resolved within 7d | T3 | 14d |
| **S2** | SLA breach | `ticket.sla_breached = true` | T2 | **24h** |
| **S3** | Ticket requesting a higher-tier capability | `ticket` body matches a feature gated in a higher `subscription.tier`, or `paywall_viewed` / `feature_locked_clicked` events | T1 | 7d |
| **S4** | Volume spike then silence | `tickets_30d ≥ 2×` prior 30d, followed by 30d at ≤20% of that rate | T3 | 30d |
| **S5** | Their reported bug shipped | `ticket.linked_issue_id` reaches Done/Released | T5 | 30d |

**S4 is the one that hides churn.** Rising tickets → escalation → silence is a stronger churn
pattern than sustained complaint: they stopped asking because they stopped expecting. Never read
S4 as "the problems are fixed" without an S1 record to prove it.

### Response

| ID | Channel | Sender → Recipient | Window | Frame | Anti-pattern |
| --- | --- | --- | --- | --- | --- |
| **S1** | Email; phone for a Sev-1 | CSM → the person who escalated, cc their manager | 14d | What happened, what changed on our side so it does not recur, and what we owe them next. **No commercial ask for 30 days** | Following a resolution with an upsell. It reads as extraction and it is what the cooldown gate exists to stop |
| **S2** | Phone within the hour, email confirming | CSM or Support lead → the ticket owner | **24h** | Name the breach before they do, state the remedy, name the owner | A canned apology. They know how long it took; they want to know what changed |
| **S3** | Email | CSM → the requester, cc the admin | 7d | Their stated job to be done, then the capability, then what it costs. This is the highest-intent trigger in the catalog | Routing it silently to Sales. The requester asked *you*; a cold AE call three days later burns both |
| **S4** | Phone | CSM → champion | 30d | Ask what they stopped bothering to report | Reading the quiet as health and closing the account as green |
| **S5** | Email | CSM → the original reporter | 30d | "You reported this on [date]. It shipped in [release]. Here is what changed" | A generic release note. The point is that we remembered who asked |

---

## 7. Family 5 — Sentiment & VoC

Source: survey tool (Delighted / Pendo NPS / Qualtrics / in-app) and call transcripts (Gong /
Fireflies / Chorus) → `interaction.sentiment`, survey responses.

### Detection

| ID | Trigger | Condition — source · field · threshold | Strength | Decay |
| --- | --- | --- | --- | --- |
| **V1** | Detractor response | NPS 0–6, or CSAT ≤ 2 of 5 | T2 | **24h** |
| **V2** | Passive response | NPS 7–8 | T3 | 7d |
| **V3** | Promoter response | NPS 9–10, or CSAT 5 of 5 with free text | T3 | **14d — momentum window** |
| **V4** | Competitor named | A competitor name appears in a `ticket`, transcript, or email thread | T2 | 7d |

**Survey staleness.** A survey older than 90 days is a historical fact, not a current signal
(`../../cs-context/references/evidence-standard.md` §7). A 6-month-old NPS 9 from a champion who has
since left is worth nothing; discard it rather than carrying it forward.

### Response

| ID | Channel | Sender → Recipient | Window | Frame | Anti-pattern |
| --- | --- | --- | --- | --- | --- |
| **V1** | Phone if a number exists, email otherwise | CSM → the respondent | **24h** | Quote their own words back, state one thing you will change and by when, ask for 15 minutes. **Close the loop even when the answer is "we cannot fix that"** | An automated "sorry to hear that" reply. A detractor who gets an autoresponder has now been told twice |
| **V2** | Email | CSM → respondent | 7d | Ask the single most useful question in CS: *what would have made that a 9?* | Ignoring passives because the score is not red. Passives are the population that silently does not renew |
| **V3** | Email | CSM → respondent, cc champion | **14d** | Thank, then ask *one* of: an introduction, a reference, a case study, or a next-milestone conversation. Never two | Stacking an advocacy ask and an expansion ask in one message. Ask spacing is 14 days minimum `[P]` |
| **V4** | Phone | CSM → champion; escalate to VP CS if it appears in a transcript with the buyer | 7d | Do not mention the competitor. Ask what they are trying to solve that we are not solving | Sending a battlecard or a comparison page. It confirms you are watching and tells them nothing new |

---

## 8. Family 6 — Billing & payment

Source: Stripe / Paddle / ChartMogul / NetSuite → `invoice`.

### Detection

| ID | Trigger | Condition — source · field · threshold | Strength | Decay |
| --- | --- | --- | --- | --- |
| **B1** | Payment failure | `invoice.payment_failures ≥ 1` in the current cycle | T2 | **24h** |
| **B2** | Invoice overdue | `invoice.status='overdue'` and `today − invoice.due_at ≥ 15` | T2 | 14d |
| **B3** | Overage incurred | An invoice line of `type='overage'`, or `usage_consumed > usage_entitlement` | T2 | 14d |
| **B4** | Payment method expiring | `invoice.payment_method_status ∈ (expiring, expired)` | T5 | 30d |

**Read B1/B2 twice.** A first card decline on a self-serve account is an administrative event. A
first *late payment* on an enterprise account that has paid on time for eleven quarters is a
commercial signal — somebody in their finance function put a hold on it, and that person has an
opinion about the renewal. Check `contact.role = procurement` activity before deciding which one
you are looking at.

### Response

| ID | Channel | Sender → Recipient | Window | Frame | Anti-pattern |
| --- | --- | --- | --- | --- | --- |
| **B1** | Automated dunning email first; CSM email if it repeats | Billing system → billing contact; CSM → champion on the 2nd failure | **24h** | Practical and short: what failed, the one-click fix, who to call. No relationship language | The CSM chasing a card decline personally on touch 1. It burns a human touch on a form field |
| **B2** | Email; phone at 30 days | CSM → champion (not the AP inbox) | 14d | Ask whether the hold is administrative or a signal. Say that plainly | Escalating to collections before asking the champion. If it is a commercial signal, collections will discover it the expensive way |
| **B3** | Email | CSM or AM → the buyer | 14d | The overage amount, the run rate, and the committed-tier alternative with the honest indifference point | Letting overages accrue silently because they bill well. Every overage invoice is a reason to shop |
| **B4** | In-app + automated email | Billing system → billing contact | 30d | One line, one link | Making this a CSM task |

---

## 9. Family 7 — Firmographic & external

Source: news alerts / Crunchbase / LinkedIn / Clearbit / Apollo → `account.employee_count`,
`account.industry`, external feeds. This is the family most often entirely missing from a CS stack,
and it is where the best reasons to write live.

### Detection

| ID | Trigger | Condition — source · field · threshold | Strength | Decay |
| --- | --- | --- | --- | --- |
| **X1** | Funding round | Crunchbase / news: new round announced | T4 | 30d |
| **X2** | M&A | They acquire, or they are acquired | T4 | 30d |
| **X3** | Layoffs / restructuring / hiring freeze | News, or `account.employee_count` down ≥10% QoQ | T4 | 30d |
| **X4** | Leadership change announced | New CxO or VP in a function we serve | T4 | 14d |
| **X5** | New office, market or geography | News, careers page, or job postings by location | T4 | 45d |
| **X6** | Competitor news aimed at them | Our competitor announces a product, price move, or a logo in their vertical | T6 | 30d |
| **X7** | Peer success story | Another customer in their vertical and size band publishes or agrees to a result | T6 | 60d |
| **X8** | Industry regulation change | A rule takes effect in their sector that our product touches | T6 | 60d |

### Response

| ID | Channel | Sender → Recipient | Window | Frame | Anti-pattern |
| --- | --- | --- | --- | --- | --- |
| **X1** | Email | CSM → champion; VP CS → exec sponsor if ARR ≥ segment threshold | 30d | Congratulate in one line, then ask what the round changes about their plan for the next two quarters. No pitch | Immediately proposing an expansion. Everyone in their inbox did that on the same morning |
| **X2** | Phone | CSM → champion; AM in parallel | 30d | Ask which side of the integration they are on, and what happens to their tooling review. This is either the biggest expansion or the biggest risk on the book | Waiting to see. Post-M&A tool rationalisation lists get written in the first 90 days |
| **X3** | Email | CSM → economic buyer | 30d | Change the whole frame to value per dollar. Offer to right-size before they ask. Do not mention adoption | An adoption message. Their problem is cost, and an adoption nudge tells them you have not read the news |
| **X4** | Exec-to-exec email | VP CS → the new leader | 14d | The 20-minute inheritance briefing: what was bought, why, what it has returned, in their predecessor's words | Waiting for them to reach out. New leaders review line items in their first quarter and default to cutting what nobody explained |
| **X5** | Email | CSM → champion | 45d | Ask whether the new site needs its own configuration, residency, or seats. Operational, not commercial | Treating it as a seat-count opportunity in the first message |
| **X6** | Do not send in isolation | — | 30d | Only useful *fused* with a V4 or a usage signal. On its own it has no reason to exist | Sending a competitive comparison unprompted. You have just introduced the competitor into the account |
| **X7** | Email | CSM → champion | 60d | Name the peer's specific mechanism and the number, and ask whether the same constraint applies to them | "Most customers your size buy X." Social proof without a stated mechanism is a pitch |
| **X8** | Email; webinar for a segment | CSM or Product Marketing → the compliance owner | 60d | What the rule requires, what our product already does about it, what they must configure, and by when | Fear-based framing. Regulators are already doing that job |

---

## 10. Suppression gate matrix

Which gates apply to which family. `✖` = the gate blocks this family's triggers; `commercial` =
blocks only the asks, not the operational message.

| Gate | U | C | R | S | V | B | X |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Account fatigue cap (≤4 / 30d) | ✖ | ✖ | ✖ | — | — | — | ✖ |
| Person fatigue cap (≤2 / 14d) | ✖ | ✖ | ✖ | — | ✖ | — | ✖ |
| Post-Sev-1 cooldown (14d) | commercial | commercial | — | — | — | commercial | commercial |
| Post-escalation cooldown (30d) | commercial | commercial | — | — | — | commercial | commercial |
| Onboarding blackout (start → TTFV) | commercial | commercial | — | — | ✖ (V3 only) | — | commercial |
| Post-uplift blackout (90d) | commercial | commercial | — | — | — | — | commercial |
| Renewal endgame (opt-out −30 → renewal) | commercial | — | — | — | commercial | — | commercial |
| Ask spacing (90d between asks; ≤2 / yr) | commercial | commercial | — | — | commercial | — | commercial |
| Health gate (band ≥ At Risk) | commercial | commercial | — | — | ✖ (V3 only) | — | commercial |
| Open-loop gate (we owe them) | ✖ | ✖ | ✖ | — | — | — | ✖ |

Support (S) and billing (B) operational messages are never suppressed by fatigue — a broken thing
and a failed payment are service, not outreach. C5 and R1 are never suppressed at all; they route
to `save-play`.

Cooldown, blackout and ask-spacing values follow published expansion-timing conventions `[P]`:
14 days post-Sev-1, 30 days post-escalation-closure, 90 days minimum between distinct asks to the
same buyer, a maximum of 2 expansion asks per account per year, an onboarding blackout until
verified time-to-first-value, and a 90-day blackout after a price increase takes effect.

---

## 11. Instrumentation minimum

Triggers you cannot detect are triggers you do not have. If these events are not emitted, mark the
family `❌ Missing` in the Coverage Ledger rather than assuming the accounts are clean.

| Event / field | Required properties | Triggers it enables |
| --- | --- | --- |
| `seat_limit_reached` / `invite_blocked` | `account_id`, `attempted_user_email`, `inviter_id`, `ts` | U8 — highest-yield and almost always missing |
| `paywall_viewed` / `feature_locked_clicked` | `account_id`, `user_id`, `feature_key`, `ts` | S3, U3 |
| `usage_meter_snapshot` (daily) | `account_id`, `meter_key`, `value`, `included_qty`, `ts` | U8, B3 |
| `integration_connected` / `integration_disconnected` | `account_id`, `integration_key`, `ts` | U9 |
| `milestone_completed` | `account_id`, `milestone_key`, `verified_by`, `ts` | U6 |
| `user_invited` / `first_seen_product` | `account_id`, `invitee_email`, `ts` | U4, U5 |
| `contact.email_status` | Bounce classification written back from the mail system | R1 — the single strongest departure signal |
| `subscription.notice_period_days` + `opt_out_deadline` | Populated from the executed contract, not assumed | C1, and the Timing multiplier in every rank |
| `subscription.auto_renew_changed_at` | Timestamp, not just the boolean | C5 |
| `interaction` rows for every outbound send | `type`, `direction`, trigger ID, body | Every fatigue cap and every reply-rate measure |

The last row is the one teams skip, and it silently disables the entire suppression layer: without
a logged send you cannot compute a fatigue cap, so the caps quietly evaluate to "clear" and the
account gets seven emails in a fortnight.

---

## 12. Source register

| Source | What it supplies here | Reliability |
| --- | --- | --- |
| Alert-hygiene conventions (common CS-ops practice) | Alerts must be actionable, owned by a named person, and carry real risk if ignored; tier into act-today / watch-this-week / information-only; collapse to account level; fire once on first condition; measure action rate; retune quarterly | Practitioner `[P]` — design rules, no measured claim attached |
| Play-shape conventions (common CS-ops practice) | Sponsor-change pair (VP CS email then CSM email); four-touch tech-touch sequence (email → in-app → phone → follow-up email) | Practitioner `[P]` — shapes, not outcomes |
| Pew Research Center (2022) | ~20% annual job-change rate — the base rate for R1 frequency | Measured `[M]` |
| Contract-market guidance (2026) | Notice periods 30/60/90 days; 30 most common in standardised SaaS agreements; 60–90 standard in negotiated enterprise agreements | `[V]` |
| Expansion-timing conventions (Lincoln Murphy, *Logical Expansion* / *Success Milestones*; CS-platform defaults) | Momentum window of 14 days after a verified milestone; cooldowns; ask spacing; onboarding and post-uplift blackouts; no new asks inside T−30 | Practitioner `[P]` |
| Common CS-platform defaults | Seat-utilisation bands (<50 / 50–70 / 70–85 / ≥85 / ≥90) | `[P]` |

**Dropped for want of a neutral source.** Figures on CSM:account ratios by touch model, on the
share of churn caused by leadership transitions, and on the reply rate of a sponsor-change play all
exist only in vendor case studies. They are not quoted here in any form, because a number kept
without its source becomes a fabrication the first time someone repeats it. Measure your own.

**Could not verify.** No published dataset was found for reply rates on *customer* (as opposed to
cold prospect) outreach, for optimal spacing between CS touches, or for in-app message engagement
benchmarks. Where this catalog states a day count for spacing or a window, it is `[P]` or `[D]` and
is labelled as such. Replace every one of them with your own measured rates by trigger ID.
