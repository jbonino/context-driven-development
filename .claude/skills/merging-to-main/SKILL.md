---
name: merging-to-main
description: Use when the owner has signed off a branch and it is ready to merge to main
---

# Merging to main

Start: **Signed off**, or a plan signed off. End: the merge pushed and the
branch gone.

1. **Stop the worktree's dev server, if one runs.**
1. **Run `uv run cdd merge {branch}` from the main checkout.** A plan or a
   chore adds its title. It runs `cdd save` first, since Claude Code
   deletes sessions after 30 days. It merges with the branch's name and
   title, deletes a ticket and its backlog row, pushes, and removes the
   branch. On a conflict, merge `main` into the branch, re-run the tests,
   and rerun it.
1. **Give the owner the short sha it prints.** The push marks the ticket's
   PR merged.
1. **Tag a plan's merge and push the tag.** A phase's plan takes
   `phase-{n}-plan`. An ad hoc plan takes `phase-{n}-adhoc-{m}`, `m` one
   past the phase's last.
