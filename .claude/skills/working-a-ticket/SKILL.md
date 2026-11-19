---
name: working-a-ticket
description: Use when picking up and implementing a backlog ticket, from claim through handoff to the owner
---

# Working a ticket

Start: **Plan signed off**. End: **Ready for review**.

1. **Claim the next open ticket on its own branch, and read the sections
   it names.**
   - Suggest `/clear` after other work.
   - Pick the earliest group in `docs/backlog/README.md` with an open
     ticket, one with no branch or worktree of its name in
     `git branch -a` or `git worktree list`. A group's tickets can run in
     separate chats.
   - Invoke `branching-from-main` for the ticket's branch.
   - Stop for the owner's review, unless the args say to go on. Give the
     Estimate's model, a Remote Control reminder, the wireframes, and the
     acceptance criteria with the ticket's link.
   - Read a small doc whole. Otherwise `grep -n` it and `sed -n` the
     matches.
   - The phase's goal, under **Now** in `docs/product_roadmap.md`.
   - The design's workflows and features the ticket names, and the
     architecture's **Testing strategy** and its **System**'s Rules.
   - The one or two latest `docs/retro/{phase}/` entries.
   - The **Release rules** atop `docs/release/phase-{n}.md`. They win over
     the ticket's Release plan.
   - If the approach is unclear, invoke `superpowers:brainstorming`.
1. **Write each of the ticket's tests until it fails
   on its assertion.**
   - Invoke `superpowers:test-driven-development`. The Gherkin is the spec.
     Each test asserts only its kind's part, per the Testing strategy.
   - Stub anything new first. A test over built code goes red against a
     revert.
1. **Add each case the tests find to the design as a row or a new
   scenario.**
   - Write it into its scenario's Examples or the design, then any
     decision it changes. A new feature or workflow is a ticket, per
     `planning-ad-hoc`.
   - Count the ticket's new scenarios by hand. A third goes to the owner. One the phase's goal needs redesigns the
     ticket. One it can spare goes under **Past its caps** in the retro
     entry.
   - A case a rule covers becomes a proposed rule in the ticket's Gherkin,
     its test `rule_` plus the rule's title. A rule for every feature of
     the system is proposed for its Rules.
   - Merge up the chain. Fold rules into a broader rule, a rule into the
     scenario whose outcome proves it, a scenario into the step that walks
     it. Record each in the ticket's Gherkin with what it replaces.
1. **Write the code until each test passes.**
   For a page change, run the app locally and screenshot it.
1. **Update each doc the change touches.**
   - Fold the Release plan into `docs/release/phase-{n}.md` per the
     playbook template. Add its lines unchecked. `releasing` checks them
     after the branch merges.
   - Edit `docs/architecture.md` where a decision changed.
   - Write the retro entry, per `writing-a-retro-entry`, with its
     **Deviations from the plan and design**.
   - Run `editing-prose` over the branch's prose.
1. **Run the checks until they pass.**
   - Run `uv run --script scripts/check.py` once, in the background. After a fix,
     run only the tests it touched.
   - Check by hand that each doc names only docs above it, per `CLAUDE.md`.
1. **Another Developer reviews the change.**
   - Invoke `superpowers:requesting-code-review` over the branch. Ask the
     reviewer whether:
     - each new or changed test asserts only its kind's part
     - a rule or design change would fold each case
     - rules merge, a rule is a scenario's outcome, or a scenario is a
       workflow's step
     - `editing-prose`'s cut ran, and each changed line follows its
       sentence rules
   - Fix Critical and Important findings. Record every finding in the
     retro's **Code review**.
1. **Hand off to the Product Owner.**
   - Push and run `gh pr create --base main --title "{ticket} — {title}" --body ""`.
   - Give in chat:
     - What shipped, in one line, with the PR's link.
     - Whether a user or the team sees or does the change. If none
       does, the code review signs it off.
     - For a page change, the sign-off link and screenshots from
       the app run locally.
     - The steps to walk the change, one click each.
     - The tests added, by kind.
     - Each case, merge and redesign, for the owner's call.
     - Each proposed rule and the tests it folds, to accept, reword or
       refuse.
     - What waits on the owner.
   - Send `PushNotification` with the ticket and "ready for review".
   - Invoke `reviewing-a-ticket`.
