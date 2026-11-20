# 001-011 — Components in the architecture — **Ad hoc**

**System.** [Scripts](../architecture.md#system-scripts) · **Estimate.** 5 — the architecture's headings, the check that matches them, and a feature's tests renamed · **Model.** Opus 5.5, medium — the check's matching changes shape

Under each system, the architecture holds components, not features. A
component's opening line names the design features it builds. Keeping
each fact in its place leaves the design and becomes the Homes, Links and Caps components.

## Acceptance criteria

- Each system heading reads `## System: {name}`, and each heading under it `### Component: {name}`.
- The checks fail on a design feature that no component names, and on a component heading under no system.
- Keeping each fact in its place is gone from the design. Its rules are decisions under `### Component: Homes`, `### Component: Links` and `### Component: Caps`, each with a `decision_` test or a baseline line.
- The caps check warns on a decision past 2 sentences.
- The `cdd` decisions sit under `### Component: Doc commands` and `### Component: Branch commands`. Each component holds 4 decisions at most.
- Features are the only bridge. `test_decision_a_workflow_with_steps_to_carry` fails on a workflow with steps and no skill of its name.
- The Checkpoints table sits under Shared. No architecture heading names a workflow or journey.
- The architecture template matches.

## Workflow steps

- None

## Build notes

- Waits on 001-008 for the decision kind.
- Rename each `scenario_` test of Keeping each fact to `decision_` for the decision it now proves.
- The design steps that linked Keeping each fact in its place drop the link.
- Fix every link to an architecture anchor that changes.
