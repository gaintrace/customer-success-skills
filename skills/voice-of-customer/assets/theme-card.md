# Theme Card — emit verbatim

> One theme, one screen. If it does not fit on one screen, run the split test in
> `../references/theme-taxonomy.md` §6. Internal document.

```markdown
### T<rank> — <THEME-CODE> <theme name> · <Category> · Priority <rank> of <N>

**Attributed ARR $<X> across <n> accounts · Risk-weighted $<Y> · Renewal exposure $<Z> (≤120d)
· Mean severity <s.s> · <emerged|growing|flat|fading|resolved|newly visible> · Evidence
<Confirmed|Supported|Anecdotal|Unreplicated>**

**Claim (customer's language):** <one sentence, quoted or near-quoted from the corpus>
**Stated as:** <what customers call it>
**Assessed cause:** <what the evidence says it is> — *<observed | inferred; if inferred, the rule>*

#### Evidence
| Account | Segment | ARR | Health band | Role | Channel | Date | Verbatim | Sev | Source ref |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | "<quote, truncated not paraphrased>" | | <ticket/interaction id> |

**Channels represented:** <n> of <m> · **Segments represented:** <list> ·
**Economic-buyer mentions:** <n>

#### Behaviour cross-check
| Account | Says | Does | Reading | Tiebreak rule applied |
|---|---|---|---|---|
| | <sentiment signal + date> | <usage/commercial signal + provenance> | <which is load-bearing> | <evidence-standard §8 rule> |

#### Symptom vs cause — what would have to be true
| Stated as | Would have to be true | Test against | Result | Assessed cause |
|---|---|---|---|---|

#### Renewal exposure
| Account | ARR | Renewal date | Notice days | Opt-out deadline | Days to opt-out | Health band |
|---|---|---|---|---|---|---|
| **Total** | **$<Z>** | | | | | |

#### Trend
| Period | Mentions | Accounts | Share of voice | Notes |
|---|---|---|---|---|
| Current | | | | |
| Prior | | | | |
| **Change** | | | **z = <value>** (screen, not a significance test) | |

Post-ship check (if a fix shipped): mentions/30d before <a> → days 30–90 after <b>. <reading>

#### Priority arithmetic
```
Risk-weighted ARR $<Y> × Intensity <i> × Trajectory <t> × Tractability <r> = $<priority>
Tie-break used: <days to nearest opt-out | ENT ARR share | economic-buyer mentions | none>
```

#### Routing — one accountable owner
| Destination | Accountable owner | Consulted | Decision requested | By | Expected effect | Success measure |
|---|---|---|---|---|---|---|

**Cost to fix:** <owner's estimate> | `UNKNOWN — requires <function> estimate by <date>`
**Cost of not fixing:** renewal exposure $<Z> · support load <computed or UNKNOWN> ·
suppressed expansion $<value>

#### Loop closure
| Who | Channel | Message summary | Owner | By | Recorded in |
|---|---|---|---|---|---|

#### What would change this read
<2–3 observable events that would move this theme's rank up or down.>

#### Gaps
- <field>: `UNKNOWN — requires <specific source and field>`
```

## Filling rules

| Slot | Rule |
| --- | --- |
| Claim | The customer's language, never the company's internal name for the problem |
| Verbatim | Truncate with `…`; never paraphrase. Always with account, role and date |
| Assessed cause | If inferred, state the inference rule and what would falsify it |
| Attributed ARR | Account grain, primary code only. Never labelled "ARR at risk" |
| Opt-out deadline | `renewal_date − notice_period_days`. Never the renewal date alone |
| Cost to fix | The owning function's number, or `UNKNOWN — requires X`. Never estimated by the analyst |
| Every routing row | action · owner · date · expected effect · success measure. All five, or it is not a recommendation |
| Empty sections | Print "checked, nothing found" — never delete the heading |
