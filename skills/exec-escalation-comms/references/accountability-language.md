# Accountability Language — the cause, the commitment, the apology

> Read this **before writing a sentence of the cause or the commitment**, and again before the
> apology decision. Everything here is mechanical: a grammar test you can run, a rewrite you can
> copy, a decision table with two exits. None of it is a style preference — the passive voice in
> a root-cause sentence is legible to every executive who has read one before, and it costs more
> than the failure it was hiding.
>
> Evidence labels: `[M]` measured · `[V]` vendor · `[P]` practitioner · `[A]` academic ·
> `[L]` legal or regulatory primary text. Rules in
> `../../cs-context/references/operating-rules.md`; craft codes in
> `../../cs-context/references/practitioner-craft.md`.

**Contents** — [1. The actor rule](#1-the-actor-rule) ·
[2. Three passive-voice tests](#2-three-passive-voice-tests) ·
[3. The phrasebook](#3-the-phrasebook) ·
[4. The apology decision](#4-the-apology-decision) ·
[5. The never-list, with rewrites](#5-the-never-list-with-rewrites) ·
[6. Commitment language](#6-commitment-language) ·
[7. The pre-send scan](#7-the-pre-send-scan)

---

## 1. The actor rule

**One rule generates most of this file: every sentence about the failure names an actor, and the
actor is "we".** Not the system, not the migration, not the process, not a person.

| Level | Sentence | Verdict |
| --- | --- | --- |
| Actor deleted | "An issue occurred that impacted availability." | Refused. Nobody did anything |
| Actor is a system | "The migration was executed without a lock check." | Refused. The migration did not decide to run |
| Actor is an individual | "An engineer ran a migration without a lock check." | Refused (`../SKILL.md` Step 8). The line that gets screenshotted |
| Actor is the customer | "The job failed because your retry settings were too aggressive." | Refused even when true. It converts a service failure into an argument they must win |
| **Actor is us** | **"We ran a schema migration without a lock check. That was our change and our miss."** | **The only accepted form** |

The construction the first two rows share is what William Safire called the *passive-evasive*
and what political analyst William Schneider named the **past exonerative tense**: it admits an
error while deleting the party responsible `[P, Safire, *Safire's Political Dictionary*; term
coined by W. Schneider]`. Executives have read it in ten prior vendor notes. It does not read as
neutrality; it reads as a legal department.

**Where the customer's configuration genuinely contributed**, the fact is stated neutrally, in
the same sentence as what *we* change so it cannot recur:

```text
Your retry interval is 30 seconds, which is inside our documented range and should have
been safe. It was not safe against this failure, and that is our defect, not your
setting. From 2 September the API rejects a retry it cannot serve instead of queuing
it, so the interval stops mattering.
```

Atlassian's incident-communication guidance reduces to the same instruction: **own the problem**,
rather than describe a problem that appears to have no owner `[P, Atlassian Statuspage
incident-communication guidance, accessed 2026-08]`.

---

## 2. Three passive-voice tests

Run all three on every cause sentence. They take four seconds each and they catch different
failures.

| # | Test | How | Fails when |
| --- | --- | --- | --- |
| 1 | **"by zombies"** | Append *by zombies* to the clause. If it still parses, the actor is missing | "The migration was executed *by zombies*" parses |
| 2 | **Front-of-sentence** | Can the sentence start with "We"? If yes, it must | "We executed the migration" is available and was not used |
| 3 | **Who gets fired** | Read the sentence and ask which party a reader would hold responsible. If the answer is "nobody" or "the customer", rewrite | "An issue occurred" → nobody |

Two further constructions evade the actor without using the passive at all, and both are refused:

| Evasion | Example | Rewrite |
| --- | --- | --- |
| **Nominalisation** — the verb becomes a noun so it needs no subject | "There was a failure of the validation step." | "We shipped a validation step that did not run." |
| **Ergative** — the object becomes the subject | "The database connection dropped." | "We exhausted the connection pool and your jobs lost their database connections." |

**The one legitimate passive** is where the actor is genuinely and permanently unknown *and* you
say so: "The record was modified at 03:14; we do not yet know by which process, and I will know
by 14:00." That is an unknown with a clock on it, not an evasion.

---

## 3. The phrasebook

Left column is what gets written under pressure. Right column is what ships. **A hit is
rewritten, not softened** — softening leaves the shape of the original visible.

### Cause and impact

| Instead of | Write |
| --- | --- |
| "An issue occurred that impacted availability." | "We took the reporting API down for 4h12m." |
| "The migration was executed without validation." | "We ran a schema migration without a lock check. That was our change and our miss." |
| "Some customers experienced degraded performance." | "Your three nightly jobs failed. Two other accounts were affected; no data was lost anywhere." |
| "We believe this may be related to a caching layer." | "We do not yet know the cause. I will know by 14:00 BST and you will hear from me either way." |
| "There was an unexpected interaction between components." | "Our deploy changed the query plan on your largest table. We did not test that path." |
| "99.2% availability against a 99.9% target." | "1,840 claims could not be filed; 61 needed manual rework — about 22 hours of your team's time." |
| "Minimal customer impact was observed." | "Four of your users hit it, for eleven minutes each. Nobody else on your account was affected." |
| "The root cause has been identified and remediated." | "We found it at 23:10 and rolled the migration back at 23:40. Your jobs ran clean from 01:55." |
| "This was caused by a third-party provider." | "Our payment provider failed for 40 minutes. We chose them and we did not have a fallback; both are ours to fix." |

### Commitment and refusal

| Instead of | Write |
| --- | --- |
| "Engineering is prioritising a fix." | "Sam Okafor has the fix landing by Tue 2 Sep; he confirmed that date in writing this morning." |
| "It's on the roadmap." | "We are not building that this year. The nearest thing we can do is the CSV export by 30 September — Sam has agreed that date." |
| "We'll try to get that done this quarter." | "I will have a yes or no from Sam by Thursday, including if the answer is no." |
| "We'll keep you posted." | "Next update 16:00 BST today, whether or not there is news." |
| "We're working to resolve this as quickly as possible." | "Two engineers are on it full-time and have ruled out replica lag. Next update 16:00 BST." |
| "We hope to have this resolved shortly." | "I do not have a fix time yet. I will have one, or a reason there is none, by 16:00 BST." |
| "We'll circle back once we have more clarity." | "I will send you the confirmed count at 14:00 even if it has not changed." |
| "This is being escalated internally." | "Our VP Engineering owns it from 10:30 today. His name is Sam Okafor and he is on this thread." |
| "We can look at some options on pricing." | *(Nothing. It routes to `renewal-negotiation` — `R11` keeps commercial content out of this note entirely.)* |

### Register under pressure (`C27`)

| Instead of | Write |
| --- | --- |
| "We're incredibly sorry for this frustrating experience!" | "We got this wrong." |
| "We completely understand your frustration and appreciate your patience." | "You said this lands in the middle of your close week. It does, and that is the worst possible timing." |
| "Rest assured, this is our top priority." | "Two engineers, full-time, since 09:41." |
| "We take reliability extremely seriously." | *(Delete. Nobody claims the opposite, so the sentence carries no information.)* |
| "Thank you for bringing this to our attention." | "You caught this before our alerting did, which is a gap of ours." |
| "Please accept our sincerest apologies for any inconvenience caused." | "Sorry — this cost your team 22 hours." |
| "Unfortunately, we are unable to accommodate that request." | "We are not going to do that. Here is why, and here is the closest thing we can do." |

`C3` applies to every right-hand cell that contains a number: **the number is the last sentence
of its paragraph, and nothing softens it afterwards.**

---

## 4. The apology decision

An apology is a tool with a narrow range, not a default courtesy. The decision has two exits and
the evidence separates them cleanly.

**The finding.** Trust is repaired more successfully by an **apology** where the violation
concerns **competence**, and by a **denial** where it concerns **integrity** and there is
evidence of innocence `[A, Kim, Ferrin, Cooper & Dirks 2004, *Journal of Applied Psychology*
89(1), 104–118]`. A reflexive apology for something you did not do gets quoted back in the
negotiation, and it converts a disagreement into an admission.

| The customer's accusation is about… | Our position | Response | Sentence |
| --- | --- | --- | --- |
| **Competence** — we tried and failed | We did it | **Apologise once**, attached to the number and a completed action | "We got this wrong, and it cost your team 22 hours. The migration is rolled back and your jobs ran clean at 01:55." |
| **Competence** | Cause not yet known | **Acknowledge the impact, not the fault**, and state the clock | "Your jobs have failed twice and that is on us to explain. I will know why by 14:00." |
| **Integrity** — we misled, hid or acted in bad faith | We did not | **Deny, plainly, with the facts.** No apology | "We did not know about this defect before your renewal. Here is the internal ticket, opened 14 August, four days after you signed." |
| **Integrity** | We did | **Apologise, name it as a judgement failure, and change the mechanism.** The mechanism change is the whole message | "We knew on 12 August and told you on the 20th. That gap was a decision and it was the wrong one. From now on a Sev-1 affecting a named account is disclosed within one hour, and Priya Raman owns that rule." |
| **A miss that is not ours** — their config, their vendor, their change | Not ours | **State the fact neutrally, no apology, no blame** | "The failing calls came from an IP range outside your allow-list. Nothing changed our side on the 14th. Here is the log slice." |

**Three constraints on any apology that survives the table:**

1. **Once, in one sentence, and never again** (`R20`, `C28`). A second apology asks the customer
   to absolve you, which makes your feelings their job. The scan in §7 refuses a second one.
2. **It travels attached to three things or not at all**: their number, a completed action with
   a timestamp, and a named next date. Alone, it is a request for absolution.
3. **Containment beats compensation.** B2B service-recovery research finds that auxiliary
   resources which shrink the magnitude of the failure elicit recovery more reliably than limited
   monetary compensation, and that response speed is the provider's most effective lever
   `[A, Hübner, Wagner & Kurpjuweit 2018, *Journal of Business & Industrial Marketing* 33(3),
   interview data from 43 informants]`. Offer the engineer, the migration, the manual re-run —
   before you offer a credit. Any credit is a commercial act and belongs to
   `renewal-negotiation` (`R11`).

**Temper the expectation.** The service-recovery-paradox meta-analysis finds the effect positive
on **satisfaction** but non-significant on repurchase intention, word of mouth and corporate
image `[A, de Matos, Henrique & Rossi 2007, *Journal of Service Research* 10(1), 60–77]`. The
same B2B study found evidence for the paradox in only 9 of 25 investigated cases `[A, Hübner et
al. 2018]`. **A recovered failure returns you to neutral. It is not an asset, and nothing built
on the assumption that this incident will strengthen the relationship survives contact.**

### Where an apology reads as weakness

| Situation | Why an apology hurts | Instead |
| --- | --- | --- |
| Announcing a price increase | It frames a legitimate commercial decision as a wrong done to them, and invites a counter before the conversation starts (`C13`) | Announce it. "From 1 January your platform fee moves to $X." Rationale after the number, never before |
| A planned EOL with proper notice | Apologising for a roadmap decision signals it might be reversible. It is not | "We are retiring the legacy export API on 1 October 2027. Here is the migration path and the person who owns yours." |
| Declining a feature request (`R19`) | "I'm so sorry we can't" invites a second ask. A clear no does not | "We are not building that. Here is why, and here is the nearest thing we can do." |
| A failure that is theirs | It gets quoted back in the negotiation as an admission | The fact, neutrally, plus what we change so it cannot recur |
| The second, third and fourth message about the same incident | Each repetition transfers the emotional work to the customer (`C28`) | Progress, timestamps, the next clock time |
| A support-tier or coverage change they are entitled to be told about | It converts a contractual notice into a favour we are asking forgiveness for | The change, the date, the notice period, the alternative |

---

## 5. The never-list, with rewrites

`../SKILL.md` Step 8 carries the short form. This is the full list. Every row is a **rewrite, not a
softening**, and each one has been the sentence that lost an account somewhere.

### Blame

| Never | Why | Rewrite |
| --- | --- | --- |
| "The engineer who deployed this…" | The line that gets screenshotted, and it teaches every colleague not to tell you the truth | "That was our change and our miss." |
| "Our support team dropped this." | Internal blame is still blame, and the customer bought one company | "Your ticket sat for four days. That is our process failing, and here is what changed on 2 September." |
| "Your admin had disabled the alert." | Converts a service failure into an argument they must win | "The alert was off. That it *could* be off without a warning is our design problem; from 2 September the console tells you." |
| "As we advised in June…" | Reads as *you were warned*, and it is the sentence their exec quotes back | "We flagged this in June and it did not land, which means we did not make it clear enough." |

### Speculation and false certainty

| Never | Why | Rewrite |
| --- | --- | --- |
| "We believe this may be related to…" | A wrong cause published early is a second failure, and it is the one they quote | "We do not yet know. I will know by 14:00 and you will hear from me either way." |
| "This should not happen again." | An unfalsifiable promise from the party that just failed | "From 2 September a migration without a lock strategy fails the build. Sam owns it and I will confirm the day it ships." |
| "This was an isolated incident." | Unknowable on the day, and catastrophic if a repeat lands | "This is the first occurrence on your account. I have checked the last 18 months of tickets to say that." |
| "We have identified the root cause" *(when you have a symptom)* | The correction costs more than the delay would have | "We know which query is failing. We do not yet know why it changed, and that is the part I will have at 14:00." |

### Internal language crossing the wall (`R18`)

| Never | Why | Rewrite |
| --- | --- | --- |
| "We've escalated this internally." | Describes our org chart, not their outcome | "Our VP Engineering owns it from 10:30. His name is Sam Okafor." |
| "This is a P1 for us." / "We've opened a war room." | Internal severity language means nothing outside, and "war room" reads as panic | "Two engineers, full-time, hourly updates to you until it is closed." |
| "You're one of our most valuable accounts." | Implies a tier, and tells them how the accounts below them are treated | *(Delete. Show it in the response, not in the adjective.)* |
| "Given the risk to the renewal…" / "at-risk account" | A leaked risk assessment ends renewals that were not otherwise at risk | *(Delete entirely. It has no customer-facing form.)* |
| "We're keen to keep you as a customer." | Attaches a commercial motive to an apology, which reads as leverage (`R11`) | *(Delete. The commercial conversation is a separate week.)* |

### Commitments (`R19`)

| Never | Why | Rewrite |
| --- | --- | --- |
| "It's on the roadmap." | The kindest-sounding sentence in customer success and the most damaging | "Not this year. The nearest thing is the CSV export, 30 September, Sam's commitment." |
| "We'll have that fixed shortly / soon / in the coming weeks." | An undated promise is measured against the customer's most optimistic reading | A named owner and a calendar date they agreed in writing, or a decision date you own |
| "The team is aiming for end of Q4." | "The team" is nobody, and "aiming" is not a commitment | Strip it. Nothing about Q4 goes in the note until Sam has agreed the date |
| "We'll make this right." | Undefined, and the customer defines it later, expensively | The specific thing: the re-run, the engineer, the migration, with a date |

### Everything else

| Never | Why | Rewrite |
| --- | --- | --- |
| "Per our SLA…" | Correct, cold, and it invokes a contract mid-relationship | "What happens next is…" — the entitlement stated as an action, not a clause |
| Exclamation marks, superlatives, "excited", "thrilled" | Reads as not having understood the situation (`C27`) | Plain full stops. Short sentences |
| "Please don't hesitate to reach out." | Ritual | "If tomorrow's run fails, message me directly — I will pick it up the same hour." |
| Anything about another customer, named or identifiable | It tells this customer exactly how you will describe them elsewhere | "Two other accounts were affected" — a count, never an identity |
| Anything you would not want screenshotted | Because it will be | Read it as a slide in their board pack, because that is one of its lives |

---

## 6. Commitment language

The five gates in `../SKILL.md` Step 4 are a grammar as much as a process. A commitment that
survives them has a fixed shape:

> **By `<weekday + date>`, `<named human + role>` will `<observable outcome the customer can
> verify>`.** *(Optionally: `<how they will see it>`.)*

| Element | Required because | Failure form |
| --- | --- | --- |
| `By <weekday + date>` | "Next week" is measured from the reader's most optimistic Monday | "shortly", "in the coming weeks", "end of Q4" |
| `<named human + role>` | A team cannot be held to a date, and the customer cannot chase one | "engineering", "the team", "we" |
| `will <observable outcome>` | The customer must be able to tell whether it happened without asking | "look into", "review", "work on", "prioritise" |
| `<how they will see it>` | Prevention nobody can observe is indistinguishable from prevention never done | Silence, then a receipt nobody believes |

**Downgrade ladder.** When a gate fails, the commitment does not soften — it moves down one rung
and is written at the rung it reaches:

| Rung | Form | Use when |
| --- | --- | --- |
| 1 · Delivery | "By Tue 2 Sep, Sam Okafor ships the lock-check gate." | Owner named and agreed in writing |
| 2 · Decision | "By Thu 4 Sep I will have Sam's answer, including if it is no." | Owner named, date not yet agreed |
| 3 · Investigation | "By Thu 4 Sep I will tell you what it would take, and whether we will do it." | No owner yet |
| 4 · Refusal | "We are not doing this. The nearest thing we can do is X." | The answer is no |
| 5 · Silence | The sentence is deleted and the gap is raised above the divider | Nothing at any rung is honestly available |

**Rung 4 outperforms rung 1 stated falsely.** A clear no with reasoning and the nearest
alternative preserves more trust than a soft yes that turns out false, and the second missed
date is the one after which nothing you say is believed (`R19`).

---

## 7. The pre-send scan

Mechanical. Run it on the customer text only, before the leak scan in
`../../cs-context/references/customer-voice.md`.

1. **Actor scan** — every sentence about the failure has a subject, and it is "we". Run the
   *by zombies* test on each.
2. **Nominalisation scan** — search for `failure of`, `there was a`, `an issue`, `an outage
   occurred`, `resulted in`, `impacted`. Each is an actor waiting to be named.
3. **Apology count** — exactly zero or one. Two is a refusal condition (`C28`). Count "sorry",
   "apologies", "regret", "unfortunately", "we appreciate your patience".
4. **Individual scan** — no named person appears as a cause, on either side. Named people appear
   only as owners of commitments.
5. **Commitment scan** — every future-tense sentence carries a weekday-plus-date and a named
   human, or it has been deleted and raised above the divider (`R19`).
6. **Speculation scan** — search for `believe`, `likely`, `appears to`, `may have`, `possibly`,
   `should not`. Each is either a fact with evidence or an unknown with a clock time.
7. **Hedge-after-number scan** — no clause follows a number or a date in the same paragraph
   (`C3`).
8. **Commercial scan** — no credit, discount, term, renewal or entitlement language anywhere
   (`R11`). One hit routes the whole paragraph to `renewal-negotiation`.
9. **Register scan** — no exclamation marks, no superlatives, no "excited"/"thrilled"/"delighted"
   (`C27`).
10. **Read-aloud** — read the first three lines out loud. If they sound like a vendor, rewrite
    them.
