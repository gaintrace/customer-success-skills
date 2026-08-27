# Role Taxonomy

> Twelve roles, each with the data that identifies it, the test that proves it, and the
> specific failure that follows from getting it wrong. A role is a claim about what a person
> can *do* — release money, block a go-live, argue for us in a room we are not in. A title is
> a claim about nothing.
>
> Canonical field names come from `../../cs-context/references/normalized-schema.md`. Do not
> invent enum values; use the extension fields in §2 where the map needs a role the enum does
> not carry.

**Contents**
- [1. Why role labels fail](#1-why-role-labels-fail)
- [2. The canonical enum and its three extensions](#2-the-canonical-enum-and-its-three-extensions)
- [3. The role_confidence ladder](#3-the-roleconfidence-ladder)
- [3A. Mobilising capacity — champion vs supporter](#3a-mobilising-capacity--champion-vs-supporter)
- [3B. The authority triangle — signs, decides, influences](#3b-the-authority-triangle--signs-decides-influences)
- [4. The twelve roles](#4-the-twelve-roles)
- [5. Identification cheat-sheet — data to role](#5-identification-cheat-sheet--data-to-role)
- [5A. Signal families — where the people come from](#5a-signal-families--where-the-people-come-from)
- [6. What each role needs from us](#6-what-each-role-needs-from-us)
- [7. Veto map — who can stop what](#7-veto-map--who-can-stop-what)
- [8. Role concentration and the 1-2-3 shape](#8-role-concentration-and-the-1-2-3-shape)
- [9. Buying-committee context](#9-buying-committee-context)
- [10. Anti-patterns](#10-anti-patterns)
- [11. Which roles exist at all — by business model](#11-which-roles-exist-at-all--by-business-model)

---

## 1. Why role labels fail

Three failures account for nearly all of it.

| Failure | What it looks like | Consequence |
| --- | --- | --- |
| **Title-to-role mapping** | "VP" → economic buyer; "Manager, Ops" → champion | A forecast built on someone who cannot fund the line item |
| **Comfort mistaken for advocacy** | The person who replies fastest and is nicest is labelled champion | The account is single-threaded on someone who has never argued for us internally |
| **Set once, never revisited** | Roles assigned at signature and never touched again | Roughly 20–30% of B2B contacts change job in a year (UserGems, 2026) `[V]`; after two years the map is fiction |

The correction for all three is the same: a role label must name the **observed behaviour**
that earned it, and carry a date.

## 2. The canonical enum and its three extensions

`contact.role` accepts exactly these nine values:

`economic_buyer` · `champion` · `coach` · `admin` · `power_user` · `user` · `blocker` ·
`technical_evaluator` · `procurement`

Three roles the map needs are not enum values. Record them as extensions so downstream skills
that read `contact.role` still work:

| Map role | Stored as `contact.role` | Plus extension | Never do this instead |
| --- | --- | --- | --- |
| Executive sponsor (customer-side) | `economic_buyer` if they hold the budget, else `coach` | `is_exec_sponsor = true` | Add an `exec_sponsor` enum value |
| Legal | `procurement` | `function = legal` | Overload `blocker` |
| Security / compliance reviewer | `technical_evaluator` | `function = security` | Overload `admin` |
| Detractor | `blocker` | `contact.sentiment ∈ {negative, hostile}` | A separate `detractor` value |
| Supporter — warm, but cannot mobilise | `coach` | `is_supporter = true` + `mobilising_capacity` 0–1 | Label them `champion` because sentiment is high |
| Executive sponsor (ours) | *not a contact row at all* | `account.exec_sponsor_internal` | Store our own people as customer contacts |

## 3. The `role_confidence` ladder

The field that stops the map lying. Print it beside every role, every time.

| Tier | Entry criteria | Permitted use | Typical source |
| --- | --- | --- | --- |
| `verified` | The customer stated it out loud, or the person performed the role in front of us | Forecast commentary · renewal planning · exec escalation targeting | A call transcript, a signature, an observed approval |
| `evidenced` | An observable behaviour proves it | Analysis, gap planning, the map — always alongside the behaviour | Order form signature, escalation approval, admin grant, evaluation chairing |
| `asserted` | A CRM field, a job title, or an assumption | Print it, flag it, put confirmation on the next call agenda | `Contact.Role`, LinkedIn, a predecessor's note |

**Rule:** any conclusion that depends on an `asserted` role is reported at one confidence level
lower than the evidence would otherwise allow, and the dependency is named. A renewal forecast
resting on an `asserted` economic buyer is a forecast resting on a job title.

## 3A. Mobilising capacity — champion vs supporter

The most enthusiastic contact is frequently not the one who can build internal consensus, and
the one who can is often more sceptical, more senior and less pleasant to deal with. Sentiment
measures how they feel about us. **Mobilising capacity measures whether their opinion moves
anything**, and the two are scored separately because they are uncorrelated often enough to lose
accounts on.

`mobilising_capacity` is an integer 0–3, one point per test, evidence only. It is scored
**before** a `champion` label is written — the label is the output of the test, never an input
to it.

| Test | Point | What counts as evidence | What does not |
| --- | --- | --- | --- |
| **M1 · Has moved a decision through this org before** | +1 | A named instance: they got budget released, secured a security exception, or drove a rollout past a competing priority — with a date | "They're very influential" · seniority · being liked |
| **M2 · Others cite them** | +1 | Their name invoked as the reason in a thread or transcript they are not on; a colleague defers to them unprompted; someone says "let me check with X" | Being copied on everything · a large team |
| **M3 · Controls budget or headcount** | +1 | Owns a budget line, or has direct reports whose time they can reassign | A big title with a shared cost centre · signing authority they have never used |

**The classification rule:**

```
champion  ⇐ sentiment ≥ positive  AND  mobilising_capacity ≥ 2  AND  advocacy_events ≥ 1
supporter ⇐ sentiment ≥ positive  AND  mobilising_capacity ≤ 1
mobilising_capacity UNKNOWN ⇒ supporter until tested. Never champion by default.
```

**A supporter does not satisfy the champion requirement anywhere in this library.** Stored as
`coach` + `is_supporter = true`, they score **0.0** on the `champion` slot of `coverage_score` —
identical to an empty slot — and therefore cannot satisfy the 1-2-3 shape, the ARR-band coverage
floor, `R5`'s second-relationship test, `renewal-prep`'s relationship gate, `pre-call-brief`'s
advocacy read, or `save-play`'s escalation criteria. Any artifact in this library that asks "do
we have a champion?" reads the coverage slot, never the sentiment column.

This is deliberately harsh, and it is the correct default: the cost of treating a supporter as a
champion is a renewal planned around someone who cannot convene the meeting where it is decided.
The cost of treating a real champion as a supporter is one extra test on the next call.

**How to raise it, in order of yield:** ask them to introduce you to whoever `decides` (the
MEDDICC test `[P]` — refusal or deflection caps M at 1); ask what they had to do to get us
approved originally; ask who else had to agree, and what changed their mind. All three surface
M1 evidence in a single conversation, and none of them is answerable with politeness.

**The sceptic case.** A contact at `neutral` sentiment with M3 is worth more than an advocate at
M0. Score them, meet them, and treat the scepticism as an objection to answer rather than a
reason to avoid the room.

## 3B. The authority triangle — `signs`, `decides`, `influences`

Three separate fields, because the person who signs is often not the person who decides, and
neither may be the person whose opinion actually moves the decision. Collapsing them is how a
renewal is lost after a positive call with the wrong person.

| Field | Definition | Filled from | Proving test |
| --- | --- | --- | --- |
| `signs` | Whose name executes the paper and who is served notice. The pen, not the authority — frequently a delegate, a CFO, or a legal signatory who has never used the product | The executed order form; the MSA notices clause, which is also where `notice_period_days` really lives | Pull the last executed document. Anything else is `asserted` |
| `decides` | The power to say yes when others say no, and to release funds not attached to a budget line | An observed override; an unbudgeted approval; the person others defer to in a transcript | Name the instance. If nobody can, it is `asserted` |
| `influences` | Whose input visibly moved the decider — a reversal, a deferral, a "let me check with X" | A decision that changed after their objection; an approval leg added late to a thread; deference on a call | Point at the decision that moved. An opinion nobody acted on is not influence |

**Concentration.** Two of three on one `contact_id` is `CONCENTRATION 2/3`; three of three is
`CONCENTRATION 3/3 — single point of authority`, which the map prices at the depth-1 structural
floor (1.00) whatever the measured depth, and ranks first in the gap plan regardless of health.
Concentration is common in mid-market and it is never a simplification: it means there is
nobody to escalate to, nobody to appeal to, and one resignation between the account and zero
authority.

**The refusal.** With `signs` UNKNOWN and the opt-out deadline inside 120 days (`R1`),
`coverage_score` is capped at 2/4 however the other three roles score, and the primary play is
forced to the signatory trace — pull the executed order form and the notices clause, name the
signatory, and confirm whether they are still there. No sentence claiming coverage is adequate
may be emitted while `signs` is unknown, because the account cannot be renewed by someone whose
identity is a guess.

**Confirming it out loud** costs one sentence and people answer it generously: *"When we get to
the renewal, who actually signs, and does anyone else have to approve it before it reaches
them?"* Ask it at the QBR, not in the notice window.

## 4. The twelve roles

### 4.1 Economic buyer

| | |
| --- | --- |
| **Definition** | The person with overall authority — "the power to say yes when others say no, and say no when others say yes." Holds P&L responsibility and can access funds not attached to a budget line (MEDDICC) `[P]` |
| **Identify from** | Contract signatory · `opportunity` primary contact role · whoever appears on the approval leg of a procurement thread · the person others defer to in a transcript |
| **Proving test** | Have they personally overruled a stakeholder, or authorised spend outside an existing budget? If nobody can name an instance, the label is `asserted` |
| **If mislabelled** | You forecast against someone who cannot fund the renewal. The commonest cause of a renewal that "went dark in procurement" |
| **Departure impact** | Severe. Roughly 65% of accounts experiencing an executive change do not renew (Sturdy AI) `[V]` |

### 4.2 Champion

| | |
| --- | --- |
| **Definition** | Power **and** influence **and** a vested interest; sells internally when we are not in the room (MEDDICC) `[P]` |
| **Identify from** | `advocacy_events` > 0 · forwarded our material internally · brought a colleague to a meeting unprompted · defended us in a transcript |
| **Proving test** | `mobilising_capacity` ≥ 2 on §3A's M1–M3, **and** `advocacy_events` ≥ 1. Then ask them to introduce you to whoever `decides` — refusal or deflection caps M at 1 and reclassifies them |
| **Entry gate** | Never assigned on sentiment. High sentiment with M ≤ 1 is a **supporter** (§4.13), which scores 0.0 on the champion coverage slot |
| **If mislabelled** | The most expensive error in CS. You believe you have advocacy and you have politeness |
| **Departure impact** | Roughly 51% churn within 12 months of a champion departure (Sturdy AI) `[V]`. Act inside 48 hours |

### 4.3 Coach

| | |
| --- | --- |
| **Definition** | Gives information and introductions but lacks the power or influence to move a decision (MEDDICC) `[P]` |
| **Identify from** | High reply rate, useful intel, no observed internal advocacy, no attendance at decision forums |
| **Proving test** | The inverse of the champion test — they answer everything and introduce nobody |
| **If mislabelled** | Single-threaded on someone who cannot save the account, while the map reads "champion: present" |
| **Play** | Keep them. A coach is genuinely valuable for intel and for finding the real champion — just never count them in the coverage score as one |

### 4.4 Technical evaluator / gatekeeper

| | |
| --- | --- |
| **Definition** | Owns architecture, integration or platform standards; can block go-live unilaterally |
| **Identify from** | Integration and API activity · security questionnaire correspondence · attendance limited to technical reviews · named on the SSO or IdP configuration |
| **Proving test** | Can they stop a deployment without asking anyone? |
| **If mislabelled** | A veto discovered in week 11 of a 12-week plan |
| **Departure impact** | Moderate for renewal, severe for any migration or expansion in flight |

### 4.5 Security / compliance reviewer

| | |
| --- | --- |
| **Stored as** | `technical_evaluator` + `function = security` |
| **Identify from** | Requests for SOC 2, penetration-test reports, DPA, sub-processor lists · appears only at renewal or at a new-module go-live |
| **Proving test** | Did a previous release wait on their sign-off? |
| **If mislabelled** | Bypassing them. A security reviewer is the one role you can never bypass — the veto is structural, not political |
| **Renewal note** | An unsolicited security review >120 days from renewal is a vendor-risk refresh; a review paired with termination-clause questions is not |

### 4.6 Procurement / vendor management

| | |
| --- | --- |
| **Identify from** | First appearance clustered near the renewal window · requests for spend history, usage reports, contract summaries · `invoice` and PO correspondence |
| **Proving test** | Do they set the process, or execute someone else's decision? Ask who signs after they finish |
| **If mislabelled** | Negotiating hard with someone who was never the decision-maker, while the economic buyer disengages |
| **Signal value** | Procurement contact outside the normal renewal window is a **strong** risk signal. Disambiguate by the artifact requested: a security questionnaire is a review; termination-clause, notice-period, data-return or transition-assistance questions are not |

### 4.7 Legal

| | |
| --- | --- |
| **Stored as** | `procurement` + `function = legal` |
| **Identify from** | Redline threads · MSA and DPA correspondence · the notices clause, which is where `notice_period_days` actually lives |
| **Proving test** | Are they interpreting the contract, or drafting an exit from it? |
| **Critical use** | Legal is the only reliable source for the **opt-out deadline**. Verify `notice_period_days` against the executed MSA notices clause, not the CRM field — CRM contract fields are hand-maintained and routinely stale |

### 4.8 Admin

| | |
| --- | --- |
| **Definition** | Holds the in-product administrative role. Technical ownership, **not** authority |
| **Identify from** | `usage_daily.admin_actions` · permission grants · user invitations · SSO configuration |
| **Proving test** | Can they add a seat without asking anyone? Can they approve the invoice? (Usually yes to the first, no to the second) |
| **If mislabelled** | Treating the admin as the buyer. The single commonest reason a renewal conversation happens two levels too low |
| **Departure impact** | Operationally severe, commercially small — unless they are also the only two-way contact, in which case see `champion-risk.md` |

### 4.9 Power user

| | |
| --- | --- |
| **Identify from** | Top-decile `core_actions` within their cohort · feature breadth · the person other users' tickets reference |
| **Proving test** | Would the workflow break next week if they stopped? |
| **Value** | The best source of second and third contacts when closing a single-threading gap, and the best source of evidence for a value story a buyer will believe |

### 4.10 End user

| | |
| --- | --- |
| **Stored as** | `user` |
| **Identify from** | `usage_event.contact_id` with no admin actions and no tickets |
| **Value** | Individually low, collectively decisive — end-user counts are the utilisation number the buyer sees. Do not name them individually in the map unless one is a champion candidate |

### 4.11 Blocker / detractor

| | |
| --- | --- |
| **Definition** | Actively prefers an alternative or the status quo |
| **Identify from** | Negative transcript sentiment · a rejected feature request they raised · detractor survey response · consistently declines meetings while remaining in the org |
| **Proving test** | Have they voiced opposition **on record**? An inference from silence is not a blocker; it is an unknown |
| **If mislabelled** | Unmodelled opposition that surfaces at the renewal, when it is too late to answer |
| **Play** | Convert, contain or bypass — chosen deliberately. See `coverage-plays.md` §4 |

### 4.12 Executive sponsor

| | |
| --- | --- |
| **Theirs** | The executive whose budget funds us. Stored as `economic_buyer` + `is_exec_sponsor = true` when they hold budget, `coach` + the flag when they do not |
| **Ours** | Our own executive assigned to the account, with a scheduled cadence. Stored on the account, never as a contact |
| **Identify from** | QBR attendance at VP+ · the person whose delegate attends in their place · the escalation path when something broke |
| **Proving test (theirs)** | Would they take a 30-minute meeting on business outcomes without the champion arranging it? |
| **Why it matters** | PMI's Pulse research found organisations where more than 80% of projects had actively engaged executive sponsors reported 76% success against 46% where fewer than half did `[A]` |

### 4.13 Supporter

| | |
| --- | --- |
| **Stored as** | `coach` + `is_supporter = true` + `mobilising_capacity` 0–1 |
| **Definition** | Genuinely wants us to succeed and says so, and cannot move a decision through their own organisation |
| **Identify from** | Positive or advocate sentiment, fast replies, warm meetings — with no M1 instance, nobody citing them, and no budget or headcount |
| **Distinguishing test** | §3A. A coach lacks *interest*; a supporter has the interest and lacks the *capacity*. Both are excluded from the champion slot, for different reasons |
| **If mislabelled** | The coverage score reads "champion: present" and the renewal is planned around someone who cannot convene the meeting where it is decided |
| **Play** | Keep them and use them: they are the cheapest route to whoever scores M ≥ 2, and they will make the introduction a cold approach would not get. Never count them in coverage |

## 5. Identification cheat-sheet — data to role

Read this column-first when you have a data point and need a role.

| Observed | Most likely role | Confidence it supports | Second reading |
| --- | --- | --- | --- |
| Signed the order form | Economic buyer | `evidenced` | A delegate signing on the buyer's authority — check the approval thread |
| Named in the MSA notices clause | The person notice is served on | `verified` | Often legal, not the buyer |
| Grants permissions, invites users | Admin | `evidenced` | Power user with elevated rights |
| Files most tickets | Admin or power user | `evidenced` | An operator escalating on someone else's behalf |
| Appears only on P1 escalations | Exec sponsor or gatekeeper | `evidenced` | A manager pulled in once |
| Organises the recurring meeting | Programme owner (coach or champion) | `evidenced` | Rarely the buyer |
| Declines and sends a delegate | Sponsor; the delegate is the operator | `evidenced` | Genuine calendar conflict — check the rate, not the instance |
| Added late to a `Cc` at senior level | An approval chain above the thread | `asserted` | Courtesy copy |
| Requests SOC 2 / DPA / pen-test report | Security reviewer | `evidenced` | Procurement running a standard pack |
| Asks about notice period or data return | Legal, on an exit path | `evidenced` | A routine contract audit — verify before escalating |
| Replies fastest, never introduces anyone | Coach | `evidenced` | An under-tested champion — run the test |
| Top-decile usage, never on an email | Power user | `evidenced` | A shared service account — check `is_external_collaborator` |
| Disputes an invoice | AP or procurement | `evidenced` | The buyer, if the dispute is about value rather than terms |
| Hard bounce on their email | Departed | `evidenced` | Domain migration or mailbox quota — see `champion-risk.md` §3 |

## 5A. Signal families — where the people come from

The enumeration sweep is exhaustive by construction: walk all seven families every time, and
print a family with nothing to report as "checked, clear" rather than dropping it. The same
seven families carry the Coverage Ledger and the confidence cap (`R23`).

| # | Family | The people it reveals | Primary fields |
| --- | --- | --- | --- |
| 1 | Product usage & adoption | Admins, power users, end users, who invites whom, who went quiet | `usage_event.contact_id`, `contact.last_seen_product`, `usage_daily.admin_actions` |
| 2 | Commercial & contract | `signs`, `decides`, procurement, legal, the paper chain | `opportunity` contact roles, contract signatory, `subscription.notice_period_days` |
| 3 | Relationship & engagement | Everyone with a two-way interaction; meeting organisers; QBR attendance; who defers to whom (`influences`) | `interaction.customer_participants`, `interaction.direction`, `response_latency_hours` |
| 4 | Support & reliability | Ticket submitters (operators) vs escalation approvers (gatekeepers); reopeners, who are blocker candidates | `ticket.contact_id`, escalation CC lists, `ticket.reopened_count` |
| 5 | Sentiment & VoC | Survey respondents, who said what on a call, advocacy events, detractors on record | `contact.sentiment`, respondent identity, transcript speakers |
| 6 | Billing & payment | AP contacts, PO owners, whoever disputes an invoice | `invoice` contact, payment approver, dispute correspondence |
| 7 | Firmographic & external | Title changes, departures, reorgs, acquisitions, new executives | Enrichment/job-change feed, news, `account.parent_account_id` |

Families 2 and 3 are the two that fill the authority triangle (§3B); family 5 is the one whose
absence hides a blocker, which is why a map built without a VoC source states that gap explicitly
rather than reporting zero detractors.

## 6. What each role needs from us

Coverage is not just presence; it is presence with the right content. Arriving at an economic
buyer with a feature update wastes the meeting you spent three months getting.

| Role | What they are measured on | What to bring | What wastes their time |
| --- | --- | --- | --- |
| Economic buyer | The business outcome and the line item | Quantified outcome against their own baseline; the renewal shape | Feature releases, usage charts without a business frame |
| Executive sponsor (theirs) | Their function's results, and risk | One page, outcomes and money, the ask in the first paragraph | Recaps, status, our internal process |
| Champion | Being right about us internally | Ammunition: the numbers they will be asked for, in their language | Asking them for information we could derive ourselves |
| Coach | Being helpful | Reciprocity — intel, benchmarks, an introduction | Treating them as a decision-maker; it embarrasses them |
| Technical evaluator | Stability, standards, no surprises | Architecture answers, version specifics, known defects with dates | Marketing language — discounted instantly and permanently |
| Security reviewer | Audit exposure | Complete documentation on first request | Partial packs that force a second round |
| Procurement | Terms, price, process compliance | Clean paper, early, with the approval path mapped | Emotional appeals; a value story they cannot action |
| Legal | Risk in the words | Redlines that move, and a named counterpart | Renegotiating commercial terms through legal |
| Admin | Their workload | Fixes, workarounds, enablement, early warning of changes | Commercial conversations they cannot influence |
| Power user | Their own output | Advanced capability, a shortcut, a beta | Being surveyed instead of helped |
| End user | Getting today's work done | Working software and short enablement | Anything with the word "strategic" in it |
| Blocker | Being proved right | A direct answer to their specific objection, in writing | Cheerfulness, and going around them |

## 7. Veto map — who can stop what

| Decision | Can veto outright | Can delay indefinitely | Cannot stop it |
| --- | --- | --- | --- |
| Renewal | Economic buyer | Procurement, legal | Admin, users |
| Price increase | Economic buyer | Procurement | Champion |
| New module go-live | Technical evaluator, security | Admin (capacity) | Power users |
| Data-processing change | Security, legal | Procurement | Everyone else |
| Seat expansion | Economic buyer | Procurement | Admin (usually can provision) |
| Reference or case study | Legal, comms | Exec sponsor | Champion |

**Never bypass a row in column one.** A bypassed veto-holder who later acquires authority
becomes the reason the account is lost, and the bypass itself becomes the argument.

## 8. Role concentration and the 1-2-3 shape

When one person holds three or more roles, that is the finding — not a convenience.

| Concentration | Reading | Action |
| --- | --- | --- |
| One person holds `signs` + `decides` + `influences` | `CONCENTRATION 3/3`. There is nobody to escalate to and nobody to appeal to; the structural multiplier is floored at 1.00 whatever the depth (§3B) | Rank it first in the gap plan whatever the health score reads. The fix is a second relationship at or above the decider, not a second user |
| One person is buyer + champion + admin | Total dependency. Departure is an extinction event for the relationship | Price it, then treat closing it as the account's top priority regardless of health |
| Buyer and champion are the same person | Common in mid-market and not inherently wrong, but there is nobody to escalate *to* | Recruit a second champion one level down, in a different function |
| Champion and admin are the same person | The advocacy is operational, not strategic. It will not survive a budget review | Build the value story with a business-side second contact |
| No role concentration but depth 2 | Thin, not concentrated. Easier to fix — the structure is right, the count is low | Add breadth first, then height |

**The target shape** for high-touch accounts is Jay Nathan's 1-2-3 triangle — one executive
sponsor, two champions, three power users `[P]`. The point is not the count; it is that the
web survives the loss of any single person.

## 9. Buying-committee context

Renewals and expansions are governed by committee dynamics, not by one relationship. The
numbers below are why a depth of 1 is indefensible on any account of size.

| Finding | Source | Label |
| --- | --- | --- |
| A typical B2B purchase involves a team of about 10 people | 6sense, 2025 | `[M]` |
| 6–10 decision-makers per complex purchase, each independently gathering 4–5 pieces of information | Gartner B2B buying research, widely cited (secondary citation — verify before quoting to a customer) | `[V]` |
| 72% of B2B purchases involve high-complexity buying groups spanning multiple functions; 10 distinct decision-maker functions | Demandbase, 2025 | `[V]` |
| 52% of buying groups include decision-makers at VP level or above | TrustRadius, 2024 | `[M]` |
| 79% of purchases require CFO approval | TrustRadius, 2024 | `[M]` |
| 70% of buyers said they worked with so many people on the supplier side that they were unsure who everyone was | SBI, 2024 | `[M]` |
| Win rate by number of departments engaged: 1 → ~28%, 2 → ~39%, 3+ → ~44% | Outreach, vendor analysis of its own customers' deal data, methodology unpublished | `[V]` |
| 74% of respondents report most revenue comes from existing customers | Pavilion / 6sense, Customer Revenue Leadership Study 2025–26, 793 customer and post-sales leaders | `[M]` |

The SBI finding cuts both ways and is worth holding onto: breadth on our side without
coordination is experienced by the customer as chaos. Name one owner per relationship in the
map, and say who is *not* to contact whom.

## 10. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Deriving the role from the job title | Derive it from an observed behaviour, and cite the behaviour |
| Labelling the friendliest contact "champion" | Run the introduction test; a coach who cannot move a decision is a coach |
| A role assigned at signature and never revisited | Re-verify at every QBR and on every change event; contacts turn over ~20–30% a year |
| Recording a role with no date | Every label carries `role_confidence` and an as-of date |
| Storing our own executive as a customer contact | `account.exec_sponsor_internal`; our people are not their org |
| Inventing an enum value for legal or security | Use the documented extension fields; downstream skills read `contact.role` |
| Treating an empty `economic_buyer` field as "no buyer exists" | An empty field usually means not recorded. Say `UNKNOWN — requires a CRM contact-role audit` |
| Naming every end user in the map | Count them; name only champion candidates |
| Bypassing security or legal because they are "not the decision-maker" | They hold a structural veto. Convert or contain — never bypass |
| Counting a coach in the coverage score | Coverage counts economic buyer, champion, technical evaluator and exec sponsor only |
| Counting a supporter as a champion because sentiment is high | §3A. Score M1–M3 first. A supporter scores 0.0 on the champion slot, exactly as an empty slot does |
| One "decision maker" field standing in for the whole buying centre | §3B. `signs`, `decides` and `influences` are filled separately; when they collapse to one person, that is `CONCENTRATION`, priced at the depth-1 floor |
| Treating `signs` as unknowable because the CRM is empty | The executed order form and the MSA notices clause both name it. Inside the renewal window, unknown caps coverage at 2/4 and forces the signatory trace |

## 11. Which roles exist at all — by business model

Resolve this before scoring anything. Scoring the absence of a role the model does not contain
manufactures risk, and it is the most recognisable form of generic output. Full profiles:
`../../cs-context/references/business-model-profiles.md`.

| If the model is | Then |
| --- | --- |
| **Product-led / self-serve** | There is frequently **no champion, no exec sponsor and no QBR**, and scoring their absence manufactures risk. Map the workspace instead: admin, the person who invites, the top user. Coverage is "an identified admin plus one other active user", not four roles. Never emit a coverage gap for a $99/month workspace |
| **Consumption / usage-based** | The map follows **workloads, not seats**. One workload carrying the account is the structural single point of failure — map its owner as a first-class role. Whoever `decides` usually sits above the platform team, not inside it |
| **Sales-led enterprise** · **Partner / channel-led** | The full taxonomy applies and the paper chain (procurement, legal, security) is part of the map, not an appendix. In channel, keep two maps — the partner's buying centre and the end customer's; coverage on the partner is not coverage on the user, and `signs` may sit with the partner while `decides` sits with the end customer |
| **Regulated vertical** | Security and compliance reviewers hold a structural veto on a months-long cycle. Map them before T−90 (`R7`), not during the renewal. `bypass` is never available against them |
| **Multi-entity / post-acquisition** | Map per contract-holding entity. Coverage is the **minimum** across entities that can independently not renew, never the average, and each entity has its own authority triangle |
| **Monthly evergreen** | `R1` does not apply as written — there is no opt-out date, so champion risk and blocker dispositions are scored continuously rather than against a renewal, and the 120-day window rules read as "always in window" |
