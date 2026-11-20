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

- Verdict: —

**Past its caps**
- The Skills system holds 6 decisions, past 4. The owner kept it in 001-008.

**Changed after sign-off**
- None
