---
name: scoping-a-phase
description: Use when the Product Owner sets the next phase's goal from the feedback, the last retro's action items and the deferred entries
---

# Scoping a phase

Start: **Feedback in** and **Retro in**. End: **Phase scoped**.

1. **Read the feedback, the last retro's action items, and each deferred
   entry whose Revisit when now holds.**
   - Suggest `/clear` after other work.
   - Read `docs/feedback.md`, the action items in the last
     `docs/retro/{n}/retro.md`, and each file in `docs/deferred/` whose
     **Revisit when** now holds.
1. **Place each entry with the Product Owner until the feedback is empty**
   ([Placing feedback](../../context-driven-development/design.md#feature-placing-feedback)). One at a time:

   | Place | When | Then |
   |---|---|---|
   | Taken up | It fits the phase's goal | It joins the goal |
   | Deferred | It can wait past this phase | Copy `.claude/context-driven-development/templates/deferred.md` into `docs/deferred/`, named for its title, with when to revisit it |
   | Dropped | It no longer holds | Git keeps it |

   Delete each placed entry from `docs/feedback.md`.
1. **Replace the goal under Now in `docs/product_roadmap.md` with this
   phase's.** Take it from the action items, the entries taken up and each
   deferred entry read in step 1. Delete those deferred entries' files.
   Defer what the phase can't hold.
1. **Commit on `main` and push.** Invoke `designing-a-phase`.
