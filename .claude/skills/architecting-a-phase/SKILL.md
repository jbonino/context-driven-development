---
name: architecting-a-phase
description: Use when a phase's design is signed off and its architecture needs writing, from the brainstorm to the architecture's sign-off
---

# Architecting a phase

Start: **Design signed off**. End: **Architecture signed off**.

1. **Brainstorm with the Product Owner until a build meets the design's
   changes and the phase's goal.**
   - Stay on the `design/phase-{n}` branch.
   - Read `docs/retro/{n}/phase-design.md`, then the design's diff against
     `main`. Read `docs/architecture.md`'s contents, then `grep -n` it and
     `sed -n` the systems the diff touches.
   - Invoke `superpowers:brainstorming`. Score each option put to the
     owner against the ethics and principles it touches.
1. **Edit the architecture's Shared section the design changes.** These are
   the stack, Where, the constraints, and the testing strategy's levels
   and runners.
1. **List each new feature on the opening line of the component that
   builds it, under the system it runs on.**
   - Name a new component or system where none fits, from
     `docs/templates/architecture.md`.
   - Merge up the chain. A new system that shares its tech with one
     already there joins it.
1. **Write the decisions each changed component needs, under its
   heading.**
   - A component holds 4 decisions at most. A heading names no workflow,
     journey or feature.
   - Facts flow down. A decision names only the design.
   - Run `uv run --script scripts/check-docs.py` until it passes, and
     `uv run --script scripts/check-caps.py`. Bring each cap warning to
     the owner.
1. **Give each decision that's hard to undo a why.** Write a footnote under
   **Why** that names each option it beat.
1. **Write the retro entry and sign off the architecture.**
   1. Invoke `editing-prose` over the changed sections.
   1. Invoke `superpowers:requesting-code-review`.
   1. Write `docs/retro/{n}/phase-architecture.md`, per
      `writing-a-retro-entry`, while the review's findings are fresh.
   1. Fill its **Signed off** line once the owner signs off, and commit.
      `writing-the-tickets` carries the branch to `main`.
