# Carrying Cost

> The build is the deposit. This file prices the loan.
>
> Three interest streams, an annual drift, a multi-year total, and the two numbers that end the
> argument: the **interest rate** (annual carrying ÷ principal) and the **share of account ARR**.
> Then the break-even generality threshold `K*`, the debt-register row that opens the day the
> work is approved, and the annual cull that re-decides every live component with today's numbers.
>
> Nothing here is a forecast. Renewal exposure is ARR × a band midpoint, stated as exposure and
> never as a churn probability (`R22`). Composites round to two significant figures.
>
> Evidence labels: `[M]` measured · `[V]` vendor research · `[P]` practitioner standard ·
> `[A]` academic, standards body or regulation · `[D]` primary document.

**Contents**
- [1. The three currencies](#1-the-three-currencies)
- [2. Estimating the inputs](#2-estimating-the-inputs)
- [3. The arithmetic](#3-the-arithmetic)
- [4. Three worked examples](#4-three-worked-examples)
- [5. The break-even generality threshold `K*`](#5-the-break-even-generality-threshold-k)
- [6. The annual cull](#6-the-annual-cull)
- [7. The debt-register row and the paydown reserve](#7-the-debt-register-row-and-the-paydown-reserve)
- [8. Pricing by business model](#8-pricing-by-business-model)
- [9. Anti-patterns](#9-anti-patterns)

---

## 1. The three currencies

Bespoke code pays interest annually in three currencies, and the memo that prices one of them
has priced none of them. The default failure is arithmetic on the principal alone.

| Stream | What it is | Where it lands | Who feels it |
| --- | --- | --- | --- |
| **Engineering interest** | Maintenance, incidents, attributable support load, eval and regression runs, third-party fees | Delivery capacity, every year | The maintainer, and the three accounts they did not get to |
| **Upgrade interest** | Hours this component adds to each platform upgrade, plus the value of releases the customer cannot take while it is pinned | The upgrade calendar | The customer, as a version they cannot have |
| **Renewal interest** | `arr_at_stake × band_uplift` — the exposure created by carrying an account-specific dependency | The renewal margin conversation | The account owner, at T-90 |

The proportions are not close to intuition. Maintenance is roughly **60% of total software
lifecycle cost** — the 40–80% band Robert Glass records as the "60/60 rule", of which enhancement
rather than defect repair is about 60% `[A · Glass, *Facts and Fallacies of Software Engineering*,
2002; Lientz & Swanson, 1980]`. Stripe's *The Developer Coefficient* (Sept 2018; 1,000+ developers
and 1,000+ C-level executives across five countries) put maintenance and bad code at **17.3 hours
of a 41.1-hour week — 42% of capacity**, split 13.5 hours on technical debt and 3.8 on bad code
`[M · self-reported survey]`. McKinsey's *Tech debt: Reclaiming tech equity* (Oct 2020; 50 CIOs at
$1bn+ financial-services and technology firms) found technical debt at **20–40% of the technology
estate's value before depreciation**, with **10–20% of the new-product technology budget** diverted
to servicing it `[M]`. At national scale, CISQ put accumulated US software technical debt at
**~$1.52tn** inside a $2.41tn total cost of poor software quality `[A · CISQ, Krasner, Dec 2022]`.

**The three-year default follows from that.** A one-year view books the deposit and one year of a
stream that runs for the component's life, and it systematically returns the wrong outcome at
Gate 4. Use one year only for a component with a written, dated sunset inside twelve months.

**None of these numbers crosses the divider** (`R18`). The carrying cost, the interest rate, the
share of ARR and the outcome word are internal; the customer hears what we will do.

---

## 2. Estimating the inputs

Every input is a claim about the future, so it carries a range, an inference rule and a falsifier
(`../../cs-context/references/evidence-standard.md` §3). What follows is where each number comes
from and the specific way it goes wrong.

| Field | Source | The trap | Default when absent |
| --- | --- | --- | --- |
| `build_hours` | The design, or a three-point estimate | A concept-stage estimate carries a 0.25×–4× spread `[A · Boehm, *Software Engineering Economics*, 1981]`. Below a written design, score rubric dimension 4 as **0** | `UNKNOWN — requires a design or a two-day spike` |
| `maintenance_h` | The engineer who will own it, asked for a **monthly** number | Annual estimates are compressed by roughly half. Ask "hours in a normal month", multiply by 12 | 15% of `build_hours` per year `[P]` |
| `incident_h` | Incident records attributed to the component | The single most underestimated input. A bespoke path with no monitoring produces incidents that are logged against something else | 40% of `maintenance_h` `[P]` |
| `support_h` | Ticket time tagged to the component, including triage that ended elsewhere | Triage time on tickets that turned out to be unrelated is still caused by the component | 25% of `maintenance_h` `[P]` |
| `eval_regression_h` | Regression-suite runtime plus the human review it needs | Zero only where a golden dataset and an automated gate exist. Hand-tuned prompts with no eval suite are code without tests | 0 where no model or prompt is involved |
| `upgrade_tax_h` | Hours added to the last upgrade by this component | Reconstructed from memory is acceptable; say so and mark it inferred | 4h per upgrade `[P]` |
| `upgrades_per_year` | **Our** release cadence, from `cs-context` — not theirs | Using the customer's upgrade appetite understates: we pay the tax whether they take the release or not | 4 |
| `third_party_cost_per_year` | Licences, infrastructure, per-call fees, a dedicated environment | Per-call fees are invisible at pilot volume. Price at production volume, not at pilot | 0, stated explicitly |
| `withheld_feature_cost` | Releases the customer cannot take while pinned | Non-zero the moment a version pin exists. Price it as the services hours to unpin plus the renewal exposure of the gap | 0 unless a pin exists |
| `band_uplift` | `churn-risk` band midpoints: **0.05** Watch · **0.15** At Risk | At Risk applies where the component is unowned or bus-factor 1 — that is a property of our staffing, not of their sentiment | 0.05 |
| `loaded_rate` | `cs-context`; salary + benefits + overhead ÷ billable hours | A guessed rate moves every threshold in the memo. Assume, record it in the Assumptions table, and state what flips at ±50% | $150/h, recorded |
| `drift` | Annual growth in carrying | See §3 | 0.15 |

**Hours convert at usable capacity, never nominal** (`R13`). A 96-hour build costs 160 hours of a
person's calendar: meetings, interrupts, internal escalations and recruiting take the rest. SPI
Research puts billable utilisation at **66.4% in 2025**, its lowest recorded `[V · SPI Research,
2026 benchmark]` — near enough the 60% convention to keep using it, and far enough from 100% that
a plan built on nominal hours is a plan that does not finish.

**Reconstructing hours after the fact is legitimate; pretending you did not is not.** Label a
reconstructed figure inferred, state the reconstruction rule ("Priya's estimate of a normal
month × 12, cross-checked against 14 tickets tagged `close-out-export` in 12 months"), and give
it a falsifier.

---

## 3. The arithmetic

```
principal            = build_hours ÷ 0.6 × loaded_rate                       (R13)

engineering_interest = (maintenance_h + incident_h + support_h
                        + eval_regression_h) × loaded_rate
                       + third_party_cost_per_year
upgrade_interest     = upgrade_tax_h × upgrades_per_year × loaded_rate
                       + withheld_feature_cost
renewal_interest     = arr_at_stake × band_uplift                            (R22 — exposure)

annual_carrying(n)   = (engineering + upgrade + renewal) × (1 + drift)^(n−1)
TCO(N)               = principal + Σ_{n=1..N} annual_carrying(n)

interest_rate        = annual_carrying(1) ÷ principal
share_of_arr         = annual_carrying(1) ÷ account_arr
```

Run `../scripts/carrying_cost.py` rather than doing this in prose. It computes the streams, the
multi-year total, `K*`, the gate sequence and the revenue trade from one JSON file, rounds
composites to two significant figures, and refuses to return a nonsense `K*` where generalising
never pays back.

### Drift

**0.15 per year is the default `[P]`.** Bespoke code gets dearer as the platform moves away from
it: interfaces it depends on are deprecated, the people who wrote it leave, and every release
widens the distance between the supported path and the private one. Hyrum's Law is the mechanism —
with enough consumers, every observable behaviour of a system becomes a dependency somebody
relies on, so the surface you must not break grows without anyone deciding it should `[P]`. The
figure is anchored on McKinsey's 10–20% of new-product budget diverted to servicing debt
`[M · Oct 2020]`, taken at the low end because a single component is a small share of the estate.

| Situation | Drift | Why |
| --- | --- | --- |
| Documented extension point, tests, owner, supported dependencies | **0.08** | The platform is not moving away from it |
| Default | **0.15** | — |
| Undocumented interface, no tests, or a pinned version | **0.25** | Every release is a merge risk |
| Bus factor 1, or the owner has given notice | **0.30**, and the component enters the cull immediately | The next incident is an archaeology project |

### Reading the two ratios

| Ratio | Threshold | What it means and what happens |
| --- | --- | --- |
| **Interest rate** | **> 100%** | The component costs more each year than it cost to build. Not automatically wrong on a component carrying $600k of ARR — always a deliberate decision, stated in the renewal margin conversation, never a default |
| **Interest rate** | **< 30%** | Cheap to carry. Rubric dimension 5 scores 4 |
| **Share of account ARR** | **> 5%** | This is a commercial decision, not an engineering one. It goes to the account owner that week `[P]` — services attached to a subscription are structurally unprofitable, and the TSIA Cloud 40 companies that break out project-services margins average **−9%** (published 2023 on Q3-2022 data) `[V]` |
| **Share of account ARR** | **> 15%** | The account is a services engagement with a subscription attached. Price the trade (`saying-no.md` §4) or decline |

**State the number and stop** (`C3`). "Three-year carrying of $110k against $980k of ARR" is the
sentence; the justification goes before it, never after. A hedge appended to a number invites a
negotiation about the number.

---

## 4. Three worked examples

All three are reproducible at $150/h, a 3-year horizon, 15% drift and four upgrades a year:

```
python3 ../scripts/carrying_cost.py ../assets/sample-request.json          # 4.1 Meridian
python3 ../scripts/carrying_cost.py ../assets/sample-request-decline.json  # 4.2 Halcyon
python3 ../scripts/carrying_cost.py ../assets/sample-request-bespoke.json  # 4.3 Kestrel
```

### 4.1 Meridian Freight — nightly close-out export (**GENERALISE**, Gate 3)

| Stream | Bespoke | Generalised | Basis |
| --- | --- | --- | --- |
| Principal | **$24,000** (96h ÷ 0.6 × $150) | **$60,000** (240h ÷ 0.6 × $150) | Written design, both variants |
| Engineering interest / yr | $9,000 (60h) | $13,200 (88h) | Maintenance 36h, incidents 14h, support 10h |
| Upgrade interest / yr | $3,000 (5h × 4) | $2,400 (4h × 4) | The general version rides the extension point |
| Renewal interest / yr | $12,000 ($240k × 0.05) | $12,000 | Watch band midpoint, exposure only |
| Year 1 · 2 · 3 carrying | $24,000 · $27,600 · $31,740 | $27,600 · $31,740 · $36,501 | 15% drift |
| **TCO(3)** | **$110k** | **$160k** | Rounded to 2 s.f. |
| Interest rate · share of ARR | **100%** · 2.4% | 46% · 2.8% | — |

The bespoke version's interest rate is exactly 100%: in year one it costs what it cost to build.
The generalised version costs 2.5× the principal and less than half the rate, which is the whole
argument for generality expressed as a number. `N_evidenced = 4.0` across four named accounts,
three at G3+, against `K* = 2` → **Gate 3 fires, outcome GENERALISE**.

### 4.2 Halcyon Distribution — bespoke SAP IDoc connector (**DECLINE**, Gate 5)

| Stream | Year 1 | Basis |
| --- | --- | --- |
| Principal | $40,000 | 160h ÷ 0.6 × $150 |
| Engineering interest | $19,800 | 100h × $150 + $4,800 middleware licence |
| Upgrade interest | $4,800 | 8h × 4 upgrades × $150 |
| Renewal interest | $9,000 | $60k at stake × 0.15 (unowned → At Risk midpoint) |
| Year 1 · 2 · 3 | $33,600 · $38,640 · $44,436 | — |
| **TCO(3)** · interest rate · **share of ARR** | **$160k** · 84% · **22.4%** | — |

Nothing about this is subtle once it is priced. The three-year total cost of ownership ($157k)
exceeds the account's entire annual ARR, and year-one carrying alone is 22.4% of it — more than
four times the commercial threshold. Gate 4 fails on three clauses at once (payback, no named maintainer, no sunset date),
Gate 5 returns **DECLINE**, and the memo carries the nearest alternative priced: the supported
flat-file path at 55% of the job for 16 hours of configuration.

### 4.3 Kestrel Health — custom approval-matrix engine (**BUILD BESPOKE**, Gate 4, revenue-contingent)

| Stream | Year 1 | Basis |
| --- | --- | --- |
| Principal | $55,000 | 220h ÷ 0.6 × $150 |
| Engineering interest | $20,100 | 134h × $150, including 12h of eval regression |
| Upgrade interest | $6,000 | 10h × 4 × $150 |
| Renewal interest | **$90,000** | $600k at stake × 0.15 |
| Year 1 · 2 · 3 | $116,100 · $133,515 · $153,542 | — |
| **TCO(3)** · interest rate · share of ARR | **$460k** · **211%** · 19.4% | — |
| Revenue trade | **$150k/yr · effective discount 25.5%** | `TCO(3) ÷ (ARR × term_years)` |

Gate 4 passes all four clauses — $600k × 1.0 savability > $460k TCO, maintainer Sam Okafor, sunset
review 2027-08-31, rollback flag-guarded inside a sprint — so the outcome is **BUILD BESPOKE**.
The interest rate of 211% is not a reason to refuse; it is a reason nobody may call this free. If
this is absorbed rather than structured, we have granted a **25.5% discount over the term** that
appears in no discount report and repeats every year the component lives. Structure it
(`saying-no.md` §4) before the build starts, not at the renewal.

---

## 5. The break-even generality threshold `K*`

`K*` is the account count at which building the general version once costs less than building the
bespoke version repeatedly. It converts "should we generalise?" from a matter of taste into a
comparison between two integers.

```
deploy_cost   = deploy_hours_per_account ÷ 0.6 × loaded_rate
bespoke_unit  = principal_bespoke + carrying_bespoke(N)
general_fixed = principal_general + carrying_general(N)

K* = ceil( (general_fixed − bespoke_unit) ÷ (bespoke_unit − deploy_cost) ) + 1
```

**Gate 3 fires when `N_evidenced ≥ K*` *and* at least two accounts sit at tier G3 or above.** Both
clauses (`productisation-path.md` §1–§2). The sum alone can be reached by four G1s, which is four
opinions with a decimal point on them.

| Case | Reading | What to do |
| --- | --- | --- |
| `bespoke_unit − deploy_cost ≤ 0` | Deploying the general version costs at least as much as building it bespoke | Generalising never pays back. Decide between bespoke and decline; the script says so rather than returning a number |
| `K* = 1` | The general version is cheaper than one bespoke build | Build the general one for this account. This is common where the bespoke path needs its own monitoring and the general path does not |
| `K* = 2–3` | The ordinary case | Fowler's rule of three is the counterweight: the third instance is where the common shape becomes visible `[P]` |
| `K* ≥ 5` | The general version carries a large fixed cost | Build bespoke now, open the debt row, and set the graduation trigger at `K*` accounts rather than generalising on hope |

**`K*` is a cost threshold, not a design argument.** Sandi Metz's rule governs the design:
*"duplication is far cheaper than the wrong abstraction"* `[P · Metz, "The Wrong Abstraction",
20 Jan 2016]`. An abstraction extracted from one instance accumulates a parameter per new caller
until nobody can change it, and the cost of that appears in `maintenance_h` two years later, where
no one connects it to the decision that caused it.

**Sensitivity to declare, and it moves in steps rather than smoothly.** `K*` is least sensitive to
the input people argue about (`build_hours`) and most sensitive to the one nobody measures
(`deploy_hours_per_account`). At Meridian, anything from 16 to 200 hours per deployment leaves
`K* = 2`; at **240 hours it becomes 3**, at 400 hours it becomes 8, and at **430 hours the
denominator goes negative** and generalising never pays back at any count. **State the flip points,
not the input.** A reviewer challenging `K*` is challenging the deployment estimate, and "K* = 2,
and it stays 2 until a deployment costs 240 hours" ends that conversation in one sentence.

---

## 6. The annual cull

Once a year, every live component is re-decided against the same gate sequence with **today's**
numbers. The commonest failure is treating the original decision as settled because it was made
carefully. **A component that cleared Gate 4 at $800k ARR does not clear it at $300k.**

| Step | Input | Test |
| --- | --- | --- |
| 1 | Today's ARR, renewal date, notice period, sponsor | Re-run Gates 0–5. Does the same gate still return the same outcome? |
| 2 | Actual carrying hours vs the estimate | Record the ratio. It is the only calibration input the next estimate gets |
| 3 | The Graduation Contract | Did the owner stay? Did the product counterpart decide by their date? A contract with a departed owner is an unowned component today |
| 4 | `N_evidenced`, re-searched | Three G3 accounts behind a bespoke build is a graduation, not a debt row |
| 5 | Usage telemetry, 90 days | Zero invocations and no ARR dependent → retire |

Each row returns exactly one disposition, with a date and a named owner:

| Disposition | Condition | Commits you to |
| --- | --- | --- |
| **Keep** | Gate 4 still passes on all four clauses | A new sunset review date ≤12 months out. Not "keep, review when convenient" |
| **Graduate** | `N_evidenced ≥ K*` with ≥2 at G3+ | The field-signal request, a named product counterpart and their decision date (`productisation-path.md` §5) |
| **Migrate** | A supported path now reaches the job | A dated cutover, an owner on each side, a rollback window, and the customer told before the change, not after |
| **Retire** | Unused 90 days, or the ARR it protected has gone | Dated notice to the customer-side owner, a rollback window, then removal from the diagram, the register, the runbook, the alerting and every credential it held |

**Every row gets a written outcome, including "keep, unchanged"** (`R14`, `C32`). An unwritten cull
decision is indistinguishable from an oversight and repeats silently for four years, which is how
components reach the point where nobody knows why they exist. Record the recovered capacity in
hours per year on every retirement — it is the only way paydown gets funded next cycle.

**The cull is where `R21` is enforced.** Every build carries an hours ceiling set at creation; a
component that has consumed its ceiling does not get the next increment as maintenance. The next
increment is a change order or a decline.

---

## 7. The debt-register row and the paydown reserve

A **Build bespoke** or **Generalise** opens a register row **the day it is approved**, not at the
next audit. Retrofitted ownership is ownership that never arrives, and undocumented context is
lost at the first holiday or reorg (`C30`). The row lives in the account's standing ledger,
`../../fde-account-plan/references/custom-work-ledger.md`.

| Field | Content | Invalid |
| --- | --- | --- |
| `component` | The name in the repo, the runbook and the alert routing — one name, everywhere | A description of the job |
| `type` | custom code · version pin · config · data · prompt/eval · knowledge · organisational | Blank |
| `account_id` · `arr_dependent` | The account and the ARR that would be exposed if it broke | A sum across components — dependencies overlap |
| `principal` | From §3, with `build_hours` and the rate that produced it | A figure with no rate attached |
| `annual_carrying` · `interest_rate` · `share_of_arr` | All three, from §3 | Any one of them alone |
| `owner` | **A named person.** They are paged when it breaks | A team, a rota, a squad name |
| `hours_ceiling` (`R21`) | The cumulative maintenance hours after which the next increment is a change order | Absent |
| `sunset_review_date` | A calendar date ≤12 months out, set at creation | "When product ships it" |
| `graduation_trigger` | The observable event that makes this a product requirement — default: a third account at G3+ | "When it makes sense" |
| `decision_record` | Link to the memo: gate, `N_evidenced`, `K*`, the nine scores, the falsifier | Absent — the decision is then re-litigated from memory |

**The paydown reserve: 15–20% of delivery capacity, against usable hours** (`R13`) `[P]`. Debt with
no reserved capacity is a list, not a plan. On a four-engineer delivery team that is roughly three
engineer-days a week, and it is the first thing cut in a quarter with a launch in it — which is
exactly the quarter in which the register grows fastest.

**Refresh cadence:** quarterly, and before every renewal. The ratio moves when ARR contracts, not
only when the register grows — the same $34k of carrying is 3.5% of ARR at $980k and 22% at $150k.

---

## 8. Pricing by business model

Resolve the profile first (`../../cs-context/references/business-model-profiles.md`).

| Model | What changes in the arithmetic |
| --- | --- |
| **Enterprise annual** | The standard shape. `arr_at_stake` is the contracted ARR that depends on the component; the decision window is `renewal_date − notice_period_days − evidence_window` (`R1`) |
| **Consumption / usage-based** | Price carrying **per unit of throughput as well as per year**, and print a 10× volume row. A bespoke path at $0.004 a call is $40/month at pilot volume and $4,000/month in production. Replace `arr_at_stake` with committed spend or trailing 90-day revenue |
| **Product-led / self-serve** | There is no services fee, no notice period and no account team to carry it, so `renewal_interest` has no band to sit in and the engineering stream has no owner. Carrying cost is effectively infinite against a single account's revenue; the default outcome is **Decline** with a configuration answer |
| **Monthly evergreen** | No notice period, so the decision window is the next billing cycle. A horizon above one year needs a written reason, because the customer can leave in 30 days and the component cannot |
| **Regulated vertical** | `eval_regression_h` and `third_party_cost_per_year` are materially higher — validation evidence, audit trails, retention. Residency and retention requirements are usually **general**, so search the base before pricing a bespoke build (`productisation-path.md` §2) |
| **Channel / partner-delivered** | The maintainer may sit at a partner you cannot page. No named human at the partner fails Gate 4 clause 2, whatever the arithmetic says. Where a partner does own it, price the coordination hours into `support_h` |

---

## 9. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Pricing the build and calling it the cost | The principal is the deposit. Price all three streams over the stated horizon, or the memo has answered a different question |
| Nominal hours | `R13`. Hours convert at ~60% usable. A 96-hour build is 160 hours of somebody's calendar |
| A one-year horizon "because we can revisit it" | Maintenance is ~60% of lifecycle cost `[A · Glass]`. One year books the deposit and a fraction of the loan, and it flips Gate 4 the wrong way |
| Renewal exposure written as a churn probability | `R22`. It is `arr_at_stake × band_uplift`, labelled exposure. A rules-based score with a percentage on it is a fabricated number with a decimal point |
| `third_party_cost_per_year = 0` because the pilot was free | Price at production volume. Per-call fees are invisible at pilot scale and material at 10× |
| An owner who is a team | A team is not paged and does not answer a schema change. Name a person, or Gate 4 fails |
| "We'll clean it up after the renewal" | The debt is heaviest exactly when the renewal is being decided. That is the argument for paying it before |
| A composite stated to the dollar | Two significant figures. `$110k`, not `$107,340` — the precision implies a measurement nobody took |
| The cull that skips the healthy rows | Every live row returns a written disposition, "keep, unchanged" included (`R14`, `C32`) |
| Sending the carrying cost or the interest rate to the customer | `R18`. It never crosses the divider, not softened, not translated, not as "the cost of supporting this" |
