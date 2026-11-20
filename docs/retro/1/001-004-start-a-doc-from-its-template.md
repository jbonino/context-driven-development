# Phase 1 — 001-004 — Start a doc from its template

The judgments that need fresh context. Everything else is in the raw
sessions under `docs/retro/raw/`, mined at phase close.

**Deviations from the plan and design**
- `cdd new` names a doc by its template's file: `ticket`, `retro-entry`, `release-playbook`, `foundations`.
- `check.py` runs `cdd check`, so the steps live in one place.
- `pyproject.toml` builds `cdd` with hatchling. `uv run` makes a `.venv`. Git ignores it. `uv.lock` is committed.
- **Each script**'s test also checks that `cdd` holds each Where path, and that a bare `cdd` prints its usage.
- The tests found four failure cases. A doc `cdd` doesn't know, a doc missing its name, a name that leaves its folder, and a phase that isn't a number. **`cdd new`** holds them in a table of cases.
- `cdd mine` has no test. The session scripts' baseline line covers it.

**Code review**

| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|
| Important | **Each script**'s "`cdd` alone" half is untested, since check-docs.py and check-caps.py still name their own paths | Fixed in round 2. The decision drops "alone". A Scripts ticket moves the paths and adds it back | the ticket |
| Important | `test_decision_cdd_new` asserted two failures its decision didn't state | Fixed. The decision folds them, for the owner's call | `architecture.md` |
| Important | `cdd new ticket ../escape` wrote outside its folder | Fixed. A name holds no slash and isn't `..`, and a phase is a number. Each has a row | the ticket |
| Minor | `test_decision_each_script` asserts the bare usage | Left. It proves `uv run cdd` resolves | — |
| Minor | `test_decision_cdd_check` asserts the printed lines | Left. The ticket asks that it print as check.py does | — |
| Minor | `cdd check caps` picked its step by position | Fixed. Steps are keyed by name | — |
| Minor | Folders were mixed into the docs dict | Fixed. They sit in their own dict | — |
| Minor | A first run needs network for hatchling, and each worktree builds a `.venv` | Left. uv caches it | — |
| Minor | `.venv/` sat under the articles comment | Fixed | — |
| Minor | Five prose lines joined clauses with a comma or colon | Fixed | — |

- Verdict: With fixes.

**Changed after sign-off**
- Round 1. **`cdd new`**'s failures became a table of cases, since one sentence packed three facts into "its args name its place". The ticket's criterion follows. Planning miss: `architecture.md`.
- Round 1. **`cdd check`** drops "a warning 0". **A form past its cap** already holds it. Planning miss: `architecture.md`.
- Round 2. **Each script** drops "alone". check-docs.py, check-caps.py, mine-transcripts.py and save-transcripts.sh still name paths. Moving them is about 3 points on Scripts, so it's a new ticket, since 001-009 is at its cap. The criterion restated the decision and kept half of it. Planning miss: the ticket, and the ticket template, which has no criterion row for a decision.
