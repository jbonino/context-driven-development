---
name: reviewing-a-ticket
description: Use when a ticket's work is ready for the owner, from the hand-off through feedback rounds, sign-off and the merge
---

# Reviewing a ticket

Start: **Ready for review**. End: **Signed off**. The goal is zero rounds.

1. **Walk the change.**
   - Give the prompt for a new chat:
     `/reviewing-a-ticket {ticket} {worktree absolute path}`. It reads the
     ticket, its retro, its PR, and `git diff --stat main...`.
   - When a user or the team sees or does the change, the owner and
     the Designer walk it on the sign-off link. Otherwise the code review
     signs it off. Go to step 3.
1. **Restate each piece of feedback in the design, and fix it in a review
   pass.** Each round:
   1. From the third round, give the new chat's prompt again.
   1. Restate the feedback as a row, a new scenario, or a verdict on a
      proposed rule. Say whether it changes a criterion, and wait for a
      yes. Past two new scenarios, Signing off a change's rule decides.
   1. Write it into the design, then any decision it changes, and a
      changed criterion into the ticket. An accepted rule takes a
      footnote. Rename a reworded one's test by hand. A refused one's test
      goes.
   1. Write its failing test first, per `superpowers:test-driven-development`,
      except for copy or style. Run only the tests you touched.
   1. For a page change, run the app locally and screenshot it.
   1. Add the change to the retro's **Changed after sign-off**. Commit it
      as `{ticket} — round N: {what changed}`, push, and give
      `https://github.com/{owner}/{repo}/compare/{last sha}...{branch}`.
      Stop.
1. **Sign off the change** when the owner says "sign off", or from step 1.
   Ask the owner's verdict on each open proposed rule and write it per
   step 2. If any round ran, invoke `superpowers:requesting-code-review`
   over the rounds. Fix Critical and Important findings and record each in
   the retro's **Sign-off review**. Run the checks until they
   pass. With no rounds, `working-a-ticket`'s run covers it.
1. **Merge to main and delete the ticket.** `git rm` the ticket. A scenario
   whose test waits, such as a skill's, goes in the retro entry. Invoke
   `merging-to-main`.
