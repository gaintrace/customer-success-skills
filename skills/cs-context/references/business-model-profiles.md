# Business Model Profiles

> The fastest way to sound like you have never worked in customer success is to talk about
> champions, QBRs and executive sponsors to a company selling a $49/month self-serve product —
> or to score a consumption business on seat utilisation, which it does not sell.
>
> This file encodes what actually differs. Read the profile matching the company before any
> analysis, and apply the **"does not apply here"** column as seriously as the rest. Knowing
> which standard CS practice is irrelevant to a given model is most of what domain expertise is.

**Contents**
- [The six axes](#the-six-axes)
- [Pricing and packaging](#axis-1--pricing-and-packaging)
- [Go-to-market motion](#axis-2--go-to-market-motion)
- [Buyer and user](#axis-3--buyer-and-user)
- [Deployment](#axis-4--deployment)
- [Vertical and regulation](#axis-5--vertical-and-regulation)
- [Contract shape](#axis-6--contract-shape)
- [Composite profiles](#composite-profiles)
- [What changes downstream](#what-changes-downstream)
- [Cross-model traps](#cross-model-traps)

---

## The six axes

A company is a point in six dimensions, not one label. "B2B SaaS" tells you almost nothing;
"seat-based, sales-led, department-buyer, multi-tenant, horizontal, annual with 30-day notice"
tells you what every skill in this library should do.

| Axis | Options |
| --- | --- |
| **1. Pricing** | per-seat · consumption/usage · flat tier · hybrid (platform fee + usage) · per-transaction · outcome-based |
| **2. Motion** | sales-led · product-led · hybrid · partner/channel-led |
| **3. Buyer** | developer · practitioner · department head · enterprise exec · SMB owner · procurement-mediated |
| **4. Deployment** | multi-tenant SaaS · single-tenant · self-hosted/on-prem · embedded/API · hardware+software |
| **5. Vertical** | horizontal · regulated (health, financial, public sector, defence) · industry-specific |
| **6. Contract** | monthly evergreen · annual · multi-year · committed spend with drawdown · pay-as-you-go |

---

## Axis 1 — Pricing and packaging

### Per-seat

| | |
| --- | --- |
| **Churn looks like** | Seat reduction first, logo loss second. Contraction is the leading edge of churn, not a separate event |
| **The signal that matters most** | Licence utilisation (`active_users_30d / seats_purchased`) and its trend |
| **Expansion motion** | Seat growth, tier upgrade, new department |
| **Activation** | A user reaching the core action in their first N days; measured per user, rolled to account |
| **Does not apply** | Consumption pacing, commitment drawdown, overage conversations |
| **The trap** | Treating a healthy utilisation ratio as health. 95% utilisation on 20 seats when 200 people could use it is a rollout failure wearing a good number |

### Consumption / usage-based

| | |
| --- | --- |
| **Churn looks like** | **Commitment shortfall**, not logo loss. The customer keeps the contract and consumes less. Then they renegotiate down. Logo churn is the last act, often a year later |
| **The signal that matters most** | Consumption pacing against commitment: `consumed_to_date / (commitment × elapsed_term_fraction)`. Below 0.7 at the halfway mark is a renewal problem already in motion |
| **Second signal** | Consumption *concentration* — one workload carrying the account is a single point of failure. Breadth of workloads beats total volume |
| **Expansion motion** | Commitment increase at renewal, new workloads, new teams, higher-tier capabilities. Overage is a *conversation*, not a win — repeated overage means the commitment was mis-sized |
| **Activation** | First production workload, not first API call |
| **Does not apply** | Seat utilisation. Per-seat expansion math. "Licences unused" framing |
| **The trap** | Reading a usage spike as health. A batch job, a migration or a one-off backfill inflates volume and tells you nothing about recurring demand. Always separate recurring from episodic consumption |
| **Second trap** | Measuring NRR monthly. Consumption is seasonal and lumpy; use TTM or the comparison is noise |

### Flat tier

| | |
| --- | --- |
| **Churn looks like** | Silent non-use, then non-renewal. Very little warning in commercial data |
| **The signal that matters most** | Depth of core-action usage and breadth of feature adoption — there is no seat or volume signal to lean on |
| **Expansion motion** | Tier upgrade, add-on modules, multi-entity |
| **Does not apply** | Utilisation ratios, overage, drawdown |
| **The trap** | Thin signal coverage. Flat-tier businesses have the least commercial telemetry, so product usage and relationship signals must carry more weight — and if product analytics is not instrumented, honest confidence is Low |

### Hybrid (platform fee + usage)

The common enterprise shape and the most misread. Score the **platform fee** as per-seat/flat
and the **usage component** as consumption, then take the worse of the two. A customer paying
the platform fee while consumption collapses is not healthy; they are paying rent on something
they stopped using, and that is a renewal that fails at the budget review.

### Per-transaction / outcome-based

| | |
| --- | --- |
| **Churn looks like** | Volume decline that mirrors *their* business, not their opinion of you |
| **The signal that matters most** | Your share of their transaction volume, if knowable. Absolute volume conflates their growth with your health |
| **Does not apply** | Most adoption framing — the customer's own demand drives the number |
| **The trap** | Treating a volume decline as dissatisfaction when their end market shrank. Always check whether the decline is idiosyncratic or sector-wide before opening a risk record |

---

## Axis 2 — Go-to-market motion

### Sales-led

Champions, executive sponsors, QBRs, procurement and multithreading are all real and all
load-bearing. The relationship family carries genuine weight. Notice periods exist. This is the
motion every generic CS article assumes.

### Product-led

| | |
| --- | --- |
| **Reality** | There is frequently **no champion, no exec sponsor and no QBR**, and inventing them produces absurd output |
| **The unit of relationship** | The individual user, then the team, then — only for accounts that cross a threshold — a buyer |
| **Signals that dominate** | Product usage, activation, billing (card failures are material), in-app behaviour, seat/workspace invites |
| **Signals that barely exist** | Exec sponsor engagement, QBR cadence, multithreading depth, procurement posture |
| **Churn mechanics** | Self-serve, instantaneous, no notice period. Detection must be **pre-emptive**, in days not quarters |
| **Involuntary churn** | Material, unlike enterprise. Card expiry, failed payments and dunning are a real share of loss and are the cheapest thing to fix |
| **Where CS actually intervenes** | In-product, automated, at the moment of friction — plus a human motion only for accounts above a value threshold or showing an expansion signal |
| **The trap** | Running enterprise plays on a PLG book. A QBR invitation to a $99/month account reads as a mistake, and the CSM hours spent on it were the wrong hours |

### Hybrid

The realistic case for most companies above $20M ARR: PLG acquisition with a sales-assisted
motion above a threshold. Score the **self-serve tail** on the PLG profile and the **assisted
segment** on sales-led. The most common error is one policy for both — the tail gets attention
it cannot repay and the enterprise accounts get a digital touch they resent.

### Partner / channel-led

| | |
| --- | --- |
| **Reality** | You may have **no direct relationship and no direct telemetry**. The partner owns the customer |
| **Signals that dominate** | Partner-reported health, partner engagement, deal registration, partner enablement level |
| **What is often absent** | End-customer usage, end-customer contacts, renewal date visibility |
| **The trap** | Scoring an account on data you do not have. If the partner holds the relationship, your Coverage Ledger is genuinely 2/7 and your confidence is Low — say so rather than producing a confident read on a customer you have never spoken to |

---

## Axis 3 — Buyer and user

| Buyer | What they respond to | What fails |
| --- | --- | --- |
| **Developer** | Precision, docs, changelogs, API stability, no marketing language. Peer proof over vendor proof | Any adjective. "Exciting", "seamless", "powerful" cause instant discount of everything else |
| **Practitioner** | Time saved on the task they actually do; a screenshot of their own workflow | Strategic framing they have no authority over |
| **Department head** | Team throughput, their own visibility upward, a number for their review | Feature depth |
| **Enterprise exec** | Business outcome, risk, consolidation, peer benchmarks. Half the length | Product detail of any kind |
| **SMB owner** | Money and time, this month. Payback measured in weeks | Anything requiring a project plan |
| **Procurement-mediated** | Terms, precedent, comparables, process | Relationship warmth — they are optimising a different objective |

When user and buyer differ — the common enterprise case — **the buying team's usage is the
signal that matters**, not the aggregate. This is the Buyer disconnect pattern, and it is the
most frequent cause of a green score on an account that does not renew.

---

## Axis 4 — Deployment

| Deployment | What changes |
| --- | --- |
| **Multi-tenant SaaS** | The default assumptions of this library hold |
| **Single-tenant** | Version drift is a risk family of its own. A customer two versions behind is unsupported and expensive, and upgrade consent becomes a renewal dependency |
| **Self-hosted / on-prem** | **You may have no usage telemetry at all.** Coverage is structurally low; lean on support volume, licence-key checks, version reporting, and relationship signals. Never fake a usage read. Renewal risk concentrates in upgrade fatigue and internal ownership change |
| **Embedded / API** | Your health is a function of *their* product's health. If their product loses users, you lose volume for reasons unrelated to you. Track their release cadence and their market |
| **Hardware + software** | Physical install base, RMA rates, field service and end-of-life schedules become risk signals. Refresh cycles drive renewals more than satisfaction does |

---

## Axis 5 — Vertical and regulation

| Context | What changes |
| --- | --- |
| **Horizontal** | Library defaults hold |
| **Healthcare / life sciences** | HIPAA/BAA, validation and change-control cycles. Security review is a **renewal-timeline dependency measured in months**, not a formality. Clinical seasonality is real |
| **Financial services** | Vendor risk management, SOC 2 / ISO evidence cycles, exit-plan requirements, concentration-risk reviews. Procurement is powerful and process-bound. Budget cycles are rigid |
| **Public sector / defence** | Fiscal-year use-it-or-lose-it dynamics, tender and re-compete cycles, FedRAMP/IL levels, and renewal by procurement vehicle rather than by relationship. A great relationship does not survive a lost re-compete |
| **Education** | Academic-calendar seasonality dominates. Summer usage collapse is normal and must be masked, not scored |
| **Retail / e-commerce** | Peak-season freeze windows. No change gets approved from November to January, and a renewal that lands in that window must be closed before it |
| **Regulated generally** | Security review, DPIA, penetration-test evidence and insurance certificates carry **weeks to months** of lead time. Missing them is the most common avoidable renewal slip in these verticals |

---

## Axis 6 — Contract shape

| Shape | Renewal mechanics | The governing date |
| --- | --- | --- |
| **Monthly evergreen** | Cancel any time, instantly. No notice period | There is no opt-out deadline — **every day is the deadline**. Score continuously on short windows |
| **Annual** | Notice period, auto-renew flag, procurement | `renewal_date − notice_period_days` |
| **Multi-year** | Long silence between decisions; risk accumulates invisibly and the relationship often dies before the renewal | Start two quarters earlier than annual. Mid-term reviews are the only defence |
| **Committed spend with drawdown** | The renewal is a *re-commitment* negotiation. Under-consumption is the whole conversation | Pacing at the two-thirds mark of the term, not the renewal date |
| **Pay-as-you-go** | No renewal event at all. "Churn" is a trailing-window definition you must choose and state | Define it explicitly in `cs-context` §2 or every metric is unreproducible |

---

## Composite profiles

Four common shapes, as a shortcut. Anything else, compose from the axes.

| Profile | Axes | Weight profile | Signals that dominate | Practices that do **not** apply |
| --- | --- | --- | --- | --- |
| **Enterprise seat SaaS** | per-seat · sales-led · dept/exec buyer · multi-tenant · annual | `enterprise` | Commercial, relationship, buying-team usage | — |
| **PLG self-serve** | per-seat or flat · product-led · practitioner · multi-tenant · monthly | `plg` | Product usage, activation, billing/dunning | QBRs, exec sponsors, multithreading, notice periods, procurement |
| **Consumption platform** | usage or hybrid · sales-led or hybrid · developer/dept · multi-tenant · committed drawdown | `consumption` | Consumption pacing, workload breadth, technical integration health | Seat utilisation, licence-based expansion math |
| **Regulated enterprise** | per-seat or hybrid · sales-led · procurement-mediated · single-tenant or SaaS · multi-year | `enterprise` | Commercial, security/compliance calendar, exec sponsor, version state | Fast-moving expansion plays; anything assuming a short paper process |

---

## What changes downstream

Once the profile is set, it drives these — record the decisions in `cs-context`:

| Downstream | Driven by |
| --- | --- |
| Risk weight profile | Pricing + motion (`enterprise` / `plg` / `consumption`) |
| The activation event | Pricing + buyer (first production workload vs first report published vs first invite) |
| The primary adoption metric | Pricing (utilisation vs pacing vs depth) |
| Whether relationship signals are scored at all | Motion (near-zero weight in pure PLG) |
| The renewal timeline and its governing date | Contract shape |
| Paper-process lead times | Vertical + deployment |
| QBR cadence and whether QBRs exist | Motion + segment |
| Expansion motion and sizing math | Pricing |
| What "churn" means, precisely | Contract shape |
| Seasonality masks | Vertical |
| Coverage Ledger realism | Deployment (on-prem and channel structurally cap it) |

---

## Cross-model traps

The specific mistakes that reveal an analysis was written from a template.

| Trap | Why it is wrong |
| --- | --- |
| Seat utilisation on a consumption business | They do not buy seats. The equivalent is commitment pacing |
| QBR cadence for a $99/month PLG account | The meeting costs more than the account contributes, and the invitation reads as a mistake |
| "No exec sponsor" as a risk flag in PLG | There was never going to be one. Scoring its absence manufactures risk |
| Opt-out deadline on a monthly evergreen contract | There is no notice period; the whole timeline framing collapses |
| Usage decline as risk during an academic summer or a retail freeze | Seasonal, and scoring it burns credibility with the CSM who knows better |
| Volume decline as dissatisfaction in a transaction business | Their market moved. Check the sector before opening a risk record |
| Confident health scores on a self-hosted or channel account | You do not have the telemetry. Coverage is 2/7 — say so |
| Treating overage as an expansion win | Repeated overage means the commitment was mis-sized, and the customer is about to renegotiate it downward |
| Applying a single NRR definition across seat and consumption lines | They are different denominators. Report separately or the blend is meaningless |
| Expansion plays inside a regulated security-review window | The paper process cannot absorb it; you will stall the renewal you were trying to grow |
| One coverage model across a hybrid book | The self-serve tail gets hours it cannot repay; the enterprise accounts get a digital touch they resent |
