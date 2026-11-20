---
name: writing-the-tickets
description: Use when the architecture is signed off and the phase's tickets need writing, from the first ticket to the plan's sign-off
---

# Writing the tickets

Start: **Architecture signed off**. End: **Plan signed off**.

1. **Split the planned work until each ticket is one feature on one system
   and 5 points or less.** Read the changed features and workflows with
   `uv run cdd read design_document "{heading}"`, and their decisions with
   `uv run cdd read architecture "{heading}"`. Splitting the work in the
   design says how. Start each ticket with
   `uv run cdd new ticket {phase}-{number}-{short-name}`. Fill every slot
   and delete the comment. Its
   acceptance criteria link each scenario to its feature. A wireframe
   stays in its feature. Its Workflow steps names each step it builds and
   that step's outcome.
1. **Check each scenario until each way a bug could break it has a row or a
   scenario in the design.** The ways are running again, being undone or
   redone, meeting work that is locked or done, bad input, and the users' real
   numbers. A feature holds 8 scenarios and 4 rules at most. Past either,
   the owner decides.
1. **Grep the backlog until each model attribute the architecture adds sits
   in a ticket.**
1. **Order the tickets in the backlog README in groups that run side
   by side.** Each group names what it waits on. A spike leads the tickets
   that need it.
1. **Start the release playbook with `uv run cdd new release-playbook {n}`,
   and write its steps in run order.** Ask
   the owner whether it releases once every ticket is done, or ticket by
   ticket, and which smoke test each stage runs.
1. **Write the retro entry and sign off the plan.**
   1. Invoke `editing-prose` over the tickets, the README and the playbook.
   1. Invoke `superpowers:requesting-code-review`. Ask the reviewer to read
      the tickets' new rows and scenarios by journey, and add any a step
      lacks for step 2's ways.
   1. Write the `phase-tickets` retro entry, per `writing-a-retro-entry`.
   1. Get the owner's sign-off, then invoke `merging-to-main`.
