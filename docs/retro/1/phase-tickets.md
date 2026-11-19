# Phase 1 — ticket pass — Keeping each fact in its place

The judgments that need fresh context. Everything else is in the raw
sessions under `docs/retro/raw/`, mined at phase close.

**Deviations from the plan and design**
- One ticket, not one per Rule. The checks exist in green-wagon, so the ticket is a port.
- No release playbook. The phase ships nothing to deploy.
- The owner scoped Pi into the phase before sign-off. A spike, 001-002, comes before 001-003. Their decisions wait for the spike.
- The README gained a Setup section.
- A chore removed the two-repo model. Docs and code share one branch. A ticket is named `{phase}-{number}-{short-name}.md`.

**Owner's calls**
- A check that reruns gives the same result. The checks only read.
- Done tickets and retros link to no heading a rename could break.
- Links in code blocks, external URLs and anchors from headings with colons or dashes are the port's edge-case tests, not design rows.
- A baseline line for a removed workflow is covered by the baseline decision.
- The checks passing on this repo's docs is proven by every ticket's run.

**Code review**

| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|
| Important | The ticket names a skill, the README and another repo, past what a ticket may name | Fixed. A ticket may name anything | `design_document.md` |
| Important | Working a ticket reads a Release plan and playbook this phase lacks | Left. The owner keeps it | — |
| Important | Rows missing for real docs, reruns, reverts, done work and bad input | Pushed back. See Owner's calls | — |
| Minor | Scenarios under a linked Rule have no link of their own | Fixed. The template allows it | — |
| Minor | Working a ticket's checks step named no command | Fixed | — |

- Verdict: With fixes.

**Signed off**
- 2026-11-19 by the Product Owner.

**Changed after sign-off**
- The design's may-name outline lost its ticket row. A ticket may name anything. Planning miss: `design_document.md`.
