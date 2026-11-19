---
name: merging-to-main
description: Use when the owner has signed off a branch and it is ready to merge to main
---

# Merging to main

Start: **Signed off**, or a plan signed off. End: the merge pushed and the
branch gone.

1. **Run `scripts/save-transcripts.sh`.** Claude Code deletes sessions
   after 30 days.
1. **Merge the branch from the main checkout.** `git pull`, then
   `git merge --no-ff {branch} -m "{branch name without its prefix} — {title}"`.
   The merge keeps the branch's own commits, which show what happened. On
   a conflict, resolve it, re-run the tests, and finish the merge.
1. **Push, and give the owner the merge's short sha.** The push marks the
   ticket's PR merged.
1. **Tag a plan's merge and push the tag.** A phase's plan takes
   `phase-{n}-plan`. An ad hoc plan takes `phase-{n}-adhoc-{m}`, `m` one
   past the phase's last.
1. **Remove the branch.**
   1. Stop the worktree's dev server, if one runs.
   1. `git worktree remove --force <path>`, `git branch -D {branch}`,
      `git worktree prune`.
   1. `git push origin --delete {branch}`.
