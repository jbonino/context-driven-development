# 001-007 — Merge a signed-off branch — **Ad hoc**

**Feature.** [Merging a signed-off branch](../design_document.md#feature-merging-a-signed-off-branch) · **System.** [Scripts](../architecture.md#scripts) · **Estimate.** 3 — merge, save sessions, delete the ticket, clean up · **Model.** Sonnet 5.5, medium — edge cases with conflicts and cleanup

`uv run cdd merge {branch}` does what merging to main does by hand: save
the sessions, merge with the message, delete the ticket, push, and remove
the worktree and branches.

## Acceptance criteria

- [Merging a signed-off branch](../design_document.md#feature-merging-a-signed-off-branch)

## Workflow steps

- [Reviewing a ticket](../design_document.md#workflow-reviewing-a-ticket) step 4: main holds the change and the ticket is gone

## Build notes

- Waits on 001-004.
- Sessions save through `scripts/save-transcripts.sh`.
- Tests run against a bare repo in a temp folder as origin.
