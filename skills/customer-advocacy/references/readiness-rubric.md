# Advocacy Readiness Rubric

> How to score a customer's readiness to advocate from **behaviour**, and the disqualifiers that
> no score overcomes. Field names are from `../../cs-context/references/normalized-schema.md`;
> evidence labels follow `../../cs-context/references/evidence-standard.md`
> (`[M]` measured · `[V]` vendor · `[P]` practitioner · `[A]` authoritative/regulatory).
>
> The single idea this file exists to enforce: **a survey score is a disposition, not a
> readiness.** Disposition is one family of seven, and it is the one that decays fastest.

**Contents**
[How to score](#how-to-score) · [Family 1 — Product usage](#family-1--product-usage--adoption) ·
[Family 2 — Commercial](#family-2--commercial--contract) ·
[Family 3 — Relationship](#family-3--relationship--engagement) ·
[Family 4 — Support](#family-4--support--reliability) ·
[Family 5 — Sentiment](#family-5--sentiment--voc) ·
[Family 6 — Billing](#family-6--billing--payment) ·
[Family 7 — Firmographic](#family-7--firmographic--external) ·
[Weight profiles](#weight-profiles) · [The disqualifier register](#the-disqualifier-register) ·
[The champion standing test](#the-champion-standing-test) ·
[The quantified outcome test](#the-quantified-outcome-test) ·
[Worked example](#worked-example) · [False positives](#false-positives-check-before-shortlisting)

---

## How to score

Each family is scored **0–100 readiness** (higher = better), then combined:

```
Readiness = Σ (family_score × weight) / Σ (weights of families with data)
```

Renormalise over the families that have data. A missing family is **not** scored zero — that
manufactures a false negative and quietly shrinks the pool. Print the renormalisation.

| Rule | Why |
| --- | --- |
| Score the **person**, then the account, then take the lower | You are asking a human, not a logo. An account at 88 with a six-week-old champion is not an 88 |
| Anything unmeasurable is `UNKNOWN — requires <source>`, never a mid-range guess | A guessed 50 in the relationship family is the difference between rung 3 and rung 8 |
| Recency beats magnitude in families 3 and 5 | A 10 given eight months ago by someone still in role is weaker evidence than a 7 given last month |
| Confidence never exceeds coverage (`R23`) | Four of seven families is a 57% read, whatever the number says |

**Score bands.** 80–100 Ready · 60–79 Ready with limits (rungs 1–5) · 40–59 Not yet (rungs 1–2) ·
0–39 Not a candidate. Bands are an **ordering**, not a probability that they say yes (`R22`).

---

## Family 1 — Product usage & adoption

**Weight 20 (enterprise).** Answers: *are they still doing the thing they would vouch for?*

| Score | Condition | Fields |
| --- | --- | --- |
| 90–100 | Core-action volume in the top tercile of their segment, 8-week normalised slope ≥ 0, breadth ≥ 60% of features in plan, and the use case they would describe is the one still running | `usage_daily.core_actions`, `feature_breadth` |
| 70–89 | Stable core usage, breadth 40–60%, no decline over 8 weeks | `usage_daily` |
| 50–69 | Flat or mildly declining; one of the two use cases in the original business case has lapsed | `usage_daily`, success plan |
| 25–49 | Core-action volume down ≥30% over 8 weeks, or breadth <25% | `usage_daily.core_actions` |
| 0–24 | Zero core actions for 30 days, or the referenced use case has been switched off | `usage_daily`, `usage_event` |

**The check that matters:** score usage **of the workflow the reference would describe**, not the
account aggregate. A customer whose Finance team is thriving cannot speak credibly about the
RevOps use case a prospect asked about. Segment by department before scoring.

**Consumption businesses:** replace this table with commitment pacing —
`usage_consumed / (usage_entitlement × elapsed_term_fraction)`. Above 0.9 scores 90+; below 0.7 at
the halfway mark scores under 40 regardless of raw volume. Separate recurring from episodic
consumption: a one-off backfill is not a story.

---

## Family 2 — Commercial & contract

**Weight 15.** Answers: *have they renewed, and does the paper permit publicity?*

| Score | Condition | Fields |
| --- | --- | --- |
| 90–100 | ≥1 renewal completed, term ≥12 months remaining or auto-renew on, no publicity restriction, expansion taken at some point | `subscription.*`, `opportunity` |
| 70–89 | ≥1 renewal completed, clean contract, no expansion history | `subscription` |
| 40–69 | First term, past the activation event, no renewal yet | `subscription.start_date` |
| 10–39 | Inside 90 days of `opt_out_deadline` with the renewal unresolved, or a discount expiring into a contested renewal | `subscription.opt_out_deadline`, `discount_expires` |
| 0–9 | Auto-renew off, notice served, or termination language requested | `subscription.auto_renew_changed_at` |

**Never trust a CRM checkbox for the publicity clause.** Read the executed MSA or order form. The
three clauses that matter: a **no-publicity / no-marketing-use** clause, a **logo-use** clause
(often permissive but time-bounded to the term), and a **mutual-NDA** scope broad enough to cover
the existence of the relationship — common in financial services and defence.

**A first-term customer can give rungs 1–4.** They cannot credibly give rung 8: a prospect's first
question is "how has it held up?", and eleven months is not an answer.

---

## Family 3 — Relationship & engagement

**Weight 22 — the highest, because advocacy is a person.**

| Score | Condition | Fields |
| --- | --- | --- |
| 90–100 | Champion ≥18 months in role, ≥1 observed internal advocacy event in 180 days, exec sponsor engaged, ≥3 engaged contacts | `contact.role`, `interaction.customer_participants` |
| 70–89 | Champion ≥180 days in role, ≥2 engaged contacts, exec sponsor known | `contact`, `interaction` |
| 40–69 | Champion in role 90–180 days, or single-threaded on a healthy relationship (`R5`) | `interaction` 90d distinct contacts |
| 10–39 | Champion <90 days in role, or the previous champion departed inside 90 days | `contact.departed_at` |
| 0–9 | Hard bounce or directory removal on the only engaged contact | `contact.email_status` |

**"Engaged" means a two-way interaction inside 90 days** — they replied or attended. A name in the
CRM is not a relationship, and a webinar registration is not engagement.

**Internal advocacy event** is the evidence that upgrades a coach to a champion: they ran a
meeting we were not in, they brought a colleague to us unprompted, they defended the line item in
front of their own finance team, or they wrote the internal justification. `[P]` MEDDICC's own
champion test — a contact who will not introduce you to the economic buyer is a coach.

---

## Family 4 — Support & reliability

**Weight 15.** Answers: *would the last 90 days come up on the call, unprompted?*

| Score | Condition | Fields |
| --- | --- | --- |
| 90–100 | No P1 in 180 days, reopen rate <5%, no SLA breach in 90 days, CSAT ≥4.5 on substantive tickets | `ticket.priority`, `reopened_count`, `sla_breached`, `satisfaction` |
| 70–89 | No P1 in 90 days, reopen rate <10%, ticket volume at or below their segment median per 100 seats | `ticket` |
| 40–69 | One P1 closed 30–90 days ago with documented root cause and no recurrence | `ticket` |
| 10–39 | P1 closed inside 30 days, or ≥3 reopens on one root cause in 90 days | `ticket.reopened_count` |
| 0 | Any open P1/Sev-1 or live escalation — **disqualifying, not scoring** | `ticket.status`, `type='escalation'` |

**Zero tickets is not a 100.** Check whether they stopped reporting rather than stopped having
problems: zero tickets alongside declining usage is the *Quiet quit* pattern in `churn-risk`, and
routing that customer into a reference call is how you find out.

---

## Family 5 — Sentiment & VoC

**Weight 13 — deliberately low.** It is the family most people score first and it is the weakest.

| Score | Condition | Fields |
| --- | --- | --- |
| 90–100 | Promoter (9–10) inside 90 days **from a contact still in role with standing**, plus a positive verbatim in their own words | survey source, `contact.role` |
| 70–89 | Promoter or CSAT ≥4.5 inside 90 days from a live contact | survey source |
| 40–69 | Positive sentiment inside 180 days, or positive call-transcript sentiment with no survey | transcripts |
| 10–39 | Sentiment older than 180 days, or from a departed contact | `contact.departed_at` |
| 0–9 | Any detractor response (0–6) inside 180 days, or a negative verbatim not yet resolved | survey source |

**Three decay rules.** A survey score older than **90 days** is a historical fact, not a signal
(`evidence-standard.md` §7). A score belongs to a **person**, not an account — if they left, the
score left. And a single respondent is not a sentiment read; state the sample size when scoring.

---

## Family 6 — Billing & payment

**Weight 5 — small, but it holds a disqualifier.**

| Score | Condition | Fields |
| --- | --- | --- |
| 90–100 | Zero late payments in 12 months, valid payment method, no disputes | `invoice.paid_at`, `payment_method_status` |
| 60–89 | Mean days-late under 15, no dispute | `invoice.paid_at − due_at` |
| 20–59 | Mean days-late 15–45, or one resolved dispute in 12 months | `invoice` |
| 0 | Invoice >60 days overdue, credit hold, or an open dispute — **disqualifying** | `invoice.status` |

A customer arguing with your finance team is not going to praise you to a prospect, and asking
them to is how the argument becomes a relationship problem.

---

## Family 7 — Firmographic & external

**Weight 10.** Answers: *does their organisation permit this, and is now their moment?*

| Score | Condition | Source |
| --- | --- | --- |
| 90–100 | Private company or a public one outside a quiet period · no vendor-mention policy · a named comms contact who has approved something before | Contract, prior approvals, IR calendar |
| 70–89 | Approvable with a known chain and a lead time we have measured | Prior approvals |
| 40–69 | Regulated vertical, policy unknown, no prior approval on record | Enrichment |
| 10–39 | In an earnings quiet period, mid-acquisition, or announced layoffs inside 90 days | News monitoring |
| 0 | Written no-publicity policy, or the prospect is a direct competitor | Contract, prospect record |

**Ask for the policy before you ask for the story.** In regulated verticals the question "does
your comms team have a vendor-mention policy, and can you send it to me?" saves six weeks and
costs the customer ninety seconds.

---

## Weight profiles

| Family | Enterprise (default) | Product-led | Consumption |
| --- | --- | --- | --- |
| Product usage & adoption | 20 | 30 | 28 |
| Commercial & contract | 15 | 12 | 17 |
| Relationship & engagement | 22 | 8 | 18 |
| Support & reliability | 15 | 15 | 15 |
| Sentiment & VoC | 13 | 22 | 10 |
| Billing & payment | 5 | 8 | 5 |
| Firmographic & external | 10 | 5 | 7 |

**Product-led:** there is frequently no champion and no exec sponsor, so scoring their absence
manufactures a false negative. Usage and sentiment carry the score, and the ladder is capped at
rung 3 until a named human has been recruited out of the base.

**Consumption:** relationship stays material because commitment renegotiation is an executive
conversation, but seat and licence framing is meaningless here.

---

## The disqualifier register

Hard gates. Print each one that fires with its evidence and its clearing date (`R14`).

| # | Disqualifier | Detection | Ceiling | Clearing test |
| --- | --- | --- | --- | --- |
| D1 | Risk band At Risk or worse | `churn-risk` band | **None** | Watch or better, sustained 30 days |
| D2 | Open P1/Sev-1 or live escalation | `ticket.status`, `type='escalation'` | Rung 1 | Closed + 30 days, root cause documented |
| D3 | Invoice >60d overdue, credit hold, open dispute | `invoice.status` | **None** | Cleared or resolved |
| D4 | Inside `opt_out_deadline`, renewal unresolved | `subscription.opt_out_deadline` | Rung 2 | Signed + 14 days |
| D5 | Champion <180 days in role | `contact.created_at`, title history | Rung 3 | 180 days + one internal advocacy event |
| D6 | Champion departure inside 90 days | `contact.email_status`, `departed_at` | Rung 3 | Successor engaged 90 days |
| D7 | No quantified outcome the customer stated | Success plan, QBR record | Rung 3 | An outcome in their own numbers |
| D8 | No-publicity / no-logo / blanket-NDA clause | Executed MSA | Rung 8 (private only) | Written legal exception |
| D9 | Earnings quiet period or pre-announcement blackout | IR calendar, their comms team | Defer all dated asks | The window they name |
| D10 | Prospect is a direct competitor of the customer | Prospect record vs their market | **Never** | Never — find another cell |
| D11 | Pool cap reached this period | Register | Rotate | Next-eligible date |
| D12 | Declined inside 90 days | Register | **No re-ask** | 90 days, after diagnosis |
| D13 | Two declines inside 12 months (`R21`) | Register | **Out of pool** | Two quarters + a repair conversation with no ask in it |
| D14 | Onboarding incomplete / activation event not reached | `cs-context` §5 | Rung 1 | Activation reached + 60 days |
| D15 | An overdue commitment we owe them | Commitment log | **None** | Delivered, then 14 days |

**D15 is the one teams skip.** Asking a customer for a favour while a promise to them is overdue
converts a small failure into a character judgement. Check the commitment log before the shortlist.

---

## The champion standing test

Four questions. Two noes cap the candidate at rung 3, whatever the score says.

| Test | Evidence that satisfies it |
| --- | --- |
| **Tenure** — ≥180 days in this role at this company | Contact created date, title history, their own LinkedIn |
| **Standing** — would their own exec take their recommendation? | They have been cited by the exec, they chair the internal forum, or they hold the budget line |
| **Advocacy already observed** — have they sold internally without us? | A meeting they ran, a colleague they brought, a justification they wrote |
| **Durability** — is anyone behind them? | ≥2 engaged contacts, so the ask does not create a single point of failure |

A candidate who passes tenure and fails standing is a **power user**, not a champion. They give
excellent product testimonials (rung 2–3) and poor executive references (rung 8), because the
prospect's buyer asks a budget question they have never had to answer.

---

## The quantified outcome test

Nothing above rung 3 ships without one. Four conditions, all required:

| Condition | Failing version | Passing version |
| --- | --- | --- |
| **Theirs, not ours** | "Users grew 40% in our platform" | "We closed Q3 in four days against eleven in April" |
| **Measured in their system** | Our product analytics | Their close calendar, their ticket queue, their P&L |
| **Stated by them, on the record** | We inferred it from usage | They said it in a QBR, an email, or a survey verbatim — quote it with the date |
| **Publishable at the precision given** | An exact revenue figure a public company cannot disclose | A percentage, a ratio, or a time saving |

If only three of four hold, the ceiling is rung 3 and the gap is named in the artifact:
`UNKNOWN — requires a customer-stated outcome; the 43% figure is ours, from product analytics`.

---

## Worked example

**Meridian Freight · ARR $310k · enterprise profile · as-of 2026-08-27**

| Family | Score | Weight | Contribution | Evidence |
| --- | --- | --- | --- | --- |
| Product usage & adoption | 85 | 20 | 17.0 | Core actions +12% over 8 weeks, breadth 58% `[Amplitude · core_actions · through 2026-08-25]` |
| Commercial & contract | 90 | 15 | 13.5 | Two renewals; auto-renew on; MSA §14 permits logo and case study `[executed MSA 2024-03-11]` |
| Relationship & engagement | 78 | 22 | 17.2 | Champion 22 months in role; ran the internal rollout review on 2026-06-04 without us; 4 engaged contacts `[interaction · 90d]` |
| Support & reliability | 62 | 15 | 9.3 | One P1 closed 2026-07-02, 56 days ago, root cause documented, no recurrence `[Zendesk · #51102]` |
| Sentiment & VoC | 88 | 13 | 11.4 | NPS 9 on 2026-07-18 from the champion, still in role `[survey · through 2026-08-01]` |
| Billing & payment | 100 | 5 | 5.0 | Zero late payments in 24 months `[Stripe]` |
| Firmographic & external | 55 | 10 | 5.5 | Private company; comms policy UNKNOWN — requires their comms contact |
| **Weighted (7/7)** | | **100** | **78.9** | |

**Readiness 79 → Ready with limits (rungs 1–5).** Disqualifiers checked: D2 does not fire (P1
closed 56 days ago, past the 30-day gate). D7 satisfied — dock-to-stock time stated by their ops
director in the Q2 review. **Ceiling: rung 5.** Not rung 8 — the firmographic gap means the comms
policy is unknown, and a private reference call is the one rung that does not need it. Ask for the
policy in the same message; if it comes back clean, rung 5 opens in the same quarter.

---

## False positives — check before shortlisting

| Trap | What it looks like | The check |
| --- | --- | --- |
| **The orphan promoter** | A 10 from someone who left in May | Match every survey response to `contact.is_active` and `departed_at` |
| **The aggregate mirage** | Account usage healthy, the referenced use case dead | Segment usage by the workflow the reference would describe |
| **Silent support** | Zero tickets read as zero friction | Cross-check against usage decline and the last unresolved cluster |
| **The enthusiastic admin** | Delighted, daily user, no budget context | Standing test — can they answer a buyer's cost question? |
| **The stale clearance** | Legal approved a case study in 2024 | Approvals expire with the contract term and with their comms lead |
| **The single-thread advocate** | One person carries the score and the relationship | `R5` — the ask itself increases concentration risk |
| **The reciprocal trap** | They agreed because we just gave them a credit | Any ask inside 14 days of a concession is contaminated (`R11`) |
| **The reference who is now a prospect's competitor** | Fine last quarter, hostile this one | Re-check the prospect's market at routing time, not at shortlist time |
