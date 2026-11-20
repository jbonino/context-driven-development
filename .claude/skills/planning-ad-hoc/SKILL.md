---
name: planning-ad-hoc
description: Use when the open phase takes on scope it didn't plan, from the plan's branch to its sign-off
---

# Planning ad hoc

Start: **Feedback in** that adds scope to the open phase. End: **Plan
signed off**.

1. **Open the plan's branch off main.**
   - Number the first ticket with the phase's next free number. Invoke
     `branching-from-main` for the ad hoc plan.
   - The scope comes from chat or the feedback. Copy an entry's
     text for step 6, then delete the entry.
1. **Edit the design.** Invoke `designing-a-phase` over the new scope,
   with the Designer for a screen. This plan holds the branch, retro entry
   and sign-off, so skip those.
1. **Edit the architecture.** Invoke `architecting-a-phase` the same way.
1. **Write the tickets.** Invoke `writing-the-tickets` for steps 1 to 3.
   End each title with `— **Ad hoc**`.
1. **Queue the tickets and their release steps.**
   - Add a group atop the backlog README.
   - A ticket with a Release plan adds unchecked lines to the phase's
     release playbook under its stage, one per setup step
     and check. The release waits for the phase.
1. **Write the `adhoc-{first ticket}-{last ticket}` retro entry**, per
   `writing-a-retro-entry`.
   Say what the scope is. Name the planning miss behind it.
1. **Sign off with the Product Owner and merge.**
   1. Invoke `editing-prose` over the above.
   1. Invoke `superpowers:requesting-code-review`. Fix Critical and
      Important findings. Record each in the retro entry.
   1. Hand off the tickets' names and what waits on the owner. Stop for
      sign-off.
   1. Invoke `merging-to-main`.
