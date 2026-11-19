# Phase 1 — architecture pass — Keeping each fact in its place

The judgments that need fresh context. Everything else is in the raw
sessions under `docs/retro/raw/`, mined at phase close.

**Deviations from the plan and design**
- None.

**Owner's calls**
- A workflow or scenario a skill runs sits in a baseline, ported from green-wagon's baseline rule.
- The check scripts start as a port of green-wagon's, less its product's parts.

**Code review**

| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|
| Important | The skill-baseline footnote described a deferred thing | Fixed. The footnote gives only the baseline's reasons | `architecture.md` |
| Important | Testing strategy held 5 decisions, past its cap of 4 | Fixed. The two baseline decisions merged | `architecture.md` |
| Important | The section heading still said Checks after the Stack named Scripts | Fixed. Renamed to Scripts | `architecture.md` |
| Important | A shell runner broke the Python stack | Fixed. `scripts/check.py` runs the checks | `architecture.md` |
| Important | No decision said how a check finds a deferred thing or a heading's twin | Fixed. A home is found by name | `architecture.md` |
| Minor | A baseline's `{kind}` was undefined | Fixed | — |
| Minor | Where listed scripts, which aren't docs | Fixed. They moved to the Scripts section | — |

- Verdict: With fixes.

**Signed off**
- 

**Changed after sign-off**
- None.
