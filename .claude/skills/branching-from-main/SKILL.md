---
name: branching-from-main
description: Use when a skill opens a branch for a ticket, a plan or a chore, from main up to date to the branch claimed in its own worktree
---

# Branching from main

Start: `main` up to date. End: the branch claimed, in its own worktree.

1. **Run `uv run cdd branch {kind} {args}`.** The kind is `ticket {number}`,
   `plan {n}`, `adhoc {number} {short-name}` or `chore {short-name}`. The
   push to `origin` claims the branch. A branch someone else holds names the
   next open ticket instead.
1. **Enter the worktree it prints**, with the harness's own worktree tool
   if it has one.
