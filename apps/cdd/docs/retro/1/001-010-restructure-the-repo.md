# Phase 1 — 001-010 — Restructure the repo

The judgments that need fresh context. Everything else is in the raw
sessions under `apps/cdd/docs/retro/raw/`, mined at phase close.

**Deviations from the plan and design**
- `cdd.py` sits in `forms/checks/` beside the checks that import it.
- `cdd` still names CDD's docs alone. A second app needs `cdd` to take the app.
- The miner and the caps check also read each doc's old path. `cdd` holds it.
- A doc may link `forms/forms.md` as well as the foundations.
- The essay now serves at `/apps/cdd/publish/articles/`. The old link breaks.
- Saved sessions and article drafts are gitignored. They move by hand after the merge.
- The foundations template's What asks for a sentence or two.

**Code review**

| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|

- Verdict: —.

**Changed after sign-off**
- None.
