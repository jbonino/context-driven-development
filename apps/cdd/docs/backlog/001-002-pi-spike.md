# 001-002 — Spike: what the skills need from Pi

**System.** [Skills](../architecture.md#system-skills) · **Estimate.** 2 — a timeboxed spike · **Model.** Sonnet 5.5, medium — reading and counting, no design calls

Find out whether CDD is worth moving from Claude Code to Pi, and which
Claude Code tools the skills need Pi to replace.

## Acceptance criteria

- A paper analysis from the sessions and Pi's docs, with no live run. If the verdict leans to move, a follow-up ticket runs one skill in Pi.
- A table of each Claude Code tool and skill the green-wagon sessions call, with its count.
- Each tool in that table has a Pi equivalent, a fallback, or "none".
- A verdict to move or stay, with the options scored against the ethics, for the owner's call.
- The findings go into the Skills section's harness decision and a deferred entry.

## Workflow steps

- None

## Build notes

- Mine the saved sessions in green-wagon's `docs/retro/raw/` with `scripts/mine-transcripts.py`. Extend the miner to count tool calls rather than write a scratch script.
- Expect tools like `Agent`, `Skill`, `PushNotification`, `SendUserFile`, `AskUserQuestion` and the superpowers skills.

## Findings

The tables live in the [deferred entry](../deferred/pi-as-a-second-harness.md).

### Verdict

Each ethic scores 1 to 5.

| Option | People care | Repo care | Fair share | Total |
|---|---|---|---|---|
| A. Stay, and add Pi alongside | 5. Users without Claude Code get CDD | 3. Each gap names its fallback | 4. Only the gaps get built | **12** |
| B. Move to Pi | 2. The owner loses phone pushes and the worktree guard | 3. Five example extensions to keep | 1. Subagents, questions and worktrees get rebuilt | 6 |
| C. Stay, with no Pi | 2. Users without Claude Code lose CDD | 5. Nothing new to tend | 5. Nothing to build | **12** |

A and C tie. The owner picks C. Pi waits in its deferred entry.
