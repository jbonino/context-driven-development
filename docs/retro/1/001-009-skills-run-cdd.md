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
| Minor | `docs/done/` stays a literal in check-docs | Left. It isn't a Where doc. It's the old home of done tickets, which only history holds | — |
| Minor | The session-scripts test spells the raw folder out | Left. Spelled out, the test fails if `cdd` moves the folder | — |
| Minor | The test of **Each script** checks three things | Left. All three are the decision's sentence | — |
| Minor | save-transcripts.sh gave no usage without its argument | Fixed. It names `uv run cdd save` | — |

- Verdict: Yes.

**Changed after sign-off**
- None.
