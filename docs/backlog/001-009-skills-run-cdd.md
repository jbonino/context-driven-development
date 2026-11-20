# 001-009 — Skills run cdd — **Ad hoc**

**System.** [Skills](../architecture.md#skills) · **Estimate.** 5 — all 13 skills and a template get read and their paths go · **Model.** Sonnet 5.5, medium — many small edits, each by rule

Each skill names docs by what they are and runs `cdd` for the
mechanics. No skill names a path.

## Acceptance criteria

- No skill names a doc's, script's or app's path, or says "in the foundations" to point at a form.
- Branching from main and merging to main each run their `cdd` verb.
- Working a ticket claims with `cdd next-ticket` and `cdd branch`.
- A skill that starts a doc runs `cdd new`, and one that reads part of a doc runs `cdd read`.
- The checks run as `cdd check`, the caps as `cdd check caps`, and mining as `cdd mine`.
- Closing a phase and scoping a phase delete a finished playbook or a taken-up deferred entry by name.
- Reviewing a ticket names the scenario baseline by name.

## Workflow steps

- [Designing a phase](../design_document.md#workflow-designing-a-phase) step 1
- [Architecting a phase](../design_document.md#workflow-architecting-a-phase) steps 1 and 2: the architecture's base
- [Writing the tickets](../design_document.md#workflow-writing-the-tickets) step 5
- [Working a ticket](../design_document.md#workflow-working-a-ticket) step 1
- [Reviewing a ticket](../design_document.md#workflow-reviewing-a-ticket) step 4

## Build notes

- Waits on 001-004, 001-005, 001-006 and 001-007.
- Rename the architecture template's Foundations section to Shared.
- Take `test_decision_a_skill_s_paths` out of the baseline.
- Planning ad hoc drops "Raise its points and ticket count". The README holds no totals.
- - Delete `scripts/check.py` once nothing runs it.
