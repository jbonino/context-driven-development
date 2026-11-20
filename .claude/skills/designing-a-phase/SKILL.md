---
name: designing-a-phase
description: Use when the roadmap's Now names a scoped phase and its design needs writing, from the foundations to the design's sign-off
---

# Designing a phase

Start: **Phase scoped**. End: **Design signed off**.

1. **Brainstorm with the Product Owner until a design meets the phase's
   goal.**
   - Invoke `branching-from-main` for the phase's plan.
   - Run `uv run cdd read product_roadmap Now`, and read the one or two
     latest entries of `uv run cdd read retro-entry {n}`. Run
     `uv run cdd read design_document "{heading}"` for each section the
     goal touches.
   - Invoke `superpowers:brainstorming`.
1. **Edit the Foundations the goal changes, with the Product Owner.**
   - Design from patterns to details. Read the retros for what repeats.
   - A new term joins the vocabulary before a workflow uses it.
1. **Edit the journeys the goal changes.**
   - Follow the Journey form. Each row links its
     workflow.
   - Wide then deep. Draft each changed journey roughly, then go through
     each with the owner.
1. **Edit the workflows the goal changes, and the checkpoints they start
   and end at.**
   - Follow the Workflow form.
   - Each step names its act and its outcome. The outcome holds on every
     branch, and a test asserts it.
   - Wide then deep. Walk two or three real cases from the repo and its data
     through each, with a verdict.
   - A workflow past its cap goes to the owner.
1. **Name each branch of a changed step as a scenario, and group the
   scenarios into features by shared context.** Titles only.
   - A branching step links its one feature in brackets. A second feature
     splits the step.
   - A scenario whose Then only repeats its step's outcome is cut.
1. **Write each scenario's Gherkin and each feature's rules, deep with the
   Product Owner.**
   - Follow the Scenario, Feature and Rule forms.
   - One act a scenario. Givens every scenario shares go in a Background.
   - An outline holds three Examples rows at least. Fewer cases are
     separate scenarios.
   - Run `uv run cdd check` until it passes. Bring each cap warning to
     the owner.
1. **Wireframe each screen a feature changes, with its copy.** The
   wireframe fills the feature's slot.
1. **Write the retro entry and sign off the design.**
   1. Invoke `editing-prose` over the changed sections.
   1. Invoke `superpowers:requesting-code-review`.
   1. Write the `phase-design` retro entry, per `writing-a-retro-entry`,
      while the review's findings are fresh.
   1. Fill its **Signed off** line once the owner signs off, and commit.
      The branch stays open for `architecting-a-phase`.
