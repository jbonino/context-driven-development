# Phase 1 — 001-007 — Merge a signed-off branch

The judgments that need fresh context. Everything else is in the raw
sessions under `docs/retro/raw/`, mined at phase close.

**Deviations from the plan and design**
- A plan or chore takes its title as a second arg. A ticket's title comes from its first line. The ticket didn't say where a title comes from.
- The ticket's delete rides in the merge commit, so a rerun has one commit to find.
- A rerun after origin moved past a rejected push stops. It names the reset that lets it rerun.
- A dirty main checkout or a dirty worktree stops it before the merge.

**Code review**

| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|
| Critical | A branch held only on origin was deleted unmerged | Fixed. It's fetched and merged first, with a test row | the ticket |
| Important | A failed commit left a half merge that a rerun called a conflict | Fixed. It aborts the merge | the ticket |
| Important | A rerun after origin moved had no way out | Fixed. It names the reset | the ticket |
| Important | A dirty main checkout went unchecked | Fixed. It stops | the ticket |
| Important | A dirty worktree's edits were thrown away | Fixed. It stops | the ticket |
| Minor | A ticket ignores a given title without a word | Fixed. The usage says a plan or chore takes one | — |
| Minor | A first line with no em dash gives the whole line as title | Left. Every ticket's first line has one | — |
| Minor | The README filter could drop a row that only links the ticket | Left. A row links one ticket | — |
| Minor | The plan and chore rows could fold into one | Left. Each kind is a row of the decision | — |

- Verdict: With fixes.
