# Phase 1 — 001-008 — Test a system's decisions

The judgments that need fresh context. Everything else is in the raw
sessions under `docs/retro/raw/`, mined at phase close.

**Deviations from the plan and design**
- `test_decision_a_skill_s_paths` has a test, so its baseline line can't mean "no test". Here it means the checks don't yet hold the real skills to it. The line fails once no skill names a path, or once the decision is gone.
- The design's A part with no home fails the check gains a row: a decision with no test named for it.

**Code review**

| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|
| Important | The path pattern matched across two code spans and missed `.yaml`, `.js` and `.html` | Fixed. Each span is tested alone | the ticket |
| Important | Skill lines inside fences were scanned | Fixed | — |
| Important | An anchor-only link read as a path | Fixed | — |
| Important | The new parts row had no design row behind it | Fixed. The design gains the row | `design_document.md` |
| Important | The A skill baseline line went stale with no error once the decision was gone | Fixed | — |
| Important | Three baseline lines cited a scenario that doesn't prove their decision | Fixed. Each cites its rule or an honest gap | the ticket |
| Minor | A code comment repeated the baseline's reason | Fixed | — |
| Minor | Any bullet that opens in bold reads as a decision | Left. Only decisions do today | — |
| Minor | The A skill baseline line held two facts | Fixed | — |

- Verdict: With fixes.

**Changed after sign-off**
- Round 1. **A skill** split into **A skill**, **A skill's paths** and **An app's things**, so the test's name matches the one sentence it checks. Planning miss: the ticket.
- Round 1. **An app's things** became **A product's things**, which a skill may name. Planning miss: `architecture.md`.
