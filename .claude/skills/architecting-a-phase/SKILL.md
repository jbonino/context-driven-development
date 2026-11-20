---
name: architecting-a-phase
description: Use when a phase's design is signed off and its architecture needs writing, from the brainstorm to the architecture's sign-off
---

# Architecting a phase

Start: **Design signed off**. End: **Architecture signed off**.

1. **Brainstorm with the Product Owner until a build meets the design's
   changes and the phase's goal.**
   - Stay on the phase's plan branch.
   - Run `uv run cdd read retro-entry {n} phase-design`, then read the
     design's diff against `main`. Run `uv run cdd read architecture
     "System: {name}"` for each system the diff touches.
   - Invoke `superpowers:brainstorming`. Score each option put to the
     owner against the ethics and principles it touches.
1. **Edit the architecture's Shared section the design changes.** These are
   the stack, Where, the constraints, and the testing strategy's levels
   and runners.
1. **List each new feature on the opening line of the component that
   builds it, under the system it runs on.**
   - Name a new component or system where none fits, shaped like the
     architecture template's.
   - Merge up the chain. A new system that shares its tech with one
     already there joins it.
1. **Write the decisions each changed component needs, under its
   heading.**
   - A heading names no workflow, journey or feature.
   - Facts flow down. A decision names only the design.
   - Run `uv run cdd check` until it passes. Bring each cap warning to
     the owner.
1. **Give each decision that's hard to undo a why.** Write a footnote under
   **Why** that names each option it beat.
1. **Write the retro entry and sign off the architecture.**
   1. Invoke `editing-prose` over the changed sections.
   1. Invoke `superpowers:requesting-code-review`.
   1. Write the `phase-architecture` retro entry, per
      `writing-a-retro-entry`, while the review's findings are fresh.
   1. Fill its **Signed off** line once the owner signs off, and commit.
      `writing-the-tickets` carries the branch to `main`.
