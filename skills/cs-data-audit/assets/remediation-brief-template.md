# Data Remediation — the one-page ask

> Emitted by `cs-data-audit` Step 11. One page, two audiences, one set of facts. Internal only:
> it carries ARR exposure and system access detail and never crosses the firewall (`R18`).
>
> Populate every field or write `UNKNOWN — requires <source>`. Do not delete a row, and do not
> round a measured input — round only the composite figures, to two significant figures.

---

## <Company> — fixing the data behind the renewal book
**<date> · prepared by <name> · decisions in scope: <N> · data as of <date>**

**The ask:** <$X or N person-days> to fix <M> gaps, starting <date>, done by <date>.
**What it buys:** <the decision that becomes reliable, and the ARR it governs>.
**If we do nothing:** <the specific wrong decision that keeps being made, and its dollar value>.

---

## For the CFO — lead with the forecast, not the data

| | |
|---|---|
| ARR forecast on inputs that failed a test | $X across N accounts |
| ARR whose renewal has **no computable opt-out deadline** (`R1`) | $X across N accounts — these cannot legitimately enter Commit |
| Reported vs reproduced GRR / NRR | X% vs Y% — variance Zpp against a 0.5pp tolerance |
| Cost of the full fix | $X / N person-days |
| ARR of a single missed save at median ACV | $X |

<One sentence stating the comparison plainly: the fix costs less than / more than one missed
save, and what follows from that.>

### Three tiers — each states what stays broken

| Tier | Cost (days / $) | What it buys | ARR it de-risks | What stays broken |
|---|---|---|---|---|
| **1 — Stop the bleeding** | | The irreversible items: events not being emitted, score history not being stored, decision dates not being captured | | |
| **2 — Make the renewal book computable** | | Contract fields document-tested and corrected; opt-out deadlines computable across the book | | |
| **3 — Make it predictable** | | Labels, point-in-time history and a reproducible metric definition | | |

**Recommended tier: <N>.** <Why this one, in one sentence naming the decision it unblocks.>
Deviating downward means <the specific decision that stays unreliable, and until when>.

---

## For the CTO / Head of Data — lead with the days

| Item | Eng days | One-off or ongoing | Blocks what | Not eng work |
|---|---|---|---|---|

**Not engineering work:** <list the fixes that are ops, CS process or a data-entry standard —
usually most of them. Naming them makes the engineering ask small and specific.>

**On the critical path behind this:** <the projects that cannot start until these land.>

---

## Sequence and gates

| Wave | Weeks | Items | Gate to advance | Owner |
|---|---|---|---|---|

**Irreversible items are in Wave 1 regardless of blast radius.** An event not emitted today is
history that cannot be backfilled; the plan says so explicitly rather than sorting by effort.

## How we will know it worked

| Measure | Today | Target | By when | Who reports it |
|---|---|---|---|---|
| Coverage (families of 7) | | | | |
| Max downstream confidence | | | | |
| ARR with a computable opt-out deadline | | | | |
| GRR reproduction variance | | | | |

Re-audit date: **<date, 60–90 days after Wave 1 completes>** — score delta per family, what
moved, what did not.

## Assumptions this brief rests on

| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
