# The Clarification Protocol

> Read this before asking the user anything, and before filling any gap.
>
> Two failures bracket this problem. A skill that **assumes** produces a confident artifact
> built on a guess, and the guess is invisible by the time someone repeats it to a customer.
> A skill that **interrogates** makes the user answer twelve questions before seeing any
> value, and they stop using it. The protocol below is how to sit between them: ask few
> questions, make them tappable, and make every unanswered thing visible instead of invented.

**Contents**
- [The three-way rule](#the-three-way-rule)
- [Never ask what you can read](#never-ask-what-you-can-read)
- [Make questions tappable](#make-questions-tappable)
- [Question design](#question-design)
- [The standard question sets](#the-standard-question-sets)
- [When the user does not answer](#when-the-user-does-not-answer)
- [The assumption register](#the-assumption-register)
- [Anti-patterns](#anti-patterns)

---

## The three-way rule

Every missing input resolves exactly one of three ways. There is no fourth way, and inventing
a plausible value is not one of them.

| | When | What you do |
| --- | --- | --- |
| **1. Read it** | The answer is in the data, in `.agents/cs-context.md`, or derivable from what you already have | Derive it. Show the derivation. Never ask. |
| **2. Ask it** | Different answers lead to **materially different work**, and you cannot derive it | Ask — tappably, batched, with a recommended default |
| **3. Mark it** | It is missing, and either the user cannot know it or it does not change the shape of the work | `UNKNOWN — requires <specific source>` in the output, and a confidence cap if it matters |

**The materiality test for asking:** would the two most likely answers produce different
recommendations, a different ranking, or a different artifact? If yes, ask. If the answer only
changes a detail you can state as an assumption, do not ask — state the assumption and carry on.

Asking about something that does not change the work is not diligence, it is friction. So is
asking three questions when the first one's answer determines the other two.

## Never ask what you can read

Before every question, run this. Most questions die here, which is the point.

| Do not ask | Get it from |
| --- | --- |
| "What's their ARR?" | The CRM or billing export, or `cs-context` §7 |
| "When do they renew?" | `subscription.renewal_date` |
| "What's their notice period?" | `cs-context` §2 — and if it is genuinely absent, that is a **finding**, not a question to bother the user with mid-analysis |
| "Who's the CSM?" | `account.owner_csm` |
| "How many seats do they have?" | `subscription.seats_purchased` |
| "Are they enterprise or SMB?" | `cs-context` §3 segment boundaries, applied to their ARR |
| "What tools do you use?" | `cs-context` §9 Source Inventory |
| "What's your fiscal year?" | `cs-context` §13 |
| "Is the account healthy?" | That is the analysis. Do not ask the user to do it. |

Asking a user something already in their context file tells them the skill did not read it,
and it is the fastest way to lose their trust in everything else the skill says.

## Make questions tappable

**Use a structured question tool when one is available** (`AskUserQuestion` in Claude Code).
Tappable options beat open prose for three reasons: the user answers in one gesture instead of
composing a sentence, the options *teach* the user what the skill can do, and the answers come
back in a vocabulary the skill already understands rather than as free text you have to parse.

Rules for the structured form:

| Rule | Why |
| --- | --- |
| **2–4 options per question, mutually exclusive** | More than four and the user reads instead of taps |
| **Recommended option first, labelled `(Recommended)`** | Most users want the default; make it one tap |
| **A one-line description under each option saying what it changes** | The user is choosing an outcome, not a word |
| **Batch up to 4 questions in a single ask** | One interruption, not four. Never drip-feed |
| **Short headers (≤12 chars)** | They render as chips: `Scope`, `Horizon`, `Audience` |
| **Never include an "Other" option yourself** | The tool supplies free-text entry automatically |
| **Multi-select only when the choices genuinely combine** | Otherwise it invites an incoherent combination |

When no structured tool is available, fall back to a numbered list with a stated default —
never an open-ended paragraph of questions.

```
Before I run this, two things:

1. Scope — (a) this renewal window [default], (b) my whole book, (c) one account
2. Horizon — (a) to each account's opt-out date [default], (b) next 90 days

Reply "1a 2a" or just say "defaults".
```

## Question design

**Ask about the decision, not the parameter.**

| Weak | Strong |
| --- | --- |
| "What weight profile should I use?" | "How do these customers buy?" → *Annual contracts with notice periods* · *Self-serve monthly* · *Usage/consumption* |
| "What's your horizon?" | "Risk of churning by when?" → *By each account's opt-out date (Recommended)* · *Next 90 days* · *This fiscal year* |
| "Do you want the long or short version?" | "Who reads this?" → *Just me, before a call* · *My VP, in the weekly review* · *The customer* |
| "Should I include expansion?" | "This account is healthy — want the expansion opportunities too, or risk only?" |

**Front-load the one question that changes everything.** Scope first, always: it determines how
much data to pull, how long the run takes, and what the artifact even is. `deepsec` asks for
scope before it does anything so the rest of the run is unattended; do the same.

**Warn about the expensive option in its own description.** "Whole base — every active account.
Slower and produces a long artifact; use for a quarterly sweep."

## The standard question sets

Reuse these across the library so users learn one vocabulary.

**Scope** — every analytical skill, asked first
> *Single account* · *Renewal window (next N days)* · *My book of business* · *Segment or cohort* · *Whole base (slow)*

**Horizon** — risk and forecast skills
> *To each account's opt-out deadline (Recommended)* · *Next 90 days* · *This fiscal quarter* · *This fiscal year*

**Audience** — every skill producing a document
> *Me, working* · *My manager / the weekly review* · *Exec staff or board* · *The customer*

**Commercial model** — when `cs-context` is absent and it changes the scoring
> *Annual contracts, notice periods, named champions* · *Self-serve monthly* · *Usage-based / consumption* · *Mixed*

**Depth** — when the user is time-boxed
> *One-pager, 5 minutes* · *Full artifact* · *Full artifact plus the customer-facing draft*

**Data on hand** — when nothing is connected
> *I'll paste or upload exports* · *Query a warehouse* · *I'll answer questions instead* · *Use what's in the context file only*

## When the user does not answer

Never block. A skill that stalls waiting for an answer has produced nothing, which is worse
than producing something with a stated assumption.

1. Proceed with the **recommended default**.
2. State it in the output, at the top, in one line: *"Run against the next 120 days of
   renewals using the enterprise weight profile — say the word and I'll re-run on a different
   scope."*
3. Record it in the **assumption register** at the bottom of the artifact.
4. If the assumption materially affects a conclusion, cap confidence and say which conclusion
   would change if the assumption is wrong.

The exception — the one case where you stop and produce nothing — is when **every** answer
would make the work unsafe or useless: coverage under 40% of the seven signal families, no
outcome labels for a backtest, or a customer-facing draft where you cannot tell who the
recipient is. Say what is missing and what it would take. Do not produce a scored artifact
from a guess.

## The assumption register

Every artifact that ran on an assumption ends with this. It is short, and it is the difference
between an analysis someone can audit and one they have to trust.

```markdown
### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | Enterprise weight profile (annual contracts) | No `cs-context` file; ACVs above $25k implied it | Usage would carry more weight; Beta and Gamma would rank higher |
| 2 | 30-day notice period where the field was blank | 3 of 12 accounts had no `notice_period_days` | Those three opt-out dates could be up to 60 days earlier — treat their urgency as a floor |
| 3 | "Active" excludes the 4 accounts flagged internal | No documented exclusion rule | ARR assessed would rise by ~$12k; no ranking change |
```

Rules: one row per assumption, each with a concrete consequence. "May affect results" is not a
consequence. If you cannot name what would change, you did not need the assumption.

## Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Asking a question whose answer is in `cs-context` | Read the file first. Always. |
| Asking six questions before producing anything | Batch four maximum, defaults on all of them, then run |
| Open-ended prose questions when a structured tool exists | Tappable options with a recommended first |
| Asking one question, waiting, asking the next | One batch, one interruption |
| Silently defaulting without saying so | State the default in the output and in the assumption register |
| Filling a blank field with an industry average | `UNKNOWN — requires X` |
| Filling a blank field with the previous period's value | Say you carried it forward, or mark it unknown |
| Inferring a segment, a notice period, or a champion and stating it as fact | Label the inference, give its rule, say what would falsify it |
| Blocking on a question the user cannot answer | Proceed on the default; cap confidence; say what would change |
| Asking "is this account healthy?" | That is the job. Do it. |
| Asking the customer's own business objective when a success plan exists | Read the success plan; ask only to confirm it is current |
| A question with four options that all produce the same output | Do not ask it |
