---
name: branching-from-main
description: Use when a skill opens a branch for a ticket, a plan or a chore, from main up to date to the branch claimed in its own worktree
---

1. **Name the branch by its kind.**

   | Kind | Branch |
   |---|---|
   | Ticket | `feature/{ticket filename, no .md}` |
   | Phase's plan | `design/phase-{n}` |
   | Ad hoc plan | `adhoc/{number}-{short-name}` |
   | Chore | `chore/{short-name}` |

1. **Claim the name.** A branch of that name in `git branch -a` or
   `git worktree list` is someone else's. With an `origin`, push `main`
   under the name. Without one, the local branch claims it. See
   [Two repos](../../../README.md#two-repos).
1. **Invoke `superpowers:using-git-worktrees` for the branch, under
   `.claude/worktrees/`.**
