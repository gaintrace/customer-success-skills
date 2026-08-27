# Estimation and Commercial Shape

> An estimate is a claim about the future. It carries a range, a stated confidence and a
> falsifier — and then, separately, a **commitment**, because a range without a commitment moves
> the decision back to the person who asked.
>
> Evidence labels: `[M]` measured · `[V]` vendor · `[P]` practitioner rule · `[A]` academic.

**Contents**
1. [Why estimates fail](#1-why-estimates-fail)
2. [The work breakdown](#2-the-work-breakdown)
3. [Three-point estimation](#3-three-point-estimation)
4. [The cone of uncertainty](#4-the-cone-of-uncertainty)
5. [Contingency](#5-contingency)
6. [Effort, duration and the calendar](#6-effort-duration-and-the-calendar)
7. [Commercial shapes and their incentive effects](#7-commercial-shapes-and-their-incentive-effects)
8. [Margin, rate and utilisation](#8-margin-rate-and-utilisation)
9. [Presenting uncertainty](#9-presenting-uncertainty)
10. [Anti-patterns](#10-anti-patterns)

---

## 1. Why estimates fail

SPI Research's 2026 Professional Services Maturity Benchmark (509 PS organisations, 245,000+
employees, $63bn of PS revenue, FY2025 data) puts average project overrun at 10.7%, improved from
11.3% the prior year — but high-performing organisations run at 6.9% against 12.1% for everyone
else, and **estimating accuracy** and **change-control discipline** are the two maturity
dimensions on which the two groups separate furthest `[M]`. Overrun is not mostly a technical
skill problem. It is an estimating and boundary problem.

| Failure | What it looks like | The fix in this file |
| --- | --- | --- |
| Estimating the happy path | Every package priced as if nothing is discovered | Three-point, with P set by what actually goes wrong (§3) |
| Anchoring on the answer the customer wants | The number arrives before the breakdown | Break down first, sum second, never adjust to a target without saying so |
| Padding every line item | A total nobody believes and a project that expands to fill it | One visible contingency at project level (§5) |
| Quoting a build from a discovery call | A 0.5×–2× range priced as a fixed fee | Quote the discovery (§4) |
| Confusing effort with duration | 80 hours promised as two weeks with one engineer at 40h/week | Usable hours and dependency wait (§6) |
| Pricing customer time at zero | The plan assumes an engineer nobody has asked | The capacity line in `scope-boundaries.md` §6 |
| The wrong commercial shape | Fixed fee on an open scope; T&M on a repeatable one | §7 |

---

## 2. The work breakdown

Estimate packages, not the project. A package is a unit that one person could own end to end and
that has an observable finish.

| Rule | Why |
| --- | --- |
| **4–40 hours per package** `[P]` | Below 4 the overhead of estimating exceeds the value; above 40 the estimate is a guess wearing a decomposition |
| **Name the finish, not the activity** | "Connector syncs 5 days error-free" beats "build connector" — the second has no end |
| **One owner per package** | Shared ownership hides the hand-off, which is where duration goes |
| **Estimate the package, not the person** | Then apply a skill factor once, visibly, if a specific person is assumed |
| **Include the unglamorous packages explicitly** | Environment setup, credentials chasing, test data preparation, re-delivery after a rejection, the handover pack, the readouts |

**The packages that are missing from most estimates** — add them by default, then remove any that
genuinely do not apply:

| Package | Default `[P]` | Why it is forgotten |
| --- | --- | --- |
| Access and credential chasing | 4–12h | It is not engineering, so nobody costs it |
| Test data preparation | 8–16h | Assumed the customer supplies it ready |
| Re-delivery after one rejection | 15% of the build package | Assumes acceptance first time |
| Acceptance support (running the test with them) | 2–4h per milestone | Assumes they will test alone |
| Documentation and runbook | 8–16h | Written last, cut first |
| Handover and knowledge transfer | 8h | Treated as a meeting |
| Project management and status reporting | 10–15% of build effort | Invisible until it is someone's evenings |
| Contingency for the assumption most likely to break | See §5 | Distributed instead of held |

---

## 3. Three-point estimation

```
Per package:   E = (O + 4M + P) / 6            σ = (P − O) / 6
Project:       E_total = Σ E                   σ_total = sqrt( Σ σ² )
Commitment:    P50 = E_total                   P80 = E_total + 0.84 × σ_total
```

| Point | Definition | The question that produces it |
| --- | --- | --- |
| **O** — optimistic | Everything known works first time, no waiting | "If the API behaves exactly as documented and their data is clean?" |
| **M** — most likely | The realistic case, given what you know today | "What would you tell a colleague it will take?" |
| **P** — pessimistic | The plausible bad case — not the catastrophe | "What if their schema is different from the sample and the first sync fails?" |

**Set P from history, not imagination.** P is the 90th-percentile outcome you have actually seen
on this class of work, not the worst thing conceivable. A P that includes "the customer
reorganises" is not an estimate; that belongs in the assumptions register with its own delta.

**Why σ is summed in quadrature.** Independent risks do not all land together. Adding widths
assumes they do, which over-quotes the project and — worse — produces a total nobody defends,
so it gets cut arbitrarily and the discipline is lost.

Worked comparison, five packages each 20h ± 10h:

| Method | Total | Reading |
| --- | --- | --- |
| Sum of most-likely | 100h | No allowance for anything |
| Sum of pessimistic | 150h | Assumes all five bad cases land — implausible |
| PERT with quadrature | E = 100h, σ = √(5 × 3.33²) = 7.5h, **P80 = 106h** | The commitment |

Six extra hours, not fifty. That is the number you can defend line by line, and it is why
per-line padding is both more expensive and less credible.

---

## 4. The cone of uncertainty

Barry Boehm's *Software Engineering Economics* (1981) introduced the cone: at the earliest
concept stage, estimates vary by roughly 0.25×–4× the eventual actual, and the band narrows as
requirements and design are fixed `[A]`. The practical consequence is that **the range width is
set by what you know, not by how confident you feel**, and no amount of experience compresses a
concept-stage estimate to a design-stage range.

| Scoping stage | What is fixed | Range to present | Contingency `[P]` | Shape that fits | Never |
| --- | --- | --- | --- | --- | --- |
| **Concept / discovery call** | The problem, roughly | 0.5×–2× | — | Quote the discovery, not the build | Never quote a fixed fee here |
| **Requirements written** | Deliverables, integrations named, volumes stated | 0.75×–1.5× | 25% | Capped T&M | Never quote a fixed fee without a design phase |
| **Design complete, spike run on the risky part** | Architecture settled, the unknown tested | 0.9×–1.25× | 15% | Fixed fee | — |
| **Reused pattern, delivered before** | Everything except their data | 0.95×–1.1× | 10% | Fixed fee | — |

**Narrowing the cone is a purchasable action, and it is cheap.** A two-day paid spike on the
single riskiest assumption typically moves an engagement from the requirements row to the design
row — from a 0.75×–1.5× range to 0.9×–1.25×. On a 400-hour engagement that is a difference of
roughly 100 hours of exposure for 16 hours of work. Offer it explicitly:

> "I can give you a number today with a range of about ±40%, or I can spend two days testing the
> assumption that worries me most — the shape of the data coming out of your ERP — and come back
> with a fixed price. The two days cost £X and they come off the build if you proceed."

That sentence converts more often than any discount, because it prices certainty rather than
asking for trust.

---

## 5. Contingency

| Rule | Reason |
| --- | --- |
| **Hold it once, at project level, visibly** | Distributed contingency is invisible, and invisible contingency is spent by default |
| **Name who releases it** | Usually the delivery owner, in writing, against a named assumption breaking |
| **Set it from the scoping stage, not from nerves** | §4's table |
| **Show it to the customer as a line, in a capped or T&M shape** | It is a ceiling they benefit from not reaching |
| **Price it in silently in a fixed fee — and record it internally** | The customer buys a number; you still need the workings for the margin review |
| **Release it, do not consume it** | Contingency unspent at the end of a milestone is reported, not absorbed into the next |

**The contingency ledger** — four columns that stop it evaporating: `assumption · reserve (hours)
· released on (date, reason) · remaining`. Report the remaining figure at every internal delivery
review. A project that has consumed 80% of contingency at 40% of milestones is a re-baseline
conversation now, not a surprise in week nine.

---

## 6. Effort, duration and the calendar

```
usable_hours_per_week = FTE × 40 × 0.60                                  (R13)
build_days            = E_total / (FTE × 8 × 0.60)
duration_days         = build_days + Σ dependency_wait_days + acceptance_days
acceptance_days       = 5 business days per milestone review + 15 days of headroom
                        before the last acceptance date                  [P]
```

`R13` — the capacity truth: usable time is about 60% of a nominal week once meetings, internal
escalations, context switching and recruiting are removed. Planning at 100% produces a schedule
that is wrong in week one and a delivery lead nobody believes by week three.

| Calendar factor to state explicitly | Typical effect |
| --- | --- |
| Their finance close week | 3–5 days where no customer-side dependency moves |
| Their change-freeze windows (retail Q4, public-sector year end) | Weeks, sometimes months |
| Public holidays on both sides, and school holidays for a single-owner dependency | Days per occurrence |
| Their security review board cadence (monthly, not on demand) | Up to 4 weeks of wait for a 2-hour review |
| Our own delivery-team leave | State it; a plan built on a person is a plan with a single point of failure |

**Effort is what you charge for; duration is what you promise.** Print both. A SOW that promises
a date without printing the effort invites the customer to compress the date; one that prints
effort without a date invites them to assume next week.

---

## 7. Commercial shapes and their incentive effects

Every shape moves overrun risk and changes what each side is rewarded for. Choosing by habit is
how a repeatable deployment ends up on T&M and an open-ended one ends up fixed-fee.

| Shape | Bears overrun | Rewards us for | Rewards them for | Use when | Failure signature |
| --- | --- | --- | --- | --- | --- |
| **Capped T&M against accepted milestones** | Them to the cap, us beyond | Efficiency; flagging early, because the cap is shared information | Approving fast — slow acceptance burns their own cap | **Default for a first deployment** | The cap becomes a fixed fee in their head; restate it as a ceiling at every review |
| **Fixed fee** | Us | Tight scope, disciplined change control, reuse | Pushing more inside the same fee | Design complete, or a pattern delivered before | Every conversation becomes a scope argument, and the relationship pays for it |
| **Pure T&M** | Them | Doing the right thing without a negotiation | Watching the burn and questioning invoices | Discovery, spikes, open-ended enablement | Budget anxiety; the meter is always running and trust erodes weekly |
| **Milestone-based payment** | Split by milestone | Getting things **accepted**, not merely delivered | Accepting promptly | Any engagement with a nervous CFO or a staged budget | An unaccepted milestone strands both the revenue and the value evidence |
| **Included in the licence** | Us, entirely and indefinitely | Nothing — there is no meter and no ceiling | Asking for everything, because it is free | Only a published, bounded configuration list | The unbounded consultancy. The most expensive shape there is |

**The recommendation.** Capped T&M against accepted milestones for a first deployment; fixed fee
only once design is complete or the pattern is a reuse; included-in-licence only where the scope
is a published list you would hand every customer unchanged.

**Deviate when procurement can transact only a fixed fee.** Then sell a paid design phase, fix
the price after it, and say why in one sentence: *"I would rather give you a firm number than a
padded one, and two weeks of design is what turns one into the other."* Fixing a price against a
0.5×–2× range and calling the difference contingency transfers a risk you have not measured.

**Hybrid shapes that work.** T&M for discovery and design, fixed fee for the build once design
closes. Capped T&M for the build, fixed fee for a well-understood migration inside it. Fixed fee
for the deployment, T&M for enablement, which is genuinely open-ended and should be priced that
way rather than absorbed.

---

## 8. Margin, rate and utilisation

**Internal only.** None of this crosses the divider (`R18`).

```
loaded_cost      = Σ (package hours × loaded hourly cost of the role doing it)
gross_margin     = (fee − loaded_cost) / fee
effective_rate   = fee / E_total
break_even_rate  = loaded_cost / E_total
```

SPI Research's 2026 benchmark puts billable utilisation at 66.4% in 2025 — the lowest in its
survey history — against 75.0% for high-performing organisations `[M]`. Two consequences for
this document:

1. **An estimate priced at 100% utilisation is priced at a number nobody achieves.** Cost the
   engagement at your actual utilisation, not at nominal capacity.
2. **In mainstream B2B SaaS the FDE function is usually expected to be at least gross-margin
   neutral** `[P]`, unlike the frontier-lab model where forward-deployed work is subsidised as
   product discovery. Know which economics you are operating under before you agree to absorb
   anything, because "we'll just do it" has a different meaning in each.

| Margin band `[P]` | Read | Action |
| --- | --- | --- |
| ≥ 40% | Healthy for a repeatable deployment | Proceed |
| 25–39% | Normal for a first-of-kind | Proceed; name the two packages carrying the risk |
| 10–24% | Thin | Proceed only with a written reuse rationale — what this engagement produces that the next one inherits |
| < 10% | Loss-leading | A commercial decision, not a delivery one. It needs a named approver above the delivery lead and a written reason |
| Negative | Subsidy | Only where a strategic reason is written down and the ARR at stake is stated |

**The reuse question, asked at scoping and not afterwards.** Which packages here produce
something a second customer inherits — a connector, a template, a reference implementation, a
documented pattern? An engagement with zero reusable output is consultancy revenue; an engagement
where a third of the packages generalise is worth accepting at a lower margin, and the decision
should be made deliberately rather than discovered later. `custom-vs-product` scores it.

---

## 9. Presenting uncertainty

Five rules. Breaking any one produces either false precision or a useless answer.

| Rule | Right | Wrong |
| --- | --- | --- |
| **Never a single number without a range** | "About 320 hours, most likely between 290 and 400" | "320 hours" |
| **Never a range without a commitment, and the commitment is the ceiling** | "We will cap it at 380 hours" | "Between 290 and 400, let's see how it goes" |
| **Name the top three drivers of the width, each with the action and date that narrows it** | "The ERP extract shape, their SSO model, and whether the archive is in scope — I can close the first two by 12 September" | "There are various unknowns" |
| **State what halving the range would cost** | "Two days on a data spike takes the top end from 400 to about 350" | Widening the range instead of testing it |
| **Never widen a range in place of doing the work** | Test the assumption | "Somewhere between four and twenty weeks" |

**The one-paragraph estimate a sponsor can act on:**

> "Four hundred hours is the number to plan against, and we will cap the fee at that. The
> realistic range is 290–400, and the width comes almost entirely from one thing: we have seen a
> sample of your invoice data but not the live extract. Two days of spike work closes that, and I
> would rather spend them before you commit a budget than after. If the extract looks like the
> sample, the number lands near 310."

Four sentences, a commitment, the driver of the uncertainty, the action that closes it, and the
falsifier. That is what converts.

**Confidence and coverage (`R23`).** Estimate confidence never exceeds what the Coverage Ledger
permits. Two families missing on a scoping run — typically commercial and relationship — means
the opt-out deadline and the customer's engineering capacity are both unknown, and neither the
date nor the duration is defensible. Say so, and cap.

---

## 10. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| A single-number estimate | Three-point, σ in quadrature, a range whose width matches the stage, and a ceiling |
| Padding every line item | One visible contingency at project level, with a named releaser |
| The number arriving before the breakdown | Break down first. An estimate reverse-engineered from a target is a budget, and it should be labelled one |
| Sum of pessimistic as the commitment | Independent risks do not all land. Use P80 |
| Fixed fee quoted from a discovery call | Quote the discovery, or run capped T&M |
| P set to the catastrophe | P is the plausible bad case. Catastrophes belong in the assumptions register with their own delta |
| Effort promised as duration | Usable hours at 60%, plus dependency wait, plus acceptance days |
| Customer-side time priced at zero | The capacity line, agreed by the manager who controls it |
| Contingency distributed into tasks | Held once, visibly, released against a named assumption |
| Contingency spent silently | The contingency ledger, reported at every delivery review |
| Utilisation assumed at 100% | Cost at your actual utilisation |
| Included-in-licence for anything unbounded | The shape with no meter. Reserve it for a published configuration list |
| Widening the range to avoid being wrong | Test the assumption, then narrow it |
| Margin never calculated at scoping | It cannot be recovered later. Compute it before signature and name the approver below 25% |
| Sending estimate workings, contingency or margin to the customer | The customer gets the ceiling, the dates, the exclusions and the change process (`R18`) |
