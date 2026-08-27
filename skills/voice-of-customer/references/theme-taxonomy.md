# Theme Taxonomy and Coding Rules

> Free text becomes comparable only when it is coded against a closed, versioned taxonomy. This
> file holds the record format, the starter taxonomy, the coding rules, the split/merge tests,
> the versioning protocol, and the reliability check that makes trend claims defensible.

**Contents**
1. [Why closed, and why versioned](#1-why-closed-and-why-versioned)
2. [The `feedback_mention` record](#2-the-feedback_mention-record)
3. [Starter taxonomy](#3-starter-taxonomy)
4. [Coding rules](#4-coding-rules)
5. [Severity and polarity](#5-severity-and-polarity)
6. [The split test and the merge test](#6-the-split-test-and-the-merge-test)
7. [Versioning — adding, renaming, deprecating a code](#7-versioning)
8. [Inter-coder reliability](#8-inter-coder-reliability)
9. [LLM-assisted coding](#9-llm-assisted-coding)
10. [Common coding failures](#10-common-coding-failures)

---

## 1. Why closed, and why versioned

An open taxonomy — codes invented as you go — produces a readout that cannot be compared to last
quarter's. Every trend claim in a VoC programme depends on the code set being stable across the
comparison window, so the taxonomy is a **schema**, governed like one: versioned, documented,
changed only at period boundaries, and recoded deliberately when it changes.

A fixed taxonomy has an obvious weakness: customer language drifts, products change, and a code
set frozen in 2024 will misfile 2026 feedback. The vendor answer to this is an *adaptive*
taxonomy — Enterpret frames it as themes that "evolve with your product so answers don't change
every time" `[V]`. The operating compromise this skill uses:

| Layer | Stability | Change window |
| --- | --- | --- |
| **Category** (12) | Frozen for at least a year | Annual review only |
| **Theme** (40–80) | Stable within a year | Additions and deprecations at period boundaries, with a version bump |
| **Sub-theme** (free) | Fluid | Any time — sub-themes are for drill-down, never for trend lines |

Trend lines are drawn at category and theme level only. Never at sub-theme level: that is where
the drift lives.

---

## 2. The `feedback_mention` record

This is a **derived coding layer** over the normalised schema in
`../../cs-context/references/normalized-schema.md`. It introduces no new source of truth — every
mention points back to an existing entity.

| Field | Type | Maps to / notes |
| --- | --- | --- |
| `mention_id` | string | Generated |
| `account_id` | string | `account.account_id` — the grain of every downstream decision |
| `contact_id` | string | `contact.contact_id`; null for anonymous survey or review sources |
| `contact_role` | enum | `contact.role` — `economic_buyer` `champion` `admin` `power_user` `user` etc. Drives weighting in ranking |
| `source_entity` | enum | `interaction` · `ticket` · `opportunity` · `churn_event` — which normalised entity this came from |
| `source_ref` | string | `interaction.interaction_id`, `ticket.ticket_id`, `opportunity.opportunity_id`, or `account_id` for `churn_event` |
| `channel` | enum | `nps` `csat` `ces` `in_app` `ticket` `call` `email` `slack` `community` `review` `cab` `exit_interview` `win_loss` `sales_loss` |
| `occurred_at` | timestamp | Event time, not import time. Staleness is computed from this |
| `verbatim` | text | The customer's words, unedited. Truncation is allowed; paraphrase is not |
| `primary_code` | string | Exactly one theme code. Non-null |
| `secondary_codes` | array | Zero or more. Never counted in ARR attribution |
| `severity` | int 1–3 | §5 |
| `polarity` | enum | `complaint` `request` `praise` `neutral_observation` |
| `taxonomy_version` | string | The version this was coded against |
| `coder` | string | Human name or model identifier — an LLM coder is named like any other coder |
| `coded_at` | timestamp | |
| `in_reliability_sample` | bool | Marks the double-coded sample (§8) |
| `loop_closed_at` | timestamp | Populated by the inner loop; null until closed |

**Join for attribution:** `feedback_mention.account_id → account.arr, account.segment` and
`→ subscription.renewal_date, notice_period_days` for the opt-out exposure column.

---

## 3. Starter taxonomy

Twelve categories. Use these as-is unless the company's product makes one meaningless; renaming
categories breaks comparability with every other company you might benchmark against and with
your own history.

| Code | Category | Scope | Default route |
| --- | --- | --- | --- |
| **ONB** | Onboarding & time-to-value | Everything between contract signature and first realised value | CS |
| **ADP** | Adoption & usability | The product does it, and it is hard to do | Product (Design) |
| **CAP** | Capability gap | The product does not do it at all | Product |
| **REL** | Reliability & performance | Uptime, latency, data accuracy, regressions | Engineering |
| **INT** | Integrations & data flow | Connectors, APIs, sync fidelity, webhooks | Product (Platform) |
| **SUP** | Support experience | Response, resolution, competence, continuity | Support |
| **PRC** | Pricing, packaging & terms | What things cost and what sits in which plan | Pricing |
| **BIL** | Billing operations | Invoicing, payment, procurement mechanics, tax | Finance |
| **ADM** | Administration, security & compliance | Permissions, SSO, audit, certifications, data residency | Product (Platform) |
| **REP** | Reporting, analytics & export | Getting data and insight back out | Product |
| **ACC** | Account management & relationship | Coverage, continuity, responsiveness, commitments | CS |
| **ROI** | Value & business case | Whether the outcome bought was achieved and can be evidenced | CS |

### Theme codes

Each row is a publishable definition. **Inclusion** and **exclusion** examples are mandatory —
without an exclusion example a code will absorb its neighbours within two periods.

| Code | Theme | Definition | Inclusion example | Exclusion example → goes to |
| --- | --- | --- | --- | --- |
| ONB-01 | Implementation ran long | Go-live slipped past the agreed date for reasons on either side | "We signed in January and were not live until May" | "Our own IT blocked the security review" → still ONB-01, note cause |
| ONB-02 | Never fully deployed | Contracted scope was never provisioned or rolled out | "Only two of five teams ever got access" | Low usage after full rollout → ADP-01 |
| ONB-03 | Training and enablement gap | Users were not equipped to use what was deployed | "Nobody showed the analysts how to build a view" | Documentation could not be found → REP-04 / docs |
| ONB-04 | Handover from Sales lost context | What was sold was not what was configured | "We had to re-explain our use case three times" | A capability was never sold → CAP-* |
| ADP-01 | Core workflow is too many steps | The task can be done, and the path is long | "It takes nine clicks to publish" | The task cannot be done → CAP-* |
| ADP-02 | Learnability / new-user drop-off | New users cannot get productive without help | "Every new joiner needs a session with us" | Existing users are productive → not this |
| ADP-03 | Navigation and findability | The capability exists and users cannot find it | "We didn't know that screen existed" | The capability is absent → CAP-* |
| ADP-04 | Mobile / offline access | Work needs to happen away from the desktop app | "Our field team can't use it on site" | Desktop performance → REL-02 |
| CAP-01 | Missing capability on the value path | Absent capability blocks the use case in the original business case | "We bought this to do X and it cannot do X" | A nice-to-have request → CAP-04 |
| CAP-02 | Capability exists but is gated by plan | It exists, they cannot reach it at their tier | "It's in Enterprise and we're on Growth" | Genuinely absent → CAP-01. **Route to Pricing, not Product** |
| CAP-03 | Scale / volume ceiling | Works at their old size, not their current one | "It times out above 50k rows" | Intermittent slowness → REL-02 |
| CAP-04 | Adjacent-workflow request | A capability outside the purchased use case | "It would be great if it also did payroll" | On the value path → CAP-01 |
| REL-01 | Outage / availability | Service unavailable | "We were down for four hours on the 12th" | Slow but up → REL-02 |
| REL-02 | Performance and latency | Available and too slow to use | "Reports take six minutes to load" | Wrong numbers → REL-03 |
| REL-03 | Data accuracy / integrity | Output is wrong or inconsistent | "The totals don't match our warehouse" | Data is right and hard to reach → REP-* |
| REL-04 | Regression from a release | Something that worked stopped working | "The July release broke our saved filters" | Never worked → CAP-01 |
| INT-01 | Connector missing | No integration with a system in their stack | "There's no Workday connector" | Connector exists and breaks → INT-02 |
| INT-02 | Integration unreliable | Exists, breaks, or silently stops syncing | "The Salesforce sync stopped and nobody told us" | Sync is correct and slow → REL-02 |
| INT-03 | API limitations | Rate limits, missing endpoints, poor docs | "There's no endpoint for bulk update" | UI limitation → ADP-01 |
| INT-04 | Notifications do not reach the work | Output does not arrive where the team already works | "We want alerts in Slack, not email" | Notification content wrong → REP-* |
| SUP-01 | Response time | Time to first human response | "It took three days to hear back" | Fast reply, no resolution → SUP-02 |
| SUP-02 | Resolution quality | Answered, not solved; repeated reopens | "We've reopened this ticket four times" | First response slow → SUP-01 |
| SUP-03 | Agent competence / context loss | The customer re-explains context each time | "I have to start from scratch with every agent" | Escalation handling → SUP-04 |
| SUP-04 | Escalation handling | Escalated issues without a closed-loop resolution | "It was escalated in June and we've heard nothing" | Routine ticket ageing → SUP-01 |
| PRC-01 | Price level | The absolute cost | "It's more than we can justify" | Cost is fine, structure is wrong → PRC-02 |
| PRC-02 | Pricing model / metric mismatch | The billing unit does not match how they get value | "We're charged per seat and we need occasional users" | Tier gating → CAP-02 |
| PRC-03 | Uplift / renewal increase | The change at renewal, not the level | "A 12% increase with no new functionality" | Base price → PRC-01 |
| PRC-04 | Contract terms and flexibility | Term length, notice, true-up, co-terming | "The 90-day notice period caught us out" | Invoice mechanics → BIL-* |
| BIL-01 | Invoice accuracy | Wrong amounts, wrong entity, wrong dates | "The invoice billed us for 40 seats we removed" | Price disagreement → PRC-01 |
| BIL-02 | Payment and procurement friction | PO handling, portals, tax, currency, payment methods | "You won't invoice against our PO system" | Invoice wrong → BIL-01 |
| ADM-01 | Permissions and roles | Cannot express their access model | "We can't stop analysts from editing" | Login/SSO → ADM-02 |
| ADM-02 | SSO / identity | Authentication and provisioning | "SCIM deprovisioning doesn't work" | Permissions after login → ADM-01 |
| ADM-03 | Security, compliance, residency | Certifications, DPAs, audit logs, data location | "Our DPO needs EU residency" | Contract language → PRC-04 |
| REP-01 | Standard reporting gaps | The out-of-box reports do not answer their question | "There's no view of usage by team" | Custom build possible and hard → REP-02 |
| REP-02 | Custom reporting effort | Possible, and it takes an analyst | "Building a report takes half a day" | Report missing entirely → REP-01 |
| REP-03 | Data export and portability | Getting their data out in a usable shape | "Export caps at 10k rows" | API access → INT-03 |
| REP-04 | Documentation and self-serve answers | The answer exists and cannot be found | "The docs stop at the basics" | Training delivery → ONB-03 |
| ACC-01 | Coverage and continuity | CSM turnover, no owner, unclear contact | "We're on our fourth CSM in two years" | Slow replies from a known owner → ACC-02 |
| ACC-02 | Responsiveness of the account team | Reply latency and follow-through on the CS side | "We asked for a quote three weeks ago" | Support tickets → SUP-01 |
| ACC-03 | Broken commitments | Something promised and not delivered | "You said the integration would ship in Q1" | Roadmap declined openly → CAP-* |
| ACC-04 | Proactivity gap | The vendor never brings anything unprompted | "We only hear from you at renewal" | Too much contact → ACC-05 |
| ACC-05 | Contact fatigue | Too many surveys, emails, or check-ins | "We get an NPS request every month" | **Also a survey-programme finding — feed §9 Instrument Health** |
| ROI-01 | Value not evidenced | The outcome may exist and cannot be shown | "I can't prove the savings to my CFO" | Outcome genuinely not achieved → ROI-02 |
| ROI-02 | Outcome not achieved | The business case did not land | "We still do the manual process alongside it" | Achieved and unmeasured → ROI-01 |
| ROI-03 | Value drift | They use it for something other than what they bought | "We only use it for the audit log now" | Original use case live → not this |
| ROI-04 | Internal sponsor cannot justify the line item | Budget-side failure regardless of product state | "My new VP is asking what this is for" | Product complaint → the relevant code |

**Reserved code:** `UNC-00 — uncodable`. Use it rather than forcing a fit. If `UNC-00` exceeds
**5% of mentions** in a period, the taxonomy is missing a code — that is the trigger for §7.

---

## 4. Coding rules

| # | Rule | Rationale |
| --- | --- | --- |
| 1 | **Code the problem, not the requested solution.** | "Add a Slack integration" is a solution; the problem is INT-04. Coding solutions produces a wish list that Product cannot prioritise |
| 2 | **One primary code per mention.** Secondary codes are recorded and never counted in ARR attribution | Multi-primary coding double-counts revenue and makes the register indefensible under challenge |
| 3 | **One mention = one account × one channel × one dated verbatim.** | Prevents a talkative admin from outweighing a segment |
| 4 | **Cap at one mention per account per channel per theme per period** before counting | The arithmetic version of "do not quote the loudest customer" |
| 5 | **Code the customer's words, never the CSM's summary.** | A summary already contains an interpretation, and you cannot separate them later |
| 6 | **Attribute the mention to the speaker's role**, not the account | A severity-3 statement from an economic buyer and one from a contractor rank differently |
| 7 | **Record `stated` and `assessed` separately** for anything from a loss channel | The exit-interview bias correction depends on both surviving |
| 8 | **Praise is coded too**, with `polarity = praise` | You cannot detect a resolved theme without it, and "you said / we did" needs the before-and-after |
| 9 | **Never recode silently.** Any recode carries a version, a date and a coder | A trend line whose history changed without a note is a fabrication |
| 10 | **`UNC-00` over a forced fit.** | Forced fits are invisible errors; `UNC-00` is a visible one that triggers taxonomy maintenance |
| 11 | **Truncate, never paraphrase, a verbatim** | Paraphrase is the mechanism by which a customer's complaint becomes the analyst's opinion |
| 12 | **Every mention keeps its `source_ref`** | A theme card that cannot be traced to the ticket will not survive an executive challenge |

---

## 5. Severity and polarity

| Severity | Name | Test | Typical routing weight |
| --- | --- | --- | --- |
| **1** | Friction | Annoying; a workaround exists and is cheap | Batch with the theme; rarely justifies its own decision |
| **2** | Workflow blocker | A workflow is blocked, or the workaround is costly, manual or error-prone | Named decision at theme level |
| **3** | Business-case blocker | The reason they bought is not achievable, or an outcome in the success plan cannot be met | Escalate individually; pair with `churn-risk` for the account |

Severity is coded from the **consequence described**, not from the customer's tone. An angrily
worded complaint about a cosmetic issue is severity 1. A calm sentence — "we've gone back to the
spreadsheet for that" — is severity 3, because it says the value path is dead.

| Polarity | Use |
| --- | --- |
| `complaint` | Something is wrong now |
| `request` | Something absent is wanted. Recode to the underlying problem per rule 1, keep the request text in the verbatim |
| `praise` | Something works. Required for resolved-theme detection and for the QBR "we did" slide |
| `neutral_observation` | Context with no valence — often the most useful material for symptom-vs-cause work |

---

## 6. The split test and the merge test

**Split test.** A theme is really two or more themes if either holds:

1. **Different owner** — two mentions inside it would be routed to different accountable functions.
2. **Different fix** — the work that resolves one would not resolve the other.

Worked example. "Reporting is bad" fails both and splits into:

| Split into | Owner | Fix |
| --- | --- | --- |
| REP-01 standard reporting gaps | Product | Build the missing view |
| REP-02 custom reporting effort | Product (Design) | Reduce the steps in the builder |
| REP-03 export and portability | Product (Platform) | Raise the export ceiling |
| REP-04 documentation | Education | Write the guide |

Four decisions, four owners, four success measures. As one theme it would have received one
under-specified roadmap line and satisfied nobody.

**Merge test.** Two themes are one if **all three** hold: same accountable owner, same fix, and
each has <5 mentions in the period. Merge, restate the prior period under the merged code, and
record the merge in the version log.

**When you split or merge, history moves with the code.** If you cannot recode history — the
usual reason is that verbatims were not retained — say so explicitly and mark every trend line
crossing that boundary as **broken series, not comparable**.

---

## 7. Versioning

| Change | When it is allowed | What it requires |
| --- | --- | --- |
| **Add a theme** | Period boundary only, when ≥5 mentions across ≥3 accounts in one period do not fit, or `UNC-00` exceeds 5% | Definition, inclusion example, exclusion example, default route, version bump |
| **Split a theme** | Period boundary, when the split test fires | New codes, recoded history or a broken-series label |
| **Merge themes** | Period boundary, when the merge test fires | Merged code, restated history |
| **Rename** | Any time | Code string is immutable; only the display name changes. Never reuse a retired code string |
| **Deprecate** | Period boundary, when a theme is genuinely resolved or the capability was removed | Mark `deprecated_at`; keep it visible in history with the resolution date so the "we did" story survives |
| **Change a category** | Annual review only | Full recode of the affected corpus, or a hard break in the series |

Version string: `MAJOR.MINOR`. MINOR for additions and renames; MAJOR for splits, merges,
category changes, or any recode. Print the version in the readout header and state whether
history was recoded.

---

## 8. Inter-coder reliability

Trend claims are only as good as coding consistency. Measure it; do not assert it.

**Protocol**

1. Draw a **random 10%** of the period's mentions (minimum 50; if the corpus is under 50, code all
   of it twice).
2. Have a second coder code them independently, blind to the first coder's codes.
3. Compute **Krippendorff's alpha** on the primary code (nominal) and separately on severity
   (ordinal). Alpha handles any number of coders, incomplete data and multiple measurement levels,
   which is why it is preferred here over percentage agreement.
4. Apply the standard social-science thresholds `[A]`:

| Alpha | Verdict | What you may publish |
| --- | --- | --- |
| ≥ 0.800 | Reliable | Trend claims, ARR attribution, routing decisions |
| 0.667 – 0.800 | Marginal | Tentative conclusions only; label the register accordingly |
| < 0.667 | Unreliable | **Discard the coding pass.** Clarify the definitions and recode |

5. Print alpha, the sample size and the coder identities in the readout Bottom Line block.

**Percentage agreement is not a substitute.** Two coders agreeing 85% of the time on a taxonomy
where one code holds 70% of the volume have demonstrated almost nothing; alpha corrects for
agreement expected by chance, which is exactly the correction you need.

**Where disagreement concentrates, the definition is wrong.** Tabulate disagreements by code
pair. A code pair that accounts for most of the disagreement needs a sharper exclusion example,
not better coders — the most common offenders are CAP-01 vs CAP-04 (value path or not) and ADP-01
vs CAP-01 (hard or impossible).

---

## 9. LLM-assisted coding

An LLM coder is a coder. It gets the same discipline, and its output is not more trustworthy for
being fast.

| Requirement | Detail |
| --- | --- |
| **Named in `coder`** | Record the model identifier and the prompt version, exactly as you would a human name |
| **Gold set** | Maintain ≥100 human-coded mentions spanning every category. Score the model against it before each period's run |
| **Same alpha check** | Compute alpha between model and human on the 10% double-coded sample. The ≥0.800 threshold applies unchanged |
| **Definitions in the prompt** | Pass the code book — definition, inclusion, exclusion — not just the code names. Code names alone produce confident misfiling |
| **Force `UNC-00`** | Instruct the model to return `UNC-00` rather than the nearest fit, and audit the `UNC-00` rate as a health check on the prompt |
| **No severity without the consequence** | Require the model to quote the consequence phrase it used to assign severity. Tone-based severity is the characteristic LLM error here |
| **Drift audit each period** | Re-score the frozen gold set. A drop against an unchanged gold set means the model or prompt changed, and last period's trend line is not comparable |
| **Human review of severity 3** | Every severity-3 mention is reviewed by a person before it reaches a theme card. These are the mentions that trigger escalations |

---

## 10. Common coding failures

| Failure | What it looks like | Correction |
| --- | --- | --- |
| Solution coding | A taxonomy full of feature names | Rule 1 — recode to the problem |
| Sentiment coding | Codes like "unhappy", "frustrated" | Sentiment is `polarity`, not a theme. A theme is a problem |
| Catch-all bloat | One code holds 40% of mentions | Split test. A code that large is a category wearing a theme's badge |
| Long-tail sprawl | Thirty codes with one mention each | Merge test, or leave them as `UNC-00` until they reach the add threshold |
| Silent recode | The chart changed and nobody knows why | Version log, every time |
| Tone-driven severity | Angry cosmetic complaints coded 3 | Code the consequence, not the volume of the voice |
| Account-blind counting | One customer's forty emails read as forty mentions | Rule 4 — cap per account per channel per theme per period |
| Praise discarded | Only complaints are coded | Rule 8 — without praise you cannot show a resolved theme |
| Coding the CSM's note | Verbatims that sound like internal language | Rule 5 — the customer's words, or nothing |
| Sub-theme trend lines | Charts drawn at the fluid layer | Trend at category and theme level only |

---

## 11. Symptom vs cause — worked examples

Run the **what-would-have-to-be-true** test on every theme that reaches the register: for
`<stated theme>` to be the actual cause of `<the outcome>`, what would have to be true — and is
it? Name the observable that would confirm it, check it, record the result.

| Stated as | Would have to be true | Test against | Result | Assessed cause |
| --- | --- | --- | --- | --- |
| "Too expensive" | Accounts citing price show comparable adoption to those who renewed | `usage_daily.core_actions` per seat vs the renewed cohort | 0.31× the renewed cohort | Value not realised; price is the language, not the cause |
| "Missing feature X" | The missing feature blocks the use case bought in the original deal | Sales handoff `primary_use_case` → product event mapping | Use case never went live | Onboarding failure surfaced as a roadmap gap |
| "Support is slow" | FRT/TTR for these accounts is worse than the renewed cohort | `ticket.first_response_at`, `resolved_at` | Equal FRT, 3.1× reopen rate | Not speed — resolution quality |

Print both `stated_reason` and `assessed_cause` for every theme; never overwrite the customer's
words with your interpretation.

## 12. Further coding and register failures

| Anti-pattern | Correction |
| --- | --- |
| NPS as a scoreboard — one number, tracked as a KPI, no verbatims | Report the score, the response rate, the ARR represented and the themes underneath it. The trajectory of a named respondent beats the level `[P]` |
| Presenting churn exit-interview reasons as the churn causes | Print `stated_reason` and `assessed_cause` separately; exit reasons over-report price and under-report "we never got it working" `[P]` |
| Free-text themes rebuilt from scratch each quarter | A closed, versioned taxonomy with a code book and a measured alpha |
| Counting a growing corpus as a growing theme | Share of voice with a minimum-volume floor, plus the newly-visible label |
| Weighting a 6-month-old NPS as current sentiment | Survey data is stale beyond 90 days; a departed respondent's score is void, not neutral |

