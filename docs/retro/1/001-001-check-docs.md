# Phase 1 — 001-001 — The checks run on this repo's docs

The judgments that need fresh context. Everything else is in the raw
sessions under `docs/retro/raw/`, mined at phase close.

**Deviations from the plan and design**
- The port dropped green-wagon checks this design lacks. Those are workflow users, journey lists, feature twins, code in the architecture and ticket ids.
- A deferred thing described outside its file is a new check.
- Journeys and rules have baselines too, one per Testing strategy kind.
- No release playbook. The phase ships nothing to deploy.

**Code review**

| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|
| Important | The rename skipped the baselines, so a renamed name left a stale line | Fixed | the ticket |
| Important | A part with no home's test counted problems but not their text | Fixed | — |
| Minor | A heading holding a link made the wrong anchor | Fixed | — |
| Minor | The rename rewrote prose in code docstrings | Fixed. It rewrites only docs and baselines | — |
| Minor | A `~~~` or four-backtick fence reads as text | Left. No doc uses one | — |
| Minor | A one-word deferred title would match common words | Left. The one title is two words | — |

- Verdict: With fixes.

**Past its caps**
- The phase journey holds 9 workflows, past 7. The owner kept it.
- Keeping each fact in its place holds 9 scenarios, past 8. The owner kept it. An outline of two rows reads worse than two scenarios.

**Changed after sign-off**
- Round 1. The model and attribute rows left A part with no home fails the check. Each needs a product's code. Planning miss: `design_document.md`.
- Round 1. The session scripts' tests became one `test_workflow_closing_a_phase` per file, for step 4. Steps 1 to 3, 5 and 6 run in a skill and wait for evals. The test check reads every test. Planning miss: the ticket.
- Round 1. The owner refused the proposed rule A rename carries a name to its tests and links. The decision **A home is found by name** already covers a rename. Its test folds into Each part has its home. Planning miss: the ticket.

**Sign-off review**

| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|
| Important | Closing a phase left its baseline with only step 4 tested | Pushed back. A baseline line beside a test fails the check. The retro names the untested steps | — |
| Important | The workflow test asserts field mappings, not only step 4's outcome | Left. They are step 4's evidence, per the owner's pick | — |
| Minor | Two retro lines read unclear | Fixed | — |
| Minor | A test helper reassigned `tmp_path` | Fixed | — |
| Minor | A helper sat below its caller | Fixed | — |
| Minor | Any `test_` file counted, not only under `scripts/` | Fixed | — |
