# Phase 1 — 001-006 — Claim the next ticket

The judgments that need fresh context. Everything else is in the raw
sessions under `docs/retro/raw/`, mined at phase close.

**Deviations from the plan and design**
- A wait counts as merged once its ticket's row is gone from the backlog. The ticket didn't say how to tell.
- `cdd branch` checks origin before it pushes. A branch on origin at main's commit made the push say "up to date" and skip the lease.
- **`cdd branch`** holds the kinds and their args in a table.

**Code review**

| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|

- Verdict: pending.

**Changed after sign-off**
- None
