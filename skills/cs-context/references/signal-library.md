# The Signal Library

> The master churn-signal taxonomy for this library. Every skill that assesses risk, health,
> or renewal likelihood reads from this file so that a risk brief, a forecast and a board
> report all mean the same thing by the same words.
>
> **Signal IDs are stable.** `U4`, `R1`, `C1` and so on are referenced by name in
> `churn-risk`, `save-play`, `churn-postmortem` and `health-score-designer`. Do not renumber.
>
> **Family mapping.** The sections below map onto the library's seven fixed signal families:
> §1 and §2 → *Product usage & adoption* · §3 → *Relationship & engagement* ·
> §4 → *Sentiment & VoC* · §5 → *Support & reliability* · §6 → *Commercial & contract*
> and *Billing & payment* · §7 → *Firmographic & external* · §8, §9 cut across.
>
> **Evidence labels are load-bearing.** `[M]` measured benchmark · `[V]` vendor research ·
> `[P]` practitioner rule of thumb · `[A]` academic. Never restate a `[P]` as a benchmark.
> Say "commonly configured at X", not "research shows X".

---


**Purpose:** runtime reference for producing analyst-grade churn-risk assessments. Every signal below is specified as: source system → field → computation → firing threshold → lead time → strength → false-positive traps.

**Evidence labels used throughout:**
- `[M]` = **Measured benchmark** from a named study with a stated sample/period.
- `[V]` = **Vendor research / marketing data** — directionally useful, methodology usually not published.
- `[P]` = **Practitioner rule-of-thumb** — widely used in CS orgs, no published measurement. Never present as a statistic.
- `[A]` = **Academic / peer-reviewed or thesis-grade**.

**Hard rule for output:** never present a `[P]` threshold as a benchmark. Say "commonly configured at X" not "research shows X."

---

**Contents**

- [0. Scoring conventions — get these right or every signal below is noise](#0-scoring-conventions-get-these-right-or-every-signal-below-is-noise)
- [1. Product usage & adoption signals (mostly LEADING, highest volume, lowest precision individually)](#1-product-usage-adoption-signals-mostly-leading-highest-volume-lowest-precision-individually)
- [2. Technical / integration signals (LEADING, high precision, low volume — the best signal-to-noise class)](#2-technical-integration-signals-leading-high-precision-low-volume-the-best-signal-to-noise-class)
- [3. Relationship & stakeholder signals (LEADING, highest strength-per-signal in enterprise)](#3-relationship-stakeholder-signals-leading-highest-strength-per-signal-in-enterprise)
- [4. Sentiment & voice-of-customer signals](#4-sentiment-voice-of-customer-signals)
- [5. Support & service signals](#5-support-service-signals)
- [6. Commercial, contract & billing signals (mix of leading and lagging; the leading ones are the highest-precision signals in the taxonomy)](#6-commercial-contract-billing-signals-mix-of-leading-and-lagging-the-leading-ones-are-the-highest-precision-signals-in-the-taxonomy)
- [7. Firmographic / external-event signals (LEADING, exogenous, often the true root cause)](#7-firmographic-external-event-signals-leading-exogenous-often-the-true-root-cause)
- [8. Value-realization & success-plan signals (LEADING; the ones a CCO actually cares about)](#8-value-realization-success-plan-signals-leading-the-ones-a-cco-actually-cares-about)
- [9. Silence — the absence signals](#9-silence-the-absence-signals)
- [10. Lagging indicators — and precisely why they are too late](#10-lagging-indicators-and-precisely-why-they-are-too-late)
- [11. Compound risk patterns — where the actual predictive power lives](#11-compound-risk-patterns-where-the-actual-predictive-power-lives)
- [12. Segment-specific differences](#12-segment-specific-differences)
- [13. Model construction, calibration and validation](#13-model-construction-calibration-and-validation)
- [14. Systematic false-positive traps (checklist before escalating anything)](#14-systematic-false-positive-traps-checklist-before-escalating-anything)
- [15. Source register](#15-source-register)
- [Appendix A — Signal priority index (rank order for triage)](#appendix-a-signal-priority-index-rank-order-for-triage)
- [Appendix B — Source-system → field crosswalk](#appendix-b-source-system-field-crosswalk)
- [Appendix C — Renewal-clock operating cadence (annual enterprise contracts) `[P]`](#appendix-c-renewal-clock-operating-cadence-annual-enterprise-contracts-p)

---

## 0. Scoring conventions — get these right or every signal below is noise

| Concept | Definition | Why it matters |
|---|---|---|
| **Account baseline** | Trailing 90-day median of the metric for *that account*, excluding the most recent 14 days | Absolute thresholds ("<5 logins/wk") mis-fire across account sizes. A weekly-cadence account that stays weekly is healthy; a daily account that drops to weekly is churning. |
| **Cohort baseline** | Median of the metric across accounts in the same (segment × product × tenure-bucket × industry) cell | Isolates account-specific decay from product-wide or seasonal decay |
| **Decay ratio** | `metric_L28 / metric_baseline_90d` | The single most reusable primitive. Fire bands: 0.85–1.0 watch, 0.60–0.85 risk, <0.60 severe |
| **Z-score vs. self** | `(x_t − μ_account_90d) / σ_account_90d` | Use when the metric is noisy/bursty (API calls, ticket volume). Fire at z ≤ −1.5 (moderate), z ≤ −2.0 (strong) |
| **EWMA smoothing** | `S_t = α·x_t + (1−α)·S_{t−1}`, α = 0.2–0.3 for weekly series | Prevents single-week holiday dips from firing risk |
| **Consecutive-period rule** | Signal only fires after N consecutive periods below threshold (N = 2 for weekly, 3 for daily) | Cuts false positives from single-period noise by roughly an order of magnitude `[P]` |
| **Seasonality mask** | Suppress or de-weight decay signals during the account's known low-season and the vendor's own holiday windows | Late Dec, national holidays, academic summer, retail freeze windows, fiscal year-end |
| **Renewal-proximity weight** | `w = 1 + k·max(0, 1 − days_to_renewal/180)`, k ≈ 1.0 | Same raw decay is materially more dangerous 45 days out than 400 days out |
| **Lead time** | Days between signal firing and the *churn decision* (not the churn date). In annual contracts the decision typically precedes the contract end date by the notice period + internal budget cycle | Enterprise notice periods cluster at 30/60/90 days; 30 is modal in standard-form SaaS agreements, 60 common in negotiated enterprise deals `[P]` |

**Critical framing:** the renewal *date* is not the deadline. The deadline is `renewal_date − notice_period_days − customer_budget_lock_days`. For an enterprise account with a 90-day notice period whose budget locks 60 days before fiscal year start, a signal that fires 100 days pre-renewal is already late.

---

## 1. Product usage & adoption signals (mostly LEADING, highest volume, lowest precision individually)

| # | Signal | Lead/Lag | Typical lead time | Strength | Source system → field | Computation | Fire threshold | False-positive traps |
|---|---|---|---|---|---|---|---|---|
| U1 | **Login/session frequency decay** | Leading | 60–150 d | Moderate | Product analytics (Pendo/Amplitude/Mixpanel/Heap) → `session_start` events; or app DB `last_login_at` | `sessions_L28 / median(sessions, trailing 90d excl. last 14d)` per account | <0.70 for 2 consecutive weeks → risk; <0.50 → severe | SSO/embedded usage that bypasses the login event; mobile vs web split; a UI change that reduces required logins; a customer moving to API-only consumption (see T1) |
| U2 | **WAU decay** | Leading | 60–120 d | Moderate–Strong | Product analytics → distinct `user_id` with ≥1 qualifying action in 7 d | `WAU_current / WAU_baseline_90d` | <0.75 for 3 consecutive weeks | Team on PTO; seasonal business; a single power user's actions being counted as "the account" |
| U3 | **MAU decay** | Leading | 90–180 d | Strong | Same as U2, 28-day window | `MAU_L28 / MAU_baseline` | <0.80 → watch; <0.60 → severe | Slowest to move; by the time MAU halves the decision is usually made. Use WAU for detection, MAU for confirmation |
| U4 | **MAU ÷ licensed seats (license/seat utilization)** | Leading | 90–270 d | **Strong** — best single predictor of *downsell*, strong for churn | CRM/billing → `contracted_seats`; product → distinct active users L28 | `MAU_L28 / contracted_seats` | <0.60 → seat-reduction risk at renewal; <0.40 → churn risk; <0.25 → near-certain downsell | Shared/service accounts inflating seats; seasonal workforces; deliberately over-bought seats for a phased rollout (check `contract_start_date` — <180 d old accounts are ramping, not dying); floating vs named licensing |
| U5 | **DAU/MAU stickiness ratio** | Leading | 60–120 d | Moderate | Product analytics | `mean(DAU over 28d) / MAU_28d` | Fire on *change*: ratio drop >25% rel. to account baseline. Absolute floor only for daily-use products | B2B SaaS commonly sits 10–20% and that is *appropriate* for weekly-cadence tools `[P]`. Absolute DAU/MAU thresholds are the most common rookie error in B2B health scores |
| U6 | **Breadth of feature adoption** | Leading | 120–270 d | Strong | Product analytics → feature-flag / event taxonomy; `distinct_feature_keys_used_L90` | `breadth = distinct_core_features_used / core_feature_catalog_size`; track `Δbreadth` QoQ | breadth <0.30 at day 120 post-go-live; or `Δbreadth ≤ −2 features` QoQ | Pendo's 2019 Feature Adoption Report (615 Pendo subscriptions with >1 yr tenure) found ~80% of features are rarely/never used and ~12% of features drive ~80% of daily usage volume `[M]`. Therefore breadth must be measured against a curated **core/value-path feature set**, never the full catalog |
| U7 | **Depth: core-action frequency** | Leading | 60–150 d | **Strong** | Product analytics → the 1–3 events on the value path (e.g. `report_published`, `deal_created`, `ticket_resolved`, `workflow_run`) | `core_actions_per_active_user_L28 / baseline` | <0.70 for 2 periods → risk | Requires an honest core-action definition validated against retained-vs-churned cohorts. If your "core action" is `page_view`, this signal is worthless |
| U8 | **Activation / "aha" event regression** | Leading | 90–200 d | Strong | Product analytics + CS platform milestone object | Account was activated (hit the aha event N times in a window), then `days_since_last_aha > 2 × historical_median_interval` | Regression sustained 30 d | New team members ramping; a legitimate workflow migration to a different (also valuable) surface |
| U9 | **Time-to-first-value (TTFV) overrun** | Leading | 180–365 d (fires during onboarding, predicts the *first* renewal) | **Strong** | CS platform / onboarding project → `go_live_date`, `first_value_event_at`, `target_ttfv_days` | `actual_ttfv / target_ttfv`; also `days_since_contract_start with no value event` | >1.5× target → risk; >2.0× → severe; no value event by day 90 → severe | Contract-start ≠ project-start when the customer causes the delay — but that does *not* reduce churn risk, only who is accountable. Published cross-company TTFV "medians" circulating online are content-marketing figures with no disclosed method — do not cite them |
| U10 | **Onboarding milestone slippage** | Leading | 180–365 d | Strong | PS/PSA tool (Mavenlink/Kantata/Jira) → milestone `due_date` vs `completed_date` | `% milestones overdue`, `cumulative_slip_days` | ≥2 milestones overdue OR cumulative slip >30 d | Slip caused by vendor-side resource constraints reads identically to customer disengagement in the data — separate by *who owns the blocked task* |
| U11 | **Services / onboarding effort overrun** | Leading | 180–365 d | Moderate | PSA → `hours_burned / hours_sold`, `scope_change_count` | Burn ratio; change-order count | Burn >1.3× sold hours, or ≥2 change orders | High burn on a *complex, engaged* deployment is a sign of investment, not risk. Pair with U8: high burn + no aha event = severe; high burn + aha achieved = healthy |
| U12 | **Data volume / record count decline** | Leading | 90–180 d | Strong (near-certain in data-resident products) | App DB → `rows_ingested`, `objects_created`, `storage_bytes`, `records_synced_daily` | `volume_L28 / baseline_90d`, plus absolute trend slope | <0.70 → risk; net-negative record count (deletions exceeding creations) → severe | Customer data hygiene projects and archival policies produce legitimate declines; check for a matching `delete` burst vs. a gradual ingestion stop |
| U13 | **New-user provisioning stop** | Leading | 90–240 d | Moderate | Product/identity → `user_created_at` | `new_users_L90` vs. prior 90 d | Zero new users in 90 d on an account that previously averaged ≥1/mo | Fully-rolled-out mature accounts legitimately stop adding users. Only meaningful when `seat_utilization < 0.85` |
| U14 | **Deprovisioning burst** | **Leading (strong) → borderline lagging** | 30–120 d | **Near-certain when combined** | Identity/SCIM/product → `user_deactivated_at` | `deactivations_L30 / active_users_start_of_period` | >10% of active users deactivated in 30 d → severe; >25% → treat as churn-in-progress | Customer-side layoffs (external, see F3) vs. deliberate consolidation off your product. Cross-check against the customer's headcount news |
| U15 | **Admin / owner change** | Leading | 60–180 d | Strong | Product `role` audit log → `role_changed`, `owner_transferred`; CS platform contact object | Change in `account_owner_user_id` or primary admin | Any change to the primary admin/owner | Routine IT rotation. Severity depends on whether the *departing* admin was the champion (see R1) |
| U16 | **Sandbox/test-only usage** | Leading | 120–270 d | Moderate | Product → `environment` field on events | `prod_events / total_events` | <0.20 after day 90 post-go-live | Legitimate long evaluation cycles in regulated industries |
| U17 | **Automation/workflow disablement** | Leading | 60–150 d | Strong | Product → `workflow.status`, `schedule.enabled` | Count of active scheduled jobs/automations; Δ vs baseline | Net −30% active automations in 60 d | Consolidation of many workflows into fewer, better ones. Check total *runs*, not just count |

---

## 2. Technical / integration signals (LEADING, high precision, low volume — the best signal-to-noise class)

| # | Signal | Lead/Lag | Lead time | Strength | Source → field | Computation | Threshold | Traps |
|---|---|---|---|---|---|---|---|---|
| T1 | **API call volume decline** | Leading | 60–150 d | Strong | API gateway logs / metering DB → `api_calls` by `account_id`, `endpoint_class` | `calls_L28 / baseline_90d`, computed **separately for critical vs. read-only endpoints** | Critical-endpoint volume <0.60 of baseline for 2 weeks | Customer efficiency work (batching, caching, moving from polling to webhooks) collapses call volume while *increasing* value. Always check `distinct_endpoints` and `records_processed`, not just request count. Note: the widely-circulated "40% MoM API decline predicts churn 60–90 days out" figure is unattributed SEO content — do not cite it |
| T2 | **Integration disconnect / OAuth token expiry** | Leading | 45–120 d | **Near-certain if unrepaired >30 d** | Integration service → `connection.status`, `token_expires_at`, `last_successful_sync_at`, `consecutive_failure_count` | Days since last successful sync; failure streak | `status = disconnected` for >7 d → risk; >30 d unrepaired → severe | A disconnect the customer *doesn't notice or fix* is the signal; the disconnect itself may be your bug. Vendor data suggests integration depth correlates strongly with retention: ProfitWell's integrations study (cited as ~500k companies) reports ~10–15% higher retention with ≥1 integration and ~18–22% with ≥4 `[V]`; Crossbeam (n=526 survey) reports users with integrations ~58% less likely to churn `[V]`. Treat these as directional vendor figures, not measured causal effects |
| T3 | **Webhook endpoint failures** | Leading | 45–120 d | Strong | Webhook delivery service → `delivery_status`, `retry_count`, `endpoint_disabled_at` | Failure rate over 7 d; auto-disable events | Endpoint auto-disabled, or >20% failures for 7 d, with no customer remediation ticket | Customer infra migration (temporary). Escalate only if no repair within 14 d |
| T4 | **SDK / API version staleness** | Leading | 180–365 d | Weak–Moderate | API gateway → `user_agent`, `api_version` header | Major versions behind current | ≥2 major versions behind AND no upgrade activity in 180 d | Conservative enterprises deliberately pin versions. Weak alone; useful as a compound term |
| T5 | **SSO / identity provider decoupling** | Leading | 30–90 d | **Near-certain** | Identity → SAML/OIDC config change, IdP app removal | Any deletion/disable of the SSO connection | Any occurrence | Legitimate IdP migration (Okta→Entra). Confirm via ticket before escalating — but escalate the *check* immediately |
| T6 | **Data export / bulk download burst** | Leading | 15–90 d | **Near-certain** | Product audit log → `export.created`, `report.bulk_download`, `api.bulk_read`, admin `data_dump` | Export volume z-score vs. account baseline; exports by an admin who is not a routine exporter | z ≥ +2.5, or any full-account export by a non-routine user | Legitimate: annual audit, BI migration, compliance/eDiscovery hold, backup policy. Distinguish by (a) is it scheduled/recurring, (b) does it cover *all* historical data, (c) does it coincide with any commercial signal (C-series) |
| T7 | **Deletion of production configuration** | Leading | 15–60 d | Near-certain | Audit log → `workspace.deleted`, `project.archived`, `pipeline.deleted` | Count of destructive admin actions L30 | Any bulk destructive action by an admin | Cleanup projects. Check whether new objects are being created in parallel |
| T8 | **Uptime/incident exposure of the account** | Leading (risk amplifier) | 60–180 d | Moderate | Status page / incident mgmt (PagerDuty, Statuspage) → incidents mapped to affected tenants | Count of Sev1/Sev2 incidents *the account experienced* in 180 d; minutes of degradation | ≥2 Sev1 in 180 d, or SLA credit issued | Incident exposure only converts to churn when combined with an unresolved sentiment signal (S-series). Alone it is a weak predictor |

---

## 3. Relationship & stakeholder signals (LEADING, highest strength-per-signal in enterprise)

| # | Signal | Lead/Lag | Lead time | Strength | Source → field | Computation | Threshold | Traps |
|---|---|---|---|---|---|---|---|---|
| R1 | **Champion departure** | Leading | 90–365 d | **Near-certain (top-tier signal)** | CRM contact `email_bounce_status = hard_bounce`; enrichment (ZoomInfo/Clearbit/LinkedIn Sales Nav) `job_change_detected`; product `last_login_at` on that user; email autoresponder "no longer with the company" | Boolean on champion contact record; also `days_since_champion_last_activity` | Any confirmed departure of a contact flagged `is_champion = true` | Vendor research from Sturdy AI (presented at an industry conference and relayed via a vendor blog) reports a **51% chance the account churns within 12 months** after a champion departs, and **~65% of accounts with an executive change do not renew**; acting within the first 48 hours was associated with customers being **33% more likely to renew** `[V]` — vendor data, methodology unpublished. Traps: title changes that are promotions (still an ally, more power); contacts flagged as champions who never were; email bounces caused by domain/MX migrations not departures |
| R2 | **Executive sponsor disengagement** | Leading | 120–270 d | Strong | Calendar/CS platform activity object → meetings with contacts where `seniority in (VP, C-level)`; email logs | `days_since_last_exec_touch`; `exec_meetings_L180` | No exec-level interaction in 180 d (enterprise) / 270 d (mid-market) → risk; exec sponsor field empty → structural risk | Exec sponsors legitimately delegate on healthy, boring accounts. Weight higher when paired with any usage decay |
| R3 | **No named executive sponsor** | Leading (structural) | Persistent | Moderate–Strong | CRM/CS platform → `executive_sponsor_contact_id IS NULL` | Boolean | Null on any account above the segment ACV threshold | Common data-hygiene failure — an empty field may mean "not recorded," not "doesn't exist". Validate before scoring |
| R4 | **Low multi-threading / single point of contact** | Leading (structural) | Persistent, converts on R1 | **Strong** | CRM/CS platform → count of contacts with an interaction in L90, by role and department | `active_contacts_L90`; `distinct_departments`; `distinct_seniority_levels` | ACV-scaled: <2 active contacts (SMB), <3 (mid-market), <5 (enterprise) → risk. Any tier with exactly 1 → severe | This is a **risk multiplier, not a standalone predictor**. Single-threaded + stable champion can run for years; single-threaded + R1 is near-certain churn. Emilia D'Anzica's practice guidance is to make a minimum contact count a *gate* on marking onboarding complete `[P]` |
| R5 | **Meeting acceptance / no-show rate** | Leading | 60–180 d | Strong | Calendar API (Google/Outlook) → `responseStatus`, `attendees`; conversation intelligence (Gong/Chorus) → `attended` | `accepted / invited` over L90; `no_show_rate`; `reschedule_count` | Acceptance <60% or ≥2 consecutive no-shows/cancellations → risk; ≥3 → severe | Genuinely busy customers. Calendar scraping under-reports when the customer uses a different calendar system. Weight declining *trend* over absolute level |
| R6 | **Unopened/declined QBR-EBR invites** | Leading | 90–200 d | Strong | Marketing automation / calendar → `invite_opened`, `responseStatus = declined` or no response | QBR held? attendee seniority? days since last QBR | No QBR held in 2 consecutive quarters for an account whose plan requires one; or QBR held with zero exec attendance | An account that declines QBRs but has strong usage and a happy champion may simply hate meetings — this is a **process** signal, and its predictive power depends on your motion. The 2025 Customer Revenue Leadership Study (Pavilion / 6sense, ≈800 customer and post-sales leaders) found "early risk detection" is the #1 Relationship & Retention goal for 62% of leaders `[M]`, which is why QBR non-attendance is over-weighted in most scorecards |
| R7 | **Email reply latency increase** | Leading | 45–150 d | Moderate–Strong | Email integration (Gmail/Outlook via CS platform or Gong/Sturdy) → thread timestamps | `median_reply_hours_L60 / median_reply_hours_baseline` | >2.0× baseline, or median latency >72 h where it was <24 h | Vacations, org changes, an assistant now triaging. Compute per-contact, not per-account |
| R8 | **Email reply-rate collapse** | Leading | 45–150 d | Strong | Same | `replied_threads / outbound_threads` L90 | <0.30 where baseline was >0.60 | Your emails may have started going to spam — check delivery/open telemetry before concluding disengagement |
| R9 | **Sentiment shift in written comms** | Leading | 60–180 d | Moderate–Strong | Conversation/comms intelligence (Sturdy, Gong, Enterpret) → per-sentence sentiment, risk tags | Rolling sentiment mean; count of risk-tagged sentences L60 | Mean sentiment drop >1σ, or ≥3 risk-tagged sentences in 60 d | Sturdy reports ~17% of customer→business communications contain an actionable "signal," across a stated corpus of 31.1M conversations / 3.2B words `[V]`. Traps: cultural/linguistic variation in directness; terse writers scored as negative; sarcasm |
| R10 | **Shift from strategic to transactional language** | Leading | 90–200 d | Moderate | Comms intelligence / call transcripts | Ratio of forward-looking terms ("next year", "roadmap", "expand", "rollout") to transactional terms ("invoice", "credentials", "export", "terminate") | Forward-looking mentions → 0 across L90 while transactional persist | Requires enough conversation volume; unusable on low-touch accounts |
| R11 | **Procurement / legal / vendor-management re-engagement** | Leading | 60–180 d | **Strong** | CRM contact `department in (Procurement, Legal, Vendor Management)`; email domain-role parsing; ticket requester role | First-touch or re-activation of a procurement/legal contact outside the normal renewal window | Any unsolicited procurement contact >120 d before renewal | Sometimes signals *expansion* paperwork or a routine vendor-risk review (SOC 2, DPA refresh). Disambiguate by the artifact requested: security questionnaire = review; **termination-clause / notice-period / data-deletion / transition-assistance questions = churn** |
| R12 | **Requests for contract termination terms or data-portability** | Leading | 30–120 d | **Near-certain** | CRM email/ticket text; CLM (Ironclad/DocuSign CLM) → clause-lookup activity | Keyword/intent detection on "notice period", "termination for convenience", "data return", "transition assistance", "wind-down" | Any occurrence | Legal teams sometimes audit all vendor contracts routinely. Still: escalate on first occurrence — the cost of a false positive here is one conversation |
| R13 | **Competitor mention in calls/tickets/emails** | Leading | 60–180 d | Strong | Conversation intelligence (Gong/Chorus) competitor tracker; ticket/email text search | Count of competitor mentions L90; mentions by senior contacts | ≥1 mention by an economic buyer, or ≥3 mentions L90 by any contact | Benchmarking exercises and casual references. Weight by *who* said it and whether it was accompanied by a feature-gap or pricing complaint |
| R14 | **CSM relationship discontinuity** | Leading (vendor-side) | 60–180 d | Moderate | CS platform → `csm_owner_id` change history | Count of CSM changes in 12 mo | ≥2 CSM changes in 12 mo | Vendor-caused; frequently the hidden driver behind a cluster of "customer disengagement" signals |
| R15 | **Community / education disengagement** | Leading | 90–240 d | Weak–Moderate | Community platform, LMS (Skilljar/Docebo/Intellum) → logins, course completions, cert expiry | Certified-admin count; `certifications_expiring_60d` | Zero certified admins remaining; community MAU → 0 | Weak alone. The 2025 Customer Revenue Leadership Study (Pavilion / 6sense) associates LMS presence in the stack with higher NRR `[M]`, so treat education decay as an adoption leading indicator, not a churn predictor in itself |

---

## 4. Sentiment & voice-of-customer signals

| # | Signal | Lead/Lag | Lead time | Strength | Source → field | Computation | Threshold | Traps |
|---|---|---|---|---|---|---|---|---|
| S1 | **NPS trajectory (not level)** | Leading | 90–270 d | Moderate | Survey tool (Delighted/Qualtrics/GetFeedback) or CS platform `nps_score`, `nps_date`, `respondent_role` | `Δnps = latest − prior` per respondent; account-level detractor ratio | Any drop ≥3 points by the same respondent; any promoter → detractor transition; detractor ratio >0.33 | Public analyses (e.g. Buffer's open NPS/churn analysis) show 0-scorers churn most, 1–6 cluster similarly, and 7–10 churn least `[V]` — i.e. the promoter/passive/detractor cut is coarse. NPS as a *level* is a weak churn predictor; **the transition is the signal**. Also: B2B response rates are low, so account-level NPS is often 1–2 people. LSE work is frequently cited secondhand for a ~0.24 correlation between NPS and revenue growth — flag as secondhand |
| S2 | **CSAT trajectory on support interactions** | Leading | 45–120 d | Moderate | Helpdesk (Zendesk `satisfaction_rating.score`, Intercom, Salesforce Service Cloud) | Rolling mean CSAT L90 vs. baseline; count of ≤2/5 ratings | Mean drop >0.5 pts on a 5-pt scale, or ≥2 bottom-box ratings in 60 d | Measures the *support interaction*, not the relationship. High-volume accounts have more chances to be dissatisfied |
| S3 | **Customer Effort Score (CES) rise** | Leading | 45–120 d | Moderate | Survey tool post-resolution | Rolling mean CES | Sustained increase >1 pt | Small samples; question-wording drift |
| S4 | **CSM subjective sentiment / "gut" field** | Leading | 60–270 d | **Strong when disciplined** | CS platform manual scorecard measure (most platforms let a measure be set manually and given a validity period) | Manual grade + mandatory comment; require refresh cadence | Any downgrade; any measure past its validity period (stale = treat as unknown, not green) | Kristen Hayer's "7 Components of a Health Score" explicitly includes **CSM Assessment** on the grounds that accounts routinely look green in the platform right up to churn `[P]`. Traps: optimism bias, sandbagging before comp cycles, and CSMs who never downgrade. Audit by comparing manual grades against realized churn |
| S5 | **Win-back / cancellation survey themes** | **Lagging** | 0 (post-decision) | n/a for prediction | Churn survey, exit interview | Coded reason taxonomy | n/a | Only useful for feeding back into the *leading* taxonomy. Self-reported reasons systematically over-report "price" and under-report "we never got it working" |

---

## 5. Support & service signals

| # | Signal | Lead/Lag | Lead time | Strength | Source → field | Computation | Threshold | Traps |
|---|---|---|---|---|---|---|---|---|
| P1 | **Ticket volume spike** | Leading | 90–240 d | Weak–Moderate alone | Helpdesk → ticket count by `account_id`, `type`, `priority` | `tickets_L30` z-score vs. account baseline, normalized per active user | z ≥ +2.0 | High ticket volume also correlates with **high engagement**. Volume alone is nearly useless; it must be conditioned on resolution and sentiment |
| P2 | **Spike-then-silence pattern** | Leading | 60–150 d | **Strong** | Helpdesk | Detect `z(tickets, month t) ≥ +1.5` followed by `tickets_{t+1,t+2} ≤ 0.25 × baseline` | Pattern match over 3 consecutive months | The single most under-implemented support signal. The customer stopped asking because they stopped trying. Trap: the issue was genuinely fixed — check whether usage (U1/U7) recovered in the same window. **Silence + usage recovery = fixed. Silence + usage decay = disengagement.** |
| P3 | **Repeat/recurring issue** | Leading | 60–180 d | **Strong** | Helpdesk → ticket `tags`, linked `problem_id`, semantic clustering (Enterpret/Unwrap) | Count of tickets in the same cluster over 180 d; count of *reopened* tickets | ≥3 tickets in one cluster in 180 d, or any ticket reopened ≥2× | The academic escalation-prediction work on IBM's support org (University of Victoria, arXiv:1901.01344, 2019) found escalation likelihood must be modeled by **aggregating ticket history per customer**, not by scoring tickets in isolation `[A]`. Practitioner framing: *persistence, not intensity*, is the signal |
| P4 | **Thread elongation / context reintroduction** | Leading | 60–180 d | Moderate–Strong | Helpdesk → comment count per ticket, customer-authored comment count | Median comments-per-ticket vs. baseline; detection of the customer restating prior context | Median comments/ticket >2× baseline | Complex products have naturally long threads. Compare within issue-type |
| P5 | **Unresolved P1 / open severity-1 aging** | Leading | 30–120 d | **Near-certain past 30 days open** | Helpdesk → `priority = urgent/P1`, `status`, `created_at` | `max(days_open)` for P1s | Any P1 open >7 d → risk; >30 d → severe | Mis-triaged priorities (customers who mark everything urgent). Normalize by whether the P1 was accepted as P1 by engineering |
| P6 | **SLA breach count** | Leading | 60–180 d | Moderate–Strong | Helpdesk SLA policy → `first_reply_breached`, `resolution_breached` | Breaches L90; breaches weighted by ticket priority | ≥2 resolution breaches L90, or any P1 breach | Contractual SLA credits issued are a *lagging* confirmation. Track breaches, not credits |
| P7 | **First-contact-resolution (FCR) decline** | Leading | 60–180 d | Moderate | Helpdesk → tickets resolved on first touch / total | FCR rate L90 by account | Drop ≥5 pts vs. account/segment baseline | SQM Group is the standard citation for a near-1:1 FCR↔CSAT relationship and a ~15-pt CSAT penalty per callback `[V]` — vendor research. The account-level FCR sample is often too small to be stable; use segment-level FCR as a leading indicator of *portfolio* risk |
| P8 | **Escalation to management / "executive escalation"** | Leading | 30–120 d | **Strong** | Helpdesk `escalated_at`, CS platform escalation object, exec-to-exec email | Count of formal escalations L180 | Any customer-initiated exec escalation | An escalation handled well is retention-positive. The risk marker is **an escalation with no closed-loop resolution within the committed date** |
| P9 | **Feature request rejection / roadmap denial** | Leading | 120–365 d | Moderate | Product feedback tool (Productboard/Canny/Jira) → request status `wont_do`, `deferred`; linked `account_id` and ARR | Count of `wont_do`/deferred requests by ARR; days since request with no status change | ≥2 rejected/deferred requests from one account, esp. if tied to a documented use case in the success plan | Most requests should be declined. The risk is a **blocking** gap — one tied to a success-plan milestone or an original purchase criterion. Score by "is this on the value path?", not by request count |
| P10 | **Bug backlog attributable to the account** | Leading | 90–240 d | Moderate | Jira → bugs with `reported_by_account`, `status`, `age` | Open bug count and age weighted by severity | ≥3 open confirmed bugs >90 d old | Engaged customers file more bugs. Condition on severity and value-path impact |

---

## 6. Commercial, contract & billing signals (mix of leading and lagging; the leading ones are the highest-precision signals in the taxonomy)

| # | Signal | Lead/Lag | Lead time | Strength | Source → field | Computation | Threshold | Traps |
|---|---|---|---|---|---|---|---|---|
| C1 | **Auto-renew flag turned off** | **Leading** | = notice period + 0–90 d (typically 30–180 d) | **Near-certain** | Billing (Stripe `cancel_at_period_end`, Chargebee, Zuora `AutoRenew`), CLM, CPQ | Boolean change-data-capture on the subscription record | Any transition `true → false` | Sometimes flipped by finance for a re-paper/restructure or a move to a new entity. **Always verify the reason within 24 h** — this is the highest-value single alert in the whole taxonomy because it is unambiguous and time-boxed |
| C2 | **Formal notice of non-renewal received** | **Lagging (decision already made)** | 30–90 d to contract end | Certain | CLM / email / CRM `opportunity.stage = Closed Lost (Churn)` | n/a | n/a | Save rates after formal notice are low; treat all effort here as exception handling, not process |
| C3 | **Seat/quantity reduction at renewal or mid-term** | Leading (for full churn) / Lagging (for the downsell itself) | 180–365 d to *full* churn | Strong | Billing → `subscription_item.quantity` change history | `Δquantity` and `Δquantity/quantity_prior` | Any reduction ≥10%; ≥25% → severe; second consecutive reduction → severe | Seat reductions from customer-side layoffs (F3) behave differently than reductions from disuse (U4). A **downsell is the most reliable predictor of the next-cycle churn** — treat every downsell as an open risk record, not a closed one |
| C4 | **Plan/tier downgrade** | Leading | 180–365 d | Strong | Billing → `plan_id`, `price_id` history | Direction of tier change | Any downgrade | A downgrade to a *better-fitting* plan can improve retention. Check whether the removed tier's features were actually used |
| C5 | **Contract term shortening** | Leading | 180–365 d | **Strong** | CPQ/CLM → `term_months` on the new order form vs. prior | `term_new − term_prior` | 36→12, 12→month-to-month, or any move to a shorter term | Sometimes a procurement-driven standardization or a co-term alignment. Term shortening + price concession is a classic "one more cycle to prove it" pattern — treat as an at-risk renewal that already happened |
| C6 | **Price concession / discount escalation at renewal** | Leading | 365 d | Moderate–Strong | CPQ → `discount_pct` history | Δ discount % renewal-over-renewal | Increase ≥10 pts | Competitive market pressure vs. value-doubt. Read alongside R13 |
| C7 | **Invoice dispute / short payment** | Leading | 60–180 d | Strong | AR/ERP (NetSuite, Sage Intacct) → `invoice.status = disputed`, `credit_memo` issued, partial payment | Count and value of disputes L180 | Any dispute >$0 on a non-billing-error invoice | Genuine billing errors are your fault, not a churn signal — but an *unresolved* dispute aging >45 d is |
| C8 | **Days-sales-outstanding (DSO) deterioration** | Leading | 60–180 d | Moderate | AR → `invoice.due_date`, `paid_at` | Account DSO vs. its own baseline and segment median | +30 d vs. account baseline, or any invoice >60 d past due | Customer-side AP process changes and PO issues. Distinguish "can't pay" (financial distress, F4) from "won't pay" (value dispute) from "AP is broken" |
| C9 | **Payment method removed / not updated after failure** | Leading | 15–60 d | **Near-certain (self-serve)** | Billing → `payment_method` deleted, `card_expiry` passed with no update, dunning attempt counts | Days since failure with no remediation | Card expired >14 d with no replacement, or payment method deleted | In self-serve this is often *involuntary* churn masquerading as intent. Recurly's benchmark network (published rates updated with July 2026 data) puts SaaS monthly churn at **3.22% total / 2.16% voluntary / 1.06% involuntary** `[M]`; involuntary share falls sharply as ARPC rises — from 1.30% at $10–25 ARPC to **0.18% at $250+ ARPC** `[M]`. Paddle/ProfitWell is commonly cited for involuntary being 20–40% of total churn `[V]` |
| C10 | **Dunning sequence entered** | Leading (self-serve) / operational (enterprise) | 7–45 d | Strong | Billing → `invoice.status = past_due`, dunning campaign state | Attempt number, days in dunning | Entry into dunning; escalate at attempt 3 | Enterprise ACH/invoice billing rarely dunning-fails; do not port SMB dunning logic to enterprise |
| C11 | **Billing/pricing/cancellation page visits** | Leading | 7–60 d | **Strong (self-serve) / Weak (enterprise)** | Web/product analytics → pageview on `/billing`, `/pricing`, `/account/cancel`, `/downgrade`; help-center article views on "how to cancel" / "export my data" | Session count on these routes L30; cancellation-flow entries without completion | Any visit to a cancellation route; ≥2 pricing-page visits by an admin in 30 d | Admins visit billing pages for routine invoice retrieval and seat adds. Fire on **cancellation and export help-content**, which has far higher intent purity `[P]` |
| C12 | **Purchase order not issued / budget not allocated** | Leading | 30–120 d | Strong | ERP/CPQ → PO number field empty inside the normal issuance window; CRM renewal opportunity `next_step` | Days to renewal with no PO where PO is required | No PO within 30 d of renewal for a PO-required account | Slow procurement is endemic. The 2025 Customer Revenue Leadership Study (Pavilion / 6sense) found buying-cycle delay correlates with retention: teams reporting normal buying cycles reported **NRR 100%**, vs **93%** (3–6 month delays) and **94%** (6+ month delays) `[M]` |
| C13 | **Renewal opportunity stage stagnation** | Leading | 30–120 d | Strong | CRM → renewal `opportunity.stage`, `last_stage_change_date`, `close_date` slippage count | Days in stage; count of close-date pushes | Stage unchanged for >30 d inside the last 90 d; ≥2 close-date pushes | CRM hygiene noise. Only trustworthy if renewals are actually managed as opportunities |
| C14 | **Multi-year deal expiring into a single-year decision** | Leading (structural) | 90–365 d | Moderate | CLM → original `term_months ≥ 24` and first true renewal decision | Boolean | First renewal after a multi-year term | Multi-year customers have often had *no* renewal scrutiny for years and no relationship muscle memory. Start these 2 quarters earlier than normal |
| C15 | **Consumption below committed minimum (usage-based/hybrid)** | Leading | 90–270 d | **Strong** | Metering/billing → `consumed_units`, `committed_units`, `overage` | `consumption / commitment` pacing vs. days elapsed in term | Pacing <0.70 at 50% of term elapsed → risk; <0.50 → severe (expect a commitment reduction at renewal) | Benchmarkit's 2025 report (CY2024, N=225) found GRR was **92% under usage-based pricing vs 88% under subscription and hybrid**, with usage-based also having the highest bottom quartile (88%) and top quartile (96%) `[M]`; NRR was highest for **hybrid subscription+usage at 110% median** `[M]`. So low pacing predicts *shrinkage* more than logo loss in these models |

---

## 7. Firmographic / external-event signals (LEADING, exogenous, often the true root cause)

| # | Signal | Lead/Lag | Lead time | Strength | Source → field | Computation | Threshold | Traps |
|---|---|---|---|---|---|---|---|---|
| F1 | **Customer acquired / merged** | Leading | 90–540 d | **Strong → near-certain if acquirer runs a competitor** | News/enrichment (Crunchbase, PitchBook, ZoomInfo Intent, Google Alerts) → M&A event on `account.domain` | Boolean + acquirer's known stack | Any announced acquisition | Cuts both ways: acquisition by a *customer of yours* can be an expansion event. The determining variable is the acquirer's incumbent vendor. Escalate to a named exec play within 30 d of announcement |
| F2 | **Leadership change at the customer (CIO/CFO/CRO)** | Leading | 90–365 d | **Strong** | Enrichment / LinkedIn / press releases | Boolean on `seniority = C-level` change in the buying center | Any C-level change in a department that owns your budget | New executives conduct vendor audits in their first 2 quarters. Overlaps with R1 — do not double-count the same person in both |
| F3 | **Layoffs / RIF at the customer** | Leading | 60–270 d | Strong (for downsell), Moderate (for logo churn) | News, layoffs.fyi, LinkedIn headcount trend, enrichment `employee_count` trend | Δ headcount over 90 d; announced RIF % | Announced RIF, or headcount −10% in 90 d | Predicts **seat reduction** (C3) far more reliably than full churn. Model it as ARR-at-risk, not logo-at-risk |
| F4 | **Financial distress / funding drought** | Leading | 90–365 d | Moderate–Strong | Crunchbase `last_funding_date`, credit data (D&B), public filings, news | Months since last raise vs. typical runway; credit score deterioration | >24 mo since last raise for a venture-backed customer; credit downgrade | Bootstrapped and profitable customers trip this falsely. Combine with C8 (DSO) — funding drought + rising DSO is the real pattern |
| F5 | **Reorg / department dissolution** | Leading | 60–240 d | Strong | LinkedIn, R1/R4 contact churn cluster, customer announcement | Count of departures within one department in 90 d | ≥3 contacts from the same department depart in 90 d | The department-level version of R1, and materially worse: the *use case* left, not just the person |
| F6 | **Budget-cycle timing** | Leading (context) | Persistent | Context multiplier | CRM `customer_fiscal_year_end`; enrichment | Days from renewal date to customer fiscal year end/start | Renewal falls within 60 d of the customer's budget lock | Not a risk signal by itself — it is a **timing constraint**. It determines when your window closes. Enterprise budget lock frequently precedes fiscal year start by 60–120 d `[P]` |
| F7 | **Strategic pivot / market exit by the customer** | Leading | 90–365 d | Strong | Earnings calls, press, product announcements | Manual/LLM review of customer public statements | Announced exit from the line of business your product serves | Rare and high-signal. Requires human/LLM reading, not a rule |
| F8 | **Industry-level shock** | Leading (portfolio) | 90–365 d | Moderate | Segment ARR concentration + macro data | Cohort churn rate by industry vs. book average | Segment churn >1.5× book average | Use for portfolio planning and coverage allocation, not per-account scoring |
| F9 | **ICP drift** | Leading (structural) | Persistent | Moderate | CRM firmographics vs. current ICP definition | Boolean `is_in_current_ICP` | Account outside current ICP | Explains chronic under-performance; not actionable at the account level. The 2025 Customer Revenue Leadership Study (Pavilion / 6sense) lists "growth within ICP" as a top acquisition goal for 45% of leaders `[M]` — poor-fit cohorts are an acquisition defect surfacing as a retention number |

---

## 8. Value-realization & success-plan signals (LEADING; the ones a CCO actually cares about)

| # | Signal | Lead/Lag | Lead time | Strength | Source → field | Computation | Threshold | Traps |
|---|---|---|---|---|---|---|---|---|
| V1 | **Unmet success-plan milestones** | Leading | 90–365 d | **Strong** | CS platform success plan object → `objective`, `milestone.due_date`, `status`, `owner` | `% milestones overdue`; `days_since_any_milestone_completed` | ≥1 milestone overdue >30 d; or no milestone completed in 120 d | Lincoln Murphy's framing: churn is a symptom; the disease is customers not reaching their **Desired Outcome**, and Success Milestones are the instrumented path to it `[P]`. Trap: success plans that exist as documents but were never agreed with the customer generate meaningless overdue flags |
| V2 | **No documented ROI / value evidence** | Leading | 180–365 d | **Strong** | CS platform custom fields → `roi_baseline_metric`, `roi_current_value`, `value_evidence_date` | Days since last quantified value artifact | No quantified value artifact in 180 d (enterprise) / 270 d (mid-market) | The absence of evidence is not evidence of absence — but at renewal it functions identically, because the customer's CFO also sees no evidence |
| V3 | **Original use case never went live** | Leading | 90–270 d | **Near-certain** | Sales handoff record `primary_use_case` mapped to a product event | Boolean: has the account ever performed the use-case's core action? | Never, by day 90 post-go-live | Requires an honest use-case→event mapping. Where it exists, this outperforms most usage aggregates |
| V4 | **Value drift: bought for X, using Y** | Leading | 180–365 d | Moderate | Same mapping as V3 | Share of core actions attributable to the sold use case | <0.25 | Using the product for something *else* valuable can be healthy — but the renewal will be evaluated against the original business case unless you re-baseline it |
| V5 | **Stakeholder cannot articulate value** | Leading | 90–270 d | Strong | QBR/EBR notes, call transcripts | LLM/manual assessment of whether the economic buyer states a quantified outcome | Any renewal-cycle conversation where the buyer cannot state the outcome | Subjective; requires disciplined note capture. This is the qualitative twin of V2 |

---

## 9. Silence — the absence signals

Silence is the most under-modeled class because it produces no row in any table. It must be computed as a **derived absence metric**, i.e. a scheduled job that emits a record when nothing happened.

| # | Signal | Lead/Lag | Lead time | Strength | Computation | Threshold (segment-scaled) | Traps |
|---|---|---|---|---|---|---|---|
| Z1 | **No meaningful customer touch in N days** | Leading | 60–270 d | Moderate–Strong | `today − max(last_meeting, last_two_way_email, last_call)` — two-way only; exclude marketing emails, NPS blasts, and automated notifications | Enterprise 45 d; mid-market 60–90 d; SMB/tech-touch 120 d `[P]` | Counting one-way vendor outbound as "touch" is the classic falsification. **Only bilateral interactions count.** |
| Z2 | **No product activity in N days** | Leading | 30–180 d | Strong | `today − max(event_timestamp)` at account level | 14 d for daily-cadence products; 30 d for weekly; 60 d for monthly/quarterly-cadence products | Requires knowing the product's natural cadence per persona. A quarterly-reporting tool with 60 days of silence is fine |
| Z3 | **No support contact in N days from a previously active account** | Leading | 60–180 d | Moderate (strong in the P2 pattern) | `today − last_ticket_created` compared to the account's historical inter-ticket interval | Interval > 3× the account's historical median | Genuinely stabilized accounts. Always pair with Z2 |
| Z4 | **Never-onboarded / dark account** | Leading | 90–365 d | **Near-certain** | Contract active, zero qualifying product events since `contract_start_date` | Any account with `days_since_contract_start > 60` and zero core events | Deployment blocked on a customer-side dependency (data migration, security review). Still churn risk — just a different play |
| Z5 | **Coverage gap (no CSM assigned)** | Leading (vendor-side) | 60–240 d | Moderate | `csm_owner_id IS NULL` or owner is inactive | Any account above the tech-touch ARR threshold with no owner for >30 d | A vendor-side operational defect that reliably shows up later as "customer disengagement" |

---

## 10. Lagging indicators — and precisely why they are too late

| Lagging indicator | Source → field | What it confirms | Why it is too late | The leading signal you should have had |
|---|---|---|---|---|
| Realized logo churn / GRR / NRR | Billing, finance | The period's outcome | The decision preceded this by 3–12 months | Everything above |
| Formal non-renewal notice (C2) | CLM/email | Decision executed | Inside the notice window there is no time to rebuild value; only commercial concessions remain | C1 (auto-renew off), R11/R12 (procurement/termination-terms), T6 (export) |
| Cancellation-flow completion (self-serve) | Product `subscription.cancel` | Decision executed | Seconds of lead time | C11 (cancel-page visits), Z2 (activity silence), C9 (payment method) |
| Downsell booked (C3/C4 realized) | Billing | Value contraction already agreed | Predicts the *next* churn but confirms this one | U4 (seat utilization), C15 (consumption pacing), F3 (layoffs) |
| Health score turning red | CS platform | Composite deterioration already severe | Most scores are dominated by usage aggregates, which are themselves slow (U3-class). The 2025 Customer Revenue Leadership Study (Pavilion / 6sense, ≈800 customer and post-sales leaders) is the source for the widely-quoted finding that **73% of CS leaders say their health score doesn't reliably predict churn** `[M]` (stat verified as attributed to that study; the underlying page in the report was not directly confirmed) | Component-level alerts, not the composite |
| Churn-reason survey / exit interview | Survey tool | Self-reported rationale | Post-mortem only; systematically biased toward "price" | V1/V2/V3 |
| Support escalation to your CEO | Email | Relationship failure already public | Recovery is possible but expensive | P5, P8, S4 |
| SLA credits issued | Billing/legal | Contractual failure realized | Money already refunded, trust already spent | P6 (breach counts), T8 |
| Win/loss of a competitive RFP for your renewal | CRM | You are in a re-bid | You are now selling, not retaining. Re-bids are the terminal state of R11 + R13 | R11, R13, C5 |

**Rule for the analyst:** any indicator whose *definition* references a completed commercial or legal act is lagging. Any indicator that references behavior or relationship state is leading. Health scores built predominantly from `MAU` and `NPS` are lagging composites wearing a leading label.

---

## 11. Compound risk patterns — where the actual predictive power lives

Single signals have poor precision. Named compounds should be pattern-matched and escalated as units. Joint probabilities below are **modeling conventions for prioritization** `[P]` unless marked otherwise — do not present them as measured churn probabilities.

| Pattern name | Component signals | Why it compounds | Typical lead time | Priority | Play |
|---|---|---|---|---|---|
| **Decapitation** | R1 (champion departure) + R4 (single-threaded) + R2 (no exec sponsor) | The only person who understood the value is gone and there is no one to transfer it to. Vendor data puts standalone champion departure at ~51% 12-month churn `[V]`; single-threading removes the recovery path entirely | 90–270 d | P0 | 48-hour exec-to-exec outreach; new-champion onboarding; re-establish the business case from scratch |
| **Quiet quit** | P2 (spike-then-silence) + U1/U7 decay + Z1 (no touch) | The customer tried, failed, stopped asking, and stopped using. Disengagement, not dissatisfaction — so no complaint ever arrives | 60–150 d | P0 | Root-cause the original ticket cluster; re-onboard rather than re-sell |
| **Exit preparation** | T6 (data export) + C1 (auto-renew off) + R11/R12 (procurement/termination terms) | Three independent systems agreeing on intent. Effectively confirmatory | 30–120 d | P0 (save motion) | Treat as a competitive re-bid; escalate to exec sponsor and commercial leadership same-week |
| **Shelfware** | U4 (seat utilization <0.5) + U6 (narrow breadth) + V3 (use case never live) | Money is being spent on nothing. Survives only while the buyer isn't looking; F2 or F4 makes them look | 180–365 d | P1 | Right-size + redeploy: trade a seat reduction for a use-case expansion and a multi-year term |
| **Budget squeeze** | F3 (layoffs) + F4 (financial distress) + C8 (DSO deterioration) + U14 (deprovisioning) | Exogenous. Value is real but affordability is not | 60–270 d | P1 | Protect the logo: term restructure, payment terms, tier down. Optimize for GRR-preserving downsell over logo loss |
| **Regime change** | F2 (new CIO/CFO) + R11 (procurement re-engagement) + R13 (competitor mention) | New exec runs a vendor consolidation review. Vendor data: ~65% of accounts with an executive change don't renew `[V]` | 90–365 d | P0 | Pre-emptive value re-justification with fresh ROI evidence; get in front of the audit rather than responding to it |
| **Technical decoupling** | T2 (integration disconnected >30 d) + T1 (API decline) + T5 (SSO removed) | The product is being unwired from the customer's stack — usually the *implementation* step of a decision already made | 45–120 d | P0 | Immediate technical escalation; a disconnect no one asked you to fix is the tell |
| **Value vacuum** | V2 (no ROI evidence) + R6 (no QBR in 2 quarters) + R2 (exec disengaged) | Nothing to defend the line item with when the budget conversation happens | 180–365 d | P1 | Force a value review with a quantified baseline before the budget cycle, not after |
| **Failed launch** | U9 (TTFV overrun >2×) + U10 (milestones slipped) + U11 (services overrun) + Z4 (dark) | First-year churn is disproportionately an onboarding failure. The 2025 Customer Revenue Leadership Study (Pavilion / 6sense) reports time-to-value as the #1 Acquisition & Onboarding goal for 60% of leaders `[M]` | 180–365 d (predicts renewal #1) | P0 | Executive-sponsored recovery plan with a re-baselined go-live; consider a contract restart/extension rather than a renewal ask |
| **Death by a thousand tickets** | P3 (repeat issue ≥3) + P5 (P1 aging) + S2 (CSAT decline) + P9 (blocking request rejected) | Accumulated unresolved friction — the pattern the IBM/UVic escalation research shows must be measured cumulatively per customer `[A]` | 60–180 d | P1 | Named engineering owner + committed dates + weekly exec-visible closure tracking |
| **Contraction spiral** | C3 (seat reduction last cycle) + U4 falling further + C5 (term shortened) | Each cycle removes another block of ARR. Downsell is the strongest available predictor of next-cycle churn `[P]` | 365 d | P1 | Never close a downsell without opening a risk record for the next cycle |
| **Consolidation target** | F1 (acquisition) + R13 (competitor mention) + T5 (SSO change to acquirer IdP) | The acquirer's stack wins by default absent a fight | 90–540 d | P0 | Map the acquirer's buying center within 30 d; sell the *acquirer*, not the acquired |

**Scoring compounds:** do not sum component scores. Use a multiplicative or rules-based escalation — e.g. `risk = 1 − Π(1 − p_i)` with per-signal `p_i` calibrated on your own churned cohort, or simply hard-escalate any account matching ≥2 components of a named P0 pattern. Additive weighted scorecards systematically under-rank compound accounts because each individual component sits below its own firing threshold.

---

## 12. Segment-specific differences

### 12.1 PLG / self-serve vs. sales-led enterprise

| Dimension | PLG / self-serve | Sales-led enterprise |
|---|---|---|
| Highest-value signal class | Product usage + billing-page/cancel-flow behavior (C11) | Relationship (R-series) + commercial (C-series) |
| Lead time available | Days to weeks | Quarters |
| Cancel mechanics | Self-service, instantaneous → detection must be pre-emptive | Notice period gives 30–90 d of structured warning |
| Involuntary churn share | Material — Recurly network data shows involuntary churn of 1.30% monthly at $10–25 ARPC vs **0.18% at $250+ ARPC** `[M]` | Small; ACH/invoice billing avoids card failure |
| Champion concept | Often absent; the "champion" is the individual user | Central; R1 dominates |
| Useful funnel context | OpenView 2023 Product Benchmarks: website→signup ≈5% (free trial) and ≈9% (freemium), with a wide spread (25th pct 2% for trials; 75th pct 20% for freemium) `[M]` | n/a |
| Retention curve shape | Front-loaded; most loss in the first weeks. Dev-tools benchmarks (boldstart, 2023) show median D7 retention ~30% and D28 ~23% `[M]` | Back-loaded around renewal events |
| Right intervention | In-product, automated, immediate | Human, exec-level, planned quarters ahead |
| Dominant failure mode | Never activated | Never re-justified |

### 12.2 SMB vs. mid-market vs. enterprise

| Dimension | SMB (<$25K ACV) | Mid-market ($25K–$100K) | Enterprise ($100K+) |
|---|---|---|---|
| Expected retention | Structurally lowest. Both Benchmarkit (2025, CY2024, N=225) and SaaS Capital (2025 survey, data through Dec 2024) find **GRR and NRR rise monotonically with ACV** `[M]` | Middle. SaaS Capital reports median NRR **102%** for the $25–50K ACV band (top quartile 111%, bottom quartile 97%) `[M]` | Highest. Benchmarkit's overall medians for CY2024: **GRR 88%, NRR 101%** `[M]`; KeyBanc/Sapphire's 16th annual private SaaS survey (Nov 2025) reports gross retention near 90% and NRR above 100% `[V/M — press summary]` |
| Dominant churn driver | Business failure, affordability, involuntary/payment | Champion departure, unrealized value | Budget cycles, exec change, consolidation, procurement |
| Detection budget | Fully automated; must run on product + billing data only | Hybrid: automated scoring + CSM review | Human-led; signals are inputs to a judgment, not a verdict |
| Practical lead-time target | 14–30 d | 60–90 d | 120–180 d |
| Signals to de-prioritize | R2/R3/R6 (exec sponsor, QBR) — the motion doesn't exist | — | U5 (DAU/MAU) as an absolute; enterprise cadence is legitimately low |
| Signals to prioritize | Z2, C9, C10, C11, U8 | U4, R1, R4, V1 | R1, R2, R11, C1, C12, F1, F2, V2 |

### 12.3 Annual vs. monthly vs. multi-year vs. usage-based

| Contract shape | Detection implication | Notes |
|---|---|---|
| **Monthly / evergreen** | Churn can occur any month → continuous scoring with short windows (7/14 d); billing signals dominate | Monthly-billed cohorts churn materially more than annual-billed; the "annual churns at ~1/3 the monthly rate" figure circulates widely from Paddle/ProfitWell commentary `[V]` — directionally consistent with the ARPC gradient in Recurly's data `[M]`, but do not present the 3× ratio as measured |
| **Annual** | Risk concentrates around the notice window; monitor on a 90/60/30-day pre-renewal cadence with the true deadline at `renewal − notice_period` | Notice periods cluster at 30/60/90 d; 30 d modal in standard-form agreements, 60 d common in negotiated enterprise `[P]` |
| **Multi-year** | Long silence between decisions; risk accumulates invisibly. Start renewal work 2 quarters earlier than for annual (C14) | Multi-year customers frequently have no living relationship at renewal time |
| **Usage-based** | Consumption pacing (C15) replaces seat utilization as the primary leading metric; "churn" often manifests as commitment reduction, not logo loss | Benchmarkit 2025: GRR **92%** under usage-based vs **88%** subscription/hybrid; NRR **110%** median for hybrid subscription+usage `[M]`. Measure NRR on a YoY or TTM basis to absorb seasonality |

### 12.4 Company-lifecycle context (for interpreting your own numbers)

The 2025 Customer Revenue Leadership Study (Pavilion / 6sense, ≈800 customer and post-sales leaders; 6th annual) reports a "mid-life" retention dip: NRR **100%** at 6–10 years of company age vs **93–94%** at 11+ years; GRR **88%** at both 6–10 and 21+ years vs **83%** at 11–15 years `[M]`. Benchmarkit similarly notes GRR declines as companies scale past ~$5M ARR because more renewal cycles have actually been experienced `[M]`. Use this when a CCO asks "is our 85% GRR bad?" — the answer depends on ACV mix, pricing model, and company age, not on a single industry median.

---

## 13. Model construction, calibration and validation

| Requirement | Specification |
|---|---|
| **Minimum lead time** | Fire risk ≥60 days before the churn *decision*; for enterprise annual contracts target ≥120 days |
| **Recall target** | Catch ≥70% of churn events with ≥30 days' notice `[P]`, measured by backtest against the trailing 12-month churned cohort |
| **Precision target** | Precision must be high enough that CSMs act on alerts. Below ~30% precision, alerts are ignored and the system is worse than nothing `[P]` |
| **Backtest method** | Freeze features at T−90, T−180, T−270 relative to each account's churn/renewal date; train on periods strictly before; never leak post-decision fields (`cancel_reason`, `close_date`, `notice_received`) |
| **Class balance** | Annual logo churn in B2B is typically 5–20% of accounts → severe imbalance. Report PR-AUC and lift-at-top-decile, not accuracy. The published SaaS churn-ML study in *Innovation & Management Review* (2025; 4,911 rows, 31 features, 54.5% churn by construction) reports Decision Tree 92.3% accuracy / 87% churn recall, SVM 90.7%/85%, Random Forest 90.6%/85%, ANN 88.6%, Logistic Regression 88% `[A]` — note the balanced class distribution makes these accuracy figures non-transferable to a real 10%-churn book |
| **Feature importance (published example)** | Same study: `age_months` (tenure) 13.4% (DT) / 10.4% (RF); `ticket_product_9-12` (avg. ticket price, months 9–12) 17.1% / 9.1%; product ID 9.5% / 7.8%. Logistic coefficients: `satisfaction_good` −1.21, `ticket_product_9-12` +0.954, `age_months` −0.964 `[A]` |
| **Recalibration cadence** | Quarterly re-weighting; annual full retrain. Signal weights drift with product changes, pricing changes and segment mix `[P]` |
| **Platform mechanics you can rely on** | Mechanics common to CS platform scorecards, whichever platform holds yours: **measures → measure groups → scorecard**; numeric, letter or colour grading schemes; scores set manually or by a rules engine; configurable weights and exceptions; and **validity periods** on manual measures, so a stale grade expires rather than persisting as green. Sub-scores are typically graded on a short fixed scale (0–10) and combined as a weighted average, with a hard cap on component count so the composite stays interpretable. Engagement-style scores are usually recomputed on a rolling window of recent user actions (about two weeks is a common choice) and normalised against comparable accounts. **Kristen Hayer's 7 components:** product usage, customer actions, demographics, company changes, customer relationship, feedback, CSM assessment `[P]` |
| **Composite design rule** | Cap any single category at ~40% of the composite; require at least one *relationship* and one *value* component so the score cannot be gamed by usage alone. Common practitioner weighting is usage ~40 / support ~25 / sentiment ~20 / exec engagement ~15 `[P]` — a starting point, not a benchmark |
| **Alert hygiene** | Every fired signal must carry: signal ID, evidence (the actual numbers), the threshold crossed, the account's baseline, the days-to-renewal, the recommended play, and an owner. An alert without evidence and a play trains CSMs to ignore alerts |

---

## 14. Systematic false-positive traps (checklist before escalating anything)

1. **Absolute thresholds on relative metrics.** Every usage signal must be normalized to the account's own baseline and its cohort. Absolute DAU/MAU floors are the single most common defect.
2. **Ramp accounts scored as decay.** Suppress usage-decay signals for accounts <90 days past go-live; score them on U9/U10/Z4 instead.
3. **Seasonality.** Mask the customer's low season, national holidays, and academic/retail freeze windows before firing decay signals.
4. **Instrumentation change masquerading as churn.** Any release that renames or removes events causes a fleet-wide "decay". Version your event taxonomy and diff account decay against fleet decay.
5. **Vendor-side causes read as customer disengagement.** CSM turnover (R14), coverage gaps (Z5), incidents (T8) and PS resourcing (U11) produce customer-looking signals.
6. **Counting one-way outbound as engagement.** Z1 must use bilateral interactions only.
7. **Champion flags that were never true.** Audit `is_champion` — in most CRMs it is stale or aspirational.
8. **Bounce ≠ departure.** Domain migrations, mailbox quota and security filters all hard-bounce.
9. **Ticket volume without resolution context.** High volume is engagement; unresolved recurrence is risk.
10. **Export/backup with a legitimate cause.** Check for recurring schedules, audit season, and compliance holds before treating T6 as intent.
11. **Auto-renew off for re-papering.** Verify within 24 hours; do not skip verification just because the signal is strong.
12. **Small-sample sentiment.** One detractor in an account with two respondents is not an account NPS.
13. **Double-counting the same human.** R1 (champion), R2 (exec sponsor) and F2 (leadership change) can all fire on one departure.
14. **Additive scoring hiding compounds.** Two sub-threshold signals from different categories are often more dangerous than one severe signal in a single category.
15. **Green health scores at churn.** Test your own score's realized precision/recall before trusting it; the 2025 Customer Revenue Leadership Study (Pavilion / 6sense) found 73% of CS leaders say theirs doesn't reliably predict churn `[M]`.

---

## 15. Source register

| Source | Type | Year / period | What it supports here |
|---|---|---|---|
| Benchmarkit, *2025 B2B SaaS Performance Metrics Benchmarks* (May 2025; CY2024 data; N=225 GRR / N=228 NRR) | `[M]` industry survey | 2025 | GRR median 88% (90%→88% over 3 yrs); NRR median 101% (105% CY21, 103% CY22); GRR/NRR rise with ACV; GRR 92% usage-based vs 88% subscription/hybrid; NRR 110% hybrid subscription+usage; GRR declines past ~$5M ARR |
| SaaS Capital, *What is a Good Retention Rate for a Private SaaS Company in 2025?* (survey through Dec 2024) | `[M]` industry survey | 2025 | NRR by ACV; $25–50K band median NRR 102% (Q3 111%, Q1 97%); median growth 24% for $1M+ ARR |
| Pavilion / 6sense, *6th Annual Customer Revenue Leadership Study* (≈800 customer & post-sales leaders) | `[M]` industry survey | 2025 | 74% of revenue from existing customers; NRR/GRR by company age; buying-readiness→NRR (100% / 93% / 94%); early risk detection top goal (62%); TTV top onboarding goal (60%); customer-enablement function 99% vs 94% NRR; "73% of health scores don't reliably predict churn" |
| KeyBanc Capital Markets & Sapphire Ventures, *16th Annual Private Company SaaS Survey* | `[M]` industry survey (accessed via press release) | Nov 2025 | Gross retention ≈90%, NRR >100%; median ACV $62K for 6-month sales cycles |
| Recurly Research, *Churn Rate Benchmarks* (subscription network) | `[M]` platform data | figures current to Jul 2026 | SaaS 3.22% monthly churn (2.16% voluntary / 1.06% involuntary); involuntary churn by ARPC 1.30% → 0.18% |
| Pendo, *2019 Feature Adoption Report* (615 Pendo subscriptions, >1 yr tenure) | `[M]` product-telemetry study | 2019 | ~80% of features rarely/never used; ~12% of features drive ~80% of daily usage |
| OpenView, *2023 Product Benchmarks*; boldstart dev-tool benchmarks 2023 | `[M]` survey / telemetry | 2023 | Website→signup 5% trial / 9% freemium; dev-tool D7 30%, D28 23% |
| Innovation & Management Review (Emerald), *Churn prediction for SaaS company with machine learning* | `[A]` peer-reviewed | 2025 | Model comparison, feature importances, logistic coefficients |
| University of Victoria / IBM support escalation study, arXiv:1901.01344 | `[A]` peer-reviewed | 2019 | Escalation prediction requires per-customer ticket-history aggregation |
| Sturdy AI research (presented at an industry conference; relayed via a vendor blog) | `[V]` vendor research | 2023–2025 | Champion departure → 51% 12-month churn; 65% non-renewal after exec change; 48-hour response → 33% more likely to renew; 17% of comms contain signals; 31.1M conversations / 3.2B words |
| ProfitWell integrations benchmark; Crossbeam (n=526); Rollworks | `[V]` vendor research | ~2019–2022 | Integration count ↔ retention lift |
| SQM Group | `[V]` vendor research | ongoing | FCR↔CSAT ≈1:1; ~15-pt CSAT penalty per callback |
| CS platform scorecard documentation (several vendors' public product docs) | `[M]` product documentation | current | Concrete scoring mechanics, windows, scales |
| Kristen Hayer (The Success League), *The 7 Components of a Health Score* | `[P]` practitioner | n.d. | Health-score component taxonomy incl. CSM assessment |
| Lincoln Murphy, *Success Milestones / Desired Outcome* (Sixteen Ventures) | `[P]` practitioner | ongoing | Churn as symptom; milestone instrumentation |
| Emilia D'Anzica (practitioner Q&A on multithreading) | `[P]` practitioner | n.d. | Minimum-contacts gate on onboarding completion |
| Alex Turkovic, *Digital Customer Success* (podcast/newsletter/masterclass) | `[P]` practitioner | ongoing | Digital-CS signal→trigger→play architecture for scaled segments |
| Dave Jackson, *Customer-Led Growth*; Pulse Europe 2018 "Predictive Health Score With or Without Usage Data" | `[P]` practitioner | 2018–2021 | Value-delivered health scoring; success plans as the CS core |

---

## Appendix A — Signal priority index (rank order for triage)

Ordered by `strength × lead time × precision`. Use this to decide what to instrument first and what to escalate fastest.

| Rank | Signal | ID | Class | Lead time | Verify within |
|---|---|---|---|---|---|
| 1 | Auto-renew flag off | C1 | Commercial | 30–180 d | 24 h |
| 2 | Champion departure | R1 | Relationship | 90–365 d | 48 h |
| 3 | Termination-terms / data-portability request | R12 | Commercial-legal | 30–120 d | 24 h |
| 4 | Bulk data export by a non-routine admin | T6 | Technical | 15–90 d | 48 h |
| 5 | Integration disconnected >30 d unrepaired | T2 | Technical | 45–120 d | 72 h |
| 6 | SSO / IdP decoupling | T5 | Technical | 30–90 d | 24 h |
| 7 | Original use case never went live | V3 | Value | 90–270 d | 1 week |
| 8 | Seat utilization <0.40 | U4 | Usage | 90–270 d | 1 week |
| 9 | Spike-then-silence in support | P2 | Support | 60–150 d | 1 week |
| 10 | Procurement/legal re-engagement off-cycle | R11 | Commercial | 60–180 d | 48 h |
| 11 | Executive change in the buying center | F2 | Firmographic | 90–365 d | 1 week |
| 12 | Unresolved P1 aging >30 d | P5 | Support | 30–120 d | 24 h |
| 13 | Consumption pacing <0.50 at mid-term | C15 | Commercial | 90–270 d | 1 week |
| 14 | Deprovisioning burst >25% of users | U14 | Usage | 30–120 d | 72 h |
| 15 | Core-action depth <0.60 of baseline, 2 periods | U7 | Usage | 60–150 d | 1 week |
| 16 | Meeting no-shows ≥2 consecutive | R5 | Relationship | 60–180 d | 1 week |
| 17 | Contract term shortening | C5 | Commercial | 180–365 d | at renewal |
| 18 | No ROI evidence in 180 d | V2 | Value | 180–365 d | 2 weeks |
| 19 | Competitor mention by economic buyer | R13 | Relationship | 60–180 d | 1 week |
| 20 | Success-plan milestone overdue >30 d | V1 | Value | 90–365 d | 2 weeks |

---

## Appendix B — Source-system → field crosswalk

| Source system | Representative objects/fields to ingest | Signals fed |
|---|---|---|
| **Product analytics** (Pendo, Amplitude, Mixpanel, Heap, Snowplow) | `event_name`, `user_id`, `account_id`, `timestamp`, feature keys, `session_start`, `environment` | U1–U8, U16, U17, Z2 |
| **App / production DB or warehouse** (Snowflake, BigQuery, Databricks) | `last_login_at`, `records_created`, `storage_bytes`, `workflow_runs`, `user_deactivated_at` | U12–U14, Z2, Z4 |
| **Identity / SCIM** (Okta, Entra ID, JumpCloud) | app assignment counts, SAML/OIDC config changes, deprovisioning events | U13, U14, T5 |
| **API gateway / metering** (Kong, Apigee, Cloudflare, internal metering) | `api_calls` by endpoint class, `api_version`, `user_agent`, `records_processed` | T1, T4, C15 |
| **Integration platform** (native connectors, Paragon, Merge, Workato) | `connection.status`, `token_expires_at`, `last_successful_sync_at`, `consecutive_failure_count` | T2, T3 |
| **Helpdesk** (Zendesk, Intercom, Freshdesk, Salesforce Service Cloud) | `ticket.id/type/priority/status`, `satisfaction_rating.score`, `escalated_at`, SLA policy breaches, comment counts, tags | P1–P8, S2, S3, Z3 |
| **Engineering** (Jira, Linear) | bug `severity`, `age`, `reported_by_account`, feature-request `status` | P9, P10 |
| **CRM** (Salesforce, HubSpot) | Contact `title`, `department`, `seniority`, `email_bounce_status`, `is_champion`; Opportunity `stage`, `close_date`, `next_step`; Account `fiscal_year_end`, `csm_owner_id`, `executive_sponsor_contact_id` | R1–R5, R14, C13, F6, Z5 |
| **CS platform** | Scorecard measures, success-plan objectives/milestones, CTAs/playbooks, activity timeline, manual sentiment, `validity_period` | S4, V1, V2, R6, Z1 |
| **Calendar / email** (Google Workspace, Microsoft 365) | `responseStatus`, attendee list, thread timestamps, reply direction | R5–R8, Z1 |
| **Conversation & comms intelligence** (Gong, Chorus, Sturdy, Enterpret, Unwrap) | transcript topics, competitor tracker hits, per-sentence sentiment, risk tags | R9, R10, R13, V5 |
| **Billing / subscription** (Stripe, Chargebee, Zuora, Recurly, Maxio) | `cancel_at_period_end`, `subscription_item.quantity`, `plan_id`, `payment_method`, `invoice.status`, dunning state, metered usage vs commit | C1, C3, C4, C9, C10, C15 |
| **ERP / AR** (NetSuite, Sage Intacct, Workday) | `invoice.due_date`, `paid_at`, `credit_memo`, disputes, PO numbers | C7, C8, C12 |
| **CLM / CPQ** (Ironclad, DocuSign CLM, Conga, Salesforce CPQ) | `term_months`, `notice_period_days`, `auto_renew`, `discount_pct`, clause-lookup activity | C1, C5, C6, C14, R12 |
| **Survey** (Delighted, Qualtrics, GetFeedback, Medallia) | `nps_score`, `csat`, `ces`, `respondent_role`, `response_date` | S1–S3 |
| **LMS / community** (Skilljar, Docebo, Intellum, Circle, Discourse) | course completions, certification expiry, community MAU | R15 |
| **Enrichment / news** (ZoomInfo, Clearbit, Crunchbase, PitchBook, Google Alerts, layoffs.fyi) | job-change alerts, `employee_count` trend, funding events, M&A, leadership changes | F1–F5, F7, R1 |
| **PSA / services** (Kantata, Certinia, Jira) | milestone `due_date`/`completed_date`, `hours_burned/hours_sold`, change orders | U10, U11 |
| **Web analytics** (GA4, Segment, internal) | pageviews on `/pricing`, `/billing`, `/account/cancel`; help-center article views | C11 |
| **Incident management** (PagerDuty, Statuspage) | incidents mapped to affected tenants, Sev level, degradation minutes, SLA credits | T8, P6 |

---

## Appendix C — Renewal-clock operating cadence (annual enterprise contracts) `[P]`

All day counts are **relative to the effective decision deadline** = `renewal_date − notice_period_days`, not to the renewal date.

| Window | Objective | Signals reviewed | Exit criteria to advance |
|---|---|---|---|
| **T−270 to T−180** | Value baseline established | V1, V2, V3, U4, U6, R2, R3 | Documented ROI baseline + named exec sponsor + success plan with future-dated milestones |
| **T−180 to T−120** | Value evidence produced and socialized | V2, V5, R6, U7, C15 | Quantified value artifact delivered to the economic buyer; QBR/EBR held with exec attendance |
| **T−120 to T−90** | Commercial intent tested | C1, C12, C13, R11, C6, F6 | Verbal intent to renew from the economic buyer; budget confirmed; PO path known |
| **T−90 to T−60** | Paper in motion; risk fully surfaced | C1, C13, R12, T6, R13 | Order form issued; all open P1s and blocking requests have committed dates |
| **T−60 to T−30** | Close and de-risk | C13, R5, C7, C8 | Signature obtained or a named exec save plan is running |
| **T−30 to T−0** | Exception handling only | All P0 patterns | Escalation to CRO/CCO; concession authority pre-approved |

**Trigger to compress the timeline:** any P0 compound pattern from §11 pulls the account into the T−90 posture immediately, regardless of actual days remaining.
