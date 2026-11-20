# Pi as a second harness

**What**

CDD's skills run in Pi as well as Claude Code, for users who can't use
Claude Code at work. Pi reads skills from `.agents/skills/`. Each skill names
a fallback for each Claude Code tool Pi lacks.

**Why deferred**

The workflow skills rely on the tools Pi lacks. Every skill would carry a
fallback for each. Deferred by the Product Owner on 2026-11-20.

**Revisit when**

Pi ships subagents, questions and phone pushes built in, or a user can't run
Claude Code.

**What Pi lacks**

Mined from green-wagon's 740 transcripts with `mine-transcripts.py --tools`.
They are 399 sessions and 341 subagents. Calls total 41,499. The In Pi
column comes from Pi 1.6.0's docs, read on 2026-11-20, not a run. A grouped
row's Transcripts is its busiest tool's.

| Claude Code tool | Calls | Transcripts | In Pi |
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
| Artifact, ReportFindings, ReadNotifications, ScheduleWakeup, bash_placeholder | 19 | 13 | None. Each is rare |

Pi has built-ins for 96% of the calls. The gaps sit in the workflow skills.
`working-a-ticket` uses a reviewer agent, a worktree, a question and a push.
Pi's docs say it asks no permission before a tool call. Nothing keeps an
agent in its worktree.

| Skill | Loads | In Pi |
|---|---|---|
| requesting-code-review | 246 | Runs. Its reviewer needs the `subagent` extension |
| working-a-ticket | 218 | Runs. Needs subagents, a worktree, a question and a push |
| editing-prose | 191 | Runs |
| signing-off-a-ticket | 179 | Runs. Needs a question |
| brainstorming | 161 | Runs. Needs a question |
| using-git-worktrees | 158 | Fallback. `cdd branch` makes the worktree |
| merging-to-main | 108 | Runs |
| creating-an-adhoc-ticket | 72 | Runs |
| writing-a-retro-entry | 43 | Runs |
| test-driven-development | 24 | Runs |
| 10 others | 55 | Runs. `phase-workflow`, `writing-a-ticket` and the rest |
| run, built-in-browser, computer-use, shopify-use-shopify-cli, shopify-admin | 14 | None |
