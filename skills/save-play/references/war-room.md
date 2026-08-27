# The War Room

> How a save play is opened, run, updated and closed. The structure below is deliberately
> bureaucratic in exactly two places — the DRI selection order and the exit criteria — because
> those are the two decisions that, left informal, cost weeks.
>
> The operational spine is GitLab's published Customer Success Escalations Process `[PROD]`, the
> most complete public production model, adapted for a commercial save rather than a technical
> escalation. Where this file states a threshold with no source, it is a practitioner convention
> `[P]`, not a benchmark.

**Contents**
- [Open criteria](#open-criteria)
- [Severity](#severity)
- [Account escalation is not ticket escalation](#account-escalation-is-not-ticket-escalation)
- [The DRI](#the-dri)
- [Channel, standup and record](#channel-standup-and-record)
- [Exit criteria](#exit-criteria)
- [The standing update](#the-standing-update)
- [Suppression while a play is open](#suppression-while-a-play-is-open)
- [Checkpoints](#checkpoints)
- [Closure](#closure)
- [The will-churn transition](#the-will-churn-transition)
- [Anti-patterns](#anti-patterns)

---

## Open criteria

A save play is expensive — two to three per CSM at a time (`R13`) — so the entry gate is written
down and applied consistently. Opening plays on accounts that need a phone call devalues every
real one, and the organisation learns to ignore the flag.

| Trigger | Severity | Opens |
| --- | --- | --- |
| Notice of non-renewal received | Critical | Same day |
| Stated intent to cancel, in writing or on a call | Critical | Same day |
| Auto-renew switched off **by the customer** | Critical | Same day (`R2`) |
| Termination or opt-out language requested from legal or procurement | Critical | Same day |
| Risk band Critical (85+) | Critical | Same day |
| Two or more P0 compound patterns matched in `churn-risk` | Critical | Same day (`R4`) |
| Risk band High (65–84) with the opt-out deadline inside 90 days | High | 2 business days |
| Risk band High with a named cause the CSM cannot resolve alone | High | 2 business days |
| Reference or top-decile-ARR account red two consecutive weeks | High | Same week |
| Bulk data export by an admin plus any usage decline | Critical | Same day |

**Verify before declaring.** Auto-renew flags are switched off by our own team for re-papering more
often than teams expect; confirm the change originated with the customer within 24 hours. A false
Critical costs internal credibility, and you only get a few.

**Do not open a play for:** a single aged ticket, a Watch-band account, an account nobody has
called, or "the CSM is worried". Those route to `book-of-business-triage` or `proactive-outreach`.

## Severity

Severity sets cadence and who is in the room. It is not a measure of how upset anyone is.

| Severity | Definition | Internal cadence | Customer cadence | Leadership |
| --- | --- | --- | --- | --- |
| **Critical** | High risk of losing the customer or a significant contraction; the relationship and the brand are exposed | Daily minimum | 3+ times per week | VP CS, CRO, VP Product; CCO informed same day |
| **High** | Major issues affecting their ability to deploy or use the product; risk of loss, contraction or future growth | 3× per week | Weekly | VP CS, CS director |
| **Medium** | Issues affecting adoption and therefore the renewal, but not the relationship | Weekly | Fortnightly | CS manager |

Product engagement scales with severity: at High, a named product manager; at Critical, a product
leadership member `[PROD]`. The principle worth copying is the **stable counterpart** — the
assigned leader stays until resolution even as individual specialists rotate in and out, so the
customer never has to understand how you are organised.

Severity is reviewed at every checkpoint and can go down as well as up. A severity that only ever
increases is a severity nobody trusts.

## Account escalation is not ticket escalation

The most common structural error. GitLab states it directly: *do not open an account escalation to
raise the priority of a support ticket* `[PROD]`.

| | Ticket escalation | Account escalation (a save play) |
| --- | --- | --- |
| **Subject** | One issue moving too slowly | The whole commercial relationship |
| **Owner** | Support | The DRI selected below |
| **Exit** | The ticket is resolved | The renewal decision is changed, or the exit is managed |
| **Wrong use** | Using a save play to jump a support queue | Using a support escalation to handle a churn risk |

Where a defect is genuinely the root cause (RC4), both exist: a ticket escalation inside support,
and a save play above it. One channel per distinct issue, with the reason in the channel name, so
the reasons for each stay focused `[PROD]`.

## The DRI

**One directly responsible individual, selected by a fixed order so no time is lost deciding.**

| Order | Condition | DRI |
| --- | --- | --- |
| 1 | A professional-services project is live on the account | The PS project manager |
| 2 | Otherwise, a CSM is assigned | The CSM |
| 3 | Otherwise | The regional CS manager |

| The DRI owns | The DRI does **not** own |
| --- | --- |
| Articulating the resolution approach | Attending every meeting — deep technical sessions run without them, so the DRI never becomes the bottleneck |
| Coordinating internal and customer resources | Doing the engineering work |
| **All communications to the customer** | The commercial negotiation, if a renewal manager owns it |
| Next steps, with owners and dates | The decision to spend beyond the approved ceiling |
| The business case for any product escalation | |

**The single-owner rule.** One person owns the plan, the customer communications and the next
steps. Splitting ownership is measurably expensive: TSIA's *State of Customer Growth and Renewal
2025* reports sales account executives handling medium-complexity renewals cost roughly 3× more
and land about 10% lower net renewal rates than dedicated renewal specialists `[M]`. The manager's
role is to ensure forward motion continues, and to step in and drive when it does not.

## Channel, standup and record

| Element | Requirement |
| --- | --- |
| **Channel** | `#save_<customer>` — created immediately, **public**, prefix-based so it is captured by retention policy. Opening message pins the record link and the initial ask; the record is bookmarked |
| **One channel per distinct issue** | `#save_acme_perf`, `#save_acme_pricing`. Mixing two causes in one channel produces two half-run plays |
| **Standup** | Set up and documented **within 24 hours**, recurring for the life of the play, with stakeholders invited directly rather than notified |
| **Record** | A formal object on the account with required fields: severity, DRI, cause code, ARR at stake, exit criteria, checkpoint dates, stop-loss condition, concession authority, customer obligations |
| **Declaration** | Posted to a company-wide channel: customer · severity · DRI · cause · ARR · exit criteria · decision date. Anyone in the company can then contribute what they know |

**The declaration is not a status update; it is a request for information.** The person who knows
that this customer's new CFO used to work at a competitor is rarely on the account team.

The record's required fields exist so the play can be audited later. In particular:

| Field | Why it is required |
| --- | --- |
| `exit_criteria` | Written at declaration, not at closure — see below |
| `stop_loss_condition` | The play is honest only if it can end (`R21`) |
| `concession_authority` | Pre-approved latitude, agreed **before** the customer conversation, so nobody improvises under pressure |
| `customer_commitment_required` | A plan with no customer obligations is a wish |
| `checkpoint_dates` | Explicit go/no-go dates, set on day one |
| `exec_sponsor_assigned` | A named person with a scheduled cadence, not "available if needed" |

## Exit criteria

**Written at declaration. This is the single most-skipped step and the reason saves run forever.**

| Property | Requirement |
| --- | --- |
| Written when opened | A required field on the record; the play cannot be declared without it |
| Specific and observable | "Relationship restored" fails. "Two named contacts engaged, a signed order form dated by 14 Oct" passes |
| Re-confirmed at every update | The standing update asks explicitly whether they have changed |
| **Mutually agreed to close** | Both sides agree the situation is resolved, documented in an email or a record entry `[PROD]` |
| Written in the customer's terms where possible | "P95 page load under 2s sustained 14 days, confirmed by their platform lead" beats "performance improved" |

| Cause | A good exit criterion |
| --- | --- |
| RC1 | The buyer agrees a forward metric and signs a re-baselined success plan |
| RC2 | Customer-verified first value event logged |
| RC3 | Written acceptance of the commitment, the workaround, or the no |
| RC4 | The customer's technical lead confirms the defect trend, in writing |
| RC5 | Three engaged contacts with a two-way interaction in the last 30 days |
| RC6 | Successor restates the business objective in their own words, second contact active |
| RC7 | A signed smaller contract with an expansion trigger recorded |
| RC8 | Included in the evaluation with criteria and a date, or a documented loss with the reason |
| RC9 | Included in the consolidation decision with criteria and a date |
| RC10 | Offboarding completed, exit interview done, qualification finding filed |
| RC11 | Signed at an agreed structure |

## The standing update

Every checkpoint, five questions, every time `[PROD]`:

1. What is the current status?
2. What are the next steps?
3. Who owns each next step?
4. **Have the exit criteria changed? If so, what are they now?**
5. **Is anything owed to the customer this week that is classed `bad` — and who is calling, when?**
   (`C26`) Name the caller and the slot, or write "nothing owed". A blank is not an answer.

The fourth question is the one people skip. Exit criteria drift silently as a situation evolves, and
a play measured against criteria nobody has restated is a play nobody can close. The fifth is the
one that decides how the play is remembered: bad news that reaches a customer as an email, before
anyone has said it out loud, costs more trust than the news itself. The slot is computed —
Monday–Wednesday, 08:00–11:30 recipient-local — and Friday is refused
(`difficult-register.md`).

The health-update structure below is worth reusing verbatim for the written entry `[PROD]`:

```
CURRENT STATE     Usage · adoption · sentiment, with dates
CONSIDERATIONS    Context outside our control: M&A, reorg, budget cycle, freeze windows
WATCH ITEMS       What could still go wrong
NEXT STEPS        Dated actions with owners
IF A WORKSTREAM IS COLD
    Why are they blocked?   What is the mitigation?   What help is needed?
```

Cadence for the written entry: monthly for all accounts, **weekly for any account in an open
play**, and each weekly entry must state progress against the risk over the past week and the plan
for the coming one `[PROD]`.

## Suppression while a play is open

One owner, one voice (`R17`). For the life of the play, suppress:

| Suppressed | Why |
| --- | --- |
| Marketing and lifecycle email to every contact on the account | Uncoordinated multi-team sending trains customers to ignore all of it |
| NPS, CSAT and in-app surveys | Asking a customer to score you mid-escalation produces a detractor and tells them nobody is coordinating |
| Expansion outreach and upsell sequences | Expansion on a red account is extraction (`R8`) |
| The ordinary cadence queue from `proactive-outreach` | It defers entirely; the play owns the relationship |
| Automated usage and renewal-reminder notifications | They arrive as tone-deaf in the middle of a difficult conversation |

Add the account to the suppression list on the day the play opens, and remove it on closure — an
unremoved suppression is how an account goes quiet for two quarters after a successful save.

## Checkpoints

Two minimum, both dated at declaration.

| Checkpoint | When | Tests |
| --- | --- | --- |
| **CP1 — is the play landing?** | ≤14 days from open | The working signals for the chosen play. Meeting accepted? Owner named? First artifact delivered? |
| **CP2 — go/no-go** | Opt-out deadline − 21 days | Are the exit criteria reachable in the time left? Run `save_economics.py` again with the actual hours spent |
| **CP3+** | Weekly at Critical | Same four questions; severity reviewed |

At each checkpoint the outcome is one of exactly four, and it is written down:

| Outcome | Meaning | Next |
| --- | --- | --- |
| **Continue** | Working signals present, criteria reachable | Keep the plan; confirm the next checkpoint |
| **Adjust** | Play is right, sequence is wrong | Revise the sequence, not the cause. Changing the cause requires re-diagnosis |
| **Restructure** | The account is savable at a different shape | Move to RC7 or RC11 structure work; re-run the economics |
| **Exit** | A stop-loss trigger fired | Open the managed exit in `graceful-exit.md` |

## Closure

Every play closes explicitly, with a written record `[PROD]`:

- Did this end positively, negatively, or with no outcome?
- Were the defined exit criteria met?
- What actually moved the outcome — the artifact, the person, the concession, or nothing we did?
- What did the customer say, in their words?
- The account's new state, and the date the customer **decided** (`R24`), not the date service ended.

Then: archive the channel · remove the suppression · update the health state · re-categorise the
renewal opportunity · post the closure notification · hand the record to `churn-postmortem`.

**Affirmatively closing a risk matters as much as declaring it.** Unclosed risk states corrupt the
forecast, and an account that quietly stops being at risk teaches the organisation nothing about
which plays work.

## The will-churn transition

Before an account may be marked will-churn, all of the following must be true `[PROD]`:

1. Every option discussed in the play has been exhausted, and the record shows them.
2. The DRI has manager agreement.
3. The renewal opportunity is re-categorised, with a called value.
4. The loss is coded to a root cause, with the decision date.

Making the give-up decision a formal, approved transition prevents both silent abandonment and the
indefinite zombie save — the play that nobody has stopped and nobody is running, which consumes a
CSM's quarter while everyone assumes someone else is on it.

## Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Exit criteria written at closure | Written at declaration; a required field |
| A committee instead of a DRI | One name, chosen by the fixed order |
| A private channel | Public and prefixed, so people who know something can find it |
| Two causes in one channel | One channel per issue, with the reason in the name |
| The DRI in every meeting | They own the outcome, not the calendar |
| A play with no checkpoint dates | Two minimum, both set on day one |
| Severity that only ever rises | Review it at every checkpoint; downgrade when the facts change |
| A save plan with no customer obligations | Name their person, their action, their date |
| Concession authority agreed during the customer call | Pre-approved before it, or nobody is negotiating — they are conceding |
| Surveys and marketing still firing | Suppress on the day the play opens |
| Closing without a record | The closure record is the only input `churn-postmortem` has |
| Marking will-churn without manager agreement | A formal transition, or the forecast is fiction |
