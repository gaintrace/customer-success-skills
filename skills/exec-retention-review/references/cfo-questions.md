# The Questions a CFO and a Board Member Actually Ask

> Thirty-two questions, the arithmetic each requires, the data you must have loaded before you
> walk in, and the trap inside each one. Prepare the top eight verbatim. The rest you should
> be able to answer from the appendix in under thirty seconds.

**Contents**
1. [How to use this](#1-how-to-use-this)
2. [The eight you will always get](#2-the-eight-you-will-always-get)
3. [Definitional and methodology questions](#3-definitional-and-methodology-questions)
4. [Segment, cohort and mix questions](#4-segment-cohort-and-mix-questions)
5. [Concentration and dependency questions](#5-concentration-and-dependency-questions)
6. [Forecast and credibility questions](#6-forecast-and-credibility-questions)
7. [Cost, headcount and payback questions](#7-cost-headcount-and-payback-questions)
8. [The hostile questions](#8-the-hostile-questions)
9. [Answers you are allowed to give](#9-answers-you-are-allowed-to-give)
10. [Who asks what](#10-who-asks-what)
11. [The rehearsal protocol](#11-the-rehearsal-protocol)

---

## 1. How to use this

Three rules make the difference between answering and surviving.

| Rule | Why |
| --- | --- |
| **Answer the question asked, then stop.** | Volunteering a second number invites a second question you have not prepared. |
| **Lead with the number, then the method.** | "104.2%, cohort basis, Enterprise only" beats a sentence of setup. |
| **If you do not know, say the number you will send and the date.** | "I do not have that split loaded; you will have it by Thursday" costs nothing. Guessing costs the room. |

Load these five artifacts before the meeting so that a live query is a lookup, not a promise:
the segment cut, the cohort triangle, the top-20 account list with ARR and opt-out dates, the
frozen forecast snapshots for the last four quarters, and the reason-coded churn list.

**The 30-second answer shape.** Every answer below fits this and nothing longer:

| Beat | Length | Example |
| --- | --- | --- |
| The number | 1 clause | "104.2%." |
| The basis | 1 clause | "Cohort method, Enterprise, TTM." |
| The one thing that explains it | 1 sentence | "Two accounts contributed 61% of Enterprise expansion." |
| What you would need to say more | only if asked | "Split by product is in A1." |

If an answer runs past four sentences, you are presenting rather than answering, and the next
question will be sharper than the one you just took.

---

## 2. The eight you will always get

| # | Question | The arithmetic | Data you must have loaded | The trap |
| --- | --- | --- | --- | --- |
| 1 | **Is that NRR move mix or performance?** | Shift-share: `ΔNRR = Σ(Δwᵢ)NRRᵢ,₀ + Σwᵢ,₀(ΔNRRᵢ) + Σ(Δwᵢ)(ΔNRRᵢ)` | Segment weights at t0 and t1, segment NRR both periods | Reporting only "mix" and folding the interaction term into it — that is how you accidentally claim or dodge credit |
| 2 | **What is the retention of the newest cohort?** | M3/M6 dollar and logo retention for the last 4 cohorts, at equal tenure | Cohort triangle with immature cells greyed | Quoting an M12 number for a cohort that is 5 months old. It does not exist |
| 3 | **What happens if the top account leaves?** | Recompute GRR and NRR with that account churned at renewal; also state top-1 share and opt-out date | Top-20 list, per-account ARR, opt-out deadlines | Answering in ARR only. They want the *rate* impact, because that is what the next investor sees |
| 4 | **Is churn concentrated or broad?** | `1 − GRR` vs logo churn; churned-account size index = `avg ARR of churned / avg ARR of all`, computed **inside each segment** | Churn list with ARR and segment | A blended index of 0.83 can hide an SMB index of 1.67. The blend inverts the answer |
| 5 | **What is the payback on CS headcount?** | `(ARR protected × attributable save uplift × gross margin) / fully loaded cost`, with the counterfactual stated | Coverage gap, historical save rate by coverage tier | Claiming 100% of retained ARR as attributable. Claim the delta, not the total |
| 6 | **How accurate was last quarter's forecast?** | `1 − abs(Called − Closed)/Called`, plus WAPE and **signed bias**, graded from the frozen T-90 and T-30 snapshots | Four quarters of snapshots | Reporting accuracy without bias. A book with offsetting errors looks accurate and is not |
| 7 | **How much of the churn did you see coming?** | Risk detection rate = `ARR flagged ≥60d before loss / total ARR lost` | Dated risk flags with timestamps | Backfilling flags after the loss. If the flag date is not immutable, the metric is theatre |
| 8 | **What would you do if we said no to the ask?** | The counterfactual: what is not done, what the exposure becomes, what you would try instead at zero cost | The prioritised list of what the hire would displace | Threat inflation. A CFO funds an argument that concedes its weakest point |

---

## 3. Definitional and methodology questions

| # | Question | How to answer | The trap |
| --- | --- | --- | --- |
| 9 | "Is that GRR cohort method or formula method?" | Name it, and state the gap. The formula method typically understates GRR and **overstates** NRR relative to cohort, because in-year new logos' churn and expansion leak in | Not knowing which one your BI tool uses |
| 10 | "Does that ARR include CARR?" | ARR excludes signed-not-live contracts; CARR includes them. Show them separately or not at all | Quoting CARR as ARR inflates growth and every retention denominator |
| 11 | "Is reactivation in NRR?" | No. Reactivation is a bridge line and a growth line; it is excluded from cohort NRR/GRR because the account was not in the t0 cohort | Including it adds ~100bps of fake retention |
| 12 | "Constant currency?" | Yes with the rate date, or no with the FX line shown separately in the bridge | Presenting an FX swing as retention movement |
| 13 | "Does expansion include contracted ramp?" | Flag ramp separately. A pre-signed step-up is not a CS or sales win in the period it lands | Booking ramp as expansion inflates NRR with no motion behind it |
| 14 | "Is usage overage in the ARR base?" | State the policy and never change it retroactively. Usage-based businesses must use TTM or a two-year look-back, never single-month | A retroactive basis change invalidates every trend you have published |
| 15 | "What is the win-back window?" | Commonly 30–90 days. Re-signs outside it are New, not never-churned | An undeclared window lets a churn become an invisible non-event |
| 16 | "Why did this metric change definition?" | The change log entry, the reason, and the restated prior periods, shown as-reported and pro-forma | A silent restatement destroys every number you have ever published |
| 17 | "Is that gross renewal rate or GRR?" | Different denominators. Gross $ renewal rate = `Renewed ARR / ATR`; GRR uses the whole base. Renewal rate is normally **lower** because ATR is the smaller denominator | Benchmarking one against the other's benchmark |

---

## 4. Segment, cohort and mix questions

| # | Question | The arithmetic | The trap |
| --- | --- | --- | --- |
| 18 | "What is NRR by ACV band?" | Segment by ACV band first — it is the most predictive cut [M: SaaS Capital 2025; Benchmarkit 2025] | Segmenting only by employee count and then wondering why benchmarks do not fit |
| 19 | "Which segment is dragging?" | Share-of-variance: `segment contribution to the miss / total miss` in dollars and percent | "SMB is soft" without the percentage of the variance it explains |
| 20 | "Are cohorts improving?" | Read **down** the M6 and M12 columns across the last 8 cohorts | Reading across a row, which just describes ageing |
| 21 | "Where in the lifecycle do we lose people?" | Hazard by tenure bucket: 0–90d, 91–180d, 181–365d, Y2, Y3, Y4+ | Front-loaded and back-loaded churn need opposite investments; a cumulative survival curve hides which you have |
| 22 | "Does churn differ by acquisition channel?" | Logo and $ churn by `original_lead_source`, cohorted | A demand-gen quality problem presented as a CS performance problem, or the reverse |
| 23 | "What is NRR excluding the top three accounts?" | Recompute on the base minus those accounts | Not having it loaded. This question is asked live and answered live |
| 24 | "Is expansion broad or from a few accounts?" | Count of expanding accounts, and top-5 share of expansion ARR | A 110% NRR carried by two accounts is not a motion, it is luck |
| 24a | "How much of expansion is price versus volume?" | Average renewal uplift = `(Renewed ARR at new price − Renewed ARR at prior price) / Renewed ARR at prior price`, on renewals that added no units. Compare it to the list-price increase to get price realisation % | Presenting a price increase as adoption-driven growth. A CFO can see the difference in the billing data |
| 24b | "Does retention differ by product?" | GRR/NRR per SKU on the same cohort, plus multi-product attach rate and the retention delta between 1-product and 2+-product accounts | Netting expansion on SKU A against contraction on SKU B and reporting only the sum |
| 24c | "What is retention for accounts that completed onboarding versus those that did not?" | Cohort GRR split by an onboarding-completion flag and by whether TTV target was met | This is the single most persuasive slide for an onboarding investment — and the one most companies cannot produce because the flag was never stored |

---

## 5. Concentration and dependency questions

| # | Question | How to answer | The trap |
| --- | --- | --- | --- |
| 25 | "What is our top-10 concentration and where is it going?" | Top 1/5/10/20 share plus the Herfindahl index, this year and last | A single number hides whether the distribution is flattening or steepening |
| 26 | "Any customer over 10% of revenue?" | Name it. Under US GAAP a single external customer at ≥10% of revenues is a disclosure item (ASC 280-10-50-42); common investor red flags are >10% single and >25% top 5 [P] | Being told this by the auditor rather than saying it yourself |
| 27 | "How exposed are we on the top-10 renewals?" | The top-10 renewal calendar **by opt-out deadline**, with risk band, exec sponsor and count of live contacts per account | Bucketing by renewal date, which shows exposure that has already resolved |
| 28 | "Is any of that revenue dependent on one person?" | Contacts-live count per top-10 account; single-threaded accounts named | ARR tables show dollars, never dependency. This is the question that finds the real risk |

---

## 6. Forecast and credibility questions

| # | Question | How to answer | The trap |
| --- | --- | --- | --- |
| 29 | "Has your forecast been biased in one direction?" | Signed bias over four quarters. Sustained bias is a coaching problem, not a model problem | Reporting absolute accuracy only |
| 30 | "How much did the T-90 call move?" | Vintage table: T-90 → T-60 → T-30 → closed, by quarter. The movement measures early-warning quality | Grading a forecast that was edited all quarter — that measures field hygiene [V] |
| 31 | "Is that save rate real?" | Publish written entry/exit criteria and the risk detection rate beside it | An undisciplined at-risk list inflates the save-rate numerator; teams flag everything |

---

## 7. Cost, headcount and payback questions

| # | Question | How to answer | The trap |
| --- | --- | --- | --- |
| 32 | "What does CS cost as a percentage of ARR?" | Fully loaded CS + Support opex / ARR. Reference: median **9% of ARR** across 1,000+ private B2B SaaS [M — SaaS Capital 2026 Spending Benchmarks]; equity-backed companies spend roughly 2× bootstrapped [M] | Quoting CS-only cost against a benchmark that includes Support, or vice versa |
| — | "Is expansion cheaper than new logo?" | Expansion CAC ratio median **$1.00** vs new-logo CAC ratio **$2.00**, CY2024 [M — Benchmarkit 2025, N=21 and N=73]. Fewer than 20% of companies compute it [M] | Asserting it without computing your own. The peer median is the argument's setup, not its proof |
| — | "What is the right ARR per CSM?" | There is **no current Grade-A public benchmark**. Every range in circulation is a CS-platform content aggregation or a rule of thumb [P] — quote none of them as a peer number. Derive yours by plotting book size per CSM against GRR and expansion, and name the point where they degrade | Importing a vendor ratio as a target. It is a capacity constant, not a benchmark |

---

## 8. The hostile questions

These are asked to test whether you are the person to fund. Answer them flatly.

| Question | The answer that works | The answer that loses the room |
| --- | --- | --- |
| "Why should we believe this number when last quarter's was wrong?" | "Last quarter I called $19.8M and closed $18.9M — 4.8% optimistic. The bias came from Commit accounts with no economic-buyer contact in 60 days. That is now a hard gate on Commit, and this quarter's call excludes $1.4M that would previously have qualified." | "Forecasting is hard." |
| "Is this a CS problem or a product problem?" | "Both, and here is the split: $1.9M of $3.1M is reason-coded *never reached go-live*, which is mine. $0.7M is coded *missing SSO*, which is roadmap. The remaining $0.5M is M&A consolidation, which is neither." | "It's complicated." |
| "Are you just flagging everything as at-risk to protect yourself?" | "At-risk has written entry and exit criteria and a date. The check is the detection rate: 56.5% of lost ARR was flagged ≥60 days out. If I were over-flagging, that number would be near 100% and the save rate would be near 100% too. Neither is." | "No, we're disciplined about it." |
| "You asked for two heads last year. What did we get?" | "Two SMB onboarding FTEs, $340k. SMB 90-day activation went 48% → 71%; SMB M6 dollar retention went 79% → 86% across the three cohorts they touched. I cannot fully attribute it — the pricing change landed in the same window — so I claim the cohort delta, not the whole movement." | A number with no counterfactual. |
| "Why is your health score not predicting this?" | "It is not, and I am not going to defend it. Red-tier churn is 1.4× Green-tier; it should be at least 3× to be worth a slide [P]. I have removed it from this pack and I will bring back a scored model with a backtest, or nothing." | Defending a score with no measured lift. |
| "Could you do this with less?" | The digital/pooled alternative, costed, with the retention delta it would cost you — offered before they ask twice. | "No." |

---

## 9. Answers you are allowed to give

| Situation | Permitted answer | Forbidden |
| --- | --- | --- |
| You do not have the split loaded | "I do not have that loaded; you will have it by Thursday." | An estimate spoken as a fact |
| The data does not exist | "`UNKNOWN — requires <source/field>`. We do not have a VoC source connected, so I cannot attach ARR to detractor themes. That connection is in the ask." | Substituting an industry benchmark for a company number |
| The signals genuinely conflict | "Usage is up 34% and auto-renew was switched off. The growth is in one team; the buying team has gone to zero. I trust the commercial signal." | Smoothing the conflict into one clean answer |
| Asked to predict a specific account | "Very likely to churn absent intervention" plus the named intervention and the date you will know | "They will churn", "guaranteed", "100%" |
| Asked for a probability | A band, with what the band means — unless the model has been backtested, in which case state the calibration ("model v3, 412 renewals, Brier 0.14, this band renewed 31% of the time") | A two-significant-figure probability from a rules-based score |
| The quarter was bad | The six-part structure in `bad-news.md`: name it, quantify it, separate what you knew from what you did not, state the change, state the leading indicator, stop | Burying it in the appendix, or trading it for a discount |

---

## 10. Who asks what

The same pack is read through four different lenses. Prepare for the lens, not the person.

| Asker | What they are actually testing | Their opening question, typically | What satisfies them |
| --- | --- | --- | --- |
| **CFO** | Whether your numbers tie and whether your forecast is a plannable input | "Does this tie to our ARR balance?" | A reconciliation with $0 variance and a signed-bias number |
| **Board member (investor)** | Whether the business is structurally improving, and whether the next round's diligence will hold | "Are the newest cohorts better?" | A cohort triangle read down the column, and concentration stated before they ask |
| **Board member (independent / operator)** | Whether you know your own weakest point | "What is the one thing you would fix?" | One issue, named, with a cost and a date |
| **CEO** | Whether they are about to be surprised in front of the board | "Is there anything in here I have not seen?" | Nothing — because you pre-briefed 48 hours ago |
| **Investor update reader (async)** | Whether the written number matches the verbal story from last quarter | — | Consistency of definitions across updates, and bad news in writing first |

**The pre-brief rule that prevents most damage:** any figure moving more than your stated
materiality threshold is walked through 1:1 with the CEO and CFO at least 48 hours ahead. The
board meeting is where you present the plan, not where anyone learns the news. A director who
hears a material number for the first time in the room will spend the rest of the meeting
testing what else you did not say.

---

## 11. The rehearsal protocol

Run this the day before. It takes forty minutes and it is the difference between a pack that
survives and one that gets picked apart.

| Step | Action | Pass criteria |
| --- | --- | --- |
| 1 | Read the pre-read aloud, timed | Under 90 seconds, and it contains the ask |
| 2 | Have someone ask the eight questions in §2, cold | Every answer under 30 seconds, with a number first |
| 3 | Open each slide and say the one sentence it exists to prove | If a slide needs two sentences, it is two slides or it is appendix |
| 4 | Hand the deck to someone who does not run CS | They can state the driver and the ask unprompted |
| 5 | Check every rate for its denominator, every benchmark for its citation | Zero exceptions |
| 6 | Name the number most likely to be challenged, and rehearse that answer twice | You are not surprised by it in the room |
| 7 | Confirm the CEO and CFO pre-briefs happened, with dates | Recorded at the top of the pack |

**Sources.** Benchmarkit *2025 B2B SaaS Performance Metrics Benchmarks* [M]; SaaS Capital
*2025 Retention Benchmarks* and *2026 Spending Benchmarks* [M]; ChartMogul *SaaS Retention
Report*, Sept 2025 [M]; SaaS Metrics Standard Board (NRR/GRR/logo standards) [M]; FASB ASC
280-10-50-42 (major-customer disclosure). No public ARR-per-CSM benchmark is cited here,
because none of Grade-A quality exists; renewal-forecast-accuracy targets are vendor claims
[V] with no clean public benchmark either.
