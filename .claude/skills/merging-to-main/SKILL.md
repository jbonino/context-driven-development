---
name: merging-to-main
description: Use when the owner has signed off a branch and it is ready to merge to main
---

# Merging to main

Start: **Signed off**, or a plan signed off. End: the merge in `main` and
the branch gone.

1. **Run `scripts/save-transcripts.sh`.** It saves the Claude Code and
   Copilot sessions. Claude Code deletes them after 30 days.
1. **Wait for a ticket's team PR to merge.** This repo's docs branch merges
   after it. A plan's branch has no team PR. See
   [Two repos](../README.md#two-repos).
1. **Merge the branch from the main checkout.** `git pull`, then
   `git merge --no-ff {branch} -m "{branch name without its prefix} — {title}"`.
   The merge keeps the branch's own commits, which show what happened. On
   a conflict, resolve it and finish the merge.
1. **Push if this repo has an `origin`, and give the owner the merge's
   short sha.**
1. **Tag a plan's merge, and push the tag if there's an `origin`.** A phase's plan takes
   `phase-{n}-plan`. An ad hoc plan takes `phase-{n}-adhoc-{m}`, `m` one
   past the phase's last.
1. **Remove the branch.**
   1. `git worktree remove --force <path>`, `git branch -D {branch}`,
      `git worktree prune`.
   1. `git push origin --delete {branch}`, if it was pushed.
