# Phase 1 — design pass — Keeping each fact in its place

The judgments that need fresh context. Everything else is in the raw
sessions under `docs/retro/raw/`, mined at phase close.

**Deviations from the plan and design**
- None. The goal needed no new workflow or journey. It changed one feature.

**Owner's calls**
- The design names no skill. How this repo meets "a workflow has a test
  named for it" is an architecture decision.
- A warning names no deferred thing.

**Code review**

| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|
| Important | A scenario that warns on a workflow a skill runs contradicts the row that fails a workflow with no test | Fixed. The scenario is cut | `design_document.md` |
| Important | No scenario checks that links and anchors resolve | Fixed. A Rule holds two link scenarios | `design_document.md` |
| Important | The feature sits at its cap of 8 scenarios | Fixed. Four Rules regroup it | `design_document.md` |
| Important | The architecture still lists the checks as deferred, with no decision on warn or fail | Left. The architecture pass takes it up | `architecture.md` |
| Minor | No scenario stops a warning from naming a deferred thing | Left. The deferred-thing scenario covers it | — |

- Verdict: With fixes.

**Signed off**
- 2026-11-18 by the Product Owner.

**Changed after sign-off**
- None.
