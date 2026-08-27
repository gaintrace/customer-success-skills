# SMART Goals for a Business Review

> Read this when writing Part C — the next-period goals. A goal without a customer-side
> owner and a measurement source is a wish that both sides will remember differently in
> ninety days.

**Contents**
1. [The nine required fields](#1-the-nine-required-fields)
2. [Twelve weak → SMART rewrites](#2-twelve-weak--smart-rewrites)
3. [Goal patterns by signal family](#3-goal-patterns-by-signal-family)
4. [Dependencies and the resourcing conversation](#4-dependencies-and-the-resourcing-conversation)
5. [How many, and how to choose](#5-how-many-and-how-to-choose)
6. [Reviewing goals at the next QBR](#6-reviewing-goals-at-the-next-qbr)
7. [Failure modes](#7-failure-modes)

---

## 1. The nine required fields

SMART is Doran's, and the original **A was Assignable** — "who will do it" was in the
acronym before "achievable" replaced it (G.T. Doran, *Management Review* 70(11), 1981,
pp. 35–36). Put it back. Every goal carries all nine:

| Field | Rule | Failure if missing |
| --- | --- | --- |
| **Baseline** | The current value, dated, with its source | Nobody can tell whether it moved |
| **Baseline agreed by · date** | A named customer person confirms the baseline **now, in writing**, before the period starts | Next review's value case is retrospective, tagged *weaker evidence*, and cannot lead the value slide (**C18**) |
| **Target** | An absolute value, not a percentage change | "Improve by 20%" of an unknown base |
| **Their owner** | A named person on the customer side who said yes out loud | The goal is ours, not theirs — the commonest defect |
| **Our owner** | A named person on our side | "The CSM team" does nothing |
| **Date** | A specific date, chosen against their calendar | Q4 is not a date |
| **Measurement source** | Entity · field · cadence, agreed by both sides | Two versions of the truth at the next review |
| **Dependency** | The thing that must happen first, with its own owner and date | The goal fails silently and is argued about later |
| **Expected effect** | Which slide-2 objective it moves, and by how much | A goal nobody can justify against the business case |

**The out-loud rule.** A customer-side owner is only an owner if they said yes in the room,
in their own voice. A name typed into a table by us is a name, not an owner. If they went
quiet when you said their name, the goal is not agreed — say so in the internal plan.

**Dates are set against their calendar, not ours.** A goal dated inside their month-end
close, their audit window or their peak season will not move, and dating it there tells them
we were not listening.

**Agree the baseline in writing, now.** This is the single cheapest thing in the whole review
cycle and the one most often skipped. A baseline agreed at the start of the period and reported
at the end is evidence; the same number reconstructed at review time looks chosen, because it
was — and `qbr-builder` will tag it `retrospective — weaker evidence` and order it below every
agreed line (**C18**). One email, four minutes: *"We're setting the December close target
against 9.0 working days as of 30 November — does that match your records?"* A one-line yes is
the whole mechanism.

**Ask for the number in their words at the same time.** "If this lands, what would you say we
took out of the close?" Their answer, logged with the date, becomes the Customer-stated cell
next period (**C5**) — and a benefit line with no customer-stated form may not lead the value
slide.

---

## 2. Twelve weak → SMART rewrites

Every rewrite below assumes its baseline was agreed in writing by the named customer owner on
the date the goal was set; without that agreement the goal is still valid but next period's
benefit line is retrospective.

| # | Weak | SMART rewrite | Baseline → target | Owner: customer · us | By | Measured in | Dependency |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | "Get Finance using it more" | Raise weekly active users in the Finance cost centre to 22 of 26 licensed seats, sustained 4 consecutive weeks | 4 → 22 WAU | P. Raman (Finance Ops Mgr) · D. Okoye (CSM) | 2026-11-28 | `usage_daily.active_users`, cohort `Finance-CC-4400`, weekly | Their IT provisions the Finance SSO group by 2026-09-19 |
| 2 | "Improve their reporting cycle" | Cut month-end close reporting cycle time from 9.0 to 5.5 working days | 9.0 → 5.5 days | J. Alvarez (Controller) · D. Okoye | 2026-12-31 (Dec close) | Their close calendar, extracted by their FP&A team | Two saved report templates built by us by 2026-10-03 |
| 3 | "Fix the integration" | Restore the CRM sync to ≥98% successful runs over a rolling 30 days, from 61% | 61% → 98% | M. Torres (CRM Admin) · S. Iqbal (Solutions) | 2026-10-17 | `integrations_active` + sync error log, weekly | Their admin grants the API user the missing object permissions by 2026-09-26 |
| 4 | "Reduce their support load" | Cut monthly `type=question` tickets on permissions from 31 to ≤10 by publishing a role guide and running two enablement sessions | 31 → ≤10 / month | L. Chen (Ops Lead) · D. Okoye | 2026-12-05 | `ticket` where `type='question'` and tag `permissions`, monthly | 40 named users attend one of the two sessions |
| 5 | "Roll out to more teams" | Onboard the Legal team — 12 named users completing first core action — as the third department on the platform | 0 → 12 users | R. Whitfield (GC) · A. Nwosu (Onboarding) | 2026-11-14 | `usage_daily` first `core_action` per user, cohort `Legal` | Legal's data-retention review closes by 2026-10-10 |
| 6 | "Get exec buy-in" | Hold one 30-minute working session with the VP Finance, with the FY27 objectives agreed in writing afterwards | 0 → 1 session, objectives in writing | J. Alvarez (Controller) sets it up · D. Okoye runs it | 2026-10-24 | Calendar record + the written objectives | The VP's Q3 board pack lands 2026-10-09 |
| 7 | "Better data quality" | Raise the share of opportunity records with a populated close reason from 42% to 90% across the two sales regions | 42% → 90% | S. Bakr (RevOps) · S. Iqbal | 2026-12-19 | Their CRM field-completeness report, monthly | Field made required by their admin by 2026-10-01 |
| 8 | "Improve adoption of reporting" | Move 8 of their 11 recurring manual reports onto scheduled dashboards, retiring the manual versions | 0 → 8 of 11 | P. Raman · A. Nwosu | 2026-11-30 | Their report inventory, reviewed jointly | We deliver the two blocked report types by 2026-10-17 |
| 9 | "Reduce risk at renewal" *(internal framing leaking into a customer goal)* | Complete the annual security re-review with zero open findings before the Q4 procurement window | 3 open findings → 0 | K. Osei (InfoSec) · our Security team | 2026-11-07 | Their GRC tracker | We supply the updated SOC 2 report by 2026-09-30 |
| 10 | "Train the new team" | Certify 15 of the 18 new Ops hires on the approvals workflow via the two scheduled sessions | 0 → 15 certified | L. Chen · A. Nwosu | 2026-12-12 | Their LMS completion export, per session | Their L&D books both rooms by 2026-10-15 |
| 11 | "Look at expanding usage next year" | Decide by 2026-11-21 whether the Manufacturing division joins in FY27, with a scoped requirements list either way | no decision → a written decision | R. Whitfield · D. Okoye | 2026-11-21 | The written decision, emailed | Discovery session with Manufacturing Ops by 2026-10-31 |
| 12 | "Keep the momentum going" *(unfixable as written)* | **Do not write this goal.** Momentum is not measurable; pick the one objective from slide 2 that is furthest behind and write a goal against that | — | — | — | — | — |

Rewrite 9 shows the firewall in action: the internal thought was renewal risk; the goal the
customer sees is a security re-review with a date. The internal reason stays internal.

Rewrite 12 is the important one. Some goals cannot be rescued, and the right move is to
delete them rather than dress them up. A goal that survives only by being vague will be
reported as "in progress" for four consecutive quarters.

---

## 3. Goal patterns by signal family

Use the family that is furthest behind on slide 3, not the one that is easiest to move.

| Family | Goal pattern | Typical baseline field | Typical dependency |
| --- | --- | --- | --- |
| **Product usage & adoption** | Raise `<metric>` in `<named team>` from `<baseline>` to `<target>`, sustained `<N>` weeks | `usage_daily.active_users`, `core_actions`, `feature_breadth` | Provisioning, SSO group, licence assignment |
| **Breadth / depth** | Onboard `<named team>` — `<N>` users completing first core action | first `core_action` per user | An internal review on their side |
| **Commercial & contract** | Decide `<named decision>` by `<date>`, with a written outcome either way | `subscription.*`, the opportunity record | Their budget cycle or procurement window |
| **Relationship & engagement** | Hold `<N>` working sessions with `<named role>`, with `<artifact>` produced | Calendar + `interaction` records | Their exec's diary; a board or planning cycle |
| **Support & reliability** | Cut `<ticket class>` from `<baseline>` to `<target>` per month via `<named change>` | `ticket` by type and tag | A fix we owe, with its own date |
| **Sentiment & VoC** | Close the loop on `<N>` named pieces of feedback, each with what changed | Survey verbatims, dated | Product decisions we do not control — say so |
| **Billing & payment** | Resolve `<N>` open invoice or entitlement discrepancies | `invoice.status`, entitlement vs usage | Their AP calendar |
| **Firmographic & external** | Align the FY`<N>` plan to their publicly stated `<objective>` by `<date>` | Their earnings call, strategy or annual report | Their planning cycle |

**Never write a goal whose measurement source is only our system when the objective is
theirs.** The close-cycle goal is measured in *their* close calendar, not our usage data.
Usage is the evidence that the mechanism worked; their number is the goal.

---

## 4. Dependencies and the resourcing conversation

Most missed goals are missed on a dependency, not on the goal. The dependency is where the
customer has to spend something — an admin's week, an IT ticket, a legal review — and it is
the part of the goal that gets agreed enthusiastically and resourced never.

**Every dependency carries its own owner and its own date, stated on the slide.** A goal
whose dependency is invisible fails silently and is argued about at the next review.

Ask the question directly at slide 9: *"Which of these three will you not be able to
resource?"* The answer is more valuable than three unqualified yeses.

| What they say | What it means | What to do in the room |
| --- | --- | --- |
| "We can probably find the time" | No resource has been assigned | Ask who, and put the name on the slide, or cut the goal to two |
| "I'll need to check with IT" | The dependency is real and unowned | Make the check itself the first dated step, with their name on it |
| "That's more of a Q1 thing" | The date is wrong, not the goal | Re-date it in the room; a goal with the wrong date fails on schedule |
| "Can you do that part for us?" | A scope question dressed as a dependency | Say yes or no in the room, and if yes it becomes **our** commitment in Part D with its own date |
| Silence | The goal is not agreed | Do not write it down as agreed. Note the silence in the internal plan |

**Three goals with resourced dependencies beat six without.** Cut to what they can actually
staff; the cut itself is a credibility move.

---

## 5. How many, and how to choose

Three is the working maximum for a 45-minute review. Past three, none of them gets a real
owner and the review turns into a list-reading exercise.

Choose by this order:

1. **The objective furthest behind on slide 3** — the one that will be asked about anyway.
2. **The one with the largest business consequence**, in their units, not ours.
3. **One that is genuinely easy** — a goal that will be visibly met by the next review keeps
   the mechanism credible. Not a vanity goal; a real one with a short path.

Never make all three hard, and never make all three ours. At least one goal should have a
customer-side owner doing customer-side work, or the review has quietly become a status
report about our workstream.

---

## 6. Reviewing goals at the next QBR

Prior-period goals appear **on slide 3 as the status column**, not only in the appendix.
Burying last quarter's unmet goals in the appendix is the most-noticed omission in a
business review, and it is noticed by exactly the person you least want to lose.

| Outcome | How to present it |
| --- | --- |
| Met | One line, with the number, and move on. Do not dwell |
| Met but irrelevant | Say so: the goal was wrong, here is the better one |
| Missed on our dependency | Ours first, with what we changed and the new date |
| Missed on their dependency | Factually, without blame: "the SSO group did not get provisioned, so the Finance rollout did not start" — then ask what would make it possible this quarter |
| Missed because the objective changed | Retire it explicitly. A silently dropped goal teaches them goals are decoration |
| Not measurable in retrospect | Own it: the measurement source was never agreed. Fix that first this quarter |

---

## 7. Failure modes

| Failure | Correction |
| --- | --- |
| "Increase adoption next quarter" | Baseline → target → both owners → date → measurement source → dependency |
| A percentage target with no baseline | Absolute values on both ends |
| Only our name against the goal | A named customer owner who said yes out loud |
| More than three goals | Cut to three; the cut is the value |
| A date inside their close, audit or peak season | Date it against their calendar |
| Measurement source unstated, or "we'll track it" | Entity · field · cadence, agreed by both sides |
| A dependency with no owner or date | Its own owner and its own date, on the slide |
| The same goal restated for a third quarter | Kill it, or find the dependency nobody resourced |
| A goal measured only in our product data when the objective is theirs | Measure in their system; use ours as evidence |
| Internal risk language inside a customer goal | Rewrite to the observable outcome; the risk framing stays internal |
