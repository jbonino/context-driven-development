# 001-009 — Skills run cdd — **Ad hoc**

**System.** [Skills](../architecture.md#skills) · **Estimate.** 3 — every skill gets read and its paths go · **Model.** Sonnet 5.5, medium — many small edits, each by rule

Each skill names docs by what they are and runs `cdd` for the
mechanics. No skill names a path.

## Acceptance criteria

- No skill names a doc's or script's path, or says "in the foundations" to point at a form.
- Branching from main and merging to main each run their `cdd` verb.
- Working a ticket claims with `cdd next` and `cdd branch`.
- A skill that starts a doc runs `cdd new`, and one that reads part of a doc runs `cdd read`.
- The checks run as `cdd check`.

## Workflow steps

- [Designing a phase](../design_document.md#workflow-designing-a-phase) step 1
- [Architecting a phase](../design_document.md#workflow-architecting-a-phase) steps 1 and 2: the architecture's base
- [Writing the tickets](../design_document.md#workflow-writing-the-tickets) step 5
- [Working a ticket](../design_document.md#workflow-working-a-ticket) step 1
- [Reviewing a ticket](../design_document.md#workflow-reviewing-a-ticket) step 4

## Build notes

- Waits on 001-004, 001-005, 001-006 and 001-007.
- Rename the architecture template's Foundations section to Base.
- Planning ad hoc drops "Raise its points and ticket count". The README holds no totals.
- Closing a phase deletes the playbook from the repo, not moves it. Delete the empty done and in-progress folders.
- Delete `scripts/check.py` once nothing runs it.
