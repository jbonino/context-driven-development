---
name: editing-prose
description: Use on every chat reply, and before finishing prose meant to last. That means docs, skills, tickets, retros, code comments, UI copy and command output
---

# Editing prose

Start: a diff or a reply with prose. End: each line passes and each file is cut.

Agents write too much. This skill runs on what anyone writes, so a person
reads it fast. A chat reply runs step 2 alone.

1. **List each file the diff's prose touches, with its word count.**
1. **Apply the sentence rules until each line passes.**
1. **Cut the prose until it's 25% shorter.** Forms skip this step.
1. **Report each file's word count before and after.** A cut the owner
   keeps short of 25% goes into the retro entry.

**Every sentence**
1. Explain it like the reader is five. Short words, short lines, one fact
   each.
1. Say what is. An option's Other considerations may say what it lacks.
1. Write present tense, current state only. History belongs in git. A
   why-comment is the exception, since blame can't recover its reasoning.
1. Write two short sentences instead of joining clauses with a comma, a
   colon or an em dash. A form's own syntax keeps its colons, like
   `Feature:` or `End:`. Its titles, scenario names and checkpoint names
   carry none.
1. Use a table, an ordered list or a diagram for steps, comparisons and
   per-item detail.
1. A sentence that answers another doc's question moves there. The
   foundations' Where says which.
1. Something deferred lives only in its `deferred/` file.

**The cut**

Cut 25% of the prose. A pass counts when it does. Forms skip the cut,
since their caps hold their prose. Their titles, steps and Thens still
take the sentence rules.

**A choice put to the owner**

Letter each option A onward. Score each 1 to 5 in a column per criterion,
then total. Bold the top total as the pick.

**UI copy**

Write for the person at the screen. Use the users' words, never code names
or ids.
