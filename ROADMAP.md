# Roadmap

Specified, not yet written. Listed here rather than in the README because a link to a skill
that does not exist is a confident claim with nothing behind it — the exact failure this
library exists to prevent. `scripts/validate_skills.py --manifest` fails the build if these
leak back into the README before they are built.

Ordered by dollar leverage per invocation, not by how interesting they are. The adversarial
review put `renewal-negotiation` first and the forward-deployed set last — four of seven
reviewers ranked the FDE cluster lowest despite it being the largest *market* gap, because
frequency times dollars favours the renewal chain.

| # | Skill | For | Why it matters | Blocks |
| --- | --- | --- | --- | --- |
| 1 | `renewal-negotiation` | AM, VP CS | The README's own chain — `churn-risk → renewal-prep → renewal-negotiation → renewal-forecast` — breaks at the step where money changes hands. `renewal-prep` and `objection-bank.md` already point at it | The renewal chain |
| 2 | `deal-to-cs-handoff` | CSM, AM | `churn-risk` names *Failed launch* a P0 pattern and nothing covers the moment it is created. Carries the promise ledger and the pre-go-live baseline — the only irreversible artifact in the lifecycle, because an unmeasured baseline can never be reconstructed | `value-case`, `onboarding-plan` |
| 3 | `value-case` | FDE, CSM, AM, CCO | Baseline capture, ROI arithmetic, attribution honesty | The renewal value story |
| 4 | `cs-playbook-designer` | CS Ops, VP CS | Triggers, SLAs, holdout measurement, kill criteria | Automation |
| 5 | `exec-escalation-comms` | CSM, VP CS, FDE, CCO | The note written to be forwarded unedited | — |
| 6 | `customer-advocacy` | CSM, CCO | Reference readiness from behaviour; pool rotation | — |
| 7 | `fde-account-plan` | FDE | Architecture as deployed, custom-work ledger, technical debt | The FDE set |
| 8 | `integration-health` | FDE, CS Ops | Silent-failure detection — the failures that raise no alert | — |
| 9 | `fde-scoping` | FDE | Scope, acceptance criteria, change control | — |
| 10 | `custom-vs-product` | FDE, Product | Build / generalise / decline, with multi-year carrying cost | — |

## Also on the roadmap, from the adversarial review

| Item | Why |
| --- | --- |
| `.agents/accounts/<slug>.md` — per-account journal | Five of seven reviewers, three of them naming it *the* change. Six features are currently section headings over a void: the health migration matrix, carry-forward triage, forecast grading against a frozen snapshot, detection lag, `R14` skips and `R21` spend ceilings all need somewhere to live |
| `scripts/score_families.py` | `risk_score.py` takes the seven sub-scores as *input*, so "reproducible" currently means the weighted sum is reproducible — the part a model gets right anyway. Deriving sub-scores from normalised tables is the part two people disagree on |
| `scripts/run_evals.py` → `docs/proof.md` | The same prompts with and without the skill, judged, side by side. The only claim in this repo a competitor cannot copy without running it |
| `scripts/check_artifact.py` | Everything today validates the *instructions*. Nothing has read an *output* |
| Consumption floors in `churn-risk` | `signal-library.md` rates commitment shortfall Strong / 90–270d lead and there is no override floor for it. `renewal-forecast` handles consumption correctly and `churn-risk` does not — so the claim that risk, QBR, forecast and board report agree already fails on the fastest-growing pricing model |

Removed from the README on 2026-08-28:

- `custom-vs-product`
- `customer-advocacy`
- `exec-escalation-comms`
- `fde-scoping`
- `integration-health`
- `value-case`
