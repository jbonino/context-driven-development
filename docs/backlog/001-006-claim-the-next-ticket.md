# 001-006 — Claim the next ticket — **Ad hoc**

**Feature.** [Claiming the next ticket](../design_document.md#feature-claiming-the-next-ticket) · **System.** [Scripts](../architecture.md#scripts) · **Estimate.** 3 — reads the backlog README and origin, then pushes · **Model.** Sonnet 5.5, medium — edge cases with branches on origin

`uv run cdd next` names the next open ticket. `uv run cdd branch
ticket 001-004` claims it and opens its worktree, as branching from main
does by hand.

## Acceptance criteria

- [Claiming the next ticket](../design_document.md#feature-claiming-the-next-ticket)

## Workflow steps

- [Working a ticket](../design_document.md#workflow-working-a-ticket) step 1: the claim is a branch on origin

## Build notes

- Waits on 001-004.
- `branch` takes each kind that branching from main names.
- Tests run against a bare repo in a temp folder as origin.
