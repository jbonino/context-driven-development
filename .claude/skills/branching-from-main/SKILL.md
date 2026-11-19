---
name: branching-from-main
description: Use when a skill opens a branch for a ticket, a plan or a chore, from main up to date to the branch claimed in its own worktree
---

# Branching from main

Start: `main` up to date. End: the branch claimed, in its own worktree.

1. **Name the branch by its kind.**

   | Kind | Branch |
   |---|---|
   | Ticket | `feature/{ticket filename, no .md}` |
   | Phase's plan | `design/phase-{n}` |
   | Ad hoc plan | `adhoc/{number}-{short-name}` |
   | Chore | `chore/{short-name}` |

1. **Push `main` to `origin` under that name.** The push claims it. A
   branch already on `origin` is someone else's.
1. **Invoke `superpowers:using-git-worktrees` for the branch, under
   `.claude/worktrees/`.**
