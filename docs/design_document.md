# Context Driven Development — Design

Read [foundations.md](foundations.md) first.
- [Context Driven Development — Design](#context-driven-development--design)
  - [Checkpoints](#checkpoints)
  - [Journey: A phase from feedback to retro](#journey-a-phase-from-feedback-to-retro)
  - [Journey: New scope and ad hoc plan from feedback to release](#journey-new-scope-and-ad-hoc-plan-from-feedback-to-release)
  - [Workflow: Interviewing the customer](#workflow-interviewing-the-customer)
  - [Workflow: Meeting the customer](#workflow-meeting-the-customer)
  - [Workflow: Scoping a phase](#workflow-scoping-a-phase)
  - [Workflow: Designing a phase](#workflow-designing-a-phase)
  - [Workflow: Architecting a phase](#workflow-architecting-a-phase)
  - [Workflow: Writing the tickets](#workflow-writing-the-tickets)
  - [Workflow: Working a ticket](#workflow-working-a-ticket)
  - [Workflow: Reviewing a ticket](#workflow-reviewing-a-ticket)
  - [Workflow: Releasing](#workflow-releasing)
  - [Workflow: Closing a phase](#workflow-closing-a-phase)
  - [Workflow: Planning ad hoc](#workflow-planning-ad-hoc)
  - [Features](#features)
    - [Feature: Placing feedback](#feature-placing-feedback)
    - [Feature: Keeping each fact in its place](#feature-keeping-each-fact-in-its-place)
    - [Feature: Splitting the work](#feature-splitting-the-work)
    - [Feature: Going red first](#feature-going-red-first)
    - [Feature: Signing off a change](#feature-signing-off-a-change)
    - [Feature: Running the playbook](#feature-running-the-playbook)
    - [Feature: Deciding a planning miss](#feature-deciding-a-planning-miss)
    - [Feature: Editing prose](#feature-editing-prose)
    - [Feature: Starting a doc from its template](#feature-starting-a-doc-from-its-template)
    - [Feature: Reading a doc by name](#feature-reading-a-doc-by-name)
    - [Feature: Claiming the next ticket](#feature-claiming-the-next-ticket)
    - [Feature: Merging a signed-off branch](#feature-merging-a-signed-off-branch)


## Checkpoints

| Checkpoint | Lives in |
|---|---|
| New product | An empty repo |
| Feedback in | The feedback in any shape. Scoping a phase places each entry |
| Phase scoped | The roadmap |
| Design signed off | The design |
| Architecture signed off | The architecture |
| Plan signed off | A git tag over a phase's plan or an ad hoc plan |
| Ready for review | The ticket and its branch |
| Signed off | Main |
| Released | The release playbook |
| Retro in | A retro |

## Journey: A phase from feedback to retro

Start: **New product** or **Released**

| # | Workflow | Role | Leaves |
|---|---|---|---|
| 1 | [Interviewing the customer](#workflow-interviewing-the-customer) or [Meeting the customer](#workflow-meeting-the-customer) | Product Owner | **Feedback in** |
| 2 | [Scoping a phase](#workflow-scoping-a-phase) | Product Owner | **Phase scoped** |
| 3 | [Designing a phase](#workflow-designing-a-phase) | Designer | **Design signed off** |
| 4 | [Architecting a phase](#workflow-architecting-a-phase) | Developer | **Architecture signed off** |
| 5 | [Writing the tickets](#workflow-writing-the-tickets) | Developer and Product Owner | **Plan signed off** |
| 6 | [Working a ticket](#workflow-working-a-ticket) | Developer | **Ready for review** |
| 7 | [Reviewing a ticket](#workflow-reviewing-a-ticket) | Developer, with the Product Owner and Designer when users see the change | **Signed off** |
| 8 | [Releasing](#workflow-releasing) | Developer | **Released** |
| 9 | [Closing a phase](#workflow-closing-a-phase) | Every role | **Retro in** |

End: **Retro in**

Interviewing the customer starts from **New product**. Meeting the customer
starts from **Released**. Steps 6 and 7 repeat for each ticket in the
backlog README's order. Step 8 runs once per ticket or once for the phase,
as the Product Owner and Developer decide.

## Journey: New scope and ad hoc plan from feedback to release

An ad hoc plan that adds scope to the open phase.

Start: **Feedback in** that adds scope to the open phase

| # | Workflow | Role | Leaves |
|---|---|---|---|
| 1 | [Planning ad hoc](#workflow-planning-ad-hoc) | Developer and Product Owner, with the Designer for a screen | **Plan signed off** |
| 2 | [Working a ticket](#workflow-working-a-ticket) | Developer | **Ready for review** |
| 3 | [Reviewing a ticket](#workflow-reviewing-a-ticket) | Developer, with the Product Owner and Designer when users see the change | **Signed off** |
| 4 | [Releasing](#workflow-releasing) | Developer | **Released** |

End: **Released**

Step 1 follows the phase journey's order in one sitting. The design comes
first, then the architecture, then the plan's tickets. It runs on one
branch with one sign-off. Steps 2 and 3 repeat for each ticket. Step 4
ships the merged tickets. The plan's retro entry waits for
the open phase's close.

## Workflow: Interviewing the customer

Responsible: Product Owner

Start: **New product**

1. Ask the customer who, what, when, where, why and how until each has an answer
1. Write the answers into the feedback

End: **Feedback in**

## Workflow: Meeting the customer

Responsible: Product Owner · Weekly or every other week

Start: **Released**

1. Demo each change that shipped until the customer has seen it
1. Write what the customer says into the feedback

End: **Feedback in**

## Workflow: Scoping a phase

Responsible: Product Owner

Start: **Feedback in** and **Retro in**

1. Read the feedback and the last retro's action items and each deferred entry whose `Revisit when` now holds
1. Place each entry until the feedback is empty ([Placing feedback](#feature-placing-feedback))
1. Replace the goal in the roadmap's Now with this phase's goal from the action items and the entries taken up

End: **Phase scoped**

## Workflow: Designing a phase

Responsible: Designer · Accountable: Product Owner

Start: **Phase scoped**

1. Brainstorm with the Product Owner until a design meets the phase's goal ([Reading a doc by name](#feature-reading-a-doc-by-name))
1. Edit the foundations the goal changes with the Product Owner
1. Edit the journeys the goal changes
1. Edit the workflows the goal changes and the checkpoints they start and end at
1. Name each branch of a changed step as a scenario and group them into features by shared context. Titles only
1. Write each scenario's Gherkin and each feature's rules with the Product Owner ([Keeping each fact in its place](#feature-keeping-each-fact-in-its-place))
1. Wireframe each screen a feature changes with its copy
1. Write the design pass's retro entry and sign off the design with the Product Owner ([Editing prose](#feature-editing-prose))

End: **Design signed off**

## Workflow: Architecting a phase

Responsible: Developer · Accountable: Product Owner

Start: **Design signed off**

1. Brainstorm with the Product Owner until a build meets the design's changes and the phase's goal ([Reading a doc by name](#feature-reading-a-doc-by-name))
1. Edit the architecture's base the design changes
1. Place each new feature under the system it runs on. Name a new system where none fits
1. Write the decisions each changed workflow and feature needs, under a heading of its own name ([Keeping each fact in its place](#feature-keeping-each-fact-in-its-place))
1. Give each decision that's hard to undo a why. Name the options it beat
1. Write the architecture pass's retro entry and sign off the architecture with the Product Owner ([Editing prose](#feature-editing-prose))

End: **Architecture signed off**

## Workflow: Writing the tickets

Responsible: Developer · Accountable: Product Owner

Start: **Architecture signed off**

1. Split the planned work into tickets. Each names its scenarios and the workflow steps it builds ([Splitting the work](#feature-splitting-the-work))
1. Check each scenario for how a bug could break it ([Signing off a change](#feature-signing-off-a-change))
1. Check that a ticket carries each model attribute the architecture adds ([Keeping each fact in its place](#feature-keeping-each-fact-in-its-place))
1. Order the tickets in the backlog README with their parallel groups
1. Write the release playbook in run order ([Starting a doc from its template](#feature-starting-a-doc-from-its-template))
1. Write the ticket pass's retro entry and sign off the plan with the Product Owner. Merge it to main ([Editing prose](#feature-editing-prose))

End: **Plan signed off**

## Workflow: Working a ticket

Responsible: Developer

Start: **Plan signed off**

1. Claim the next open ticket in the backlog README on its own branch, and read the phase's goal in the roadmap and the design and architecture sections it names ([Claiming the next ticket](#feature-claiming-the-next-ticket))
1. Write each of the ticket's tests until it fails on its assertion ([Going red first](#feature-going-red-first))
1. Add each case the tests find to the design as a row or a new scenario ([Signing off a change](#feature-signing-off-a-change))
1. Write the code until each test passes
1. Add the ticket's lines to the release playbook and write its retro entry. Update any other docs the change touches ([Editing prose](#feature-editing-prose))
1. Run the checks until they pass ([Keeping each fact in its place](#feature-keeping-each-fact-in-its-place))
1. Another Developer reviews the change and the Developer fixes what it finds. Its findings join the ticket's retro entry ([Editing prose](#feature-editing-prose))
1. Hand off what shipped to the Product Owner with how to walk it and what waits on them

End: **Ready for review**

## Workflow: Reviewing a ticket

Responsible: Developer · Accountable: Product Owner

Start: **Ready for review**

1. Walk the change ([Signing off a change](#feature-signing-off-a-change))
1. Restate each piece of feedback as a new scenario or row in the design, and fix it in a review pass ([Signing off a change](#feature-signing-off-a-change))
1. Sign off the change ([Signing off a change](#feature-signing-off-a-change))
1. Merge to main and delete the ticket ([Merging a signed-off branch](#feature-merging-a-signed-off-branch))

End: **Signed off**

## Workflow: Releasing

Responsible: Developer · Accountable: Product Owner

Start: **Signed off**

1. Run each stage's steps in the release playbook in order. Check each box as it verifies ([Running the playbook](#feature-running-the-playbook))
1. At each sign-off the playbook names, the Product Owner walks each merged ticket and says yes
1. Write the release's retro entry

End: **Released**

## Workflow: Closing a phase

Responsible: Developer · Accountable: Product Owner

Start: **Released**

1. Gather each role's feedback on the phase with the Product Owner's read first
1. Read every retro entry in the phase
1. Diff what shipped against the phase's tag and each ad hoc plan's tag
1. Mine the agents' sessions for their cost and time and the skill steps they skipped
1. Walk every planning miss with the Product Owner grouped by kind, each scenario past its caps among them ([Deciding a planning miss](#feature-deciding-a-planning-miss))
1. Write the retro ([Editing prose](#feature-editing-prose))

End: **Retro in**

## Workflow: Planning ad hoc

Responsible: Developer · Accountable: Product Owner

Start: **Feedback in** that adds scope to the open phase

1. Open the plan's branch off main. An entry it takes up leaves the feedback
1. Edit the design as Designing a phase does. The Designer joins for a screen
1. Edit the architecture as Architecting a phase does
1. Write the plan's tickets as Writing the tickets does
1. Put the tickets at the head of the backlog README and their steps in the release playbook
1. Write the plan's retro entry with the scope and the planning miss behind it ([Editing prose](#feature-editing-prose))
1. Sign off the plan with the Product Owner. Merge it to main

End: **Plan signed off**

## Features

A scenario is one way a workflow step can go. A step with one outcome
states it and takes no scenario.

### Feature: Placing feedback

```gherkin
Feature: Placing feedback
  The feedback from when it's written until scoping places each entry.

  Scenario: New scope the Product Owner wants starts an ad hoc plan
    Given a phase is open
    When the Product Owner wants more scope
    Then it starts an ad hoc plan right away

  Scenario: A blocker starts an ad hoc plan
    Given a phase is open
    When a blocker stops work or loses data
    Then it starts an ad hoc plan right away

  Scenario: An entry the goal fits is taken up
    Given the Product Owner is scoping a phase
    When an entry fits the phase's goal
    Then the goal takes it up
    And it leaves the feedback

  Scenario: A deferred entry the goal fits is taken up
    Given the Product Owner is scoping a phase
    When a deferred entry's `Revisit when` holds and it fits the phase's goal
    Then the goal takes it up
    And its file in `deferred/` is deleted

  Scenario: An entry that can wait is deferred
    Given the Product Owner is scoping a phase
    When an entry can wait past this phase
    Then it gets its own file in `deferred/` with when to revisit it

  Scenario: An entry that no longer holds is dropped
    Given the Product Owner is scoping a phase
    When an entry no longer holds
    Then git alone keeps it
```

### Feature: Keeping each fact in its place

```gherkin
Feature: Keeping each fact in its place
  Each fact holds its place down the stream.

  Rule: Each part has its home

    Scenario Outline: A part with no home fails the check
      Given <part> with no <home>
      When the Developer runs the checks
      Then the checks fail on the part

      Examples:
        | part                                | home                                      |
        | a rule                              | two scenarios under it                    |
        | a journey                           | test named for it                         |
        | a workflow                          | test named for it                         |
        | a scenario                          | test named for it                         |
        | a rule                              | test named for it                         |
        | a test                              | source it names                           |
        | a deferred entry                    | `Revisit when` line                       |

    Scenario: A deferred thing described outside its file fails
      Given a doc other than its deferred/ file describes a deferred thing
      When the Developer runs the checks
      Then the checks fail on that line

  Rule: A doc names only what's above it

    Scenario Outline: A file that names one it may not fails the check
      Given <file> names a doc other than the foundations or <may>
      When the Developer runs the checks
      Then the checks fail on that line

      Examples:
        | file                 | may                                                   |
        | the design           | nothing                                               |
        | the architecture     | the design                                            |
        | the code             | nothing                                               |
        | the roadmap          | nothing                                               |
        | a deferred entry     | the design                                            |
        | the backlog README   | its own tickets                                       |
        | the release playbook | the tickets and the architecture's systems            |

    Scenario: An architecture heading with no design heading fails the check
      Given the architecture heads decisions with a workflow or feature the design doesn't have
      When the Developer runs the checks
      Then the checks fail on the heading

    Scenario: A design feature no system lists fails the check
      Given a design feature that sits on no system's opening line in the architecture
      When the Developer runs the checks
      Then the checks fail on the feature

  Rule: Every link resolves

    Scenario: A link to a missing file fails the check
      Given a doc links to a file that doesn't exist
      When the Developer runs the checks
      Then the checks fail on the link

    Scenario: A link to a missing heading fails the check
      Given a doc links to an anchor no heading in its file makes
      When the Developer runs the checks
      Then the checks fail on the link

  Rule: Each form stays under its cap

    Scenario: An outline under three rows warns
      Given a scenario outline with two Examples rows
      When the Developer runs the checks
      Then the checks warn
      And the owner decides whether to split it into scenarios

    Scenario Outline: One more than the cap warns
      Given a <doc> at its cap of <cap>
      When one more is added
      Then the checks warn
      And the owner decides whether to redesign <upstream>

      Examples:
        | form                 | cap                    | upstream              |
        | journey              | 7 workflows            | the journey           |
        | workflow             | 8 steps                | its journey           |
        | workflow step        | 1 feature              | the step              |
        | feature              | 8 scenarios or 4 rules | its workflows         |
        | architecture section | 4 decisions            | its feature or system |
```

### Feature: Splitting the work

```gherkin
Feature: Splitting the work
  One ticket to build and what it carries.

  Scenario: An unverified outside system gets a spike first
    Given an outside system whose behaviour is unverified
    When the Developer writes the tickets
    Then a spike comes before the tickets that need it

  Scenario: A prerequisite with no screen gets a ticket first
    Given a prerequisite with no screen
    When the Developer writes the tickets
    Then its ticket comes before the tickets that need it

  Scenario: A workflow whose steps name no feature of its system gets a ticket of its steps
    Given a changed workflow whose steps name no feature in the system its skill runs on
    When the Developer writes the tickets
    Then it gets a ticket of its steps with no scenarios

  Scenario: A spike's finding updates the plan
    Given a spike over an outside system
    When the Developer finishes it
    Then its finding goes into the design or the architecture
    And the tickets that need it name that section

  Rule: A ticket is at most one feature on one system and 5 points

    Scenario: A feature past 5 points splits by scenario
      Given a feature's changed scenarios estimated past 5 points
      When the Developer writes the tickets
      Then they split by scenario into tickets of 5 points or less

    Scenario: A single scenario past 5 points goes to the owner
      Given one scenario estimated past 5 points
      When the Developer writes the tickets
      Then the owner decides how to split it

    Scenario: A feature across two systems splits by system
      Given a feature's changed scenarios touch two systems
      When the Developer writes the tickets
      Then they split into a ticket per system

    Scenario: A scenario that needs another ticket built first gets its own ticket
      Given a feature's scenario can't be built until another ticket is done
      When the Developer writes the tickets
      Then that scenario gets its own ticket, ordered after the ticket it needs
      And the feature's other scenarios don't wait for it
```

### Feature: Going red first

```gherkin
Feature: Going red first
  A ticket's tests go red before its code.

  Rule: Every test is written failing before the code

    Scenario Outline: A test that doesn't fail on its assertion is not yet red
      Given a new or changed test that <runs> before the code
      When the Developer <acts>
      Then it fails on the assertion it names
      And the Developer writes the code

      Examples:
        | runs                           | acts                              |
        | passes over code already built | reverts that code, then undoes it |
        | passes                         | fixes the test                    |
        | stops on a compile error       | stubs what's missing              |
        | stops on a missing module      | stubs the module                  |
        | stops on a missing install     | installs it                       |
```

### Feature: Signing off a change

```gherkin
Feature: Signing off a change
  Who walks a ticket, what it takes on, and who signs it off.

  Scenario Outline: A way a bug could break a scenario joins the design
    Given a scenario that could break when <it>
    When the Developer writes the tickets
    Then the design gains a row or a scenario for that case

    Examples:
      | it                    |
      | runs again            |
      | is undone or redone   |
      | meets a locked step   |
      | gets bad input        |

  Scenario: A change a user sees or does is signed off by the Product Owner
    Given a ticket that changes what a user sees or does
    And another Developer has reviewed it
    When the Developer walks the change
    Then the Product Owner and Designer walk it too
    And the Product Owner signs it off
    And another Developer reviews the feedback rounds' changes at sign-off

  Scenario: A change no user sees or does signs off at review
    Given a ticket that changes nothing a user sees or does
    When another Developer reviews it
    And the Developer fixes what the review finds
    Then the review signs it off

  Rule: A ticket takes two new scenarios at most

    Scenario: A new Examples row joins the design
      Given a ticket that has added two new scenarios in building or review
      When an Examples row on one of its scenarios is found
      Then it joins the design and the ticket's tests cover it

    Scenario: A new rule joins the design
      Given a ticket that has added two new scenarios in building or review
      When a rule across two of its scenarios is found
      Then it joins the design and the ticket's tests cover it

    Scenario: A third scenario the phase's goal needs redesigns the ticket
      Given a ticket that has added two new scenarios in building or review
      When a third scenario the phase's goal needs is found
      Then the ticket is redesigned in place

    Scenario: A third scenario the phase's goal can spare waits
      Given a ticket that has added two new scenarios in building or review
      When a third scenario the phase's goal can spare is found
      Then it goes to the ticket's retro
      And the ticket signs off with the two
```

### Feature: Running the playbook

```gherkin
Feature: Running the playbook
  The playbook from the first stage to the last.

  Scenario: Running the playbook again starts at the first unchecked box
    Given a playbook with boxes checked in an earlier sitting
    And no ticket has merged since
    When the Developer runs it again
    Then it starts at the first unchecked box

  Scenario: Running the playbook after a merge starts at the ticket's lines
    Given a playbook with boxes checked in an earlier sitting
    And a ticket merged and added its lines since
    When the Developer runs it again
    Then it starts at the ticket's first new line

  Scenario: A failed step the Developer fixes
    Given a step that fails its check
    When the Developer fixes it and the step verifies
    Then the run goes on from that step
    And the fix is written into the architecture

  Scenario: A failed step the Product Owner skips
    Given a step that fails its check
    When the Product Owner skips it
    Then the release's retro entry names the step and why and what stood in for it
```

### Feature: Deciding a planning miss

```gherkin
Feature: Deciding a planning miss
  The Product Owner decides each planning miss at the phase's close.

  Background:
    Given the Product Owner walks the phase's planning misses

  Scenario: A miss the next phase must fix becomes an action item
    When a miss needs fixing in the next phase
    Then it becomes an action item in the retro

  Scenario: A miss that can wait is deferred
    When a miss can wait past the next phase
    Then it gets its own file in `deferred/` with when to revisit it

  Scenario: A miss that no longer holds stays in its retro entry
    When a miss no longer holds
    Then it stays only in its ticket's retro entry

  Scenario: A kind seen once is proposed to stay in its entry
    When a miss's kind shows up once in the phase
    Then its proposed call is to stay in its entry
    And the Product Owner may choose another

  Scenario: A kind seen twice or more is proposed as an action item
    When a miss's kind shows up in two tickets or more
    Then its proposed call is an action item
    And the Product Owner may choose another
```

### Feature: Editing prose

```gherkin
Feature: Editing prose
  Prose a person or an agent writes, before someone reads it.

  Scenario: Prose is cut by a quarter
    Given a diff that changes prose
    When its writer edits it
    Then each file is 25% shorter
    And the hand-off gives each file's word count before and after

  Scenario: A form takes the sentence rules alone
    Given a diff that changes a form
    When its writer edits it
    Then its titles, steps and Thens follow the sentence rules
    And its length stays

  Scenario: The owner keeps a cut short of a quarter
    Given a cut that falls short of 25%
    When the owner keeps it
    Then the retro entry names the file and its cut

  Scenario: Review finds a line that breaks a sentence rule
    Given a change whose writer has edited its prose
    When another Developer reviews it
    Then each line that breaks a sentence rule is a finding
```

### Feature: Starting a doc from its template

```gherkin
Feature: Starting a doc from its template
  A user names the doc and its name. The command knows where its template and its place are.

  Scenario Outline: A new doc lands in its place from its template
    Given the <doc> has a template
    When a user starts <name>
    Then the doc is the template, at <place>
    And the command prints its path

    Examples:
      | doc              | name                 | place                                  |
      | ticket           | 001-010-foo          | the backlog, as 001-010-foo.md         |
      | retro entry      | phase 1, phase-design | phase 1's retro, as phase-design.md   |
      | release playbook | phase 1              | the release folder, as phase-1.md      |
      | foundations      | garden               | garden's foundations.md                |

  Scenario: A doc that already exists stays as it is
    Given that doc already exists
    When a user starts it again
    Then the command fails and the doc is unchanged

  Scenario: A doc with no template fails
    Given a doc name that has no template
    When a user starts one
    Then the command fails and lists the docs that have one
```

### Feature: Reading a doc by name

```gherkin
Feature: Reading a doc by name
  A user reads part of a doc by what the doc is and the heading it wants.

  Scenario Outline: A doc prints as much as a user names
    Given <names>
    When a user reads it
    Then the command prints <prints>

    Examples:
      | names                                   | prints                          |
      | a doc and one of its headings           | that heading's section and no more |
      | a doc and no heading                    | the whole doc                   |
      | a doc kept as a file each, and a phase  | each of that phase's files whole |

  Scenario: A heading inside a gherkin fence is no section
    Given a heading that sits only inside a gherkin fence
    When a user reads it
    Then the command fails and lists the doc's headings

  Scenario: A heading the doc lacks fails
    Given a heading the doc doesn't have
    When a user reads it
    Then the command fails and lists the doc's headings

  Scenario: A doc name with no place fails
    Given a doc name the Where table doesn't hold
    When a user reads it
    Then the command fails and lists the names it holds
```

### Feature: Claiming the next ticket

```gherkin
Feature: Claiming the next ticket
  The next ticket is the first open one in the backlog README.

  Scenario: The first open ticket whose waits are done is next
    Given a group whose tickets wait on nothing still in the backlog
    When the Developer asks for the next ticket
    Then the command names the first ticket in it with no branch on origin

  Scenario: A ticket claimed meanwhile can't be claimed twice
    Given a ticket whose branch reached origin after it was named
    When the Developer claims it
    Then the claim fails and names the next open ticket

  Scenario Outline: Each kind of branch is claimed by its name
    Given a <kind> with no branch on origin
    When the Developer claims it
    Then origin holds <branch> and its worktree is open

    Examples:
      | kind          | branch                       |
      | ticket        | feature/001-004-foo          |
      | phase's plan  | design/phase-2               |
      | ad hoc plan   | adhoc/001-004-foo            |
      | chore         | chore/foo                    |

  Scenario: A branch already in this checkout is reused
    Given the branch exists here and on origin, claimed by this Developer
    When the Developer claims it again
    Then the command opens its worktree and pushes nothing

  Scenario: No open ticket says so
    Given every ticket in the backlog is claimed or waits
    When the Developer asks for the next ticket
    Then the command says none is open and what each waits on
```

### Feature: Merging a signed-off branch

```gherkin
Feature: Merging a signed-off branch
  The merge carries the work to main and clears what the branch left.

  Scenario: A clean merge clears the branch
    Given a signed-off branch that merges clean
    When the Developer merges it
    Then main holds it with the branch's name and title in the message
    And its sessions are saved and its ticket, worktree and branches are gone

  Scenario: A plan or chore merges with no ticket to delete
    Given a signed-off plan or chore branch
    When the Developer merges it
    Then main holds it and nothing in the backlog is deleted

  Scenario: A rejected push keeps the branch
    Given main on origin moved after the merge began
    When the push is rejected
    Then the worktree and branches stay
    And the command says to merge again

  Scenario: A rerun finishes a partial merge
    Given main on origin holds the merge but the branches remain
    When the Developer merges again
    Then the command clears what remains and merges nothing twice

  Scenario: A conflict stops the merge
    Given a signed-off branch that conflicts with main
    When the Developer merges it
    Then nothing merges and the worktree and branches stay
    And the command names the conflicting files
```
