# SMART Goal Library

> Eight worked goals, each shown as the weak version people actually write and the rewrite that
> survives a customer executive reading it. Every rewrite carries a baseline with a source, a
> target, a date, owners on both sides, a measurement method, and the dependency most likely to
> block it.
>
> Evidence labels: `[M]` measured · `[PROD]` published production configuration · `[V]` vendor ·
> `[P]` practitioner · `[A]` academic.

**Contents**
- [1. The gate](#1-the-gate)
- [2. The four tests and the falsification test](#2-the-four-tests-and-the-falsification-test)
- [3. Eight worked goals](#3-eight-worked-goals)
- [4. Fast rewrite bank](#4-fast-rewrite-bank)
- [5. Goals by business model](#5-goals-by-business-model)
- [6. Setting a target that is ambitious rather than fictional](#6-setting-a-target-that-is-ambitious-rather-than-fictional)
- [7. Anti-patterns](#7-anti-patterns)

---

## 1. The gate

The original acronym, from Doran's 1981 article in *Management Review*, reads **Specific,
Measurable, Assignable, Realistic, Time-related** `[A]`. The later substitution of "Achievable" for
**Assignable** removed the only letter that required a named human, and success plans have been
paying for it since. This library uses the original.

| Letter | Requirement | Rejection test |
| --- | --- | --- |
| **S** — Specific | The population, the exclusions, and the definition of the counted event | Two analysts pulling the number get different answers |
| **M** — Measurable | A named system, a named field, a stated frequency, a named person who re-runs it | "We will track it", with no source |
| **A** — Assignable | One named customer owner **and** one named vendor owner | Only our names appear |
| **R** — Realistic | The arithmetic that makes the target reachable, taken from their own data | A round number nobody derived |
| **T** — Time-related | A date. "By Q4" is not a date | A quarter, a season, or "ongoing" |

Goal-setting research supports the specificity requirement directly: specific, difficult goals
outperform "do your best" instructions across decades of studies, because a do-your-best goal has no
external referent and is defined idiosyncratically by each person (Locke & Latham; meta-analysed
across 183 independent studies by Klein, Wesson, Hollenbeck & Alge, *Psychological Bulletin*, 1999)
`[A]`. A vague goal is not a kinder goal — it has no performance effect at all.

Lincoln Murphy's constraint sits on top of it: *Objective + Conditions + Time Frame* make a goal,
and **without a timeframe a goal is just a wish** `[P]`. His "Conditions" are the specific qualities
that must hold for the customer to feel successful — meet the number the wrong way and they will
still judge the programme a failure.

---

## 2. The four tests and the falsification test

| Test | Question | Failure means |
| --- | --- | --- |
| **Ownership** | Is a named customer employee on the hook? | It is a vendor task, not a goal |
| **Compensation** | Is a named executive measured on the parent objective? | It will lose to something that is |
| **Money** | Can it convert to currency with a unit economic they supply? | It can never appear in the renewal value case |
| **30-day** | Is there a leading indicator that moves within 30 days? | Failure surfaces a quarter late |
| **Falsification** | Could two people looking at the same data disagree about whether it is done? | The success criteria are not criteria |

---

## 3. Eight worked goals

Every goal below is written for a fictional account. Numbers are illustrative of the *shape*; use
your own customer's data, never these figures.

### Goal 1 — Support cost, from ticket and telemetry data

| | |
| --- | --- |
| **Weak** | "Increase self-service usage and reduce ticket volume." |
| **Rewritten** | **Reduce Tier-1 support tickets from 412 to 290 per 1,000 active accounts per month by 31 December 2026**, by extending the in-product help widget from 3 surfaces to all 11 and publishing knowledge articles for the remaining 2 of the top-4 ticket topics. |
| **Baseline** | 412 per 1,000 active accounts/month · Q1 mean, 2026-01-01 → 2026-03-31 · support export, `ticket.type = tier_1`, pulled 2026-04-04 by Priya N. |
| **Target · date** | 290 per 1,000 · 2026-12-31. Milestones: 30 Sep 6 surfaces live · 31 Oct both articles published · 30 Nov all 11 live |
| **Owners** | Customer: Priya N., Director Support Ops. Vendor: CSM + Solutions Architect |
| **Measurement** | Support platform monthly export, denominator from product analytics MAU; re-run by Priya on the 5th |
| **Realistic because** | 31% observed deflection on the 3 already-covered surfaces × 63% topic coverage implies a 105–160 ticket reduction band; the target sits at the low end |
| **Leading indicator** | Widget impressions on new surfaces ≥4,000/week by 15 Oct; deflection ≥25% within 3 weeks of each launch |
| **Value** | 122 tickets/1,000 × 11.9k accounts ÷ 1,000 = 1,452/month × $18.40 = $26.7k/month; 70% attribution set by the customer ⇒ ~$224k/year, classed **cost avoidance** |
| **Blocking dependency** | Widget rollout rides their front-end release train, which ships 15 Sep and 15 Nov only; article authoring needs 40 hours of SME time not yet allocated |

### Goal 2 — Licence activation, from seat and workflow data

| | |
| --- | --- |
| **Weak** | "Improve onboarding and increase usage of unused licences." |
| **Rewritten** | **Increase weekly active users in the Claims organisation from 214 (39.6%) to 405 (75%) of 540 provisioned licences by 31 March 2027**, by lifting certification completion from 22% to 70% and cutting median time-to-first-action from 34 days to 10. |
| **Baseline** | 214 weekly active of 540 provisioned · week of 2026-08-17 · product analytics weekly cohort report; certification 22% from their LMS export, 2026-08-15 |
| **Target · date** | 405 weekly active · 2027-03-31. Milestones: 31 Oct curriculum revised and manager dashboard live · 31 Dec certification ≥50% · 28 Feb WAU ≥340 |
| **Owners** | Customer: D. Okafor, VP Claims Operations — certification written into Q4 team objectives. Vendor: CSM + Enablement |
| **Measurement** | Weekly active = ≥1 completed claim workflow in a 7-day window, Claims org only; product analytics weekly cohort report plus LMS completion export |
| **Realistic because** | In their own cohorts, certified users are weekly active 71% of the time against 17% uncertified; applying 71% to a 70%-certified population predicts ~78% active, so 75% sits below the model output |
| **Leading indicator** | Certification starts ≥45/week from 15 Oct; median time-to-first-action ≤18 days by 30 Nov |
| **Value** | Converts a ~$147k downsell exposure on 326 idle licences into a defensible retain; productivity benefit stated separately with a 50% recapture rate and its own risk adjustment |
| **Blocking dependency** | Claims peak season (Nov–Jan) suppresses training time; enforcement above director level is unconfirmed |

### Goal 3 — Revenue influence, with an honest attribution design

| | |
| --- | --- |
| **Weak** | "Drive $4.2M of additional revenue through increased proposal-module usage." |
| **Rewritten** | **Increase proposal-module usage from 36% to 70% of qualified opportunities across all 7 regions by 30 June 2027, and hold the win-rate differential at ≥5 points in a matched-region comparison**, with EMEA-South and APAC held as a staged control through Q1 to test causality. |
| **Baseline** | 36% of qualified opportunities · trailing 2 quarters to 2026-08-31 · CRM opportunity report joined to the product event log; win rate 34.2% adopted (n=488) vs 26.9% non-adopted (n=852) |
| **Target · date** | 70% usage · 2027-06-30. Staged rollout 1 Nov (3 regions) · 1 Feb (2) · 1 Apr (final 2); controls released after 31 Mar |
| **Owners** | Customer: M. Reyes, VP RevOps (measurement) and the regional sales directors (adoption). Vendor: CSM + Value Engineer |
| **Measurement** | Qualified = stage ≥3 and value ≥$25k; usage = ≥1 proposal generated. Matched-cohort analysis run monthly by their RevOps team |
| **Realistic because** | Two regions already run at 61% and 74%, so 70% is demonstrated inside their own business rather than assumed |
| **Leading indicator** | Per-region usage weekly; ≥50% within 6 weeks of each regional launch |
| **Value** | Presented twice: gross (5pts × 852 previously non-adopting deals × $86k) and attributed at the customer-set 40%. The artifact carries the sentence "correlational until the matched-region comparison completes in Q1; two regions are deliberately held to test it" |
| **Blocking dependency** | A 1 Jan pricing change and a concurrent methodology rollout confound the read; regional directors have no shared incentive tied to usage |

### Goal 4 — Establishing a baseline, when none exists

| | |
| --- | --- |
| **Weak** | "Demonstrate ROI by the renewal." |
| **Rewritten** | **Establish a measured baseline for order-error rate across the 4 distribution centres, agreed in writing by the Operations Director, by 15 October 2026** — reconstructed from their WMS exception log for 2026-04-01 → 2026-09-30, with the method documented and a named owner who will re-run it monthly. |
| **Baseline** | None exists. That is the finding, and it is why this is the first objective |
| **Target · date** | A signed-off baseline record with value, window, source, owner and unit economic · 2026-10-15 |
| **Owners** | Customer: J. Vance, Operations Director. Vendor: CSM + Data Engineer |
| **Measurement** | WMS exception log, `exception_type in (pick_error, pack_error)`, per 10,000 lines shipped, monthly |
| **Realistic because** | The log exists and holds 18 months of history; the work is extraction and agreement, not instrumentation |
| **Leading indicator** | Extract delivered to the customer by 26 Sep; their review meeting held by 8 Oct |
| **Value** | None claimed yet, and saying so is the point. No ROI claim is made against this objective until the baseline is agreed |
| **Blocking dependency** | Warehouse-systems team capacity; their October stocktake occupies the same people |

### Goal 5 — A goal for a technical buyer

| | |
| --- | --- |
| **Weak** | "Improve pipeline reliability." |
| **Rewritten** | **Reduce the failure rate on the main branch from 30% to under 5%, with the root cause documented and shared with their engineering lead, by 28 February 2027**, measured as failed runs ÷ total runs on protected branches over a trailing 30 days. |
| **Baseline** | ~30% failure rate on main · 2026-07-01 → 2026-08-31 · CI export, protected branches only, pulled 2026-09-02 by their platform lead |
| **Target · date** | <5% · 2027-02-28. Milestones: 31 Oct required checks enabled on all protected branches · 30 Nov flaky-test quarantine live · 31 Jan failure rate <10% |
| **Owners** | Customer: A. Bello, Platform Engineering Lead. Vendor: CSM + Solutions Architect |
| **Measurement** | CI analytics, failed runs ÷ total runs, trailing 30 days, reviewed fortnightly |
| **Realistic because** | 62% of current failures trace to 9 known flaky tests already identified in their own triage doc |
| **Leading indicator** | Failed-pipeline reruns per week falling for 3 consecutive weeks; median time to green under 25 minutes |
| **Value** | Engineer hours lost per failed release × loaded hourly rate, customer-supplied; classed **productivity**, recapture rate stated |
| **Blocking dependency** | A change freeze covers their November peak trading window |

### Goal 6 — Expansion of scope, written as the customer's outcome

| | |
| --- | --- |
| **Weak** | "Roll out to more teams." |
| **Rewritten** | **Onboard the EMEA and APAC claims teams — 168 users — to production with ≥60% weekly active in each region by 30 November 2026**, so that regional backlog reporting runs on one system before the FY27 planning cycle. |
| **Baseline** | 0 users in EMEA and APAC · as-of 2026-08-27 · provisioning export |
| **Target · date** | 168 provisioned, ≥60% weekly active per region · 2026-11-30 |
| **Owners** | Customer: L. Marchetti, Regional Operations Manager (EMEA) and T. Nakamura (APAC). Vendor: CSM + Onboarding Manager |
| **Measurement** | Provisioning export plus weekly active by region, product analytics, weekly |
| **Realistic because** | The North America rollout reached 64% weekly active within 8 weeks with the same enablement package |
| **Leading indicator** | Both regional kickoffs held by 20 Sep; ≥40% weekly active within 4 weeks of each go-live |
| **Value** | Retires two regional spreadsheet processes; their cost supplied by the regional managers |
| **Blocking dependency** | Data-residency review for EMEA has no named reviewer yet — a register row, with a date |

### Goal 7 — A quality goal, made falsifiable

| | |
| --- | --- |
| **Weak** | "Achieve 100% customer satisfaction on all tickets in FY27." |
| **Rewritten** | **Raise Tier-1 CSAT from 4.1 to 4.4 on a 5-point scale by 30 June 2027**, measured on at least 300 responses per quarter so the number is stable enough to act on. |
| **Baseline** | 4.1 mean · FY26 Q4, 312 responses · support platform CSAT export, 2026-07-05 |
| **Target · date** | 4.4 · 2027-06-30 |
| **Owners** | Customer: Priya N., Director Support Ops. Vendor: CSM |
| **Measurement** | Post-resolution survey, Tier-1 tickets only, quarterly, minimum 300 responses or the quarter is reported as insufficient |
| **Realistic because** | Their own top-quartile agents already average 4.5; the target is the median moving toward a level already achieved internally |
| **Leading indicator** | First-response time under 2 hours on ≥90% of Tier-1 tickets, monthly |
| **Value** | Not monetised. Listed in the un-monetised panel beside the ROI figure, never inside it |
| **Blocking dependency** | Response volume drops below 300 in Q2 because of their seasonal ticket mix — state the risk now, not at the review |

### Goal 8 — A governance goal, because some objectives are structural

| | |
| --- | --- |
| **Weak** | "Get executive buy-in." |
| **Rewritten** | **Secure a named executive sponsor at VP Operations or above and a signed 12-month programme charter by 15 October 2026**, with the charter naming the three objectives, their owners and the review cadence. |
| **Baseline** | No named sponsor; last executive-level contact 2026-03-12 · CRM activity record |
| **Target · date** | Sponsor named in the CRM and charter signed · 2026-10-15 |
| **Owners** | Customer: D. Okafor to nominate. Vendor: VP Customer Success — not the CSM; an exec ask travels better from an exec |
| **Measurement** | Signed charter document; sponsor recorded as `economic_buyer` on the account |
| **Realistic because** | Two of the three objectives already sit inside that VP's scorecard |
| **Leading indicator** | Introduction meeting scheduled within 14 days |
| **Value** | Structural. A renewal without an executive-sponsor meeting inside two quarters does not enter Commit (**R6**) |
| **Blocking dependency** | Their reorganisation completes on 1 October; the right person may not exist until then |

---

## 4. Fast rewrite bank

| Weak | Rewritten |
| --- | --- |
| "Increase adoption" | "Raise weekly active licensed users in the Claims org from 214/540 (40%) to 405/540 (75%) by 31 March, owned by D. Okafor" |
| "Improve reporting" | "Cut month-end close reporting from 6 business days to 3 by the September close, freeing 96 analyst hours per quarter" |
| "Reduce churn" | "Reduce logo churn in the SMB book from 2.4%/month to 1.8%/month by Q4, measured on the monthly cohort report" |
| "Use the API more" | "Automate the top 3 manual data transfers identified on 12 Sep, removing 22 hours/week of analyst effort, by 30 November" |
| "Better visibility for managers" | "Give all 14 regional managers a daily backlog view they open ≥3 times a week by 31 October, so queue rebalancing happens before the backlog ages past 5 days" |
| "Reduce risk" | "Close the 6 open audit findings related to access review by the Q3 internal audit, evidenced in their GRC tool" |
| "Faster onboarding of new staff" | "Cut time from new-hire start date to first independently completed claim from 21 days to 10 by 31 January" |
| "Consolidate tools" | "Retire the 2 named point tools at their renewal dates (14 Nov and 3 Feb), removing $84k of annual licence cost" |

---

## 5. Goals by business model

Read `../../cs-context/references/business-model-profiles.md` before writing targets. The same goal is
right in one model and meaningless in another.

| Model | Goals that work | Goals that do not |
| --- | --- | --- |
| **Annual enterprise, seat-based** | Licence activation by department, workflow throughput, cost per transaction, cycle time | Anything measured only in aggregate logins |
| **Consumption / usage-based** | Committed-spend attainment, cost per unit of their output, workloads migrated by date | Seat utilisation — there are no seats to under-use |
| **Self-serve / PLG** | Activation rate per cohort, paid-conversion rate, workspace-level habit metrics | Quarterly executive review milestones; there is no executive to review with |
| **Platform with services** | Go-live per module, services burn against plan, verified outcomes per module | A single account-level adoption percentage that hides module-level failure |
| **Regulated / public sector** | Compliance deadlines, audit findings closed, evidence artifacts produced | Anything whose date can slip; the regulatory date is the target date |

---

## 6. Setting a target that is ambitious rather than fictional

Four derivations, in order of defensibility. Show the arithmetic on the face of the plan.

| Method | How | Example |
| --- | --- | --- |
| **Internal best-performer** | Take a segment of their own business already achieving it | "Two regions run at 61% and 74%, so 70% is demonstrated" |
| **Observed mechanism** | Apply a rate you have measured to the population you will cover | "31% deflection on covered surfaces × 63% topic coverage = 105–160 tickets; target at the low end" |
| **Cohort comparison** | Compare to customers of yours in a similar journey, stated as a range, never as a promise | "Comparable rollouts reached 60% within 8 weeks; we plan to 60% at 12 weeks" |
| **Customer-set stretch** | They name it. Use the low end of any range they give | "They said 70–80%; the plan says 70%" |

**Never** set a target from an external benchmark without a haircut and a label, and never set one by
rounding up from what looks good in a deck. A target nobody derived is the first thing an executive
challenges, and losing that exchange costs the plan its credibility for a year.

---

## 7. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| A goal with a target but no baseline | The baseline is the deliverable; write that goal instead |
| "A" read as Achievable | Assignable. One named human on each side, or it is not a goal |
| A quarter as the deadline | A date |
| A goal only we can influence | Find the customer-owned lever; ours is an initiative beneath it |
| A round-number target | Show the derivation; four methods, in order of defensibility |
| A goal with no leading indicator | Add one that moves within 30 days, with a threshold |
| Gross value presented as attributed value | Present both, with the attribution percentage the customer set |
| Monetising satisfaction or morale inside the ROI figure | Separate un-monetised panel, adjacent, labelled |
| A goal whose measurement source will not exist at the target date | Register it as a measurement-integrity risk now |
| Revising a target upward mid-flight without a changelog | Record what input changed and who agreed it |
