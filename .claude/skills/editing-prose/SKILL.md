---
name: editing-prose
description: Use on every chat reply, and before finishing prose meant to last- docs, skills, tickets, retros, code comments, UI copy and command output
---

A chat reply runs step 2 alone.

1. **List each file the diff's prose touches, with its word count.**
1. **Fix each line until it passes the sentence rules**
   ([Editing prose](../../context-driven-development/design.md#feature-editing-prose)).
   - One fact per sentence. Write two short sentences, not one joined by a
     comma, a colon or an em dash. A form's own syntax keeps its colons.
   - Say what is, in present tense. History belongs in git. A why-comment
     is the exception.
   - Something deferred lives only in its `deferred/` file.
   - Use a table, an ordered list or a diagram for steps, comparisons and
     per-item detail.
   - UI copy uses the user's words, never code names or ids.
1. **Cut each file until it's 25% shorter.** Forms skip this step.
1. **Report each file's word count before and after.**
