# Org Inference

> You will almost never be handed an org chart. You will be handed an email archive, a
> calendar, a ticket queue and a contact export, and from those you can reconstruct most of
> the structure that matters — provided every line you draw is labelled with how you got it.
>
> The rule that governs this whole file: **an inferred reporting line is drawn dashed, written
> as "understood to report to", and confirmed out loud.** Confirming an inferred org chart is
> one of the cheapest and highest-yield questions in customer success. It is flattering, it
> takes ten seconds, and people correct it generously.

**Contents**
- [1. What you are actually inferring](#1-what-you-are-actually-inferring)
- [2. The signal table](#2-the-signal-table)
- [3. Thread-position analysis](#3-thread-position-analysis)
- [4. Calendar behaviour](#4-calendar-behaviour)
- [5. Product and support telemetry](#5-product-and-support-telemetry)
- [6. Seniority bands](#6-seniority-bands)
- [7. Composing the structure](#7-composing-the-structure)
- [8. Confirming it out loud](#8-confirming-it-out-loud)
- [9. Multi-entity accounts](#9-multi-entity-accounts)
- [10. Identity resolution traps](#10-identity-resolution-traps)
- [11. Anti-patterns](#11-anti-patterns)

---

## 1. What you are actually inferring

Three separate structures live underneath the phrase "org chart", and conflating them is the
first mistake.

| Structure | Question it answers | Best evidence | Decays |
| --- | --- | --- | --- |
| **Reporting** | Who does this person report to? | Titles, thread position, delegation patterns | Slowly (reorgs) |
| **Decision** | Who has to agree before money moves? | Approval threads, procurement participation, who ends a thread | Per purchase |
| **Operating** | Who actually does the work with us? | Product telemetry, ticket submission, meeting attendance | Fast (weeks) |

The **decision** structure is what governs a renewal, and it is rarely identical to the
reporting structure. A director with budget authority outranks a VP without it for our
purposes. Draw the reporting structure because it is legible; annotate the decision structure
on top of it, because that is the one that matters.

## 2. The signal table

| Observable | Inference | Confidence | The trap |
| --- | --- | --- | --- |
| Meeting-invite organiser vs attendee | Organiser is the programme owner, usually not the buyer | **High** | An assistant or a coordinator organises on someone's behalf — check whether the organiser ever speaks |
| Who is copied on contract and procurement threads | The paper-process participants and the approval chain | **High** | Standard distribution lists copy people who have no role |
| Ticket submitters vs whoever approves an exception | Operator vs gatekeeper | **High** | A manager filing on behalf of their team looks like an operator |
| In-product admin and permission grants | Technical ownership — **not** authority | **High** for technical roles only | The commonest source of a renewal conversation held two levels too low |
| Senior addresses added late to a `Cc` | An approval chain exists above the thread | Medium | A courtesy copy, or someone forwarded it for information |
| Whose reply ends a thread | Decision authority | Medium | The last reply is often just the last person with time |
| Declines an invite and sends a delegate | The decliner is the sponsor; the delegate is the operator | Medium | A genuine conflict. Judge the rate over 90 days, never a single instance |
| Reply latency asymmetry — one person's reply resets everyone else's | Deference | Medium | Time zones |
| Title parsing plus public sources | Reporting band | Medium | Titles are not comparable across companies. A "Director" at a 200-person company may outrank a "VP" at a 20,000-person one |
| Shared surname or an identical email pattern | Nothing at all | **None** | Do not infer relationships from names |
| Who is on the `To` line vs `Cc` on our own outbound | Nothing about their org | **None** | That structure is ours, not theirs |

## 3. Thread-position analysis

The highest-yield source, and the one most often left unread. Work over the last 180 days of
`interaction` records where `type = 'email'`.

| Pattern | Reading | Confidence |
| --- | --- | --- |
| Person A adds Person B to a thread, and B was not previously on it | A is escalating to or consulting B. B is senior on this topic | Medium–High |
| B is added only when a decision, a price or a date is required | B is in the approval chain | High |
| A moves from `To` to `Cc` after B joins | A has handed the thread over | Medium |
| A always replies within an hour; after B replies, A stops | Deference to B | Medium |
| A person appears on exactly one thread per quarter, always about paper | Procurement or legal, not a stakeholder | High |
| A person is on every thread and answers none | An observer — often a manager keeping visibility. Real, but not a relationship | Medium |
| A new address on a thread with a domain we have not seen | Either an external adviser, or an acquisition. Check `account.parent_account_id` and the domain's public registration | Medium |

**Two corrections to apply before reading anything.** First, exclude our own internal
participants — an internal thread's shape says nothing about their org. Second, exclude
distribution lists and aliases (`support@`, `billing@`, `no-reply@`); they inflate apparent
breadth and are the commonest source of a fictitious contact.

## 4. Calendar behaviour

| Pattern | Reading | Threshold |
| --- | --- | --- |
| Consistently declines and sends the same delegate | The decliner is the sponsor; the delegate is the operating owner | ≥2 occurrences in 90d |
| Attends only quarterly reviews, never working sessions | Executive sponsor posture | Any |
| Attends everything, organises nothing | Power user or a subject expert | Any |
| Organises and attends everything | Programme owner — the coordination hub, and often the single-threading risk | Any |
| Acceptance rate falling against their own 12-month baseline | Disengagement — see `champion-risk.md` §2.4 | <60% over 90d |
| A new name accepts on the first invite | A successor already installed, or a new hire briefed to take this over | Any |

**Coverage caveat.** Calendar data is usually connected for only some of the account team's
mailboxes. If it is partial, say so in the Coverage Ledger and do not read absence as
disengagement — you may simply be looking at one CSM's calendar.

## 5. Product and support telemetry

| Observable | Reading | Field |
| --- | --- | --- |
| Grants permissions, provisions seats, configures SSO | Admin — technical ownership | `usage_daily.admin_actions` |
| Invites the most users | The internal rollout owner. A champion candidate, and the best route into a second function | `usage_event` where `event_name` is an invite |
| Top-decile `core_actions` within their cohort | Power user | `usage_event.contact_id` |
| Files most tickets | Operator | `ticket.contact_id` grouped over 180d |
| Appears only on P1s and escalations | Gatekeeper or exec sponsor | `ticket.priority`, escalation CC lists |
| Reopens tickets | The person the friction actually lands on. Reopens are worth more than new tickets | `ticket.reopened_count` |
| High usage, zero interactions, never on an email | Either a genuine end user, or a shared service account | Cross-check `is_external_collaborator` and the identity rules in `../../cs-context/references/normalized-schema.md` §3 |

## 6. Seniority bands

Use bands, not titles, and record the evidence for the band. `multithread_height` is the
highest band with a two-way interaction in 180 days.

| Band | Typical titles | Evidence that confirms the band | What it can usually do |
| --- | --- | --- | --- |
| **C-level** | CxO, President, MD | Named in public filings or the company site; chairs an exec forum | Kill or fund anything |
| **VP** | VP, SVP, Head of *(function)* | Owns a budget line; other contacts defer | Fund within their function |
| **Director** | Director, Senior Manager *(large orgs)* | Approves within a threshold; runs the evaluation | Fund small, block anything technical |
| **Manager** | Manager, Team Lead | Owns headcount, not spend | Escalate, not decide |
| **IC** | Analyst, Engineer, Specialist, Coordinator | — | Use, advocate, block operationally |

**Never compare a title across companies without a size adjustment.** Record `employee_count`
from `account` alongside the band; a Director at 200 people and a Director at 50,000 are not
peers, and treating them as such produces a `multithread_height` that reads adequate and is not.

## 7. Composing the structure

Walk this in order. Stop at the first step that resolves each person.

1. **Anchor on what is stated.** Anything the customer told us on a call or in an email is
   `verified`. Start there and never overwrite it with an inference.
2. **Place the paper chain.** Signatory, notices contact, procurement, legal. This is the most
   reliable sub-structure because it is written down in the contract.
3. **Place the operating layer** from product and support telemetry — admins, power users,
   ticket submitters. High confidence, low seniority, and the layer that changes fastest.
4. **Place the decision layer** from thread position and calendar behaviour. Medium confidence,
   and the layer that decides renewals.
5. **Join the layers** with reporting lines: solid where stated, dashed where inferred.
6. **Print what is missing as a role, not as a blank.** "No security reviewer identified" is a
   finding; an empty box is an oversight.
7. **Date every node.** A person with no interaction in 180 days is drawn greyed or marked
   stale, whatever the structure says.

**Conflicts.** When telemetry and titles disagree, telemetry wins for the operating structure
and titles win for nothing. When a stated structure and an inferred one disagree, the stated
one wins and the inference is recorded as falsified — that is a useful event, because it tells
you which of your inference rules is unreliable on this account.

## 8. Confirming it out loud

Three questions that cost one sentence each and repay more than any enrichment feed:

| Ask | Why it works |
| --- | --- |
| "Here's how I understand your side — is that roughly right?" *(share the map, dashed lines and all)* | People correct a diagram far more readily than they answer an open question about hierarchy |
| "When this comes up for renewal in November, who else has to nod?" | Asks about the decision structure, which is the one you need, without asking anyone to describe their org |
| "Is there anyone I should be keeping in the loop who I'm not?" | Surfaces the unmodelled blocker and the security reviewer in one question |

Do this **before** the renewal window, not inside it. Asking who signs six weeks out reads as
a vendor scrambling; asking six months out reads as planning.

## 9. Multi-entity accounts

Subsidiaries, regions and post-acquisition groups break every account-level metric quietly.

| Case | What breaks | Treatment |
| --- | --- | --- |
| Subsidiaries with separate contracts | Roll-up counts group contacts as coverage for an entity that has none | Map **per contract-holding entity**. Set `parent_account_id` and state the reporting grain in the header |
| One contract, several operating entities | Depth looks healthy; the entity that will actually cancel has depth 1 | Report depth per entity and take the minimum as the account's structural read |
| Post-acquisition, acquirer's stack in play | The acquired champion's influence is at its lowest immediately after close | Map the **acquirer's** buying centre within 30 days. Selling to the acquired entity's champion is selling to the losing side of a consolidation |
| Shared services or a group procurement function | The real economic buyer sits outside the entity we serve | Add the group function explicitly, with `function = procurement`, even if we have never met them |
| Regional entities with local budget | A group-level exec sponsor is not coverage for a regional renewal | Coverage is scored per entity. Never count a group exec twice |
| Multi-domain enterprise (`acme.com`, `acme.co.uk`) | One account splits into several, understating ARR and depth | Maintain `account.domains[]`; see `../../cs-context/references/normalized-schema.md` §3 |

**The multi-entity coverage rule:** an account's coverage score is the **minimum** across the
entities that can independently choose not to renew, not the average and not the maximum.
Averaging hides exactly the entity that leaves.

## 10. Identity resolution traps

These corrupt a stakeholder map before any inference is made. Check them first.

| Trap | Effect on the map | Handling |
| --- | --- | --- |
| Free-email addresses at a paying account | Real contacts dropped; depth understated | Explicit contact mapping; never domain-match free providers |
| Aliases and distribution lists | Fictitious contacts; depth overstated | Exclude anything matching `support@`, `billing@`, `info@`, `no-reply@` |
| Agencies and consultants using the product for the client | Attributes influence to someone with none | Flag `is_external_collaborator`; they are stakeholders, but not of this org |
| Shared or service accounts | One "user" hides ten humans, or one human looks like ten | Flag and exclude from per-person scoring |
| Post-acquisition domain change | Every contact appears to depart at once | Check for a domain migration before asserting any departure |
| Employees of ours testing in production | Inflates apparent internal coverage | `is_internal` exclusion rule, documented |
| Duplicate contact records | Splits one person's history in half, understating depth and recency | De-duplicate on email before scoring; record the join rate |

**Record the join rate.** Below 90%, note it. Below 80%, every relationship metric derived
from product telemetry is Low confidence — the unmatched users are not randomly distributed,
and they cluster in exactly the teams you have not met.

## 11. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Drawing an inferred reporting line as solid | Dashed line, "understood to report to", listed in the Inferences table with a falsifier |
| Inferring authority from a job title | Titles set the band; behaviour sets the authority |
| Comparing titles across companies without size context | Record `employee_count` next to the band |
| Counting a distribution list as a contact | Exclude aliases before computing depth |
| Treating a single declined invite as delegation | Judge the rate over 90 days |
| Reading absence from a partially connected calendar as disengagement | State the coverage gap; absence of data is not data |
| Averaging coverage across entities | Take the minimum across entities that can independently not renew |
| Selling to the acquired entity's champion after a takeover | Map the acquirer's buying centre inside 30 days |
| Asking who signs six weeks before the renewal | Ask six months out, as planning |
| Overwriting a stated structure with an inferred one | Stated wins; record the inference as falsified and learn from it |
