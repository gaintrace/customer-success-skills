# The Internal Call Note Standard

> Section A of the post-call artifact. Written first, before the CRM diff and long before the
> customer recap. It is the only durable record of what a conversation actually meant, and it
> is read by people who were not there — the next CSM, the renewal owner, the postmortem.

**Contents**
1. [What the note is for](#1-what-the-note-is-for)
2. [The ten blocks](#2-the-ten-blocks)
3. [What happened vs what was said vs what was meant](#3-what-happened-vs-what-was-said-vs-what-was-meant)
4. [The translation table — INTERNAL to TRANSLATE](#4-the-translation-table--internal-to-translate)
5. [Sentiment, with evidence](#5-sentiment-with-evidence)
6. [Stakeholders and competitive intelligence](#6-stakeholders-and-competitive-intelligence)
7. [Signal family deltas](#7-signal-family-deltas)
8. [Contradicting the account plan](#8-contradicting-the-account-plan)
9. [Answer depth — the exchange count](#9-answer-depth--the-exchange-count)
10. [Nothing in your head for two weeks](#10-nothing-in-your-head-for-two-weeks)
11. [Quality checks](#11-quality-checks)

**Evidence convention:** `[M]` measured · `[V]` vendor-analysed · `[P]` practitioner rule of
thumb · `[D]` derived here.

---

## 1. What the note is for

Four readers, four different needs. A note that serves only the first is a diary entry.

| Reader | When | What they need from it |
| --- | --- | --- |
| You, next month | Before the next call | What you promised, what they promised, what you were worried about |
| The next CSM | On handover | Why this account is the way it is — the history that is not in the data |
| The renewal owner | T-120 onward | Commercial signals, decision path, who actually decides |
| `churn-postmortem` | After a loss | The earliest detectable signal, and whether anyone wrote it down at the time |

The fourth reader is the reason this standard is strict. Loss reviews consistently find that
the signal was visible months earlier and was recorded as "good call, they're happy". The note
is where you either capture the thing that turns out to matter, or you don't.

**Write the note before the recap, always.** Writing the customer email first contaminates the
note with the framing you chose for the customer. The note gets softer, the risk language gets
diluted, and by the time you write it you have already decided the call went fine.

---

## 2. The ten blocks

| # | Block | Evidence tier | Skip if empty? |
| --- | --- | --- | --- |
| 1 | What happened | Observed only | No — write "standard agenda, nothing unusual" |
| 2 | What was said → what it likely meant | Inferred, with the rule stated and `exchanges` ≥ 2 | Yes, if genuinely nothing was implied |
| 3 | Sentiment read | Observed quotes → inferred read | No |
| 4 | Stakeholders | Observed | No — write "no change" |
| 5 | Competitive intelligence | Observed | No — write "none mentioned — checked, clear" |
| 6 | Signal family deltas (all seven) | Mixed | **Never.** Untouched families print as "not covered on this call" |
| 7 | What this contradicts in the account plan | Inferred | Yes, if nothing was contradicted |
| 8 | Commitment ledger | Observed | No |
| 9 | Open questions and thin answers | Observed + a depth count | **Never.** Prints "None — every central-issue line reached two or more exchanges" |
| 10 | Not written down anywhere else | Observed, from your own head | **Never.** Prints "None — blocks 1–9 carry everything I know about this account" |

Blocks 9 and 10 are the two that a rushed note drops, and they are the two nobody else can
reconstruct. Block 9 is where an answer that got one exchange goes instead of becoming a
finding (§9). Block 10 is the handover block (§10).

**Explicit non-findings are the point.** "No competitor mentioned — checked, clear" is a
different statement from silence, and only one of them tells the next reader that you looked.

---

## 3. What happened vs what was said vs what was meant

Three passes, kept separate. Collapsing them is what produces notes that are confident and
wrong.

| Pass | Contains | Example |
| --- | --- | --- |
| **What happened** | Observable facts only. Agenda covered, who attended, who spoke, what was demonstrated, time split, who joined late or left early | "60 minutes booked, ran 48. Dana joined at 12 min, left at 40. Ken presented the site-1 numbers. We did not reach the roadmap section." |
| **What was said** | Verbatim quotes with speaker and timestamp | "Dana: 'What's the per-seat number going to look like next year?' [00:14]" |
| **What it likely meant** | The inference, the rule, and the falsifier | See below |

Every inference in block 2 carries four parts, per
`../../cs-context/references/evidence-standard.md` §3:

> **Observed:** the CFO joined for 8 minutes, asked only about per-seat cost, and left before
> the roadmap section [Fireflies · transcript 2026-08-26 · 00:04–00:12].
> **Inferred:** this renewal will be decided on unit cost, not capability.
> **Rule applied:** economic buyer attends, asks only price questions, skips value content ⇒
> the decision criteria have narrowed to price.
> **What would falsify it:** a follow-up question from the CFO about outcomes, or the champion
> reporting that a business case was requested.

Stating the rule is what lets a colleague disagree with the *rule* rather than with you. An
inference without a rule is an opinion in a document that looks like a record.

**Common inference rules worth reusing:**

| Observed | Inference | Rule | Falsified by |
| --- | --- | --- | --- |
| Economic buyer skips the value section | Decision has narrowed to price | Attention allocation reveals decision criteria | A later request for a business case |
| Customer brings a colleague you have not met | The internal case is being widened | Unprompted introductions cost social capital | The colleague turns out to be a replacement for a departing contact |
| They ask about contract mechanics unprompted | A decision process has started on their side | Procurement questions are not idle | Routine annual audit or compliance review |
| Long pause after a price statement | The number is above their expectation | Silence after a number is a negotiation reflex | A stated budget that matches the number |
| Champion answers for the buyer | The buyer is disengaged or deferring | Proxy answering indicates absent ownership | The buyer confirms in writing afterwards |
| They describe a workaround they built | A product gap they have stopped raising | Building around a gap means they gave up on it being fixed | An open feature request with a recent update |

---

## 4. The translation table — INTERNAL to TRANSLATE

Every line extracted from the call is tagged `SHARE`, `TRANSLATE` or `INTERNAL` before the
recap is written. This table is the reference for the middle class. **The `INTERNAL` wording
never travels**, in any channel, including Slack Connect and shared documents.

| `INTERNAL` observation | `TRANSLATE` counterpart | `NEVER` |
| --- | --- | --- |
| "Champion weakening; sponsor absent from three consecutive calls" | "Would it help to bring Dana into the November session so she has the full picture?" | |
| "Single-threaded — one contact carries the whole relationship" | "Is there anyone else on your team who should be in these sessions?" | |
| "Finance org never onboarded — 0 of 22 seats active" | "Finance hasn't started yet — worth a 30-minute session to get the first three users set up?" | |
| "Licence utilisation 43%; they are over-provisioned" | *Say nothing.* Never volunteer that they are paying for seats they do not use before you understand why | Yes — until you have the reason |
| "They named Competitor X — evaluation underway" | "You mentioned you're comparing options — what would you want to see side by side?" | |
| "ARR at risk $148k; exposure-weighted $89k" | — | Yes, always |
| "Health band moved to At Risk" / "risk score 68" | — | Yes, always |
| "Forecast moved from Commit to At Risk" | — | Yes, always |
| "Save play activated; exec escalation Monday" | "I've asked our VP of Customer Success to join the next session." | |
| "Their new VP is hostile to the incumbent stack" | "You're new to this — what would you want to see from us in your first quarter?" | |
| "Champion is being managed out" | *Say nothing to anyone outside the account team.* | Yes, always |
| "They are over budget and will ask for a discount" | — | Yes — never pre-empt a discount conversation in writing |
| "Their procurement team is slow; last cycle took 11 weeks" | "Last time the paper took about 11 weeks — shall we start earlier this year?" | |
| "We have no exec sponsor and cannot get one" | "Would it be useful to get our leadership team in front of yours before the renewal?" | |
| "Support has been poor and they have every right to be angry" | "You told us this is the third failure this year, and your team lost two days." | |

**Three tests before any line goes in the recap:**

1. **The forward test.** If the customer forwarded this email to their CEO, is there a sentence
   you would want back? If yes, it is `INTERNAL`.
2. **The read-aloud test.** Would you say this sentence to their face, in these words? If not,
   you are writing internal analysis in a customer document.
3. **The third-party test.** Does this sentence characterise a person who is not on the thread?
   If yes, delete it — this is where the worst leaks live.

---

## 5. Sentiment, with evidence

"Sentiment: positive" is not a finding. Sentiment is a claim, and claims carry evidence.

| Field | Rule |
| --- | --- |
| Per person, not per account | An account does not have a sentiment; people do, and they differ |
| Quote + timestamp | The specific line that produced the read |
| Prior read + delta | The change is the signal. A neutral contact who was an advocate last quarter is worth more attention than a contact who has always been neutral |
| Confidence | High only with a transcript. Notes-only reads are capped at Low per the evidence standard |
| Non-verbal, if observed | "Left camera off for the whole call, first time in six months" is evidence. Say it is an observation, not a conclusion |

**Anti-patterns specific to sentiment:**

| Anti-pattern | Correction |
| --- | --- |
| Reading tone as sentiment | A blunt person being blunt is not deterioration; compare against their own baseline |
| Treating politeness as satisfaction | Grade D language is politeness under time pressure |
| Carrying a stale NPS forward | A survey score older than 90 days is a historical fact, not a current signal |
| Averaging across attendees | Report each person; an advocate and a hostile buyer do not average to neutral |
| Letting the loudest voice set the account read | Weight by role — the economic buyer's neutral outranks a power user's enthusiasm |

---

## 6. Stakeholders and competitive intelligence

**Stakeholders.** Capture on every call, even when nothing changed:

| Capture | Why |
| --- | --- |
| Anyone present who is not in the CRM | Create the contact today; a contact created months late loses its history |
| Anyone named but not present | "I'll check with Marcus" tells you Marcus exists and has authority |
| Anyone who has stopped appearing | Absence across three consecutive calls is a signal, and it is invisible unless attendance is logged |
| Role and influence changes | Based on observed behaviour, per `crm-update-rules.md` §3 |
| Who deferred to whom | The clearest available read on real authority |

**Competitive intelligence.** Record five things, or write "none mentioned — checked, clear":

| Field | Rule |
| --- | --- |
| Vendor named | Exactly as they said it. "The other one we looked at" is a vendor with an unknown name — write `UNKNOWN — requires follow-up` |
| Exact quote | Never paraphrase competitive language; the wording carries the stage |
| Who said it | A competitor named by the economic buyer is a different event from one named by an admin |
| Evaluation stage | Idle comparison · active evaluation · in procurement · decision made. State which and why you think so |
| Trigger fired | T1 in `crm-update-rules.md` §8, same day |

**Consolidation language is the highest-severity variant.** "We're consolidating vendors",
"looking at the overall stack", "reviewing all our tooling" describe a decision that may be
made above your buyer's head, on a timeline you are not in. It fires a same-day `save-play`
and a forecast review regardless of how positive the rest of the call was.

---

## 7. Signal family deltas

The seven families are fixed library-wide. Print all seven after every call. A family the call
did not touch prints as `No change — not covered on this call`, which tells the next reader you
checked rather than that you forgot.

| Family | What a call can tell you | What it cannot |
| --- | --- | --- |
| **Product usage & adoption** | Reported blockers, teams not started, workarounds built, features they did not know exist | Actual usage — verify in the product analytics source before anything acts on it |
| **Commercial & contract** | Stated intentions, budget position, procurement path, notice awareness, consolidation | The contract record itself |
| **Relationship & engagement** | Attendance, who speaks, who defers, no-shows, willingness to commit, multithreading | Email and meeting frequency between calls |
| **Support & reliability** | Grievances, incidents they have not ticketed, trust damage, unresolved history | Ticket volume, SLA performance |
| **Sentiment & VoC** | Direct quotes — the strongest sentiment evidence available | Whether the account as a whole feels this way |
| **Billing & payment** | Invoice disputes, payment friction, who owns the budget line | Payment history |
| **Firmographic & external** | Reorgs, funding, acquisitions, layoffs, leadership change, market pressure | Anything not volunteered |

**A call is strong evidence for two families and weak for five.** Relationship & engagement and
Sentiment & VoC are directly observed; the rest are self-reported and must be verified in the
source system before a play fires on them. State this in the Coverage Ledger rather than
letting the reader assume a call updated everything.

---

## 8. Contradicting the account plan

The most valuable block and the most often omitted, because writing it means admitting the plan
was wrong.

| Column | Content |
| --- | --- |
| Account plan assumption | What we believed before this call, quoted from the plan or the last note |
| What the call showed | The specific evidence |
| So what changes | The concrete change — a play, a date, an owner, or a plan section to rewrite |

Worked rows:

| Assumption | What the call showed | So what changes |
| --- | --- | --- |
| "Dana is our executive sponsor" | Dana joined 12 minutes late, asked only about cost, left before the roadmap | She is the economic buyer, not a sponsor. We have no sponsor. Ken to be asked for an introduction to the COO by 19 Sept — owner Ravi |
| "Expansion path is the compliance module in Q1" | They named a competitor for compliance specifically | Expansion is contested. Size the competitive gap before any pricing goes out — owner Ravi, 5 Sept |
| "Renewal is a formality; auto-renew is on" | Procurement asked for the termination clause | Not a formality. Category demoted from Commit to Most Likely with a written explanation — owner AM, same day |

**If nothing contradicted the plan, say so.** A note that never contradicts the plan across six
months is either an account with no surprises or a CSM who is not looking.

---

## 9. Answer depth — the exchange count

The first answer is rehearsed, the second is considered, the third is true. A note that records
a first answer as a finding has recorded the customer's public position and filed it as fact.

**`exchanges` is an integer, recorded on every open question and on every customer-stated fact
that touches the account's central issue.** It counts the separate times we asked and they
answered *on that issue* in this call and the ones before it — not the number of sentences they
spoke. Three sentences in one breath is one exchange.

| `exchanges` | Grade | Where the line may go | Where it may not |
| --- | --- | --- | --- |
| 1 | **Thin** | Block 9, with a follow-up written verbatim | Block 2, the CRM diff, the recap's decisions, any downstream skill's evidence |
| 2 | Considered | Block 2, with the inference rule stated; CRM diff evidence | Cannot alone move a forecast category |
| ≥ 3 | Tested | Anywhere in the artifact, as a finding | — |

**The follow-up column is the mechanism, not the count.** A thin answer with a count and no
follow-up has been graded and abandoned. The cell holds the literal sentence you will say:

| Thin answer recorded | Follow-up to ask (valid) | Follow-up to ask (invalid) |
| --- | --- | --- |
| "Budget's tight this year" | "When you say tight — is the line reduced, or frozen until something is approved?" | "Explore the budget situation" |
| "We're consolidating vendors in Q1" | "Who is running the consolidation, and what did they ask you for first?" | "Understand the consolidation" |
| "The rollout's been fine" | "Walk me through the last time it wasn't fine." | "Check on rollout health" |
| "Marcus handles that side" | "And what else does Marcus decide that we should be talking to him about?" | "Clarify Marcus's role" |

The right-hand column is a topic. A topic is what you write when you do not yet know the
question, and it produces the same thin answer next call.

**The event is never thin — only the explanation is.** A stated commercial decision ("we're
consolidating vendors in Q1", "auto-renew is off", "notice is going in") is an observed event
under `R2`, and it is logged verbatim, fires its trigger and moves the commercial family on a
single exchange. What is thin is everything behind it: who is running it, what triggered it,
what we would have to be for us to survive it. The event goes in block 2 and the CRM diff; the
reason goes in block 9 with the follow-up written out. Suppressing an R2 event because it got
one exchange is a misreading of C2 and the most expensive mistake this rule can produce.

**Why one exchange is not evidence.** The first answer is the one the person has already given
to their own manager. It is optimised to close the topic, not to be accurate. This is the same
reason `R16` caps a call at three discovery questions and requires silence after each: depth is
bought with follow-ups, not with coverage.

---

## 10. Nothing in your head for two weeks

Undocumented context survives exactly until the first holiday, reorg or resignation, and it is
precisely the context nobody can reconstruct afterwards. The data is still in the systems; the
reason it looks the way it does is not.

**Two mechanisms carry this, and neither is a reminder:**

1. **A note is written on every interaction, in every mode.** Recap-only produces the stub note
   first and the email second. Internal-only produces the note. A call with nothing to report
   produces a note that says so. There is no mode in which the customer receives text and the
   account record receives nothing.
2. **Days since the last written note is computed and printed in the note header.** Not
   remembered — computed, from the account's interaction history, alongside the count of
   interactions since that have no note against them. Past 14 days, block 10 becomes a backlog:
   one row per unwritten interaction, each with a date to write it up.

**What belongs in block 10.** Not a summary of the call — blocks 1–8 already hold that. Block 10
holds what a successor cannot get from the record:

| Kind | Example |
| --- | --- |
| The aside before the call started | "Ken mentioned his reorg lands in November; he said it off-agenda and I have never written it down" |
| The reason a name is never mentioned | "We stopped copying Marcus after the 2025 escalation. Nobody has told the new AM why" |
| Inherited history | "The previous owner said their CFO vetoed a three-year term in 2024. No ticket, no email, no note" |
| The unstated rule | "They will not take a Friday meeting. Learned by losing two" |
| What you would say on a handover call | Everything you would say out loud and have not typed |

**Where it can no longer be reconstructed, write `UNKNOWN — requires <person>` and log it as a
gap.** An invented reconstruction is worse than the gap, because the next reader cannot tell
them apart. Every block-10 row leaves with an owner and a date, the same as a commitment — the
row is the debt, the dated task is the repayment.

---

## 11. Quality checks

- [ ] Written **before** the customer recap
- [ ] All ten blocks present; empty ones marked "checked, clear" rather than dropped
- [ ] `exchanges` recorded as an integer on every block-2 and block-9 row; no block-2 row below 2
- [ ] Every thin (`exchanges` = 1) line sits in block 9 with a verbatim follow-up, and nowhere else
- [ ] Days since the last written note computed in the header; block 10 non-empty, with a backlog row per unwritten interaction past 14 days
- [ ] "What happened" contains no interpretation
- [ ] Every inference states its rule and what would falsify it
- [ ] Every sentiment read carries a quote, a timestamp and a prior-read comparison
- [ ] Sentiment confidence capped at Low where there is no transcript
- [ ] All seven signal families printed, including untouched ones
- [ ] Competitive intelligence block populated or explicitly "none mentioned — checked, clear"
- [ ] No-shows and late arrivals recorded
- [ ] Account plan contradictions written, or an explicit "nothing contradicted"
- [ ] Every commitment carries owner, action, due date, grade, expected effect, success measure and its source quote
- [ ] Nothing in the note has been softened because the customer might one day read it
