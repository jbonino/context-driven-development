# 001-001 — The checks run on this repo's docs

**Feature.** [Keeping each fact in its place](../design_document.md#feature-keeping-each-fact-in-its-place) · **System.** [Scripts](../architecture.md#scripts) · **Estimate.** 5 — a port of two working scripts and their tests, less the product's parts · **Model.** Sonnet 5.5, medium — the scripts and tests exist, so the work follows their pattern

One command checks every doc in this repo. It fails on a fact out of place
or a broken link, and it warns on a form past its cap.

## Acceptance criteria

- [Each part has its home](../design_document.md#feature-keeping-each-fact-in-its-place)
  - A part with no home fails the check
  - A deferred thing described outside its file fails
- [A doc names only what's above it](../design_document.md#feature-keeping-each-fact-in-its-place)
  - A file that names one it may not fails the check
  - An architecture heading with no design heading fails the check
  - A design feature no system lists fails the check
- [Every link resolves](../design_document.md#feature-keeping-each-fact-in-its-place)
  - A link to a missing file fails the check
  - A link to a missing heading fails the check
- [Each form stays under its cap](../design_document.md#feature-keeping-each-fact-in-its-place)
  - An outline under three rows warns
  - One more than the cap warns

## Workflow steps

- [Working a ticket](../design_document.md#workflow-working-a-ticket) step 6: the checks run until they pass

## Build notes

- Port `scripts/check-docs.py`, `check-caps.py`, `test_check_docs.py` and `test_check_caps.py` from `~/personal/green-wagon/scripts/`. Cut what reads `apps/`, Django, Shopify and ticket ids in code.
- Rename each test to its scenario's name, per the Testing strategy.
- Write `scripts/check.py` to run the tests, then the checks.
- Seed `scripts/workflow-baseline.txt` and `scripts/scenario-baseline.txt` with each workflow and scenario a skill runs. Each baseline opens with one `#` line for the reason.
- Point step 6 of `.claude/skills/working-a-ticket/SKILL.md` at `uv run --script scripts/check.py`, in place of the check by hand.
- Add the command to the README's Commands.
