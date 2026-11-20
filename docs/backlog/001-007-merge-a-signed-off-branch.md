# 001-007 — Merge a signed-off branch — **Ad hoc**

**System.** [Scripts](../architecture.md#system-scripts) · **Estimate.** 3 — merge, save sessions, delete the ticket, clean up · **Model.** Sonnet 5.5, medium — edge cases with conflicts and cleanup

`uv run cdd merge {branch}` does what merging to main does by hand. It saves
the sessions, merges, deletes the ticket, pushes, and removes the worktree
and branches.

## Acceptance criteria

- `test_decision_cdd_merge` holds **`cdd merge`**: a clean merge carries the branch's name and title and clears it. A plan or chore deletes no ticket. A conflict or a rejected push leaves everything. A rerun finishes a partial merge.

## Workflow steps

- None

## Build notes

- Waits on 001-004.
- Sessions save through `scripts/save-transcripts.sh`.
- Tests run against a bare repo in a temp folder as origin.
