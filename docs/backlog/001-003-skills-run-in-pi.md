# 001-003 — The skills run in Pi

**Feature.** None. It changes the Stack · **System.** [Skills](../architecture.md#skills) · **Estimate.** 5 — every skill gets read, and each Claude Code-only step gets a fallback · **Model.** Sonnet 5.5, medium — the spike's table settles each call

A user who can't use Claude Code runs every CDD skill in Pi, with no step
that only works in Claude Code.

## Acceptance criteria

- Each skill runs in Pi, or names its fallback for each Claude Code-only tool, per the spike's table.
- Pi finds the skills from this repo with no copy.
- The README says how to run CDD in Pi.

## Workflow steps

- None

## Build notes

- Waits on 001-002. Use its sections in the architecture.
