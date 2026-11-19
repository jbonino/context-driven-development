# 001-002 — Spike: what the skills need from Pi

**Feature.** None. It changes the Stack · **System.** [Skills](../architecture.md#skills) · **Estimate.** 2 — a timeboxed spike · **Model.** Sonnet 5.5, medium — reading and counting, no design calls

Find out whether Pi can run CDD's skills on a Copilot sign-in, and which
Claude Code tools the skills need it to replace.

## Acceptance criteria

- Pi signs in with Copilot and runs one skill, such as `editing-prose`, end to end.
- A table of each Claude Code tool and skill the green-wagon sessions call, with its count.
- Each tool in that table has a Pi equivalent, a fallback, or "none".
- The findings go into the architecture's Stack and the Skills section. Ticket 001-003 names them.

## Workflow steps

- None

## Build notes

- Mine the saved sessions in green-wagon's `docs/retro/raw/` with `scripts/mine-transcripts.py`. Extend the miner to count tool calls rather than write a scratch script.
- Expect tools like `Agent`, `Skill`, `PushNotification`, `SendUserFile`, `AskUserQuestion` and the superpowers skills.
