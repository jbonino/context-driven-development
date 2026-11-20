# Phase 1 — 001-009 — Skills run cdd

The judgments that need fresh context. Everything else is in the raw
sessions under `docs/retro/raw/`, mined at phase close.

**Deviations from the plan and design**
- Reviewing a ticket ran the rename by its script's path, and no verb held it. `cdd check rename {old} {new}` now runs it, so **`cdd check`** names it.
- The check reads `/clear`, a branch's name and a GitHub link as paths. The skills say them in words instead.
- `cdd merge` already saved the sessions. It now saves through `cdd save`, so merging to main runs no separate save step.
- The architecture template already said Shared. Nothing was renamed.
- No release playbook exists yet, so there was no Release plan to fold in.
- The test of **Each script** skips docstrings. A docstring's run line isn't a path the script reads.

**Code review**

| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|

- Verdict: {Yes, No or With fixes}.

**Changed after sign-off**
- None.
