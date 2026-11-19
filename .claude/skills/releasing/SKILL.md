---
name: releasing
description: Use when the owner says to release, deploy or ship, and when working through a playbook in docs/release/
---

# Releasing

Start: **Signed off**. End: **Released**, every box in
the phase's playbook checked.

Work `docs/release/phase-{n}.md`. The deploy runs through the team's own
process. The playbook lists the setup and checks each ticket's Release plan
names. Its **Release rules** name the smoke test.

1. **Run each section's steps in order, the smoke test last. Check each
   box as it verifies.** A section is one stage of the team's process.
   - Start at the first unchecked box. After a merge, start at the
     ticket's first new line.
   - Say what the line changes. Then, by its kind:

     | Kind | You do |
     |---|---|
     | Command | Print the full command with its real target and run it through Bash. The owner approves the call. If they deny it or it needs their login, they run it and paste the output |
     | Check on a screen | Give the owner the steps and the expected result. They report back |
     | Owner-only | Name it and wait |

   - Each approval covers one command on the target named. Before a
     command that deletes data, say what it removes and from where. Show
     each command's output and run the line's check.
   - On a failed check, stop. The owner decides on a retry. Write the
     verified fix into its system's section of `docs/architecture.md` and
     go on from that line.
   - The owner may skip a line that can't run. Check its box and add
     `Skipped:` with why and what stood in.
   - Commit the checked boxes once per sitting.
1. **At each sign-off the playbook names, the owner walks each merged
   ticket and says yes before the next section runs.** Give the steps to
   walk each ticket, one click each. Only a yes in chat counts.
1. **Write the release's retro entry**, per `writing-a-retro-entry`. Name
   each skipped line, why, and what stood in for it.

## A denied command

A denial is a decision. Stop, and name the command and why it matters.
The owner adds a permission rule, or runs it and pastes the output.
