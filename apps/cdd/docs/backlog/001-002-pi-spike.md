# 001-002 — Spike: what the skills need from Pi

**System.** [Skills](../architecture.md#system-skills) · **Estimate.** 2 — a timeboxed spike · **Model.** Sonnet 5.5, medium — reading and counting, no design calls

Find out whether CDD is worth moving from Claude Code to Pi, and which
Claude Code tools the skills need Pi to replace.

## Acceptance criteria

- A paper analysis from the sessions and Pi's docs, with no live run. If the verdict leans to move, a follow-up ticket runs one skill in Pi.
- A table of each Claude Code tool and skill the green-wagon sessions call, with its count.
- Each tool in that table has a Pi equivalent, a fallback, or "none".
- A verdict to move or stay, with the options scored against the ethics, for the owner's call.
- The findings go into the architecture's Stack and the Skills section. Ticket 001-003 names them.

## Workflow steps

- None

## Build notes

- Mine the saved sessions in green-wagon's `docs/retro/raw/` with `scripts/mine-transcripts.py`. Extend the miner to count tool calls rather than write a scratch script.
- Expect tools like `Agent`, `Skill`, `PushNotification`, `SendUserFile`, `AskUserQuestion` and the superpowers skills.

## Findings

Mined from 678 green-wagon sessions with `mine-transcripts.py --tools`, and
checked against Pi 1.6.0's docs on 2026-11-20. Calls total 41,499.

| Claude Code tool | Calls | Sessions | In Pi |
|---|---|---|---|
| Bash | 29,490 | 727 | Equivalent. `bash` |
| Edit, Read, Write, Grep | 8,842 | 309 | Equivalent. `edit`, `read`, `write`, `grep` |
| Skill | 1,216 | 340 | Equivalent. Agent Skills from `.agents/skills/`, run as `/skill:name` |
| ToolSearch | 433 | 214 | Equivalent. The built-in `tool_search` extension |
| Agent, SubagentHandback, SendMessage, ListAgents | 664 | 312 | Fallback. The example `subagent` extension runs each as its own `pi` process |
| AskUserQuestion | 215 | 92 | Fallback. The example `question.ts` extension |
| EnterWorktree, ExitWorktree | 307 | 147 | None. Start `pi` in the worktree `cdd branch` prints |
| PushNotification | 143 | 128 | Fallback. The example `notify.ts` extension notifies the desktop, not the phone |
| Monitor, TaskStop | 99 | 26 | None. `bash` with `nohup`, polled |
| SendUserFile | 50 | 23 | None. The reply names the file's path |
| WebFetch, WebSearch | 21 | 9 | None. `curl` or a third-party package |
| Artifact, ReportFindings, ReadNotifications, ScheduleWakeup | 17 | 13 | None. Each is rare |

Pi has built-ins for 96% of the calls. The gaps sit in the workflow skills.
`working-a-ticket` uses a reviewer agent, a worktree, a question and a push.
Pi asks no permission before a tool call. Nothing keeps an agent in its
worktree. A grouped row's Sessions is its busiest tool's.

The skills `run`, `built-in-browser` and `computer-use` have no Pi equivalent.

### Verdict

Each ethic scores 1 to 5.

| Option | People care | Repo care | Fair share | Total |
|---|---|---|---|---|
| **A. Stay, with Pi as a second harness** | 5. Users without Claude Code get CDD | 3. Each gap names its fallback | 4. Only the gaps get built | **12** |
| B. Move to Pi | 2. The owner loses phone pushes and the worktree guard | 3. Five example extensions to keep | 1. Subagents, questions and worktrees get rebuilt | 6 |
| C. Stay, with no Pi | 2. Users without Claude Code lose CDD | 5. Nothing new to tend | 5. Nothing to build | 12 |

A ties C and keeps the phase goal. A live run in Pi waits for 001-003.
