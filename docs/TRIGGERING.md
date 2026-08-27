# Triggering

> The `description` field is the only thing loaded until a skill fires. In a thirty-skill
> library covering one domain, it is also the only thing standing between the user and the
> wrong skill running. Two failures dominate, and they pull in opposite directions.

| Failure | What it looks like | Cause |
| --- | --- | --- |
| **Under-triggering** | The user asks for exactly this and nothing fires | Descriptions written in the vocabulary of the skill's name rather than the user's |
| **Collision** | Five skills claim the same prompt and the wrong one wins | Overlapping phrases with no disambiguation |

Both are measurable:

```bash
python3 scripts/check_triggers.py                 # hygiene, collisions, routing
python3 scripts/check_triggers.py --collisions    # phrase collisions only
python3 scripts/check_triggers.py --route "acme has gone quiet, should I worry"
```

`evals/routing.json` holds realistic prompts mapped to the skill that must win. It is the
acceptance test for triggering, and a change to any description must keep it passing.

---

## The six rules

### 1. Write phrases that survive a real company name

This is the rule most descriptions get wrong. A trigger phrase containing a placeholder noun
never matches a real prompt, because the user types a company name where your placeholder is.

| Wrong | Right |
| --- | --- |
| `'is this account going to churn'` | `'going to churn'` |
| `'prep me for the [account] call'` | `'prep me for'`, `'call with'` |
| `'build the QBR for this customer'` | `'build the qbr'`, `'qbr deck'` |
| `'their usage has dropped'` | `'usage has dropped'`, `'usage is down'` |

**Keep the fragment, drop the subject.** Two to four words, name-independent.

### 2. Write the way a CSM talks, not the way the skill is named

Users do not type `perform churn risk analysis`. They type `acme has gone quiet, should I be
worried`. At least a third of every description's phrases must be conversational and
first-person — `'my renewals'`, `'they've gone quiet'`, `'I have a call with'`, `'where do I
start'`, `'my gut says'`.

A skill whose triggers are all noun-phrases only fires for users who already know it exists,
which are the users who least need the help.

### 3. No bare generic terms

In a customer success library, `'churn'`, `'renewal'`, `'health'`, `'report'` and `'risk'` are
claimed by five skills each. A bare generic guarantees a collision and the winner is arbitrary.
Qualify it: `'churn risk for my book'`, not `'churn'`.

### 4. Say what the skill is *not* for

Every description ends with pointers to the siblings that would otherwise steal or lose the
prompt. This is what resolves a collision at read time.

> `... For the renewal execution runbook once risk is known, see renewal-prep. For portfolio
> revenue math, see renewal-forecast. For the intervention plan on an already-red account,
> see save-play.`

### 5. Be pushy — models under-trigger

Include an explicit instruction to fire even when the user does not name the concept:

> `Use this whenever someone is trying to work out whether a customer will stay, even if they
> never say the word 'churn'.`

### 6. Eight to fifteen phrases, under 1024 characters

Fewer than eight and coverage is too thin. More than fifteen and the phrases become generic
enough to collide. The character limit is a hard constraint of the format.

---

## Where the boundaries sit

The four renewal-adjacent skills are the highest-collision cluster in this library. The
boundary that resolves them:

| Prompt shape | Skill | Because |
| --- | --- | --- |
| "Will they leave? Why?" | `churn-risk` | Assessment |
| "It renews in November — what happens between now and then?" | `renewal-prep` | Execution runbook for one account |
| "What is my number this quarter?" | `renewal-forecast` | Portfolio revenue |
| "It's red — what do we actually do?" | `save-play` | Intervention on an already-red account |

Same pattern across the other clusters:

| Cluster | Split on |
| --- | --- |
| `retention-report` vs `exec-retention-review` | Recurring operational report vs the board/exec narrative |
| `cs-context` vs `cs-data-audit` | Set up the shared context vs audit instrumentation quality |
| `voice-of-customer` vs `churn-postmortem` | Themes across the base vs the root cause of one loss |
| `stakeholder-map` vs `proactive-outreach` | Who do we know vs what do we send them |
| `expansion-finder` vs `renewal-negotiation` | Find and size the opportunity vs negotiate the commercial terms |
| `fde-account-plan` vs `integration-health` vs `fde-scoping` | The whole deployment vs the connectors vs the scope before work starts |
| `coverage-and-capacity` vs `exec-retention-review` | Model the headcount vs present the case |

---

## The routing corpus

`evals/routing.json` is the contract. Each case is a prompt in natural user phrasing plus the
skill that must win.

```json
{"prompt": "acme has gone really quiet, should I be worried", "expect": "churn-risk"}
```

Rules for adding cases:

- **Use a real-sounding company name.** That is what catches placeholder-shaped phrases.
- **Write how someone actually types**, including lowercase and missing punctuation.
- **Two to three cases per skill**, spanning the obvious phrasing and the oblique one.
- A skill with no case in the corpus is untested and will be reported as such.

`AMBIGUOUS` in the report is not a pass. It means the intended skill won by less than 1.5
points, which will not hold up under a slightly different phrasing — add a disambiguating
phrase to one of the two.

---

## Checklist for a new or edited description

- [ ] 8–15 phrases, under 1024 characters
- [ ] Every phrase is name-independent — no `[account]`, no "this customer"
- [ ] At least a third are conversational and first-person
- [ ] No bare generic terms
- [ ] A pushy "Use this whenever … even if they don't …" clause
- [ ] "see `<sibling>`" pointers for every skill it could be confused with
- [ ] 2–3 cases added to `evals/routing.json`
- [ ] `python3 scripts/check_triggers.py` passes, with no `AMBIGUOUS` on the new cases
