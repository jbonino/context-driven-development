# Phase 1 — 001-001 — The checks run on this repo's docs

The judgments that need fresh context. Everything else is in the raw
sessions under `docs/retro/raw/`, mined at phase close.

**Deviations from the plan and design**
- No check covers the model row or the attribute row of A part with no home fails the check. Each needs a product's code. The owner decides whether they leave the design.
- The test check reads only the check scripts' tests. The session scripts' tests carry no prefix. The owner decides.
- The port dropped green-wagon checks this design lacks. Those are workflow users, journey lists, feature twins, code in the architecture and ticket ids.
- A deferred thing described outside its file is a new check.
- Journeys and rules have baselines too, one per Testing strategy kind.
- The ticket proposes A rename carries a name to its tests and links.
- No release playbook. The phase ships nothing to deploy.

**Code review**

| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|

- Verdict: {pending}.

**Past its caps**
- The phase journey holds 9 workflows, past 7. The owner kept it.
- Keeping each fact in its place holds 9 scenarios, past 8. It goes to the owner.

**Changed after sign-off**
- None.
