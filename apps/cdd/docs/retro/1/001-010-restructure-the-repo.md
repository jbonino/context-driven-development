# Phase 1 — 001-010 — Restructure the repo

The judgments that need fresh context. Everything else is in the raw
sessions under `apps/cdd/docs/retro/raw/`, mined at phase close.

**Deviations from the plan and design**
- `cdd.py` sits in `forms/`. It serves every app and does more than check.
- `cdd` still names CDD's docs alone. A second app needs `cdd` to take the app.
- The miner and the caps check also read each doc's old path. `cdd` holds it.
- A doc may link `forms/forms.md` as well as the foundations.
- The essay now serves at `/apps/cdd/publish/articles/`. Old links to its images break.
- Saved sessions and article drafts are gitignored. They move by hand after the merge.
- The foundations template's What asks for a sentence or two.

**Code review**

| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|
| Important | The Checkpoints table's Evidence names the old `docs/` paths | Fixed | architecture.md. Its test reads Where alone |
| Important | The deferred README names the old template path | Fixed | The ticket |
| Important | Testability shapes the plan points to the forms under What | Fixed | The ticket |
| Minor | test_cdd's docstring names `scripts/` | Fixed | — |
| Minor | The miner shortens new paths to `docs/` and leaves `forms/` paths whole | Fixed | — |
| Minor | The test of **Each script** asserts four things | Left. It predates this ticket | — |
| Minor | The Pi spike ticket names `scripts/mine-transcripts.py` | Left. It means green-wagon's repo | — |

- Verdict: With fixes.

**Changed after sign-off**
- Round 1. `cdd.py` moved from `forms/checks/` to `forms/`. Planning miss: the ticket's wireframe gave it no place.
- Round 2. `articles/` redirects to the essay's new address, so old links still work. Planning miss: the ticket said the essay still serves but not at which address.

**Sign-off review**

| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|
| Important | The essay's old address puts Where at 5 decisions, past its cap of 4 | Left. The owner keeps it apart from **An app** | The ticket |
| Minor | Old links to the essay's images break | Left. A redirect can't forward an image. The deviation says so | — |
| Minor | The test of **An app** let any file under `articles/` pass | Fixed. It allows only the redirect page | — |
| Minor | The redirect test matches one exact string | Left. It asserts its decision's sentence | — |
| Minor | The retro said twice why `cdd.py` moved | Fixed | — |

- Verdict: With fixes.

**Past its caps**
- Where holds 5 decisions. The owner keeps the essay's old address as its own decision.
