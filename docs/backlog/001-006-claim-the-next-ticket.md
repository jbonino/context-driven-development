# 001-006 — Claim the next ticket — **Ad hoc**

**System.** [Scripts](../architecture.md#system-scripts) · **Estimate.** 3 — reads the backlog README and origin, then pushes · **Model.** Sonnet 5.5, medium — edge cases with branches on origin

`uv run cdd next-ticket` names the next open ticket. `uv run cdd branch
ticket 001-004` claims it and opens its worktree, as branching from main
does by hand.

## Acceptance criteria

- `test_decision_cdd_next_ticket` holds **`cdd next-ticket`**: it skips a ticket that waits or has a branch on origin, and with none open it says what each waits on.
- `test_decision_cdd_branch` holds **`cdd branch`**: each kind gets its branch name. A push that fails names the next open ticket. A branch already here is reused.

## Workflow steps

- None

## Build notes

- Waits on 001-004.
- Tests run against a bare repo in a temp folder as origin.
