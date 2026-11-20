# Context Driven Development — Architecture

How Context Driven Development is built, shaped around [design.md](design_document.md).

- [Shared](#shared)
  - [Stack](#stack)
  - [Where](#where)
  - [Testing strategy](#testing-strategy)
- [Checkpoints](#checkpoints)
- [Skills](#skills)
  - [Feature: Placing feedback](#feature-placing-feedback)
  - [Feature: Splitting the work](#feature-splitting-the-work)
  - [Feature: Signing off a change](#feature-signing-off-a-change)
  - [Feature: Running the playbook](#feature-running-the-playbook)
  - [Feature: Deciding a planning miss](#feature-deciding-a-planning-miss)
  - [Feature: Going red first](#feature-going-red-first)
- [Scripts](#scripts)
  - [Feature: Keeping each fact in its place](#feature-keeping-each-fact-in-its-place)
  - [Feature: Starting a doc from its template](#feature-starting-a-doc-from-its-template)
  - [Feature: Reading a doc by name](#feature-reading-a-doc-by-name)
  - [Feature: Claiming the next ticket](#feature-claiming-the-next-ticket)
  - [Feature: Merging a signed-off branch](#feature-merging-a-signed-off-branch)
- [Why](#why)

## Shared

### Stack

| Unit | Tech | Carries |
|---|---|---|
| Skills | Claude Code skills in Markdown | Workflow skills and the helpers they share |
| Scripts | Python under `uv`, run as one `cdd` command, tested with pytest | Keeping each fact in its place and Closing a phase |
| Git | Branches and tags | A claimed ticket and a plan's sign-off |
| Docs | Markdown, Gherkin and Mermaid | The design, the architecture, feedback, tickets, retros |

### Where

| Doc | Path |
|---|---|
| Foundations | `docs/foundations.md` |
| Design | `docs/design_document.md` |
| Architecture | `docs/architecture.md` |
| Roadmap | `docs/product_roadmap.md` |
| Deferred | `docs/deferred/`, a file per entry named for its title |
| Ticket | `docs/backlog/`, a file per ticket |
| Backlog README | `docs/backlog/README.md` |
| Feedback | `docs/feedback.md` |
| Release playbook | `docs/release/phase-{n}.md` |
| Retro | `docs/retro/{n}/` |
| Saved sessions | `docs/retro/raw/`, gitignored |
| Templates | `docs/templates/` |

- **A finished playbook** and **a taken-up deferred entry** are deleted by name. Git keeps them.
- **A plan's sign-off** is a git tag.[^why-a-plan-is-a-git-tag]
- **A claimed ticket** is its branch.

### Testing strategy

| Kind | Asserts | Prefix |
|---|---|---|
| Journey | Each workflow's End is the next workflow's Start | `journey_{journey}` |
| Workflow | Each step's outcome | `workflow_{workflow}` |
| Scenario | Its Then, one test for each Examples row | `scenario_{scenario}` |
| Rule | The fact across its scenarios, beyond what their Thens prove | `rule_{rule}` |
| Decision | Its sentence | `decision_{subject}` |

- **A test's name** runs its kind's prefix, then its source's title: `test_scenario_a_third_scenario_the_phase_s_goal_can_spare_waits`.
- **A test's kind** is the only part it asserts. Review moves a stray assertion.[^why-a-test-asserts-only-its-kind]
- **A known gap** sits in a baseline line with its reason, as does each workflow and scenario a skill runs. The check fails on a line whose reason is gone.[^why-a-known-gap-sits-in-a-baseline]

## Checkpoints

The owner reads this table against the design's journeys and names the
workflow to run next.

| Checkpoint | Evidence | Left by |
|---|---|---|
| New product | No design | — |
| Feedback in | An entry in `docs/feedback.md`. A blocker's opens with **Blocker** | Interviewing or Meeting the customer |
| Phase scoped | The roadmap's Now names phase n | Scoping a phase |
| Design signed off | `docs/retro/{n}/phase-design.md` holds a **Signed off** line | Designing a phase |
| Architecture signed off | `docs/retro/{n}/phase-architecture.md` holds a **Signed off** line | Architecting a phase |
| Plan signed off | Tag `phase-{n}-plan` or `phase-{n}-adhoc-{m}` | Writing the tickets or Planning ad hoc |
| Ready for review | A ticket's branch holding its retro entry | Working a ticket |
| Signed off | The ticket merged to main and gone from the backlog | Reviewing a ticket |
| Released | Every box checked in the phase's playbook | Releasing |
| Retro in | `docs/retro/{n}/retro.md` | Closing a phase |

## Skills

Placing feedback · Splitting the work · Signing off a change · Running the playbook · Deciding a planning miss · Going red first · Editing prose

- **A feature here** runs inside a workflow's skill.[^why-two-systems]
- **A workflow with steps to carry** runs on the skill of its name.[^why-one-skill-per-workflow]
- **A skill** holds its workflow's steps and the facts they act on. It names a doc by what it is and runs `cdd` to read, start or claim one. It names no path and no app's things, since every app runs it.[^why-a-skill-names-no-doc]
- **A helper** serves several workflows and carries no workflow's name.

### Feature: Placing feedback

- **An entry** takes any shape.[^why-feedback-lives-in-one-file]
- **A deferred entry** has a `Revisit when`.

### Feature: Splitting the work

- **A ticket** is a file from the ticket template.
- **A spike** is timeboxed to a ticket's cap in points.

### Feature: Signing off a change

- **A ticket's hand-off** says whether a user sees or does the change.
- **The reviewer** is a separate agent.[^why-a-separate-reviewer]
- **A deferred scenario** goes under **Past its caps** in the ticket's retro entry. Closing reads it there.

### Feature: Running the playbook

- **The playbook** opens each line with its system.
- **The deploy** runs through the team's own process. The playbook lists only the setup and checks each ticket's Release plan names.
- **A failed step's fix** goes into its system's section.

### Feature: Deciding a planning miss

- **A miss's kind** is each `Planning miss` in a retro entry, in a table column or a bullet's last line. A table counts only its severity rows.

### Feature: Going red first

- **The red rule** runs inside the ticket-working skill.[^why-red-runs-in-the-skill]

## Scripts

Keeping each fact in its place · Starting a doc from its template · Reading a doc by name · Claiming the next ticket · Merging a signed-off branch

- **Each script** runs as `uv run cdd <verb>`. `cdd` alone holds each doc's path, from Where.[^why-one-command]
- **`cdd check`** runs the checks, and `cdd check caps` the caps alone. A failure exits 1. A warning exits 0.
- **A baseline** is `scripts/{kind}-baseline.txt`, one per Testing strategy kind. A decision a scenario already covers sits in it with that scenario's name.
- **The session scripts** save the sessions before a merge, and `cdd mine {n}` mines a phase's at its close.

### Feature: Keeping each fact in its place

- **A form past its cap** warns. A form's cap is read from the Examples of the outline that warns, and a ticket's from the rules of Splitting the work and Signing off a change. A ticket's new scenarios are the titles its branch adds since its plan's tag, less those main gains from other tickets. A rename counts as new.[^why-a-cap-warns]
- **A system** lists each of its features on its opening line. A feature takes a heading only for its decisions.
- **A link** resolves to a file, and its anchor to a heading's GitHub slug. Naming one below means a link to it or a code file's path. Doc paths and tag formats pass.
- **A home** is found by name. A test matches its source by its prefix and title. A deferred thing matches its file's title. An architecture heading matches a design heading.[^why-a-test-s-name-says-its-kind-and-source]

### Feature: Starting a doc from its template

- **A doc's template** is the file in Templates with the doc's name.

### Feature: Reading a doc by name

- **A section** runs from its heading to the next heading of its level or higher. A heading in a fence opens none.
- **A doc kept as a file each** reads as each of its files in name order.

### Feature: Claiming the next ticket

- **A claim** is the push of the ticket's branch to origin, named as branching from main names it. The push that fails lost the race.

### Feature: Merging a signed-off branch

- **A merge** saves the sessions first. It cleans up only after main is pushed.

## Why

Why each decision that's hard to undo holds, and the options it beat.

[^why-a-test-s-name-says-its-kind-and-source]: The checks match each test to its source by name. A test that names no source fails. **Other considerations:** A tag or comment naming the source, which a rename leaves stale.

[^why-a-test-asserts-only-its-kind]: One test per fact means a change breaks one test. Review holds this rule. A check can't tell what an assertion proves. **Other considerations:** A design scenario per layer, which put a decision into the design.

[^why-a-known-gap-sits-in-a-baseline]: A line names the gap and why. A line whose reason is gone fails, so it leaves. A baseline that empties is deleted with the code that reads it. **Other considerations:** A doc's list of untested items, which keeps two lists of one thing. A check that skips what a skill runs, which hides the gap. A check that fails until a skill is tested, which never passes.

[^why-a-plan-is-a-git-tag]: A tag marks the exact plan. The retro diffs what shipped against it. Every other checkpoint already shows in a file. **Other considerations:** A tag at every stage. A signed-off line in the plan's docs, which a later edit can carry along unseen. The plan's merge commit found by its message, which breaks on a reworded message.

[^why-one-skill-per-workflow]: Each step of a workflow has one role. A fresh session loads one skill. Talking with the customer and writing it down needs none. **Other considerations:** A skill for every workflow, which wraps two plain steps in a file to load. One skill playing five workflows, which hid which skill ran a step.

[^why-a-skill-names-no-doc]: A fresh session reads one file and acts. A doc that moves changes `cdd` alone, not each skill. A skill's steps may part from its workflow's where practice teaches better. The retros catch the skill steps an agent skipped. **Other considerations:** A skill naming each doc's path, which every move edits. A skill naming its product's things, which serves one app alone. Each step linking to the design's step, which costs a second read. A check that a skill copies its workflow's steps, which proves the words and not the work.


[^why-two-systems]: A system says what its features run on. A Developer then knows whether to open a skill or a script. **Other considerations:** One system, which says nothing. Plan and Build, or Planning, Delivery and Checks, which leave Keeping each fact in its place between two.

[^why-a-cap-warns]: A cap is soft. The owner may keep a form past it, as the phase journey keeps 9 workflows. A failing check would stand for good. The checks count each form alike. One count serves every skill. **Other considerations:** A check that fails, which the phase journey would fail forever. The owner's call is a choice. Each skill counting by reading, which repeats the count in every skill.

[^why-a-separate-reviewer]: An agent reads its own work with the reasoning that wrote it. It misses what that reasoning missed. **Other considerations:** The building agent reviewing itself, which is cheaper and sees less.

[^why-red-runs-in-the-skill]: No check can see a test's first run. **Other considerations:** A check over the test files' history, which can't tell a failing assertion from a compile error.

[^why-feedback-lives-in-one-file]: Scoping empties it. Any entry left is feedback. A meeting pastes in as written. **Other considerations:** A file per meeting, which each shrinks apart. A file per phase, where feedback written in one phase belongs to the next.

[^why-one-command]: A skill names a verb, and the folders can move under it. **Other considerations:** A script path in each skill, which a move breaks. A Makefile, which needs make in Pi too.
