---
name: closing-a-phase
description: Use when the phase is released and its retro needs writing, from the team's feedback to the retro's action items
---

# Closing a phase

Start: **Released**. End: **Retro in**. The entry is the `phase-close`
retro entry, per `writing-a-retro-entry`.

1. **Gather each role's feedback, the Product Owner's first.**
   - Suggest clearing the chat after other work.
   - Ask the Product Owner's read before any measure. Then each other
     role's.
1. **Read each of the phase's retro entries whole**, with
   `uv run cdd read retro-entry {n}`.
1. **Diff what shipped** from `phase-{n}-plan` and each
   `phase-{n}-adhoc-{m}` tag to `main`. A change no entry explains is a
   planning miss. Write its entry from the commits, with the owner's
   one-line why.
1. **Mine the sessions** with `uv run cdd mine {n}`, in the
   background. Read the owner's notes in the retro entries, then the order
   of acts. A restart, a step out of order or a retry points at a skill
   step. Extend the miner rather than write a scratch script. Check its ticket
   count against the entries before using its numbers.
1. **Walk every planning miss with the Product Owner, by kind**,
   grouped by pattern with a proposed call each, in one message.
   A miss's kind is its `Planning miss` cell on a severity row, or a
   bullet's last line. Each **Past its caps** line is a miss too. A
   kind seen once is proposed to stay. A kind seen in two tickets or
   more is proposed as an action item.

   | Miss | Goes to |
   |---|---|
   | Fix next | An action item in the retro |
   | Can wait | A deferred entry, from `uv run cdd new deferred {title}` |
   | No longer holds | It stays in its entry |

1. **Write the retro** from `uv run cdd new retro {n}`.
   - Invoke `editing-prose`. Act on an action item once the owner says
     so.
   - Delete the phase's release playbook by name once every box is
     checked. Git keeps it.
   - Last, sharpen this skill from the session.
