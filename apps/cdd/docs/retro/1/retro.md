# Phase 1 — retro

Themes pulled from the phase's retro entries in `apps/cdd/docs/retro/1/`,
and what changes because of them.

## What went well

- The owner likes the new structure. Forms, apps and `cdd` each have one home.
- The essay drew good feedback from readers.
- Every ticket shipped with its code review fixed before sign-off.

## What could improve

- Reviews kept finding failure cases no doc had named. Git failures, races, dirty checkouts and bad input came up in five tickets and the ad hoc plan.
- Four chores landed on main with no plan and no retro entry.
- The miner reports 5 of 11 tickets. Its cost and estimate numbers don't hold this phase.

## Planning misses

| Kind | Miss | Entry | Call |
|---|---|---|---|
| the ticket | Failure cases unnamed: git failures, races, dirty checkouts, a path leaving its folder | 001-004, 001-006, 001-007, 001-008, 001-011 | Action item |
| `design_document.md` | Scenarios missing for unhappy paths and other kinds | adhoc-001-004-001-010, 001-001, 001-008, phase-tickets | Action item |
| `architecture.md` | A decision packed several facts | 001-004, 001-005, 001-011 | Dropped. The decision-cases chore fixed it |
| the ticket template | A criterion restated its decision | 001-004 | Dropped. The template has a Decision row |
| `product_roadmap.md` | Pi scoped before its spike | 001-002 | Dropped. Seen once |
| Tests | A miscounted total | 001-002 | Dropped. Seen once |
| Past its caps | Skills holds 7 decisions, past 4 | 001-008, 001-011 | Deferred |
| Past its caps | The phase journey holds 9 workflows, past 7 | 001-001 | Deferred |
| Past its caps | Where holds 5 decisions, past 4 | 001-010 | Dropped. The essay's old address goes once its links die |
| Past its caps | Keeping each fact in its place holds 9 scenarios, past 8 | 001-001 | Dropped. Seen once |
| No plan | Four chores landed with no entry | chore-* | Action item |
| Tests | The miner drops sessions on `main`, reads no points and counts no prompts | this close | Action item |

## Action items

- [ ] Fix the miner. It counts sessions recorded on `main`, reads each ticket's points and counts the owner's prompts. Lands in `apps/cdd/scripts/mine-transcripts.py`.
- [ ] Keep tickets until the close. A merge drops only the ticket's README row, and closing a phase deletes the files. Lands in `cdd merge`, merging-to-main and closing-a-phase.
- [ ] Name failure cases upstream. The design and ticket passes list each feature's failure cases before sign-off. Lands in designing-a-phase and writing-the-tickets.
- [ ] A chore runs plan, deliver and learn. planning-ad-hoc takes a chore with no tickets, working-a-ticket runs it, and it gets a retro entry.
