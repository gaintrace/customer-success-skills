# The Productisation Path

> Generality is the dimension most often asserted and least often evidenced. This file makes the
> claim carry weight: six evidence tiers, a four-source search that prints its negatives, the
> counting rules that stop one customer being reported as a market, the field-signal request
> product can act on, and the Graduation Contract without which **"we'll productise it later"**
> is a feeling booked to nobody.
>
> The whole path exists to answer one question with a number instead of an opinion: *how many
> named accounts, at what evidence tier, want this same job?*
>
> Evidence labels: `[M]` measured · `[V]` vendor research · `[P]` practitioner standard ·
> `[A]` academic, standards body or regulation · `[D]` primary document.

**Contents**
- [1. The evidence tiers](#1-the-evidence-tiers)
- [2. The search](#2-the-search)
- [3. Counting rules](#3-counting-rules)
- [4. Designing the general shape](#4-designing-the-general-shape)
- [5. The field-signal request](#5-the-field-signal-request)
- [6. The Graduation Contract](#6-the-graduation-contract)
- [7. When product declines](#7-when-product-declines)
- [8. Proving the generalisation worked](#8-proving-the-generalisation-worked)
- [9. Anti-patterns](#9-anti-patterns)

---

## 1. The evidence tiers

Count **accounts, named, with ARR and renewal date**. "Several customers" is a countable thing
left uncounted, and it is the single most common sentence in a memo that later turns out to have
served one account.

| Tier | What it is | Weight | Sourced from | Falsifier |
| --- | --- | --- | --- | --- |
| **G0** | Someone internal believes others would want it | **0.00** | An opinion in a Slack thread | — never counted |
| **G1** | An account mentioned it once, verbally, no record | **0.25** | Call notes, transcript | The speaker cannot restate the job when asked |
| **G2** | An account asked in writing, use case unstated | **0.50** | Email, ticket, portal request | The written ask names only a mechanism |
| **G3** | An account asked in writing **with the job stated**, matching the Step 1 reduction | **1.00** | Ticket or portal record carrying the use case | The stated job differs from ours once reduced (§3) |
| **G4** | An account already runs a workaround in production, or has paid for the same outcome | **1.50** | Usage telemetry, a prior SOW, an invoice | The workaround serves a different outcome |
| **G5** | An account made it a written purchase or renewal condition | **2.00** | Opportunity record, redline, MSA amendment | The condition was withdrawn or never signed |

`N_evidenced = Σ weights`. **Gate 3 requires `N_evidenced ≥ K*` *and* ≥2 accounts at G3 or above.**
A single G5 is a large customer, not a market — four G1s sum to 1.0 and represent nothing that has
been written down anywhere.

**Why the tiers are weighted this way.** G4 outranks G3 because a workaround running in production
is a revealed preference: somebody is paying a person's time every week rather than waiting.
That is the strongest non-commercial evidence available, and it is invisible to any process that
counts only what was asked for. **Ask about the last time, never about "generally"** (`C1`) — "walk
me through what your team did at the last month-end" produces G4 evidence; "would you find this
useful?" produces G0 and a false yes, because nobody refuses a hypothetical feature.

**Tier decay.** A G3 request older than 12 months is re-tiered to G2 unless the account confirms
it still matters; a G5 condition on an expired contract is re-tiered to G3. Requests age out of
relevance faster than the register that holds them, and staleness that flatters the count is the
one direction of error nobody notices (`../../cs-context/references/evidence-standard.md` §7).

---

## 2. The search

**Search before you assert, and print the negatives.** "Searched the request portal 2026-08-27
with `close-out export` and `supplier code`; three accounts matched, two at G3" is evidence.
"I think a few others want it" is not, and it never survives the first challenge in a product
review. Walk all four sources every time — a search that stops at the first hit finds the accounts
that were easiest to find, which is the accounts that complain most.

| # | Source | What to query | What it yields | The negative to print |
| --- | --- | --- | --- | --- |
| 1 | **Request portal / Jira** | `type = feature_request` with a linked `account_id`, plus 3–5 job synonyms, not the artefact name | G2 and G3 | "Portal searched `<terms>` on `<date>`; `<n>` matches, `<k>` linked to an account" |
| 2 | **Ticket queue** | Tickets describing the *job*, including ones closed as "working as designed" | G2, G3, and the real volume | "`<n>` tickets across `<k>` accounts in 12 months; `<m>` closed without a fix" |
| 3 | **Product telemetry** | Accounts running a manual equivalent: exports followed by re-upload, an integration user doing the step, a scheduled job at the same hour | **G4 — the tier nobody searches** | "Telemetry checked for `<pattern>`; `<n>` accounts show it" |
| 4 | **Closed-lost and renewal notes** | Loss reasons, redlines, renewal conditions, security or procurement blockers | G5, and the ARR the gap has already cost | "`<n>` closed-lost records mention it; `<k>` renewals carried it as a condition" |

**Two more sources when the model calls for them.** In a regulated vertical, search the compliance
requirements register before anything else — residency, retention, audit-export and access-review
requirements are almost always *general*, sitting unasked in every regulated account because each
one assumes it is the only one that needs them. In a channel model, search the partner's own
request log; a partner-delivered account files its requests with the partner, not with us.

**Never ask a colleague a question the systems answer** (`C6`). Canvassing the team is the last
step, not the first, and its output is G0 unless it produces a record you can link. The question
that turns G0 into something countable is *"which account, and where is it written down?"*

### Recording the search

Every generality claim carries this block, in the memo, above the evidence table:

```
Searched 2026-08-27 · request portal (REQ, terms: "close-out export", "supplier code",
"code translation") · Zendesk (12 months, same terms) · telemetry (export-then-reupload
pattern, 90 days) · closed-lost + renewal notes (8 quarters).
Found: 4 accounts. Not found: no closed-lost record mentions it; no partner-log access.
Coverage: 3.5 / 4 sources → N_evidenced is a floor, not a ceiling.
```

**A partial search caps confidence, it does not stop the memo** (`R23`). State which source was
unavailable and which direction the gap biases: a missing telemetry search hides G4 accounts, and
G4 is the tier that most often turns a Decline into a Generalise.

---

## 3. Counting rules

The reduction from `decision-rubric.md` §1 is what stops this becoming a wrong Generalise. Two
accounts asking for "a custom dashboard" usually want different things; two asking for "the same
reconciliation file in the drop at 06:00" want one thing.

| Rule | Ruling | Why |
| --- | --- | --- |
| Same artefact, different job | Count **one** — the one whose job matches ours | The abstraction that serves both is two features wearing one name |
| Same job, different artefact | Count **both**, at their own tiers | The job is the unit. Their mechanism preferences are inherited from other vendors |
| Two contacts at one account | Count **one account**, at the highest tier either reached | The unit is the account, because the ARR is |
| A parent and its subsidiaries on separate contracts | Count separately **only** where each has its own renewal date and its own budget holder | Otherwise one buying decision is being reported as two |
| An account that churned | Count at half weight, and say so | The need was real; the willingness to pay is unproven |
| A prospect in an open opportunity | Count at G2 maximum until it is a written condition | A deal that has not closed is a hypothesis about a market |
| Our own internal use | Count **zero** | It is not a customer, and it is the easiest evidence to reach for |
| An account already on the workaround and content | Count at G4, and record that they are content | It raises `N_evidenced` and lowers the urgency. Both are true |

**Do not ARR-weight `N_evidenced`.** Weighting by revenue converts the generality test into the
payback test and destroys the distinction the gate sequence exists to make: **generality is the
product argument, ARR is the services argument, and they answer different questions.** Report ARR
in a separate column, where a reader can see the concentration for themselves.

**Bracket the count.** `N_evidenced` from a complete four-source search is a point estimate;
from a partial search it is a floor. Print it as `4.0 (floor — telemetry not searched)` rather
than as a bare number, and give the count a falsifier: *"a fifth account at G3 would raise this
to 5.0 and Gate 3 fires regardless of `K*`."*

---

## 4. Designing the general shape

Generalising is not "the same code with an `if` in it". The general version is defined by three
properties, and a design missing any one of them is a bespoke build with a wider blast radius.

| Property | Test | Failure mode |
| --- | --- | --- |
| **A documented extension point** | A second account deploys it **without a fork** and without a change to shared code | Every deployment edits the core; `upgrade_tax_h` rises with each account |
| **Configuration, not branching** | New account behaviour is a config value, not a code path | A parameter per caller until nobody can change it safely |
| **An owner in delivery, named** | One person is paged and answers a schema change | Shared ownership, which is no ownership under load |

**Duplication is far cheaper than the wrong abstraction** `[P · Metz, "The Wrong Abstraction",
20 Jan 2016]`. An abstraction extracted from one instance accumulates a parameter per new caller
until every change requires understanding all of them, and that cost surfaces two years later in
`maintenance_h`, where nobody connects it back to the decision that caused it. Fowler's rule of
three is the counterweight: the third instance is where the common shape becomes visible `[P]`.
The practical rule is to **build the second one bespoke, then extract from two working
instances** — unless `K* = 1`, where the general version is already cheaper than one bespoke build
(`carrying-cost.md` §5).

**Review the abstraction after the second deployment, on a dated commitment.** If it needed a
change to shared code to land the second account, the extension point is not one, and the
component goes back into the debt register as bespoke work with a wider surface.

**What generality is worth, in margin.** TSIA reports productised services achieving roughly
**10–15% higher gross margin than custom engagements** `[V · TSIA]`, against a Cloud 40 baseline
where project services average **−9%** (published 2023 on Q3-2022 data) `[V]`. That gap is the
entire commercial case for this file.

---

## 5. The field-signal request

The deliverable is not "we told product about it". A conversation in a hallway leaves nothing that
survives a reorg (`C30`). The deliverable is a written request a product manager can act on
without re-doing the discovery.

| Section | Required content | Invalid |
| --- | --- | --- |
| **The job** | One line, no mechanism named, from the Step 1 reduction | The artefact the first customer asked for |
| **The customers' words** | Verbatim quotes, each with speaker, title, date and source | A paraphrase — a quote is the customer's own framing and it survives the retelling (`C5`) |
| **Who hits it** | Every account: name, ARR, renewal date, tier, what they asked for | "Several enterprise customers" |
| **`N_evidenced` and the search** | The sum, the tier breakdown, the four sources with dates, and the negatives | A count with no method |
| **What we have built or will build** | Principal, annual carrying, interest rate, `K*` — from `carrying-cost.md` | The build estimate alone |
| **The general shape** | The abstraction that serves all of them, with the extension point named | This customer's version, generalised in prose |
| **What it unblocks** | The ARR that stops being contingent on a bespoke path, and the accounts it belongs to | A total with no accounts behind it |
| **The decision we need, and by when** | A **decision date**, tied to the earliest opt-out deadline in the evidence table | A ship date, or "as soon as possible" |
| **What we do if you decline** | The fallback with its carrying cost, written now | "We'll figure it out" |

**Ask for a decision, never for a place on the roadmap.** A decision date is something a PM can
give you this quarter; a roadmap slot is something they cannot give you at all, and asking for one
converts a specific request into an open-ended obligation. The request is fully answered by
"no, and here is why" — that answer lets you price the fallback and write the customer note today.

**The date belongs to the PM who agreed it** (`R19`). Nothing from this document reaches the
customer as a date until a named owner has agreed it in writing, and even then what the customer
hears is *when we will tell them the decision*, not what the decision will be.

---

## 6. The Graduation Contract

Every **Generalise** and every **Build bespoke** carries five fields. **A missing field means the
work is not approved, whatever the meeting concluded.** This is the mechanism that makes "we'll
productise it later" mean something: without an owner and a date it books the cost to nobody, and
the person who inherits the component in eighteen months has no one to ask.

| Field | Requirement | Worked example |
| --- | --- | --- |
| **Owner** | A named person. They are paged when it breaks and they answer schema changes | Jo Nkemdirim, Delivery Engineering |
| **Sunset review date** | A calendar date set at creation, ≤12 months out | 2027-06-30 |
| **Graduation trigger** | The observable event that makes this a product requirement. Default: a third account at G3+ | "A third account reaches G3, or `N_evidenced` ≥ 5.0" |
| **Product counterpart** | The named PM or engineering owner who has read the §5 request, and the date they decide by — a decision date, not a ship date | Ana Ruiz, PM Integrations — decides by 2026-10-15 |
| **Fallback if product declines** | What we do then, with its carrying cost, written now | "Own it in delivery: $28k/yr carrying, 46% interest, re-decided at the 2027-06-30 cull" |

Two further fields travel with it into the register (`carrying-cost.md` §7): the **hours ceiling**
(`R21`) after which the next increment is a change order rather than maintenance, and the
**decision record** — gate, `N_evidenced`, `K*`, the nine rubric scores and the falsifier — so the
decision is not re-litigated from memory by someone who was not there.

**One outcome per request** (`R17`). "Build it, *and* work around it, *and* raise it with product"
is three half-executions and no owner. The gate sequence returns one word; the field-signal request
is part of the disposition for **Generalise**, **Work around** and **Decline** alike, not a fourth
outcome that softens the other three.

---

## 7. When product declines

A declined request is a normal outcome and a useful one — it converts an open question into a
priced decision. What it must not do is disappear.

| Step | Action | Owner | Timing |
| --- | --- | --- | --- |
| 1 | Get the decline **in writing**, with the reason and a revisit condition (`R14`) | The PM | At the decision date |
| 2 | Re-run the gate sequence with roadmap collision now scored 4 | You | Same week |
| 3 | Price the fallback: own it in delivery, migrate to the nearest supported path, or decline to the customer | You | Same week |
| 4 | Update the register row: new disposition, new sunset review date, drift raised if the component now has no product path | You | Same week |
| 5 | Tell the customer the decision, without the internal reasoning (`R18`) and without a date nobody owns (`R19`) | You | Within 5 working days of the decision date you promised them |

**The revisit condition is the whole value of the written decline.** "Not now — revisit when a
third enterprise account makes it a renewal condition" is a decision with a trigger; "not on the
roadmap" is an ending, and it guarantees the same request arrives again next quarter with nobody
able to say what changed.

**Escalate the decline exactly once, on evidence, not on volume.** The escalation is the §5
document plus the ARR that has become contingent since it was written. Re-raising the same request
with the same evidence in a louder voice costs credibility that the next request will need.

---

## 8. Proving the generalisation worked

Generalisation is justified on a prediction, so it gets measured like one. Without this step every
"we generalised it" claim is unfalsifiable, and the register fills with shared components that
serve one account.

| Measure | Target | When | If missed |
| --- | --- | --- | --- |
| **Second deployment without a fork** | Zero changes to shared code | At the second account | The extension point is not one. Re-register as bespoke, raise drift to 0.25 |
| **Deploy hours per account** | Within 1.5× the `deploy_hours_per_account` used to compute `K*` | Each deployment | Recompute `K*`. Above 2×, generalising has stopped paying back |
| **Actual vs estimated carrying** | Within 1.5× the estimate | At the first cull | Record the ratio — it is the only calibration the next estimate gets |
| **Accounts served** | ≥ `K*` within 12 months | At the sunset review | Below `K*`, this is a bespoke build with extra abstraction. Migrate or retire |
| **Graduation** | The trigger fired and product decided | At the trigger | Chase the decision date once, in writing, then re-price the fallback |

**The economics of not measuring this are well documented at the industry level.** Pendo's *2019
Feature Adoption Report* found **80% of features rarely or never used**, with about **12% of
features generating 80% of daily usage volume**, and estimated public cloud companies spent
roughly **$29.5bn** on features that may rarely or never be used `[V · Pendo, 2019]`. The Standish
Group's earlier figure — **45% of features never used and 19% rarely**, 64% combined — came from a
keynote on four internal applications and is directional rather than measured `[V · Jim Johnson,
XP2002]`. Both point one way: shipping the general version is not the same as it being used, and
the account count at the sunset review is the only evidence that settles it.

---

## 9. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| "I'm sure other customers want this" | Named accounts, ARR, renewal date and a tier, or `N_evidenced = 0`. The sentence is G0 in every case |
| Generalising from one large account | ≥2 accounts at G3+ before Gate 3 fires. One instance produces the wrong abstraction `[P · Metz]` |
| Counting the artefact rather than the job | Reduce first (`decision-rubric.md` §1). Two "custom dashboards" are usually two jobs |
| A search that stops at the request portal | All four sources, with dates and negatives printed. Telemetry is the one that hides G4 accounts |
| ARR-weighting `N_evidenced` | Generality is the product argument; ARR is the services argument. Report ARR in its own column |
| "We'll productise it later" | The five-field Graduation Contract, with a person, a decision date and a written fallback — or the sentence does not count |
| A product counterpart who is "product" | A named PM who has read the request and agreed a decision date. `R19` binds the date to them |
| Asking product for a roadmap slot | Ask for a decision by a date. "No, because X" is a complete and useful answer |
| A shared component nobody deployed twice | Measure it at the sunset review (§8). Below `K*` accounts it is a bespoke build with extra abstraction |
| Telling the customer their request is "being productised" | `R18` and `R19`. They hear when we will tell them the decision, never the internal disposition |
