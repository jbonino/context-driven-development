---
name: scoping-a-phase
description: Use when the Product Owner sets the next phase's goal from the feedback, the last retro's action items and the deferred entries
---

# Scoping a phase

Start: **Feedback in** and **Retro in**. End: **Phase scoped**.

1. **Read the feedback, the last retro's action items, and each deferred
   entry whose Revisit when now holds.**
   - Suggest clearing the chat after other work.
   - Run `uv run cdd read feedback`, `uv run cdd read retro {n}` for the
     last phase, and `uv run cdd read deferred`. Keep each deferred entry
     whose **Revisit when** now holds.
1. **Place each entry with the Product Owner until the feedback is empty.** One at a time:

   | Place | When | Then |
   |---|---|---|
   | Taken up | It fits the phase's goal | It joins the goal |
   | Deferred | It can wait past this phase | Run `uv run cdd new deferred {title}`, and say when to revisit it |
   | Dropped | It no longer holds | Git keeps it |

   Delete each placed entry from the feedback.
1. **Replace the goal under Now in the roadmap with this phase's.** Take
   it from the action items, the entries taken up and each deferred entry
   read in step 1. Delete each deferred entry taken up, by its name. Git
   keeps it.
   Defer what the phase can't hold.
1. **Commit on `main` and push.** Invoke `designing-a-phase`.
