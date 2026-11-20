# Phase 1 — 001-006 — Claim the next ticket

The judgments that need fresh context. Everything else is in the raw
sessions under `docs/retro/raw/`, mined at phase close.

**Deviations from the plan and design**
- A wait counts as merged once its ticket's row is gone from the backlog. The ticket didn't say how to tell.
- `cdd branch` checks origin before it pushes. A branch on origin at main's commit made the push say "up to date" and skip the lease.
- The kinds' args moved into a table under **`cdd branch`**. The ticket named no args.
- Both commands read origin's main, not this checkout. A worktree from an older commit had a stale backlog.

**Code review**

| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|
| Important | A failed ls-remote read as no branch on origin | Fixed. A git failure exits with its error | the ticket |
| Important | A failed fetch or push read as a lost race | Fixed. Lost only when origin then holds the branch | the ticket |
| Important | `next-ticket` read this checkout's README, maybe stale | Fixed. It reads origin's main | `architecture.md` |
| Important | A failed track went unchecked, and a stale folder was reused | Fixed. Each is checked, and the folder must hold the branch | the ticket |
| Minor | A name git won't take read as a lost race | Fixed. `git check-ref-format` first | — |
| Minor | A case's name didn't match what it checked | Fixed | — |
| Minor | 001-009's assertion is a second case in one row | Left. It reads plainer beside the waits it lists | — |
| Minor | The reuse case doesn't prove no second push | Left. A second push would fail the run | — |
| Minor | The two decisions were hard to read | Fixed. Reworded under the cap | — |
| Minor | A retro bullet named no deviation | Fixed | — |
| Minor | No sign the prose cut ran | Fixed. Cut the decisions and this entry | — |

- Verdict: With fixes.

**Changed after sign-off**
- None
