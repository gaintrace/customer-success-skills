# The Custom-Work Ledger

> Everything built for one customer that is not product, priced in dollars per year, with a name
> against it and a plan to productise or retire it. This is the debt that quietly makes an account
> unrenewable — or renewable at a margin nobody would have agreed to up front.
>
> Evidence labels: `[M]` measured · `[V]` vendor research · `[P]` practitioner standard ·
> `[A]` academic, standards body or regulation.

**Contents**
- [Why the ledger exists](#why-the-ledger-exists)
- [Discovery — the seven hiding places](#discovery--the-seven-hiding-places)
- [Taxonomy: seven kinds of deployment debt](#taxonomy-seven-kinds-of-deployment-debt)
- [Pricing: principal and interest](#pricing-principal-and-interest)
- [A worked ledger](#a-worked-ledger)
- [Disposition](#disposition)
- [The productisation path](#the-productisation-path)
- [Retiring something](#retiring-something)
- [Saying no to a custom build](#saying-no-to-a-custom-build)
- [Escalating a real product gap](#escalating-a-real-product-gap)
- [Governance](#governance)
- [Anti-patterns](#anti-patterns)

---

## Why the ledger exists

Deployment debt differs from product debt in three ways that make it more dangerous and less
visible: **it runs on someone else's infrastructure**, often outside your CI and your monitoring;
**it has no backlog**, because it was never a ticket; and **it surfaces at the renewal**, as a
margin conversation or an upgrade that cannot happen, rather than as a build failure.

Ward Cunningham's 1992 metaphor is exact and worth using literally: shipping code that does not
match your understanding of the domain is borrowing, and every hour later spent working around it
is interest `[P]`. Martin Fowler's quadrant adds the distinction that matters in the field —
whether the debt was taken **deliberately or inadvertently**, and whether it was **prudent or
reckless** `[P]`. Most deployment debt is deliberate and prudent at the moment of creation ("we
ship the connector or we miss go-live") and becomes reckless purely by remaining unowned.

The role's second success axis — operating leverage, patterns reused across deployments — is
measured here and nowhere else. An engineer with high customer impact and zero leverage is running
a consultancy inside a software company `[D · Palantir, OpenAI and Anthropic forward-deployed job
postings, fetched 2026-08-27]`.

## Discovery — the seven hiding places

Walk all seven, every time, and **print the negatives**. "No scripts outside version control,
verified against the deploy history 2026-08-26" is a finding a successor needs; silence is not.

| # | Hiding place | How to find it | What it usually turns out to be |
| --- | --- | --- | --- |
| 1 | Pilot-era code still in production | Repo search by account name; deploy history predating go-live | An interim connector written to unblock a date |
| 2 | Scripts on a laptop or a personal cloud account | Ask every engineer who has touched the account, **by name**; check scheduled jobs with no repo | A weekly reconciliation someone runs by hand |
| 3 | Hand-edited production config | Diff live config against the declared baseline | Feature flags, limits and mappings set during an incident |
| 4 | Undocumented transformations | Compare source schema against the fields their reports consume | Business logic living in a view or a mapping file |
| 5 | Pinned versions and pinned model snapshots | Version headers, SDK user agents, config pins | A pin added to stop a regression, never revisited |
| 6 | Hand-tuned prompts and evals with no regression gate | Prompt store, eval history, last regression-run date | Behaviour tuned by hand that a model change silently breaks |
| 7 | Reports and dashboards built once and never owned | BI workspace audit by creator and last-modified | A dashboard for a steering group that stopped meeting |

**The question that finds the rest:** ask every engineer who has ever worked this account, "what
would break if you were unavailable for a month?" The answer is the ledger's missing rows, and it
is also the bus-factor input for `technical-risk.md`.

## Taxonomy: seven kinds of deployment debt

| Type | Concrete example | Detection | Standard remedy |
| --- | --- | --- | --- |
| **Custom code** | One-off connector written during the pilot, still in production, unowned | Inventory with owner, last-modified, test coverage | Assign an owner and a sunset date; migrate to the supported path |
| **Version** | Three releases behind; a deprecated API still called; a pinned model snapshot | Version drift against the sunset calendar | Dated upgrade plan with a **named customer-side owner** and a window |
| **Config** | Hand-edited production config; a snowflake environment | Config diff against a declared baseline | Move to config-as-code; codify the diff first |
| **Data** | Undocumented transformations, schema drift, broken lineage, stale mappings | Schema-drift monitor; lineage audit | Contract-test the schema; document the lineage |
| **Prompt / eval** | Prompts tuned by hand, no eval suite, a model upgrade changes behaviour silently | Regression run on every model or prompt change | Golden dataset from their real distribution, regression gate, rollback trigger |
| **Knowledge** | One engineer understands the deployment | Bus factor computed from authorship and incident history | Runbook, recorded walkthrough, a second engineer on the rota |
| **Organisational** | The champion left; nobody on their side owns the integration | Stakeholder-map staleness | Re-anchor with a named owner, or plan the wind-down |

## Pricing: principal and interest

```
build_cost (principal) = build_hours × loaded_hourly_rate

annual_carrying (interest)
    = (maintenance_hours + incident_hours + upgrade_tax_hours × upgrades_per_year)
      × loaded_hourly_rate
    + third_party_cost_per_year

interest_rate          = annual_carrying ÷ build_cost
carrying_share_of_arr  = Σ annual_carrying ÷ account_arr
```

| Input | Where it comes from | The trap |
| --- | --- | --- |
| `build_hours` | Time tracking, or the delivery plan | Reconstructed after the fact is fine; say so |
| `maintenance_hours` | The engineer's own estimate, per year | Ask for a monthly number and multiply — annual estimates are compressed |
| `incident_hours` | Ticket and incident time attributed to this component | The number people underestimate most |
| `upgrade_tax_hours` | Hours this component adds to each platform upgrade | The reason a deployment stops upgrading |
| `upgrades_per_year` | Your release cadence, not theirs | |
| `third_party_cost_per_year` | Licences, infrastructure, per-call fees | |
| `loaded_hourly_rate` | `cs-context`; if absent, **assume and record it** | A guessed rate moves the 5% threshold — put it in the Assumptions table |

Run `../scripts/custom_work_ledger.py`; it applies this model and the disposition rules below.

**An interest rate above 100% means the component costs more every year than it cost to build.**
That is not automatically wrong — a component carrying $600k of ARR can justify it — but it is
always a decision, and it is a decision someone must have made on purpose.

## A worked ledger

From `../assets/sample-custom-work.json`, at a $150/hr loaded rate against $980k ARR:

| Item | Build | Carrying $/yr | Interest | Others | Disposition |
| --- | --- | --- | --- | --- | --- |
| Carrier EDI normaliser | $30,000 | $29,550 | 98% | 7 | **Productise** |
| Exception-triage prompts and evals | $13,500 | $21,300 | 158% | 3 | **Generalise** |
| WMS reconciliation connector | $18,000 | $18,900 | 105% | 1 | **Own it** |
| Account-code mapping file | $2,400 | $11,700 | 488% | 0 | **Migrate** |
| Legacy SFTP listener | $6,000 | $5,550 | 93% | 0 | **Retire** |
| Depot throughput dashboard | $3,600 | $1,500 | 42% | 0 | **Retire** |
| **Total** | **$73,500** | **$88,500 (9.0% of ARR)** | | | |

Read it in this order. The **488%** row is the cheapest thing to fix and the most expensive thing
to keep — a $2,400 build costing $11,700 a year because a hand-maintained file gates every finance
report. The **7-other-customers** row is not debt at all, it is a product requirement that has been
mis-filed as delivery work for a year. And **9.0% of ARR** puts the whole ledger over the
commercial threshold, so the disposition plan goes to the account owner this week rather than into
next quarter's engineering backlog.

## Disposition

Take the first row that matches. The rules are ordered so that leverage beats convenience.

| Condition | Disposition | What it commits you to |
| --- | --- | --- |
| ≥5 other customers hit the same problem | **Productise** | A field-signal writeup to product, an owner there, and a dated decision — not a promise to the customer (`R19`) |
| 2–4 other customers | **Generalise** | One shared template or reference implementation owned by delivery, and the second deployment uses it |
| 0–1 others · a supported path exists · ARR depends on it | **Migrate** | A dated cutover, a named owner on each side, and a rollback window |
| 0–1 others · no supported path · ARR depends on it | **Own it** | A named maintainer, tests, a runbook entry, a sunset review date, and the carrying cost in the renewal margin conversation |
| Unused 90 days · no ARR depends on it | **Retire** | A dated notice, a rollback window, and removal from the risk register |

**The commercial threshold.** Total annual carrying cost above **5% of the account's ARR** makes
disposition a commercial decision rather than an engineering one: it goes to the account owner that
week and into the renewal margin conversation. A library convention `[P]`, not a measured
benchmark. It sits low because services attached to a subscription are structurally unprofitable —
TSIA reports project-based services at product companies averaging gross margins in the mid-30s
with best-in-class in the high 40s, while the TSIA Cloud 40 companies that break out
project-services margins average **−9%** (TSIA, published 2023 on Q3-2022 data) `[V]`.

**Capacity for paydown.** Reserve 15–20% of delivery capacity for it, and plan against usable hours
rather than nominal ones — roughly 60% of a week survives meetings, interrupts and escalations
(`R13`) `[P]`. A paydown plan with no reserved capacity is a list, not a plan.

## The productisation path

The deliverable is not "we told product about it". It is a field-signal writeup they can act on:

| Section | Content |
| --- | --- |
| The problem, in the customer's words | Quoted, not paraphrased |
| Which customers hit it | Named, with ARR and renewal dates |
| What we built, and what it cost | Build hours, carrying cost, interest rate |
| The general shape | The abstraction that would serve all of them, not this customer's version |
| What it unblocks | ARR that stops being contingent on a bespoke path |
| What we will do if product declines | The honest fallback, with its carrying cost |

**"If it is the third time you have built it, it is a product requirement, not a customisation."**
The write-up is then the deliverable, and the delivery estimate is the evidence.

## Retiring something

Retirement is the only disposition that removes a risk-register row permanently, and it is the one
most often skipped because it feels like it needs permission.

1. **Prove it is unused** — no invocations in 90 days, and no dependency in config or code.
2. **Name what would break if you are wrong**, and check that specific thing.
3. **Give dated notice** to the customer-side owner. Never remove something silently, even if the
   telemetry says nobody uses it; someone's quarterly process may be the exception.
4. **Keep a rollback window** — disable first, delete after the window.
5. **Remove it everywhere**: the diagram, the ledger, the risk register, the runbook, the alert
   routing, and any credential it held.
6. **Record the recovered capacity** in hours per year. It is the only way paydown gets funded next
   quarter.

## Saying no to a custom build

The most valuable sentence in the role, and the least practised. Three parts, in this order, and
none of them optional:

1. **The decision, first.** "We're not going to build that."
2. **The reason, in their interest.** "It would sit outside the upgrade path and break the first
   time either side changed a schema — you'd be carrying that, not us."
3. **The nearest thing we can do**, specifically, with what it costs them.

What makes it fail: burying it under context, offering it to the roadmap to soften the moment
(`R19` — never commit a date you do not own), or making the reason internal ("it's not on our
roadmap"). "It's on the roadmap" when it is not is the kindest-sounding sentence in customer
success and the most damaging.

**A no belongs in a conversation where you are not also delivering bad news or asking for
something (`R11`).** Say it in its own moment, in writing afterwards, once.

The refusal that crosses to the customer is in `../assets/customer-technical-note.md`. What never
crosses: the carrying cost, the interest rate, the disposition word, and any comparison to another
customer (`R18`).

## Governance

| Practice | Cadence | Why |
| --- | --- | --- |
| Every custom artifact gets an owner and a sunset review date **at creation** | At creation | Retrofitting ownership is how items become unowned permanently |
| Ledger refresh | Quarterly, and before every renewal | The ratio moves when ARR contracts, not only when the ledger grows |
| Carrying cost into the renewal brief | Every renewal | Unpaid deployment debt is a commercial risk, not an engineering one |
| Paydown reserve | 15–20% of delivery capacity `[P]` | Debt without reserved capacity is never paid |
| Written skip | Quarterly (`R14`) | An undeclared deferral is indistinguishable from an oversight and repeats for four quarters |

## Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| A ledger with no dollar figures | Price every row; an unpriced ledger loses every argument against a feature request |
| Counting build cost and calling it debt | Build cost is the principal; the carrying cost is what recurs and what decides |
| Summing `arr_dependent` across items | Dependencies overlap — report the largest single dependency, not a sum |
| "We'll clean it up after the renewal" | Debt is heaviest exactly when the renewal is being decided; that is the argument for paying it before |
| Building it because the customer is large | Size justifies **owning** it explicitly with a maintainer and a sunset date; it never justifies leaving it unowned |
| Forking the product | Extension points have an upgrade path and a support contract; a fork has neither |
| An owner who is a team, not a person | A team is not paged; a person is |
| Retiring silently because telemetry says it is unused | Dated notice, rollback window, then delete |
| Treating a hand-tuned prompt set as configuration | It is code with no tests until a golden dataset and a regression gate exist |
