# Loss Review Record — template

> Emit verbatim. Every field is populated or written `UNKNOWN — requires <source>`; no row is
> dropped for having no data. Internal document: nothing here reaches a customer in any wording.

---

# Loss Review — <Account> · decided <decision_date> · $<arr_lost> ARR
**Internal document.** Contains risk and attribution language that must never reach a customer.
**Run on:** <scope> · facilitator <name> · account owner <name> · data as-of <date>.
<One line naming anything taken as a default rather than answered.>

## Bottom Line
<Four sentences: what we lost, the root cause in one clause, the detection lag, and the one fix
with its owner and date.>

| | |
|---|---|
| ARR lost | $X (<full churn / quasi-churn / tier downgrade / seat churn>) · tenure <N> months · renewal number <N> · segment <segment> |
| Decision date | <date> — basis `<observed / inferred_autorenew / …>` · notice <date> · effective <date> |
| Opt-out deadline that governed | <date> — decided <N> days <before/after> it · save window <notice − decision> days |
| **Was a decision made?** | <**Yes** — `active_decision_evidence`: <dated events> / **No — the renewal lapsed**, coded `<no-decision / deprioritised / budget-freeze / orphaned-renewal / budget-loss>`> |
| **Decision-process vs competitive** | Decision-process **<n>/5** — <markers> · Competitive **<n>/5** — <markers> · `decision_owner_vacancy_days` <N or UNKNOWN — no decision owner was ever identified> |
| Stated reason · root cause | "<verbatim>" — <name, role, date, how asked> → <one clause, vendor-side> |
| **Detection lag** | **<N> days** — detectable <date>, flagged <date>, first intervention <date> · failure mode `<mode>` |
| Savable | `<A / B / C / D>` — `<sub-code>` · Green at T−90? <Yes → scoring defect / No, band was <band>> |
| Systemic fix | <fix> — <owner> — by <date> · Confidence <High/Medium/Low> (<criteria met>) |

## 1. Timeline — T−540 → T−0
| Day | Date | Family | Event | Evidence | Tier | Known then? |
|---|---|---|---|---|---|---|
| T−<N> | <date> | <family> | <one clause, past tense, factual> | `[system · field · date]` | Observed/Inferred | Yes/No |

**Families with no retained history:** <list, with the retention horizon of each source.>

## 2. Stated reason vs proximate cause vs root cause
| | Content | Evidence | Where they diverge |
|---|---|---|---|
| **Stated** | "<verbatim>" | <who, role, date, how it was asked> | |
| **Proximate** | <the dated event that converted decay into decision> | `[system · field · date]` | |
| **Root** | <the vendor-side condition we own and can change> | Five whys, §5 | |

## 3. Earliest detectable signal
| Signal | Detectable date | System that held it | Alert existed? | First flagged | First intervention |
|---|---|---|---|---|---|
| <ID + name> | <date> (T−<N>) | `<system · field>` | <no / yes, threshold X> | <date> (T−<N>) | <date> (T−<N>) |

```
detection_lag   = <decision> − <detectable>   = <N> days
recognition_lag = <flagged>  − <detectable>   = <N> days
realised_lead   = <decision> − <flagged>      = <N> days
action_lag      = <intervention> − <flagged>  = <N> days
identity check  : recognition_lag + realised_lead = detection_lag  ✓
```
**Failure mode: `<mode>`.** <One sentence on what this mode implies for the fix and who owns it.>

## 3a. Was a decision made? — the two-axis score
Scored before the taxonomy, and before any competitor is named. Neither axis may be left blank;
neither substitutes for the other. Rubric and markers: `../references/root-cause-taxonomy.md` §3a.

| Axis | Score | Markers present (each with its dated evidence) |
|---|---|---|
| **Decision-process** | <n>/5 | <C13 stalled opportunity · C12 no PO / F6 freeze · F5/F2 reorg · R1/R3 owner left, no successor · Z1 60 silent days — list only those evidenced, each with `[system · field · date]`> |
| **Competitive** | <n>/5 | <R13 rival named by an economic buyer · R11 re-bid or RFP · R12 termination terms beside a named alternative · replacement confirmed by a second independent source · C6 concession demanded against a named price> |

| Field | Value |
|---|---|
| `active_decision_evidence` | <the dated events proving a decision was run, or **empty — the renewal lapsed**> |
| `decision_owner_vacancy_days` | <N> · last dated interaction with a renewal decision-holder <date, name, role> — or `UNKNOWN` |
| `competitor_claimed` | <a rival named but never confirmed by a second source, or `none`> |

**Reading:** <one sentence naming the higher axis and what it forces.> Where decision-process ≥3
and competitive ≤1, §7 may not propose a competitive fix — no battlecard, no enablement, no price
response. Where competitive < 3 or the replacement is unconfirmed, `primary_reason` may not be
`competitive-displacement`.

## 4. Classification
| Field | Value |
|---|---|
| `primary_reason` | |
| `secondary_reason` | |
| `locus` | |
| `origin_stage` → `surfaced_stage` | <where it started> → <where it showed up> |
| `type` (impact) | |
| `competitor` | <named **and confirmed by two independent sources** / none / in-house / no-replacement> |
| `decision_process_score` · `competitive_score` | <n>/5 · <n>/5 |
| `stakeholder_change_involved` | <yes, role / no> |

## 5. Five whys — why did *we* not prevent it
1. **Why did they not renew?** <fact + `[evidence]`>
2. **Why <that>?** <fact + `[evidence]`>
3. **Why <that>?** <fact + `[evidence]`>
4. **Why <that>?** <fact + `[evidence]`>
5. **Why <that>?** <fact + `[evidence]`>

**Root cause:** <the thing we own and can change.>
**Stop rule applied:** <own-and-change / pre-headcount / redirected from human error.>

## 6. Savability and attribution
**Verdict: `<A/B/C/D>` — `<sub-code>`.** <Two sentences, including what a save would have cost in
hours and dollars, and whether that cost was worth paying.>

| Function | Weight | Mechanism (never a person) | What would have had to be different | Seen before? |
|---|---|---|---|---|
| | % | | | Nth time |
| **Total** | **100%** | | | |

<Owner's dissent, if any — one line with its reasoning.>

## 7. Systemic fix
| # | Action | Owner | By | Expected effect | Success measure |
|---|---|---|---|---|---|
| 1 | <the one primary fix> | <function lead> | <date ≤90 days> | <what changes for the class of account> | <observable, dated> |

**Matches the higher axis:** <decision-process / competitive — and which score it answers.>
**Not doing:** <the rejected fix, and why.>

## 8. Model feedback
| Change | Current | Proposed | Evidence (N records) | Backtest | Alert budget | Owner | By |
|---|---|---|---|---|---|---|---|
<Or: "No change — N=1. `<signal>` added to the watch list; revisit at 3 records.">

## 9. Win-back posture
| Re-approach after | Trigger event | What would have to be true | Who holds the relationship |
|---|---|---|---|

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | | | <a concrete consequence, not "may affect results"> |

### Coverage Ledger
| Signal family | Source checked | History retained to | Status | Notes |
|---|---|---|---|---|
| Product usage & adoption | | | ✅/⚠️/❌ | |
| Commercial & contract | | | | |
| Relationship & engagement | | | | |
| Support & reliability | | | | |
| Sentiment & VoC | | | | |
| Billing & payment | | | | |
| Firmographic & external | | | | |

**Coverage: X / 7 (Y%) → confidence capped at <level>.**
Blind spots: <which families are missing, how far back history actually reaches, and what that
gap hides. The usual casualty is the earliest detectable date — it moves later than the truth,
which makes the detection lag look better than it was.>
