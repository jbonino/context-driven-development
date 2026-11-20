# Phase 1 — 001-004 — Start a doc from its template

The judgments that need fresh context. Everything else is in the raw
sessions under `docs/retro/raw/`, mined at phase close.

**Deviations from the plan and design**
- `cdd new` names a doc by its template's file: `ticket`, `retro-entry`, `release-playbook`, `foundations`.
- `check.py` runs `cdd check`, so the steps live in one place.
- `pyproject.toml` builds `cdd` with hatchling. `uv run` makes a `.venv`, which git ignores. `uv.lock` is committed.
- **Each script**'s test also checks that `cdd` holds each Where path, and that a bare `cdd` prints its usage.
- The tests found one case: a doc missing its name fails. It's a row in `test_decision_cdd_new`.
- `cdd mine` has no test. The session scripts' baseline line covers it.

**Code review**

| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|

- Verdict:

**Changed after sign-off**
- None
