# Phase 1 — 001-011 — Components in the architecture

The judgments that need fresh context. Everything else is in the raw
sessions under `docs/retro/raw/`, mined at phase close.

**Deviations from the plan and design**
- The caps table moved from the design's outline to the architecture, under **A form past its cap**. The caps script reads it there.
- Each Skills feature heading became a component named for what it builds: Feedback, Tickets, Review, Playbook, Retro, Red tests and Prose.
- Checks holds 4 decisions: A home, A doc's links, A link and A form past its cap. The old **A system** decision folded into **A home**.
- **A workflow with steps to carry** is now one whose step links a feature. The customer workflows link none, so they need no skill.
- A component that builds no design feature opens with its decisions. Checks and both command components do.
- Architecting a phase, in the design and its skill, now places a feature on a component.
- Merges: the four rule tests and nine scenario tests folded into six `decision_` tests. The baseline drops eight lines.

**Code review**

| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|
| Important | An opening-line name the design lacks passed | Fixed. It fails, with a case | the ticket |
| Important | Old-style top headings such as `## Skills` passed | Fixed. A top heading is Shared, a system or Why | the ticket |
| Minor | The workflow-skill check skipped table steps | Fixed. It shares the caps script's step pattern | — |
| Minor | The home test branched over two tables | Fixed. One table | — |
| Minor | The test-name test also asserts rename | Left. Rename keeps a test's name on its source | — |
| Minor | The caps test repeated its shared assertions per row | Fixed. One test | — |
| Minor | The caps script's docstring was garbled | Fixed | — |
| Minor | A home holds five facts, two repeating Foundations and editing-prose | Left. Checks is at its cap of 4 | — |
| Minor | Three decisions joined clauses with commas | Fixed. Split into sentences | — |
| Minor | The architecting skill restated the component cap | Fixed. Dropped | — |
| Minor | No word counts show the prose cut ran | Left. The architecture grew by its new headings and the moved caps table | — |
| Minor | A caps fixture linked a gone anchor | Fixed | — |

- Verdict: With fixes.

**Past its caps**
- The Skills system holds 6 decisions, past 4. The owner kept it in 001-008.

**Changed after sign-off**
- None
