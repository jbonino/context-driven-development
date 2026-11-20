# Phase 1 — 001-010 — Restructure the repo

The judgments that need fresh context. Everything else is in the raw
sessions under `apps/cdd/docs/retro/raw/`, mined at phase close.

**Deviations from the plan and design**
- `cdd.py` sits in `forms/checks/` with the checks that import it. The wireframe gave it no place.
- `cdd` still names CDD's docs alone. A second app needs `cdd` to take the app.
- The miner and the caps check read a doc at its old path in history from before the move. `cdd` holds that path in `before_the_move`.
- A doc may link `forms/forms.md` as well as the foundations.
- The essay's address moves to `/apps/cdd/publish/articles/`. Pages serves the repo's root, so the old link breaks.
- Saved sessions and article drafts are gitignored, so `git mv` left them in the main checkout. They move by hand after the merge.
- The foundations template's What now asks for a sentence or two. The forms table lives in `forms/forms.md`.

**Code review**

| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|

- Verdict: —.

**Changed after sign-off**
- None.
